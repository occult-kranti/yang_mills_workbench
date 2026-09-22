# Z2 reverse: all-time relative heat for the actual vacuum and preparations

The actual 21-state Ritz heat, centered at its own ground and evaluated as
specified below, approximates the actual full T-graph heat on its retained
vacuum with true-output-relative vector error **less than 0.000600**, uniformly
for every `0<=lambda<=1/100` and every `sigma=alpha*t/hbar>=0`. For every
retained physical vector `f` with `||f-Omega||<=1/100`, the same-input relative
error is **less than 0.000720**, on the same continuous coupling and time
sets. These are certified upper bounds, not measured approximation errors.

The new short-time argument uses the exact vacuum cancellation and the
complete retained-to-omitted map. It is joined to the independently valid
spectral late-time estimate at `sigma=29/10`. Both true and Ritz ground
energies are retained throughout. The denominator is the actual evolved
norm; no additive floor is inserted into its definition.

At time zero the exact and evaluated retained evolutions agree exactly.
At zero coupling the physical retained evolutions agree at every time; for
the actual vacuum the evaluated vector also agrees exactly. For nonvacuum
preparations at zero coupling, any rounded excited exponential has its
separate scalar arithmetic error. The mathematical physical error remains
exactly zero. The preparation ball does not include all retained inputs.

Authorship is independent reverse model-agent work. No current forward/Z2
solution was read or exchanged before freeze. Accepted X2/Z1 premises are
shared; model-agent reconstruction and review are not external peer review.
Scientific priority is unverified. No additional research loop is executed.

## 1. Reconstruct the target and its sufficient conditions

Starting backward from a useful relative bound requires three ingredients:
a positive lower bound on the true evolved input norm, a small early-time
error respecting retained input, and a small late-time error respecting the
actual two ground projections. Z1's general retained-input obstruction
shows that the denominator condition cannot be omitted. Its late-time
overlap-floor implication supplies only the last part of this reconstruction.

Keep precisely the actual open `(3,3,2)` SU(2) graph, with 18 vertices,
33 links, 20 square faces, product Haar measure and all 18 Gauss constraints.
Use the full infinite-dimensional invariant Hilbert space and

    L=H_lambda/alpha=K+cI-lambda X, c=20lambda,
    X=sum_p x_p, x_p=Tr(U_p)/2,
    P=1_[0,9/2)(K), Q=I-P, A=PLP on P Hphys.

The admitted X1/X2 premises give self-adjointness on `D(L)=D(K)`, compact
resolvent, a smooth invariant polynomial core, form domain `H1` and operator
domain `H2` in the physical space. P reduces K, preserves these domains,
and has orthonormal basis `Omega=1, phi_p=2x_p` for all 20 faces. All retained
vectors and residual products below are smooth physical polynomials. The
full electric excited spectrum is at least 3, and `L>=K`. Thus the true
ground epsilon is simple, the rest of spec L is at least 3, and
`0<=epsilon<=mu<=c<=1/5`, where mu is the actual Ritz ground energy.

Set, each centered by its own exact ground,

    S(sigma)=exp[-sigma(L-epsilon)],
    S_R(sigma)=exp[-sigma(A-mu)]P,
    R(sigma,f)=||(S-S_R)f||/||Sf||, 0!=f in P Hphys.       (1)

For finite sigma the denominator is positive by injectivity of the exact
heat spectral multiplier. On our admitted input class we prove a stronger
uniform positive lower bound below. We never divide by the Ritz output,
the operator norm of S, or a denominator modified by a fitted constant.

The positive physical scales `a,E_star,alpha/E_star,hbar` are fixed. Lambda
is the given constant coupling; energies displayed are in units alpha.
Preparation radius, overlap threshold and proof joining time are
dimensionless approximation diagnostics/input restrictions. The joining
time corresponds to `t=(29/10)hbar/alpha`; it changes no action or clock.
This is neither the selected-memory Htilde, the canonical model, nor the
homogeneous S/W model. No constant is transferred between those models.

