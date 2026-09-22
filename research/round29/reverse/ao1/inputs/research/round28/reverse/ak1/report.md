# AK1 reverse: a constructive variance floor for the actual origin Wilson loop

Under the unchanged AK1 contract, the actual I1/AJ1/AJ2 homogeneous orthant
state satisfies

    Var_omega(W) >= 119/576 > 1/5

for every real |tau|<tau_* with |tau|<=2^-16, uniformly over the inherited
fixed selected-coefficient ranges. This is investigation 9. The extra numerical
cap does not evaluate tau_* or certify a chosen positive admissible coupling.
AJ2's qualitative positivity remains valid on its wider symbolic regime.

This is an independent reverse derivation of a shared contract proposal.
Sources and instructions froze before production; root's source preflight
passed before the derivation. Current forward AK1 and current skeptical AK1
science were not read. Historical names designate modern research methods,
not participation or endorsement. No historical checker was imported or run.

## 1. Work backward from the variance

Let rho be the actual positive trace-one local density on the full region R,
let P=|Omega_R^0><Omega_R^0| be its reference product-vacuum projector, and
write d=||rho-P||_1 (the full trace norm, not half that norm). Suppose

    Tr(P W)=0,  Tr(P W^2)=1/4,  ||W||<=1,  d<=1/24.       (1)

Trace duality then bounds both actual moments:

    |m|=|Tr(rho W)|<=d,
    Tr(rho W^2)>=1/4-d,
    Var_rho(W)>=1/4-d-d^2>=119/576.                       (2)

The unknown actual mean is retained, and its square costs 1/576 in the final
certificate. The margin above 1/5 is 19/2880. In particular a sufficient
overlap premise for (1) is

    epsilon:=1-Tr(rho P)<=1/2304,                         (3)

provided the general mixed-density estimate d<=2 sqrt(epsilon) is proved.
The actual reference-energy estimate below gives the strictly smaller ceiling
7/16384. No interacting moment is set equal to a Haar moment.

## 2. Same model, full support, and every incident group

A coarse site b=(i,j,k) owns all three positive original links at each tail
(4i+r,2j+s,k), 0<=r<4, 0<=s<2. Euclidean division gives unique ownership
pi(x,y,z)=(floor(x/4),floor(y/2),z). Its unreduced space is L2(SU(2)^24).
The three selected xy faces at local tails (0,0,0),(1,0,0),(2,0,0) use ten
links; fourteen links, including every z link, are free. Only the unreduced
spaces tensorize in this argument; a physical tensor factorization is not
assumed.

Retain fixed |lambda_L|,|lambda_R|<=alpha/2, |mu|<=alpha/8, with alpha,hbar,
E_star,a positive and fixed. Delta=alpha/8 is a physical energy, tau is a
dimensionless omitted-action coupling, and the numerical cap is a proof
subregime. The actual normalized finite Hamiltonian is

    Hhat_Lambda=sum_(b in Lambda) h_b
                  +sum_(b+S subset Lambda) phi_b,
    h_b=(H_strip,b-E_strip,b+alpha sum_free C_e)/delta,
    h_b>=I-P_b, h_b Omega_b^0=0,
    S={0,e_x,e_y,e_z},
    phi_b=-(tau/3) sum_(21 omitted anchored faces) W_f,
    ||phi_b||=M=7|tau|.                                  (4)

The unique onsite vacuum is the selected strip ground vector times constant
free-link vectors. The ground scalars in (4) are part of the reference, and
are not dropped. I1 supplies the specified whole-star orthant limiting state
on |tau|<tau_*=min(c1(S),1/(2c2(S)))/7, with unevaluated positive constants.
AJ1 supplies its normal densities on full local factors and the actual full
bounded physical GNS completion; AJ2 supplies qualitative Wilson nonvacuity.
The homogeneous sum is nonsummable in global norm at nonzero tau. No dyadic,
canonical, independently resampled plaquette, or finite AH state enters here.

For a face at original p in axes a<c, its canonical oriented links are
(p,a,+), (p+e_a,c,+), (p+e_c,a,-), (p,c,-). Thus its owners are pi(p),
pi(p+e_a),pi(p+e_c), with no diagonal-corner tail. The eight xy anchors have
three selected faces. Their five omitted remainders have supports {0,e_x}
once, {0,e_y} three times, and {0,e_x,e_y} once. The eight xz faces give six
{0,e_z} and two {0,e_x,e_z}; the eight yz faces give four {0,e_z} and four
{0,e_y,e_z}. This proves the full multiplicities 1,3,1,10,2,4 and union S.
Each retained group costs all 21 faces, regardless of a face's smaller support.

The frozen observable is

    W=Tr[U_x(0) U_z(e_x) U_x(e_z)^(-1) U_z(0)^(-1)]/2.    (5)

