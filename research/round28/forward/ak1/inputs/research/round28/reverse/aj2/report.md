# AJ2 reverse: an actual nonzero homogeneous Wilson fluctuation

This independent reverse report proves qualitative nonvacuity throughout the
inherited I1/AJ1 symbolic coupling interval. The original elementary xz Wilson
multiplier has no point spectral projections on its complete local Hilbert
space. The actual locally normal state therefore has strictly positive Wilson
variance. Its centered physical vector has a nonzero positive energy spectral
measure and a strictly positive imaginary-time correlation at every finite
time, with the inherited gap upper bound. No numerical variance, energy moment,
threshold eigenvalue, or continuum conclusion is asserted.

The advisor supplied the observable and proposed the level-set/normality route
in the frozen contract. This is an independent derivation and new diagnostic
implementation of that shared question, not an independent physical observation.
Current forward AJ2 and current skeptic AJ2 mathematics remain unread through
the producer freeze. Source and instruction snapshots preceded scientific work;
the advisor released production only after the unchanged input pack passed the
standard preflight. The full seven-loop draft and its network are inherited
project knowledge. No historical interpretation is a premise of this proof.

## 1. Actual model and inherited operator facts

A coarse site b=(i,j,k) in the positive orthant owns all three positive-direction
original links with tails in

    T_b={(4i+r,2j+s,k): 0<=r<4, 0<=s<2}.

Its full Haar Hilbert space has 24 links: the ten-link selected strip and
fourteen free links. Ownership is pi(x,y,z)=(floor(x/4),floor(y/2),z). Heads
beyond a region boundary retain their original gauge actions. These are full
unconstrained tensor factors; physical factors are not presumed to tensorize.

Retain the fixed selected coefficients |lambda_L|,|lambda_R|<=alpha/2 and
|mu|<=alpha/8, the onsite reference h_b of I1, and all 21 omitted anchored
Wilson faces in each interaction

    phi_b=-(tau/3) sum_(21 omitted faces) W_f,
    ||phi_b||=M=7|tau|,  S={0,e_x,e_y,e_z}.

Finite coarse cuboids retain exactly those complete stars b+S lying inside
the cuboid. The limit is that particular I1 whole-star orthant ground state,
not a dyadic state or a changed boundary prescription. The homogeneous
interaction is not a bounded summable global perturbation at nonzero tau.
The regime stays exactly

    |tau|<tau_* = min(c1(S),1/(2c2(S)))/7,

with unevaluated positive source constants; no numerical admissible coupling
is extracted. The fixed positive alpha and E_star are energies, a is the fixed
lattice spacing, and hbar has units energy times time. Tau is dimensionless.

AJ1 supplies the actual normal local densities rho_R on the full B(K_R), the
normal represented local algebras, and compatible original-endpoint Haar
averaging. For the algebra of **all bounded local gauge-invariant operators**,
its GNS cyclic space H_cyc equals the joint gauge-fixed subspace. It reduces
the closed, nonnegative, vacuum-centered generator G. Its restriction G_phys
has zero eigenspace exactly C Omega and spectrum in
{0} union [1/2,infinity). In physical units

    delta=alpha/8, H_phys=delta G_phys,
    Spec(H_phys) subset {0} union [g,infinity), g=alpha/16.

These are the source-correct AJ1 results, including its post-review spectator
closure clarification. They do not assume a local tensor-product operator
algebra is norm dense in a larger B(K), and do not assume arbitrary bounded
local vectors belong to the generator domain. I1's tested resolvent theorem
for bounded local A,B and its separate source-qualified creator core are not
interchanged here. AJ2 uses only the already closed reducing physical generator.

## 2. Reconstruct the actual face and complete region

Let o=(0,0,0), x=(1,0,0), z=(0,0,1). The ordered path is
o -> x -> x+z -> z -> o, and its holonomy and observable are

    Q=U_x(o) U_z(x) U_x(z)^(-1) U_z(o)^(-1),
    W=Tr(Q)/2.

