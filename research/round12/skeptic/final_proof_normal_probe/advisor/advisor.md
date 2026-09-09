# Round 12 advisor: rigorous driven truncation and the remaining bridges

Contract: `ym12-driven-two-square-v1`. Date: 9 September 2026. This is an exact finite-graph evolution theorem and a bounded review of two proposed bridges. The graph and gauge theory are unchanged from round 11. Representation truncation, time integration, floating-point evaluation, graph volume, and the continuum limit are separate operations. No mass field or adjustable gap term is introduced.

The new result is a factorial bound for exact full versus exact Galerkin evolution from a state with finite polynomial-degree support. For the electric vacuum and degree cutoff D,

\[
 \|\psi(t)-\psi_D(t)\|
 \le \min\{2,A(t)^{D+1}/(D+1)!\},\qquad
 A(t)=\int_0^t(|\lambda_1(s)|+|\lambda_2(s)|)\,ds.
 \tag{DYN1}
\]

There is no exponential factor in this bound. A separate numerical evolution error must still be added before a computed trajectory is certified. The derivation and constants below were independently examined by the round-12 skeptic; the solver independently identified the same block argument. Those reviews are mathematical reviews, not proof-assistant formalizations.

## 1. What round 11 already completed

The inherited setting is the open two-square graph with seven distinct oriented links and six independently gauged vertices. Both plaquette loops are based at the upper shared vertex and have the same circulation. Tree gauge leaves (U,V) modulo simultaneous conjugation, with

\[
 x=\operatorname{Tr}U/2,\quad y=\operatorname{Tr}V/2,
 \quad z=\operatorname{Tr}(UV)/2,
\]

\[
 \Omega=\{ |x|,|y|\le1:(z-xy)^2\le(1-x^2)(1-y^2)\},
 \quad d\mu=(2/\pi^2)\,dx\,dy\,dz.
\]

The physical space is L²(Omega,mu), interpreted through invariant functions on SU(2)^2. The shared-link electric derivative is L_U-R_V, where the skew generators use exp(i s sigma_a/2). The physical operator is

\[
 K_\rho=3(C_U+C_V)+\rho S,
 \qquad S=-\sum_a(L_U^a-R_V^a)^2,
 \quad \rho>0.
 \tag{BASE1}
\]

rho=1 is the uniform seven-link sum. Other fixed positive rho values weight this existing shared electric energy. They do not add a field. The trace-coordinate mixed derivatives and inherited group domain remain essential. The constant normalized Haar wavefunction, denoted e0=1, is the unique electric ground state. It is the initial vacuum of the full Hamiltonian only when the initial magnetic coefficients vanish.

Let P_d be the orthogonal projector onto all polynomials of total degree at most d, with P_(-1)=0 and Pi_d=P_d-P_(d-1). Round 11 established:

* dim P_d=binomial(d+3,3), and the polynomial union is dense.
* Every P_d reduces K_rho, so every orthogonal degree shell is invariant.
* The complete electric eigenvalues are 3j(j+1)+3k(k+1)+rho*ell(ell+1), with j=(a+c)/2, k=(b+c)/2, ell=(a+b)/2 for a,b,c>=0.
* The physical realization is selfadjoint on the lifted invariant H²(SU(2)^2) domain, or equivalently the closure of the polynomial operator. No Dirichlet condition is imposed on the physical wavefunction at the boundary of Omega.
* Exact stationary finite-to-infinite gap certificates and a continuous coupling-square bound were independently replayed.

The round-11 driven histories were finite-Galerkin numerical studies. Their observed degree differences, norm defects and work residuals did not certify the untruncated evolution. This round supplies the missing representation-error theorem; it does not retroactively rename the old numerical diagnostics. Historical source and output files remain unchanged.

## 2. Dynamical assumptions and existence

On a finite interval [0,T], consider

\[
 H(t)=\alpha(t)K_\rho+
 \lambda_1(t)(I-X)+\lambda_2(t)(I-Y),
 \quad (Xf)(x,y,z)=xf,quad (Yf)(x,y,z)=yf.
 \tag{H12}
\]

For the physical driver family, alpha(t)>0 and lambda_i(t)>=0 are prescribed coefficients, and rho is fixed. The state-norm theorem itself only needs real locally integrable alpha and real lambda_i with w(t)=|lambda1(t)|+|lambda2(t)| integrable. Smooth positive coefficients are a sufficient more restrictive working contract. hbar=1, so energy times time is dimensionless. Restoring hbar divides all integrated generator actions by hbar.

