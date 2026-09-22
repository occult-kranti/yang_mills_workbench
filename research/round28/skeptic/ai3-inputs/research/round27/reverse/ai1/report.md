# AI1 reverse: reconstructing what the endpoint can identify

This report and its checker were derived independently from the frozen AI1 contract and inherited AD1/AD2 evidence. No current forward AI1 solution was read. This is a Feynman-method lens (alternative explanations and discriminating measurements), not historical-person endorsement. The conclusions concern explicitly defined readout maps. They do not assert equality of different finite-q Hamiltonians.

## 1. Readout domain and inherited functions

Write a=alpha/hbar>0, u=1-q in (0,1), and kappa=a eta u^3>0. The physical reference hbar and E_star remain fixed; comparing a also compares alpha/E_star. For theta=z/84 the inherited elementary, single-six-cycle and coherent-six-cycle endpoints are

    F_0(z)=1,
    F_X(z)=2/3+cos(2theta)/4+cos(2sqrt(3)theta)/12,
    F_+(z)=1/3+cos(2theta)/2+cos(2sqrt(3)theta)/6
        +i[sin(2theta)/4+sin(2sqrt(3)theta)/(4sqrt(3))].       (R1)

The certified physical endpoint theorem has 0<z<=10^-6. The displayed finite trigonometric functions are entire; their analytic extensions allow structural-identification arguments at zero. This does not enlarge the physical transfer theorem. Exact derivatives are

    F_+'(0)=i/84, F_X'(0)=0, F_X''(0)=-1/3528,
    F_+''(0)=-1/1764.                                    (R2)

Their derivation uses d^n exp(i lambda z/84)/dz^n=(i lambda/84)^n and the complete AD2 source spectral measures. For example the X second moment is 2, giving -2/84^2. The checker independently expands the trigonometric formulas with rational coefficients; no floating cancellation near one is used.

## 2. Two different experiments encoded by the time label

**Scaled-time readout.** The triple (F_0(z),F_X(z),F_+(z)) as a function of the dimensionless label z is independent of alpha, eta and q. Its complete values identify none of them. If physical timestamps T(z)=z/kappa are also supplied, the timestamps identify the composite kappa; that information comes from the time protocol, not the universal endpoint ordinate. Demodulation needs the electric carrier calibration, so the ability to form these curves is not itself an alpha measurement.

**Formal physical-time readout.** Define a surrogate map, explicitly distinct from the finite-q model,

    D_j(t;p)=F_j(kappa t), 0<kappa t<=10^-6.               (R3)

Equality of the complete coherent curves on any open common time interval implies equality of their analytic extensions, hence of D_+'(0)=i kappa/84. Conversely equal kappa makes every D_j identical by substitution. Thus the fibers of this map are exactly

    alpha eta (1-q)^3 = constant*hbar.                   (R4)

F_X alone identifies kappa^2 through -3528 D_X''(0). Positivity identifies kappa; in a signed extension, X cannot distinguish kappa from -kappa. The imaginary coherent slope does distinguish that extension. The elementary demodulated probe is constant and identifies no slow parameter despite its inherited nonzero variance.

An exact distinct-parameter example in units alpha/E_star=1 and hbar/E_star=1 time unit is

    p1=(alpha=1, eta=1/16, q=999/1000),
    p2=(alpha=1, eta=1/2, q=1999/2000),
    p3=(alpha=2, eta=1/32, q=999/1000).

All have kappa=1/16000000000 in inverse time units. Their complete surrogate demodulated curves agree, including every derivative. These are algebraic countermodels, not a claim that these q values have small inherited full-system errors. Compensation survives arbitrarily near q=1: take u2=u1/2, eta2=8 eta1, eta1<1/8, and arbitrary u1 in (0,1).

## 3. Undoing the demodulation requires actual clock information

Define another explicitly formal surrogate:

    U_0(t)=exp(-3 i a t),
    U_X(t)=exp(-9 i a t/2) F_X(kappa t),
    U_+(t)=exp(-9 i a t/2) F_+(kappa t).                  (R5)

