# A1 independent derivation: local control and its exact obstruction

This derivation was written before reading the forward A1 implementation or evidence. The implementation in this directory is new and uses no forward imports or reused project source. It treats the full link Hilbert space and the physical Gauss sector explicitly.

On the full tensor product of L²(SU(2), normalized Haar) link spaces, let P_e project onto the constant function. Let P_p be the product of these four commuting projections on a square and Q_p=1−P_p. The plaquette multiplier x_p=Tr(U_p)/2 is real and has norm at most one. The product of four independent Haar links is Haar, including inverse orientations. Thus its mean is zero and its second moment is 1/4. Integrating over all four plaquette links gives P_p x_p P_p=0. Since P_p has rank one on those links, ||x_p P_p||²=1/4, and x_p P_p already lies in Q_p. Consequently ||Q_p x_p P_p||=1/2 exactly. The action on other links is the identity. This is an operator statement on the full space, not a finite matrix approximation.

Inserting P_p+Q_p on both sides gives the exact split x_p=Q_p x_p Q_p+P_p x_p Q_p+Q_p x_p P_p. The missing P_p x_p P_p term vanishes; the two off-diagonal terms do not. In the normalized character basis, xχ₀=χ₁/2 and xχ_n=(χ_(n−1)+χ_(n+1))/2 for n≥1. Finite principal matrices reproduce the local vacuum coupling but are used only to check the split; their spectral norm is not substituted for the full multiplication norm.

The edge projections commute, so their joint occupation basis proves Q_p≤Σ_(e∈p)(1−P_e). A nontrivial link representation has label n=2j≥1 and Casimir n(n+2)/4≥3/4. The exact difference n(n+2)−3=(n−1)(n+3) proves 1−P_e≤4C_e/3 on the full quadratic-form domain. Hence Q_p≤(4/3)Σ_(e∈p)C_e. Actual open three-dimensional cubic incidence is at most four plaquettes per link, giving Σ_p Q_p≤(16/3)Σ_e C_e.

For any form-domain vector, |⟨ψ,Q_p x_p Q_p ψ⟩|≤||Q_pψ||². The diagonal magnetic sum therefore satisfies

\[
\left|\left\langle-\sum_p\lambda_p Q_p x_p Q_p\right\rangle\right|
\le\frac{16}{3}\max_p|\lambda_p|\left\langle\sum_e C_e\right\rangle.
\]

Relative to H₀=αΣC_e the coefficient is 16 max|λ_p|/(3α). The energy units must not be suppressed. Boundary links may have smaller incidence; no lower-degree boundary is assigned the bulk value as an equality.

All P_e commute with left and right group actions and therefore with vertex gauge transformations. The projections and all operators in the split preserve the physical Gauss sector. Nevertheless the local Casimir estimate is an unprojected link estimate. The unprojected one-link gap is 3α/4. The physical square character carries four fundamental links and has electric energy 3α. Replacing the former by the latter incorrectly strengthens the projector estimate by a factor of four; a single fundamental link state explicitly falsifies that replacement.

Now choose any actual square p in the open graph and the normalized physical vector ψ_t=(Ω+tχ_p)/sqrt(1+t²), with t real and χ_p=2x_p. Both terms are gauge invariant and belong to the electric operator domain. Character orthogonality gives ||χ_p||=1, ⟨Ω,χ_p⟩=0, ⟨Ω,x_pχ_p⟩=1/2 and ⟨χ_p,x_pχ_p⟩=0. It follows exactly that

\[
\langle H_0\rangle_{\psi_t}=\frac{3\alpha t^2}{1+t^2},\qquad
\langle-\lambda_p x_p\rangle_{\psi_t}=\frac{-\lambda_p t}{1+t^2}.
\]

Every other elementary-square magnetic term has zero expectation in this vector: a distinct square has an edge absent from p, and center sign reversal on that link kills each relevant term. Thus the example also isolates λ_p inside a full collection of couplings.

For nonzero t the signed quotient is −λ_p/(3αt), and its magnitude diverges as t→0 whenever λ_p≠0. No finite constant can give a pure form bound |⟨V⟩|≤c⟨H₀⟩ for the full magnetic perturbation. The diagonal part has zero expectation in this example; all linear-in-t work comes from the vacuum-offdiagonal part. At λ_p=0 the quotient is zero for nonzero t. At t=0 both expectations vanish and the quotient is undefined, not a computed zero. Signs of λ_p and t determine the sign of the magnetic energy without affecting the absolute divergence.

This is a failure of a proposed pure relative-bound shortcut, not a gap-closing theorem. Bounds with an additive vacuum-energy term and applicable local stability theorems are not excluded. A1 stops before an all-order/local contraction argument for overlapping interactions. No numerical dense-family threshold is inferred from 1/2 or 16/3. The advisor owns the source-applicability audit; this independent derivation does not claim to have extracted its missing constant.

The independent program completed 97 named checks, and a subsequent read-only comparison reconstructed the forward evidence through 22 additional named comparison gates. Ordinary and optimized Python outputs are byte identical; repeated runs count once. The forward source was read only after this independent derivation and implementation, and no forward code was imported. Its operator, graph and signed-trial values agree. The standalone entry point is `python check.py --output NEW_OUTPUT_DIRECTORY`; outputs must be outside the frozen source directory.

The advisor identified one real validation defect after the initial 95 checks passed: a Boolean coordinate could alias integer one in an edge endpoint or a face vertex. Both malformed inputs were reproduced as incorrectly accepted. Strict integer triples are now required at every coordinate occurrence, and two held-out regression cases reject the former aliases. The original source, two-case failure record and initial 95-check outputs are retained in history. This affected malformed graph admission, not the proved formulas or the valid graph results. The complete final source and independent comparison are bound by the manifest. No further A1 obstruction remains beyond the explicitly missing dense-family stability estimate; A2 has not been executed.