Newton analysis/synthesis is applied to the sufficiency of the target
conditions and their synthesis into (1). Tesla's whole-mechanism method
is applied to every omitted physical channel and both centering terms.
Historical analogies supply no mathematical premise or physical parameter.

## 2. Reconstruct the complete retained residual map

The actual Ritz matrix, reassembled in all 21 dimensions, is

    A00=c, A0p=Ap0=-lambda/2, Apq=(3+c)delta_pq.

Write the exact algebraic quantities

    s=sqrt(9+20lambda^2), d=(s-3)/2,
    kappa=lambda/(3+d), mu=c-d,
    N=(1+5kappa^2)^(-1/2), phi_R=N(Omega+kappa X),
    G_R=|phi_R><phi_R|, gamma=3+d.

The exact identities `d=5lambda*kappa` and `(3+d)kappa=lambda` prove the
ground equation. The bright gap is s and the 19 dark gaps are gamma.
These are spectra of A, not an assertion that P is invariant under L.

The complete X2 residual channels are

    chi_p=4x_p^2-1, eta_pq=4x_p*x_q (p<q).

There are 20 normalized orthogonal spin-one channels and 190 normalized
orthogonal face-pair channels, all orthogonal to P. X2's conditional Haar
calculation includes shared edges; pair normalization does not assume all
face holonomies independent. Distinct spin labels establish orthogonality
of the spin-one channels. The actual graph's 190 nonzero pair parity masks
are distinct and not face masks. The checker reconstructs these masks,
including the absence of an XOR-zero set of four distinct faces. Each
shared-edge pair is the complete physical product, including its electric
singlet and triplet components; neither component is discarded.

Let `T=QLP:P Hphys -> Q Hphys`. Since QKP=0, multiplication gives exactly

    T Omega=0,
    T sum_p b_p phi_p
       =-(lambda/2)[sum_p b_p chi_p
                    +sum_(p<q)(b_p+b_q)eta_pq].          (2)

This reconstructs the entire omitted map for every retained vector, rather
than just the ground residual column. For arbitrary complex b, the channel
orthogonality and expansion of the cross terms give

    ||T sum b_p phi_p||^2
      =(lambda^2/4)[19 sum_p |b_p|^2+|sum_p b_p|^2],
    ||T||=beta=(sqrt(39)/2)lambda.                        (3)

On the face coefficients `T* T=(lambda^2/4)(19I+11*)`. The checker constructs
the actual 210-by-21 coefficient matrix and verifies its 21-by-21 Gram
matrix exactly. Its largest eigenvalue is `39lambda^2/4`, attained on the
symmetric face vector. Retaining only spin-one channels would instead give
`lambda^2/4`: a factor-39 error in the squared operator norm. This sharper
retained-map bound follows from the same complete physical channel premise
that already determined X2's ground residual.

In particular

    r=T phi_R=(L-mu)phi_R=-N lambda kappa (X^2-5),
    rho^2=||r||^2=(195/4)lambda^2*kappa^2/(1+5kappa^2).

The residual norm uses all channels:
`X^2-5=(1/4)sum chi_p+(1/2)sum eta_pq`, whose squared norm is
`20/16+190/4=195/4`. Expanding the fourth Haar moment independently gives
`20/8+6*190/16-25=195/4`. These are complete vector decompositions, not a
finite-dimensional replacement for the infinite omitted dynamics.

## 3. Full spectral data and a positive true denominator

Let G be the actual true rank-one ground projection and `delta=mu-epsilon`.
The accepted full spectral-measure argument, using the actual excited
spectrum at least 3 and the finite second moment of phi_R, gives

    0<=delta<=rho^2/(3-mu),
    ||G-G_R||<=D:=rho/(3-mu).                              (4)

For example, the first inequality follows by taking the phi_R expectation
of `(L-epsilon)(L-3)>=0` on spec L; it equals
`rho^2-delta*(3-mu)`. The second follows by applying the residual to the
true excited spectral subspace. The actual gap of `L-epsilon` is at least
`3-epsilon>=3-mu`; no finite-matrix gap is substituted for this premise.

