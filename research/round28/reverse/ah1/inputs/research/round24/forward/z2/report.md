# Z2 forward: useful all-time relative heat accuracy for the actual vacuum

The actual 21-state Ritz heat has true-output-relative error below **0.00028
at every heat time**, for the actual retained vacuum and every coupling
0<=lambda<=0.01. Every normalized retained vector within norm 0.01 of that
vacuum has error below **0.00044** for its own true output. An independently
checkable class, with Ritz ground overlap at least 0.99, has all-time error
below **0.002**. These conservative certificates include the separately
bounded scalar arithmetic below. They are not measured approximation errors.

The new step is an actual early-time residual estimate joined to an
independently valid late-time spectral estimate. The vacuum begins with zero
omitted residual. Its subsequently generated residual includes every X2
channel. The preparation extension also computes the complete omitted
operator Gram matrix. No denominator constant is inserted or fitted.

Authorship: independent forward model-agent derivation; current reverse/Z2
was not read or discussed before freezing this submission. Inherited premises
and separate model agents do not constitute external peer review. Newton's
analysis/synthesis motivates specifying the true-output quotient and its
missing denominator premise. Tesla's whole-mechanism check motivates the full
omitted Gram calculation and the separate centering term. Neither historical
analogy nor an unverified priority claim supplies a mathematical premise.

## 1. Actual model, retained space and inherited full-operator facts

Keep the open (3,3,2) SU(2) graph, 18 vertices, 33 links, 20 elementary faces,
product Haar measure and every vertex Gauss constraint. On its full physical
Hilbert space use exactly

    L=H_lambda/alpha=K+lambda(20-S), S=sum_p W_p,
    P=1_[0,9/2)(K), A=PLP on P Hphys,
    epsilon=min spec L, mu=min spec A,
    E(sigma)=exp[-sigma(L-epsilon)],
    E_R(sigma)=exp[-sigma(A-mu)]P, sigma=alpha t/hbar.

The positive scales a,E_star,alpha/E_star,hbar remain fixed. Lambda is constant
in [0,1/100]. Energies and residual norms below are divided by alpha;
projection, preparation and relative errors are dimensionless. A joining time
is a proof choice in these fixed units. Preparation radii and overlap floors
restrict the approximation question; they do not modify the action or clock.

X1/X2 establish the common self-adjoint domain D(L)=D(K), smooth invariant
polynomial core, compact resolvent, simple ground, and actual full physical
excited spectrum >=3. P reduces K and its domain. P has exactly the
orthonormal basis Omega=1, phi_p=2W_p, p=1,...,20. Every retained vector is a
smooth invariant polynomial. These full-operator facts, including the gap,
are inherited premises; the checker does not replace them with a matrix gap.

The actually assembled matrix has A00=c=20lambda, A0p=Ap0=-lambda/2,
Apq=(3+c)delta_pq. Set

    D=sqrt(9+20lambda^2), w=(D-3)/2, mu=c-w,
    h=lambda/(D+3), Z=1+20h^2,
    f=(Omega+h sum_p phi_p)/sqrt(Z), G_R=|f><f|,
    f0=<f,Omega>=sqrt[(D+3)/(2D)],
    q=||(I-G_R)Omega||=sqrt[(D-3)/(2D)].                 (1)

The bright Ritz gap is D, the other 19 gaps are gamma=(D+3)/2>=3.
Let G be the true ground projection and B=QLP, Q=I-P. From X2,

    F=S^2-5, ||F||^2=195/4,
    r=Bf=-(2lambda h/sqrt(Z))F,
    rho^2=||r||^2=195lambda^4/[2(D+3)D],
    delta=mu-epsilon in [0,rho^2/(3-mu)],
    ||G-G_R||<=p=rho/(3-mu), g=3-mu.                  (2)

X2's residual-enriched variational bound proves delta>0 for lambda>0.
The full true heat has excited decay at least exp(-g sigma). Both E and E_R
are contractions under their own correct ground shifts. The heat output norm
is positive on every nonzero input at every finite time by spectral
injectivity. The quotient being bounded here is precisely

    R(sigma,x)=||(E(sigma)-E_R(sigma))x||/||E(sigma)x||. (3)

It uses the same input in numerator and denominator. We never divide by the
Ritz output, the operator norm of E, or an artificially enlarged denominator.

## 2. The complete omitted operator, including preparation directions

Since QK P=0 and QS Omega=0, B Omega=0. For each retained face,

    B phi_i=-2lambda(W_i S-1/4).                       (4)