Remove the common scalar phase chi(t)=integral_0^t(lambda1+lambda2)ds and define W(t)=-lambda1(t)X-lambda2(t)Y. Its norm is at most w(t), since ||X||=||Y||=1. Put theta(t)=integral_0^t alpha(s)ds. The electric propagator is U0(t,s)=exp[-i(theta(t)-theta(s))K_rho], a unitary operator preserving every P_d. The interaction-picture perturbation U0(0,t)W(t)U0(t,0) is strongly measurable, bounded, selfadjoint and has integrable norm. The norm-convergent iterated integral construction gives a unique unitary interaction-picture propagator. This defines full mild evolution without pretending that K_rho is bounded.

The Galerkin Hamiltonian is H_D(t)=P_D H(t)P_D on P_D. Its finite evolution is unitary in the physical Haar inner product. The full and projected states use the same initial vector and the same scalar phase. Removing a phase on only one side changes the state-norm comparison. Gauge invariance is preserved throughout because the physical Hilbert space and all operators are already gauge invariant.

For the main theorem assume a normalized initial state psi0 in P_d0 and D>=d0. The electric vacuum has d0=0. No assumption is made that psi(t) stays in that initial shell. If lambda_i(0) are nonzero, the initial constant state is still covered by the mathematics but must not be called the interacting vacuum.

## 3. Degree bandwidth is the decisive structural lemma

Multiplication by x or y maps P_d into P_(d+1). Selfadjointness gives the reverse restriction: if r>=d+2, then for f in Pi_r and g in Pi_d,

\[
 \langle f,Xg\rangle=0,\qquad
 \langle f,Yg\rangle=0,
\]

because Xg,Yg are in P_(d+1). Taking adjoints handles r<=d-2. Therefore

\[
 \Pi_r W(t)\Pi_d=0\quad\text{if }|r-d|>1.
 \tag{BAND1}
\]

This is a bandwidth-one statement in orthogonal physical degree shells. It would not follow from a raw matrix that uses monomials with the Euclidean inner product. Conjugating by the electric propagator preserves (BAND1), because that propagator preserves every shell. A common scalar potential affects phase but cannot cross a shell boundary.

The shared link is present in K_rho and controls its spectrum and phases. The theorem does not replace it by independent rotors. It uses only the proved fact that its exact physical action preserves the degree flag.

## 4. One-sided Duhamel proof and the factorial constant

First work with the exact normalized Galerkin solution psi_D. For d0<n<=D define R_n^D=P_D-P_(n-1), the finite tail of shells n through D, and u_n=R_n^D psi_D. Since the electric term is block diagonal, the equation for u_n contains its own selfadjoint compressed Hamiltonian plus one forcing term:

\[
 i\dot u_n=R_n^D H_D R_n^D u_n
 +\Pi_n W(t)\Pi_{n-1}\psi_D(t).
 \tag{TAIL1}
\]

The initial u_n vanishes. The homogeneous propagator in this finite block is unitary. Duhamel and ||W||<=w imply

\[
 \|u_n(t)\|\le\int_0^t w(s)
 \|\Pi_{n-1}\psi_D(s)\|\,ds.
 \tag{TAIL2}
\]

At the first step, the source norm is at most one. At later steps it is at most ||u_(n-1)||. Induction, using A'=w almost everywhere, gives

\[
 \|R_n^D\psi_D(t)\|
 \le\min\{1,A(t)^{n-d_0}/(n-d_0)!\}.
 \tag{TAIL3}
\]

For n=D this controls the last retained shell. Embed psi_D into the full space. Its only missing Schrödinger forcing is

\[
 r_D(t)=(I-P_D)H(t)\psi_D(t)
 =\Pi_{D+1}W(t)\Pi_D\psi_D(t).
 \tag{RES1}
\]

The full propagator is unitary, so variation of constants gives the exact a posteriori inequality

\[
 \|\psi(t)-\psi_D(t)\|
 \le\int_0^t\|r_D(s)\|\,ds.
 \tag{RES2}
\]

For d0=D, the last-shell norm is simply bounded by one. For D>d0 use (TAIL3). In both cases,

