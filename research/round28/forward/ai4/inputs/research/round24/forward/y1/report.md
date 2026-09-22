# Y1 forward — finite spatial control of the canonical endpoint

Independent forward derivation before current reverse Y1. The model is exactly canonical M/N/U with the fixed U1 rank observable W. Newton's forward reconstruction requires a complete spatial approximation; Tesla's full-system check keeps boundary return paths. No T finite-graph gap or S homogeneous coefficient enters this result.

## Complete reference factors and the finite region

Start with F_0, the eight singleton free-link factors in U1's three paths X,Y,Z. The inherited partition puts every other reference factor either on one free link or on a complete ten-link selected strip. For a factor set F write E(F) for **all** its links. For an omitted elementary face f write c(f) for all reference factors owning its four links. Define recursively

    I(F)={omitted f: links(f) meets E(F)},
    F_(k+1)=F_k union union_(f in I(F_k)) c(f),
    O_k={omitted f: c(f) subset F_k}.                 (Y1.1)

These rules are independent of q. Every factor has at most ten links and every link meets at most four plaquettes, so every step is finite. The rule uses actual positive-orthant boundaries and complete reference strips. It never replaces a strip by only the links visible in W.

The independent geometry implementation obtains:

| Depth k | Reference factors | Complete links | Retained omitted faces | Omitted faces crossing its boundary |
|---|---:|---:|---:|---:|
| 0 | 8 | 8 | 1 | 18 |
| 1 | 35 | 98 | 20 | 105 |
| 2 | 135 | 297 | 129 | 198 |

Define, with the original coefficients unchanged,

    V_(q,k)=-alpha tau_q sum_(f in O_k) q^|anchor(f)| x_f/24,
    H_(q,k)=H_0+V_(q,k).                             (Y1.2)

No finite-face budget is renormalized. All selected reference strip Hamiltonians stay in H_0, including the outside factors. H_(q,k) separates into a finite-factor operator on F_k and unchanged reference dynamics outside. Its factor Hilbert spaces remain the complete SU(2) Haar spaces, with every spin. Finite space is not finite dimension.

Each retained face is an entire gauge-invariant Wilson multiplier. Complete reference factors preserve gauge actions and their closed domains. V_(q,k) is bounded self-adjoint, so D(H_(q,k))=D(H_0). The physical invariant sector reduces it. This approximation changes a spatial boundary for comparison; it introduces neither a new coupling nor a fitted clock.

## Connected-word matching and the full omitted tail

Let beta_q^t and beta_(q,k)^t denote the same negative-time conjugation convention as U2. Pass both to the interaction picture of the **same** H_0. Each coefficient of V_q has norm ≤alpha tau_q/24; reference evolution preserves its complete factor support. Every possibly nonzero ordered nested commutator starts on F_0 and each next face meets the union accumulated so far. Repeated faces and all orderings remain.

At step j, all accumulated factors lie in F_j by (Y1.1). Hence every connected word of length n≤k uses only faces in O_k. Its time integrals and coefficients in full and restricted dynamics agree exactly. At n>k, the restricted series is the subset of full words with every face in O_k. Subtracting cancels those words exactly; the difference consists only of omitted words. Thus a **single** full-series tail upper bound suffices, rather than two independent entire tails.

U2's actual full connected count gives, for p=8/3 and x=10 alpha tau_q |t|/hbar,

    norm of all order-n words ≤ a_n x^n,
    a_n=(p)_n/n!,  x<1.

Its proof counts complete-factor incidence, growth by at most three factors per face, all ordered words, the commutator factor two and simplex 1/n!. For each q<1, global bounded perturbation theory first justifies the series; its connected majorant then bounds the omitted tail uniformly. No unbounded H_0 BCH expansion or finite-spin simulation is used. Therefore

    ||beta_q^t(W)-beta_(q,k)^t(W)||
      ≤ sum_(n=k+1)^infinity a_n x^n
      ≤ D_k(x):=a_(k+1) x^(k+1)/(1-x)^(k+4).        (Y1.3)

The second inequality is Taylor's integral remainder for (1-x)^(-p): the derivative of order k+1 is (p)_(k+1)(1-u)^(-p-k-1), bounded by its value at x; its exponent p+k+1=k+11/3 is at most k+4. This bounds the **whole** omitted tail, not just the first missing shell. It includes excursions crossing the chosen boundary and returning to W.

