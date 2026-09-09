# Yang–Mills round 9: advisor derivations and next proof obligations

**Disposition, 9 September 2026.** Build and verify the finite four-dimensional pure SU(2) Wilson theory, and prove exactly what its Schwinger–Dyson identities characterize. The results below are elementary conditional or finite-regulator theorems rederived for this project; no novelty claim is made. They do not construct continuum Yang–Mills. The current official [Clay problem page](https://www.claymath.org/millennium/yang-mills-the-maths-gap/) continues to list the problem as open.

The assigned advisor read the prior `research/round8/spectral-proof.md`, the local `qeg-research-advisor` skill and its pipeline. Review covered the equations and inferences below. It did not audit the new lattice implementation, rerun earlier QED simulations, or read every proof in the cited papers. Root and independent implementer/verifier roles own those tasks.

## 1. Fixed physical and mathematical contract

- Gauge group SU(2); four Euclidean lattice directions; finitely many link variables.
- Normalized product Haar measure, no gauge fixing, no matter or added scalar, no gravity.
- Wilson action, counting each elementary unoriented plaquette once:

\[
S_W(U)=\beta_W\sum_p[1-\tfrac12\operatorname{ReTr}U_p],\qquad
d\mu_W=Z_W^{-1}e^{-S_W}dH.
\]

- Positive physical coupling \(\beta_W=4/g_0^2\). Algebraic identities remain valid for finite real beta, but reflection-positivity claims here are restricted to the usual positive-coupling Wilson model.
- Left derivative on a link: \(L_aF(U)=\left.\partial_tF(e^{it\sigma_a/2}U)\right|_{t=0}\).
- Periodic directions must have lengths at least two for the usual independent-link staple formula. More generally, require that every plaquette containing the varied independent link contains it exactly once. A length-one periodic direction violates that premise and requires repeated-link derivatives.
- Results concern dimensionless lattice variables. Lattice spacing, temporal extent, spatial volume, bare coupling and operator renormalization are different controls.

This changes the previous physical contract. The Maxwell–Dirac energy identities are useful verification experience, but they provide no theorem about the nonabelian Wilson measure. The QED Landau pole, a finite Landau-level cutoff, and Landau gauge are different concepts.

## 2. Exact finite-lattice Haar identity and its local SU(2) form

For every smooth insertion f and each link/color derivative, Haar invariance gives

\[
0=\int L_a(fe^{-S_W})\,dH
\quad\Longrightarrow\quad
\boxed{\langle L_af-fL_aS_W\rangle_W=0.}\tag{H1}
\]

Compactness makes the integral finite and removes boundary terms; no perturbation expansion or flat gauge-potential measure is used. The sign follows from differentiating \(e^{-S_W}\), not from a convention remembered from a paper that uses \(e^{+S}\).

Condition on every other link. With a correctly oriented, **unnormalized** staple sum A independent of U, write

\[
S_W=C-\tfrac{\beta_W}{2}\operatorname{ReTr}(UA)=C-\beta_Wa_0,
\qquad UA=a_0I+i\boldsymbol a\cdot\boldsymbol\sigma.
\]

The sum A is quaternionic but need not be an SU(2) matrix. In particular \(a_0^2+|\boldsymbol a|^2\) is not generally one. For an interior link in four dimensions A has six staple terms.

Multiplication by \(e^{it\sigma_a/2}\) gives \(L_aa_0=-a_a/2\), \(L_a^2a_0=-a_0/4\), so

\[
L_aS_W=\frac{\beta_Wa_a}{2},\qquad
L_a^2S_W=\frac{\beta_Wa_0}{4}.
\]

Choosing \(f=L_aS_W\) in (H1), then summing over a, yields

\[
\sum_a\langle(L_aS_W)^2-L_a^2S_W\rangle_W
=\frac14\langle\beta_W^2|\boldsymbol a|^2-3\beta_Wa_0\rangle_W=0.\tag{H2}
\]

The residual \(\beta_W^2|\boldsymbol a|^2-3\beta_Wa_0\) is **four times** the summed derivative expression. Their zeros coincide; their numerical residual magnitudes differ. At an all-identity four-dimensional configuration it equals \(-18\beta_W\) per link. At beta zero it vanishes for every configuration and cannot diagnose a sampler.

**Acceptance uses.** Compare the local action increment with a complete plaquette-action recomputation, compare derivatives with matrix perturbations, then check (H2) in ensembles with autocorrelation-aware uncertainty. An ensemble average consistent with zero supports one necessary identity. It does not establish exact stationarity, independence, or a mass gap.

## 3. Partial theorem: the complete identity hierarchy characterizes finite Gibbs law

**Theorem H3.** Let \(M=G^E\) for finite E and connected compact Lie group G, with normalized product Haar measure H. Let \(S\in C^\infty(M;\mathbb R)\). Let the link derivatives \(L_i\) range over a basis of the Lie algebra on every independent link. A Borel probability measure \(\nu\) is \(Z^{-1}e^{-S}H\) if and only if

\[
\int_M(L_if-fL_iS)\,d\nu=0
\quad\text{for every }f\in C^\infty(M)\text{ and every }i.\tag{H3a}
\]

No absolute-continuity assumption on nu is needed.

**Proof.** Gibbs law implies the identities by (H1). Conversely define the finite nonzero measure \(d\eta=e^Sd\nu\); S is bounded on the compact manifold. Insert \(f=e^S\phi\), with arbitrary smooth phi, into (H3a). The two S-derivative terms cancel, leaving

\[
\int_ML_i\phi\,d\eta=0.\tag{H3b}
\]

For the left flow \(\Phi_i^t\), the smooth bounded function
\(F_i(t)=\int\phi(\Phi_i^tU)d\eta(U)\) has derivative
\(F_i'(t)=\int L_i[\phi\circ\Phi_i^t](U)d\eta(U)=0\).
Thus eta is invariant under each one-parameter generator. These flows generate each connected factor G, hence their products generate all left translations on M. Smooth test functions are dense in continuous functions on compact M, so invariance extends to continuous tests and therefore to the measure. Uniqueness of normalized Haar measure gives \(\eta=cH\). Therefore \(\nu=ce^{-S}H\), and probability normalization fixes \(c=Z^{-1}\). This proves both directions.

**What this removes.** The finite-theory hierarchy has no additional probability-law ambiguity if all its test functions and generators are known exactly.

**What remains.** A finite implementation checks finitely many insertions with finite precision. The theorem neither closes a truncated hierarchy nor constructs its continuum limit. Compactness and connectedness are substantive premises: disconnected components would require additional information to fix their relative weights.

## 4. Exact negative control: one Ward residual accepts a wrong measure

Take one SU(2) variable \(U=u_0I+i\boldsymbol u\cdot\boldsymbol\sigma\), with \(u_0^2+|\boldsymbol u|^2=1\), and \(S=-\beta u_0\), for finite positive beta. Consider

\[
\nu_{\rm bad}=\tfrac12\delta_I+\tfrac12\delta_{-I}.
\]

This singular two-point measure is different from the smooth positive Gibbs density. Nevertheless,

\[
\langle\beta^2|\boldsymbol u|^2-3\beta u_0\rangle_{\nu_{\rm bad}}=0
\quad\text{for every beta}.\tag{F1}
\]

The two center elements have zero vector part and opposite scalar parts. This is exact cancellation, not a Monte Carlo fluctuation. The complete hierarchy rejects this measure: choose \(f=u_0u_a\). Then

\[
L_af=\tfrac12(u_0^2-u_a^2),\qquad L_aS=\tfrac\beta2u_a,
\]

so at both center elements \(L_af-fL_aS=1/2\). Hence

\[
\langle L_af-fL_aS\rangle_{\nu_{\rm bad}}=\tfrac12.\tag{F2}
\]

The supplied exact-rational fixture checks (F1) and (F2). This is a one-link conditional model counterexample to the inference rule “one satisfied Ward residual implies the correct distribution.” It is not alleged to be an equilibrated four-dimensional lattice ensemble.

## 5. Independent normalized convolution benchmark

Define an auxiliary Markov integral operator on \(L^2(SU(2),H)\), with \(\beta>0\):

\[
(K_\beta f)(U)=\int\frac{\exp[\tfrac\beta2\operatorname{ReTr}(UV^\dagger)]}{Z_\beta}f(V)dH(V).
\]

For \(U=\cos\theta I+i\sin\theta\hat n\cdot\sigma\), normalized class Haar measure is \((2/\pi)\sin^2\theta d\theta\). For \(n=2j+1\), the spin-j character is \(\chi_j(\theta)=\sin(n\theta)/\sin\theta\). Direct integration gives

\[
Z_\beta=\frac{2I_1(\beta)}\beta,
\qquad
\int e^{\beta\cos\theta}\chi_j(\theta)dH
=I_{n-1}(\beta)-I_{n+1}(\beta)=\frac{2nI_n(\beta)}\beta.
\]

Central convolution and Schur orthogonality divide this last coefficient by the representation dimension n. Thus every matrix element in the spin-j sector has eigenvalue

\[
\boxed{\lambda_j=I_{2j+1}(\beta)/I_1(\beta).}\tag{K1}
\]

The factor n must not survive in the eigenvalue. Spin zero gives eigenvalue one. For positive beta every Bessel coefficient is positive. The kernel is symmetric, normalized and smooth; Peter–Weyl completeness therefore proves positivity of this operator, not merely positivity of a sampled matrix.

There is also a simple rigorous strict contraction on mean-zero states. Its density is bounded below by \(\epsilon_\beta=e^{-\beta}/Z_\beta>0\). Therefore \(K_\beta=\epsilon_\beta\Pi+(1-\epsilon_\beta)Q\), where Q is Haar-invariant Markov, and

\[
\|K_\beta\!\upharpoonright_{1^\perp}\|\le1-\epsilon_\beta<1.\tag{K2}
\]

This bound degenerates as beta grows. At beta zero the operator is the projection onto constants and the Bessel ratio formula must be evaluated by its limit. Positive eigenvalues approaching zero do not supply a uniform lower operator bound.

**Boundary of inference.** This convolution is a representation-theory calibration, not the complete four-dimensional gauge-invariant transfer operator. Spatial plaquette weights, gauge projection and interacting many-link states are absent. Its spin-sector energies are not glueball masses. The historical [Lüscher transfer-matrix construction](https://doi.org/10.1007/BF01614090) and [Menotti–Pelissetto reflection-positivity work](https://doi.org/10.1007/BF01221251) concern the proper lattice construction; their full proofs were not audited in this bounded review.

## 6. A current claimed construction: one precise local proof objection

The June 2026 [Faizal–Shabir preprint](https://arxiv.org/abs/2606.19362) claims a continuum construction. This review examined its abstract and selected Appendix C steps, not all 593 pages. After Eq. (C.94), PDF page 190, printed page 188, it states: “Both suprema are bounded by” the product-space L1 kernel norm. That direction is false for general kernels. A repair needs additional uniform row/column estimates for the specific kernel family. The objection below rejects this inference; it does not prove that every proposed construction in the paper is irreparable.

**Counterexample that retains positivity and Markov normalization.** On N atoms with uniform probability, let \(\Pi\) be the matrix with entries \(1/N\); let B be the identity except that its upper-left two-by-two block has all entries 1/2. Let \(v=(1,-1,0,\ldots)/\sqrt2\) and

\[
P_0=(1-c)B+c\Pi,\qquad P_1=P_0+\delta vv^T,
\quad0<c<1,\quad0<\delta<1-c.
\]

Both transition matrices are symmetric, positive semidefinite, row-stochastic, and strictly positive entrywise. To see positive semidefiniteness, B and Pi are orthogonal projections, \(Bv=\Pi v=0\), and the added rank-one term is positive semidefinite. Row sums of the added term vanish. Its two negative off-diagonal entries have magnitude \(\delta/2<(1-c)/2\), so entrywise positivity survives.

The density kernels with respect to uniform probability are \(K_r=NP_r\). Direct calculation gives

\[
\|P_1-P_0\|_{2\to2}=\delta,
\quad\|K_1-K_0\|_{L^1(H\otimes H)}=2\delta/N,
\quad\sup_i\frac1N\sum_j|K_1-K_0|_{ij}=\delta.\tag{F3}
\]

The first remains fixed while the second tends to zero. No universal multiplicative factor repairs the inequality for this family. These matrices need not satisfy every extra assumption of that preprint; the example establishes precisely that symmetry, positive semidefiniteness, strict kernel positivity, and Markov normalization do not suffice for the asserted implication.

**Correct replacement.** For the difference kernel D, independently prove
\(R=\operatorname*{ess\,sup}_x\int|D(x,y)|d\mu(y)\) and
\(C=\operatorname*{ess\,sup}_y\int|D(x,y)|d\mu(x)\).
Then Schur's test gives \(\|D\|_{2\to2}\le\sqrt{RC}\). Alternatively, a controlled Hilbert–Schmidt L2 kernel bound implies the operator bound. Uniformity as volume and ultraviolet cutoffs change remains to be established, rather than inferred from locality alone.

`check_exact_counterexamples.py` verifies the row sums, symmetry, strict entrywise positivity, eigenvector, product L1 and Schur values using exact rational arithmetic for six N values. Positive semidefiniteness and the operator norm are established by the preceding projection/rank-one proof; the script does not pretend that one eigenvector alone proves an operator norm.

## 7. Conditional transfer-stability lemma: the next useful bridge

Let T and S be positive self-adjoint contractions on one common Hilbert space, with the **same** normalized vacuum Omega and \(T\Omega=S\Omega=\Omega\). Suppose for physical time step a that

\[
\|T|_{\Omega^\perp}\|\le e^{-ma},\qquad\|T-S\|\le\varepsilon_a,
\qquad e^{-ma}+\varepsilon_a<1.
\]

Both operators preserve \(\Omega^\perp\). The triangle inequality gives

\[
\|S|_{\Omega^\perp}\|\le e^{-ma}+\varepsilon_a,
\quad
\Delta_S\ge-\frac1a\log(e^{-ma}+\varepsilon_a)>0.\tag{T1}
\]

Here \(\Delta_S\) means the spectral lower bound for the logarithmic generator on the vacuum-orthogonal sector; when a kernel exists, restrict to the support where the logarithmic generator is defined. For n time steps the telescoping identity also gives

\[
\|S^n-T^n\|\le n\varepsilon_a.\tag{T2}
\]

To retain any chosen \(0<m_*<m\), a sufficient condition is
\(\varepsilon_a\le e^{-m_*a}-e^{-ma}\sim(m-m_*)a\).
To derive fixed-time convergence from (T2), one needs \(\varepsilon_a=o(a)\), since \(n\approx t/a\). A bare \(\varepsilon_a\to0\) is insufficient for that argument.

This is an actionable conditional theorem, not a proven renormalization comparison for Yang–Mills. Matching the Hilbert spaces and vacuum, proving the operator norm with a correct estimate, maintaining gauge-invariant states, and obtaining uniformity in volume are explicit missing hypotheses. They must be checked before the planner adds edge T1 to a physical continuum route.

## 8. Strong-coupling source normalization and continuum obstruction

[Shen–Zhu–Zhu, 2204.12737v1](https://arxiv.org/pdf/2204.12737), Eq. (1.2), uses density \(\exp[N\beta_{SZ}\operatorname{Re}\sum_p\operatorname{Tr}U_p]\). Its SU(N) assumption is \(|\beta_{SZ}|<1/[16(d-1)]\). Matching the Wilson exponent gives \(\beta_W=N^2\beta_{SZ}\); thus SU(2), d=4 requires \(|\beta_W|<1/12\). Theorem 1.4 concerns the Langevin functional inequality; Corollary 1.6 separately proves spatial covariance decay. These are fixed-spacing results. Relevant definitions, assumptions and introductory theorem statements were read, not the entire 43-page proof.

In the ordinary asymptotically free continuum program, the bare coupling approaches zero and beta_W grows without bound as a shrinks. A theorem confined to beta_W below 1/12 therefore cannot be followed directly along that trajectory. This does not refute the strong-coupling theorem. It identifies a missing renormalization argument connecting regimes. A fixed-spacing finite-volume gap also supplies no uniform physical mass by itself.

The official [Jaffe–Witten description](https://www.claymath.org/wp-content/uploads/2022/06/yangmills.pdf) requires a nontrivial quantum theory on four-dimensional spacetime with an actual positive physical gap for every compact simple group, under appropriately stringent field-theory axioms. SU(2) is a useful first nonabelian target, but does not cover every group. Reconstruction, infinite volume, continuum control and nontriviality remain independent obligations.

## 9. Bidirectional obligation graph and down-selection

| Direction | Established or conditional implication | Missing premise to expose |
|---|---|---|
| Forward | Compact product Haar + finite smooth Wilson action → normalized finite Gibbs law | No missing premise at this finite regulator |
| Forward | Haar invariance → all identities H1 | Correct action and every derivative convention |
| Meeting | Complete H1 family ↔ finite Gibbs law, H3 | Finitely sampled identities do not meet the complete-family premise |
| Forward calibration | SU(2) characters → exact auxiliary convolution spectrum K1 | Full interacting gauge transfer operator absent |
| Backward | Physical Hamiltonian gap ← common exponential decay on dense physical-state family | Round-8 spectral lemma hypotheses, including all times and positive spectral representation |
| Backward | Decay in the continuum ← limits of uniformly bounded matched correlators | Continuum construction and uniform physical decay rate |
| Backward | Stable transfer gap ← T1 with admissible comparison maps | Correct operator error of order a, common vacuum, uniform volume control |
| Unresolved join | Strong-coupling fixed-lattice control → weak-coupling continuum trajectory | Controlled renormalization and reconstructed nontrivial limits |

The A*-style proof planner should treat conjunctions as obligations, not as a scalar confidence score. In particular, H3 requires the quantifier over **all smooth insertions**; deleting that quantifier must fail certificate replay. A source citation establishes what an external theorem assumes, not that the project satisfies it.

| Rank | Candidate | Feasible result now | Main falsifier | Verdict |
|---|---|---|---|---|
| 1 | Finite SU(2) Wilson code + H1/H2/H3 | Exact theorem and authentic nonabelian simulation diagnostics | Wrong staple orientation, wrong beta normalization, F1/F2 false pass | Execute in this round |
| 2 | Positive convolution spectrum | Exact group-integral calibration for numerical weights | Missing representation-dimension factor; missing Haar sine-squared weight | Execute as auxiliary benchmark |
| 3 | Controlled transfer comparison | T1/T2 conditional proof; F3 rejects bad norm transfer | L1-only estimate and insufficient o(a) scaling | Derive now; actual YM bound remains open |
| 4 | Wilson-loop positivity bootstrap | Finite admissible constraints and bounds on small observables | Invalid loop identities, truncation treated as completeness, uncertified SDP tolerances | Next bounded implementation after H1 verified |
| 5 | Full strong-to-weak continuum construction | Formal proof-obligation map | Regulator-dependent constants or assumed reconstruction | Research frontier, no completion claim |

The [2025 SU(3) positivity-bootstrap paper](https://arxiv.org/abs/2502.14421) provides a concrete next method combining loop equations and positivity to bound plaquette expectations. Only its abstract and publication metadata were read here. A plaquette bound is not a mass-gap bound. A useful project extension would generate exact loop constraints, then verify a small optimization certificate independently before attempting larger truncations.

## 10. Concrete experiments and review gates

1. Freeze the plaquette-counting convention. On multiple admissible geometries compare all-link action to local-staple action differences using independent complex-matrix operations. Detect both an orientation error and a factor-two coupling mutation.
2. Check generator derivatives of the action, first and second order. Include all-identity, random Haar, a zero staple sum if constructible, and small positive beta. Reject degenerate periodic dimensions instead of silently applying a formula outside its domain.
3. Run short Wilson ensembles at beta inside the translated rigorous strong-coupling range and at a separate larger beta. Report each run as a finite simulation. Keep initialization, burn-in, effective sample size and autocorrelation uncertainty separate from exact identities.
4. Check several SD insertions, retaining F1/F2 as a deliberate false-pass fixture. Multiple passes strengthen diagnostics but still do not supply H3's infinite set of identities.
5. Compare convolution eigenvalues obtained by independent Haar quadrature with Bessel ratios. Keep beta-zero limits and large-beta overflow control explicit. Do not plot these as full four-dimensional masses.
6. Run the exact F3 family and plot both product L1 and Schur/operator norms. Use it to test the proof planner: reject the L1-only rule, accept the correct Schur rule only with both bounds supplied.
7. Plan an actual transfer comparison only after defining the common physical Hilbert-space embedding. Record an obstruction if vacuum normalization, gauge projection or uniform row bounds cannot be supplied. Do not manufacture a positive mass term to force a pass.

## 11. Primary-source ledger and actual reading depth

| Source | Location inspected | Use and remaining limitation |
|---|---|---|
| [Clay maintained page](https://www.claymath.org/millennium/yang-mills-the-maths-gap/) | Current full page | Official open-problem status |
| [Jaffe–Witten](https://www.claymath.org/wp-content/uploads/2022/06/yangmills.pdf) | Problem statement and constructive discussion in parsed primary text | Exact target; full bibliography not reread |
| [Shen–Zhu–Zhu](https://arxiv.org/pdf/2204.12737) | Eq. 1.2, Assumption 1.1, Theorems 1.2/1.4, Corollary 1.6, nearby discussion | Correct normalization and distinct finite-spacing results; no full proof replication |
| [Lüscher 1977](https://doi.org/10.1007/BF01614090) | Publisher metadata | Original transfer-matrix reference; no claim of full-text audit |
| [Menotti–Pelissetto 1987](https://doi.org/10.1007/BF01221251) | Publisher metadata and indexed abstract | Reflection positivity reference; attempted primary PDF returned no readable full text |
| [Chatterjee et al., 2608.05415v1](https://arxiv.org/html/2608.05415v1) | Sections II–III and continuum-scope discussion | Compact-group identities; ordered/unordered counting in Eq. 8 appears inconsistent, so its numerical force prefactors were not adopted |
| [Sternbeck–Schaden–Mader](https://arxiv.org/abs/1502.05945) | Abstract and selected Landau-gauge derivation | Gauge-fixed identities need extra structures; no identification with our unfixed insertions |
| [Guo et al., 2502.14421](https://arxiv.org/abs/2502.14421) | Abstract and publication metadata | Next bootstrap candidate; no code or SDP certificate replicated |
| [Faizal–Shabir, 2606.19362v1](https://arxiv.org/pdf/2606.19362) | Abstract and selected Appendix C, C.82–C.104 | Precisely scoped norm-inference objection; no full-manuscript verdict |

The exact local counterexample and complete-hierarchy proofs can be checked independently of the external authors' conclusions. The reports must retain both the accepted finite results and the missing continuum premises.

## 12. Independent review correction and final execution

The independent skeptic accepted H3, F1/F2, F3, the conditional T1/T2 hypotheses, and the beta normalization. It found a real evaluator defect in the first rational fixture: required checks used Python `assert`, which disappears under `python -O`, while the script would still report success. The corrected fixture uses explicit recorded gates and raises on failure; success requires a nonempty completed gate list, and output records the evaluator source hash.

Normal and optimized execution each completed the same 68 gates with identical counterexample values. Deliberately injected failure exited with code 1 in both modes and wrote no false-success artifact. `optimization_gate_review.json` records the comparison. These 68 checks are implementation checks of the stated exact fixtures; they are not 68 independent theorems or evidence of a continuum Yang–Mills gap. The numerical thresholds and mathematical statements were unchanged by the repair.
