# V1 reverse — reconstructing a finite readout without changing the dynamics

Independent model-agent reconstruction, frozen before reading the current forward solution. Shared U1/U2 premises remain correlated; this is not outside peer review. Newton's backward reconstruction asks what data suffice for the complex connected correlator. Tesla's loading check retains the complete system, the complement of the observed local subspace, and measurement disturbance. Historical or esoteric statements enter no equation.

## Endpoint first, and the necessary accuracy

Write H_j for the full canonical summable Hamiltonian, j=0,q, and beta_j^t(A)=exp(-itH_j/hbar) A exp(itH_j/hbar), in the frozen contract's convention. For a state omega_j define C_j^A(t)=omega_j(A beta_j^t(A))-omega_j(A)^2. The U2 target supplies, for z=C eta in (0,10^-6],

    liminf |C_q^W(T_q)-C_0^W(T_q)| >= L(z) > z/168,
    L(z)=z/84-(44/9)(80z/7)^2/(1-80z/7)^5,
    T_q=C(hbar/alpha)(1-q)^(-3).

All physical scales stay fixed. A q-independent Hermitian contraction A with ||A-W||<=delta satisfies, for every state and every real t,

    |C_j^A(t)-C_j^W(t)| <= 4 delta.                    (R1)

Indeed the product difference is (A-W)beta(A)+W beta(A-W), of norm at most 2 delta. The squared-mean difference is at most 2 delta. Automorphisms preserve norm, so no factor of T_q appears. Consequently

    liminf |C_q^A(T_q)-C_0^A(T_q)| >= L(z)-8 delta.    (R2)

In particular delta<z/1344 is sufficient. Delta is dimensionless observable error, not a Hamiltonian coefficient or physical clock. For an unconstrained self-adjoint approximation with ||A||<=1+delta the replacement is 8delta+4delta^2 in (R2). A strong or state-specific approximation at t=0 does not automatically supply the norm hypothesis in (R1).

## Exact three-outcome observable, on the entire Hilbert space

The inherited local factor is H_F=L^2(SU(2)^8,dHaar), before restriction to gauge-invariant states. Let o=Omega_F and p=psi_plus be the orthonormal invariant U1 vectors. Let P=|o><o|+|p><p| and W_F=|p><o|+|o><p|. On H_F define

    P_plus=(P+W_F)/2, P_minus=(P-W_F)/2, P_zero=I_F-P.
    W_F=P_plus-P_minus; W_F^2=P_plus+P_minus.          (R3)

These are pairwise orthogonal positive projections summing to the identity. They commute with every local gauge action because o,p are invariant. Extend all three by identity outside F. They form an exact q-independent local PVM with outcomes +1,-1,0, including the infinite-dimensional zero eigenspace. This has delta=0 in (R1). It is already finite outcome; no spectral cutoff or approximation to H_q was performed. The local rank-two part is not a finite-rank operator on the whole infinite system.

The binary POVM E_plus=(I+W)/2, E_minus=(I-W)/2 is another exact first-moment readout. Its outcome-square expectation is always 1, whereas omega(W^2) need not be 1. Thus it does not preserve variance by identifying outcome variance with operator variance. The three-outcome PVM does preserve both single-time moments. Neither single-time result specifies a real-time two-point measurement instrument.

## Finite binary settings for the complex two-point quantity

A two-time sequential PVM measurement changes the state. Its real outcome product need not equal the complex number omega(W beta(W)). For example on span{o,p}, W is sigma_x, U=diag(1,i), beta(W)=U W U*=sigma_y, and the state o has omega(W beta(W))=i. The outcome-weighted sequential PVM product is zero. The checker retains a third spectator coordinate to detect loss of P_zero. This is an algebraic counterexample, not a Hamiltonian trajectory or an approximation to H_q.

There is an exact abstract finite-setting protocol when coherent unitary control and preparation of omega_j are supplied. Put

    R_plus=W+P_zero, R_minus=W-P_zero.

Both are gauge-invariant local self-adjoint unitaries, and W=(R_plus+R_minus)/2. For each sigma,tau in {+,-}, let

    K_sigma,tau=R_sigma beta_j^t(R_tau).

These are unitary on the full Hilbert space, and

    omega_j(W beta_j^t(W)) = (1/4) sum_sigma,tau omega_j(K_sigma,tau).  (R4)