The four owners are 0,0,e_z,0. The minimal complete R={0,e_z} contains all
48 original links, twenty selected and twenty-eight free. Its sixteen tails
are 0<=x<=3, 0<=y<=1, 0<=z<=1. The full endpoint set adds four x heads at
x=4, eight y heads at y=2, and eight z heads at z=2: 36 endpoint actions
in total. Link transformations U_(v,w)->g_v U_(v,w) g_w^(-1) telescope
around (5) to conjugation at zero, so W belongs to the actual bounded physical
algebra. SU(2) half-traces are real and bounded by one. No outgoing head is
clipped, and the two-factor observable cover is not a four-site interaction
star.

For any finite complete region F, the exact orthant incident anchors are

    I_+(F)=(F-S) intersect Z_+^3,
    I_Lambda(F)={b in I_+(F): b+S subset Lambda}.           (6)

Indeed an intersection site has r=b+s, and conversely every such anchor meets
F. Set union counts a group meeting both sites only once. For R, the only
nonnegative differences are 0 and e_z. Hence n_+(R)=2. In a cubic volume
with side count n, retained anchor coordinates are 0,...,n-2. At n=2 only
zero survives; for every n>=3 both anchors survive. More generally no allowed
finite cuboid containing R can have more than these two incident groups.

| Cuboid | Links | Endpoints | Whole stars | Incident groups at R | Charged group faces |
|---|---:|---:|---:|---:|---:|
| (2,2,2) | 192 | 120 | 1 | 1 | 21 |
| (3,3,3) | 648 | 342 | 8 | 2 | 42 |
| (4,4,4) | 1536 | 736 | 27 | 2 | 42 |

For an n-cube these global counts follow analytically from 8n^3 tails,
three links per tail, 14n^2 added heads, and (n-1)^3 anchors. The translated
incidence-only control F={(1,1,1),(1,1,2)} has seven orthant anchors: its
two sites, their two x predecessors, their two y predecessors, and (1,1,0).
It is absent from the 2-cube, has four retained groups in the 3-cube, and
seven in the 4-cube. No translated variance claim is made. Counting only
anchors in F is blind at the origin R; the same rule loses three or five
groups in these interior fixtures. That blind origin control is preserved.

## 3. The actual energy and overlap estimates

For completeness, AJ1's local-energy argument applies to precisely (4).
Reset R in the actual finite ground density to

    rho'_Lambda=P tensor Tr_R rho_Lambda.

The finite ground has finite reference energy by bounded perturbation of the
finite reference sum. Positive bounded spectral truncations and monotone
convergence justify unchanged exterior energy in the mixed reset density.
It has zero reference energy in R and finite total form energy, so it is a
valid mixed variational trial state. The exact finite ground scalar, exterior
reference energies, and disjoint interactions cancel in the difference.
Every complete incident group changes expectation by at most 2||phi_b||.
Consequently

    Tr(rho_Lambda,R h_R)<=2M n_Lambda(R)<=28|tau|,
    h_R=h_0+h_ez.                                        (7)

This is not a small global perturbation argument or an individual-face
incidence estimate. It works for both signs and all fixed allowed selected
coefficients. AJ1's local normality and actual trace-norm local-state limit
identify rho_R. Passing each bounded spectral truncation of the positive h_R
to that limit and then increasing the truncation yields

    Tr(rho_R h_R)<=28|tau|<=7/16384.                       (8)

The estimate is in normalized reference-energy units. Its physical reference
energy version multiplies by delta; it is not the physical spectral first
moment of the centered Wilson vector.

On the full two-factor Hilbert space, commuting onsite vacuum projectors give

    h_R >= (I-P_0)+(I-P_ez)
          = I-P + (I-P_0)(I-P_ez) >= I-P.                 (9)

The identities use lifted projectors; P=P_0 P_ez is rank one. The inequality
holds as a closed quadratic-form inequality, and therefore for positive
density expectations, allowing infinity before (8) is applied. Both-free-link
and strip excitations are included. Thus

    epsilon=Tr[rho_R(I-P)]<=Tr(rho_R h_R)<=7/16384.

Since 7*2304=16128<16384, this proves the sufficient overlap premise (3).

## 4. Mixed-density trace distance and the actual reference moments

For any unit psi and unit Omega, put e=1-|<Omega,psi>|^2. If e=0 the
projectors agree. Otherwise their difference is supported on their
two-dimensional span, with trace zero and eigenvalues +/-sqrt(e), as is
seen in the basis Omega and the normalized orthogonal component of psi.
Its trace norm is exactly 2sqrt(e), including the orthogonal endpoint.

For arbitrary positive trace-one rho on this separable local Hilbert space,
write its trace-class spectral decomposition rho=sum_j p_j |psi_j><psi_j|.
Trace-norm convergence, the triangle inequality and Cauchy--Schwarz give

    ||rho-P||_1 <= 2 sum_j p_j sqrt(1-|<Omega,psi_j>|^2)
                <= 2 sqrt(sum_j p_j(1-|<Omega,psi_j>|^2))
                 = 2 sqrt(1-Tr(rho P)).                  (10)

