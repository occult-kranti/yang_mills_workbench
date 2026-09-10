# A2: internally overlapping strips with a summable remainder

## Full graph and a proof for every volume

Retain the full n-vertex open cubic lattice, n>=2, its n^3 vertices, 3(n-1)n^2 oriented links and 3n(n-1)^2 elementary faces. Every link retains its electric Casimir. The full Hilbert space is the untruncated product of normalized SU(2) link Haar spaces, with all-vertex Gauss restriction applied after the full-space ground argument. There are no external charges.

Place a three-face xy strip at each anchor (4i,2j,z), with 0<=i<floor(n/4), 0<=j<floor(n/2) and 0<=z<n. Each contains consecutive x-faces at offsets 0,1,2 and exactly the ten links of accepted A1. Hence the exact count is n floor(n/4) floor(n/2). Distinct x anchors differ by four and their strip vertices cover disjoint four-column sets; distinct y anchors cover disjoint pairs of rows; different z layers have different xy links. Thus their link supports are disjoint. Within each strip the three face interactions overlap. All links between strips remain as free factors of the reference operator.

The mask only accepts complete strips. Boxes n=2,3 have none, and incomplete terminal columns for other n are not silently assigned truncated clusters. The implemented sample boxes n=2 through n=9 test the signed graph construction; the preceding arithmetic establishes the count and disjointness for every n.

Every remaining face contains a link outside every cluster. There are three exhaustive cases:

1. An xz or yz face has a z-directed link. No selected xy strip uses any such link.
2. An unselected xy face at odd lower y has a y-link crossing an odd y interval. The clusters' y-links only occupy even intervals.
3. For an xy face at even lower y, a fitting complete x block with offset 0,1,2 would be selected. A remaining face must instead cross x=4i+3 or lie in the incomplete terminal x block. Its x-link is absent from all selected strips.

These cases include every incomplete boundary and the cluster-free small boxes. The witness function uses integer arithmetic for arbitrary n; finite graph materialization is separately capped. Each saved remaining-face ledger entry names an actual witness edge in that face's signed word.

## Dressed product ground and one remainder norm

Write cluster end coefficients as alpha times ratios bounded in absolute value by 1/2 and each bridge ratio by 1/8. The accepted A1 operator on each ten-link strip has a unique full-space ground and gap at least alpha/8. Signed and zero ratios remain within this theorem. Their full tensor sum, together with all free links, has a unique dressed cluster-product ground Psi_ref. Its reference gap is at least alpha/8. If there are no clusters, the exact full-space free gap is 3alpha/4; alpha/8 is used only as a conservative consequence.

For any remaining face, the witness edge is a constant free-link factor in Psi_ref. Conditional Haar integration therefore gives <Psi_ref,x_f Psi_ref>=0, pointwise in the other link values. The unknown cluster wavefunctions need not be constant. For V=-sum_remaining nu_f x_f, put beta_n=sum_remaining |nu_f|. Then ||V||<=beta_n and <Psi_ref,V Psi_ref>=0. The same two spectral directions as A1 yield

    E1(H)>=E_ref+alpha/8-beta_n,
    E0(H)<=E_ref,
    Delta_full>=alpha/8-beta_n.

The generic comparison without this zero reference mean would lose 2beta_n. These bounds use the untruncated operator, its unchanged elliptic domain and compact resolvent on each finite compact group product. Every potential is bounded and smooth. If the full gap lower bound is positive, uniqueness and the absence of nontrivial one-dimensional characters of the continuous vertex SU(2) group make the full ground gauge invariant. The reducing physical subspace contains that ground, so the full-space lower bound also bounds its physical excitation gap. No factorization of the physical Hilbert space is asserted.

## Positive orthant budget and exact finite ledgers

For a face with lower anchor (x,y,z), in any of the three orientations, set

    w_f=2^(-x-y-z)/24,
    nu_f=alpha tau w_f