\[
 \boxed{\displaystyle
 \|\psi(t)-\psi_D(t)\|
 \le\varepsilon_D(t):=
 \min\left\{2,\frac{A(t)^{D-d_0+1}}{(D-d_0+1)!}\right\}.}
 \tag{FACT1}
\]

The cap 2 follows because both states have norm one. A Dyson comparison that bounds the two complete series separately would introduce a factor 2 and an exponential tail majorant. Neither is necessary: (RES2) has one forcing term, and the tail-block induction uses exact unitary evolution. This argument retains all repeated excursions within the projected space and does not discard higher perturbative orders.

If A(t)<=Amax is proved for the interval, the same bound with Amax holds uniformly in time. For a general initial state approximated by a normalized phi0 in P_d0, add the independently bounded initial norm error ||psi0-phi0||. Unitarity transports that preparation error without growth. An interacting initial ground state with an infinite representation tail therefore needs an initial-state certificate in addition to (FACT1).

This is a bounded partial theorem toward controlled dynamics. It establishes convergence as D increases at fixed graph, time interval, drive action and initial support. It is neither a uniform-in-time statement for a drive with growing A nor a spectral mass-gap theorem.

## 5. What the new common action variable means

For alpha(t)>0 define kappa_i=lambda_i/alpha, kappa_plus=kappa1+kappa2, kappa_minus=kappa1-kappa2, and tau(t)=integral_0^t alpha(s)ds. Then

\[
 w(t)=\alpha(t)\max(|\kappa_+(t)|,|\kappa_-(t)|),
\]

\[
 A(t)=\int_0^{\tau(t)}\max(|\kappa_+|,|\kappa_-|)\,d\tau.
 \tag{SCALE1}
\]

For nonnegative magnetic coefficients, kappa_plus>=|kappa_minus| and A=integral kappa_plus d tau. Thus forward Hamiltonian coefficients and backward error bounds use the same coefficient map and the same physical clock. A is an integrated prescribed drive, not a physical field, a fitted mass, a regulator, or a free quantity chosen after seeing the error.

At fixed physical lambda_i(t), the estimate does not depend explicitly on alpha: the unbounded electric part contributes only unitary motion within degree shells. The actual error can still depend strongly on alpha through phases. At fixed kappa_i and fixed physical duration T, changing a constant alpha changes tau and A. At fixed dimensionless protocol and dimensionless duration, changing alpha rescales physical time. These are different comparisons. Equal A does not imply equal evolved states; it supplies the same conservative bound, not an equivalence of protocols.

Signed drivers illustrate why absolute values are required. A vanishing signed integral of a coefficient is not a small interaction action in a noncommuting evolution. A final leakage probability is also insufficient: in the elementary two-state example H=sigma_x, initial |0>, and a cutoff retaining only |0>, the full state at t=pi is -|0>. Leakage is zero while the same-phase vector error is 2. Phase-insensitive observables can agree in that example, so the claimed metric must always be named.

## 6. Rigorous residual evaluation and time-integration separation

The boundary norm in (RES2) has an exact finite algebraic representation. If c(t) is the monomial coordinate vector of psi_D and G is the exact Haar Gram matrix, let M(t) be the form matrix of P_D W P_D and N(t) the form matrix of P_D W² P_D. Then

\[
 \|r_D(t)\|^2=c(t)^*\,[N(t)-M(t)G^{-1}M(t)]\,c(t).
 \tag{GRAM1}
\]

This is the same boundary quadratic form used in round 11, now evaluated on the actual trajectory. It is positive semidefinite. It is not the Euclidean squared norm of raw coefficient entries. A verified integral of its square root can be sharper than (FACT1), especially for the previous stronger drive. Point samples or an ordinary quadrature error estimate do not certify its integral.

For an absolutely continuous computed path tilde psi_D inside P_D, define its finite-equation residual

\[
 d_D(t)=i\dot{\widetilde\psi}_D(t)-H_D(t)\widetilde\psi_D(t).
\]

Unitarity of exact Galerkin evolution proves

\[
 \|\psi_D(t)-\widetilde\psi_D(t)\|
 \le\eta_{\rm init}+\int_0^t\|d_D(s)\|\,ds
 =:\eta_{\rm time}(t).
 \tag{NUM1}
\]

Combining with (FACT1) gives

