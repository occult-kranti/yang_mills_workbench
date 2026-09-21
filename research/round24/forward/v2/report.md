# V2 forward — finite confidence and an actual physical clock budget

Independent forward derivation, after V1 review and before reading reverse V2. Newton's synthesis requires a finite-data error bound; Tesla's loading criterion retains preparation, controlled full dynamics and clock error. The result is a conditional resource certificate, not an implemented experiment.

## Target and estimator

Keep exactly the fixed U1 W, the U2 canonical summable H_j, stationary states omega_j (j=0,q), and physical scales. Select one q<1 and one requested T_q **before data collection**. Use V1's local unitaries K=W+iP_0, K*=W-iP_0. Four products K_s beta_j^t(K_r) and ancilla X/Y give eight binary settings per model. A ninth setting measures the three-outcome W mean. Each setting uses N fresh, independently prepared trials with identically distributed bounded outcomes in [-1,1]. Across different settings independence is unnecessary for the union bound.

Let xhat_j,sr and yhat_j,sr be the two sample means, and mhat_j the three-outcome mean (already in [-1,1]). Define

    Dhat_j=(1/4) sum_(s,r) (xhat_j,sr+i yhat_j,sr)-mhat_j²,
    Dhat=Dhat_q-Dhat_0.                                  (V2.1)

This estimates the complex connected difference. It is not the average product of sequential W outcomes. Squaring a finite sample mean introduces bias; our confidence bound controls its realized error without claiming unbiasedness.

## Stochastic and systematic assumptions

For every setting, preparation error is bounded by s in trace norm relative to the intended stationary density operator in the full Hilbert representation. No factor 1/2 is hidden in s: |tr((rho_tilde-rho)B)|≤s for ||B||≤1. More generally this can be replaced by dual norm of the state functionals. The implemented ancilla/mean observable differs from its intended observable, at its actual execution time, by at most g in operator norm and remains a Hermitian contraction with outcomes [-1,1]. Here g is a direct complete-setting error bound, not a promise that individual gate errors stay bounded for the enormous time T_q. Then each implemented expectation differs from its ideal one by at most s+g.

All shots for model j share an execution time t_j with |t_j-T_q|≤(hbar/alpha) theta. Fixed timing offsets and calibrated setting errors are the declared model. If times vary between settings/shots, one needs a corresponding per-setting regularity bound instead of silently using this common-time estimate.

For a sample mean of N independent [-1,1] variables,

    P(|mean-E mean|>r)≤2 exp(-N r²/2).

A short self-contained derivation: the second derivative of the centered log moment generating function is the variance under exponential tilting. A variable of range two has variance at most one (subtract the midpoint and minimize mean-square deviation). Integrating twice yields log E exp(lambda(X-EX))≤lambda²/2. Independence, exponential Markov inequality, lambda=r and its negative give the displayed two-sided bound. The union bound over 18 settings gives failure probability at most 36 exp(-Nr²/2). Thus

    N ≥ (2/r²) log(36/kappa)                            (V2.2)

gives confidence at least 1-kappa for all 18 mean errors at this one selected q/time. No simultaneous continuum of q/t or correlated-run certificate follows.

On the confidence event each scalar estimated mean differs from the intended value at t_j by at most e=r+s+g. The real and imaginary averages each have error ≤e; their complex modulus error is ≤2e. Because both the true and estimated W means lie in [-1,1], |mhat²-m²|≤2e. Per-model connected error is ≤4e; the difference costs ≤8e.

## Actual commutator and clock regularity

The reference factorization is the actual U1 factorization. On the eight free singleton factors, u=Omega_F and v=psi_+ are exact eigenvectors of H_F with energies 0 and E=9alpha/2. Thus W maps D(H_0) into itself and

    [H_0,W]=E (|v><u|-|u><v|) tensor I_out,
    ||[H_0,W]||=E.                                     (V2.3)

To justify the domain assertion, on the finite tensor core the outside H_out commutes with W and the local rank operators map into the two finite-energy vectors. The displayed bounded commutator estimate extends by graph-norm closure to D(H_0). Bounded V_q and D(H_q)=D(H_0) then give

    ||[H_q,W]||≤9alpha/2+2||V_q||
                =alpha(9/2+eta/4).                    (V2.4)

