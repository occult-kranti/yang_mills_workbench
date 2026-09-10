# Independent B2: a signed finite-graph coupling box

For the actual two-cube physical SU(2) Hamiltonian H=αΣ_eC_e−Σ_pλ_px_p, α>0, the entire real coefficient box |λ_p|≤3α/8 satisfies

\[
\Delta_{\rm physical}\ge\alpha\frac{27-3\sqrt{70}}{16}
\approx0.11876245024860835\,\alpha.
\]

When all eleven magnitudes equal 3α/8, with arbitrary signs, a separate ground-energy trial improves the bound to

\[
\Delta_{\rm physical}\ge\alpha\frac{3+15\sqrt3-3\sqrt{70}}{16}
\approx0.2425600823444308\,\alpha.
\]

These are lower bounds for the full untruncated physical operator on this fixed graph. They are not inferred from sampled coupling values, gaps between trial eigenvalues, or an infinite-volume limit.

## Complete form on a codimension-one subspace

B1 supplies the orthonormal physical subspace P=span(Ω,χ_0,…,χ_10), the reducing electric complement Q=1−P with QH₀Q≥9αQ/2, and the exact subtracted cross Gram of W=QVP. In particular, with r=max_p|λ_p|/α,

\[
\|W\|^2\le\frac{21}4\alpha^2r^2,
\qquad QHQ\ge\alpha(9/2-11r)Q.
\]

Take any normalized physical form-domain vector ψ perpendicular to the bare vacuum Ω. Write ψ=u+v, u=Pψ and v=Qψ. Since u has no vacuum coordinate, its P magnetic form vanishes exactly by B1's complete mixed-triple Haar identities; its electric form is 3α||u||². Cauchy–Schwarz and the full operator W bound therefore give

\[
\frac{\langle\psi,H\psi\rangle}{\alpha}
\ge3s^2+c t^2-2bst,
\quad s=\|u\|,\ t=\|v\|,\quad
c=9/2-11r,\ b=\sqrt{21}\,r/2,
\]

where s,t≥0 and s²+t²=1. This uses the complete Q space; no finite tail sample replaces it. Compact resolvent and the closed form permit Courant–Fischer min–max. Choosing the codimension-one subspace Ω-perpendicular gives a lower bound for the full E₁ even though Ω is not the interacting ground. Separately, the vacuum trial yields E₀≤⟨Ω,HΩ⟩=0. Thus any positive lower bound obtained here for E₁ also bounds E₁−E₀ from below.

## Analytic coverage of all eleven signed coefficients

For r≤3/8, c≥3/8 and b≤3√21/16. Because s and t are nonnegative norms, the quadratic form is bounded below by

\[
3s^2+\frac38t^2-\frac{3\sqrt{21}}8st.
\]

This comparison is valid on nonnegative norm coordinates. It is not a claim that every varying scalar matrix exceeds the endpoint matrix in Loewner order for arbitrary signed scalar coordinates. Indeed, the difference between the r=0 matrix and the endpoint matrix has zero first diagonal and nonzero off-diagonal; its determinant is negative. Treating that difference as positive semidefinite would be wrong.

The endpoint scalar matrix has diagonals 3,3/8 and off-diagonal −3√21/16. Its lower eigenvalue is K=(27−3√70)/16. Independently of the eigenvalue formula, the shifted matrix M−KI is positive semidefinite: its diagonal entries are nonnegative and its determinant is zero. Equivalently, when the first diagonal is positive, completion of a square leaves a zero Schur complement. The exact inequality 27²>9·70 proves K>0. This covers the entire real eleven-dimensional box, including zeros and all signs, because only absolute coefficient bounds entered. No grid-coverage inference is used.

At a general sample radius r, the scalar expression is

\[
R(r)=\frac{3+c-\sqrt{(3-c)^2+21r^2}}2.
\]

The retained radius values are 0,1/8,1/4,12/43,1/3,3/8,2/5,1/2. The last two illustrate insufficient scalar estimates outside the frozen box; they do not enlarge the accepted theorem. At r=0 the cross vanishes and R(0)=3 exactly. All actual claimed box certificates verify the complete eleven-component vector, so an oversized component cannot be hidden behind a passing label.

## A separately valid ground-energy trial

The exact P Hamiltonian is a star matrix with vacuum diagonal zero, face diagonal 3α and vacuum-to-face entries −λ_p/2. Its nontrivial lowest Ritz value is

\[
E_{0,\rm trial}=\frac{3\alpha-\sqrt{9\alpha^2+\sum_p\lambda_p^2}}2.
\]

For all endpoint magnitudes, Σλ_p²=99α²/64, giving E₀≤α(24−15√3)/16<0. Signs do not change this value. Subtracting this upper bound on E₀ from the independently established lower bound αK on E₁ gives the stronger endpoint gap stated above. Subtracting two Ritz eigenvalues would instead be an invalid lower-bound argument. Sparse or interior vectors do not receive an endpoint-only improvement merely from an attached metadata flag.

## Independent rational bounds and edge cases

The independent radical routine uses rational Newton iteration from a certified upper bound u≥√q, with lower bound q/u. Each update u←(u+q/u)/2 remains an upper bound because its squared excess over q is (u²−q)²/(4u²)≥0. Exact rational squares are recognized by a separate integer bisection. The routine stops at an explicitly bounded radical-interval width. Every returned interval is checked by rational squaring.

