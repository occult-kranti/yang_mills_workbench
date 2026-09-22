# X1 forward: a gauge-compatible spectral truncation with a delayed all-time certificate

The actual finite T graph admits finite kinetic spectral projections and a
certified, separately ground-centered heat approximation in operator norm for
every **sigma >= tau > 0**. The approximation converges uniformly on that entire
delayed half-line as the cutoff increases. At sigma=0 every zero-extended finite
approximation instead has error exactly one. This is a topology obstruction, not
a large observed numerical error. The proof below includes all excluded sectors.

The checker constructs the actual 21-dimensional vacuum-plus-face compression,
including its exact magnetic coefficients and ground-energy enclosure. It also
executes rational error budgets for larger cutoffs. It does **not** assemble those
larger matrices or claim a practical high-accuracy implementation. The valid
replacement theorem is stronger than fixed-window strong convergence but has an
explicit positive starting time. The requested practical-truncation parent goal
therefore remains limited. Scientific priority is unverified.

Authorship: independent model-agent derivation. Current reverse/X1 and ongoing
W2 solutions were not read. Shared contracts and inherited mathematical premises
make this correlated project evidence, not external peer review. Newton's
analysis/synthesis motivates identifying the approximation topology first;
Tesla's complete-mechanism check motivates retaining the excluded return channel.
Neither historical analogy supplies a mathematical premise.

## 1. The physical space and the finite projection

Use exactly the open cubical graph with vertices
{0,1,2} x {0,1,2} x {0,1}, its 33 nearest-neighbour links and 20 square faces.
All 18 vertex Gauss actions are imposed, including the boundary vertices. Set

    Hphys = L2(SU(2)^33, normalized product Haar)^SU(2)^18,
    K = H_E/alpha = sum_e C_e,
    L = H_lambda/alpha = K + lambda V,
    V = 20 - sum_(p=0)^19 W_p, W_p = Tr(U_boundary(p))/2.

The fixed scales a,E_star,alpha/E_star,hbar are positive; sigma=alpha*t/hbar.
The dimensionless lambda lies in [0,1/100]. This is the actual H_lambda, not
T1's full-space leading-memory comparison Htilde. The cutoff R, starting heat
time tau, splitting time T and requested error eta are numerical/proof
parameters. They modify neither the action nor the clock.

For R>3 let P_R=1_[0,R)(K) on Hphys and Q_R=I-P_R. In the full product
Peter-Weyl decomposition an edge label j_e has energy j_e(j_e+1), and its
matrix-coefficient block has dimension (2j_e+1)^2. Each block is preserved by
left and right translations. Vertex gauge transformations are products of
these translations, so their averaging projection commutes with every block
and with K. Selecting sum_e j_e(j_e+1)<R and then the invariant tensors gives
the same orthogonal P_R whichever selection is performed first. Each j_e is
bounded, there are finitely many label tuples, and each invariant subspace is
finite dimensional. Thus P_R is an actual finite-rank orthogonal projection
on the complete physical space, not a matrix chosen by analogy.

The physical realization of K has domain H2(SU(2)^33) intersect Hphys, form
domain H1 intersect Hphys, and a smooth invariant Peter-Weyl core. Spectral
calculus gives P_R D(K) subset D(K), K P_R=P_R K on D(K), Q_R D(K) subset
D(K), and K|_Q >= R. The finite image consists of smooth functions. Since V
is a bounded smooth real invariant multiplier, 0<=V<=40, L is self-adjoint on
D(K), with the same form domain. The product elliptic resolvent is compact;
restriction to a reducing closed physical subspace and bounded perturbation
preserve compactness.

Write A=P_R L P_R on P_R Hphys, C=Q_R L Q_R on Q_R D(K), and
B=Q_R L P_R=lambda Q_R V P_R. These are genuine compressions. A>=0, C>=R,
and the actual full block domain is P_R Hphys direct-sum Q_R D(K).
Because Q_R I P_R=0 and ||V-20I||<=20,

    ||B|| <= b := 20 lambda.                                  (1)

No assumption that B vanishes is made. The choice b improves the naive bound
40lambda by removing a scalar only from the off-diagonal estimate. The scalar
20lambda remains in every diagonal operator and ground energy.

## 2. Exact t=0 obstruction and a complete finite-time tail bound