Integrating the commutator identity strongly on D(H_j), then extending by density, yields

    ||beta_j^(t+h)(W)-beta_j^t(W)||≤|h| ||[H_j,W]||/hbar.

This is regularity of this particular W, proved using its domain and bounded commutator. It is not norm continuity for arbitrary bounded observables under an unbounded generator. The stationary disconnected mean is constant. Multiplying by ||W||=1 gives the same clock bound for C_j. Therefore the pair of possible timing errors costs at most (9+eta/4)theta and

    |Dhat-[C_q(T_q)-C_0(T_q)]|
      ≤ B := 8(r+s+g)+(9+eta/4)theta                  (V2.5)

with probability ≥1-kappa. Every added parameter is a measurement tolerance or resource: N count, kappa probability, r/s/g dimensionless errors, theta dimensionless physical timing tolerance. The actual physical timing tolerance is hbar theta/alpha. None changes the generator, action, lattice spacing or clock calibration.

## One enclosed sufficient endpoint budget

Choose eta=1/2, z=10^-6, C=2*10^-6, q=999999/1000000. The physical time is T_q=2*10^12 hbar/alpha. From U2 define

    b(q)=P(q)/[24(1-q)^3(1+q)^2(1+q²)],
    P(q)=2+5q+5q²+6q³+3q⁴,
    tau=eta/[8b(q)], s_dyn=C tau/(1-q)^3,
    d²=(tau² b(q²)/96)/[(1-eta)/8]²,
    L_q=s_dyn q⁴/96-6d-(44/9)(10s_dyn)²/(1-10s_dyn)^5.

The name s_dyn is distinct from preparation error s. The checker encloses d with integer square roots at denominator 2^180; all other expressions are exact rationals. It verifies L_q>10^-8. This is a finite-q consequence of the inherited full-system theorem, not a limit extrapolation.

Set r=s=g=theta=10^-10, kappa=1/100. Since exp(9)>3600, proved by a positive finite Taylor sum, N=18/r²=1.8*10^21 shots per setting suffices for (V2.2). The 18 settings need 3.24*10^22 fresh trials. The budget is

    B=8*3*10^-10+(73/8)*10^-10=3.3125*10^-9.

Consequently P(|Dhat|>6.6875*10^-9)≥0.99, conditional on the preparation, setting-error, clock and independence hypotheses. The strict inequality follows from L_q>10^-8. A confidence interval for the unknown true complex difference is the disk of radius B centered at Dhat, rather than a fabricated observed value.

The required time error is hbar/(alpha*10^10), only 5*10^-23 of T_q. The trial count and relative timing requirement are severe. No apparatus, full-state preparation, full-evolution circuit, spin cutoff, wall-clock runtime or resource-optimal procedure is supplied. The explicit finite number is a sufficient mathematical budget, not evidence of practicality.

## Checks and objections

The checker recomputes the finite-q enclosure and sufficient resource arithmetic. It explicitly evolves a three-coordinate algebraic fixture, constructs the controlled-unitary ancilla state, traces out the system, and computes X/Y means. Reversing the Y sign and substituting sequential outcomes are detected by computed nonzero discrepancies. Finite dyadic complex entries in that fixture are exactly representable; the scientific resource bounds use Fraction/integer arithmetic. The fixture is a control for operator order and phase, not simulation of H_q.

A Bernoulli control gives a positive probability of all +1 results at finite N; finite samples do not give deterministic expectation recovery. Excessive systematic error makes the lower certificate inconclusive. An unbounded diagonal Hamiltonian exchanging ever-higher levels with a bounded shift has unbounded commutator, so (V2.3) must not be dropped when translating clock error.

Source context: Hoeffding, *Probability Inequalities for Sums of Bounded Random Variables*, JASA 58 (1963), 13–30, DOI https://doi.org/10.1080/01621459.1963.10500830. Publisher abstract/identity consulted 2026-09-21; the particular concentration proof is supplied above rather than attributed to unread pages. V1's inspected coherent-readout sources support the standard primitive. Scientific priority is unverified. The contribution is this model's explicit conditional error/resource certificate. Wilson endpoint witnesses, actual measurement implementation, homogeneous gap and four-dimensional continuum theory remain open.
