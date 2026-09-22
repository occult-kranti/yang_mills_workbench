# X1 reverse: what an actual finite spin truncation can certify

**Scoped result.** A finite-rank approximation has an exact error of one at
time zero in full physical operator norm. This also obstructs the T selected
space's full operator norm, because that space is infinite dimensional.
The valid replacement proved here is a uniform finite-window, full-vector
error bound for *all retained low-degree initial states*, including separate
ground centering. The construction uses the actual 33-link SU(2) graph and
all Gauss constraints. Its degree-four sector has dimension 21 and an
explicit, exactly calculated magnetic matrix. It leaks to excluded physical
states; that matrix is not an autonomous sector of the full Hamiltonian.

This is an independent reverse reconstruction from the frozen X1 contract
and named inherited inputs. No current forward X1 or ongoing W2 output was
read. Independent implementations share the contract and inherited premises;
they are not independent physical observations or external peer review.

## 1. Backward requirements and the fixed model

To make a truncation certificate meaningful one must specify: the norm's
initial-state class, a gauge-compatible finite projection reducing the
electric domain, an estimate for all omitted transitions, and the energy
used to center both evolutions. A small exact matrix alone supplies none of
these missing implications. Newton's analysis/synthesis workflow motivates
this reconstruction. Tesla's whole-mechanism check motivates the explicit
excluded spin-one channel below. These are our modern mathematical uses of
the methods; historical analogy is not a premise.

Use the open rectangular grid with vertex sizes (3,3,2), 18 vertices,
33 edges, and all 20 elementary square faces. The gauge action is
g_e -> k_source g_e k_target^-1 at every vertex, with no external charges.
On the closed invariant subspace H_phys of L2(SU(2)^33, product Haar), set

    L = H_lambda/alpha = K + lambda V,
    K = sum_e C_e,       V = 20 I + W,
    W = -sum_(20 faces p) x_p,       x_p = Tr(holonomy_p)/2.

Here 0 <= V <= 40, ||W|| <= 20, and 0 <= lambda <= 1/100 is constant.
The dimensionless heat time is sigma=alpha t/hbar. Fixed a, E_star,
alpha/E_star, and hbar stay positive. No fitted clock or change of action
occurs. This is the actual H_lambda, not T1's separate H_tilde with a
modified complementary block. T2's 60 lambda^2 comparison is not a
truncation error and is not added to our estimate.

The inherited physical electric gap is 3: gauge invariance rules out a
nonempty active edge support with a degree-one vertex; the simple grid has
girth four; every nontrivial edge costs at least 3/4. The vacuum Omega=1 is
the unique zero state, and a normalized fundamental square character has
energy 3. This argument concerns every spin, not a tested finite list.

## 2. Actual projections, gauge symmetry and closed domains

Peter-Weyl decomposes a link into irreducibles j=n/2, n=0,1,..., with
Casimir n(n+2)/4 and matrix-coefficient space dimension (n+1)^2. The product
decomposition is a complete orthogonal sum over 33 integer labels n_e.
The vertex gauge representation acts within each label block because each
edge action is a left/right representation action. Thus Haar gauge
averaging commutes with every complete label-block projector.

Define d=sum_e n_e and P_N as the sum of the *whole gauge-invariant label
blocks* with d<=N, for an integer N>=0. This is a joint electric spectral
truncation; it is not necessarily a single total-energy interval. It has
finite rank, preserves every Gauss constraint, and increases strongly to I
on H_phys. Including entire representation blocks is essential. An open
single-link fundamental function changes sign under the central gauge
transformation at one endpoint and is not a physical retained state.

K is self-adjoint with the inherited smooth invariant Peter-Weyl core and
compact resolvent. In its label decomposition, its operator domain is

    D(K)={f: sum_labels E_labels^2 ||f_labels||^2 < infinity}.

Since P_N is a spectral sum, P_N D(K) is in D(K), KP_N=P_NK on that domain,
and P_N is also reducing for the closed form domain D(K^(1/2)). Its range
consists of smooth finite polynomials. Bounded real multiplication gives
D(L)=D(K), the same form domain and compact resolvent. The genuine finite
Galerkin generator is A_N=P_N L P_N restricted to P_N H_phys, with the
ordinary finite-dimensional domain. Its injection i_N back into H_phys is
used in every comparison. No projection is applied to the actual dynamics.