Initialize a two-level ancilla in |+>, apply controlled K, and measure ancilla X or Y. Its reduced state is (1/2)[[1,conj(omega(K))],[omega(K),1]], so the respective binary means are Re omega(K), Im omega(K). Four pairs times two quadratures give eight binary settings. The connected subtraction uses the three-outcome measurement's mean, estimated on separate fresh preparations. K=R_sigma U_j R_tau U_j* uses the **actual** full evolution with both time signs; an implementation needs this coherent control, or an independently verified equivalent circuit. No efficient implementation, laboratory instrument, finite-dimensional simulator, or bound on accumulated gate error at T_q is established here. Equation (R4) is an operational quantum-instrument definition under explicit capabilities, not a claim that those capabilities exist in the workbench.

If every component real/imaginary mean is known within r and the separately estimated mean m within b (clipped to [-1,1]), a single-model connected estimate has absolute error at most 2r+2b. The tighter first term sqrt(2)r is also valid; 2r keeps the sufficient budget rational. Comparing the two models costs at most 4r+4b, uniformly in t **provided the assumed component accuracy is uniform**. With observable error included, 8delta+4r+4b<L(z) retains a positive certified margin. Finite outcomes do not themselves promise a fixed finite number of shots for a vanishing accuracy or simultaneous confidence over a continuum of times. Such resource/error certification remains a next premise.

Primary technical source inspected: Ekert et al., *Direct estimations of linear and non-linear functionals of a quantum state*, arXiv:quant-ph/0203016v1, pp.1–2, Fig.1 and Eq.(1), https://arxiv.org/pdf/quant-ph/0203016 (21 September 2026). It supplies the controlled-unitary interferometric expectation principle. The local completions, four-term decomposition, and U2 error budget above are derived here; the source does not certify this infinite-system apparatus.

## Wilson obstruction, and what it does not say

W_F is a nonzero finite-rank integral operator on a nonatomic Haar space. An ordinary Wilson multiplication operator is M_f. For any such bounded f,

    ||W_F-M_f|| >= ||f||_infinity,
    ||W_F-M_f|| >= 1-||f||_infinity,
    hence ||W_F-M_f|| >= 1/2.                         (R5)

For completeness, the first inequality is proved directly: for any c<||f||_infinity, choose infinitely many disjoint positive-measure subsets of {|f|>c}. Their normalized indicators form an orthonormal sequence e_n. Finite rank gives ||W_F e_n||->0, while ||M_f e_n||>=c. Apply the reverse triangle inequality and let c increase. The second inequality is the ordinary triangle inequality and ||W_F||=1. This argument uses the full local operator norm required by (R1); it does not require a compactness theorem to be imported. Extending by identity outside F leaves that norm unchanged. The obstruction remains for any bounded multiplication readout, including any bounded function of Wilson loops, in this norm topology.

Therefore the accurate norm-transfer route in (R2) cannot replace W by Wilson multiplication. This is **not** a proof that Wilson correlators converge, that none has its own endpoint witness, or that weaker state-dependent approximations fail. The finite-outcome PVM and its unitary completions are gauge-invariant bounded local operators, not Wilson multipliers. Physical-sector-only norm reductions would need their own quotient-space argument; (R5) is explicitly a full local-space obstruction.

## Admitted scope and executable evidence

R1–R4 are full-Hilbert-space identities/bounds. R5 is a full-local-space norm obstruction. The executable verifies finite-dimensional identities that hold on the displayed invariant two-vector sector plus its complement, and exact rational budget arithmetic; it neither approximates nor numerically evolves the infinite Hamiltonian. Its Gaussian rational matrix algebra is implemented here without floating-point unitary checks, external packages or assert statements. The wrong-model controls detect a missing zero outcome, a binary-variance substitution, treating sequential outcomes as the complex correlator, dropping unitary completions, excessive observable error, and confusing finite readout with finite dynamics. The z interval inherits U2's analytic monotonicity proof, with its endpoint arithmetic rechecked exactly.

Result: exact finite outcomes and conditional coherent readout are established; the inherited endpoint bound transfers with an explicit uniform accuracy margin. Practical resources, full-control accuracy, a Wilson-multiplication witness, homogeneous gap, energy calibration, four-dimensional continuum construction, and scientific priority remain open. An equation newly arranged here is not evidence of historical novelty.