\[
 \|\psi(t)-\widetilde\psi_D(t)\|
 \le\varepsilon_D(t)+\eta_{\rm time}(t).
 \tag{NUM2}
\]

The cap 2 need not apply to a nonnormalized numerical state. A declared ODE tolerance, small norm defect, energy/work agreement, or agreement of two solvers is not a rigorous bound on the integral in (NUM1). Such results remain numerical diagnostics unless a validated residual or another rigorous time-integration bound is supplied.

A direct full-equation residual also exists. The finite residual is in P_D and the missing-boundary term is orthogonal to it, so

\[
 \|i\dot{\widetilde\psi}_D-H\widetilde\psi_D\|^2
 =\|d_D\|^2+\|(I-P_D)W\widetilde\psi_D\|^2.
 \tag{NUM3}
\]

This supports a combined a posteriori enclosure if both terms and their time integral are rigorously bounded. One must not substitute a numerical path into the exact-unitarity induction of Section 4 without accounting for its residual and initial error.

### A concrete finite-dimensional midpoint bound

On one interval of length h with midpoint m, suppose the finite physical H_D(t) is twice continuously differentiable. Put B=H_D(m), C=H_D'(m), and M2=sup ||H_D''(t)|| on this interval. Then exact frozen-midpoint evolution satisfies

\[
 \|U_D(t+h,t)-e^{-ihB}\|
 \le \frac{h^3M2}{24}
 +\frac{h^3\|[B,C]\|}{12}
 +\frac{h^4\|C\|^2}{32}.
 \tag{MID1}
\]

To prove it, compare H_D with B+(s-m)C. The integral norm of the Taylor remainder is M2*h³/24. In the B interaction picture the linear perturbation is (s-m)C_s. Its first integral can replace C_s by C_s-C_m because integral(s-m)ds=0. The bound ||C_s-C_m||<=|s-m| ||[B,C]|| gives the h³/12 term. The second Duhamel remainder is at most one half the square of integral |s-m| ||C|| ds, namely h⁴||C||²/32; exact unitarity avoids an exponential estimate. Summing local errors is valid by telescoping products of unitary exact and frozen-step propagators.

Every norm in (MID1) is on the finite physical Gram space. It is invalid to use ||K|| as a finite number on the full Hilbert space. Also, the compressed matrices P_D X P_D and P_D Y P_D need not commute even though X and Y commute before projection. Their commutator must not be discarded when calculating [B,C]. For fixed alpha and a centered scalar phase, ||C|| and M2 are bounded by the sums of the absolute coefficient derivatives. A crude bound is ||[B,C]||<=2||B|| ||C||; an exact finite matrix norm bound can improve it.

If derivative bounds are unavailable, the simpler exact Duhamel inequality integral ||H_D(s)-H_D(m)|| ds remains valid. At constant alpha, using first-derivative coefficient bounds L1,L2 gives a local h²(L1+L2)/4 estimate. It is conservative and only first order after summation, but does not require claiming an unproved second-order global constant.

Even a rigorous midpoint discretization bound does not certify the evaluation of matrix exponentials or floating arithmetic. For a finite selfadjoint B and a proved ||B||<=R, the Taylor polynomial of exp(-ihB) through degree q has operator remainder at most (hR)^(q+1)/(q+1)!, by the integral remainder and unitarity. This allows a separate validated exponential layer. If each approximate step has operator error beta_j relative to the exact unitary frozen step, the product error is at most product_j(1+beta_j)-1. Exact rational computation or outward-rounded interval arithmetic must also account for the actual arithmetic used. An unverified floating matrix exponential is not made exact by attaching this analytic formula.

## 7. Bounded observables and a carefully delimited energy result

For two normalized states at distance epsilon and any bounded selfadjoint observable O,

\[
 |\langle O\rangle_\psi-\langle O\rangle_\phi|
 \le\min\{2\|O\|,2\|O\|\epsilon\}.
 \tag{OBS1}
\]

For x,y,z the norm is one. Differences of expectations of 1-x or 1-y have the same bound as x or y because the constant cancels between normalized states. This cancellation requires modification if a numerical state is not normalized. A general safe estimate uses (||psi||+||tilde psi||)||O|| ||psi-tilde psi||.