The four distinct positively stored links have tails/directions
(o,x), (x,z), (z,x), (o,z). Their respective owners are 0,0,e_z,0.
Thus the minimal complete coarse-factor region is R={0,e_z}, containing 48
original links, not four. Its tails are all (i,j,k) with
0<=i<=3, 0<=j<=1, 0<=k<=1. Every endpoint is in the disjoint union

    those 16 tails;
    (4,j,k), 0<=j,k<=1                       [4 new x heads];
    (i,2,k), 0<=i<=3, 0<=k<=1               [8 new y heads];
    (i,j,2), 0<=i<=3, 0<=j<=1               [8 new z heads].

There are 36 endpoint SU(2) actions, including 20 heads outside the tail set.
The checker enumerates all 48 links and 36 vertices, verifies unique tail
ownership and path incidence, and exports their labels. No corner diagonal
tail or independent plaquette coordinate is inserted. The xz face is one of
the omitted faces, not one of the three selected xy-strip faces.

For every full endpoint assignment g_v, stored links transform as
U_e -> g_tail U_e g_head^(-1). Inverse occurrences transform with the reversed
endpoints, and cancellation along the displayed closed path gives
Q -> g_o Q g_o^(-1). Hence W is a local physical observable under all 36
actions; spectator endpoint transformations cause no difficulty.
For SU(2), Tr(Q) is real and |Tr(Q)/2|<=1. Consequently multiplication by W
is bounded self-adjoint on K_R=L2(SU(2)^48,Haar^48). Its norm is exactly one:
neighborhoods of Q=I and Q=-I have positive measure, although the endpoint
level sets themselves have measure zero, as proved next.

## 3. Every actual Wilson level has zero Haar measure

Hold fixed all original link variables except U_x(o), which occurs exactly
once and only positively in Q. Then Q=U_x(o)A for a fixed SU(2) matrix A.
Right translation preserves normalized Haar measure, so its conditional law
is Haar on SU(2), independently of all these fixed values. This is a statement
about the original product reference measure, not factorization of the actual
interacting state.

Identify SU(2) with unit quaternions (s,v) on S3. Normalized Haar is normalized
rotation-invariant surface measure, and Tr(Q)/2=s. Slicing S3 at s gives the
probability density

    dnu_H(s)=(2/pi) sqrt(1-s^2) 1_[-1,1](s) ds.             (1)

For example the surface parametrization (s,sqrt(1-s^2)n), n in S2, has
surface element sqrt(1-s^2) ds dArea_S2; dividing by Area(S3)=2pi^2 yields
(1). Its integral is one. Thus every singleton has measure zero, including
s=0 and s=+/-1; levels outside [-1,1] are empty. Fubini in the one actual link
and the remaining 47 spectator variables proves

    Haar^48{configuration: W=c}=0 for EVERY real c.         (2)

For the full local multiplication operator, its spectral projections are
E_W(B)=multiplication by 1_{W in B}. Equation (2) proves E_W({c})=0 as an
operator for every c. More generally E_W(B)=0 whenever nu_H(B)=0; the converse
also holds by the same pushforward identity. In particular ker(W-cI)={0}.
This is stronger than merely observing that W is nonconstant. A measurable
nonconstant function can have positive-measure constant regions.

## 4. Actual normality implies qualitative positive variance

The actual restriction omega|B(K_R) has a positive trace-class density rho_R
with trace one by AJ1. Write rho_R=sum_j p_j |psi_j><psi_j|, p_j>0,
sum_j p_j=1. The spectral probability of the actual Wilson observable is

    nu_omega(B)=Tr(rho_R E_W(B))
               =sum_j p_j integral_{W in B}|psi_j|^2 dHaar^48. (3)

It is absolutely continuous with respect to the pushforward nu_H, hence
nonatomic by (2). No converse absolute continuity or full support is asserted.
Let m=omega(W), a real number. Since W is bounded, its variance exists and

    V=omega((W-mI)^2)=sum_j p_j ||(W-mI)psi_j||^2.          (4)

