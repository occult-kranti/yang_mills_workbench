# Exceptions, local dynamics and a controlled moment hierarchy

The strongest next step is to replace two global assumptions with local, testable statements. On connected gauge graphs, bounded plaquette interactions permit locality estimates even though each link has infinitely many electric representations. In the one-plaquette identity hierarchy, retaining variance and higher moments under positivity constraints permits rigorous outer bounds without guessing a closure. These are compatible methods for removing separate obstacles. They do not identify a real-time Hamiltonian state with a Euclidean Gibbs measure.

The official Yang–Mills existence and mass-gap problem remains unsolved. Its endpoint includes a nontrivial four-dimensional quantum field theory, the required axiomatic structure, and a positive finite physical spectral threshold. A finite model, a lower-dimensional theory, or an action with extra fields must be labelled by that changed scope. [Clay status](https://www.claymath.org/millennium/yang-mills-the-maths-gap/), [official formulation, Section 4](https://www.claymath.org/wp-content/uploads/2022/06/yangmills.pdf).

## 1. The inherited results and the two selected obligations

Round 12 establishes a controlled finite-graph result. In the two adjacent square model, degree flags reduce the electric operator, while trace multiplication changes degree by at most one. For a normalized initial state of degree at most d₀, the exact full-space and exact Galerkin evolutions obey

\[
 \|\psi(t)-\psi_D(t)\|\le
 \min\!\left(2,\frac{A(t)^{D-d_0+1}}{(D-d_0+1)!}\right),
 \qquad A(t)=\int_0^t\sum_p|\lambda_p(s)|\,ds .
\]

That theorem is specific to its established degree bandwidth and initial-state support. The exact rational two-segment fixture also controls the approximation algorithm, yielding a total state error below 0.000337501. None of its source hashes or historical acceptance statuses should change in this round.

The growing-box estimate from round 12 has an explicit volume-dependent factor. Its deterioration cannot decide whether the actual gap closes. Local dynamics offers a different observable and a different useful uniformity: a bounded observable deep inside a box should become insensitive to the remote boundary for a fixed finite time. This is obligation R13-L.

The failed point-concentration closure is equally specific. It deletes a strictly positive variance from an exact compact identity. Replacing it with a vector of constrained moments answers a more informative question: what interval of values is still compatible with a finite subset of the exact identities and positivity? This is obligation R13-M.

The full four-dimensional mass gap is not the acceptance criterion for either calculation. Each milestone should first deliver its own derivation, rejection controls and independently replayable evidence.

A further source audit found an applicable product-vacuum stability theorem. The accompanying weak-coupling-stability.md checks Yarotsky's infinite-dimensional hypotheses, the finite blocking of outgoing links, a precise boundary embedding and the Gauss restriction. It yields a qualitative volume-uniform Hamiltonian gap for sufficiently small static λ/α at fixed spacing. This is a stronger spectral route than locality alone, but it requires an additional smallness premise and supplies no evaluated coupling threshold. The updated roadmap records this as R13-Y; the broader ground-state and continuum obligations remain open. [Yarotsky, Theorems 1–3](https://arxiv.org/pdf/math-ph/0411042).

## 2. A change-of-variable contract

Classify every proposed addition before using it. A coordinate change can simplify a proof while preserving the model. An unknown expectation supplies missing information but needs further equations. A regulator or smearing scale defines an approximation. A new physical field or deformation changes the action and must eventually be removed or matched by an independently proved equivalence.

| Quantity | Meaning | Permitted inference | Required check |
|---|---|---|---|
| κ=λ/α | Dimensionless Hamiltonian coefficient ratio | Re-express a fixed action when α>0 | Recover α and physical time; never divide at α=0 |
| κ_E | One-plaquette Euclidean exponential tilt | Defines dμ proportional to exp(κ_E x) dHaar | Do not equate κ_E with λ(t) or a ground-state density |
| A(t) | Integrated absolute drive | Controls the existing representation-tail theorem | Signed cancellation cannot replace absolute values |
| J(t) | Uniform local plaquette strength bound | Controls a finite-time locality estimate | Must be uniform over graph size on the selected time interval |
| R and d(X,Y) | Boundary radius and interaction-support distance | Controls how many interaction steps can connect supports | Count link supports, not only plaquette-center distance |
| mₙ and v=m₂−m₁² | Moments and variance of a declared measure | Restores fluctuations omitted by scalar closure | Positivity, support and higher exact identities |
| r | Moment hierarchy order | Defines a nested outer approximation | All constraints from lower orders remain present |
| a, L=na | Spacing and physical box size | Labels a regulator path | Fix physical observables, embeddings and coupling matching |
| L_c and aₙ | Compactification circumference and deformation coefficients | Defines center-stabilized compactified Yang–Mills | Removing deformation/compactification requires a controlled bridge |
| τ_f | Positive gauge-field flow time | Defines smoothed observables | It is not real time and does not create a physical spectral gap |

The two selected branches meet at an operating rule rather than a common adjustable mass: the same support, measure or Hilbert space must occur on both sides of an implication. A shared symbol cannot identify different states or different limits.

## 3. Legitimate exceptions and scope-changing alternatives

### SU(2) has an exact trace simplification

For U,V in SU(2), Cayley–Hamilton gives V+V⁻¹=Tr(V)I. Therefore

\[
 \operatorname{Tr}U\operatorname{Tr}V
 =\operatorname{Tr}(UV)+\operatorname{Tr}(UV^{-1}).
\]

With normalized traces w(U)=Tr(U)/2 this becomes w(U)w(V)=[w(UV)+w(UV⁻¹)]/2. At the matrix level this reduces products of traces. Under expectation it reduces a double-trace observable to other loop observables; it does not factorize an expectation into a product of expectations. In particular, it does not set v=0.

Kazakov and Zheng exploit finite-N trace identities and positivity in their lattice bootstrap. SU(2) loop equations are linear on the appropriate single-trace loop space. The loop geometry remains unbounded, so reducing trace count does not close the hierarchy at a finite loop length. This is a useful exact exception, with explicit source normalization. [Finite-N bootstrap, v4, Sections 1–3](https://arxiv.org/html/2404.16925v4).

### Graph topology changes the available physical states

A finite tree with Gauss law imposed at every vertex and no external charge has only the constant physical state after tree gauge reduction. Removing cycles therefore removes the nontrivial excitations rather than proving a nontrivial mass gap. Adding charges or leaving boundary gauge transformations unconstrained changes this conclusion, because an open electric flux line can then be physical.

On a simple open hypercubic graph containing a square, any nonempty charge-free spin-network support must contain a cycle. Its minimum length is four; each nontrivial SU(2) link contributes Casimir at least 3/4, giving the free physical gap 3α under the round-12 normalization. Triangles, parallel edges or periodic identifications with short cycles require a revised constant. Their difference is an exact graph exception, not a contradiction of the square-graph theorem.

The locality theorem below does not need this free physical gap. Its input is local tensor support, bounded interactions and a bounded-degree graph. A topology change can invalidate the spectral constant without invalidating the locality framework. This separation is useful when choosing tests.

### Strong coupling and lower dimensions are useful controlled regimes

Shen, Zhu and Zhu establish infinite-lattice stochastic and Euclidean results for a specified strong-coupling region. Their SU(N) condition is |β_SZ|<1/[16(d−1)], with density proportional to exp(Nβ_SZ Σ ReTr U_p). In the standard Wilson convention β_W=N²β_SZ; for SU(2), d=4 this gives β_W<1/12. This fixed-spacing regime does not follow a weak-coupling continuum trajectory β_W→∞. [Original paper, definitions and main results](https://arxiv.org/pdf/2204.12737).

Two-dimensional Yang–Mills admits rigorous Wilson-loop constructions and a Euclidean/Hamiltonian comparison in specified geometries. Those are excellent benchmarks for a reconstruction algorithm, but the dimension changes the ultraviolet problem and the local degrees of freedom. [Ashtekar et al.](https://arxiv.org/abs/hep-th/9605128). The 2026 revision of the two-dimensional Langevin universality result covers the trivial bundle on a torus and connected compact groups. It does not supply a four-dimensional gap theorem. [Chevyrev and Shen, v3](https://arxiv.org/abs/2302.12160v3).

Three-dimensional stochastic constructions and renormalization results have further specific boundaries: local stochastic-time dynamics, gauge-covariant renormalization, and in one branch Higgs fields. The August 2026 Abelian scaling result is for U(1), with local-in-time convergence to a stochastic heat equation. These are technical lessons about consistent variables and renormalization, not replacements for the pure nonabelian four-dimensional endpoint. [3D Yang–Mills–Higgs](https://arxiv.org/abs/2201.03487v2), [gauge-covariant renormalization](https://arxiv.org/abs/2503.03060v2), [Abelian scaling](https://arxiv.org/abs/2608.27828v1).

### Compactification can improve calculability while changing the task

A concrete extension on R³×S¹ is

\[
 S_{\rm def}=S_{\rm YM}
 +\int_{\mathbb R^3}\frac{d^3x}{L_c^3}
   \sum_{n=1}^{\lfloor N/2\rfloor}a_n
   |\operatorname{Tr}\Omega(x)^n|^2,
\]

where Ω is the circle holonomy. Ünsal and Yaffe use positive deformation coefficients to preserve center symmetry and develop a controlled small-circle semiclassical description. Their large-N volume-independence argument has symmetry and limit conditions; finite-N small-circle calculations do not by themselves prove the undeformed R⁴ result. A proposed reverse route must control removing the deformation, decompactifying, the approximation remainder and the physical spectrum throughout. [Original action and analysis, Sections 2–3](https://arxiv.org/pdf/0803.0344).

An auxiliary field introduced by an exact integral identity can preserve a theory if integrating it out reproduces the original measure, normalization and observables. A new Higgs field, Proca mass or arbitrary gauge-kinetic function generally does not. A positive flow time is another legitimate tool: it smooths the gauge field and defines useful observables, but it is not a new physical mass parameter. [Wilson flow](https://arxiv.org/abs/1006.4518).

## 4. Milestone R13-L: connected-graph local dynamics

### Model and support

Work first on the unreduced tensor product

\[
 \mathcal H_\Lambda=\bigotimes_{\ell\in E(\Lambda)}L^2(SU(2),dU_\ell),
 \qquad
 H_\Lambda=\sum_\ell\alpha_\ell C_\ell
       +\sum_{p\subset\Lambda}\lambda_p(1-W_p),
\]

where C_ℓ is the positive link Casimir, α_ℓ≥0 is fixed, W_p=ReTr(U_p)/2 is bounded by one, and each plaquette uses four link factors. Fix a bounded local gauge-invariant observable O_X. A later restriction to the physical invariant sector is valid because the electric and plaquette terms commute with all local gauge transformations. Do not assume the gauge-invariant Hilbert space factorizes over links.

Remove the scalar Σ_pλ_p from the Heisenberg calculation; it has no commutator effect. The interaction Φ_p=−λ_pW_p has norm at most |λ_p|. This factor matters: bounding λ_p(1−W_p) directly gives 2|λ_p| and a weaker constant, while silently mixing the two conventions creates a factor-of-two error.

For a fixed finite graph the on-link electric sum is self-adjoint on its natural tensor-product core and has a self-adjoint closure. Adding a bounded finite plaquette sum preserves self-adjointness. Use its unitary free propagator to form

\[
 \widetilde\Phi_p(t)=e^{itH_0}\Phi_p e^{-itH_0}.
\]

This preserves both the support of p and the interaction norm. The unbounded electric spectrum does not appear in the norm of the interlink interaction. It must still remain in the propagator and in actual trajectories.

This scope is supported by Nachtergaele, Sims and Young: their interaction-picture framework explicitly permits unbounded self-adjoint on-site terms and strongly continuous bounded interactions. The local sites in this application are links. Their Sections 3.2–3.3 give locality and volume-comparison statements under a summable interaction norm. [NSY, v2](https://arxiv.org/html/1810.02428v2#S3.SS2).

### Forward route

1. Identify the four-link support of every plaquette and the maximum incidence q of plaquettes at a link. A d_s-dimensional simple hypercubic lattice has q≤2(d_s−1).
2. Pass to the interaction picture without truncating the electric spectrum.
3. Bound a commutator recursively by commutators with interacting plaquettes.
4. Each nonzero term is a chain of overlapping supports from X to Y. If no chain of length below R exists, those Taylor orders vanish identically.
5. Bound the number of next supports by a graph-independent degree constant and integrate the ordered time simplex, producing a factorial denominator.
6. Apply Duhamel only to interactions omitted at the boundary. Sum boundary shells with their actual growth bound.
7. Obtain an operator-norm Cauchy estimate for the evolution of a fixed bounded local observable as the boundary recedes, uniformly over a fixed compact time interval.

The implementation must select and verify its own explicit constants, distance convention and boundary counting. A schematic exponentially small light-cone tail is not an executable certificate. A term that includes the total volume defeats the intended milestone unless a subsequent summation removes that dependence.

### Backward route

Suppose the target is a tolerance ε for the boundary effect on O_X at time T. Work backward from a sufficient locality inequality to the required radius R, interaction envelope J, incidence bound q and distance definition. Then verify forward that the actual graph and coefficients satisfy those same hypotheses. A chosen R is an algorithmic resource; it does not change the target action.

Next separate any representation and time-integration errors inside that local region. Round 12 supplies one two-square representation theorem, not a ready-made certificate for every larger subgraph. The local theorem can certify removal of a distant boundary even when a specific simulation of the retained region still has numerical error.

### Mandatory rejection tests

Test zero interaction, zero time, disjoint components, adjacent and overlapping observable supports, a graph with an omitted shared link, negative coefficients handled by absolute values, a nonuniform but bounded coupling profile, and reversed time. Test the distance-zero branch directly: a formula beginning at a positive path length cannot bound an already overlapping commutator.

Do not infer that arbitrary electric energy observables are covered: C_ℓ is unbounded. Do not infer that the limiting dynamics is norm-continuous on the entire algebra B(L²(SU(2))). The free unbounded generator can already violate that continuity. Strong continuity in an appropriate representation and norm convergence with growing regions are different claims.

Finally, finite propagation does not imply a spectral gap. A system can have local, even noninteracting dynamics and arbitrarily small excitation energies. Taking lattice spacing to zero changes the couplings and converts link distance to physical distance; a fixed-spacing propagation constant need not remain uniformly useful in that limit.

## 5. Milestone R13-M: exact moment constraints

### The declared measure

For finite real κ, take the one-plaquette measure

\[
 d\mu_\kappa(x)=Z_\kappa^{-1}e^{\kappa x}
       \frac{2}{\pi}\sqrt{1-x^2}\,dx,
 \quad -1\le x\le1,
 \quad m_n=\int x^n\,d\mu_\kappa.
\]

The compact integration identity is

\[
 n m_{n-1}-(n+3)m_{n+1}
       +\kappa(m_n-m_{n+2})=0. \tag{M1}
\]

At n=0, omit the negative-index term. For κ≠0, this expresses every higher moment as an affine function of u=m₁, starting with m₀=1. For κ=0 use the recurrence directly; division by κ is invalid. The Haar values are odd moments zero and m₂r=Catalan(r)/4ʳ.

At κ=1, a minimal formula check is

\[
 m_2=1-3u,\quad m_3=13u-3,\quad
 m_4=16-66u.
\]

These are algebraic checks of the recurrence, not a solution for u. Large cancellations make exact rational arithmetic useful at increasing order.

### Necessary moment and support matrices

At hierarchy order r≥1 retain m₀,…,m₂r and impose

\[
 M_r=(m_{i+j})_{i,j=0}^r\succeq0,\qquad
 L_{r-1}=(m_{i+j}-m_{i+j+2})_{i,j=0}^{r-1}\succeq0. \tag{M2}
\]

For a polynomial p of degree at most r, the first condition is E[p(x)²]≥0. The second is E[(1−x²)q(x)²]≥0 for degree(q)≤r−1. Both follow from the actual measure. Add all instances of M1 involving retained moments. For κ≠0, n=0,…,2r−2 suffices to generate them. At κ=0 the vanishing highest coefficient permits a separate direct Haar branch.

A rational vector c giving cᵀM_r(u)c<0 or cᵀL_{r−1}(u)c<0 is a rigorous exclusion certificate. If the expression is affine in u, its exact sign and slope identify an entire excluded half-line. Rational dual matrices that are exactly positive semidefinite provide another certificate format. Floating eigenvalues or solver tolerances alone do not certify either feasibility or exclusion.

Nested feasible sets provide outer mean intervals [l_r,h_r]. A finite feasible vector may correspond to many measures and is not automatically the particular Gibbs measure. The claim accepted at finite order is containment of the true moment, not equality with a floating candidate.

### Variance bounds and parameter edges

For κ≠0, M1 gives the exact identity

\[
 v=m_2-m_1^2=1-\frac{3u}{\kappa}-u^2. \tag{M3}
\]

Bound this polynomial over the entire certified interval, including its stationary point if present. Evaluating only the two endpoints can miss its maximum. For negative κ use parity m_n(−κ)=(−1)^n m_n(κ), while variance is even. At κ=0, v=1/4 exactly.

Independent checks should include the known analytic lower floor v≥e^(−2|κ|)/4, exact positive series with rational remainder bounds, or separately certified quadrature. Such a comparison tests whether the interval contains a independently derived answer. It does not turn the numerical mean into a proof of continuum physics.

### An exact scalar equation exists in coupling space

There is a useful exception to the need for a guessed algebraic closure. The family μκ is already constructed and differentiable in κ: compact support justifies differentiation under its integral on every bounded κ interval. Differentiating the normalized expectation gives

\[
 \frac{du}{d\kappa}=\langle x^2\rangle_\kappa
       -\langle x\rangle_\kappa^2=v>0. \tag{M3a}
\]

Combining this susceptibility identity with M1 gives the exact coupling-space equation

\[
 \kappa u'(\kappa)+3u(\kappa)
       =\kappa[1-u(\kappa)^2],
 \qquad u(0)=0,\quad u'(0)=\tfrac14 . \tag{M3b}
\]

Its regular solution begins u(κ)=κ/4−κ³/96+O(κ⁵). At zero, use the regular branch and the derivative condition, not the divided formula with 3u/κ. At negative coupling use odd parity. The positive variance makes u strictly increasing at every finite real κ; the susceptibility is a measure-specific fluctuation observable.

This is a complete scalar relation for the one-plaquette mean as a function of its external Euclidean coupling. It works because differentiating the known exponential family carries the missing fluctuations. It neither eliminates fluctuations nor supplies a real-time Hamiltonian equation or a physical glueball mass. A numerical solution of M3b still requires its own integration and initial-series error control before it can be called a certificate.

### Why the complete hierarchy determines this measure

The following mathematical extension is derived here for the declared compact scalar measure and should receive independent review before promotion. Assume an infinite sequence with m₀=1 satisfies M1 for every n and M2 for every r. Positivity and the compact-support moment theorem produce a probability measure μ supported on [−1,1].

Polynomial insertions in M1 give E[(1−x²)f′]=E[(3x−κ(1−x²))f]. Approximate a continuous f′ uniformly by polynomials and integrate to extend this equality to all C¹ functions f. In the sense of distributions,

\[
 D[(1-x^2)\mu]=[\kappa(1-x^2)-3x]\mu. \tag{M4}
\]

On (−1,1), write ν=(1−x²)μ. Since ν′=[κ−3x/(1−x²)]ν, its density is proportional to e^(κx)(1−x²)^(3/2). Dividing by 1−x² gives the required interior density e^(κx)√(1−x²). An endpoint atom contributes nothing to (1−x²)μ but a nonzero atom to the right side of M4, so no endpoint atoms are allowed. Normalization fixes the remaining constant.

This also gives convergence of the nested outer mean intervals without a rate. Diagonal entries of M2 and L bound even moments between zero and one; Cauchy–Schwarz bounds odd moments. From any sequence of feasible truncated vectors at increasing orders, extract a diagonal convergent subsequence. Its limit obeys every positivity and recurrence constraint and hence is the unique moment sequence above. If either endpoint of the nested mean intervals stayed separated from the true mean, it would yield a contradictory limiting sequence.

This proof does not establish a useful rate, nor validate every finite floating optimization. It explains why increasing constraints is a principled replacement for setting missing moments by hand. Extending the construction to loops on an interacting lattice requires the correct shared-link identities and a much larger positivity family.

The convergence statement concerns the full feasible intervals. A particular algorithm may search only a finite set of witness polynomials and return wider intervals. Its outputs inherit convergence only if they approach those full intervals with a certified vanishing optimization slack. The current implementation contract proposes exact signed dual witnesses and positive-semidefinite inner points with a per-side slack at most 2/2ᵇ. When those certificates successfully replay, taking hierarchy order r and precision b to infinity connects its reported enclosures to the mathematical limit. No claim is made that the algorithm necessarily succeeds for every r, κ or resource budget.

For precise quantifiers, this last implication requires a sequence of successfully certified levels rⱼ→∞ and errors εⱼ→0 at one fixed finite real κ. An implementation that supports only r≤6 does not establish such a sequence. Its successful finite certificates remain valid outer bounds. The all-order premise includes normalization m₀=1 explicitly; the zero sequence satisfies the homogeneous recurrence and matrix inequalities but cannot be admitted as a probability measure.

## 6. Connecting both directions without assuming the missing theorem

The local-dynamics branch proceeds from local Hilbert factors and bounded interactions to a volume limit for selected bounded observables. Backward from a continuum mass gap, that helps only after identifying a limiting vacuum state, positive generator and physical scale. The moment branch proceeds from an exact measure to identities and certified static observable intervals. Backward from reconstructed correlations, it would need space-time insertions, reflection positivity, convergence of the relevant observable family and a decay rate in physical units.

There is no reviewed implication from “local dynamics exists” plus “one-plaquette moments are determined” to “four-dimensional Yang–Mills has a gap.” They concern different sectors of the construction. A proof planner must leave that target unreachable when these are its only new premises.

The rule inventory carries its locality hypotheses explicitly: one common locally integrable absolute interaction envelope, identical shared on-link generators and retained interaction coefficients, a fixed finite bounded observable support, and a nested exhaustive region family whose omitted-boundary distance tends to infinity. A merely summable function on one fixed region does not establish a volume limit. These are prerequisites to the route rather than consequences of naming its final estimate.

The useful meeting variables are explicit: the same lattice spacing a, the same geometry, an actually matched transfer or Hamiltonian normalization, and the same renormalized observable family. Each may eventually become a sequence or a function, but its values must be constrained by the theory rather than selected to force a positive answer.

## 7. Updated experiments and acceptance gates

| Experiment | Hypothesis | Discriminating result | Status before independent replay |
|---|---|---|---|
| L1: interaction support | Unbounded link terms preserve support in the interaction picture | Remove one shared-link incidence; the wrong path count is rejected | Planned implementation |
| L2: boundary radius | A fixed local bounded observable has vanishing remote-boundary error | Increasing R improves a certified tail at fixed T and J, without total-volume growth | Planned derivation and tests |
| L3: disconnected control | No interaction chain gives exactly zero influence | A nonzero predicted transfer on disconnected supports is rejected | Planned negative control |
| L4: scale control | Fixed-spacing locality does not give a uniform continuum velocity | Substitute α(a),λ(a), physical R=a r and retain the exposed a dependence | Planned diagnostic |
| M1: rational hierarchy | More exact positivity constraints narrow an outer mean interval | Exact exclusion certificates replay at held-out κ and order | Planned implementation |
| M2: variance | Nonzero fluctuation is compatible with all retained equations | Interval propagation includes the true v and rejects point closure | Planned independent comparison |
| M3: zero/sign edges | κ=0 and κ<0 are valid separate cases | Haar branch and parity hold without division by zero | Planned edge tests |
| M4: full hierarchy | All orders determine the compact measure uniquely | Independent critic checks M4, endpoint atoms and compactness | Derived, review pending |
| P1: proof replay | Only supplied mathematical implications are traversed | Removing positivity, locality hypotheses or physical-scale matching blocks dependent targets | Planned integration |

Once the concrete acceptance questions have been answered, preserve all attempted cases and update the roadmap. Additional parameter scans should resolve a named remaining uncertainty. They should not be represented as exhausting infinitely many possible methods.

## 8. Source and process corrections

The strongest source-level lesson is to use the equation and its assumptions together. The explanatory sentence after NSY Eq. (3.69) says the boundary estimate improves at a small distance to the omitted region. The displayed summable, decaying F-tail instead improves as that distance grows. This appears to be a local prose typo; it does not invalidate the inequality or its proof. The implementation should test monotonicity against the inequality. [NSY, Section 3.3](https://arxiv.org/html/1810.02428v2#S3.SS3).

Use arXiv submission histories for versions. An experimental HTML rendering date is not a new mathematical version. The latest finite-N bootstrap version checked here is v4, dated December 4, 2024. The NSY mathematical version checked is v2, dated March 1, 2019, even though its HTML shows a later rendering date.

This is a targeted primary-source review. The full proofs of the long lower-dimensional SPDE papers were not audited; those records are used only for their explicit scope. Numerical result acceptance remains the responsibility of independent executable checks bound to the final source bytes. No external researcher is represented as having reviewed this project.

## References

The accompanying sources.json records exact URLs, mathematical versions, sections read, provenance and limitations. Primary sources are cited inline at the claim they support. Original derivations and scope deductions in this document are distinguished from those source statements; no novelty claim is made for established locality or moment methods.
