# Round 10 advisor: a certified interacting SU(2) loop

Contract: `ym10-one-square-v1`. Written 9 September 2026. This is a project derivation and source review, not a claim of a novel solution of the Yang–Mills Millennium Problem. Numerical acceptance is owned by the independent verifier, not this document.

The selected target adds a magnetic potential to the previous electric rotor and imposes the gauge constraints of an actual closed square. It has infinitely many representation states even though its spatial graph is finite. We can remove this representation truncation with explicit eigenvalue enclosures. We cannot infer an infinite-volume or four-dimensional continuum gap from that result.

## 1. Exact physical contract

Take an oriented cycle with four distinct vertices and four independent links. Each link carries an SU(2) matrix; its reversed orientation carries the inverse. The unconstrained Hilbert space is the product of four normalized Haar L² spaces. At vertex v the gauge transformation is U_e -> g_source U_e g_target^{-1}. The physical Hilbert space is the invariant subspace under independent transformations at all four vertices. There are no external color charges, matter fields, gravitational degrees of freedom, theta term, additional boundaries, or periodic link identifications.

Let C_e be the positive quadratic Casimir of a link, normalized so spin j has eigenvalue j(j+1), with fundamental generators sigma_a/2. Define K=sum_e C_e and V=1-ReTr(U_p)/2, where U_p is the oriented loop product. Units are hbar=1, and the Hamiltonian is

\[
H(\alpha,\lambda)=\alpha K+\lambda V,
\qquad \alpha>0,\quad 0\le\lambda<\infty. \tag{H1}
\]

Both alpha and lambda carry energy units. Time is already continuous. Coefficients are fixed during a spectral calculation. Gauge invariance follows because the loop product transforms by conjugation and each link Casimir is bi-invariant. V is a bounded multiplication operator with 0<=V<=2.

An optional normalization match to a standard Kogut–Susskind convention is

\[
\alpha=\frac{g^2}{2a},\qquad
\lambda=\frac{2}{g^2a},\qquad
\kappa=\frac\lambda\alpha=\frac4{g^4},\qquad
\alpha\lambda=\frac1{a^2}. \tag{H2}
\]