For later controls, the complete residual and its kinetic support at K<=8
also give, as in reverse X2/Z1,

    delta >= rho^2/(8+40lambda-mu+rho)>0  (lambda>0).

This follows from the true two-vector variational compression on phi_R
and r/rho. The positive-coupling normalization is not used at lambda=0.
Forward X2's sharper first energy moment remains attributed to that
accepted direction and is not used or claimed rediscovered here.

Since `||G_R Omega||=N`, the triangle inequality gives

    ||S(sigma)Omega||>=||G Omega||>=N-D.

If `f=Omega+e` is retained and `||e||<=eta`, then

    ||S(sigma)f||>=||Gf||>=N-D-eta.                       (5)

This lower bound is for the original true output; it is not an alteration
of (1). Norms need not be exactly one inside the stated ball, and
`||f||<=1+eta`. Unit physical preparations, with phase aligned to Omega,
are included whenever they satisfy the ball condition. Nonretained errors
are outside this certificate: the evaluated finite heat acts as P at zero
time and would immediately discard such components.

## 4. Genuine short-time Duhamel estimate for the vacuum and its ball

On the common retained domain, the exact intertwining defect between the
two own-ground-centered generators is

    (L-epsilon)P-P(A-mu)=T+delta P.

Differentiate `S(sigma-u) S_R(u)f` strongly for retained f and integrate:

    (S-S_R)f
       =-integral_0^sigma S(sigma-u)(T+delta P)S_R(u)f du.

Every `S_R(u)f` is a smooth retained polynomial. The full S is strongly
continuous and contractive, and T+delta P is bounded on the finite retained
space. These facts justify the vector integral with the actual unbounded
full generator. All exterior returns remain inside the full S factor.
No autonomous evolution on the residual channel set is assumed.

The actual vacuum has no dark Ritz component, so

    S_R(u)Omega=e^(-s u)Omega+(1-e^(-s u))N phi_R,
    T S_R(u)Omega=N(1-e^(-s u))r.

The missing-channel source is exactly zero initially, as (2) requires.
Using contraction on the delta term gives the genuine early-time bound

    ||(S-S_R)Omega||
       <=delta*sigma+N*rho*J_s(sigma),
    J_s(sigma)=sigma-(1-e^(-s sigma))/s.                  (6)

Here `J_s(0)=J'_s(0)=0`; its omitted-channel contribution begins at
`N*rho*s*sigma^2/2`. The total derivative need not vanish because the
two exact centering energies differ by delta. Directly in the actual
graph, `Q(L-epsilon)Omega=0` and
`Q(L-epsilon)^2 Omega=T A Omega=lambda^2(X^2-5)`.
Its squared norm is `(195/4)lambda^4>0` at positive coupling. The checker
verifies that coefficient vector, including all pair channels. Thus a
first-derivative or retained-vacuum cancellation is not mistaken for a
closed evolution.

For arbitrary retained preparation error e, use
`S_R(u)e=G_R e+S_R(u)(P-G_R)e`. Since `||T G_R||=rho`,
`||T||=beta`, and the Ritz excited gap is gamma,

    ||T S_R(u)e||<=eta*(rho+beta*e^(-gamma u)).

The centering term adds at most `delta*eta*sigma`. Therefore

    ||(S-S_R)f|| <= E_eta(sigma)
      :=delta*sigma+N*rho*J_s(sigma)
        +eta*[(delta+rho)*sigma
               +beta*(1-e^(-gamma sigma))/gamma].        (7)

This is a new retained-input estimate, valid from zero time and involving
the actual complete omitted residual. Its preparation budget is tighter
than replacing T by the generic potential bound `20lambda`, or than
integrating beta*eta without using Ritz excited decay.

## 5. Join to late-time spectral control over a continuous coupling interval

Independently of the Duhamel derivation, true and Ritz spectral calculus
give the X2 absolute bound

    ||S-S_R|| <=D+e^(-(3-mu)sigma)+e^(-gamma sigma).

On the preparation ball this implies

    ||(S-S_R)f|| <=L_eta(sigma)
      :=(1+eta)[D+e^(-(3-mu)sigma)+e^(-gamma sigma)].      (8)