on every remaining face. The weights are positive. Summing over the three orientations and the entire nonnegative orthant gives 3*2*2*2/24=1. Thus beta_n<=alpha |tau| for every n, and

    Delta_physical >= alpha(1/8-|tau|).

For |tau|=1/64 and alpha>=alpha_min>0 in common physical units, this proves the uniform finite-volume lower bound 7alpha_min/64. The generic bound at the same scale is 3alpha/32. The dimensionless remainder coefficient is not a Hamiltonian energy by itself; its physical coefficient includes alpha.

The code also retains the actual finite budget. Let S_m=sum_(k=0)^(m-1)2^-k. The exact total existing-face weight is S_(n-1)^2 S_n/8. Summing the three x-offset weights 1+1/2+1/4 gives the selected-strip weight

    (7/96) [sum_(i<floor(n/4))2^(-4i)]
             [sum_(j<floor(n/2))2^(-2j)] S_n.

Subtracting gives the finite remaining weight W_n and the stronger per-volume estimate alpha(1/8-|tau|W_n). The uniform proof uses only W_n<=1 from the positive orthant sum. A possible limiting value such as 107/135 is not substituted for a proved all-volume upper bound. No finite overshoot is claimed or required.

## Scope, boundary reclassification and controls

Canonical nonzero end magnitudes alpha/2, bridge magnitude alpha/8 and tau=1/64 make every actual face coefficient nonzero. The remaining coefficients decay with position, so this is an inhomogeneous full-support exception. It is not the homogeneous nondecaying Yang-Mills family. Signed nonzero ratios and negative tau preserve the absolute-value bound. Tau=0 is a valid sparse-remainder exception without full support; a zero selected cluster coefficient also removes full support.

The finite-volume family is not literally the restriction of one fixed infinite coefficient assignment at every boundary. For example, face f2:4,0,0 already exists at n=6 but belongs to an incomplete terminal strip and has coefficient 1/24576 in the alpha=1, tau=1/64 fixture. At n=8 the full strip fits and the same face has the cluster coefficient 1/2. Each fixed local assignment eventually stabilizes, but this statement and the uniform finite-volume gap estimate do not construct a thermodynamic operator, state or spectral limit.

At |tau|=1/8 the safe uniform estimate is exactly zero and remains insufficient. A positive finite-volume estimate can coexist with that zero uniform estimate because W_n<1. These statuses are kept separately. If 1/8-|tau| is negative, multiplying it by alpha_min would not follow from alpha>=alpha_min; the claimed common-bound field is therefore missing. A negative per-sample comparison remains a valid insufficient estimate. Two nonunit alpha scales verify this separation.

A nonzero homogeneous remainder does not meet the summable premise. At least the 2n(n-1)^2 xz and yz faces remain, so its total absolute coefficient budget diverges with n. The rejection concerns this proposed uniform proof condition; it does not declare the finite homogeneous operator undefined. Zero homogeneous coefficients are the trivial exception. Explicit coefficient ledgers preserve signs, zero entries and every boundary face.

## Reproduction and gate

Run `python -B check.py --output ../a2-output`. The single active dependency chain is check.py to summable.py to cluster.py. The last file is an unchanged copy of the accepted A1 bridge.py, used to replay its local bound; it is not a second A2 implementation or a superseded draft. All three are self-contained and source bound. Exact collection.json and volume.csv retain all graphs n=2 through n=9, the full face ledgers, signed/zero/endpoint/scale fixtures and the real boundary-reclassification diagnostic. Large counts and anchor iteration are lazy; materialized graphs and cluster lists have the same cap of twelve. Rational geometric sums have an explicit finite arithmetic cap, separate from the all-n proof. These limits are not theorem limits.

Normal and optimized runs must give identical semantic output bytes. Independent scientific verification is separate from the author suite. This completes A2 only; the post-A advisory decision must precede any B1 work. The homogeneous dense stability goal and the continuum Yang-Mills construction remain open.