This follows by expanding Tr(2I-U_p-U_p^dagger)=4(1-ReTr U_p/2) in the Hamiltonian in Eq. (1) of Froland–Grabowska–Li. It is a declared convention, not a new relation deduced from the gap. Their work treats two plaquettes and is useful for the next coupled-graph step. [Primary source](https://arxiv.org/html/2512.22782v1).

## 2. Gauge reduction and three equivalent formulations

Gauge fixing the three links of a spanning tree leaves one loop U. The remaining gauge transformation conjugates U. Conversely, two square configurations with conjugate loop holonomy are gauge equivalent. Product Haar integration reduces to normalized Haar integration over U after the tree coordinates are integrated out. Consequently

\[
\mathcal H_{\mathrm{phys}}\simeq L^2(SU(2),dU)^{\mathrm{Ad}}.
\tag{R1}
\]

This is different from an open link gauged independently at both endpoints, whose invariant subspace contains only constants. A tensor product of independently conjugation-invariant plaquette wavefunctions is also insufficient for two adjacent plaquettes: the shared-link electric terms and simultaneous residual conjugation retain relative-orientation information.

Write the eigenvalues of U as exp(+-i theta), 0<=theta<=pi. The physical measure is (2/pi)sin²theta dtheta. The orthonormal basis is the SU(2) character

\[
\chi_{n/2}(\theta)=\frac{\sin((n+1)\theta)}{\sin\theta},
\qquad n=0,1,2,\ldots . \tag{R2}
\]

Every one of the four link Casimirs acts on the loop character with eigenvalue j(j+1), so K chi_(n/2)=n(n+2)chi_(n/2). The representation product identity chi_(1/2) chi_(n/2)=chi_((n+1)/2)+chi_((n-1)/2), with chi_(-1/2)=0, gives the exact Jacobi operator

\[
H_{nm}=[\alpha n(n+2)+\lambda]\delta_{nm}
-\frac\lambda2(\delta_{n,m+1}+\delta_{n,m-1}). \tag{R3}
\]

The missing n=-1 state is a physical boundary of the representation sequence. Adding it would change the model. The diagonal electric coefficient includes all four links; applying an additional factor of four after (R3) is an error.

The unitary map u(theta)=sqrt(2/pi) sin(theta) f(theta) converts the physical space to L²(0,pi). It takes (R3) to

\[
\widetilde H=-\alpha\frac{d^2}{d\theta^2}-\alpha
+\lambda(1-\cos\theta),
\quad D(\widetilde H)=H^2(0,\pi)\cap H^1_0(0,\pi). \tag{R4}
\]

The Dirichlet endpoints belong to u, not directly to f. A constant physical wavefunction f is the sine ground state u proportional to sin(theta). Omitting the Haar factor or imposing Dirichlet conditions on f gives another spectrum.

For an independent exact special-function representation set z=theta/2. The differential equation becomes Mathieu's equation with q=-2lambda/alpha. Dirichlet conditions at z=0 and z=pi/2 select even-order odd Mathieu functions. In terms of their characteristic values b_m(q),

\[
E_k=\lambda-\alpha+\frac\alpha4
b_{2k+2}(-2\lambda/\alpha),\qquad k=0,1,\ldots . \tag{R5}
\]

The one-square reduction and its Mathieu solution are established in Bauer et al., Sec. IV and Appendix B; the formulas above were independently reduced before matching conventions. Floating-point evaluation of b_m is an independent numerical comparison, not a rigorous interval certificate. [Primary source](https://arxiv.org/pdf/2307.11829).

## 3. Finite-graph theorem without representation truncation

**Theorem G.** For every fixed alpha>0 and finite lambda>=0, (H1) has a selfadjoint realization on D(K), compact resolvent, a unique ground state, and strictly positive first excitation gap Delta=E_1-E_0. E_0>=0, and E_0>0 when lambda>0.

**Proof.** In the character basis K is the diagonal selfadjoint operator with eigenvalues n(n+2) on its natural domain. Its resolvent is compact because the diagonal resolvent coefficients tend to zero. Multiplication by lambda V is bounded and symmetric; the bounded perturbation preserves selfadjointness on D(K). The resolvent identity preserves compactness. Thus H has a sequence of finite-multiplicity eigenvalues tending to infinity. Nonnegativity follows from K>=0 and V>=0.

To establish simplicity, use (R4). Two solutions of the regular second-order differential equation at the same energy that obey u(0)=0 are proportional: their initial derivatives determine them uniquely. Therefore the Dirichlet eigenspaces have dimension one. Selfadjointness identifies geometric and spectral multiplicities. In particular E_0<E_1. For strict E_0 positivity when lambda>0, an eigenstate with zero energy would have both K and V expectations zero. The first forces f to be constant, whereas that state has positive V expectation. This is impossible. QED.

This proves an infinite-dimensional quantum result on a finite spatial graph. Compactness of the graph configuration space is precisely part of the proof; it cannot be silently carried into the infinite-volume field-theory limit. The same compactness argument supplies no quantitative uniform gap as graph size increases.

## 4. Rigorous removal of the character cutoff

N always denotes retained basis dimension. Retained indices are n=0,...,N-1; the first omitted index is n=N. For the first two eigenvalues require N>=2. Let P_N project onto these states and A_N=P_NHP_N. Define

\[
\tau=\alpha N(N+2),\qquad c=\lambda/2. \tag{T1}
\]

On the tail Q=1-P_N, its compressed Hamiltonian T satisfies T>=tau I. This bound uses compression of the nonnegative magnetic operator; bounding only its positive diagonal and forgetting its offdiagonal terms would incorrectly yield tau+lambda. The P-Q coupling is the single link -c|N-1><N| plus its adjoint.

Choose a rational R satisfying

\[
\mu_1(A_N)<R<\tau,\qquad
\eta=\frac{c^2}{\tau-R},\qquad
B_N=A_N-\eta|N-1\rangle\langle N-1|. \tag{T2}
\]

For x in P_N and y in Q, Young's inequality gives

\[
-2c\operatorname{Re}(\overline{x_{N-1}}y_N)
\ge-\eta|x_{N-1}|^2-\frac{c^2}{\eta}\|y\|^2.
\]

Together with T>=tau this proves the quadratic-form bound H>=B_N direct_sum R I. For lambda=0, no Young division is needed because the coupling vanishes and H is diagonal. Since mu_1(B_N)<=mu_1(A_N)<R, the first two min–max levels of the comparison operator are exactly those of B_N. The Rayleigh–Ritz upper bound uses the retained subspace. Therefore

\[
\mu_k(B_N)\le E_k(H)\le\mu_k(A_N),\qquad k=0,1. \tag{T3}
\]

Exact rational finite-matrix enclosures l_k^B<=mu_k(B_N)<=u_k^B and l_k^A<=mu_k(A_N)<=u_k^A imply

\[
l_1^B-u_0^A\le\Delta\le u_1^A-l_0^B. \tag{T4}
\]

The lower endpoint must be tested for positivity. A negative lower endpoint means this certificate is inconclusive; it does not contradict Theorem G. The choice R must use a certified upper bound for mu_1(A_N), and must be rejected if R>=tau. An ordinary floating-point eigenvalue is not a valid decisive premise.

The bound can be sharpened through the energy-dependent Schur complement. For rational x<tau,

\[
A_N-xI-\frac{c^2}{\tau-x}P_{N-1}
\ \le\ A_N-xI-c^2\langle N|(T-xI)^{-1}|N\rangle P_{N-1}
\ \le\ A_N-xI. \tag{T5}
\]

The number of eigenvalues of H below x equals the negative inertia of the middle matrix because T-xI is strictly positive. This is a possible next refinement; it is not needed when the simpler shared-R enclosure already answers the declared precision question.

These are nonperturbative form inequalities. The recent truncation literature motivates boundary amplitudes and rapidly decreasing tails, but leading-order truncation estimates do not replace (T3). Ciavarella's Sec. 2.1 explicitly introduces perturbation theory for a single-mode example; later sections study dynamics and larger systems. [Primary source](https://arxiv.org/html/2508.00061v4).

## 5. Exact-arithmetic certificate requirements

For rational alpha, lambda, R, A_N and B_N have rational entries. Finite eigenvalue brackets can be certified through Sturm inertia using exact rational characteristic-polynomial recurrences or an equivalent exact LDL decomposition. The implementation must define how zero pivots, exact endpoint eigenvalues and lambda=0 are handled. A zero is not replaceable by a machine epsilon when the result is called exact.

For a Jacobi matrix with nonzero offdiagonal c, the characteristic recurrence is p_0=1, p_1=d_0-x and p_(r+1)=(d_r-x)p_r-c²p_(r-1). At a non-eigenvalue x, the number of sign changes, with internal zero entries handled by the Sturm convention, is the number of eigenvalues below x. Endpoints that are exact roots need an explicit strict/non-strict convention. The diagonal c=0 case should directly count diagonal entries.

The checker should reconstruct rational matrices from the mathematical input contract, validate every bracket's index, recheck R<tau, recompute eta and the gap subtraction, and verify the complete list of declared cases. Decimal display values are only rendered approximations to exact rational endpoints. A mismatch in units or matrix factors invalidates the certificate even when its integer arithmetic is flawless.

## 6. Continuous variables with exact consequences

Rescale H=alpha h(kappa), kappa=lambda/alpha. The dimensionless gap delta(kappa) obeys Delta=alpha delta(kappa). Write h(kappa)=D+kappa I-kappa X, where X is multiplication by cos(theta) and ||X||=1. The common kappa I does not affect gaps. Min–max eigenvalue stability under bounded perturbations gives

\[
|\delta(\kappa)-\delta(\kappa_0)|
\le2|\kappa-\kappa_0|. \tag{C1}
\]

Thus a certified pointwise bound delta(kappa_i)>=b_i proves delta(kappa)>=b_i-2r_i throughout |kappa-kappa_i|<=r_i. A finite collection of intervals whose union covers a declared compact range and whose lower margins are all positive proves a gap uniformly on that entire range. Point samples alone do not. The exact interval endpoints, coverage and margins must all be replayed.

For alpha>=alpha_min>0 and kappa in such a certified domain, Delta>=alpha_min times the certified common dimensionless lower bound. Qualitatively, continuity and Theorem G also ensure a positive minimum on every compact kappa domain. That compactness argument gives existence, not a useful numerical constant.

Several analytic controls follow directly:

\[
\Delta(\alpha,0)=3\alpha,\qquad
\Delta(\alpha,\lambda)\ge3\alpha-\lambda. \tag{C2}
\]

The second bound uses H>=alpha K, hence E_1>=3alpha, and the constant-class trial state E_0<=lambda. It is useful when lambda<3alpha. In the parity operator P|n>=(-1)^n|n>, PXP=-X. The gap is therefore even under lambda->-lambda when the operator is extended to finite negative lambda. Near kappa=0, ordinary isolated-eigenvalue perturbation theory gives

\[
e_0=\kappa-\kappa^2/12+O(\kappa^4),\quad
e_1=3+\kappa+\kappa^2/30+O(\kappa^4),\quad
\delta=3+7\kappa^2/60+O(\kappa^4). \tag{C3}
\]

These expansion checks do not give a rigorous remainder bound over arbitrary kappa. A plausible further hypothesis is delta(kappa)>=3, or monotonicity for kappa>=0. Neither assertion is admitted by the current proof. A finite certified interval does not prove an all-kappa statement.

## 7. A rigorous failure of unconstrained parameter tuning

For fixed lambda>0 let alpha decrease to zero. For 0<w<=pi, take the two-dimensional trial space spanned by sin(pi theta/w) and sin(2pi theta/w), supported on [0,w] and extended by zero. These are admissible quadratic-form states. The maximum kinetic expectation is bounded by 4pi²alpha/w²-alpha, while 1-cos(theta)<=theta²/2 gives the potential bound lambda w²/2. Consequently

\[
0<\Delta\le E_1
\le\frac{4\pi^2\alpha}{w^2}+\frac{\lambda w^2}{2}-\alpha.
\]

Choosing w⁴=8pi²alpha/lambda, when alpha/lambda<=pi²/8, yields

\[
\Delta\le2\sqrt2\,\pi\sqrt{\alpha\lambda}-\alpha
\longrightarrow0. \tag{F1}
\]

At alpha=0, H is multiplication by lambda(1-cos(theta)). For lambda>0 its spectrum is the interval [0,2lambda]; the zero-energy point has no normalizable eigenvector. For alpha=lambda=0 every state has zero energy and the unique-vacuum premise also fails. Therefore positivity at every alpha>0 is not uniform as alpha approaches zero. The matched Kogut–Susskind path alpha lambda=1/a² is a different path and cannot use this counterexample as its continuum conclusion.

## 8. Variable taxonomy and rejected shortcuts

| Quantity | Role | Valid change | Obligation |
|---|---|---|---|
| alpha | Constant electric energy coefficient | Compare exact Hamiltonians with alpha>0 | Preserve units; gap scales with alpha |
| lambda | Constant magnetic energy coefficient | Continuous parameter scan | Keep full potential and cutoff bound |
| kappa=lambda/alpha | Dimensionless ratio | Certified interval coverage | Use (C1), exact coverage and positive margins |
| N or j_max=(N-1)/2 | Representation regulator | Increase N | Certify omitted infinite tail; N is not a new field |
| a | Spatial lattice spacing | Change graph-scale matching | Fix physical observables and increase graph extent appropriately |
| g(a) | Bare matched coupling | Follow a specified renormalization trajectory | Cannot fit g merely to enforce a desired gap |
| alpha(t), lambda(t) | Prescribed drivers | Time-dependent Hamiltonian | Include work alpha'(t)<K>+lambda'(t)<V> and state/domain regularity sufficient for evolution and finite <K> |
| Extra scalar, mass or coupling field | New physical theory | Specify action, state, gauge transformation and dynamics | Establish a controlled decoupling limit to pure Yang–Mills |

A gauge-boson mass inserted by hand changes the local gauge contract. A gauge-invariant scalar completion changes the field content. Neither fills an unproved premise of the original pure Yang–Mills problem. Connecting this branch to Einstein–QED would require a separately specified Einstein–Yang–Mills–matter theory and its stress/conservation identities; the old U(1) scalar result does not supply SU(2) gauge constraints or a four-dimensional quantum construction.

## 9. Theory map and selected bidirectional route

| Node | Status in this contract | Immediate predecessors | Next obligation |
|---|---|---|---|
| SU(2) Lie algebra and normalized Haar measure | Declared mathematical setting | Compact group | Gauge action |
| Product link Hilbert space | Defined | Four-link graph, Haar measure | Gauss invariant sector |
| Casimir normalization | Declared and independently checkable | sigma/2 generators | Four-link kinetic factor |
| Gauss constraint | Imposed | Independent vertex gauge group | Tree gauge reduction |
| One-loop conjugation quotient | Derived | Gauge orbit classification | Character completeness |
| Peter–Weyl class characters | Established input | Compact representation theory | Exact Jacobi operator |
| Magnetic character product | Derived identity | SU(2) Clebsch–Gordan rule | Nearest-neighbor representation coupling |
| Radial Dirichlet formulation | Derived | Haar unitary map | Independent equation oracle |
| Selfadjoint compact resolvent | Proved G | Positive alpha, bounded V | Discrete spectrum |
| Unique finite-graph vacuum | Proved G | Regular radial ODE | Positive pointwise gap |
| Infinite-tail threshold | Proved T1 | Positive magnetic compression | Finite lower comparison |
| Rank-one lower block | Proved T2–T3 | Tail threshold, strict R range | Eigenvalue enclosure |
| Rational Sturm inertia | Exact finite algebra method | Rational matrix and zero policy | Brackets with index certificates |
| Infinite-space gap interval | Proved conditional T4 | Four verified brackets | Positive certified margin |
| Continuous kappa stability | Proved C1 | Bounded multiplication perturbation | Whole-range coverage |
| Uniform compact-domain gap | Proved when coverage passes | C1 and positive margins | More plaquettes |
| Two-square physical Hilbert space | Next explicit target | Seven links, six vertices, Gauss law | Coupled loops and intertwiners |
| Two-square truncation theorem | Unproved here | Correct coupled Hamiltonian | Tail bound including cross terms |
| Graph-volume uniform bounds | Open dependency | Increasing connected graphs | Infinite spatial volume |
| Bare-coupling/spacing matching | Open dependency | Common physical scale, RG control | Continuum trajectory |
| Nontrivial continuum correlations | Open dependency | Tightness and renormalization | Axiom/reconstruction checks |
| Positive physical gap uniform in limits | Open dependency | Common state family and scale | Spectral reconstruction |
| Four-dimensional pure Yang–Mills construction | Unresolved Millennium target | All continuum axioms and nontriviality | Full mass-gap conclusion |
| Einstein–Yang–Mills–matter coupling | Separate theory | Action-derived common stress/current | Gravity constraints and quantum closure |

**Forward frontier.** Start with the graph, group, normalization and positive-alpha contract. Derive gauge reduction, characters, the Jacobi operator and tail threshold. Separately prove selfadjointness and the finite-graph spectral meaning. Execute rational brackets and obtain pointwise infinite-space gap bounds.

**Backward frontier.** A positive bound for all kappa in a chosen range needs a finite interval cover with positive local margins. Each local margin needs a certified pointwise gap and the Lipschitz theorem. Each pointwise gap needs the correct first two infinite-space eigenvalue brackets. Those require a strict tail threshold, a valid R and correctly indexed exact finite-matrix brackets.

**Meeting.** The frontiers meet at the independently replayed bracket-and-tail certificate plus the proved continuity constant. A Horn/A* planner may locate and replay these obligations. It does not prove the gauge reduction, Young inequality, spectral theorem or certificate implementation. Those arguments remain inspectable in this document and the verifier's independent review.

**Negative controls.** Withdraw gauge projection: no route to the physical-loop claim. Withdraw tail positivity or its strict R bound: no finite-to-infinite eigenvalue route. Withdraw the interval cover: only pointwise results remain. Add the continuum target: it stays underivable because volume, scale, reconstruction and nontriviality nodes have no admitted proofs. Changing an unknown node into an assumed fact is not progress.

## 10. Ranked next experiments and stop criteria

1. **Selected now — character-tail certification and continuous-range coverage.** Compare exact rational brackets to independent radial/Mathieu values at zero, small, intermediate and large kappa. Predeclare the bracket-width gate. Test offdiagonal and four-link factor mutations, invalid tail thresholds, zero coupling, exact-eigenvalue endpoints, incomplete case collections and interval-cover gaps. Stop after required cases and held-out defects are resolved.
2. **Next — two adjacent squares.** Use the seven-link Kogut–Susskind Hamiltonian, impose all six vertex Gauss constraints, derive the shared-link electric cross terms in a gauge-reduced basis, and independently check against the unreduced constrained construction. This removes the separable one-loop assumption. Do not use a tensor product of two independent rotor spectra as the interacting answer.
3. **Later — volume and physical scale.** Repeat a common observable and operator-bound contract on growing graphs with coupling and scale matching. Explicitly track which constants grow with volume. A few positive finite-size gaps or successful numerical extrapolations remain evidence, not uniform continuum proof.

The official Clay page still identifies the Yang–Mills problem as unsolved; nothing in this finite-graph contract supplies the missing four-dimensional construction. [Official problem status](https://www.claymath.org/millennium/yang-mills-the-maths-gap/).

## 11. Source and novelty boundary

This is targeted reading. The original 1975 Kogut–Susskind article's abstract and metadata were inspected; full text required authorization. It supplies historical provenance for canonical lattice gauge theory, not unchecked equation-level authority here. [Original article](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.11.395).

The one-plaquette solution is already in the literature. Our added work is the explicit independently checked finite-to-infinite error contract, its exact-arithmetic implementation, the continuous-parameter coverage certificate, and retained falsifiers. These are useful project advances without a claim of mathematical novelty or a proof of the prize problem.

## 12. Independent mathematical review

The separately assigned skeptic reviewed R1–R5, Theorem G, T1–T5, C1–C3 and F1 on 9 September 2026 and reported no mathematical objection. The reviewer independently checked the Lipschitz factor, the localized two-state trial bound and the perturbative coefficients. This is an agent mathematical review, not credentialed human peer review or proof-kernel verification. The reviewer also required explicit state/domain regularity before extending the time-dependent work identity to the untruncated operator; that condition is now stated in the variable taxonomy. Numerical and code verdicts belong to the separate executed audit.
