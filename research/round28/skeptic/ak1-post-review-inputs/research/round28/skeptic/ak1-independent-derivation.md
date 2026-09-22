# AK1 independent skeptical derivation

This is the current AK1 skeptic's own derivation, prepared after the root's
61-snapshot preflight and before reading any current AK1 producer mathematics.
The contract proposes the overlap/trace-distance route; that proposal is shared,
not an independently invented premise. This role is distinct from my disclosed
handoff closeout of the earlier AJ2 review. No AK2 question is executed here.

## 1. Model, exact support and the inherited energy premise

Retain the actual I1/AJ1/AJ2 homogeneous omitted interaction in the positive
coarse orthant, its complete-star finite-volume prescription and fixed
selected-strip coefficients. The physical constants alpha,hbar,E_star,a are
positive and fixed. Set delta=alpha/8. The regime is the intersection

`|tau|<tau_* = min(c1(S),1/(2c2(S)))/7` and `|tau|<=c=1/65536`.

The positive source constants remain unevaluated. In particular the additional
numerical cap c does not certify that c, or any chosen positive number, lies
below tau_*. This proof preserves AJ2's qualitative result on the wider
original symbolic interval.

A block b=(i,j,k) owns all three positive original links at tails
`(4i+r,2j+s,k)`, r=0,1,2,3 and s=0,1. Its 24 unreduced link factors contain
the ten-link selected xy strip and fourteen free factors. Ownership is unique
by Euclidean division; outgoing heads retain their original gauge actions.
This is not a tensor factorization of the constrained physical space.

For original unit steps x,z, use exactly

`W=Tr[U_x(0) U_z(x) U_x(z)^(-1) U_z(0)^(-1)]/2`.

The closed path is `0 -> x -> x+z -> z -> 0`. The stored positive links have
owners 0,0,z,0 and signs +,+,-,-. Its minimal complete region is
`R={0,z}`. The region contains 48 links, twenty selected-strip links and
twenty-eight free links. Its sixteen tails have x=0..3, y=0..1, z=0..1.
Adding four x-heads, eight y-heads and eight z-heads gives all 36 endpoints.
The full endpoint transformations telescope to conjugation of the holonomy
at its base. Thus W is bounded, real, self-adjoint and gauge invariant,
with norm one on the original local Hilbert space.

Let P_b be the unique reference-vacuum projector and let

`h_b=(H_strip,b-E_strip,b+alpha sum_free C_e)/delta >= I-P_b`.

The exact reference scalar is subtracted. These are nonnegative operators
on the unreduced factors, with the operator/form domains established in
A1/I1/AJ1. A free rotor's physical gap 3alpha/4 equals 6delta. For
`h_R=h_0+h_z` and `P=P_0 tensor P_z`, the commuting tensor factors give,
on the closed form domain,

`h_R >= (I-P_0) tensor I + I tensor (I-P_z) >= I-P`.

For example the difference in the last inequality is
`(I-P_0) tensor (I-P_z)>=0`. The product vacuum is unique and has exactly
zero reference energy. No physical excited-vector energy is used here.

AJ1 supplies the actual normal local densities and the proved bound

`Tr(rho_Lambda,R h_R)<=2M n_Lambda(R)`, `M=7|tau|`,

where n counts every complete retained 21-face star meeting R. The trial
state is a mixed vacuum reset on R, whose exterior marginal is unchanged;
bounded spectral truncations justify its unbounded reference energies.
The exact finite ground scalar, exterior reference terms and disjoint
interactions cancel. This inherited proof is not replaced by a global
summable perturbation estimate.

For S={0,x,y,z}, an incident anchor must be r-s, with r in R, s in S.
After imposing nonnegative coarse coordinates their union is exactly
`I_+(R)={0,z}`. The anchor at zero meets both region sites and is counted
once. Therefore every finite containing cuboid has n_Lambda(R)<=2, and

`Tr(rho_Lambda,R h_R)<=4M=28|tau|`.

For cuboid side counts (2,2,2), (3,3,3), (4,4,4), the retained target
incidences are respectively 1,2,2, charging 21,42,42 complete group faces.
The first smaller-boundary value is not replaced by its limiting value.
The interior incidence-only control R'={(1,1,1),(1,1,2)} has seven distinct
nonnegative incident anchors: each point minus S, with the shared anchor
(1,1,1) counted once. R' is absent from the first cuboid; it has four
retained incident stars in the second and seven in the third. Counting
only anchors in R' would miss incoming groups. No variance theorem for
translated observables is inferred from this control.