The two quantities (7) and (8) bound the same numerator for the same
operators and the same retained vector. Dividing their minimum by the
positive (5) proves an all-time relative certificate. This avoids both
invalid extrapolations: a spectral tail evaluated at late time cannot
prove smallness at zero, and the growing early Duhamel budget cannot alone
give a useful uniform bound on an infinite time interval.

For a transparent certificate on every `0<=lambda<=ell<=1/100`, define

    rho_bar=sqrt(195/4)*ell^2/3,
    h_bar=3-20ell, D_bar=rho_bar/h_bar,
    delta_bar=rho_bar^2/h_bar,
    N_under=(1+5ell^2/9)^(-1/2),
    beta_bar=sqrt(39)*ell/2, s_bar=sqrt(9+20ell^2).

Indeed `kappa<=ell/3`, `N<=1`, `mu<=20ell`, `s<=s_bar`, and `gamma>=3`.
Thus rho, delta, D and beta have the displayed upper bounds; N has the
displayed lower bound. No sampled monotonicity in coupling is needed.
The function `J_s(sigma)=integral(1-e^(-s u))du` increases with s, and
`(1-e^(-gamma sigma))/gamma=integral e^(-gamma u)du` decreases with gamma.
Consequently valid uniform replacements in (7)-(8) are

    Ebar_eta(sigma)=delta_bar*sigma+rho_bar*J_sbar(sigma)
        +eta*[(delta_bar+rho_bar)*sigma
                   +beta_bar*(1-e^(-3sigma))/3],
    Lbar_eta(sigma)=(1+eta)[D_bar+e^(-h_bar*sigma)+e^(-3sigma)],
    q_eta=N_under-D_bar-eta>0.                            (9)

Ebar increases with sigma and Lbar decreases. With any fixed joining time
T>0, (9) yields on the entire half-line

    R(sigma,f)<=min(Ebar_eta(sigma),Lbar_eta(sigma))/q_eta,
    sup_(sigma>=0) R(sigma,f)
       <=max(Ebar_eta(T),Lbar_eta(T))/q_eta.              (10)

Use `ell=1/100`, `T=29/10`. Exact outward rational arithmetic gives the
following rounded explanatory values; the JSON fractions are authoritative.

| Quantity | Vacuum, eta=0 | Retained ball, eta=0.01 |
|---|---:|---:|
| True-output floor q_eta | 0.9998891029031 | 0.9898891029031 |
| Early absolute bound at T | 0.0005974367868 | 0.0007082526917 |
| Late absolute bound at T | 0.0005472349480 | 0.0005527072974 |
| All-time relative upper bound | 0.0005975030481 | 0.0007154869061 |
| Safe strict bound, including evaluation | 0.000600 | 0.000720 |

The column bounds are upper certificates for every coupling in the frozen
interval. Time and coupling sample tables in results.json illustrate the
formulas but are not used to cover either continuous variable. Zero coupling
is also treated by its exact reducing-space identity, giving physical error
zero rather than merely the nonzero endpoint majorant. At sigma=0 (6)-(7)
give exactly zero, before any division.

## 6. Checkable overlap, preparation margin and the distinct ideal-input task

For any nonzero retained f, an independently certified Ritz overlap

    |<phi_R,f>|>=a||f||, a>D

implies `||Sf||>=(a-D)||f||` at every time. For the explicit preparation ball,

    |<phi_R,f>|/||f|| >=(N-eta)/(1+eta)
       >=(N_under-eta)/(1+eta)>0.9801705181>0.98.          (11)

Hence it has a checkable positive normalized overlap margin as well as the
stronger direct denominator (5). The actual coefficients needed to check
an input are just

    |<phi_R,f>| = N |f_0+(kappa/2)sum_p f_p|.

For input coefficients represented with interval uncertainty, enclose this
scalar and ||f||. Equivalently use the rational Ghat of the next section:
`||Ghat f||/||f||` is computed from its rational quadratic form. Its
difference from the exact normalized Ritz overlap is at most
`||Ghat-G_R||`. Include coefficient/norm evaluation error as an additional
certified amount e_ov and require `a_hat-e_ov>D`. Coefficient preparation
uncertainty and arithmetic uncertainty are different terms; a merely
computed positive overlap with no error margin is insufficient.

