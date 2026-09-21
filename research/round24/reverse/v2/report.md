# V2 reverse — sufficient confidence, implementation and physical time budgets

Independent reverse derivation, completed before reading forward V2. Shared V1/U2 premises are inherited, not independently observed. Newton's reverse question is what accuracy makes an actual finite-q endpoint distinguishable; Tesla's complete-mechanism question includes preparation, phase-sensitive readout, physical time and omitted levels. Neither historical analogy supplies a physical constant.

## One endpoint and eighteen finite settings

Fix q<1 and T_q=C(hbar/alpha)(1-q)^(-3) before gathering data. The protocol measures the V1 four unitary expectations for each model j=0,q, each in two quadratures; one further three-outcome W setting estimates m_j=omega_j(W). This is nine settings per model, eighteen total. Use n independent fresh preparations per setting. Outcomes lie in [-1,1]. Independent, non-identically distributed repetitions are allowed if every preparation/instrument satisfies the uniform error conditions below. Correlated preparations are not covered.

For each quadrature take its sample mean and average the four products' real and imaginary components with weight 1/4. Subtract the square of the separately sampled W mean. The difference of these two complex estimates is Dhat. It targets D=C_q^W(T_q)-C_0^W(T_q), with the actual stationary states and actual full evolution. No two-level dynamics approximation enters. Finite outcome count is not finite sample certainty.

If every sample mean deviates from the mean of its own actual expected outcomes by at most r, all sampling inequalities used below hold. For independent X_k in [-1,1],

    Prob(|n^(-1) sum(X_k-E X_k)|>r) <= 2 exp(-n r^2/2).

Here is a short self-contained justification. For each centered variable, the second derivative of its log moment-generating function is the variance in an exponentially tilted distribution supported in an interval of length two, hence at most one. Its log-MGF and first derivative vanish at zero, so log E exp(lambda(X-EX))<=lambda^2/2. Independence, exponential Markov, optimization at lambda=r and both signs give the displayed bound. A union bound over eighteen settings yields

    Prob(all eighteen deviations <=r) >= 1-36 exp(-n r^2/2).      (R6)

This applies to one predeclared q and time. It is not simultaneous confidence over all q, a time continuum, indefinitely repeated analyses, or adaptively selected stopping times. The checker calculates this deterministic sufficient inequality; it draws no simulated experimental samples.

## Actual commutator and its domain

Let F be the eight singleton reference factors of W. On H_F the local reference energy h_F satisfies h_F o=0 and h_F p=E p, E=9alpha/2. The rank operators made from o,p preserve D(h_F), and direct calculation gives

    [h_F,W_F]=E(|p><o|-|o><p|),  ||[h_F,W_F]||=E.

Both h_F and the nonnegative exterior reference Hamiltonian have commuting spectral measures in the incomplete tensor product. On their common finite-energy core W_F tensor I commutes with the exterior generator and the displayed local commutator is bounded. Approximate a vector in D(H_0) by joint spectral cutoffs. W is bounded, and H_0 W xi = W H_0 xi + [H_0,W]xi on the core; closedness passes this to D(H_0). Thus W preserves the full domain and [H_0,W] has a bounded extension of norm E. This proof uses the actual local eigenvectors, not an assumption that every bounded observable preserves an unbounded generator's domain.

For q<1, V_q is bounded, ||V_q||=alpha eta/8, D(H_q)=D(H_0). Hence

    ||[H_q,W]|| <= alpha(9/2+eta/4)=hbar kappa_q,
    ||[H_0,W]|| = 9alpha/2=hbar kappa_0.               (R7)

P_zero=I-W^2 commutes with H_0. The unitary completions R_plus/minus=W +/- P_zero have norm one, preserve the same domain, and satisfy the same respective bounds (R7), using 2||V_q|| ||R|| for the interacting contribution. Integrating the strong derivative between any two times gives the norm inequality

    ||beta_j^(t+e)(R)-beta_j^t(R)|| <= kappa_j |e|.     (R8)

The bounded integrand controls the operator norm after vectorwise integration. No norm continuity theorem for arbitrary bounded operators or unbounded H is claimed. Ground-energy shifts commute with R and do not affect (R7). These quantities have physical units: kappa has inverse time, and e has time.

## Systematic bias, including independent clock jitter

