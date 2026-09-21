# Z1 reverse: actual retained inputs obstruct uniform relative heat accuracy

**Result.** For every fixed 0<lambda<=1/100, the actual 21-state Ritz
approximation has unbounded all-time, all-retained-input relative vector
error when the denominator is the norm of the true evolved vector.
The proof uses the actual physical retained vector `(L-epsilon)Omega`.
A second vector, the fully computed Ritz bright state `(A-mu)Omega`, has
true-denominator relative error tending to one. Thus the obstruction is
visible without numerically preparing the exact-energy-dependent first
vector. It is compatible with X2's small absolute late-time error.

At lambda=1/100 and sigma=6, the first normalized witness has relative
error greater than 4.84; the computed second witness has relative error
between 0.9485 and 1.0515. The time is exactly 6 hbar/alpha. At lambda=0
the two evolutions agree on every retained input, and the relative error
is zero at every finite time. These distinct quantifiers are essential.

This is an independent reverse model-agent derivation. No current
forward/z1 solution was read or exchanged before freeze. Prior X2 findings
are shared admitted premises, not independent physical observations or
outside peer review. No Z2 is selected or executed here.

## 1. The relative question and its nonzero denominator

Use precisely the X2 physical SU(2) graph, product Haar measure, all vertex
Gauss constraints and full infinite-dimensional physical Hilbert space.
Set

    L=H_lambda/alpha=K+cI-lambda X,  c=20lambda,
    X=sum_(20 faces p) x_p,  x_p=Tr(U_p)/2,
    P=1_[0,9/2)(K), A=PLP on P H_phys.

P has the actual orthonormal basis Omega=1 and phi_p=2x_p, dimension 21.
It commutes with gauge averaging and K, preserves the operator and form
domains, and contains smooth invariant polynomials. X2 supplies the
complete all-sector ground construction: L is self-adjoint on D(K),
has compact resolvent, simple ground epsilon, and excited spectrum >=3.
All vectors below belong to that domain. A is the actually assembled
physical matrix, not a two-state system substituted for the full graph:

    A00=c,  A0p=Ap0=-lambda/2,  Apq=(3+c)delta_pq.

Let mu be its ground eigenvalue, and G,G_R the respective rank-one ground
projections of L,A. Define the separately centered operators

    S(sigma)=exp[-sigma(L-epsilon)],
    S_R(sigma)=exp[-sigma(A-mu)]P,
    sigma=alpha t/hbar >=0.

For every nonzero f in P H_phys and finite sigma, define

    R_true(sigma,f)=||(S-S_R)f||/||Sf||.                  (1)

The denominator is strictly positive: the spectral multiplier
exp[-sigma(E-epsilon)] is positive at every finite E, so its spectral
integral against a nonzero vector cannot vanish. This uses injectivity,
not a uniform lower spectral bound on heat. The denominator can tend to
zero as sigma tends to infinity. The tested uniform claim is a finite
bound on sup_(sigma>=0) sup_(f in P, ||f||=1) R_true(sigma,f).

At sigma=0 both evolutions equal f for this retained input class, so (1)
is zero. X1's full-input rank obstruction at zero time is not a Z1
counterexample. An excluded spin-one face is not admitted as a Z1 input.
Dividing an operator-norm error by ||S||=1 would instead reproduce an
absolute error and would not answer (1).

Keep the fixed positive a,E_star,alpha/E_star,hbar and constant coupling
0<=lambda<=1/100. No coefficient is inserted in the action or clock.
The selected input and any overlap restriction are approximation-protocol
choices. This is the actual T graph; its constants are not transferred to
canonical Y/V or homogeneous W/S dynamics.

## 2. Actual Ritz and full-ground information

Write the admitted exact Ritz quantities as

    s=sqrt(9+20lambda^2),  d=(s-3)/2,
    mu=c-d,  kappa=lambda/(3+d),  N0=(1+5kappa^2)^(-1/2),
    phi_R=N0(Omega+kappa X),  G_R=|phi_R><phi_R|.

Here <X>=0, ||X||_Haar^2=5, and KX=3X. The two scalar identities
`(3+d)kappa=lambda` and `d=5lambda kappa` give the actual Ritz ground
equation. The bright excited gap is s and the other 19 gaps are 3+d.

The complete X2 residual is

    (L-mu)phi_R=-N0 lambda kappa (X^2-5),
    ||X^2-5||^2=195/4.

Its 20 spin-one and 190 face-pair channels are all retained in this premise.
A spin-one-only calculation would keep 1/39 of the squared residual and
cannot supply the same spectral certificate. Let rho be its full norm,
delta=mu-epsilon, and h=3-mu>0. X2's actual spectral measure and residual
variational argument give, throughout the positive coupling range,

    0<delta_-:=rho^2/(8+40lambda-mu+rho)
          <=delta<=delta_+:=rho^2/h,
    ||G-G_R||<=D:=rho/h.                                (2)

