# X2 reverse: a complete physical Ritz residual and late-time certificate

**Result.** The actually assembled vacuum-plus-20-face sector gives a
certified full-graph ground energy and projection, and its separately
centered heat approximates the full physical heat in operator norm by less
than **0.000085 for every sigma>=5 and every 0<=lambda<=1/100**. This includes
the small calculation's uniform arithmetic and time-evaluation error. No
large unassembled cutoff is used. The omitted residual has exactly 210
orthogonal physical channels: 20 spin-one faces and 190 distinct face pairs.

At lambda=1/100 the dimensionless true ground energy satisfies the outward
interval

    0.1998333232507006 <= epsilon <= 0.1998333359872953,

and the ground-projection error is at most 0.000083108605. These are
conservative spectral certificates, not measured errors. The time condition
is t>=5 hbar/alpha with the contract's fixed scales. This is an absolute
late-time heat result on this finite graph, not real-time, relative,
homogeneous, thermodynamic or continuum accuracy.

Authorship is an independent reverse model-agent derivation. Current
forward/x2 was not read or discussed before freeze. Shared inherited
premises make this project review distinct from outside peer review. X1's
accepted reports are inherited evidence; its earlier independent results
are not relabeled as new X2 derivations.

## 1. Reconstruct the needed claims before estimating the matrix

A desired full-graph ground claim cannot follow from the Ritz eigenvalue
alone. Sufficient data are: a normalized physical Ritz vector, its complete
full-Hamiltonian residual, a certified separation from the actual excited
spectrum, and the actual self-adjoint domain. A late-time operator estimate
then needs both actual and Ritz ground projections and their separate
centering. Arithmetic must preserve a unit ground eigenvalue at arbitrarily
large heat times. These are the backward obligations answered below.

Keep X1's open (3,3,2) grid, 18 vertices, 33 edges, 20 square faces and all
18 vertex Gauss constraints. On product-Haar L2 restricted to invariants,

    L = H_lambda/alpha = K + lambda V = K + c I - lambda X,
    K=sum_e C_e,   X=sum_(20 faces p) x_p,  x_p=Tr(U_p)/2,
    c=20lambda,   0<=V<=40,   ||X||<=20.

The constant coupling lies in [0,1/100]. Fixed a,E_star,alpha/E_star,hbar
remain positive; sigma=alpha t/hbar. The dimensionless quantities computed
below are spectral observables or approximation diagnostics. They are not
new action parameters or fitted clocks. L is the actual graph operator,
not T1's selected-memory comparison H_tilde and not the W/S model.

X1 proves that K has compact resolvent, operator domain H2 intersect the
physical invariant space, form domain H1 intersect that space, and smooth
invariant Peter-Weyl core. Bounded invariant multiplication preserves its
operator and form domains. The vacuum Omega is the unique electric ground;
the complete physical electric excited spectrum is at least 3. All these
facts apply beyond any spin cutoff. The finite projection P used here is
both X1's degree<=4 projection and its kinetic-energy<9/2 projection. It
commutes with gauge averaging and K and preserves their closed domains.
Its exact orthonormal basis is Omega and phi_p=2x_p for the 20 faces.

The retained matrix A=PLP is actually assembled and rechecked:

    A00=c,   A0p=Ap0=-lambda/2,   Apq=(3+c) delta_pq.

It has 19 face-difference eigenvectors of eigenvalue 3+c and a two-vector
vacuum/symmetric-face block. This is a symmetry decomposition of A, not
an invariant finite sector of L.

Newton's analysis/synthesis method motivates the sufficiency checklist.
Tesla's whole-mechanism method motivates the full omitted-channel audit.
Historical resonance or symbolism supplies no modern theorem premise;
there is no new historical claim or claimed historical endorsement here.

## 2. Exact Ritz state and the full residual

Define, without subtractive numerical evaluation when computing kappa,

    s=sqrt(9+20lambda^2),  d=(s-3)/2,
    mu=c-d,              kappa=lambda/(3+d),
    N0=(1+5kappa^2)^(-1/2),
    phi=N0 (Omega+kappa X).

