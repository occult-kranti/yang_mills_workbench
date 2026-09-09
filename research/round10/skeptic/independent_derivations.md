# Independent derivation before reviewing production code

## Model and reduction

Take a single oriented cycle with four vertices and four SU(2) links, product Haar measure, and independent gauge transformations at the four vertices. Gauge fixing three tree links to the identity leaves the holonomy of the fourth link, with residual conjugation. The gauge-invariant Hilbert space is therefore unitarily identified with the central functions in L²(SU(2), Haar). This is an exact reduction of this finite graph, not a reduction of the complete spatial lattice to independent plaquettes.

The spin-j character is orthonormal in the class-function space. The electric Casimir on each of the four links acts as j(j+1), so alpha times the sum of four Casimirs has eigenvalue 4 alpha j(j+1)=alpha n(n+2), with n=2j. Multiplication by half the fundamental trace is cos(theta); the character product identity gives its matrix elements one half immediately above and below the diagonal. Thus the Hamiltonian with magnetic potential lambda(1-cos(theta)) has diagonal alpha n(n+2)+lambda and off-diagonal -lambda/2, n>=0.

The radial Haar measure is (2/pi) sin²(theta) dtheta. The unitary transformation u(theta)=sqrt(2/pi)sin(theta)f(theta) gives

    H u = -alpha u'' + [lambda(1-cos(theta))-alpha]u,

on (0,pi), with Dirichlet boundaries and the standard H² intersection H¹_0 operator domain. For alpha>0 and any finite real lambda this is a regular one-dimensional Schrödinger problem: compact resolvent, a simple positive ground-state wavefunction, and strictly ordered eigenvalues. These facts establish a positive gap for each fixed parameter pair on this finite graph. They supply no bound uniform in increasing spatial volume.

At alpha=0 the operator is multiplication by a continuous potential: for lambda>0 its spectrum is [0,2 lambda], the bottom is not an L² eigenstate, and there is no isolated vacuum gap. At alpha=lambda=0 every state has energy zero. This boundary cannot be included by continuity in a claimed uniform positive-gap theorem.

For lambda=0 the spectrum is exactly alpha n(n+2) and the first gap is 3 alpha. For negative lambda, reflection theta -> pi-theta gives E_k(-lambda)=E_k(lambda)-2 lambda for positive lambda. The gap is an even function of lambda, although the physical study may restrict lambda>=0.

## Infinite-tail lower enclosure

Let P retain n=0,...,N-1 and Q retain n>=N, N>=2. For alpha>0 and lambda>=0 the magnetic multiplication operator is nonnegative, so QHQ >= tau Q, tau=alpha N(N+2). P H Q couples only the boundary vector n=N-1 to n=N, with magnitude c=lambda/2. Take a rational U such that mu_1(A)<U<tau, A=PHP, and set delta=c²/(tau-U).

For every (p,q) in the quadratic-form domain, Young's inequality bounds the interface term below by -delta|p_(N-1)|² -(tau-U)||q||². Consequently

    H >= [A-delta P_boundary] direct_sum U I_Q.

Since the first two finite eigenvalues of A-delta P_boundary are below U, the min-max principle gives

    eig_k(A-delta P_boundary) <= E_k(H) <= eig_k(A), k=0,1.

If rational finite-matrix eigenvalue intervals are L_k^-<=eig_k(A-delta P)<=L_k^+ and A_k^-<=eig_k(A)<=A_k^+, then

    L_1^- - A_0^+ <= E_1(H)-E_0(H) <= A_1^+ - L_0^-.

The lower gap can be negative for a coarse N without invalidating the enclosure. Increasing N may sharpen it. A positive interval endpoint must be obtained from proved rational brackets, not by rounding a floating eigensolver output and calling it certified.

## Dynamic coefficients

For differentiable prescribed alpha(t),lambda(t) and unitary evolution under the same Hamiltonian, d<H>/dt = alpha'(t)<K> + lambda'(t)<V>. The state commutator contribution cancels because the generator and measured Hamiltonian coincide. If alpha is fixed, only lambda'<V> remains. This is external source work, not energy conservation of a closed system. A dynamical physical field would require its own action, kinetic term and backreaction; no such field is created by changing a coefficient in time.

## Independent-verification strategy

Finite-matrix interval checks will use a dense rational congruence inertia implementation, with symmetric pivoting and 2x2 pivots where needed. This avoids importing the producer's tridiagonal Sturm recurrence. A separate finite-difference radial calculation tests the graph normalization and first-gap trend. Neither ordinary floating-point finite differences nor high-precision values are promoted to interval arithmetic.