The all-time mechanism also applies more broadly to an overlap cone,
without asserting the sharper ball bound. For every retained f,

    ||(S-S_R)f||/||f||
       <=(delta+rho)*sigma+beta*(1-e^(-gamma sigma))/gamma.

This follows from the preparation-error part of the same complete-map
Duhamel argument. Combine it with (8) at eta=0 and divide by a-D.
At the cap majorants, `a=0.98`, `T=29/10`, the resulting all-time physical
relative bound is below 0.012 (the enclosed value is about 0.011308705).
Thus the checkable overlap condition has an all-time version, not only
Z1's late-time implication. Its looser bound is not substituted for the
stronger vacuum-neighborhood result.

If the purpose is to compare the evolved prepared vector with the ideal
vacuum's evolved vector, that is a different input comparison. Since S is
contractive, `||Sf-SOmega||<=eta`. The corresponding bound for evaluated
Ritz heat is

    ||S_evaluated f-S Omega||/||S Omega||
      <=[min(Ebar_eta,Lbar_eta)+eta+e_eval*(1+eta)]
           /(N_under-D_bar).                            (12)

The eta in (12) is state-preparation bias relative to the intended ideal
input; it is not physical truncation or scalar arithmetic. The headline
0.000720 result compares both evolutions on the same prepared f as (1)
requires, not with a different ideal input. No state-preparation measurement
or laboratory feasibility is claimed.

At `a<=D` or `eta>=N_under-D_bar`, this denominator certificate supplies
no positive floor and is rejected. This is failure of the sufficient
condition, not a claim that every such actual denominator vanishes. The
retained Ritz-bright vector `(A-mu)Omega` has exactly zero Ritz overlap;
the checker verifies its exclusion. Z1's actual counterexamples and
unrestricted failure remain intact.

## 7. An all-time scalar evaluator with exact ground and endpoint behavior

Let U be the projection onto Omega and the symmetric face vector, and
`P_dark=P-U`. The exact small heat representation is

    S_R=G_R+e^(-s sigma)(U-G_R)+e^(-gamma sigma)P_dark.    (13)

The checker encloses s by integer-square-root bounds at denominator 10^30,
then encloses kappa by rational interval operations. Choose midpoint
values kappa_hat, s_hat and `gamma_hat=(3+s_hat)/2`. Form

    v_hat=Omega+(kappa_hat/2)sum_p phi_p,
    Ghat=|v_hat><v_hat|/(1+5kappa_hat^2).

This is an exact rational rank-one orthogonal projection. Its full 21-by-21
idempotence and trace are executed. It lies in U, so `U-Ghat` and P_dark
are exact mutually orthogonal projections. Each remains paired with a
positive rounded excited gap; the ground coefficient is exactly one.

For all allowed rational coupling inputs, the s interval has width at most
10^-30 and the kappa interval has width less than 10^-30. The elementary
rank-one angle identity gives
`||Ghat-G_R||<=sqrt(5)|kappa_hat-kappa|<=(9/4)10^-30`.
For positive a,b, the mean-value estimate
`sup_sigma |e^(-a sigma)-e^(-b sigma)|<=|a-b|/min(a,b)`
controls each excited gap; both exact and rounded gaps are at least 3.
In (13) the projection difference is multiplied by `1-e^(-s_hat sigma)`.
A safe uniform representation bound is therefore

    e_rep <= [(9/4)+(2/3)]10^-30.

No rounded absolute ground energy is multiplied by an unbounded time.

For actual scalar evaluation at x>=0, the checker returns exactly 1 at x=0.
For `0<x<=96`, it bounds e^x between its degree-160 positive Taylor
polynomial and that polynomial plus
`x^161/[161!*(1-x/162)]`, reciprocates, rounds endpoints outward at
denominator 10^30, and returns the midpoint. The reciprocal interval's
unrounded width is at most

    W=96*(80!)^2/[161!*(1-96/162)].

