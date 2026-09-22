# AC2 forward: old-input cancellation improves the all-time heat bound

This independent second-loop derivation uses the frozen AC1 pair and review, including the exact forward-origin 293-state metric matrix. No current reverse AC2 work was read. It proves a relative error below 0.000037 for every time, every 0<=lambda<=1/100 and every normalized original P21 input within 0.01 of the vacuum. This improves the inherited Z2 bound 0.00044 and AC1's conservative 0.0014 on the same preparation class and physical clock. The output is a rigorous computable bound for the exact retained semigroup, not a sampled trajectory or a new matrix-exponential evaluator.

## Exact compression and every new channel

Let P=P293, P1=P21, N=P-P1 and P_f=P1-|Omega><Omega|. Keep L=K+lambda(20-S), A=PLP, mu=min spectrum A, epsilon=min spectrum L, c=20lambda and B=(I-P)LP. The AC1 rational coordinates have Gram weights three on 62 triplets and one otherwise. Reconstructing all basis labels and face-pair channels independently gives

    N A N=D_N+cN,  D_N>=9/2,
    C=N A P1=-lambda N S P_f,
    C Omega=0, ||C||=(sqrt(39)/2)lambda,
    B P1=0, ||B||<=20lambda.                       (AC2.1)

The magnetic N-to-N block is exactly zero by actual global center parity. The exact 20-by-20 Gram of N S P_f has diagonal five and off-diagonal 1/4, i.e. (19/4)I+(1/4)J, whose largest eigenvalue is 39/4. Both shared-edge branches are essential: their squared weights 1/16+3/16 add to 1/4. The checker reconstructs the complete sparse matrix and Gram, not just its bright input. The bound on B remains the complete new-column remainder; none of the 272 channels is discarded.

All vectors are in the common actual domain, P reduces K and the finite compressed evolution is smooth. The original P21 is not autonomously invariant under A: C is nonzero. The cancellation B P1=0 holds only on initial old inputs, and must be propagated through the N equation instead of asserted at positive time.

## Retained evolution loads the new channels gradually

Take a unit x in P1 with ||x-Omega||<=eta=1/100, u(t)=exp[-t(A-mu)]x and y(t)=N u(t). Its exact equation and initial condition are

    y'=-(D_N+c-mu)y-C P_f u,  y(0)=0.

Since 0<=mu<=c, its free decay rate is at least d=9/2. On the continuous interval lambda<=Lambda<=1/100, use the AC1 rational envelopes

    g=3-20Lambda, r21=7Lambda²/3, p21=r21/g,
    r+=20Lambda p21, p+=r+/g, delta+=r+²/g,
    q+=3Lambda/4+3p21/2, b=q++eta.

Here the actual new Ritz ground f+ satisfies ||P_f f+||<=q+, and the actual retained excited part of x has norm at most b. The latter follows ||(I-|f+><f+|)Omega||<=|| (I-|f21><f21|)Omega||+|| |f+><f+|-|f21><f21| ||<=3Lambda/4+p21, with the displayed 3p21/2 a conservative common envelope. Both compressed and full centered excited gaps are at least g. Therefore

    ||P_f u(t)||<=q++b exp(-g t),
    ||y(t)||<=Cbar[q+(1-exp(-dt))/d
                    +b(exp(-gt)-exp(-dt))/(d-g)],
    Cbar=25Lambda/8 >=sqrt(39)Lambda/2.              (AC2.2)

This uses every retained component and the full matrix coupling, including possible feedback through P_f; it does not neglect repeated passages through N. The spectral bound on u already includes them. It is a source-sensitive upper bound, not a closed two-block approximation to the original Hamiltonian.

## Full error, centering and denominator

Let E(t)=exp[-t(L-epsilon)] and E+(t)=exp[-t(A-mu)]P. On retained inputs the derivative in the exact Duhamel identity contains B plus the distinct scalar delta=mu-epsilon. AC1 proves 0<=delta<=delta+, and ||B u||=||B y||<=20Lambda||y||. Integration of (AC2.2) gives the early-time estimate

    V(t)=delta+ t+(20Lambda)Cbar{
       (q+/d)[t-(1-exp(-dt))/d]
       +b/(d-g)[(1-exp(-gt))/g-(1-exp(-dt))/d]}.
                                                        (AC2.3)

Every term is an integral of a nonnegative kernel. A simpler increasing envelope, valid for all t>=0, is

    Vbar(t)=delta+ t+(20Lambda)Cbar[q+ t/d+b/(gd)].
                                                        (AC2.4)

The transient integral identity gives the last term's bound 1/(gd). The distinct ground shifts are charged by delta+ t; using the same arbitrary center would invalidate an all-time comparison.

Independently, the actual full/new ground-projector distance is at most p+, so the complete spectral tails yield

    J(t)=p++(2b+p+)exp(-gt).

The true full output denominator is bounded using the inherited 21-state full-ground residual, independently of the new Ritz vector:

    ||E(t)x||>=D:=1-5Lambda²/9-eta-p21>0.          (AC2.5)

Thus for any chosen join t0, the exact all-time relative error is at most max(Vbar(t0),J(t0))/D. This is a theorem on every t, obtained by the increasing early envelope and decreasing late envelope; no time grid supplies its uniformity.

At Lambda=1/100 choose t0=13/5, corresponding to the unchanged physical time (13/5)hbar/alpha. A positive rational Taylor sum proves exp(182/25)>1400, hence exp(-g t0)<1/1400. Exact values are

| Quantity | Certified value |
|---|---:|
| True denominator D | 7127/7200 |
| Early absolute upper bound | 457097/12600000000 |
| Late absolute upper bound | 2441/78400000 |
| All-time relative upper bound | 457097/12472250000 < 0.000037 |

All envelopes are uniform on the entire coupling interval, so this is not a cap-only calculation. At t=0 the true retained error is exactly zero; (AC2.3) also gives zero. At lambda=0 P reduces the actual generator and both ground shifts vanish, giving exact agreement at all times. The coarse late estimate can be nonzero at lambda=0 and is superseded by this exact identity.

## Arithmetic, interpretation and scope

The executable reconstructs every AC1 sparse entry and compares it with the frozen matrix in the correct Gram; it also computes the full old-to-new Gram, its two eigenvalues, the continuous envelopes and positive denominator. Every stored numeric certificate is rational and has zero arithmetic error. No matrix exponential is numerically evaluated here, so a later trajectory evaluator must separately charge its arithmetic approximation. Physical omitted channels are already charged in B and cannot be absorbed into a rounding allowance.

The admitted class remains normalized x in the original P21 radius-0.01 ball. AC1 allowed a larger P293 ball with a weaker bound; this sharper certificate is not asserted for that enlarged class, because y(0)=0 is essential. It also does not give generic relative control on ground-null inputs, a real-time theorem, a changing graph-size guarantee or a continuum approximation.

Newton's forward/reverse method motivates independently verifying the identifying metric; Tesla's loading criterion is realized by the full 272-column envelope and retained feedback. No historical claim enters the proof. Scientific priority is unverified. The finite-graph accuracy target is advanced within this actual preparation/heat scope; homogeneous inversion and physical continuum scale matching remain open.