Let E(sigma)=exp(-sigma L) and E_R(sigma)=exp(-sigma A) P_R, with E_R
extended by zero to Hphys. Then E(0)=I and E_R(0)=P_R. The physical space is
infinite dimensional: normalized spin-j characters on one fixed square are
orthogonal invariant eigenvectors of K with energy 4j(j+1), unbounded in j.
An excluded such character gives

    ||E(0)-E_R(0)|| = ||Q_R|| = 1.                            (2)

Ground centering leaves (2) unchanged. The same obstruction holds after the
T selected compression J*: J*P_R J has finite rank on infinite-dimensional H3,
so ||I-J*P_R J||=1. Replacing the omitted dynamics by an identity is a different
approximation; it cannot be called the zero-extended finite heat operator.

On domain vectors the block variation-of-constants formula gives

    Q_R E(s) = exp(-s C) Q_R
               - integral_0^s exp(-(s-u)C) B P_R E(u) du.

The contraction property ||E(u)||<=1 implies

    ||Q_R E(s)|| <= exp(-Rs) + b/R.                          (3)

All integrals here are strongly continuous vector integrals, first obtained
on D(K) and extended by density and the displayed bounds. No norm-Bochner
integral or operator-norm Taylor series for K is assumed. In the P equation,

    P_R E(s)-E_R(s)
       = - integral_0^s exp(-(s-u)A) B* Q_R E(u) du.

Using (3) and the triangle inequality for the two output components gives

    ||E(s)-E_R(s)|| <= exp(-Rs) + 2b/R + b^2 s/R.            (4)

One may cap (4) by 2. The b^2 term is the return path through excluded
states. Omitting it would not follow from the block equations. At lambda=0
the exact error is ||exp(-sK)Q_R||=exp(-rho_R s), where rho_R is the first
excluded physical kinetic eigenvalue, rho_R>=R. At s=0 this is still one.

## 3. Ground energies and projections belong to the actual operators

The inherited all-sector Gauss argument gives the unique constant electric
ground Omega and the next electric eigenvalue 3. Briefly, an active spin
support has no vertex of degree one; a nonempty support contains a cycle,
and this graph's girth is four. Each active edge costs at least 3/4. An actual
square fundamental character attains 3. This is a full decomposition argument.

The Haar expectations <Omega,V Omega>=20 and V>=0 give, by min-max for L
and for A (P_R contains Omega and the energy-3 faces),

    0<=epsilon:=min spec L <= epsilon_R:=min spec A <= c:=20lambda,
    E_1(L)>=3, E_1(A)>=3,
    excitation gaps >= g:=3-c >=14/5.                       (5)

Both grounds are therefore simple. Let G and G_R be their rank-one
projections, with G_R extended by zero. Their eigenvalues are spectral
quantities, not fitted energy shifts. Put d=R-c>0. For a normalized actual
ground psi, the Q equation and C>=R give

    ||Q_R psi|| <= ell:=b/d.

P_R psi is nonzero because epsilon<R. Eliminating Q_R psi in its ground
equation yields the actual Schur term B*(C-epsilon)^-1 B. Comparing with
A>=epsilon_R proves

    0<=delta_R:=epsilon_R-epsilon <= b^2/d.                 (6)

This retains the minus-self-energy sign. Projecting the P equation onto
the excited space of A, where A-epsilon>=3-epsilon>=g, gives

    ||(P_R-G_R)psi|| <= b ell/g.

For rank-one projections their norm distance is the sine of the angle
between their unit vectors. Orthogonality of the two components then gives

    ||G-G_R|| <= ell sqrt(1+(b/g)^2)
                <= D_R:= (b/d)(1+b/g).                    (7)

Bounds exceeding one may be capped by one. These are conservative actual
all-sector estimates. Neither an assumed common ground nor the 21-state
example below is used to prove them.

## 4. Uniform centered approximation on every delayed half-line

Define the exact centered objects

    S(s)=exp[-s(L-epsilon)],
    S_R(s)=exp[-s(A-epsilon_R)] P_R.

Choose tau>0 and a splitting time T>=tau. Multiplying (4) by the necessary
centering factor, and bounding the difference of the two scalar exponentials
by s delta_R exp(cs), gives, throughout tau<=s<=T,

    ||S(s)-S_R(s)|| <= F_R(tau,T),
    F_R(tau,T)=exp(cT)[ exp(-R tau)+2b/R+b^2 T/R+T b^2/(R-c) ]. (8)

For s>=T the spectral gaps (5) instead give

    ||S(s)-S_R(s)|| <= ||G-G_R||+2exp(-g s)
                      <= D_R+2exp(-gT).                    (9)