Every original face anchored at a tail in one block has support given by
the owners of its base, base+x_a and base+x_b. Among the 24 anchored
faces three are selected; all 21 omitted faces belong to the full
four-site star. The checker explicitly reconstructs every face of every
incident retained group. Counting only individual faces actually touching
R would not justify the reset comparison of full coarse-factor operators.

The limiting normal density rho_R satisfies the same energy bound: apply
the known local-state convergence to bounded spectral truncations of h_R
and use monotone convergence. Hence the actual vacuum deficit obeys

`e=Tr[rho_R(I-P)] <= Tr(rho_R h_R) <= 28|tau| <= 7/16384 = e_*`.

This bound is uniform over the selected-coefficient ranges because their
inherited normalized onsite gap is uniform and every interaction norm is
bounded by the same M. It concerns the specified whole-star orthant state.

## 2. A trace-distance inequality valid for mixed local densities

For a unit vector psi and reference vacuum Omega_R, the difference of
the two pure projectors has trace norm

`|| |psi><psi|-P ||_1 = 2 sqrt(1-|<Omega_R,psi>|^2)`.

To prove it, decompose psi into its component along Omega_R and the
orthogonal component. The difference vanishes outside their span and has
two eigenvalues plus/minus the square root above; the parallel endpoint
has zero difference. This is a two-dimensional spectral calculation,
not an assumption that the actual local density is pure.

For any positive trace-one density rho_R write its spectral decomposition
`sum_j p_j |psi_j><psi_j|`. The series converges in trace norm. The triangle
inequality followed by the weighted Cauchy-Schwarz inequality gives

`T:=||rho_R-P||_1 <= 2 sum_j p_j sqrt(1-|<Omega_R,psi_j>|^2)`
`                  <=2 sqrt(sum_j p_j(1-|<Omega_R,psi_j>|^2)) = 2 sqrt(e)`.

Partial sums and trace-norm convergence justify the countable case.
The symbol T is the full trace norm; the half-distance convention would
be T/2. The actual mixed density is not assigned pure-projector equality.

At the frozen cap, `4e_* = 7/4096 < 1/576`, since 4032<4096.
Consequently `T<=1/24`. No floating square root is used for this ceiling.

## 3. Actual reference moments and transport of the unknown mean

The product reference vacuum has one strip ground wavefunction in each
block and the Haar constant on every free link. The original link U_z(0)
is one of those free factors even when the selected strip is entangled.
Condition on all other original links. The holonomy is `A U_z(0)^(-1)`
with fixed A in SU(2); inversion and left translation preserve Haar.
The conditional half trace is the scalar coordinate of a uniform unit
quaternion. Symmetry gives its mean zero, while its four equal component
second moments sum to one. Therefore, for this actual reference vector,

`<Omega_R,W Omega_R>=0`, `<Omega_R,W^2 Omega_R>=1/4`.

The other factors integrate their normalized squared reference wavefunction.
No independence of plaquette holonomies or interacting conditional Haar law
is asserted. The normalized Haar fourth moment 1/8 is used only in controls.

Write m=Tr(rho_R W) and q=Tr(rho_R W^2). Schatten duality and ||W||=1
give `|m|<=T`. The generic second-moment estimate gives `q>=1/4-T`, hence

`Var_omega(W)=q-m^2 >=1/4-T-T^2 >=119/576 >1/5`.

The exact final margin of this deliberately conservative route is 19/2880.
The squared actual unknown mean has been charged; m is not set to zero.

An independent refinement is available without any new physical premise.
Since `0<=W^2<=I` and `Tr(rho_R-P)=0`, subtract I/2 inside the trace:

`|Tr[(rho_R-P)W^2]| <= ||rho_R-P||_1 ||W^2-I/2|| <= T/2`.

Thus the same argument also proves the separately attributed stronger floor

`Var_omega(W) >=1/4-T/2-T^2 >=131/576 >1/5`,

with exact margin 79/2880. It uses an effect bound for W^2; applying its
half-factor to an arbitrary signed W would be wrong. Neither fraction is
claimed optimal or equal to the actual interacting variance. For tau=0
the energy bound forces rho_R=P and the exact variance is 1/4.

