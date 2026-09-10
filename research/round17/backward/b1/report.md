# B1 independent derivation: dense two-cube physical trial

The graph has vertices (x,y,z) with x=0,1,2 and y,z=0,1, positive coordinate links, and all eleven elementary squares. It has twelve vertices and twenty links. The internal square is counted once. The Hilbert space is the untruncated gauge-invariant subspace of the link Haar space, with Gauss law at every vertex and no external charges. H=αΣC_e−Σ_(p=1)^11 λ_p x_p, α>0, uses signed physical energies λ_p. The link-disjoint theorem from A2 is inapplicable to this dense support.

## Actual graph and all trial entries

Let χ_p=2x_p be the ordinary fundamental character of the oriented face holonomy. Its link product is Haar, so ⟨χ_p⟩=0, ⟨χ_p²⟩=1, and ⟨χ_p⁴⟩=2. Distinct face characters have zero overlap: the actual two-face support has a center-odd edge. It follows that Ω,χ₁,…,χ₁₁ are orthonormal. These are smooth gauge-invariant cylindrical functions in the electric operator domain.

Every link in χ_p carries representation j=1/2 and every other link is constant. Thus H₀χ_p=4α(3/4)χ_p=3αχ_p. The vacuum-to-face magnetic entry is ⟨Ω,Wχ_p⟩=−λ_p/2. Every face-to-face magnetic entry is zero. To check repeated indices correctly, form the *exponent multiplicity* of each face in χ_p x_f χ_q and sum those exponents on each link modulo two. For p=q=f there are three copies, for exactly two equal labels the exponents are two and one, and for three distinct labels all exponents are one. In every case an odd link exists. Center reversal of that link kills the integral. Squared-character Gram entries instead have even exponents and must be evaluated by the nonzero Haar second moment; replacing exponent counts by a set would give the wrong answer.

The resulting twelve-state matrix has diagonal 0,δ,…,δ with δ=3α and entries −λ_p/2 connecting the vacuum to each face. This is a full matrix-element calculation within the physical domain, not a physical Hilbert-space truncation assumption.

## Trial ground upper bound and a separate full excited lower bound

Put L=Σ|λ_p| and Q=Σλ_p². If Q>0, the trial matrix reduces on the vacuum and the face vector proportional to (λ₁,…,λ₁₁) to a two-dimensional block with offdiagonal −√Q/2; the other ten trial directions have eigenvalue δ. Its lowest eigenvalue is

\[
E_{\rm trial}=\frac{\delta-\sqrt{\delta^2+Q}}2.
\]

If Q=0 the vacuum remains the trial ground with energy zero. In both cases the Rayleigh–Ritz principle gives E₀(H)≤E_trial. An independent exact determinant calculation tests the characteristic factor (δ−z)^10[z²−δz−Q/4], including z=δ and the zero-coupling degeneration.

For the *full physical* free Hamiltonian, the gap is δ=3α. A nonvacuum gauge-invariant spin network has no vertex incident on exactly one nontrivial representation: that representation alone cannot form a singlet. Its active support has minimum degree at least two and contains a cycle. The actual coordinate graph is bipartite, has no triangles and has a four-link square. Thus at least four nontrivial links contribute at least 3α/4 each; a fundamental face character attains 3α. This argument concerns the full physical spectrum, not the unprojected single-link gap.

The perturbation is bounded with ||W||≤L, so full-operator min–max gives E₁(H)≥δ−L. Combining this *lower* bound with the ground *upper* bound gives

\[
\Delta(H)\ge\frac{\delta+\sqrt{\delta^2+Q}}2-L.
\]

The trial matrix's own gap is generally larger and is not a full physical lower bound. A large-coupling fixture explicitly contrasts its positive gap with an insufficient combined full-operator estimate.

## Exact common-ratio threshold and numerical certification

For eleven equal magnitudes |λ_p|=αr, r≥0, divide the sufficient gap bound by α:

\[
g(r)=\frac{3+\sqrt{9+11r^2}}2-11r.
\]

If 22r−3≤0 positivity is immediate. Otherwise squaring the equivalent positive-sided inequality yields 11r(12−43r)>0. Hence this bound is strictly positive exactly for 0≤r<12/43, zero at r=12/43 and negative beyond it. At the endpoint the radical is exactly 135/43, so a floating residual cannot turn zero into a positive certificate.

At r=3/11 the older global estimate δ−L vanishes, but the combined bound equals (√(108/11)−3)/2>0. The signs of equal-magnitude coefficients do not affect L or Q; signed unequal coefficients are evaluated individually. This is a finite dense-graph improvement, not a volume-uniform result.

The independent radical method uses rational Newton upper iterates with directed decimal-grid rounding and the reciprocal lower bound q/u. Exact rational squares are recognized separately. Every output interval is checked by squaring its endpoints; finite iteration caps remain explicit precision failures. This differs from an integer dyadic-square-root bracket. All matrix and interval acceptance uses rational arithmetic; rounded values are for display only.

No field or action coefficient is added to obtain this result. A future additional representation or trial amplitude would enlarge a candidate state space at the same Hamiltonian parameters. B2 remains unexecuted until the advisor reviews B1's exact failed endpoint.

The completed independent program passes 23 focused gates, including all 144 Gram entries, all 1,584 inserted magnetic entries and exact determinant evaluations for seven parameter fixtures. A separate 14-gate comparison reconstructs the forward graph's face ordering and all its saved entries, then admits its dyadic brackets by exact square inequalities and compares them with the independent rational Newton intervals. Ordinary and optimized outputs are byte identical; repeated execution counts once.

At the old endpoint the independent lower endpoint is 2667956144051/40000000000000, approximately 0.066698903601275. The forward method obtains a tighter valid dyadic endpoint; both intervals contain the same analytic sufficient bound. At the new endpoint both methods return exact zero and preserve the insufficient status. The deliberate zero-step Newton case preserves its precision failure. Substitution of the trial gap as a physical lower bound and relabeling the exact zero endpoint as positive are independently rejected.

The complete forward matrix/Haar module, runner and fixed evidence were read after the independent derivation and implementation. No forward code is imported. The comparison checks the same geometric faces despite a different enumeration order. No material discrepancy was found. The graph parser checks integer coordinates and axes, signed paths and complete distinct squares. This is a scoped analytic and exact-arithmetic review, not exhaustive branch coverage or a formal proof-assistant verification.

Run `python check.py --output NEW_OUTPUT_DIRECTORY`; the output must be outside the source directory. The separate `compare.py --producer SOURCE_DIRECTORY --evidence EVIDENCE_DIRECTORY --output NEW_OUTPUT_DIRECTORY` reproduces the focused comparison. The manifest binds these files and both acceptance records. The remaining B2 endpoint improvement has not been executed.
