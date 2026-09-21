# Z1 forward: an actual retained physical input has unbounded relative heat error

For every fixed 0<lambda<=1/100, the all-time relative error of the 21-state
Ritz heat is unbounded when accuracy is required on **every retained input**
and the denominator is the norm of that input's true centered heat evolution.
The obstruction occurs on an actual vector in the vacuum/symmetric-face
plane. It is not the excluded-input, time-zero obstruction from X1.

At lambda=1/100 a fixed normalized retained witness has relative error greater
than 6.9 at sigma=6, and its lower bound grows exponentially thereafter.
A second, directly computable Ritz-excited vector has relative error tending
to one; at sigma=8 that error is within 0.0001 of one. Small X2 absolute
errors remain valid. They do not control division by a decaying true output.

Authorship: independent forward model-agent derivation. No reverse/Z1
solution was read. Shared premises and agent review are not external peer
review. The Newton method is used to define the relative inference before
fitting an error budget; the Tesla method is used to retain the true ground
component and every channel responsible for its displacement. No historical
analogy supplies a mathematical premise. Scientific priority is unverified.

## 1. Precise relative quantity, spaces, units and inherited facts

Keep the actual open (3,3,2) SU(2) graph, all 18 Gauss constraints, and the
full infinite-dimensional physical Hilbert space Hphys. Let

    L=H_lambda/alpha=K+lambda(20-S), S=sum_(20 faces p) W_p,
    P=1_[0,9/2)(K), A=PLP on P Hphys,
    epsilon=min spec L, mu=min spec A,
    E(sigma)=exp[-sigma(L-epsilon)],
    E_R(sigma)=exp[-sigma(A-mu)]P.

P Hphys has the orthonormal basis Omega=1 and phi_p=2W_p, dimension 21.
E_R is extended by zero to the full physical space. K and L have the same
self-adjoint domain, the smooth invariant polynomials are a core, and P
reduces K and its domain. All our inputs are smooth retained polynomials.
The actual true ground projection G and Ritz projection G_R=|f><f| are simple;
the full physical excited spectrum of L is >=3. These are X1/X2 all-sector
results, not a finite-matrix gap substituted into the full problem.

For each finite sigma>=0 define

    R_lambda(sigma)
      = sup_(0!=x in P Hphys) ||[E(sigma)-E_R(sigma)]x|| / ||E(sigma)x||.  (1)

The denominator is the true output norm **for the same input x**. It is
strictly positive: a self-adjoint heat operator has positive spectral
multiplier exp[-sigma(E-epsilon)] at every finite spectral energy and is
injective. For fixed finite sigma its restriction to finite-dimensional
P Hphys has a positive minimum singular value, by compactness of the unit
sphere. Thus (1) is finite at each finite time. The claim refuted below is a
bound uniform over all times, not the definition of a quotient at infinity.

Dividing instead by ||E(sigma)P|| is a different operator-norm ratio. It does
not impose relative accuracy on each input, and the obstruction here does
not refute that different quantity. Using ||E_R(sigma)x|| also changes the
question; its behavior is identified separately below.

The positive scales a,E_star,alpha/E_star,hbar are fixed and
sigma=alpha*t/hbar. All displayed energies are divided by alpha. Lambda is
constant in [0,1/100]. Denominator and input restrictions are approximation
choices, not action parameters or fitted physical clocks. The exact actual
and Ritz ground energies each remain in their own exponential. Htilde and
the canonical or homogeneous models are not used.

## 2. Actual Ritz equations and a certified positive energy displacement

Write c=20lambda, D=sqrt(9+20lambda^2), w=(D-3)/2. The actual matrix is

    A00=c, A0p=Ap0=-lambda/2, Apq=(3+c)delta_pq,
    mu=c-w,
    f=(Omega+h sum_p phi_p)/sqrt(1+20h^2),
    h=lambda/[2(3+w)], f0=<Omega,f>=sqrt[(D+3)/(2D)].         (2)

X2 computes its full residual in the actual graph:

    r=(L-mu)f=-(2lambda h/sqrt(1+20h^2))(S^2-5),
    rho^2=||r||^2=195lambda^4/[4(3+w)D].                    (3)