For complete complex curves on a physical-time interval the inverse map is

    a=-Im U_0'(0)/3,
    kappa=84[Im U_+'(0)+(9/2)a].                         (R6)

Equality of a,kappa is necessary by these derivatives and sufficient by (R5). Therefore these three undemodulated surrogate curves identify alpha and r=eta(1-q)^3, but not eta and q separately. For fixed a,kappa, set r=kappa/a in (0,1); the full fiber is

    0<q<1-r^(1/3), eta=r/(1-q)^3.                       (R7)

The first two rational examples belong to this fiber; p3 is separated by its carrier. This is conditional structural identifiability, requiring known physical times, a fixed action reference, phase-resolved complex correlations and the declared surrogate model. Intensity-only measurements lose the elementary carrier entirely. Derivatives of (R5) are not asserted to be derivatives of the actual finite-q stationary correlators.

Uniform sampling t=n Delta also leaves a carrier alias even if kappa is known: replace

    alpha' = alpha+4 pi hbar m/(3 Delta),
    eta' = eta alpha/alpha', q'=q,                       (R8)

with positive alpha' and 0<eta'<1. The elementary extra phase is 4 pi mn and the six-cycle extra phase is 6 pi mn, so all sampled surrogate curves coincide. At sufficiently fine Delta this requires a bounded prior alpha range or nonuniform times to exclude; sampling alone without such assumptions does not. The checker verifies these phases as exact integer multiples of 2pi, not approximate trigonometric equalities. The alias applies to any samples inside the inherited z window; it does not extend the physical theorem to all n.

## 4. Why this is not a finite-q nonidentifiability theorem

AD2's exact retained center contains Q(q), with face weights q^4 and q^5, and s_q, not merely F(kappa t). The state, spatial-tail and averaging errors also retain eta and q. Thus indistinguishable endpoint surrogates can have different finite-q readouts. Moreover q->1 with z fixed sends physical time to infinity; t fixed instead gives z=kappa t->0. Differentiation at t=0 cannot be interchanged with that growing-time limit without a new uniform derivative theorem.

A small scalar value error is insufficient derivative control: e_N(t)=epsilon sin(Nt) has sup |e_N|<=epsilon but e_N'(0)=epsilon N. The checker gives exact derivative counterexamples. This is a generic information counterexample, not a claimed gauge-theory perturbation. No actual finite-q initial-slope measurement is inferred from (R2) or (R6).

## 5. A discriminating next readout, with obligations

The inherited reached matrix contains both q^4 and q^5 face-flip amplitudes. A candidate is a pair of actual multiplication observables B_r=(chi_C+chi_(C triangle f_r))/sqrt(2), where both characters are six-cycles and the connecting face has anchor exponent r=4 or 5. Each source is a normalized coherent pair. In the averaged retained matrix, its first moment is q^r. If both retained phase slopes can be inferred at a common physical scale, their ratio is q, cancelling the common alpha tau_q/(96 hbar). With calibrated alpha and a nonzero amplitude, eta can then be reconstructed from tau_q=eta/[8b(q)]. This algebra proposes a discriminator; it does not establish an actual measurement.

The next contract must freeze actual cycles and multiplication norms; prove their complete reached components and exterior exclusion; retain stationary-state, collar, finite-time, clock and numerical errors for both observables; infer slopes or finite differences with an independent remainder bound; show nonzero denominators and noise separation; and keep alpha's calibration explicit. A ratio of two coincident limiting endpoint slopes would erase q again. A constant-rescaling fit must not be substituted for these conditions. No homogeneous-model or continuum matching is supplied here.

## 6. Verification and conclusion

Run `python3 -B research/round27/reverse/ai1/check.py --output /absolute/fresh/directory`. Only Python's standard library is required. Exact rational checks cover analytic coefficients, distinct compensation fibers, conditional inversion, log-parameter Jacobian ranks, signed ambiguity, carrier aliasing, and failure of value-only derivative control. They illustrate and stress the proofs; a finite Taylor list alone does not prove equality of entire curves. Every contract source and additionally consulted inherited local source is hash-bound, together with this report and the checker. Python optimization must not disable checks.

The contribution is a source-specific identification classification and exact countermodels for these declared Wilson endpoint surrogates. It clarifies a missing measurement, not a new mass-gap theorem. The canonical family, homogeneous model, finite physical graph and continuum target remain distinct. Scientific priority of structural identification is unverified and no general-method novelty is claimed.