Multiplication by a fundamental matrix element changes a link spin only
to j+/-1/2, with the negative branch absent at j=0. A square multiplier
uses four different edges. Consequently W maps P_d into P_(d+4), and the
electric semigroup preserves P_d. This selection rule is all-sector
representation theory, not a claim inferred from the 21-state example.

## 3. Exact obstruction, then a useful finite-window target

Let U(sigma)=exp(-sigma L), U_N(sigma)=exp(-sigma A_N), and extend the latter
as i_N U_N P_N. At sigma=0 their difference is I-P_N and has norm exactly
one, for every finite N. Explicit witnesses exist: a square Wilson
character of spin j=n/2 with 4n>N is normalized, gauge invariant, electric
energy n(n+2), and excluded. The centered evolutions have the same initial
obstruction. For the T selected Hilbert space H3, J*P_NJ is finite rank,
so I_H3-J*P_NJ likewise has norm one. Neither statement is an inference
from an unsuccessful upper bound. For real-time full-space unitary
evolution the distance to any finite-rank operator is at least one at
every time, by testing its kernel; no real-time approximation is claimed.

Instead fix d0<=N and a physical observation window 0<=sigma<=S<infinity.
The target is the operator norm from P_d0 H_phys to *all* H_phys. Set

    r=floor((N-d0)/4)+1,    z=20 lambda sigma,
    T_r(z)=sum_(n>=r) z^n/n!.

For fixed sigma, the bounded-perturbation Dyson expansion around
K+20lambda I converges in operator norm; its simplex integrals are defined
strongly on vectors.
Each n-interaction term has norm at most e^(-z) z^n/n!. For n<r, all
intermediate degrees remain <=N, so the actual and Galerkin terms agree
on P_d0. Taking both remaining tails proves the full excluded-state bound

    ||(U-i_N U_N P_N)P_d0||
       <= min(2, 2e^(-z) T_r(z))
       <= min(2, 2 z^r/r!).                              (1)

The first cap uses the two positive-generator contractions. The factorial
relaxation follows from (r+k)!>=r!k!, not a sample of time points. All
paths that leave and return to P_N remain in the omitted Dyson tail;
none is declared absent. This is a heat-semigroup certificate, and no
operator-norm Taylor expansion of the unbounded generator is required.

## 4. Separate ground centering, with an explicit excluded-ground bound

Let epsilon=min spec L and epsilon_N=min spec A_N. Compact resolvent and
the vacuum trial vector give actual ground eigenvalues with

    0<=epsilon<=epsilon_N<=20lambda.

Since L>=K and A_N>=P_N K P_N, their second eigenvalues, whenever present,
are >=3. The ground is therefore simple and its excitation gap is
>=3-20lambda>=14/5. A one-dimensional A_N has a trivially simple ground.
The electric vacuum is only a trial vector, not the interacting ground.

A useful ground-tail certificate is much sharper in N than the generic
Schur energy estimate alone. For a normalized actual ground psi write
c=20lambda-epsilon>=0 and

    R_c = (K+c)^(-1) on Omega-perp, extended by zero on Omega,
    T = -lambda R_c (I-|Omega><Omega|) W,   ||T||<=a=20lambda/3.

Projecting (K+c)psi=-lambda Wpsi gives
psi=<Omega,psi>Omega+Tpsi. Since a<=1/15, the Neumann expansion converges
in Hilbert norm. R_c preserves every degree flag, and T raises degree by
at most four. Thus, with r_g=floor(N/4)+1,

    ||(I-P_N)psi|| <= tau_N = a^r_g/(1-a).                (2)

The coefficient |<Omega,psi>|<=1 was retained in proving this upper
bound. It is nonzero because a ground orthogonal to Omega would have
energy >=3, contrary to epsilon<=1/5. At lambda=0, tau_N=0.