The factor 195/4 in ||S^2-5||^2 includes 20 spin-one faces and 190 two-face
products, with the shared-edge singlet/triplet branches retained. A spin-one-
only residual would understate rho^2 by a factor of 39. X2 also proves that
xi=-(S^2-5)/sqrt(195/4) has <xi,Lxi>=nu=236/39+c and <xi,Lf>=rho.
The reviewed variational/residual argument yields, for delta=mu-epsilon,

    d_low=2rho^2/[nu-mu+sqrt((nu-mu)^2+4rho^2)]
        <= delta <= d_high=rho^2/(3-mu).                  (4)

These are actual full-graph bounds. In particular delta>0 for every positive
lambda. Also 0<=epsilon<mu<=c<=1/5 and g:=3-mu>0 is a lower bound for the
true excitation gap. We re-enclose the radicals and constants independently
in this check; the complete physical residual proof remains the admitted X2
premise, not a newly claimed Z1 observation.

The particularly useful exact identity is

    L Omega=c Omega-(lambda/2)sum_p phi_p in P Hphys.       (5)

Thus (I-P)L Omega=0 even though (I-P)Lf is nonzero. Magnetic action on Omega
has only the constant and fundamental face components. This singles out an
actual physical input for the relative obstruction.

## 3. A fixed retained vector with no true-ground overlap

For lambda>0 take

    u=(L-epsilon)Omega
      =(c-epsilon)Omega-(lambda/2)sum_p phi_p.              (6)

It is a nonzero actual gauge-invariant retained polynomial, with

    ||u||^2=(c-epsilon)^2+5lambda^2.

It depends on the true spectral quantity epsilon; it is a mathematical
witness, not a claim that a finite laboratory routine prepares a perfectly
ground-orthogonal state from rounded energy data. Formula (4) encloses its
coefficient and all the constants used below. The next section provides a
fully computable alternative witness as well.

If psi is a normalized true ground, self-adjointness on the common domain
gives <psi,u>=< (L-epsilon)psi,Omega>=0. Hence Gu=0 and

    ||E(sigma)u|| <= exp(-g sigma)||u||.                   (7)

In contrast, by (5) and the Ritz eigen-equation,

    <f,u>=<f,(A-epsilon)Omega>=delta f0>0.                 (8)

Therefore ||E_R(sigma)u||>=delta f0 at every time. Reverse triangle inequality
and (7) show, with kappa=delta f0/||u||,

    ||[E(sigma)-E_R(sigma)]u|| / ||E(sigma)u||
        >= kappa exp(g sigma)-1.                          (9)

To justify the division step, the exact denominator is positive as proved
above; the reciprocal of (7) has the correct direction. A negative right
side at short times is merely an uninformative lower bound. For every fixed
positive lambda, kappa>0, so (9) proves

    sup_(sigma>=0) R_lambda(sigma)=infinity.               (10)

The normalized u/||u|| is fixed while time grows; no moving-input choice is
needed. For any requested finite bound M, times with
sigma >= g^-1 log[(M+1)/kappa] violate a strict bound below M. At lambda=0
this construction becomes the zero vector and is not divided by its norm.

This also proves that Ppsi cannot be parallel to f at positive coupling.
If it were, its Omega component in the true ground equation would have both
eigenvalues epsilon and mu, forcing delta<psi,Omega>=0. The vacuum overlap
is nonzero: L>=K>=3(I-|Omega><Omega|) implies

    |<Omega,psi>|^2 >=1-epsilon/3 >=1-mu/3>0.              (11)

The strict energy error in (4) therefore rules out that tempting missing-
ground-overlap assumption in this actual model.

## 4. A directly computable retained vector with relative error tending to one

Define a second input using only the exactly known Ritz energy,

    v=(L-mu)Omega=w Omega-(lambda/2)sum_p phi_p.            (12)

It is a nonzero retained physical vector for lambda>0. The matrix in (2)
and w(3+w)=5lambda^2 give

    Av=(mu+D)v, <f,v>=0,
    ||E_R(sigma)v||=exp(-D sigma)||v||.                   (13)

Yet its true ground overlap is nonzero:

    <psi,v>=(epsilon-mu)<psi,Omega>=-delta<psi,Omega>.

By (11), with

    eta=delta sqrt(1-mu/3)/sqrt(w^2+5lambda^2)>0,
    ||E(sigma)v|| >= ||Gv|| >=eta||v||.                   (14)

The reverse triangle inequality now proves a two-sided quantitative limit
for the primary denominator of (1):

    | ||[E(sigma)-E_R(sigma)]v||/||E(sigma)v|| -1 |
       <= exp(-D sigma)/eta.                              (15)

