# Product-vacuum stability gives a genuine fixed-spacing Hamiltonian gap

**Verdict:** Yarotsky's small bounded-interaction theorem applies to the unreduced link Hilbert space of the static SU(2) lattice Hamiltonian after a finite blocking of link orientations. It yields a qualitative, volume-independent positive Hamiltonian gap for sufficiently small magnetic/electric ratio. Infinite-dimensional link spaces are explicitly allowed. The available theorem states existential constants; this review does not produce an evaluated numerical coupling threshold.

“Weak interaction” here means a small plaquette perturbation of the electric product vacuum. In the usual gauge-coupling convention this is an electric-dominated, strong bare gauge-coupling regime. It is distinct from weak bare gauge coupling.

## 1. Exact primary theorem and reading boundary

Yarotsky, *Quasi-particles in weak perturbations of non-interacting quantum lattice systems*, arXiv:math-ph/0411042v1, November 11, 2004, specifies possibly infinite-dimensional site Hilbert spaces, nonnegative self-adjoint possibly unbounded hₓ with a unique vacuum and gap at least one, and bounded perturbations φₓ supported on translates of one finite range S. Theorem 1 asserts constants c₁(S), c₂(S)>0 such that sufficiently small ε=supₓ‖φₓ‖ gives a unique finite-volume ground state and a vacuum-subtracted gap at least 1−c₂ε, uniformly in the empty-boundary finite volume. Theorems 2–3 provide the corresponding ground-state limit and a self-adjoint gapped generator in its GNS representation. Translation invariance is introduced only afterward for the quasiparticle claims, which are not imported here. [Primary paper, definitions and Theorems 1–3, pp. 2–4](https://arxiv.org/pdf/math-ph/0411042).

The same author reviews the expansion behind these statements in Section 2, referring to earlier proofs. This review checked the displayed hypotheses, theorem statements and that selected expansion discussion, rather than independently rebuilding the complete cluster expansion. No value for c₁ or c₂ is evaluated in the inspected statements.

## 2. Exact link-to-site dictionary

Fix a spatial dimension d≥2, a spacing a>0, α>0, and real static plaquette coefficients with λ_max=supₚ|λₚ|<∞. Every positively oriented link is represented exactly once by its tail x and direction i. Group the d outgoing links at x into

\[
 \mathcal K_x=\bigotimes_{i=1}^dL^2(SU(2),dU_{x,i}),
 \quad h_x=\frac43\sum_{i=1}^d C_{x,i},
 \quad \delta_0=\frac{3\alpha}{4}.
\]

The normalized constant Ωₓ is the unique hₓ vacuum. Each nonconstant link representation has j≥1/2 and C=j(j+1)≥3/4, so hₓ has gap one. Its unboundedness is permitted by the theorem.

An elementary plaquette based at x in directions i<j uses link cells x, x+eᵢ and x+eⱼ. Thus every such interaction fits in a translate of the fixed finite set S={0,e₁,…,e_d}. With Wₚ=Tr(Uₚ)/2, ‖Wₚ‖=1. Remove the scalar magnetic offset, divide the Hamiltonian by δ₀, and group all based plaquettes at x:

\[
 \phi_x=-\frac1{\delta_0}\sum_{i<j}\lambda_{x,ij}W_{x,ij},
 \qquad
 \epsilon=\sup_x\|\phi_x\|
 \le\frac{4}{3}\binom d2\frac{\lambda_{\max}}\alpha.
 \tag{Y1}
\]

The omitted scalar offset changes the ground energy but not the spectral gap. These steps are a regrouping and rescaling of the same static gauge Hamiltonian, not new fields or an electric-representation truncation.

## 3. The boundary convention must be explicit

The source's empty boundary keeps φₓ only when the entire translate x+S lies inside the chosen cell set B. For d>2 this can omit some boundary plaquettes whose actual three-cell support lies in B while another unused point of x+S does not. Therefore the source boundary prescription must not silently be called the all-contained-plaquette prescription.

The qualitative finite-volume gap also covers the latter prescription by a padding argument. Enlarge B to B⁺ containing every x+S with x∈B. For this finite-volume application choose each bounded φₓ to contain exactly those based plaquettes whose actual support lies in B, and set all other φₓ to zero. This is an allowed inhomogeneous interaction family with the same range S and the same bound Y1. The Hamiltonian in B⁺ is the desired all-contained-plaquette Hamiltonian on B plus decoupled free cells in B⁺\B. The gap of the sum is the minimum of the desired gap and the free-cell gap. Hence the theorem's lower bound for the padded system also bounds the desired finite-volume gap.

This argument uses a separate admissible perturbation family for each finite B, which is legitimate because the theorem's constants depend on S rather than the values or number of φₓ. It establishes a uniform finite-volume bound. For a specific infinite-volume state construction, use the source's stated empty-boundary sequence and Theorems 2–3. Equality of limits obtained from every other boundary sequence is a separate assertion and is not needed for this application.

Outgoing links at an outer cell face may be dangling. The full-space theorem permits them. Imposing Gauss law at every endpoint removes charge-free dangling electric flux; it does not introduce lighter physical excitations.

## 4. Consequence with a qualitative threshold

Let P=binom(d,2), and choose

\[
 \kappa_*=\frac{3}{4P}
       \min\left(c_1(S),\frac1{2c_2(S)}\right)>0.
\]

For λ_max/α<κ*, Y1 and the source theorem give

\[
 H_B-E_B\ge\frac{3\alpha}{8}(I-P_{\Omega_B}),
 \tag{Y2}
\]

uniformly over the declared finite volumes. The same qualitative lower threshold applies to the source's infinite-volume generator. In d=3, the perturbation estimate is simply ε≤4λ_max/α. The coefficient 3α/8 is an algebraic consequence of choosing c₂ε<1/2, not a numerically certified interval in λ/α. A simulation at any particular positive λ/α cannot be labelled inside κ* until a valid numerical threshold is independently extracted.

## 5. Restricting to Gauss-invariant states

Every electric Casimir and Wilson plaquette commutes with the local SU(2) gauge transformations. On a finite graph the unique full-space ground vector therefore spans a one-dimensional representation of the finite product of vertex SU(2) groups. A continuous one-dimensional unitary representation of this product is trivial: its Lie-algebra character vanishes on commutators, while su(2) is equal to its commutator algebra. Connectedness then makes the group character trivial. The ground vector is gauge invariant.

The physical sector is a reducing subspace containing that ground vector. Restricting Y2 to it preserves the lower-gap inequality. This does not assert that the physical Hilbert space is a tensor product, or that the first full-space charged excitation is a glueball. The physical gap can exceed the full-space lower bound.

The limiting state is gauge invariant because each finite-volume state is. In its GNS representation the closure generated by local gauge-invariant observables and the vacuum gives the vacuum physical sector. Restricting the gauge-commuting limiting generator retains its lower-gap bound. Nontrivial physical observables require their own nonzero variance; at the electric product point, an elementary Wilson loop has mean zero and second moment 1/4. The uniform local ground-state cluster expansion reviewed in the source Section 2 supplies continuity of fixed local expectations in the small perturbation regime; this additional input retains a nonzero Wilson variance after possibly shrinking that qualitative regime. This variance continuation is not inferred from the existence of a limit in Theorem 2 alone. No quasiparticle dispersion or isolated glueball assertion is inferred.

## 6. Why this advances the roadmap and where it stops

This supplies an actual Hamiltonian ground-state stability route at fixed spacing, rather than merely a stochastic generator or Gibbs functional inequality. It addresses part of the earlier NEXT-GROUND obligation in a sufficiently small interaction regime. It complements the locality estimate: locality handles finite-time propagation broadly, while this theorem needs a small static perturbation and controls the vacuum spectrum.

The continuum obstruction remains explicit. In the workbench convention,

\[
 \alpha(a)=\frac{g_H(a)^2}{2a},\qquad
 \lambda(a)=\frac{2}{g_H(a)^2a},\qquad
 \frac{\lambda(a)}{\alpha(a)}=\frac4{g_H(a)^4}.
\]

A weak-bare-coupling path g_H(a)→0 leaves every fixed small-κ* domain. The theorem gives no continuation of its gap estimate across that exit. It also does not construct a renormalized relativistic continuum observable family or identify a finite nonzero continuum mass. Choosing a different arbitrary g_H(a) to preserve the small ratio changes the proposed scaling path and does not complete the target.

## 7. Acceptance and next proof obligation

The source theorem and the blocking/Gauss restriction must be reviewed separately. Accept the applicability result only after checking the infinite-dimensional hypothesis, interaction range, boundary padding, units, gauge-invariant vacuum and existential threshold language. The next concrete improvement would be to extract an explicit conservative c₁,c₂ from the original expansion or another applicable constructive stability theorem. That is a new proof task; no finite numerical scan can supply it.