For each scalar sample, a second calculation checks that subtracting the returned lower eigenvalue bound leaves both scalar diagonals and the determinant nonnegative. This provides an independent congruence/positive-semidefinite check, including the r=0 zero-first-diagonal case, where division by that diagonal would be invalid. The requested displayed gap-constant interval width is at most 10⁻¹² in dimensionless units; physical interval widths scale with α. Coarse endpoint intervals remain insufficient when their sign or width cannot certify the target. A coarse negative lower endpoint is not rescaled by α_min as though a lower energy scale preserved that inequality direction.

Two nonunit physical scales are retained. A common physical lower bound α_minK requires α≥α_min>0 explicitly. A dimensionless coupling box alone does not supply a common physical energy scale. The endpoint ground-energy interval is labelled in units of α, and its use in the gap calculation preserves lower/upper directions.

## Actual failure mechanisms for missing premises

Deleting the scalar cross term would give an unjustified lower scalar eigenvalue 3/8 at the endpoint. In the full endpoint scalar matrix, the vector (1,√21) has norm squared 22 and quadratic form 3, hence Rayleigh quotient 3/22<3/8. This directly refutes that deletion in the comparison argument; it is not a claim that a particular physical vector realizes every worst-case inequality simultaneously.

The P form only vanishes magnetically after the vacuum coordinate is removed. For the actual vector Ω+χ_0, the magnetic quadratic form is −λ_0, not zero. Dropping the codimension-one requirement therefore invalidates the asserted P estimate. Dropping the complete tail premise permits abstract extensions such as diag(0,0,3), whose gap is zero. A separate Ritz counterexample diag(0,1/8,3), restricted to trial coordinates 0 and 2, has trial gap 3 but true gap 1/8. These are explicitly scoped logical counterexamples, not spectra claimed for the two-cube operator.

The source-facing premise fields record mathematical antecedents. Their Boolean values are not proof objects or substitutes for the accepted B1 source replay: the project proof adapter must independently admit the actual complement, projection and cross results. Missing complement, cross and codimension-one antecedents are rejected. The B1 amendment remains applicable: fourth-order independent Haar agreement is true, Gaussian repeated moments falsify exact Haar data, and unsubtracted PV²P remains a possible conservative upper bound even though it is not the exact sharper cross Gram used here.

## Bare-coupling applicability check

The advisor's primary-source review of [Bauer and collaborators, equations 55–56](https://arxiv.org/pdf/2307.11829) supplies H_E=g²ΣC_e/(2a) and H_B=ΣTr(2I−U_p−U_p†)/(2g²a). In SU(2), Tr U_p=Tr U_p†=2x_p. Removing the additive constant 2N_faces/(g²a), which does not affect a spectral gap, therefore gives

\[
\alpha=\frac{g^2}{2a},\quad\lambda=\frac2{g^2a},\quad
r=\frac4{g^4},\qquad r\le\frac38\iff g^4\ge\frac{32}3.
\]

The rational implementation independently verifies this algebra with nonunit spacings. Along g→0, r diverges and leaves the selected box. This is an obstruction to applying this particular sufficient bound on that path, not a disproof of a continuum mass gap. The arbitrary signed mathematical box is not silently identified with the usual positive homogeneous bare-coupling model, and A2's decaying family is distinct again. The source's other numerical or truncation constructions have not been reproduced here.

## Final review and retained integrity correction

The final independent suite passes 32 named checks. Its complete producer comparison passes 28 additional checks, reconstructing all eleven fixed certificates, the eight scalar samples, complete radical and ground-trial transports, source-bound B1 antecedents and the exact coupling CSV. The producer's dyadic cells are independently identified by integer bisection and checked against rational Newton enclosures; shifted-matrix principal minors supply a second scalar validation. Producer solver routines are not imported for the arithmetic oracle. An isolated subprocess imports the producer only to retest the repaired admission boundary. Ordinary and optimized Python give byte-identical scientific and comparison outputs.

The source audit found an actual pre-freeze defect: a caller could mutate the producer's required full-complement declaration to false and still receive a certificate marked analytically positive. On-disk hashes alone did not detect this in-memory change. The original source and reproduced false admission are retained in history. The repaired producer compares its premise map, file pins, precision target and sample inventory against an initial canonical snapshot before admission. Independent subprocess checks now reject both the original false-complement mutation and a relaxed precision target. The independent conditional-antecedent helper also rejects changes to its initial declaration.

Review of the independent output caught ambiguous names such as physical_gap_interval. They were replaced by explicit lower-formula interval names, with a statement that upper endpoints do not upper-bound the physical gap. The original source and results are retained; the numerical values did not change. All displayed enclosures throughout this report concern analytic bound or trial-energy expressions. The fixed-graph spectrum is constrained only in the proved one-sided directions.

The producer implementation, runner, report and source/premise bindings were reviewed in full. No further material defect was found after the documented repair. The final manifest binds the scientific results, complete comparison, source review and retained failures. C1 remains unexecuted pending the advisor gate.

The advisor then caught a portability defect in the comparison wrapper: recursively collecting producer files also collected evidence folders when the accepted repository layout nested them under the source directory. That failure was reproduced on a copied layout and retained. The wrapper now excludes only the known output and comparison directories, while continuing to reject undeclared source files. The repaired accepted-style copy produces byte-identical comparison results, and an added undeclared source file still fails. These two bounded portability checks are recorded separately from the 32 scientific and 28 comparison checks; they do not change the physics or add another research loop.