For completeness, expand the difference as <psi-phi,O psi>+<phi,O(psi-phi)> and apply Cauchy–Schwarz to each term. Unit norms give the factor two. Each expectation lies in [-||O||,||O||], giving the separate cap. This proves (OBS1) for a named bounded observable and a proved operator norm; it supplies no inequality for an unbounded observable without additional assumptions.

Neither K nor H is bounded, so (OBS1) cannot be used with an invented global energy norm. There is a separate energy corollary at fixed alpha and rho. Assume differentiable real lambda_i and sufficient common-domain/form regularity for the full and Galerkin work identities. Smooth initial polynomial states and smooth finite drivers are a sufficient working setting. Each exact solution obeys

\[
 \frac{d}{dt}\langle H(t)\rangle
 =\dot\lambda_1\langle I-X\rangle+
 \dot\lambda_2\langle I-Y\rangle.
 \tag{WORK1}
\]

The same initial retained vector has identical initial full and Galerkin energy. The Galerkin work identity has no extra boundary contribution because expectations of H and P_D H P_D agree on a state in P_D. Therefore (OBS1) gives

\[
 |E(t)-E_D(t)|\le
 2\int_0^t (|\dot\lambda_1|+|\dot\lambda_2|)
 \varepsilon_D(s)\,ds.
 \tag{WORK2}
\]

This controls energy through the proved work identities and bounded coordinates, not through the norm of H. Work must be computed by its own integral in a numerical test, with quadrature and state errors controlled separately. Defining work as an endpoint energy difference would make the test circular. For jumps in a piecewise driver include the corresponding instantaneous parameter-work terms; the smooth-driver formula alone does not include them.

If alpha varies, the physical energy balance includes dot alpha <K>. If rho varies it also includes the derivative of the shared-link coefficient times <S>. The simple (WORK2) proof then needs additional moment control or a separately derived rescaled-energy argument. The state-norm theorem does not by itself fill this unbounded-observable premise.

## 8. Concrete scale checks and acceptance boundary

For vacuum start and A(T)=1/2, the representation-only bounds are exactly 1/384 at D=3 and 1/3840 at D=4. These are approximately 0.00260417 and 0.000260417. They concern exact evolutions, independent of the time-stepping implementation.

The round-11 cosine protocol has lambda1=1-cos(pi*t/2), lambda2=1.5[1-cos(pi*t/2)] on [0,2], hence A(2)=5. At D=4, (FACT1) caps at 2 and is uninformative. This is an honest limitation of a conservative bound, not a failed evolution. A shorter or weaker explicitly declared drive can answer the bounded test of whether the theorem and computation agree; it does not improve the accuracy claim for the unchanged old protocol. For that stronger protocol, a validated boundary-residual integral is the more informative next route.

The minimal numerical acceptance contract distinguishes four quantities: a rigorously bounded drive action; the analytic representation bound; a rigorous time-discretization/residual bound; and a bound for exponential evaluation/roundoff. If only the first two are implemented, the delivered result is an exact representation theorem plus numerical comparisons, not a certified total numerical state error. Mutations must reject signed-area substitution, a wrong initial degree, a wrong cutoff index, removal of the last-shell coupling, Euclidean use of a nonorthogonal Gram matrix, and a dropped common scalar phase in a vector-norm comparison.

### A new exact-rational fixture can close the numerical layer

Consider a newly declared piecewise-constant protocol with alpha=rho=1, electric-vacuum initial state, D=3 and two successive intervals of physical duration one. Choose (lambda1,lambda2)=(1/20,1/10) on the first interval and (1/10,1/20) on the second. These coefficients are nonnegative and weight the existing plaquette terms. The protocol is distinct from the old cosine history; starting from the electric vacuum does not assert ground-state preparation for the nonzero first magnetic Hamiltonian.

For both intervals the action rate is 3/20, so A(2)=3/10 and

\[
 \varepsilon_{\rm rep}=\frac{(3/10)^4}{4!}
 =\frac{27}{80000}.
 \tag{EX1}
\]

The maximum eigenvalue of K on P_3 is 45/2. More generally, at rho=1 the degree-D maximum is 3D(D+2)/2: the quadratic electric energy is convex on the exponent simplex, and its maximum is attained at c=D. Hence each full finite Hamiltonian has norm at most 45/2+2(3/20)=114/5. Keep its scalar identity term in the exact polynomial; no separate phase approximation is then needed.

