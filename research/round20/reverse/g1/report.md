# G1 reverse reconstruction: fixed-time operator convergence without norm time continuity

Return to the original lattice Hamiltonian with coefficient alpha. The external
finite-diffusion coefficient c from F does not occur. For any finite real tau,
`V=-alpha*tau*sum w_f x_f` is a bounded self-adjoint perturbation of H_ref;
smallness needed for a gap is unnecessary for this dynamics statement.

For unbounded self-adjoint H and K on a common reference domain with bounded
B=H-K, the Duhamel formula is a strong operator integral. Its norm estimate is

\[
\|e^{-itH/\hbar}-e^{-itK/\hbar}\|
\le |t|\|B\|/\hbar.
\]

The strong-integral formulation is deliberate: point-norm continuity of the
conjugated bounded perturbation need not hold. Applying the estimate to both
sides of a Heisenberg conjugation yields `2||A||||B||||t|/hbar`.

Fix a local bounded A and include both its support and V_M in a finite central
set of complete factors. In every sufficiently large literal box, the truncated
Hamiltonian is central K_M plus disjoint remote clipped references. Their
Heisenberg action on A agrees exactly with the infinite truncated action.
Bounding the finite omitted tail and the infinite omitted tail separately gives

\[
\|\alpha_t^{box}(A)-\alpha_t^\infty(A)\|
\le4\|A\||t|\epsilon_M/\hbar.
\]

Literal link operators embed canonically into the full factors of the A2
representation. Remote boundary vectors are irrelevant to this operator bound.
For each fixed physical t, the limit lies in the norm closure of local bounded
factor operators because the truncated action is local. Isometry, multiplication,
and the inverse time -t extend from these approximants, yielding an automorphism
for each t. The group law follows from the implementing Hilbert-space unitary
group, which is strongly continuous by self-adjointness. The convergence bound
is uniform on any fixed compact time interval, though it does not establish a
propagation velocity or a continuum limit.

Scalar boundary energy subtraction cancels exactly in Heisenberg conjugation:
`exp[it(H+cI)/hbar] A exp[-it(H+cI)/hbar]` equals the unshifted conjugation.
This is a valid exception to the E1 fixed-resolvent obstruction. It does not make
absolute energies or the unnormalized unitary operators invariant under the
shift.

Strong continuity of those unitaries must not be promoted to point-norm time
continuity on the full algebra of local bounded operators. On an actual free
SU(2) link, the normalized characters chi_n have Casimir energies
`E_n=alpha*n*(n+2)/4`. Define a bounded norm-one operator T by
`T chi_n=chi_(n+1)` and zero on the orthogonal complement of the character
subspace. Its Heisenberg matrix coefficients acquire phase
`exp[it*alpha*(2n+3)/(4hbar)]`. At

\[
t_n={4\pi\hbar\over\alpha(2n+3)}\longrightarrow0,
\qquad\|\alpha_{t_n}(T)-T\|=2.
\]

The lower bound follows by testing chi_n and the upper bound is twice ||T||.
At tau=0 this is already the actual original lattice dynamics. A bounded V
changes its evolution by at most `2||T||||V||||t_n|/hbar`, so the limsup remains
2 for every fixed finite tau. Thus this defect is not repaired by a small
summable perturbation. A norm-continuous observable subalgebra would require a
separate restriction.

The checker executes signed-time and signed-amplitude exact ledgers, the actual
SU(2) character spacing/phase identity, and all eight boundary support phases.
Missing hbar, replacement of original alpha by the F coefficient, insufficient
central support and incorrect promotion of scalar phase cancellation are kept
separate. Fixed-time norm convergence and strong Hilbert continuity are the
admitted outcomes.
