# Yang–Mills prize target: advisor dossier

Checked 9 September 2026. This is a bounded source check and proposed research design, not an exhaustive literature review. Prior project achievements are known here from the supplied conversation transcript, not a fresh examination of their code.

## Official target and status

Clay currently labels Yang–Mills existence and mass gap **Unsolved**. It allocates $1 million to each Millennium Prize Problem. [Official status](https://www.claymath.org/millennium/yang-mills-the-maths-gap/), [prize allocation](https://www.claymath.org/millennium-problems/).

The target is a nontrivial four-dimensional quantum theory of pure Yang–Mills for **every compact simple gauge group**. A construction must meet rigorous quantum-field axioms, and its physical Hamiltonian must have vacuum energy zero with

\[
\operatorname{spec}(H)\cap(0,\Delta)=\varnothing,\qquad \Delta>0,
\]

with a finite nonzero excitation scale. The official formulation also asks that gauge-invariant local observables have the expected short-distance Yang–Mills behavior. Confinement, matter-field extensions, and general curved manifolds are additional questions rather than replacements for this target. [Jaffe–Witten official formulation, §§4–5](https://www.claymath.org/wp-content/uploads/2022/06/yangmills.pdf).

Euclidean conventions useful for a new branch are \(A=A_\mu^aT^a dx^\mu\), \(F=dA+A\wedge A\), and

\[
S_E=\frac1{4g^2}\int_{\mathbb R^4}F^a_{\mu\nu}F^a_{\mu\nu}\,d^4x.
\]

Here the positive invariant Lie-algebra quadratic form and generator normalization must be declared. Writing this action is a definition of the intended formal model, not a quantum construction. A Euclidean approach must establish the hypotheses of reconstruction, including reflection positivity; positivity of an ordinary energy coefficient is a different property. [Osterwalder–Schrader, original reconstruction paper](https://doi.org/10.1007/BF01645738).

## What the existing project can and cannot transfer

The following judgments are our logical comparison of the official target with the user's supplied project descriptions.

| Existing work | Transferable method or obligation | Unsupported conclusion |
|---|---|---|
| Finite Maxwell–Dirac existence theorem | Norm preservation, coercive bounds, explicit continuation assumptions, independent proof replay | Finite ODE existence constructs a local continuum quantum field theory |
| Positive effective Maxwell coefficient | A useful regulator-specific nondegeneracy condition | This coefficient is a Hamiltonian mass gap or reflection positivity |
| Tangent source response | Linearization, causal support and independent finite-difference checks | One driven response determines all quantum correlation functions or their spectral support |
| Joint momentum/Landau-cutoff obstruction | Need regulator-uniform bounds and declared limit order | A truncation coefficient divergence establishes a physical Landau pole theorem |
| Scalar extension | Action-derived energy exchange and decoupling checks | An inserted scalar mass proves a dynamically generated gap of pure Yang–Mills |
| Einstein constraint identity | Conserved stress is necessary for consistent backreaction | Gravity closure supplies the flat-space nonabelian construction |

U(1) QED is abelian: its curvature has no commutator self-interaction. The pure nonabelian theory is a separate branch. In particular, changing U(1) into SU(2) is a change of theory, requiring a new action, state space, gauge constraints, and verifier.

## Primary research baselines

1. **Strong-coupling lattice theorem.** Shen–Zhu–Zhu establish infinite-volume lattice results, functional inequalities and exponential correlation decay in explicit strong-coupling ranges. For SU(N), their assumption is \(|\beta|<1/[16(d-1)]\), with their \(\beta N\) action normalization. This does not establish the four-dimensional weak-coupling continuum limit. [Original preprint, later CMP 2023](https://arxiv.org/abs/2204.12737). Reading depth: primary abstract and authors' institutional account; full proof not independently audited in this turn.
2. **Numerical spectrum.** Athenodorou–Teper compute SU(N) glueball spectra and other quantities with the Wilson plaquette action, then extrapolate to the continuum and large N. This is an appropriate numerical reference, with finite-spacing, volume and topology questions to reproduce; it is not a constructive proof. [Original paper](https://arxiv.org/abs/2106.00364). Reading depth: primary abstract; tables not independently re-fitted in this turn.
3. **Different ultraviolet running.** Gross–Wilczek demonstrate asymptotic freedom in nonabelian gauge theories. QED's short-distance renormalization problem has a different sign structure; a QED subtraction prescription does not transfer this nonabelian mechanism. [Gross–Wilczek original paper](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.30.1343), [Gell-Mann–Low original QED paper](https://journals.aps.org/pr/abstract/10.1103/PhysRev.95.1300). Reading depth: primary abstracts; no claim of full-paper audit.

Search results also returned self-published 2026 claims of full solutions. Those claims were not audited and are not accepted evidence; Clay's current official status remains the status source. Do not convert a search result's advertised theorem or AI checker counts into verified mathematics.

## Bidirectional obligations

This is our proposed dependency graph, not a claimed proof and not a claim that a search algorithm can discover unknown analytic estimates automatically.

**Forward frontier**

F1. Specify a compact-simple group, local regulator, gauge-invariant observable algebra and physical units.

F2. Construct the finite-regulator probability measure or physical Hamiltonian, without conflating gauge-fixing ghosts with physical states.

F3. Prove regulator-level symmetry and positivity properties; derive quantitative bounds.

F4. Find bounds that remain controlled along a renormalized continuum trajectory and as physical volume grows. Track the lattice spacing \(a\), physical box length \(L\), and coupling \(g(a)\) separately.

**Backward frontier**

B1. A physical gap needs exclusion of low-energy spectrum throughout the reconstructed physical Hilbert space, not only one operator channel.

B2. A transfer-matrix strategy needs \(\Delta_{a,L}=-a_t^{-1}\log[\lambda_1(T_{a,L})/\lambda_0(T_{a,L})]\) in physical units, with a limit theorem preserving a positive lower bound. \(\lambda_1\) here denotes the top of the nonvacuum spectral sector when it need not be an isolated eigenvalue.

B3. Reconstruction needs limiting local correlation functions with the relevant regularity, covariance, locality, positivity and vacuum properties; a positive numerical Hankel matrix on selected times checks only finitely many necessary inequalities.

B4. The limiting theory must be nontrivial and have the required Yang–Mills short-distance structure. A limit containing only the vacuum does not satisfy the prize problem.

**Meeting obligation:** regulator removal + physical scale control + positivity/reconstruction + spectrum control. Every AND premise needs an explicit certificate; failure to derive an obligation means open, not false. Strong coupling at fixed lattice spacing and the weak-coupling continuum path are separate nodes.

## A precise conditional bridge that is provable now

This is a standard functional-calculus argument reproduced here, not a new Yang–Mills theorem.

Assume nonnegative self-adjoint \(H_n\) and \(H\) are already realized on a common Hilbert space, \(H_n\to H\) in the strong-resolvent sense, and one fixed \(\delta>0\) satisfies \(\operatorname{spec}(H_n)\cap(0,\delta)=\varnothing\) for every n. Then \(\operatorname{spec}(H)\cap(0,\delta)=\varnothing\).

Proof: for any continuous compactly supported \(f\) inside \((0,\delta)\), functional calculus gives \(f(H_n)=0\). Strong-resolvent convergence gives \(f(H_n)\to f(H)\) strongly, so \(f(H)=0\). Since this holds for every such f, the interval has no spectral support. Vacuum existence/uniqueness and nontriviality require additional premises. A sequence of lattice Hilbert spaces does not automatically provide the assumed common realization or convergence.

Positive finite gaps alone do not suffice. On \(\ell^2(\{0,1,2,\dots\})\), let

\[
H_ne_0=0,\quad H_ne_k=\max(1/n,1/k)e_k\ (k\ge1).
\]

Each \(H_n\) has gap \(1/n\). The operators converge in norm to \(He_0=0,\ He_k=k^{-1}e_k\), but H has positive spectrum accumulating at zero. This directly defeats the implication “every regulated model is gapped, therefore the limit is gapped.”

## Three tractable falsifiable experiments

These are proposed tests, not results run by this advisor. They test failure modes needed by future physics work; none is a Yang–Mills mass-gap measurement.

### E1. Detect a finite-box gap that vanishes

Use the free massless scalar with Dirichlet boundaries on a cubic box. With N interior sites per axis and spacing \(a=L/(N+1)\), the exact lowest oscillator frequency is

\[
\omega_{\min}(N,L)=\frac{2\sqrt3}{a}\sin\frac{\pi}{2(N+1)}.
\]

Compare a sparse Dirichlet-Laplacian eigenvalue calculation with this formula. At fixed L, refine N and check convergence to \(\sqrt3\pi/L\); then increase L and check the gap vanishes. Include a massive control \(\sqrt{m^2+\omega_{\min}^2}\to m\). Pass only if the code distinguishes discretization convergence from the infinite-volume limit. Avoid periodic zero-mode removal: it would silently change the observable sector.

### E2. Break a false mass plateau using an exact spectral mixture

Set \(C(t)=e^{-t}+10^{-8}e^{-0.05t}\). Both weights are positive. Compare local effective mass \(m_{\rm eff}(t;h)=h^{-1}\log[C(t)/C(t+h)]\) across short and long windows. A short window mimics mass 1 although the slowest visible energy is 0.05; equal contributions occur at \(t=\log(10^8)/0.95\). Derive from the positive spectral representation that \(-d\log C/dt\) is a weighted mean of energies, and its derivative is minus their variance. Therefore an apparent plateau approaches the lowest overlapping energy from above and does not certify a lower bound on all physical energies.

Use log-sum-exp to avoid underflow. Check positive-semidefiniteness of \(K_{ij}=C(t_i+t_j)\), and a negative-weight mutation as a deliberate violation. A finite matrix pass is a diagnostic, not a proof of all reflection-positivity inequalities. Add a hidden orthogonal channel to demonstrate that even an exact one-channel spectrum need not be the theory's lightest sector.

### E3. Audit the renormalization sign and units

In \(t=\log(\mu/\mu_0)\), integrate the *one-loop model equations*

\[
\frac{de}{dt}=\frac{e^3}{12\pi^2},\qquad
\frac{dg}{dt}=-\frac{11C_Ag^3}{48\pi^2}.
\]

Compare with \(e^{-2}(t)=e_0^{-2}-t/(6\pi^2)\) and \(g^{-2}(t)=g_0^{-2}+11C_At/(24\pi^2)\). Choose small initial couplings and stop interpretation before perturbation theory fails. Check that switching from \(\log\mu\) to \(\log\mu^2\) changes derivatives by 1/2; this catches the common factor-of-two convention error. The formal QED pole \(t_*=6\pi^2/e_0^2\) is an extrapolation of this model, not an all-orders physical prediction or a proof of triviality. A good fit of one coefficient after subtraction must not be reported as a continuum completion.

## Acceptance decisions for the main project

- Add a separate Yang–Mills prize page and maintain the Einstein–QED branch as a different open project.
- Prefer the first two exact-control experiments before expensive nonabelian simulations; they test the most dangerous false proof patterns cheaply.
- A next true nonabelian benchmark should first reproduce a declared SU(2) finite-lattice action, gauge transformation invariance, plaquette identities and autocorrelation-aware sampling. Spectral claims then need channel coverage, volume and spacing studies, and error budgets.
- Classify assertions as source fact, reproduced theorem under assumptions, numerical evidence, conjecture, rejected inference, or uncomputed. Never infer a proof from the number of passing unit tests.