If V=0, every positive-weight psi_j is in ker(W-mI), which is {0}. This
contradicts trace rho_R=1. Therefore V>0, throughout the full inherited
symbolic regime, including tau=0. Neither faithfulness nor a continuity
neighborhood of the Haar vacuum is required. The proof gives no numerical
value or uniform positive margin for V.

The GNS null left ideal is N_omega={A:omega(A* A)=0}. Equation (4) says that
W-mI is not in this ideal. The isometry [A] -> pi(A)Omega identifies its
nonzero class in the physical local quotient with

    chi=(pi(W)-mI)Omega in H_cyc,
    <Omega,chi>=0, ||chi||^2=V>0.                          (5)

Here membership in H_cyc follows directly from bounded local gauge invariance
of W-mI. It does not require an operator-domain assertion. Local normality
does not make N_omega trivial for all local operators.

## 5. Positive imaginary-time consequence with actual units

Let P_H be the spectral resolution of the closed H_phys, and define

    mu_chi(B)=<chi,P_H(B)chi>.

It is a finite positive Borel measure, with total mass V. The unique vacuum
and (5) give mu_chi({0})=0. The inherited spectral exclusion therefore implies
support(mu_chi) subset [g,infinity). The measure is nonzero since V>0.
In particular the physical positive-energy sector is not empty. This is a
nonzero vector statement, not construction of a normalizable eigenvector.

For every finite t>=0 the bounded semigroup is defined on every vector and

    C(t)=<chi,exp(-t H_phys/hbar)chi>
        =integral_[g,infinity) exp(-t E/hbar) dmu_chi(E),
    0<C(t)<=V exp(-alpha t/(16 hbar)).                    (6)

Strict positivity follows because the integrand is strictly positive at
every finite energy and mu_chi is a nonzero positive measure. Equivalently,
some finite interval [g,L] has positive measure and its integral is positive.
At t=0, C(0)=V. Dominated convergence gives continuity at zero, and (6) gives
C(t)->0 as t->infinity. Both t and hbar retain their physical meanings.

The support lower bound does not assert mu_chi({g})>0, that g is the lowest
overlapping energy, or that any overlapping lowest energy is attained as an
eigenvalue. It gives an upper bound with rate g, not a universal lower bound
with that rate or an extracted mass. Replacing imaginary time by real time
changes the integrand to a phase and proves no magnitude decay. No matching
to another model, thermodynamic boundary family, or continuum is supplied.

No assumption chi in D(H_phys) or D(sqrt(H_phys)) was used. The first and
second energy moments would respectively require those form/operator domain
conditions; bounded locality alone supplies neither. In particular no finite
derivative at t=0 is claimed. Quantitative variance and energy-moment results
are outside this investigation.

## 6. Discriminating controls, with their exact scope

The following are mathematical countermodels or reference diagnostics, not
substitutes for (2)--(6) in the actual homogeneous state.

* A constant multiplier cI has zero centered variance in every state. Thus
  boundedness, locality, and gauge invariance alone do not prove (5).
* B=1_{W>0} is nonconstant and has positive-measure levels. The normalized
  vector psi=sqrt(2)1_{W>0} defines a normal rank-one density with B psi=psi,
  so Var(B)=0. This directly invalidates a nonconstancy-only proof.
* The Haar constant vector defines a normal but nonfaithful rank-one density
  on B(K_R). By symmetry E_H W=0 and E_H W^2=1/4. Nonfaithfulness does not
  prevent positive variance for this particular atomless multiplier. A
  projection onto any vector orthogonal to the constant is a nonzero positive
  operator with zero expectation in that state.
* The normalized reference vector psi=2W has E W=0 and variance
  4 E_H W^4=1/2, since E_H W^4=1/8. Thus two normal local states already give
  different Wilson variances. Neither reference value is omega's variance.
  The fundamental character chi_1/2=2W has Haar norm squared one and fourth
  moment two; these are character/reference identities only.