The omitted expression is orthogonal to every retained face by the actual
three-face parity rule. Haar integration gives E W_i^4=1/8 and
E W_i^2 W_j^2=1/16 for distinct faces, including shared-edge pairs by the
exclusive-edge conditional Haar argument in X2. The graph has no three-face
or four-distinct-face zero parity mask. Thus the complete fourth-moment sum
gives

    <W_i S-1/4,W_j S-1/4> = 5/4 if i=j, 1/16 if i!=j,
    (B*B)|_faces=lambda^2[(19/4)I+(1/4)J_20].         (5)

The checker reconstructs (5) by summing all 160,000 ordered fourth moments on
the actual graph. The symmetric eigenvalue is 39lambda^2/4 and the 19 dark
eigenvalues are 19lambda^2/4; the vacuum eigenvalue is zero. Therefore

    M=||B||=sqrt(39)lambda/2.                         (6)

The same Gram sum gives ||F||^2=195/4 and the residual in (2), providing two
representations of the relevant omitted norm. In its original expansion F
contains 20 spin-one terms plus all 190 face products. The graph has 128
edge-disjoint pairs and 62 shared-edge pairs. The latter retain both singlet
and triplet branches. Haar norms in (5) include their complete sum; no branch
is discarded or assigned the wrong electric energy. Keeping only spin-one
terms gives B*B=lambda^2 I/4 on the face space and underestimates its symmetric
eigenvalue, as well as rho^2, by a factor 39.

## 3. Actual early-time vacuum error, with its own centering term

The exact Ritz vacuum trajectory contains only its ground and bright modes:

    E_R(s)Omega=G_R Omega+exp(-Ds)(Omega-G_R Omega),
    coefficient of every phi_p=lambda(1-exp(-Ds))/(2D).

Consequently its complete instantaneous omitted residual is

    B E_R(s)Omega=-(lambda^2/D)(1-exp(-Ds))F,
    ||B E_R(s)Omega||=beta(1-exp(-Ds)),
    beta=lambda^2 sqrt(195)/(2D).                    (7)

In particular it vanishes exactly at s=0; replacing it by Bf from the start
would lose this actual-input fact. Formula (7) nevertheless keeps every
channel of F for positive time.

Differentiating E(t-s)E_R(s)x for x in P, then integrating, gives the exact
strong Duhamel identity

    (E(t)-E_R(t))x
      =-integral_0^t E(t-s)[B+delta P]E_R(s)x ds.      (8)

All differentiated vectors lie in the common operator domain: E_R(s)x stays
in the finite smooth subspace, and L E_R(s)x is continuous. This suffices for
the vector-valued fundamental theorem; no unbounded operator-norm derivative
is assumed. The plus delta inside the residual is necessary because
(L-epsilon)-(A-mu) on P is B+delta P. In particular the vacuum error has
initial derivative -delta Omega even though B Omega=0.

Contraction and (7) prove for every finite t>=0

    ||(E(t)-E_R(t))Omega|| <= V(t),
    V(t)=beta[t-(1-exp(-Dt))/D]+delta_upper t.         (9)

This is a genuine finite-time, full-operator estimate, with V(0)=0. It is
increasing and eventually grows. It will only be used on an initial window;
its growth is neither physical divergence nor an all-time small bound.

## 4. Independent spectral estimate and positive vacuum denominator

The true and Ritz ground projections give separately

    ||E(t)Omega||>=||G Omega||>=f0-p=:a_v>0,
    ||(I-G)Omega||<=q+p.

Decomposing the two heat outputs spectrally yields

    ||(E(t)-E_R(t))Omega||
       <=L_v(t):=p+(q+p)exp(-g t)+q exp(-D t).        (10)

This estimate is decreasing and valid independently of (9). Both estimates
hold at all finite t, so R(t,Omega)<=min(V(t),L_v(t))/a_v. In particular for
any joining time tau,

    sup_(t>=0) R(t,Omega)
      <=max(V(tau),L_v(tau))/a_v.                    (11)

Equation (11) uses monotonicity of (9) before tau and of (10) after tau.
It does not reuse the late-time X2 claim at time zero or extend a linearly
growing Duhamel estimate indefinitely. The full complement remains in E,
G, g and the complete residual. The denominator is its actual norm with a
proved lower bound, without any denominator regularization.

## 5. Explicit preparation neighborhood and computable overlap class

First take a normalized x in P Hphys and choose its overall phase so that
||x-Omega||<=eta. This is a vector-norm condition in the physical Hilbert
space, not a trace-distance or infidelity convention. Write e=x-Omega.
Because ||B G_R||=rho and the excited Ritz decay is at least exp(-3s),

    ||B E_R(s)e|| <=eta[rho+M exp(-3s)].

Combining this with (8)-(9) proves the initial-window error bound

    V_eta(t)=V(t)+eta[(rho+delta_upper)t+M(1-exp(-3t))/3]. (12)