This follows because the Taylor polynomial is at least `x^80/80!`.
The scalar midpoint error is at most `W/2+10^-30<3*10^-30`. For x>96,
the evaluator returns zero; the exact tail is at most
`80!/96^80<3*10^-30`. These inequalities are checked rationally. Thus the
procedure has a uniform all-time scalar guarantee, including the unbounded
time branch; a table at finitely many times is not presented as the proof.
The two excited projections are orthogonal, so scalar errors cost their
maximum. A safe combined bound is

    e_eval <= [(9/4)+(2/3)+3]10^-30 <6*10^-30.

Its relative cost is `e_eval*(1+eta)/q_eta`, approximately 6*10^-30 for
the ball, far below the physical truncation budget. There is no sampling
uncertainty. The executable accepts exact rational time/coupling data;
the analytic estimates hold for all real times/couplings. Encoding or
calibration error in an arbitrary real physical input is an additional
error source, not silently charged to this scalar guarantee.

At sigma=0 all scalar factors are exactly one and the evaluated operator
is exactly P, hence identity on every admitted input. At lambda=0,
`Ghat=G_R=|Omega><Omega|` and the evaluated vacuum output is exactly Omega
for all times. Exact physical evolution on a general retained vector is
`G_R+e^(-3sigma)(P-G_R)` in both models. A nonvacuum vector can retain the
small scalar evaluation error in its excited factor; it does not have a
spurious physical truncation error.

One-sided miscentering is a genuine rejecting control. The actual positive
delta lower bound implies that at `sigma=1/delta_lower`, centering the
Ritz heat by epsilon reduces its ground coefficient below e^-1<1/2,
while centering full L by mu increases its ground coefficient above e>2.
These are changes to the centering, not the exact representation (13).
A common scalar rescaling of numerator and its matching denominator would
cancel; it does not justify changing only one evolution.

## 8. Executable checks, source scope and limits

The standard-library checker uses explicit exceptions rather than Python
assertions. Its 15 genuine Boolean controls include the complete retained
map and factor-39 lost-channel failure, the actual vacuum second derivative,
the zero overlap/preparation floor, the actual one-sided centering error,
the need for both time regimes, the excluded bright input, exact endpoints,
and the rational projector/scalar tail. A large early-time budget does not
prove actual long-time error; it only demonstrates why that bound alone
cannot certify the stated target.

All contract-declared dependencies and instruction snapshots are checked
against the frozen contract. The source inventory records actual additional
reads; live instruction/skill references read for this producer are copied
into owned immutable input snapshots with origin hashes. Prior reverse Z1's
checker and packaging were read for their exact arithmetic and binding
format, without importing or executing its implementation. Both X2 reports,
both Z1 reports, the Z1 review, decision and gates provide admitted context.
No current forward Z2 material was read. No outside technical lookup was
needed: the new map, Duhamel and spectral estimates are explicitly derived
from the named complete physical premises. Selected historical reference
notes are method context, not a claim of fresh primary-source reading.

The following replay commands each write exactly results.json and
controls.json into a fresh external directory:

    python3 -B research/round24/reverse/z2/check.py --output /absolute/fresh/z2-reverse
    python3 -B -O research/round24/reverse/z2/check.py --output /absolute/fresh/z2-reverse-O

Normal and optimized outputs must match byte-for-byte before freeze. The
submission binds the contract, every declared instruction/dependency,
actual additional input snapshots and reads, the report, checker, source
inventory, replay and both frozen outputs. Earlier and shared files remain
unchanged. Independent model-agent review, same-producer interpreter
replay, and physical evidence have distinct roles.

This establishes a useful finite-graph, all-time heat approximation on the
actual vacuum and the stated retained input classes. It gives no unrestricted
relative bound, no exact interacting ground, no real-time estimate, no
growing-volume guarantee, no model identification or fitted energy/clock,
and no homogeneous or four-dimensional continuum mass-gap construction.
The new preparation condition repairs a precise approximation question;
it does not repair the unresolved parent continuum problem.