The Haar identities <X>=0, <X^2>=5 and KX=3X give ||phi||=1. The algebraic
relations d=5lambda kappa and (3+d)kappa=lambda show Aphi=mu phi. It is
the simple finite ground: its gaps are gamma_dark=3+d, multiplicity 19,
and gamma_bright=s, multiplicity one. At lambda=0 take kappa=d=mu=0.
All vectors in this calculation are smooth physical polynomials in D(L^2).

Applying the *full* L rather than its compression yields the exact residual

    r=(L-mu)phi = -N0 lambda kappa (X^2-5).                (1)

It is orthogonal to the whole retained space P, not just to phi. The
constant projection is removed by 5; the face projections vanish by the
actual three-face center-parity rule. A wrong negative face coefficient
in phi instead leaves the nonzero retained X coefficient -2lambda before
normalization, so its small residual claim is rejected.

## 3. Complete omitted channels from SU(2) Haar integration

For every face let chi_p=4x_p^2-1 be its normalized spin-one character.
For every unordered pair p<q let eta_pq=4x_p x_q. These are physical,
normalized vectors. To prove the pair normalization even when faces share
an edge, integrate a link unique to p first and a link unique to q second:
each integration of the squared half-trace is 1/4, hence
<x_p^2 x_q^2>=1/16. No false independence of shared links is needed.

Distinct chi_p are orthogonal by different complete spin-one edge labels.
Every eta_pq has center parity mask boundary(p) XOR boundary(q), which is
nonzero and is not a single face mask. The actual graph enumeration finds
all 190 such pair masks distinct: no four distinct face boundaries have
XOR zero. Thus different pair channels are orthogonal, and every pair
channel is orthogonal to the even-parity spin-one channels and to P.
This proves a complete orthogonal decomposition of the residual vector,
not completeness of the whole infinite omitted Hilbert space:

    X^2-5 = (1/4)sum_p chi_p + (1/2)sum_(p<q) eta_pq.

Consequently

    ||X^2-5||^2 = 20/16 + 190/4 = 195/4,
    rho^2 := ||r||^2
       = (195/4) lambda^2 kappa^2/(1+5kappa^2).            (2)

A second exact formulation expands the fourth moment. The 20 equal-face
terms contribute 20/8, the 6*190 two-pair terms contribute 6*190/16, and
all other parity types vanish. Thus <X^4>=295/4 and subtracting 25 again
gives 195/4. The checker executes both formulations using the actual graph.

The spin-one-only squared residual retains just 1/39 of (2), missing all
190 face-pair channels. Its nonzero coefficient was a useful X1 witness,
but it was not a complete residual estimate. All relevant products are
included here, including pairs that touch through an edge or vertex and
pairs with disjoint edge sets. No generic finite block fixture is used.

## 4. From residual to the actual energy and ground projection

Let epsilon=min spec L and G its ground projection; let G_R=|phi><phi|.
The actual operator satisfies L>=K and has compact resolvent. Min-max and
the vacuum trial vector give epsilon<=mu<=c<=1/5, actual second eigenvalue
>=3, and a simple ground. The required spectral separation is

    h=3-mu>0.

Write delta=mu-epsilon>=0. The spectral measure of phi obeys
(E-epsilon)(E-3)>=0 on the full spectrum, so

    0 <= <(L-epsilon)(L-3)>_phi = rho^2-delta(3-mu).

Therefore the full-space Temple bound, derived here from its hypotheses,
is delta<=rho^2/h. Also the excited part of the residual has every
|E-mu|>=h, so

    ||G-G_R|| = ||(I-G)phi|| <= rho/h.                    (3)

These use the full physical excited spectrum, not a finite-matrix gap
substituted for an unproved full gap. The original domains and spectral
second moment justify the expectation identity.

