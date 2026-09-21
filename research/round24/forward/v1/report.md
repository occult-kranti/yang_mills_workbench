# V1 forward — exact finite outcomes and uniform readout error

Independent forward derivation, frozen before reading the current reverse solution. Historical Newton analysis/synthesis directs the backward question “what measurement preserves the signal?” and the forward error proof. Tesla's whole-device requirement separates spectral readout from access to the interacting evolution. Historical sources supply no operator-theory premises.

## Full-space statement and three outcomes

Use the U1/U2 canonical summable full-link SU(2) model exactly, including the physical invariant sector, states omega_q and dynamics beta_q. The eight-link local space is H_F=L²(SU(2)^8,dHaar), completed without a spin cutoff. Write u=Omega_F and v=psi_+ from U1: these are orthonormal gauge-invariant vectors. On H_F, W_F=|v><u|+|u><v|; on the full reference product representation W=W_F tensor I_out. The gauge-invariant bounded local algebra contains this operator. W is dimensionless and q-independent. Its nonzero eigenvectors are (u±v)/sqrt(2), with eigenvalues ±1. All other local vectors have eigenvalue zero.

Define full-space projections P_+=(W²+W)/2, P_-=(W²-W)/2 and P_0=I-W². Their positivity, orthogonality and sum I follow from W³=W and self-adjointness. Thus W=P_+-P_- has **exactly three outcomes** {-1,0,+1}; no spectral approximation is necessary. P_0 has infinite local rank. Every projection is gauge invariant and acts locally tensored with identity; the full dynamics and outside degrees of freedom are retained.

An ideal three-state pointer gives a concrete mathematical measurement dilation: V xi=sum_a P_a xi tensor |a>, so V*V=I and the pointer Born probabilities are omega(P_a). A controlled shift on a three-state pointer extends this isometry to a unitary. This is an operational specification in abstract quantum measurement theory, not a finite circuit synthesis or a laboratory implementation. Its finite number of outcomes is not a finite rank state space or a truncation of H_q.

For imperfect calibrated output labels r_a satisfying |r_a-a|≤delta, let A=sum_a r_a P_a. Then ||A-W||≤delta and ||A||≤1+delta, on the actual infinite Hilbert space. delta is a dimensionless readout accuracy; it changes neither action nor physical clock. Fixed labels give a q-independent A. Labels r_a=(1-delta)a for 0≤delta<1 are one explicit three-outcome implementation. Unknown projection/control errors must separately imply the same operator norm condition before the following bound applies.

## Uniform connected-correlation transfer

For any state omega, any automorphism beta and self-adjoint W,A as above, define C_A=omega(A beta(A))-omega(A)omega(beta(A)). This definition also covers nonstationary states. Positivity of a state gives |omega(B)|≤||B||. Add and subtract W beta(A):

    ||A beta(A)-W beta(W)|| ≤ delta(1+delta)+delta = 2delta+delta².

The product of means has the same bound, because |omega(A)|≤1+delta, |omega(W)|≤1, and the two individual mean differences are ≤delta. Consequently

    |C_A-C_W| ≤ 4delta+2delta².                         (V1.1)

In each stationary U2 state this is its inherited connected autocorrelation. Applying (V1.1) to q and 0 and using the reverse triangle inequality gives, simultaneously for every t and q<1,

    |C_(A,q)(t)-C_(A,0)(t)|
      ≥ |C_(W,q)(t)-C_(W,0)(t)|-8delta-4delta².         (V1.2)

No derivative, locality growth bound, continuity in operator norm of the evolution, or factor count is needed: unitary evolution is an isometry for bounded-operator norm. In particular the bound is uniform on the entire growing interval |t|≤T_q.

Retain z=C eta in (0,10^-6], T_q=C(hbar/alpha)(1-q)^-3, with fixed a,E_star,alpha/E_star,hbar. The inherited U2 margin is

    L(z)=z/84-(44/9)(80z/7)²/(1-80z/7)^5 > z/168.

Thus liminf endpoint difference for A is at least L(z)-8delta-4delta². For the explicit q-independent resolution delta=z/100000, the error is <z/10000 throughout this interval, and

    liminf |C_(A,q)(T_q)-C_(A,0)(T_q)| > z/200.         (V1.3)