## 4. Discriminating controls and their scope

The new checker uses rational arithmetic, original-link geometry and both
quaternion and independent complex-matrix multiplication. These finite
calculations audit the proof; the closed-form, mixed-state and limiting
arguments above establish the actual infinite-dimensional statement.

* For psi=(3/5,4/5), pure-projector deficit is 16/25 and full trace norm
  is 8/5. Removing the square root gives 32/25 and removing the factor
  two gives 4/5; both proposed upper bounds fail.
* The genuinely mixed density `(P+|psi><psi|)/2` has determinant 4/25,
  deficit 8/25 and full trace distance 4/5. It is not a rank-one density,
  and the square of its distance is strictly below 4e. The valid mixed
  inequality is not a universal pure-projector equality.
* Opposite two-dimensional pure states and W=diag(-1,1) saturate the full
  signed-observable bound T. The effect diag(0,1) saturates T/2. These
  distinguish the two moment costs rather than mixing distance conventions.
* On the same actual local configuration space, the normalized vector
  `sqrt(1+W) Omega_R` is a normal state. Conditional reference integration
  gives mean 1/4, second moment 1/4 and variance 3/16. This rejects both
  assigning Haar variance to every normal state and omitting the squared
  mean. It is an alternative state, not an evaluation of the ground.
* For the event |W|<epsilon with epsilon=1/4, the normalized vector
  `1_event Omega_R/sqrt(probability)` is a valid normal concentrating
  state. The conditional half-trace density is
  `(2/pi)sqrt(1-w^2) 1_[-1,1] dw`, so its band probability is positive
  and at most 4epsilon/pi<2epsilon=1/2. Its vacuum overlap is precisely
  that probability. Its positive variance is at most 1/16, but its
  vacuum deficit exceeds 1/2 and therefore its reference-energy
  expectation (possibly infinite) exceeds 1/2. It fails the additional
  energy/overlap premise, whose actual-state cap is 7/16384. Normality
  alone remains insufficient. No finite form energy is claimed for
  these discontinuous indicators.
* Complete group enumeration detects loss of the second origin-region
  anchor and incoming interior groups. It also distinguishes a group
  meeting both sites once from a per-site sum that counts it twice.
  An absent translated region is recorded as absent, not as a tested
  zero-incidence physical state.
* A shifted two-level reference checks that its true vacuum scalar must
  be removed. A separate scale diagnostic compares dimensionless
  deficit 1/4 with physical local energy 1/256 when delta=1/64; omitting
  division by delta would give a false deficit ceiling. These numbers
  belong to abstract controls, not to a changed actual model.
* Abstract positive source constants compatible with tau_*=c/2 allow
  a test value 3c/4 below the numerical cap but above tau_*.
  This demonstrates why the cap alone supplies no stability admission;
  it does not evaluate the actual source constants.

## 5. Evidence and remaining scope

The 40-page eight-loop draft was read completely through its immutable
text extraction; the relevant AJ dependency and equation nodes were read
in the fixed network. Both full AJ1/AJ2 reports, their controlling
post-reviews and A1/A2/I1 reference arguments were read. The external
cluster-expansion theorem remains inherited, with its original reading
depth; no new primary-source retrieval or priority audit is claimed.

All contract sources and used instructions were snapshotted before science.
The initial 55-input preparation metadata is preserved beside its disclosed
six-instruction completion; root preflight covered the final 61 snapshots.
The checker reads owned repository copies only. Installed absolute origins
are preparation provenance, never runtime dependencies. Source snapshots
and historical checkers are not executed as the new algorithm.

The conclusion is a constructive actual Wilson variance floor at least 1/5
in the specified conditional coupling subregime, with the independent
stronger floor 131/576. This is an application of standard projector,
trace-class and Haar tools to the source-bound homogeneous model; scientific
priority is unverified. It neither evaluates tau_* nor proves a numerical
nonzero stability interval, global faithfulness, equality of other boundary
states, physical scale/model matching or a continuum Yang-Mills theorem.
The local reference-energy estimate is not the physical first energy moment
of the excited Wilson vector. No physical form/operator-domain claim,
commutator sum rule, spectral window, lower heat decay or numerical mass is
established. AK2 is unselected and unexecuted here.