For T_q=C(hbar/alpha)(1-q)^-3, z=C eta in (0,10^-6], retain U2's actual identity tau_q/(1-q)^3≤3eta/2. Thus x≤15z<1 simultaneously for all q in (0,1) and all |t|≤T_q, and

    sup_(|t|≤T_q) ||beta_q^t(W)-beta_(q,k)^t(W)||
      ≤D_k(15z).                                    (Y1.4)

The physical time and spatial q-profile are unchanged. The estimate is a local-observable operator norm bound; it is not a norm approximation of the entire global propagator on every state.

## Stationary states and correlation transfer

A stationary finite-region calculation needs its own ground state. The finite partial sum satisfies ||V_(q,k)||≤alpha eta/8, has zero reference mean, and the same codimension-one gap argument as M2 supplies a unique ground Psi_(q,k), with other uncentered spectrum ≥gbar=alpha(1-eta)/8. Its ground is invariant under the gauge action and equals its F_k ground tensored with the outside reference vacuum.

Distinct omitted faces are orthogonal in the reference state by the inherited free-Haar parity argument. A partial sum has a smaller squared residual:

    sigma_(q,k)^2=alpha² tau_q²/2304
                    sum_(f in O_k) q^(2|anchor(f)|)
                ≤sigma_q².

The gap-to-reference spectral argument gives

    d_(q,k)=||P_(q,k)-P_0||≤sigma_(q,k)/gbar≤sigma_q/gbar=:dhat_q.

This bound is valid even when its right side is greater than one, though then it is loose. Define the actual stationary connected correlations

    C_q(t)=omega_q(W beta_q^t(W))-omega_q(W)^2,
    C_(q,k)(t)=omega_(q,k)(W beta_(q,k)^t(W))-omega_(q,k)(W)^2.

Trace duality for rank-one projections and splitting both means gives a coefficient 6 for a change of stationary state between these bounded expressions. The two projectors differ by at most d_q+d_(q,k)≤2dhat_q. Combining with (Y1.4) yields

    sup_(|t|≤T_q)|C_q(t)-C_(q,k)(t)|
       ≤D_k(15z)+12dhat_q.                           (Y1.5)

This includes both means and the state change. Scalar ground-energy phases cancel in the two respective Heisenberg conjugations; neither is dropped from an uncentered propagator. An optional computation in Omega gives only a reference-state proxy and costs 6dhat_q to reach the true full correlation plus (Y1.4); Omega is generally not stationary for H_(q,k). We do not label that proxy a finite-region stationary result.

Since dhat_q→0, U2's full stationary endpoint lower bound transfers:

    liminf_(q→1) |C_(q,k)(T_q)-C_0(T_q)|
      ≥L(z)-D_k(15z),
    L(z)=z/84-(44/9)(80z/7)^2/(1-80z/7)^5>z/168.    (Y1.6)

For k=1, D_1(x)=(44/9)x²/(1-x)^5. The ratio D_1(15z)/z is increasing, and exact arithmetic at z=10^-6 proves

    D_1(15z)<z(1/168-1/250),
    liminf |C_(q,1)(T_q)-C_0(T_q)|>z/250.           (Y1.7)

The finite spatial system therefore retains an actual endpoint signal with the original growing time. It is still an infinite-dimensional 98-link problem and a varying q family, not the 21-state T compression or a solved trajectory.

## Evaluated error and geometry checks

At z=10^-6, depth one has uniform operator error below 1.101*10^-9; depth two below 2.568*10^-14. For eta=1/2, C=2*10^-6 and q=999999/1000000, T_q=2*10^12 hbar/alpha. The checker encloses dhat_q with an integer-square-root interval at denominator 2^180 and combines the U2 finite-q lower bound with (Y1.5). It proves the **stationary** depth-one difference from the reference has magnitude greater than 8*10^-9 at that endpoint. This is a lower certificate, not a simulated or measured complex value.

The executable reconstructs the actual strip/free partition, positive-boundary plaquette incidence and F_k. It checks every connected first face and 736 possible ordered second-face words on these regions. The induction above proves arbitrary order; enumeration does not replace it. It verifies the actual origin-xz four-link cover expands to 22 complete links and sees the hidden crossing xz face anchored at (2,1,0), which an edge-only rule misses. It confirms the U1 resonant yz face is retained, boundary omissions remain, the tail is positive, and neither q coefficients nor the clock are renormalized.

The remaining uncertainty is computation and control inside the finite-factor Hilbert space: rigorous finite-spin leakage, actual ground-vector construction, real-time evolution and coherent circuit accuracy are not supplied. The source/newton/tesla method lessons require that these be separate targets. Scientific priority is unverified. There is no homogeneous gap or four-dimensional continuum construction claim.