Let T_100(H_j)=sum_(k=0)^100 (-i H_j)^k/k!, and form the exact state

\[
 \widetilde\psi_3(2)=T_{100}(H_2)T_{100}(H_1)e_0.
\]

All generator matrix entries in the raw monomial coordinate representation are rational, with selfadjointness understood in the exact Haar Gram metric. The complex polynomial products can therefore be evaluated using Gaussian-rational arithmetic, without square-root orthonormalization or floating point. If that arithmetic and the declared input matrices/product order are independently checked, the delivered rational vector is exactly this polynomial vector. Define the rational number

\[
 b=\frac{(114/5)^{101}}{101!}.
\]

The unitary integral Taylor remainder and the product estimate prove

\[
 \boxed{\displaystyle
 \|\psi(2)-\widetilde\psi_3(2)\|
 \le\frac{27}{80000}+2b+b^2.}
 \tag{EX2}
\]

There is no time-freezing error because each target segment is exactly constant. The finite exponential approximation contributes 2b+b². Exact arithmetic removes the floating-roundoff term, conditional on the actual implementation and rational state artifact being verified. This is a complete mathematical error contract for this specific new fixture. It becomes a certified delivered numerical state only after the independent checker reconstructs its graph-derived matrices, rational coefficients, two ordered segments, polynomial order, state vector, norm bound and final rational inequality. No other trajectory inherits that validation automatically.

A signed companion with lambda1=+1/20 then -1/20 and lambda2=1/10 on both intervals has the same norm/action bounds, but belongs to the explicitly signed-driver extension. It can test the false signed-area shortcut. The nonnegative swap protocol above remains the primary physical-family fixture. Work at its jumps is a separate Stieltjes/jump-work calculation; (EX2) certifies the state without claiming a smooth-driver work identity across a jump.

## 9. Independent challenge of the volume comparison

The volume researcher proposes a finite connected simple open hypercubic spatial graph with E links and at least one square, no external charges, uniform electric coefficient alpha>0, and nonnegative finite magnetic coefficients lambda_p. Its physical electric gap is exactly 3alpha. In a gauge-invariant spin-network basis a nonempty support of nontrivial link representations cannot have a vertex with only one incident nontrivial representation: that would require a singlet inside a nontrivial irreducible representation. A finite graph with no degree-one support vertex contains a cycle. Open simple hypercubic graphs have no triangles or parallel-edge two-cycles, so at least four links are nontrivial, each with Casimir at least 3/4. A fundamental square loop attains total Casimir 3.

The full unconstrained product space has electric gap 3alpha/4 instead. Using 3 there would be a physical-sector error. Graphs with periodic short identifications, parallel edges, charged boundaries or no square require a changed argument.

The normalized one-link Casimir heat kernel at time 4 is between 3/4 and 5/4, as established in round 11. On E links, at physical time 4/alpha, the kernel ratio is at most (5/3)^E. The potential oscillation is 2*sum lambda_p. Feynman–Kac and the same ground-state variance comparison then yield

\[
 \Delta_E\ge3\alpha(3/5)^{2E}
 \exp[-16\textstyle\sum_p\lambda_p/\alpha].
 \tag{VOL1}
\]

I independently checked both factors: the ground-state ratio acquires exp[8 sum lambda_p/alpha], and the weighted variance comparison squares it. This is an explicit positive finite-volume bound whose constants deteriorate with volume. Its decay does not prove that the actual physical gap closes.

A precise method check is q independent copies of the exact two-square model. Their tensor-sum Hamiltonian has unique product ground state and exact gap equal to the one-copy gap, independent of q. Applying the earlier heat estimate to all q blocks instead gives

\[
 B_q=3\alpha(9/25)^{2q}
 \exp[-16q(\lambda_1+\lambda_2)/(3\alpha)]\longrightarrow0.
 \tag{VOL2}
\]

This rigorously demonstrates deterioration of the comparison method while the benchmark's true gap stays positive. The copies form a disconnected tensor benchmark. They do not establish a gap for a growing connected lattice, nor provide a counterexample to such a gap. The next useful volume bridge is control of fixed local observables at fixed physical time with constants depending on interaction range and boundary distance, followed by a separate stationary/continuum argument. Such a locality theorem remains a proposed experiment here.