Normalization matters in the independent spectral and denominator bounds:

    ||E(t)x||>=a_eta:=f0-eta-p>0,
    ||(I-G_R)x||<=q+eta, ||(I-G)x||<=q+eta+p,
    L_eta(t)=p+(q+eta+p)exp(-g t)+(q+eta)exp(-3t).     (13)

Hence the all-time bound is max(V_eta(tau),L_eta(tau))/a_eta. The certified
example is eta=1/100 and tau=8/5. It compares E_R(t)x with E(t)x for the same
prepared input. If the desired target remains E(t)Omega, an additional
preparation bias must be charged: ||E(t)(x-Omega)||<=eta. Thus the absolute
error for that different target is at most eta+max(V_eta(tau),L_eta(tau));
preparation error is not hidden inside the 0.00044 truncation certificate.

Second, a normalized retained input can instead be admitted by the computable
Ritz-overlap condition

    |<f,x>|>=a>p.                                    (14)

It gives the true denominator floor a-p and excited Ritz norm at most
b=sqrt(1-a^2). The same proof yields

    V_a(t)=(rho+delta_upper)t+M b(1-exp(-3t))/3,
    L_a(t)=p+(p+b)exp(-g t)+b exp(-3t),
    sup_t R(t,x)<=max(V_a(tau),L_a(tau))/(a-p).        (15)

The executed example is a=0.99 and tau=2. This is an all-time implication;
its new early term is essential. It is distinct from Z1's inherited
conditional late-time implication. The vector ball in (12) also gives the
explicit Ritz margin |<f,x>|>=f0-eta. At the cap this exceeds 0.9899 and the
corresponding true floor exceeds 0.9898.

Condition (14) is checkable from the 21 coefficients. If a normalized
nominal vector x0 is known within norm eta of actual normalized x, and a
certified calculation encloses |<f,x0>| below by a_nom, then the certified
actual overlap is at least a_nom-eta. When the Ritz vector is approximated by
a unit fhat with error u and the inner-product evaluation has error v, a
computed lower value a_hat gives a_nom>=a_hat-u-v. The normalized vector
(1,h,...,h) has derivative norm at most sqrt(20), so the midpoint construction
below permits the explicit choice u=3 width(h). One must therefore verify
a_hat-u-v-eta>p before dividing. A zero or insufficient floor is rejected;
Z1's ground-null and bright counterexamples are not admitted by this repair.

No claim is made that every retained vector lies in these classes. An
unretained preparation component is outside these numerical thresholds. It
has immediate truncation error ||Qx|| at t=0 and requires a separately stated
budget. This limitation keeps the retained-input time-zero exception exact.

## 6. Continuous coupling certificate and evaluated useful bounds

The computation uses simple analytic envelopes, not a coupling grid. For
any 0<=lambda<=Lambda<=1/100 define

    rbar=sqrt(195)Lambda^2/6, gbar=3-20Lambda,
    pbar=rbar/gbar, dbar=195Lambda^4/(36gbar),
    qbar=sqrt(5)Lambda/3, fbar=sqrt(1-5Lambda^2/9),
    Mbar=sqrt(39)Lambda/2, Dbar=sqrt(9+20Lambda^2).     (16)

Then rho,beta<=rbar, delta_upper<=dbar, p<=pbar, q<=qbar, f0>=fbar,
M<=Mbar, g>=gbar and D,gamma>=3. For the integral in (9),
t-(1-exp(-Dt))/D=integral_0^t(1-exp(-Ds))ds increases with D, so Dbar gives
an upper bound there. Replacing the late bright gap by 3 is conservative.
Every envelope is uniform on the complete interval [0,Lambda]. At Lambda
=1/100, outward rational arithmetic gives the following explanatory values;
the exact fractions in results.json are authoritative.

| Admitted input | Join sigma | True denominator floor | Early absolute bound at join | Late absolute bound at join | All-time relative bound |
|---|---:|---:|---:|---:|---:|
| Actual vacuum | 1.5 | >0.99988910 | <0.000272426 | <0.000278939 | <0.00028 |
| Normalized retained 0.01 vector ball | 1.6 | >0.98988910 | <0.000402430 | <0.000425510 | <0.00044 |
| Normalized retained Ritz overlap >=0.99 | 2 | >0.98991687 | <0.001930150 | <0.000954747 | <0.002 |

The tighter computed relative bounds are approximately 0.000278969856,
0.000429855530 and 0.001949809666. All three are upper certificates for every
time and every coupling in the interval. Additional Lambda=1/200 and zero
rows are interval certificates too, rather than sampled evidence substituted
for (16). Joining times correspond to 1.5,1.6,2 times hbar/alpha. They are
not adjusted physical rates or new model constants, and are not claimed
optimal.