In the actual block equation with x=P_Npsi, y=(I-P_N)psi, the offdiagonal
block B_N=(I-P_N) L P_N satisfies ||B_N||<=20lambda: the scalar 20 and K
have no offdiagonal block. A_N x=epsilon x-B_N* y gives, by Rayleigh-Ritz,

    0<=epsilon_N-epsilon
      <= 20lambda tau_N/sqrt(1-tau_N^2)
      <= delta_N := 20lambda tau_N/(1-tau_N).             (3)

Here tau_N<=1/14<1, so all denominators are positive. This bounds the
excluded actual ground, not just a finite-matrix eigenvalue error.
As a second, coarser sufficient estimate, (I-P_N)K(I-P_N)>=q_N with
q_N=max(3,3(N+1)/4). The Schur ground equation gives
epsilon_N-epsilon <= (20lambda)^2/(q_N-20lambda). These distinct estimates
are not combined as if they were independent measurements.

Define the separately centered operators E=exp[-sigma(L-epsilon)] and
E_N=exp[-sigma(A_N-epsilon_N)]. Multiplying the unshifted difference by
the *actual* exp(epsilon sigma), and treating the unequal energies
separately, gives

    ||(E-i_N E_N P_N)P_d0||
      <= min(2, 2 T_r(z)+1-exp[-sigma(epsilon_N-epsilon)])
      <= min(2, 2 exp(z) z^r/r! + sigma delta_N).         (4)

The scalar term has the displayed sign because epsilon_N>=epsilon. Both
centered generators are nonnegative. The estimate is valid uniformly for
0<=sigma<=S by replacing sigma with S. It vanishes exactly at sigma=0,
and throughout the window at lambda=0 on the retained input class.
For fixed S,d0, both terms tend to zero as N increases. On a growing
window S(N) one must explicitly check both terms in (4); there is no
all-time conclusion from this factorial finite-window majorant.

For example, at the worst coupling 1/100, S=1, d0=0 and N=20, r=r_g=6.
The exact/enclosed checker gives a sufficient centered error less than
1/1,000,000 on the vacuum input, with all degrees outside N retained in
the proof. This is a dimensionless error for 0<=t<=hbar/alpha, not an
assumed laboratory time. The high-sector N=20 matrix has not been
assembled or exponentiated in this loop.

## 5. An actual exactly computable finite sector, and its escaping channel

For N=4 the only nonconstant allowed labels have four active edges, all
j=1/2, forming a four-cycle. The actual grid's four-cycles are precisely
its 20 square faces. A bivalent invariant at each cycle vertex is unique.
Hence P_4 H_phys has the orthonormal basis

    Omega, phi_p=2x_p, p=0,...,19,    dimension 21.

The product of independent link Haar variables around a simple square is
Haar. Therefore int x=0, int x^2=1/4, and int x^4=1/8. Different faces
are orthogonal by edge-center parity. The checker independently enumerates
every four-cycle and every ordered triple of faces: no triple of their
edge parity masks has XOR zero. All triple-face Haar integrals vanish.
Consequently the *actual* 21 by 21 dimensionless Galerkin matrix is

    (A_4)00=20lambda,
    (A_4)0p=(A_4)p0=-lambda/2,
    (A_4)pq=(3+20lambda) delta_pq.                       (5)

There are 19 face-difference eigenvectors of energy 3+20lambda. In the
vacuum/symmetric-face subspace its two eigenvalues are

    epsilon_4=20lambda+(3-sqrt(9+20lambda^2))/2,
    e_plus   =20lambda+(3+sqrt(9+20lambda^2))/2.         (6)

Equation (5) is a true finite spin truncation, not a generic block
fixture. Its 2 by 2 diagonalization is an exact symmetry of A_4 only.
For each face, chi_(1,p)=4x_p^2-1 is a normalized spin-one character of
degree eight and electric energy eight. Exact Haar integration gives

    <chi_(1,p), L phi_p> = -lambda/2.                   (7)

Terms from other faces vanish by parity. Thus B_4 is nonzero for every
lambda>0, proving that (5) omits actual physical channels. Also
||W Omega||^2=5; using only the 19 Q2 complementary faces would give the
wrong vacuum coefficient here. This retains the distinction between the
full graph and its selected-memory compression.