This is an accuracy guarantee for each fixed chosen z; it is not a uniform positive margin as z→0. Exact W corresponds to delta=0 and retains U2's original bound. For A=(1-delta)W there is additionally the exact stronger identity C_A=(1-delta)² C_W. A scalar offset cI cancels from connected correlations; such an offset is not a discriminating negative control.

## A complex two-time readout is an additional operation

A pair of ordinary sequential projective W measurements need not yield omega(W beta(W)), which can be complex. Measuring the real product of two recorded outcomes always has a real mean and includes first-measurement disturbance. We do not infer an endpoint measurement protocol from the three-outcome spectral theorem alone.

There is an exact conditional finite-outcome interferometric protocol. Put K=W+iP_0. Since WP_0=0 and W²+P_0=I, K is unitary and W=(K+K*)/2. Therefore

    omega(W beta(W))=(1/4) sum_(s,r in {+,-}) omega(K_s beta(K_r)),
    K_+=K, K_-=K*.

Each product is unitary. With an ancilla prepared in |+>, a controlled product gives a reduced ancilla whose X and Y means are respectively the real and imaginary parts of the product expectation (with the displayed control convention |0><0| tensor I + |1><1| tensor U). Eight settings of binary ancilla readout recover the complex correlation. Single-time spectral readout supplies the mean; disconnected subtraction must use separately estimated means. This works also for mixed states by linearity.

The assumed resources are state preparation for omega_q, controlled K/K*, and controlled **actual** beta_q(K_r) at t up to T_q. The existence of these abstract bounded unitaries does not establish efficient synthesis, finite-volume dynamics error, experimental feasibility, or a q-uniform cost. Sampling uncertainty is separate from delta; no finite sample can give a deterministic exact expectation. We supply the exact measurement identity and operator-error transfer, leaving engineering and a sample/circuit-error budget open.

## Wilson obstruction in the declared norm

W is not Wilson multiplication. More strongly, on non-atomic Haar H_F no local multiplication M_g can approximate W_F with error less than 1/2. Let d=||W_F-M_g||. For any 0<m<||g||_infinity the set {|g|>m} has positive measure. Non-atomicity supplies an orthonormal sequence e_n supported there. Since W_F has finite rank, ||W_F e_n||→0; whereas ||M_g e_n||≥m. Hence d≥m and, taking m up to the essential supremum, d≥||g||_infinity. The triangle inequality 1=||W_F||≤d+||g||_infinity≤2d proves d≥1/2. Tensoring with the outside identity preserves the operator norm. The same argument applies on the local gauge-invariant completion using its non-atomic loop quotient; at minimum the full-link norm claim already excludes the stipulated full-link norm approximation. Gauge-invariant Wilson functions are included among multiplication functions.

This is a proved obstruction to this norm-approximation route. It says nothing about state-dependent weak approximations, nor whether a *different* Wilson-multiplication witness has an endpoint signal. Replacing the whole dynamics by its two-state compression remains unauthorized.

## Checks and scope

check.py uses exact rational arithmetic to verify the three-projection algebra, output-label perturbation, transfer constants and strict cap margin. A three-coordinate representation records u,v and one vector in the complement, verifying a finite algebraic identity; the preceding Hilbert-space argument, not this fixture, handles the infinite complement and actual evolution. Controls remove the signal, shrink labels, and expose the missing imaginary part of sequential readout. The multiplication obstruction is proved analytically using an infinite orthonormal sequence; a finite diagonal matrix fixture cannot certify it.

Primary technical reading: Allen et al., *A Tutorial on Quantum Dynamics Simulations on Quantum Computers. Part I: Closed Systems*, Yale-hosted author manuscript, Section 4.5, https://cqdmqd.yale.edu/sites/default/files/2024-04/quantum_dynamics_tutorials_PartI_0.pdf (accessed 2026-09-21). Consulted its Hadamard-test expectation-value framework; the displayed ancilla identity is derived here. It supports the readout primitive and does not prove the U2 model claim or its resource feasibility. The finite-spectrum and norm estimates above are self-contained standard operator arguments. Scientific priority is unverified.

Accepted forward scope: exact finite outcomes, uniform error transfer, and a norm-approximation obstruction for Wilson multiplication. Actual circuit implementation, finite sample certification, a Wilson witness, the homogeneous gap and four-dimensional continuum construction remain open.