Consequently the complete certificate is

    sup_(s>=tau)||S(s)-S_R(s)||
       <= min(2, max(F_R(tau,T), D_R+2exp(-gT))).            (10)

This is operator norm on all Hphys, so contraction under J gives the same
upper bound on the full selected H3. It is absolute, not a relative quotient.
It includes an arbitrarily long heat-time window and its nonzero ground
projection limit. First choose T to make the last exponential small and then
R to make F_R and D_R small. This proves

    lim_(R->infinity) sup_(s>=tau)||S(s)-S_R(s)||=0           (11)

for every fixed tau>0, uniformly in lambda in [0,1/100] using endpoint constants.
The order of this proof matters: at fixed T the right side of (10) retains
2exp(-gT); at tau=0 the exact obstruction (2) remains. No analogous all-time
unitary statement follows; real-time dynamics lacks the heat smoothing used
in (3) and (9).

Executed rational certificate: at the worst coupling 1/100, tau=1, T=4 and
R=1024, the checker encloses (10) strictly below 1/500. All positive/negative
exponentials used for that conclusion receive rational series bounds, not
floating-point point samples. Thus a finite matrix **exists** whose exact
centered heat is within 0.002 on t>=hbar/alpha. This run does not build that
matrix. The numeric bound is a rigorous existence/construction budget, not a
computed trajectory or a claim that a 21-state approximation attains 0.002.

## 5. An actually constructed 21-dimensional physical sector

For the cutoff R=9/2, P_R Hphys has the orthonormal basis Omega=1 and
phi_p=2W_p for all 20 faces. Completeness at this cutoff is provable. A
nonempty support with four edges is a square cycle; degree-two Gauss
invariance forces all four spins equal, so below 9/2 only j=1/2 is allowed.
A five-edge degree-at-least-two simple bipartite support is impossible:
with five vertices it would be an odd cycle; with at most four vertices its
bipartite edge bound is four. A support with at least six active edges costs
at least 9/2. Each square's invariant intertwiner is unique at every vertex.
The checker independently enumerates every four-cycle and finds exactly the
20 elementary faces.

Haar orthogonality gives ||phi_p||=1 and distinct face states are orthogonal
by a central flip of an edge in their symmetric difference. Every triple
face product has zero Haar integral: repeated faces leave one nonempty odd
parity set, and three distinct squares cannot have empty symmetric difference
on this graph. The checker exhausts all 20^3 ordered triples. It follows that
the exact physical compression, in this orthonormal basis, is

    A_00 = 20lambda,
    A_0p = A_p0 = -lambda/2,
    A_pq = (3+20lambda) delta_pq.                            (12)

These are the actual 21x21 coefficients, not a generic fixture. On the
19-dimensional face subspace whose coefficient sum is zero the eigenvalue
is 3+20lambda. On span(Omega, (1/sqrt20)sum_p phi_p) the two eigenvalues are

    epsilon_- = 20lambda + [3-sqrt(9+20lambda^2)]/2,
    epsilon_+ = 20lambda + [3+sqrt(9+20lambda^2)]/2.           (13)

At lambda=1/100 the checker encloses epsilon_- with rational square-root
bisection and verifies all entries and the invariant two-vector relations
using exact fractions. The finite ground energy is positive and strictly
below 20lambda. It is an upper bound on the actual ground by min-max.

This finite sector is not invariant under H_lambda. For a fixed face, the
actual spin-one character chi_1(U_p) has kinetic energy 8 and norm one.
The SU(2) character identity W_p phi_p=(1+chi_1(U_p))/2 gives

    <chi_1(U_p), L phi_p> = -lambda/2.                      (14)

Other faces are excluded from this matrix element by their nonempty central
parity. Thus (14) is an explicit omitted physical channel for positive lambda.
The checker verifies the exact character polynomial identity. Treating (12)
as the autonomous full physical system is rejected by an actual coefficient.

For general R a finite algorithm is explicit: enumerate the bounded spin
labels, form invariant tensors at every vertex by finite SU(2) coupling, and
integrate the Wilson-polynomial matrix elements. Equivalent polynomial Haar
Gram matrices and exact linear algebra avoid numerical gauge projection.
For rational lambda the coefficients are algebraic and can be enclosed by
algebraic-number isolation; Haar quaternion monomial moments are rational.
An orthonormal spin-network basis introduces only explicit algebraic factors.
This is a finite mathematical construction, not a cost estimate. At R=1024
each edge has j<=63/2, giving the loose pre-Gauss dimension bound
(sum_(n=0)^63 (n+1)^2)^33 = 89440^33. Energy and Gauss restrictions lower it;
this run does not compute the actual large-cutoff dimension or coefficients.