A useful positive lower bound on delta proves an actual centering
difference. Each product in (1) has link label n=2j<=2 and total degree
sum n<=8. Since n(n+2)/4<=n for n=0,1,2, its entire kinetic support lies
at K<=8. For lambda>0 put u=r/rho. It is orthogonal to phi and

    <u,Lu> <= M:=8+40lambda,     <phi,Lu>=rho.

The smaller eigenvalue of this actual two-vector variational compression
bounds epsilon from above. With D=M-mu>0 and
sqrt(D^2+4rho^2)<=D+2rho, it follows that

    rho^2/(M-mu+rho) <= delta <= rho^2/h.                 (4)

The lower bound is strictly positive for lambda>0. At lambda=0 both
bounds are zero without dividing by rho. This is a variational extension
using the *complete actual residual*, not an artificial toy matrix.

At lambda=1/100 the exact/enclosed execution gives

    mu                 approximately 0.19983334259156393,
    rho^2              <= 5.415765e-8,
    6.6042686e-9        <= delta <= 1.9340864e-8,
    ||G-G_R||          <= 8.3108605e-5.

The full rational intervals, rather than these rounded display values,
are authoritative in results.json. Multiplying energy/residual quantities
by alpha restores physical units. Projection and heat errors are
dimensionless; h is not a fitted physical clock or a continuum mass gap.

## 5. Late-time heat on all physical input vectors

Define S(sigma)=exp[-sigma(L-epsilon)] and the zero-extended finite
S_R(sigma)=exp[-sigma(A-mu)]P. The actual gap is at least 3-epsilon>=h.
The finite excited gap is 3+d. Spectral calculus therefore gives on the
whole infinite-dimensional physical Hilbert space

    ||S-S_R|| <= rho/h + exp(-h sigma)+exp[-(3+d)sigma].   (5)

This compares the operators centered by their own genuine ground energies.
It includes their distinct ground projection limits as sigma tends to
infinity. At the coupling cap, (5) is below 8.424509e-5 for all sigma>=5.
Compression by J can only decrease this norm. This statement has a
different input class and time set from X1 reverse's retained-input
finite-window bound; their numerical examples are not combined.

The formulas also certify the entire frozen coupling range. Indeed
kappa'=6/[s(3+s)]>0, d'=10lambda/s, and mu'=20-d'>0 on the range.
Thus rho, mu and rho/(3-mu) increase with lambda. Use their endpoint bounds
and gamma_dark>=3. Including the uniform arithmetic certificate below,

    sup_(0<=lambda<=1/100, sigma>=5) ||S-S_evaluated||
        < 8.42454e-5 < 0.000085.                         (6)

No additional physical loop or model matching enters this range extension.
At sigma=0, S=I while the finite operator is P, so the full-space norm error
is exactly one; a normalized excluded spin-one face witnesses it. At
lambda=0 the energies and ground projections agree, but full heat still
has excluded free modes. Its error is exp[-(9/2)sigma], because a fundamental
six-cycle realizes the first excluded electric level. Zero ground error
does not mean zero full heat error.

## 6. Actually evaluated finite spectral representation and arithmetic

Let P_b be the projection onto Omega and the normalized symmetric face
sum; P_d=P-P_b. An exact finite spectral representation is

    S_R = G_R + exp(-s sigma)(P_b-G_R)
                  + exp[-(3+d)sigma] P_d.               (7)

In the original 21 basis its ground projection has just three entry types:

    (G_R)00=1/(1+5kappa^2),
    (G_R)0p=kappa/[2(1+5kappa^2)],
    (G_R)pq=kappa^2/[4(1+5kappa^2)].

The checker encloses square roots with integer arithmetic at denominator
10^24. It uses midpoint rational kappa_hat to form the *exact rational
rank-one projection* G_hat from those three formulas, and verifies
G_hat^2=G_hat and trace G_hat=1 on all 21 dimensions. Rounded positive
gaps s_hat and (3+d)_hat accompany that projection. The constant ground
coefficient remains exactly one. This is an actually evaluated small
calculation, not an existence statement for unknown high-cutoff coefficients.