The volume researcher's further conditional tests were also examined. For the one-square operator 4C+kappa(1-x), division of its action on exp(theta*x) by that function gives kappa-theta²+(3theta-kappa)x+theta²x². This cannot be constant unless theta=kappa=0. Thus a Wilson Gibbs density cannot simply be substituted for the true interacting quantum ground-state density.

An estimate on the actual ground state would be different: in the link Casimir metric SU(2) is a radius-two sphere with Ricci tensor g/2. If the actual positive ground state on every product graph satisfied Ric-2 Hess(log phi)>=c*g with a common c>0, its ground-state transform would have a Poincare bound c, hence a physical gap at least alpha*c. A sufficient uniform Hessian block-row norm is eta<1/4, yielding c=1/2-2eta. No such uniform estimate is supplied. It is a precise missing premise, not an accepted replacement of the quantum measure by a Gibbs ansatz.

The proposed limit rule likewise requires a real limiting theory. On a common Hilbert space, a uniform vacuum-complement bound, strongly convergent nonzero rank-one vacuum projections, and strong convergence to a strongly continuous semigroup with a nonnegative selfadjoint generator do preserve that lower gap. Merely taking strong limits at each t>0 does not construct such a generator: A_j=j(I-P) has limiting heat operators P for every t>0, which are discontinuous at zero on the full space. The volume report now explicitly includes this condition and counterexample. Finally, a common physical exponential rate on a dense family of centered vectors excludes lower spectral weight by positivity of their spectral measures; one measured observable or one fitted finite-time decay does not control the whole physical sector. These conditional bridges retain their unproved construction, uniformity and density premises.

## 10. Independent review of compact identities and scalar closure

The root's closure experiment uses a different, explicitly identified measure: a one-plaquette Euclidean tilted Haar density proportional to exp(kappa*x)sqrt(1-x²) on [-1,1]. Its kappa and moments must not be identified with the real-time two-square state or its Hamiltonian ground state. Differentiating (1-x²)^(3/2) exp(kappa*x) f(x) and integrating gives

\[
 \langle(1-x^2)f'\rangle
 =\langle[3x-\kappa(1-x^2)]f\rangle,
\]

\[
 n m_{n-1}-(n+3)m_{n+1}+\kappa(m_n-m_{n+2})=0.
 \tag{CL1}
\]

At n=0 the first term is zero; m0=1 is a separate normalization. For v=m2-m1², the first identity is 3m1=kappa(1-m1²-v). The variable v is an existing fluctuation observable. Naming it supplies neither an evolution equation nor a closure of higher moments.

Because dmu_kappa/dmu0>=exp(-2|kappa|), the minimum-over-constants characterization of variance gives

\[
 v\ge e^{-2|\kappa|}/4>0.
 \tag{CL2}
\]

This weighted comparison and the entire recurrence were independently checked. Setting m2=m1² while preserving the actual m1 leaves residual kappa*v in the first identity. At kappa=0 that identity is blind, while the next forces m2=1/4. Thus the explicitly defined point-concentration closure fails. This is not a claim that every scalar ansatz sets v=0.