Thus the directly computable normalized Ritz-bright input has relative error
tending to one. It alone precludes a useful uniform relative tolerance below
one, even without constructing the true-energy witness u. The stronger
unboundedness statement uses u and is a separate consequence.

If the denominator were instead the Ritz output norm, (13)-(14) would give
the diverging lower bound eta exp(D sigma)-1 for this v. That is a different
relative quantity and is not substituted for (1) in proving (9)-(10).

## 5. Evaluated consequence, arithmetic and exact exceptions

The standard-library checker reassembles the actual 21-state matrix and
verifies the star-block polynomial relation and input membership. It encloses
D, rho, delta and the witness norms with rational square-root bounds. From
(4), c-epsilon=w+delta and positivity, one sufficient lower bound is

    kappa >= d_low f0 / sqrt[(w+d_high)^2+5lambda^2].       (16)

At lambda=1/100 the rational enclosures prove

    kappa > 4*10^-7, g>=14/5,
    eta > 3.86*10^-7,
    relative error on u at sigma=6 >6.9,
    |relative error on v at sigma=8 -1| <10^-4.            (17)

The stronger enclosed values are approximately kappa_lower=4.00213e-7,
eta_lower=3.86664e-7 and the u lower bound at sigma=6 is about 6.92269.
These decimal descriptions are secondary to the exact rational output.
Positive exponential Taylor partial sums provide lower bounds for (9);
positive Taylor bounds followed by reciprocals enclose the decaying
exponential in (15). No floating-point result admits a claim.

All bounds use the exact own-ground-centered definitions of E and E_R.
If L were instead centered by mu, its true-ground factor would grow as
exp(delta sigma), because (4) proves delta>0. That would change the problem.
The present obstruction remains even though both correctly centered heat
operators are contractions; it results from different ground overlaps and a
decaying denominator. There is no arithmetic-error floor in (9): the exact
mathematical u is defined by epsilon, and its reported interval does not
pretend that every nearby coefficient is exactly orthogonal to psi.

At sigma=0, E(0)x=E_R(0)x=x for every retained input, so (1) is exactly zero.
An excluded spin-one face would instead have full-space initial error one,
but it is outside this input class and is rejected as a Z1 witness.
At lambda=0, P reduces L=K, both centering energies are zero, and the two
operators agree on P at every finite time. Thus R_0(sigma)=0 identically.
The positive-coupling witnesses becoming zero at lambda=0 are not used to
erase this exact exception or manufacture a division by zero. A fixed-time
small-coupling limit is consistent with unbounded error at late times for
each fixed positive coupling.

## 6. Meaningful next repair and scope

The failure identifies a specific missing condition: a nonvanishing true
ground component on admitted inputs, or another explicit lower bound on
their evolved norm. For example, if an admitted input satisfies
||Gx||>=a0||x|| with a0>0, then ||E(sigma)x||>=a0||x|| and an absolute
operator certificate converts to a relative bound after division by a0.
Z2 could seek a checkable input condition from Ritz ground overlap and X2's
projection-distance certificate, together with a useful time window. It
would be a restricted approximation theorem, not a change of the action.
No Z2 target is selected or executed here.

This exact obstruction is for (1) on the declared finite graph. It is not
divergent physical heat, invalidity of X2's absolute bound, failure of every
relative norm, a claim about generic two-state toy dynamics, or a transfer
to the canonical/homogeneous or continuum models. The actual excluded
residual in (3)-(4) is essential to making the ground-energy displacement
and therefore the two overlaps strictly nonzero.

Current contract dependencies are source-bound. X2 reports, decision and
skeptical review were read for the complete residual and ground facts. The
six gate JSON records were parsed and inspected for their admission status,
source bindings and scope; their different models' dynamical constants are
not imported. All declared method snapshots, including x-complete-residual,
are retained. Previously read Newton/Tesla sources remain the frozen inherited
context; no fresh historical claim or primary-source priority comparison is
made. Earlier X1/X2 files are unchanged.

The standalone checker writes exactly results.json and controls.json, uses
explicit exceptions, and is replayed normally and under -O into fresh output
directories outside the repository. Its finite matrix verifies identities
of the actual retained compression; the self-adjoint spectral arguments above
establish the full-operator obstruction. Current reverse/Z1 material was not
read. This is a completed obstruction result, not a positive relative-accuracy
theorem or external peer review.

    python3 -B research/round24/forward/z1/check.py --output /absolute/fresh/z1
    python3 -B -O research/round24/forward/z1/check.py --output /absolute/fresh/z1-O