For kappa and kappa_hat the rank-one angle formula gives
||G_R-G_hat||<=sqrt(5)|kappa-kappa_hat|<=(9/4)|kappa-kappa_hat|.
For positive a,b, bounded Duhamel gives
sup_sigma |exp(-a sigma)-exp(-b sigma)|<=|a-b|/min(a,b).
Using (7), a ground coefficient difference costs only the projection
error; the two gap errors have the displayed scalar bounds. No growing
sigma times a rounded *ground* energy is silently discarded.

The scalar time evaluator is also explicit. For 0<=x<=96 it bounds exp(x)
by its degree-160 Taylor polynomial plus the positive geometric remainder
x^161/[161!(1-x/162)], reciprocates, and rounds outward at denominator
10^30. It returns the midpoint. The polynomial is at least x^80/80!, so
the reciprocal interval's unrounded width is uniformly at most

    96 (80!)^2/[161!(1-96/162)].

After outward rounding the scalar error is <3e-30. For x>96 it returns
zero, whose error is <=80!/96^80<3e-30. Thus this is an all-time evaluated
representation with a uniform scalar certificate; it does not rely on
sampling finitely many times. The positive excited spectral projections
are orthogonal, so the two scalar errors cost their maximum, not a
dimension-dependent matrix-entry sum.

Uniformly over the coupling range the combined projection, positive-gap
rounding and scalar evaluation error is <3e-25. This is separate from the
roughly 8.4e-5 physical truncation bound. results.json contains rational
entry classes of the actually evaluated 21-state heat at sigma=5, along
with full exact matrix coefficients, residual channels, energy intervals,
projection bounds and late-time certificates at sigma=4,5,10. Floating
point is not used to admit any inequality. No statistical or sampling
uncertainty is present in these deterministic calculations.

If one instead centers the full L by mu, its true ground factor grows
as exp(delta sigma); (4) proves delta>0 at positive coupling. Independently
rounding any centered operator's ground exponent upward causes growth,
while rounding it downward loses its unit ground limit. Such a shift is
not the representation (7), and is explicitly rejected.

## 7. Checks, source scope and remaining limits

Fifteen controls include the complete 210-channel norm, the omitted-pair
failure, wrong normalization and Ritz sign, invalid separation, positive
and negative ground rounding, exact rational projection, scalar tail,
lambda-zero exceptions and the time-zero obstruction. They use explicit
exceptions, not assertions, and normal/-O runs must agree byte-for-byte.
The primary model is the actual graph; no generic finite algebra fixture
substitutes for its gauge, Haar or residual statements.

All X2 contract dependencies were read: Q2/T2 and X1 reverse were retained
from the prior turn; X1 forward, skeptical review, decision and admission
record were inspected for this loop. The frozen instruction snapshots,
including the newly added W residual/iteration lesson, were applied.
W's numerical constants are not used here. The Newton/Tesla historical
research references and supplementary domain/centering guidance read in
X1 remain frozen inherited method inputs, not newly verified primary
historical sources. The source-binding inventory records reading depth.
No new outside mathematical or historical lookup was needed; all new
claims above are derived from the named admitted premises. Scientific
priority remains unverified.

The useful late-time full-graph target is certified with a genuinely
manageable sector. This does not prove accurate earlier-time full-input
evolution, a relative error, real-time control, efficient large-volume
scaling, measured energy calibration, a homogeneous mass gap or a
four-dimensional continuum construction. No Y/Z work is selected or
executed by this producer.

    python3 -B research/round24/reverse/x2/check.py --output /absolute/fresh/x2-reverse
    python3 -B -O research/round24/reverse/x2/check.py --output /absolute/fresh/x2-reverse-O

Each invocation writes exactly results.json and controls.json. The
submission binds the contract, every declared dependency and instruction
snapshot, actual additional inherited inputs, this report, executable,
source inventory and both frozen outputs. Prior X1 bytes remain unchanged.