The current source comparison is limited to the displayed conventions of Chatterjee–Frasca–Ghoshal–Groote, arXiv:2608.05415v1. Its introduction labels the continuum expansion formal; Sections IV–V omit the ghost sector and impose an extra closure assumption. Those sections do not prove the missing continuum construction. In the stated Hermitian-generator convention, direct trace calculations find a factor-two disagreement between the first and later action sums in Eq. 8, a factor-one-quarter staple derivative in Eq. 14, and a missing source factor i in Eq. 18. A periodic side-at-least-three fixture retains the derivative discrepancy. Eq. 29 also requires rank(eta^T g eta)=N²-1<=D, excluding full SU(3) color at D=4; this rank argument alone does not exclude SU(2). These are local formula/ansatz limitations, not a rejection of Haar invariance or every possible reduction. [Primary source, Sections II–V](https://arxiv.org/html/2608.05415v1).

The root initially encoded the formula-test constants directly. After review, its fixture calculates the relevant diagonal Gaussian-rational matrix traces and includes the periodic multiplicity check. That correction improves the executed algebraic test; numerical quadrature of tilted moments is still a diagnostic, not an interval proof. Independent reviewer artifacts must supply their own executed verdicts.

## 11. Current primary-source reading and novelty boundary

Ciavarella–Hariprakash–Halimeh–Bauer, arXiv:2508.00061v4, was checked at its 4 September 2026 revision and read in Sections 2.1–2.2, including the boundary/Dyson discussion. Those sections explicitly use leading-order perturbative estimates and small-parameter conditions in the displayed time-independent refinements. They motivate the boundary question but do not substitute for the nonperturbative proof (TAIL1)–(FACT1). Our bound grows with accumulated drive action and does not claim the source's time-independent refinement. [Primary truncation source](https://arxiv.org/html/2508.00061v4).

The full two-square operator and static theorem remain the already reviewed round-11 inputs, with their sources and hashes retained. This round claims an inspectable project derivation and an explicit verification contract, not mathematical novelty. The official four-dimensional Yang–Mills problem remains open. [Clay Mathematics Institute](https://www.claymath.org/millennium/yang-mills-the-maths-gap/). The source ledger records reading depth, versions, limitations and local artifact hashes.

## 12. Roadmap with concrete stop conditions

| Item | Status at this advisor handoff | Next obligation |
|---|---|---|
| Round-11 two-square graph, quotient, shared-link operator and domain | Completed and independently reviewed in its frozen history | Reuse exact source/parameter matches |
| Round-11 stationary cutoff certificates and coupling-square cover | Completed for their declared domain | Do not apply them to dynamics automatically |
| Round-11 driven numerical histories | Completed numerical diagnostics | Preserve their missing truncation claim |
| Round-12 exact driven representation bound | Proved FACT1; independently checked derivation | Replay action, support and degree gates in solver/verifier |
| Rigorous total error for a concrete computed trajectory | New exact-rational fixture has the complete analytic contract EX2 | Independently check its exact matrix/state artifact; ordinary floating cosine remains conditional |
| Round-12 finite-volume comparison | Derived and independently challenged VOL1 | Keep its E and plaquette dependence explicit |
| Volume-independent gap from this comparison | Rejected inference | A decaying lower estimate says nothing decisive about actual gap closure |
| Point-concentration moment closure | Rejected for the defined finite tilted-Haar benchmark | Retain variance and further moment/positivity constraints |
| General scalar reduction or a controlled continuum hierarchy | Unresolved | State its full assumptions, gauge/ghost content and error control |
| Four-dimensional construction, reconstruction, nontriviality and physical gap | Unresolved | No current inference rule produces these nodes |

Select three high-value next bridge experiments, rather than adding unrelated variables:

1. **Complete a total-error trajectory certificate on the present graph.** Use the exact action/degree theorem and a validated time solver or residual integral. Retain the old A=5 drive as a hard case and a declared smaller-action protocol as a discriminating fixture. Separately certify bounded observables and, at fixed alpha, work-derived energy. Stop when one useful protocol has a valid complete error budget and all known wrong-model mutations are rejected; an unvalidated floating trajectory remains labeled numerical.
2. **Test a local observable as a connected graph grows.** Fix its support, physical time, coefficients and initial preparation. Derive an interaction-picture locality estimate that handles unbounded on-link electric terms and bounded finite-range plaquette interactions; expose every dependence on distance and coordination. Then compare increasing open boxes. This could close a finite-time volume bridge, but does not itself produce a stationary mass gap or a continuum limit. Stop at one proved local estimate and one independently checked graph family.
3. **Replace a guessed scalar closure with a controlled finite moment hierarchy.** On the explicit compact Euclidean measure, impose normalization, support and positive moment-matrix conditions alongside more Haar identities; derive upper/lower intervals for a chosen moment or variance. Use the point-concentration failure and the source coefficient/rank tests as retained falsifiers. A future continuum claim additionally needs a common regulated measure, gauge/ghost completion when appropriate, uniform estimates and reconstruction. Stop once one finite-hierarchy enclosure is proved and replayed; do not equate adding a variable with closing its equation.

The machine-readable inventory and inference rules distinguish these analytic implications from external executable gates. Source hashes establish provenance, not truth. Removing a bandwidth, initial-support, unitary-evolution or action-integral premise blocks the factorial route. Removing validated numerical error premises blocks only a total-computed-error claim, while leaving the exact representation theorem intact. No rule allows finite trajectories, finite-volume positivity or a selected identity subset to imply the four-dimensional target.