At sigma=0, E(0)x=E_R(0)x=x for every retained x, so the exact relative error
is zero. At lambda=0, B=0, both ground energies vanish and P reduces K;
E(sigma)x=E_R(sigma)x for every retained x and every finite sigma. These
identities take precedence over the coarser separate spectral-tail budget,
which need not vanish for arbitrary excited retained inputs. No residual or
overlap witness is divided by zero at lambda=0.

## 7. Physical truncation, representation and scalar evaluation are separate

For the finite evaluation retain the exact spectral form from X2,

    E_R(sigma)=G_R+exp(-D sigma)(U-G_R)
                       +exp[-(D+3)sigma/2](P-U),

where U projects onto Omega and the symmetric face vector. Enclose D by
rationals of width at most 10^-48, take its midpoint Dhat, and bound
h=lambda/(D+3). The midpoint hhat defines an exact rational normalized
rank-one projector Ghat. The ground coefficient remains exactly one.
Use the positive rounded gaps Dhat and (Dhat+3)/2 for the two excited
projectors. Their all-time representation error is bounded by

    5 width(h)+width(D)/4
      <=(5/3600+1/4)10^-48 <10^-45.                  (17)

The angle estimate follows from the normalized vectors (1,h,...,h); the
excitation-gap error uses sup_s s exp(-3s)<=1/3. Both exact and rounded
representations are exactly P at time zero. Rounding an independent ground
shift would instead grow or remove the asymptotic ground coefficient and
would invalidate this all-time statement. Actual delta>0 also shows why
centering the full heat by mu is a different problem: its true ground grows
as exp(delta sigma).

The scalar evaluator uses the degree-160 positive Taylor polynomial for
exp(x) on 0<=x<=96 and its geometric tail, then reciprocates and rounds
outward at denominator 10^32. Since the polynomial is at least x^80/80!,
the reciprocal interval width before rounding is uniformly bounded by

    96(80!)^2/[161!(1-96/162)].

For x>96 it returns zero with error <=80!/96^80. The maximum, with outward
rounding, is below 3*10^-30; x=0 returns exactly one. Orthogonal excited
projectors make their scalar error cost the maximum. Combining this with
(17) costs less than 4*10^-30 in absolute operator norm, then division by
the respective positive denominator floor adds the stated relative cost.
The checker verifies that all three displayed thresholds survive this cost.
It also produces the rational 21-component evaluated vacuum output at
sigma=1.5. Arbitrary nonnegative rational requested arguments can be
evaluated by the same scalar function; its error proof holds over the real
half-line. This is not a claim that a finite time table evaluates all real
times. For uncertain lambda or time inputs their uncertainty must be charged
separately from this exact-rational arithmetic.

At lambda=0 the physical error is exactly zero. The vacuum numerical output
is exact too, because it contains only its unit ground coefficient. For a
general excited retained input a scalar evaluation of the free heat can
still have the separately stated arithmetic error; no physical truncation
error is manufactured or hidden by that scalar cost.

## 8. Evidence, controls and remaining scope

The standard-library checker writes exactly results.json and controls.json
into a requested fresh absolute output directory. It reconstructs the actual
matrix and full omitted Gram, uses exact rational radical/exponential
enclosures, and has explicit exceptions that remain active under Python -O.
Discriminants reject omitted pair channels, wrong Ritz sign, zero/insufficient
denominator floors, wrong centering and wrong time scope. The early estimate
at sigma=30 fails the advertised small budget, while the late estimate at
zero is too large: the joined theorem, not either claim alone, is admitted.
Normal and optimized fresh replays must give identical output bytes.

All frozen Z2 dependencies and method snapshots are bound, together with the
actual additional source reads, report, checker, input snapshots and frozen
outputs. The X2/Z1 gate files were parsed for admission, scope and binding
structure; duplicated producer manifests are provenance, not new physical
derivations. The complete X2 and Z1 reports and Z1 independent review supply
the inherited premises. The old forward checkers were inspected for actual
graph/arithmetic and submission conventions. Installed Newton/Tesla research
references and paired centering, residual, and reconstruction/interval
lessons were read and snapshotted.
This applies documented methods; it does not claim a fresh primary-source
historical verification or a literature-priority search.

The new physical result is a sufficient finite-graph all-time approximation
certificate on explicitly restricted inputs. It supplies no exact ground
wavefunction, generic all-input relative bound, real-time theorem,
large-volume uniformity, homogeneous or canonical model theorem, physical
mass calibration, continuum construction or verified scientific priority.
Earlier admitted files are unchanged; this producer does not select or start
another loop. Mathematical proofs, rather than checker flags alone,
establish the stated full-operator scope.

    python3 -B research/round24/forward/z2/check.py --output /absolute/fresh/z2-forward
    python3 -B -O research/round24/forward/z2/check.py --output /absolute/fresh/z2-forward-O
