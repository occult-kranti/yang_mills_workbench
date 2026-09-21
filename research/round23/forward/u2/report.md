# U2 forward — a full-system endpoint lower bound

Same-author derivation and critical self-review, using the frozen U1 observable. This proves actual endpoint nonconvergence for one bounded gauge-invariant local autocorrelation in the canonical summable model. It is not a claim about Wilson multiplication observables, the homogeneous model, or a continuum theory.

## Statement

Keep a,E_star,alpha/E_star,hbar>0 and eta in (0,1) fixed. Let epsilon=1−q, T_q=C(hbar/alpha)epsilon^−3, and z=Ceta. For the exact U1 W with ||W||=1, Var_0(W)=1 and reference excitation E=9alpha/2, write C_q for its stationary connected autocorrelation, C_0(t)=e^(−iEt/hbar). For every fixed

    0 < z ≤ 1/1,000,000,

the full-system estimate below proves

    liminf_(q→1−) |C_q(T_q)−C_0(T_q)|
      ≥ z/84 − (44/9)(80z/7)²/(1−80z/7)^5
      > z/168 > 0.                                      (1)

The endpoint γ=3 therefore fails as a general local-correlator convergence statement in this model. N1's sufficient γ<3 interval is sharp in this existence-of-an-observable sense. Equation (1) is neither the exact asymptotic value nor a failure statement for every observable or every C. q=1 remains outside the summable model. The actual variance of W is positive for all sufficiently large q by U1's bound.

## Complete-factor connected series

Fix q<1 first. V_q is a norm-convergent bounded self-adjoint sum, ||V_q||=alpha eta/8, and H_q has exactly D(H_0). Define Z(t)=U_0(−t)U_q(t) and V_I(r)=U_0(−r)V_qU_0(r). This is a strongly continuous bounded self-adjoint interaction-picture generator. The bounded perturbation identity on D(H_0), extended by density, gives Z′=−iV_I Z/hbar. Iteration of the strong equation for F(t)=Z(t)WZ(t)* gives its time-ordered nested-commutator series. Each vector integral defines a bounded operator; no operator-norm continuity of V_I is assumed.

For fixed q and finite t, the usual global Dyson majorant exp(2||V_q|| |t|/hbar) establishes convergence and uniqueness. It may be huge as q→1; it is used for validity, not the uniform estimate. Absolute convergence of the face sum allows its expansion at each finite order. Reference evolution preserves the **complete** factor support of each face, not merely its displayed links. Every factor owns at most ten links; every link meets at most four plaquettes. Therefore each factor is incident to at most 40 omitted faces. Each face touches at most four factors.

Start from W on eight factors. Read an ordered nested word from its innermost commutator outward. A new face must meet the current union; otherwise that commutator vanishes. At step k=0,...,n−1 there are at most 8+3k factors and at most 40(8+3k) possible faces. This includes repeated faces, all geometries, and all factors reached so far. It overcounts harmlessly. Disconnected words vanish even though V_q acts throughout the system. Every coefficient is ≤alpha tau_q/24, every commutator costs at most 2, and the ordered simplex has volume |t|^n/n!. With s=alpha tau_q |t|/hbar, the nth order contribution has norm at most

    (s/12)^n/n! * Π_(k=0)^(n−1) 40(8+3k)
      = (10s)^n (8/3)_n/n!.                              (2)

This estimate is uniform in q and uses no finite-volume truncation. The derivation is on the full Hilbert space, so its bound also applies to the invariant sector. One can first expand finite face sums and then pass to the norm-convergent perturbation at each fixed q,t; the same connected majorant bounds every coefficient and its tail. No exchange of a q-limit with an uncontrolled infinite expansion is needed.

For x=10s<1, summing (2) from n=2 gives

    R(x)=(1−x)^(-8/3)−1−(8/3)x
      ≤ Rhat(x)=(44/9)x²/(1−x)^5.                        (3)

Indeed the second derivative is (88/9)(1−u)^(-14/3). Its Taylor integral remainder is at most half that derivative's upper value times x², and (1−x)^(-14/3)≤(1−x)^(-5). The inequality is valid on the entire interval [0,1), not inferred from a few checked coefficients.

## Signal and state error

U1 gives the exact first-order scalar response. Taking the bounded matrix element of the remainder in (3), then replacing the stationary state at cost ≤6d_q, proves

    |e^(iEt/hbar) C_q(t) − 1 − i s_q q⁴/96|
      ≤ 6 sigma_q/gbar + Rhat(10s_q),                    (4)

for t≥0, s_q=alpha tau_q t/hbar and 10s_q<1. Here sigma_q²=alpha² tau_q² b(q²)/96 and gbar=alpha(1−eta)/8. Scalar ground-energy centering is already included by the stationary definition of C_q; (4) never drops an uncanceled ground phase. The phase e^(iEt/hbar) does not change |C_q−C_0| or the physical clock.

The analytic state estimate tends to zero: sigma_q/gbar=O(epsilon^(3/2)). A complete finite-q bound is

    |C_q(t)−C_0(t)|
      ≥ s_q q⁴/96 − 6 sigma_q/gbar − Rhat(10s_q).         (5)

A negative right side is simply inconclusive. It is not a negative physical error or evidence of convergence. The website displays (5) as a certified lower estimate, never a simulated trajectory.

## Endpoint and strictly positive margin

At T_q, s_q=C tau_q/epsilon³ and

    tau_q/epsilon³ = 3eta(1+q)²(1+q²)/P(q) → 8eta/7.

Also P(q)−2(1+q)²(1+q²)=q+q²+2q³+q⁴≥0, giving tau_q/epsilon³≤3eta/2. Thus x_q≤15z<1 uniformly for the stated interval. In (5), s_q q⁴/96→z/84, x_q→80z/7 and the state error vanishes, proving the first inequality in (1).

To prove the positive margin for every z in (0,10^−6], divide Rhat(80z/7) by z. This equals (44/9)(80/7)² z/(1−80z/7)^5 and is increasing; its derivative has positive numerator proportional to 1+4(80/7)z. At z=10^−6 exact rational arithmetic verifies this ratio <1/168. Hence the same strict inequality holds throughout the interval and (1) follows. No numerical limiting extrapolation is used.

## Verification and interpretation

The checker verifies the connected counting identity, profile polynomial bound, rational endpoint margin, and enclosed square roots for finite-q examples at eta=1/2, C=1/500000. It proves interval-square inequalities with integers; floats are only for display. The reverse checker uses a different rational tail upper bound from coefficient domination. These are correlated same-author checks, not independent proof review.

Newton's forward/backward method was used to require sufficiency beyond U1's derivative. Tesla's mechanism/loading method required all bulk paths. Historical alchemy, theology and resonance analogies add no premises. The mathematical ingredients are standard Dyson/connected-support methods applied to this model; priority is unverified.

Primary technical reading: Nachtergaele–Sims, arXiv:1410.8174v1, Section 2, Proposition 2.1 and Lemma 2.2, https://arxiv.org/pdf/1410.8174. Inspected strong continuity, vectorwise integrals and bounded time-dependent generators. The paper supports this framework; it does not state (1). The geometry and constants in (1)–(5) are derived above. No general unbounded interaction theorem is being invoked for V_q.

Limits: the lower bound is deliberately small and not optimized; practical measurement/readout of the rank operator, Wilson-multiplication witnesses, larger Ceta, full limiting dynamics, homogeneous and continuum construction remain open. No additional loop is executed here.