Assume every prepared state rho satisfies half trace norm distance from its intended stationary state at most epsilon_p. On bounded contractions this gives expectation bias at most 2epsilon_p. Assume the implemented effective Hermitian readout differs from its ideal contraction in operator norm by at most epsilon_i, including all coherent circuit/control errors apart from the explicitly counted common evolution-time error. Put s=2epsilon_p+epsilon_i. This is an accuracy assumption about an entire implemented setting; it is not established by counting gates or naming an apparatus.

Allow each quadrature setting and each shot a physical time displacement e with |e|<=h. Equations (R7)–(R8), and ||R_sigma||=1, bound a quadrature expectation's time bias by kappa_j h. The means used in the connected subtraction are single-time W expectations and have no evolution-time error. On the probability event (R6), each model's real and imaginary uncentered reconstruction has component error <=r+s+kappa_j h. Bounding complex magnitude by the sum of its two component magnitudes costs <=2(r+s+kappa_j h). The measured W mean remains in [-1,1], so its square has error <=2(r+s). Therefore

    |Dhat-D| <= B = 8(r+s)+2(kappa_q+kappa_0)h
                  =8(r+2epsilon_p+epsilon_i)
                    +2(9+eta/4)(alpha h/hbar).         (R9)

This deliberately covers independently displaced settings; when all settings share exactly the same displaced time, the direct W-correlator bound can improve the timing coefficient. An independently measured numerical confidence radius does not bound unknown coherent bias, preparation errors or clock drift. The ideal conditional readout still assumes full-system evolution with both signs and preparation of the actual ground states. No construction of those resources is supplied.

## A fully finite numerical sufficiency example

Choose eta=1/2, z=Ceta=10^-6, C=2*10^-6, q=1-10^-8. The time is

    alpha T_q/hbar = 2*10^18.

Using the actual U2 finite-q certificate, not merely its liminf, define

    b(q)=P(q)/[24(1-q)^3(1+q)^2(1+q^2)],
    P(q)=2+5q+5q^2+6q^3+3q^4, tau=eta/[8b(q)],
    s_q=C tau/(1-q)^3, x_q=10s_q,
    d_bound^2=eta^2 b(q^2)/[96(1-eta)^2 b(q)^2],
    L_q=s_q q^4/96-6 sqrt(d_bound^2)-(44/9)x_q^2/(1-x_q)^5.

The checker encloses sqrt(d_bound^2) by a rational interval using integer square roots. It proves x_q<1 and L_q>z/100=10^-8 with that upper root bound. These are certified inequalities, not observed or simulated trajectories.

Take r=z/10000=10^-10, epsilon_p=epsilon_i=z/10^6=10^-12 and alpha h/hbar=z/10^6=10^-12. Choose n=18/r^2=1.8*10^21 shots per setting. Then nr^2/2=9 and exp(9)>3600, certified by a finite positive rational Taylor sum, so (R6) has failure probability below 1/100. The eighteen settings require 3.24*10^22 state preparations. The total bound is

    B=8.4225*10^-10 < L_q,
    |Dhat| >= L_q-B > 9.15775*10^-9

with probability at least 99%, under all stated preparation/control/independence assumptions. The last strict bound uses only L_q>10^-8. The absolute physical time tolerance h=10^-12 hbar/alpha corresponds to relative tolerance h/T_q=5*10^-31. These are unoptimized sufficient resources and plainly impractical for a direct experiment. No absolute seconds or measured energy scale can be inferred without calibrating alpha/hbar. More shots do not repair a violation of the systematic or timing budget.

## Controls and result

Exact checks reconstruct the imaginary ancilla quadrature sign from U=diag(1,i), W=sigma_x and their product. Reversing the measured Y sign gives the opposite complex answer. The checker rejects excessive systematic bias, omitting the finite-q state term, and interpreting a positive-probability finite-sample error event as deterministic certainty. It verifies the commutator norm algebra on the displayed eigenvector sector; the closed-domain proof above handles the full Hilbert space. A singleton algebra calculation is not a numerical simulation of H_q.

Accepted scope: an explicit finite-sample conditional distinguishability certificate at a declared endpoint, with a genuine W-specific physical timing estimate. Remaining limitations: enormous sufficient resources, assumed full-system coherent control and preparation, unimplemented calibration, possible correlations, no Wilson-multiplication witness, no homogeneous or continuum result, and unverified scientific priority. This completes the selected V2 investigation and does not execute another goal.