We use reverse X2's coarser complete-kinetic-support lower bound. Forward
X2's sharper shared-edge energy moment was independently reviewed, but
is not relabeled as a new reverse result or needed for this obstruction.

Choose the normalized true ground psi with positive vacuum overlap a0.
That choice is possible: a ground orthogonal to Omega would have energy
at least 3, contradicting epsilon<=c<=1/5. The projection estimate gives
a useful quantitative lower bound:

    a0^2=<Omega,G Omega> >= N0^2-D >0.                   (3)

At the coupling cap, the checker encloses
delta_->6.6042686e-9, delta_+<1.9340864e-8 and a0>0.99993067.
The positivity in (2), not merely nonidentical full ground projections,
is the key additional actual-model fact.

## 3. An actual retained vector with unbounded true-relative error

The special identity `L Omega=c Omega-lambda X` lies wholly in P. Thus
the following is an actual retained physical vector:

    u=(L-epsilon)Omega=(c-epsilon)Omega-lambda X,
    n=||u||=sqrt[(c-epsilon)^2+5lambda^2],  v=u/n.        (4)

For lambda>0, n>=sqrt(5)lambda>0. Self-adjointness and the actual ground
equation imply <psi,u>=0, so Gv=0. The exact Ritz equation instead gives

    <phi_R,u>=(mu-epsilon)<phi_R,Omega>=delta N0,
    ||G_R v||=beta:=delta N0/n>0.                       (5)

This explicitly establishes different ground-overlap kernels on the
*retained* space. The statement G!=G_R alone would not prove it, because
different full-space projections can have proportional retained ground
vectors. Here (4)-(5) use the actual vacuum row and strict energy shift.
Equivalently, assuming Ppsi proportional to phi_R contradicts the vacuum
row of the ground equation by delta times its nonzero vacuum coefficient.

The actual excited heat satisfies ||Sv||<=exp(-h sigma). Ritz spectral
orthogonality gives ||S_R v||>=||G_R v||=beta. The triangle inequality
therefore yields the rigorous finite-time lower bound

    R_true(sigma,v) >= max(0,beta exp(h sigma)-1).        (6)

It diverges as sigma tends to infinity for every fixed positive lambda.
No division by a zero finite-time denominator and no hypothetical
two-level fixture enter the argument. The infinite complement is present
in the true epsilon, ground equation and full excited spectral bound.

The vector v uses the exact spectral quantity epsilon. Equation (4) is a
precise actual-model existence witness; an energy interval alone does
not numerically prepare a vector exactly orthogonal to the true ground.
We therefore give a separately computable witness next. This distinction
does not weaken the unrestricted all-input theorem, which includes (4).

For evaluated lower bounds, write c-epsilon=d+delta and use

    beta >= beta_- := delta_- N0 /
                         sqrt[(d+delta_+)^2+5lambda^2],

with interval endpoints chosen outward. At lambda=1/100,
beta_->2.9533546e-7 and h>2.8001666574. The exact/enclosed checker gives

| sigma | Lower bound on R_true(sigma,v) |
|---:|---:|
| 6 | 4.8465 |
| 7 | 95.1599 |
| 8 | 1580.5794 |

These are lower bounds from the full spectral argument, not simulated
trajectories or measurements of the relative error.

## 4. A fully computed retained bright witness

Using only the small actual matrix and its known ground, form

    w=(A-mu)Omega=d Omega-lambda X,
    n_R=||w||=sqrt(d^2+5lambda^2),  z=w/n_R.              (7)

For positive lambda this is a normalized actual physical retained vector,
computed from an algebraic square root. In the vacuum/symmetric-face
plane it is exactly the Ritz bright eigenvector:

    <phi_R,w>=0,   (A-mu)w=s w,   S_R z=exp(-s sigma)z.

It is not true-ground orthogonal. Since L Omega=A Omega,

    <psi,w>=(epsilon-mu)<psi,Omega>=-delta a0,
    ||Gz||=b:=delta a0/n_R>0.                           (8)

Hence ||Sz||>=b at every time. Reversing the triangle inequality on the
norm ratio gives

    |R_true(sigma,z)-1| <= exp(-s sigma)/b.              (9)

Thus R_true(sigma,z) tends to exactly one. This explicitly computed
witness already prevents any uniform useful relative tolerance below
one. At the cap, outward enclosures give b>2.9532319e-7 and

| sigma | Certified interval for R_true(sigma,z) |
|---:|---:|
| 6 | [0.9485, 1.0515] |
| 7 | [0.9974, 1.0026] |
| 8 | [0.99987, 1.00013] |