There is also an actual centering distinction. Give the P_4 ground an
unnormalized vacuum coefficient one. Every face coefficient is
lambda/[2(3+20lambda-epsilon_4)]>0. For a fixed excluded spin-one face,
the only surviving matrix element from this vector is its matching
face coefficient times -lambda/2; the other spin-one face characters
have different Peter-Weyl labels and are orthogonal. Thus B_4 applied
to the finite ground is nonzero. Adding a small complementary component
with the opposite sign lowers its Rayleigh quotient linearly before
the quadratic cost, proving epsilon<epsilon_4 when lambda>0. The
ground-centering error is real, even though (3) only upper-bounds it.

The checker evaluates (5) with exact rational arithmetic, encloses (6)
with integer-square-root intervals, checks all 19 invariant difference
vectors, and calculates (7) from SU(2) class moments. It also checks the
ground-tail and window constants with rational arithmetic and an explicit
exponential Taylor remainder. None of these outputs is a simulated
trajectory, Monte Carlo sample, or full P_20 coefficient calculation.

## 6. Numerical error, controls and limits

Equation (4) compares the two *exact* operators. Suppose an implemented
matrix Ahat_N is Hermitian with ||Ahat_N-A_N||<=eta, and a numerical
ground estimate ehat_N satisfies |ehat_N-epsilon_N|<=eta_g. Bounded
Duhamel relative to the exact nonnegative centered A_N-epsilon_N gives
a further operator error <=exp[S(eta+eta_g)]-1, before numerical
exponentiation error. If that last error is <=xi uniformly on the window,
add xi. This remains true if Ahat_N-ehat_N has a small negative spectrum;
one must not use a contraction bound without that check. Initial-state
mismatch is separate as well. This loop supplies exact A_4 coefficients
and enclosures, not certified assembly costs or xi for a large matrix.

The controls reject: finite-rank full-space accuracy at t=0; treating a
finite low matrix as invariant despite (7); using the 19-face memory
coefficient in place of 20 physical faces; identifying 20lambda with the
actual finite ground despite (6); dropping the centering energy-error
term; and changing the physical window by changing alpha/hbar. The last
is an analytic units control: at fixed sigma a different alpha/hbar is a
different physical t, not a matched physical prediction. Lambda=0 and
time=0 on retained states are valid exact exceptions. The checker raises
explicit exceptions, so Python -O preserves its acceptance conditions.

The proved result is a finite-graph heat approximation with a specified
initial class and finite physical window, plus an exact full-space
obstruction. It is not a relative operator ratio, an all-time norm
truncation theorem, a measured clock calibration, homogeneous stability,
thermodynamic uniformity, a continuum construction or a novelty claim.
The next useful unresolved step is actual certified assembly and numerical
evaluation at a nontrivial cutoff, or a separate positive-time/full-input
or all-time/retained-input theorem selected after review. X2 is not
selected or executed by this producer.

## Reading depth and reproduction

Read completely: every X1 contract dependency and frozen instruction
input, root/team instructions, both installed method SKILL texts, their
historical research references, and the supplemental method snapshots in
inputs/. The historical source references are inherited corpus summaries;
this producer did not reopen primary historical texts and makes no new
historical assertion. Additional inherited proof inspection: Q1 forward
checker graph routine (lines 64-93), Q2 forward checker graph routine
(83-108), P2 forward report's opening graph/gauge convention (1-24), and
Q1 forward report's graph/face discovery matches. Their complete source
files are bound because their inspected passages guided graph identity.
No outside source or theorem lookup was needed: the modern claims above
are explicit derivations from the admitted Peter-Weyl, graph and bounded
perturbation premises. Priority is unverified.

The current X1 contract and prospective instruction snapshot supersede
historical solo/stop wording preserved in the supplemental snapshots.
Only frozen instruction bytes are bound; mutable live AGENTS and installed
skills are not new submission dependencies.

    python3 -B research/round24/reverse/x1/check.py --output /absolute/new/x1-reverse
    python3 -B -O research/round24/reverse/x1/check.py --output /absolute/new/x1-reverse-O

Each command writes exactly results.json and controls.json. The submission
binds the contract, all declared dependencies and instruction inputs,
additional inspected inherited proof sources, frozen supplemental inputs,
this report, the checker and its two frozen outputs.