* For every 0<epsilon<1, the normal rank-one state with vector
  psi_epsilon=1_{|W|<epsilon}/sqrt(nu_H((-epsilon,epsilon))) is defined because
  (1) assigns that band positive measure. Symmetry gives mean zero and
  0<Var(W)<epsilon^2. This proves the absence of a positive uniform margin
  over all normal states. Weak-star compactness of the state space of B(K_R)
  gives a subnet limit as epsilon->0, with value zero on W^2. It is a
  nonnormal state with atomic restriction to C*(W), since a normal state
  cannot have zero variance by (4). This is not a nonexistent delta-vector
  in L2, nor a claim of uniqueness of the singular extension.
* On C2 with vacuum e0, H=diag(0,g), and A=(I+sigma_x)/2, the uncentered
  heat correlation is (1+exp(-tg/hbar))/4, while its centered correlation is
  exp(-tg/hbar)/4. Omitting the actual mean retains a vacuum plateau.
* The one-dimensional vacuum Hilbert space satisfies the inherited spectral
  inclusion with an empty positive sector. Its centered local vectors are
  zero. Spectral exclusion alone does not prove a nonzero spectral measure;
  (4) is the added nonvacuity step.
* A centered vector at energy 2g has C(t)=V exp(-2gt/hbar). It has no atom at
  g and contradicts a proposed lower bound V exp(-gt/hbar) at t>0. A vacuum
  plus multiplication by E on L2([g,2g],dE), with a constant excitation vector,
  has infimum of excitation support g but no threshold atom or eigenvector.
  An energy eigenvector instead gives constant magnitude V under real-time
  evolution. The checker uses q=exp(-gt/hbar)=1/2 as an exact diagnostic time;
  it does not approximate the actual spectral integral.
* On C e0 plus l2(n>=1), set H e_n=g 4^n e_n and
  v=sum_(n>=1)2^(-n)e_n. Then ||v||^2=1/3, but its form energy is
  g sum_(n>=1)1=infinity. The bounded self-adjoint A=|v><e0|+|e0><v| has norm
  1/sqrt(3)<=1, gives the centered vector v, and may be declared physical
  under the trivial gauge action. This abstract countermodel shows that
  bounded observable hypotheses by themselves do not imply form or operator
  domain membership. It is not a new domain claim about the actual W.

The exact checker derives the complete face geometry and uses rational unit
quaternions for every original link and endpoint. It checks conjugation of
the original holonomy, and tests a missing-head and a charged-word variant.
Any nondiscriminating development fixture is retained explicitly if one is
encountered; a test that does not discriminate is never relabeled a rejection.
The executable's finite controls audit implications and normalization. The
analytic proofs, including Fubini, trace-class normality, the GNS quotient and
the spectral theorem, carry the infinite-dimensional conclusions.

## 7. Reproduction and source closure

Run `python research/round28/reverse/aj2/check.py --output /absolute/fresh/dir`
from any working directory; repeat with `python -O` into another fresh absolute
directory. Only the Python standard library is used. The checker requires a
fresh destination, verifies the declared contract and source hashes, reads all
instruction bytes from its owned snapshots, and exports one results.json.
Absolute instruction origins remain provenance in the unchanged inventory;
they are never runtime dependencies. The results bind this report, checker,
the contract, every declared repository original, input manifests/freezes and
every owned snapshot with flat repository-relative paths. The top freeze
includes every owned file except its exact own top freeze.json, including all
nested historical source freezes. Normal/optimized output equality is recorded
separately. No historical checker is imported or executed for this result.

Primary-source dependency depth is inherited and explicit: the I1 reports and
correction supply the symbolic model theorem, AJ1 supplies the proved local
regularity and closed physical restriction, and the source-topology note
separates Yarotsky's bounded-local resolvent tests from his creator core.
These bound documents and the seven-loop draft were read. No new primary
source retrieval or claim of new historical reading is made in AJ2. The local
SU(2) level-set and spectral-measure arguments above are derived here.

This closes investigation 8 within the frozen qualitative target. It neither
selects nor executes the fifth goal pair, proves a numerical variance margin,
evaluates tau_*, asserts global faithfulness, or solves the Yang--Mills
continuum mass-gap problem. Scientific priority remains unverified.