The alternative relative denominator ||S_R f|| is also well-defined
on every nonzero retained f at finite time. For the same computed z,

    ||(S-S_R)z||/||S_R z|| >= b exp(s sigma)-1 -> infinity.

At sigma=6 that alternative ratio is greater than 18.42. The two
denominators are named separately and never treated as interchangeable.

## 5. Centering, exact exceptions and compatible absolute accuracy

Every equation uses epsilon for the full heat and mu for the Ritz heat.
Centering the full L at mu instead gives an extra exp(delta sigma), with
actual positive delta. At sigma=1/delta_- its ground grows by more than
exp(1)>2. Centering A at epsilon instead damps its unit ground to less than
exp(-1)<1/2 at that same time. These are actual energy-shift controls,
not new physical clocks. A *common* scalar shift applied to both operators
multiplies a vector numerator and its matching denominator by the same
factor and cancels. A one-sided shift does not have that invariance.

At lambda=0, P reduces K and epsilon=mu=0, so Sf=S_Rf for every retained
f and every finite sigma. Both unnormalized witnesses (4),(7) vanish,
and dividing by their norms would be invalid. Their normalized limiting
direction is an electric face state, which has exact zero approximation
error at zero coupling. Also at sigma=0 every admitted retained input has
relative error zero. Neither exception supplies uniformity in positive
coupling and unbounded time; the order and range of these limits differ.

X2's small absolute late-time error remains valid. On (4) the true output
decays while a tiny erroneous Ritz ground component survives. On (7) a
tiny true ground component survives while the Ritz bright output decays.
These mechanisms explain how small absolute errors coexist with large
relative errors. They use the complete model's energy shift and overlaps,
not a failed upper-bound budget.

## 6. A useful repair candidate, without selecting Z2

The missing denominator can be controlled by a stated input condition.
If a normalized retained f obeys ||Gf||>=b0>0, then ||Sf||>=b0 and any
absolute error certificate A(sigma) implies R_true<=A(sigma)/b0. A
computable sufficient condition uses the known Ritz vector:

    |<phi_R,f>|>=a||f||,  a>D
      => ||Gf||>=||G_Rf||-D||f|| >=(a-D)||f||.            (10)

Thus the inherited X2 absolute theorem implies, conditionally,

    R_true(sigma,f) <=
       [D+exp(-h sigma)+exp(-(3+d)sigma)]/(a-D).         (11)

At the cap, a=1/10 and sigma>=5 give a sufficient bound below 0.000844.
The checker evaluates this direct inherited implication as a repair
candidate, without selecting or executing Z2. The overlap floor restricts
admissible inputs; it is not an action deformation or a fitted denominator.
It needs a verified preparation/overlap condition in any implementation.
A finite time window is another possible restriction, but no small
all-input finite-window relative certificate is asserted here.

## 7. Exact checks and source scope

The standard-library checker reconstructs the actual 21x21 matrix and
checks its Ritz and bright equations using exact arithmetic in
Q(sqrt(9+20lambda^2)). This verifies all original face coefficients and
the orthogonality identity, not just a chosen 2x2 numeric fixture. It
reconstructs the inherited complete residual normalization and evaluates
the actual energy and overlap bounds with rational square-root and
exponential enclosures. Floating point is not used for acceptance.

Thirteen controls include wrong witness sign, missing true-ground overlap,
the 39-fold incomplete residual, invalid gap, zero coupling, time zero,
wrong retained sector and one-sided centering. Explicit exceptions survive
Python -O. Each run writes exactly results.json and controls.json; normal
and optimized replays are compared byte-for-byte. All displayed decimal
claims are loose outward summaries of the rational certificates.

The frozen Z1 dependencies and instruction snapshots were read or retained
from the preceding work. X2 forward, its review and its advisor decision
were read after admission. The six prior gates were parsed for admission
status, reviewed scope and source inventory; their duplicated large
payloads are not new mathematical premises. The new complete-residual
instruction was read in full. The frozen Newton/Tesla methodological
references remain historical context, not modern proof authority. Their
workflow motivates the inverse-overlap question and complete-channel
checks, without a new historical or external-source claim.

No new primary-source lookup was needed for these explicit spectral and
matrix derivations from admitted premises. Scientific priority remains
unverified. The result concerns this finite physical graph and fixed
clock only; it gives no real-time, homogeneous, thermodynamic, continuum
or physical mass-calibration theorem. Prior accepted evidence remains
immutable and no Z2 production has begun.

    python3 -B research/round24/reverse/z1/check.py --output /absolute/fresh/z1-reverse
    python3 -B -O research/round24/reverse/z1/check.py --output /absolute/fresh/z1-reverse-O