## 6. Numerical error and centering are separate obligations

(10) compares exact operators L and A. A numerical implementation must add
coefficient construction, ground/excitation spectral computation, and matrix
function evaluation errors. A sampled residual is not a certified integral.

A useful finite-matrix coefficient bound is available. If Ahat is Hermitian
on the same finite image with ||Ahat-A||<=kappa and 2kappa<g, the interpolation
A+u(Ahat-A) has ground gap h>=g-2kappa. Differentiating its separately centered
heat and writing it as ground projection plus decaying remainder makes the
ground-ground term vanish exactly. The two mixed terms integrate to at most
2kappa/h; the remainder-remainder operator and scalar terms each cost at most
kappa/(e h). Hence

    sup_(s>=0)||S_Ahat(s)-S_A(s)|| <=4kappa/(g-2kappa).       (15)

Here both finite operators are centered by their **own exact** ground energy.
The strong finite-matrix argument is a direct differentiation identity; it
does not silently bound an arbitrary approximate exponential routine. A
separately certified uniform evaluation error nu adds to (10)+(15).

Simply rounding epsilon_R to epsilon_R+zeta while otherwise leaving A fixed
cannot work uniformly on the half-line. On its ground vector the putative
centered heat is exp(s zeta). For zeta>0 it diverges; for zeta<0 it tends to
zero, giving a limiting error one. On a finite window one may instead use
the valid bound T|zeta| exp(T|zeta|). A viable all-time numerical spectral
representation must enforce an exactly zero ground exponent of the finite
approximate operator and separately enclose its projector and positive gaps.
The checker executes both signs of this discriminant on the actual finite
sector. No fitted physical clock is introduced.

## 7. Evidence, source reading, and the next missing premise

The standalone standard-library checker writes exactly results.json and
controls.json. Explicit exceptions, not Python assertions, enforce its
conditions. Normal and optimized replay must agree byte-for-byte. It tests
the actual graph/face compression, every triple parity, high-spin omitted
coupling, t=0, lambda=0, cutoff behavior, return/centering budgets, an invalid
gap denominator and the numerical shift obstruction. Exact fractions and
rational square-root/exponential enclosures are arithmetic evidence; the
written domain, completeness and all-time arguments supply the infinite-space
proof. No Monte Carlo, laboratory observations or high-cutoff trajectory are
reported.

Every X1 contract dependency/instruction is bound in submission.json, as are
the further inherited Q1 report/check source actually consulted and the
producer's own evidence. Mutable live project guidance and installed skills
are represented by immutable copies in inputs/, with source provenance. The
Q1 check was consulted through its graph construction and control code (first
210 lines); no Q1 code is imported or executed by this checker. The historic
Round23 handoff/roadmap was read for scope only; the current Round24 contract
and team instruction supersede its stop boundary.

Primary technical reading on 2026-09-21: Bauer, D'Andrea, Freytsis and
Grabowska, *A new basis for Hamiltonian SU(2) simulations*,
[arXiv:2307.11829v1](https://arxiv.org/html/2307.11829v1), abstract and
Introduction through the basis/truncation discussion (retrieved lines 58-80).
That text describes electric representation bases and their truncation, with
efficiency depending on the regime. It supports background/provenance only;
this report's particular cutoff theorem and constants are derived above.
The page's later rendered date is not treated as a new paper version. A v3
HTML URL returned 404; the opened version is v1. No complete comparison of
truncation literature or priority claim is made. Historical research references
were read from the installed skills, not independently reverified manuscript
by manuscript in this loop; no new historical factual claim is needed here.

The next useful step is to exploit actual sparse sector coefficients and
boundary residuals to obtain a materially cheaper certified cutoff, or to
design a numerical ground/projector representation with rigorous uniform
evaluation error. Neither task has been executed as X2. No real-time,
homogeneous-volume, continuum, mass-calibration or practical quantum-circuit
claim follows from this finite-graph heat result.

    python3 -B research/round24/forward/x1/check.py --output /absolute/fresh/x1
    python3 -B -O research/round24/forward/x1/check.py --output /absolute/fresh/x1-O