This is an inequality for mixed densities, not the pure-state equality
imposed on rho. Countably infinite sums follow by trace-class approximation;
the weights sum to one. Applying (8)--(10),

    d^2<=4epsilon<=7/4096<1/576, hence d<=1/24.            (11)

The factor two and square root cannot be omitted. In contrast to an
unproved interacting Haar law, the reference moments can be evaluated.
Condition on all original links except the actual free link u=U_z(0).
The reference vector is independent of u despite selected-strip
entanglement; its remaining squared density integrates to one. The
holonomy is A u^(-1), with A fixed under that conditioning. Haar inversion
and left translation preserve Haar, so its scalar quaternion coordinate
has mean zero and second moment 1/4. The first identity follows by sign
symmetry; the second follows because four rotation-symmetric squared
coordinates sum to one. Fubini proves Tr(PW)=0 and Tr(PW^2)=1/4 for the
actual selected-strip product vacuum, uniformly in the selected coefficients.
This completes (1), and (2) proves the stated actual variance floor.

## 5. Controls, evidence and limits

The new standard-library checker reconstructs all original face words,
selected/free sets, the 48 links and 36 endpoints, finite whole stars and
both incidence formulations. It retains every complete 21-face group and
uses rational noncommuting quaternions to check full endpoint covariance.
Those fixtures audit the analytic geometry; they do not prove the limiting
state theorem by finite sampling.

The trace-distance diagnostic is a genuine mixed density
rho=[[17,6],[6,8]]/25 and P=diag(1,0). It has determinant 4/25, trace one,
purity 17/25, epsilon=8/25 and ||rho-P||_1=4/5. Both the missing-factor
bound sqrt(epsilon) and missing-root bound 2epsilon fail. Pure-state equality
would also give an incorrect value. A separate pure density from (3/5,4/5)
saturates the valid factor-two square-root bound. These finite matrices
diagnose (10); its trace-class proof supplies the infinite-dimensional result.

Two legitimate alternative normal states test what the actual energy premise
adds. The vector sqrt(1+W) Omega_R^0 is normalized and has mean 1/4, second
moment 1/4 and variance 3/16, using the same conditional reference law and
its vanishing odd moments. Thus omitting the squared mean or assigning Haar
variance to all normal states falsely certifies the target. Separately, put
B={|W|<1/4} and psi_B=1_B Omega_R^0/sqrt(p), where p=Tr(P1_B)>0. This
normal state has mean zero and 0<Var(W)<1/16. Its reference overlap is p.
The Haar scalar density (2/pi)sqrt(1-w^2), inherited and proved in AJ2,
gives p<=1/2 using pi>2 and the band length 1/2. Hence its overlap defect
is at least 1/2, and (9) forces reference energy at least 1/2 (possibly
infinite). It violates (8), which is the additional model-specific premise.
No finite-energy assertion is made for this discontinuous band vector.

An exact scalar fixture retains E_strip and delta=alpha/8: adding the same
scalar to the raw Hamiltonian and its ground leaves h unchanged, whereas
omitting the subtraction gives a nonzero, here negative, vacuum energy.
Dividing by alpha instead of delta loses the unit projector inequality.
An abstract possible choice c1=2^-20,c2=1 makes the symbolic tau_* smaller
than 2^-16; it rejects the inference that the extra cap evaluates the source
constants. These are logical diagnostics, not actual source-constant values.

The origin outgoing-only incidence test is explicitly nondiscriminating and
retained beside its discriminating interior replacements. There was one
administrative input-copy path resolution failure before the input manifest;
its unchanged snapshots and correction are recorded there. Any scientific
execution failure or later repair is recorded in production-history.json;
none is erased or counted as another investigation.

Reproduce from any working directory with fresh absolute destinations:

    python -B research/round28/reverse/ak1/check.py --output /absolute/fresh/normal
    python -B -O research/round28/reverse/ak1/check.py --output /absolute/fresh/optimized

Only results.json is emitted per run. Runtime reads are owned repository
snapshots and owned author files; installed absolute origins are provenance
only. Flat bindings include the script, report, contract, all required
originals, input manifest and every snapshot. Final freeze includes every
owned file except its exact top-level freeze.json, including inputs/freeze.json.
Fresh normal/optimized byte equality is recorded in validation.json.

The reading ledger distinguishes complete AJ1/AJ2 proof and instruction
readings from focused manuscript reading, network structure/current-node
review, and source-byte-only preservation of archival material. No new
external source retrieval or whole-paper audit is claimed. Standard trace
distance, reference Haar moments and AJ1's admitted energy estimate are
applied here; scientific priority is unverified.

This dimensionless variance floor makes no new assertion about a physical
first moment, form/operator domain of W Omega, commutator or f-sum identity,
spectral window, lower decay bound, numerical mass, evaluated stability
radius, other boundary limit, global faithfulness, model matching or continuum
Yang--Mills. AK2 remains the advisor's adaptive selection after review.
