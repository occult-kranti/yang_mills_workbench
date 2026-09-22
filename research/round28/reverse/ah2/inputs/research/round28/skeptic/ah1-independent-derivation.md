# AH1 independent skeptic: complete 561-state enrichment and all-time heat certificate

This derivation and new checker were produced under the frozen AH1 contract, before reading either current producer's science. The graph is reconstructed from its coordinates, and all new counts, metric entries and bounds are computed from that reconstruction. Historical reports provide named mathematical context; no historical checker is imported or executed. The Newton and Tesla methods motivate reconstructing the actual observable and charging every omitted channel, not an endorsement by historical people.

The result is a **561-dimensional** physical enrichment with a positive diagonal Gram, a complete exact sparse magnetic matrix, a simultaneous outside-map envelope and an all-time true-relative heat error below **0.0022** for the contracted preparation class. The executed rational bound is approximately `0.002159617722188484`. This is a theorem about the exact retained semigroup; no numerical heat evaluator or exact enriched ground diagonalization is claimed.

## 1. Full graph, gauge actions and electric cutoff

Vertices are lexicographic triples in `{0,1,2,3} x {0,1,2} x {0,1}`. A positively oriented link is labeled by its tail and axis; a face is labeled by its lexicographic anchor and ordered axes `a<b`. Its word is

`U(v,a) U(v+ea,b) U(v+eb,a)^-1 U(v,b)^-1`.

The checker constructs all 24 vertices, 46 links and 29 faces, including every internal face. Connectivity gives cycle rank `46-24+1=23`. All original link variables remain. At each of the 24 vertices, including boundary vertices, the gauge action is `Ue -> g_tail Ue g_head^-1`. Trace words are invariant by telescoping conjugation. An exact noncommuting rational quaternion fixture checks every face and detects both a missing inverse in its word and a wrong head-vertex Gauss action. Neither tree-coordinate deletion nor a naive sum of independent-cycle Casimirs supplies the electric operator: a four-link fundamental face costs `4*(3/4)=3`, not `3/4`.

The physical Hilbert space is the closed invariant subspace of normalized product Haar `L2(SU(2)^46)`. Peter-Weyl edge labels have electric energies `j_e(j_e+1)`; left/right translations preserve each label block, so all Gauss averaging commutes with `K=sum_e C_e`. The invariant spin tensors select the physical part of those finite blocks. There are finitely many blocks and finite multiplicities below any electric energy bound, hence the physical K has compact resolvent. Its operator domain is the square-summability domain weighted by total energy squared, equivalently the invariant product `H2` space; its form domain uses one energy weight, equivalently invariant `H1`. Finite invariant Peter-Weyl sums are a smooth core.

Set `S=sum_p Wp`, `Wp=Tr(U_boundary(p))/2`, `L=K+lambda(29-S)`. Since `-29<=S<=29`, the real smooth gauge-invariant multiplier `29-S` is between zero and 58. Thus for the declared nonnegative coupling, `L>=K>=0`; bounded perturbation gives `D(L)=D(K)`, the same form domain, smooth invariant core and compact resolvent. The positive physical factors are fixed: `H=alpha L`, `sigma=alpha t/hbar`. This is a new finite uniform-coupling graph, not the canonical summable or homogeneous model.

A nontrivial invariant support cannot have a degree-one active vertex: a single nonzero irreducible representation has no invariant tensor. Every active edge costs at least `3/4`. Below the strict cutoff `9/2`, there are at most five active edges. The graph is simple bipartite and has girth four. A nonempty minimum-degree-two support must contain a cycle. With at most five edges it has just one component. If it has four vertices, bipartiteness permits at most four edges; if it has five vertices and five edges, every degree is two and it would be an impossible odd five-cycle. Fewer vertices cannot contain a bipartite cycle. Consequently the support is one four-cycle. The checker independently finds every four-cycle from pairs of common graph neighbors and proves that the resulting set equals exactly the 29 elementary faces.

At each degree-two vertex the invariant tensor forces the two edge spins to agree and is unique up to scale. Therefore a four-cycle has one common spin j and energy `4j(j+1)`. The strict cutoff selects only `j=1/2`, whose normalized function is `phi_p=Tr(U_boundary(p))=2Wp`. The only zero-energy state is the constant vacuum Omega. Hence

`P0=1_[0,9/2)(K)=span{Omega,phi_0,...,phi_28}`,

with rank 30, unique electric vacuum and exact full physical electric gap 3. An actual perimeter of two adjacent coplanar faces has six fundamental edges and energy exactly `9/2`; its normalized character is a counterexample to replacing the strict endpoint by an inclusive one. The later enrichment may include that state, but the initial projection does not.

## 2. Individually resolved actual functions and Haar Gram

Unordered pairs always use `p<q`. The new graph has 406 such pairs: **96 share one edge and 310 share no edge**. The second group includes pairs that meet only at a vertex; their product vectors remain actual eigenvectors even when the surrounding ambient electric shell has other intertwiners. Distinct faces share at most one edge, as checked for every pair.

For one face put `c_p=phi_p^2-1`, its spin-one character. For a pair put `eta_pq=phi_p phi_q`. If their edge sets are disjoint, define `d_pq=eta_pq`. If they share an edge, let `E0` be Haar averaging in that common original link. It commutes with both endpoint gauge actions. Since `1/2 tensor 1/2=0 direct-sum 1`, the two exact generated branches are

`s_pq=2 E0 eta_pq`, `t_pq=2(eta_pq-E0 eta_pq)`.

These definitions retain orientation and intertwiner information as actual polynomial functions. For a reversed shared orientation one uses the corresponding inverse path; the character is real and invariant under reversing its entire closed loop. No fit or arbitrary vector within an ambient degenerate shell replaces these functions.

The checker independently computes the local Haar identity with three independent unit quaternions G,A,B. Expanding `eta=chi(AG)chi(G^-1 B)` as a sparse polynomial and integrating G by exact sphere moments gives `E_G eta=chi(AB)/2`. The moment rule on the four real quaternion coordinates is zero for any odd exponent and, for exponents `2n_i`, equals

`prod_i (2n_i-1)!! / prod_(r=0)^(sum n_i-1) (4+2r)`.

Full exact integration gives `||eta||^2=1`, `||E0 eta||^2=1/4`, `||eta-E0 eta||^2=3/4`, and zero singlet/triplet cross term. Thus s and t have metrics 1 and 3, respectively. This calculation does not assume shared face holonomies are jointly independent. Edge-disjoint products have norm one by independence of their original edge variables, even when vertices touch. Fundamental and spin-one characters each have norm one.

The complete candidate list is:

| Actual function | Count | Norm squared | Electric energy |
|---|---:|---:|---:|
| Omega | 1 | 1 | 0 |
| phi_p | 29 | 1 | 3 |
| c_p | 29 | 1 | 8 |
| d_pq | 310 | 1 | 6 |
| s_pq | 96 | 1 | 9/2 |
| t_pq | 96 | 3 | 13/2 |

Every pair mask is the XOR of its two face edge masks. The checker enumerates all 406 masks and verifies that they are distinct, nonzero and unequal to every single-face mask. Individual edge-center translations are Haar preserving. These masks therefore prove orthogonality between different pairs and the original odd face sector. They also separate pair states from vacuum and the integer-spin face characters. Two branches of the same pair are orthogonal by their distinct K eigenvalues. Distinct spin-one characters have different nontrivial representation supports and are orthogonal by Peter-Weyl orthogonality, even though their center masks are all zero. The vacuum is a separate representation support.

The exact candidate Gram is consequently diagonal, with 96 entries equal to three and all others one. It has no kernel, and the quotient rank is **561**. The code exports every individual representation support, electric eigenvalue and Gram weight. Each shared singlet has six fundamental edges; each triplet adds a spin-one shared edge. This proves that P+ reduces K and preserves its operator/form domains. P+ is complete for the specified individually resolved generated span. It is not the complete ambient electric-energy shell, and a K-cyclic closure of summed columns need not separate individual degenerate channels.

A deliberate duplicate-description control creates Gram `[[1,1],[1,1]]` and null vector `(1,-1)`. The corresponding electric and magnetic columns annihilate that null vector, whereas replacing the Gram by the identity would lose the relation. Thus an empty kernel in the actual graph is an executed result, not a convention that would suppress dependencies if they occurred.

## 3. Every retained magnetic column and the full outside map

Assign central link signs `+1` on x links, `(-1)^x` on y links and `(-1)^(x+y)` on z links. The checker verifies that their product is negative on every oriented face. This Haar-preserving transformation commutes with gauge averaging and K and sends `S -> -S`. Vacuum and every quadratic generated function are even; phi faces are odd. Consequently every magnetic matrix element within either parity class is exactly zero. A uniform flip of all links instead leaves each square even and fails this purpose. Global parity alone does not establish pair-mask independence; the separate exhaustive masks and representation arguments above are essential.

The remaining complete action follows from the pointwise identities

`S Omega=(1/2)sum_p phi_p`,

`S phi_p=(1/2)Omega+(1/2)c_p +(1/2)sum_(q edge-disjoint) d_pq +(1/4)sum_(q shared-edge)(s_pq+t_pq)`.

These identities include every term in the original 29-face multiplier. They are not only the bright summed column. In the stated physical coefficient Gram, self-adjointness fixes each reverse entry: `G_i S_ij=G_j S_ji`. In particular the triplet-to-face coefficient is `3/4`, while the face-to-triplet coefficient is `1/4`. Metric-blind ordinary transposition is wrong. This, together with the proved same-parity zeros, determines the entire `P+ S P+` matrix, including all nonvacuum columns. The output stores its complete sparse entries; every unlisted entry is an explicitly proved structural zero. The action of L is the stored diagonal K plus `lambda(29 I-S)`.

On the full physical space define

`B=(I-P+) L P+=-lambda(I-P+) S P+`.

K reduction and the complete old columns prove **BP0=0**. Orthogonal projections in the physical Gram and `||S||<=29` give the simultaneous bound **`||B||<=29lambda`** on every retained input and every coherent combination. This charges all new-input leakage and all unretained intertwiners. It is not a collection of separate column bounds combined without correlations and not an exact cubic outside Gram.

The full map is nonzero for positive lambda. The normalized same-face spin-3/2 character `xi_p=phi_p^3-2phi_p` has energy 15 and lies outside P+. The exact Haar checker verifies

`<xi_p, S c_p>=1/2`.

The same-face term follows from character multiplication; other face terms have the wrong individual edge-center mask. Therefore `||B c_p||>=lambda/2`. This is a concrete new-input channel refuting B=0 while BP0=0 remains exact. The lambda=0 case is handled separately.

## 4. Original Ritz state, full residual and two nested projector bounds

Let m=29, c=m lambda and

`D0=sqrt(9+m lambda^2)`, `w=(D0-3)/2`,
`h=lambda/[2(3+w)]`, `Z=1+m h^2`,
`f0=(Omega+h sum_p phi_p)/sqrt(Z)`, `mu0=c-w`.

The complete P0 compression is a star: vacuum diagonal c, face diagonals `3+c`, and vacuum/face couplings `-lambda/2`. Its bright two-dimensional block has the displayed simple ground; the other 28 face directions have eigenvalue `3+c`. The checker independently verifies the exact bright equations in the quadratic number field `w^2+3w=m lambda^2/4`, and encloses the actual cap radical and residual by directed rational intervals. At lambda=0, h=w=0 and f0=Omega, without division by lambda.

Put `F=S^2-m/4`. The full residual is

`(L-mu0)f0=-(2lambda h/sqrt(Z))F`.

The complete original-source Gram, reconstructed from every resolved magnetic column, is diagonal `m/4` with off-diagonal `1/4`; equivalently it is `((m-1)/4)I+(1/4)J`. It gives `||F||^2=m(2m-1)/16=1653/16`. The same norm follows from the exact Haar fourth moment and pair masks. The complete F electric weights are

`m/16` at energy 8, `310/4` at energy 6, `96/16` at energy 9/2 and `3*96/16` at energy 13/2.

They sum to `1653/16`; their first energy moment is `m(3m-1)/4`. Dropping either shared branch strictly undercounts an actual old-source norm. Thus the exact full residual norm obeys

`rho0^2=m(2m-1)lambda^2 h^2/(4Z)`.

Since `h<=lambda/6`, `Z>=1` and `sqrt(1653)<41`, the uniform envelope is `r0=(41/12)Lambda^2`, with `Lambda=1/100`.

Before any residual inference, positivity and min-max show

`0<=epsilon<=mu+<=mu0<=29lambda<3`,

and second eigenvalues of full L, A0 and A+ are at least 3. Indeed K has one eigenvalue below 3 and the vacuum trial energy is below 3. Compactness then supplies actual simple isolated ground projections G, G0 and G+. Negative lambda would invalidate this nonnegative-potential argument. Define `g=3-29Lambda=271/100`.

There are **two separate p0 estimates**. In the full spectral measure of f0, excited energies differ from mu0 by at least `3-mu0>=g`, so

`||G-G0||=||(I-G)f0||<=rho0/g<=p0:=r0/g`.

Because BP0=0, `Lf0` is completely retained in P+. The residual of f0 in A+ is therefore exactly the same full residual, not merely bounded by an old selected part. The independently isolated A+ spectral measure yields

`||G+-G0||=||(I-G+)f0||<=rho0/g<=p0`.

Now `B G0=0`. For a normalized exact enriched ground f+,

`rho+=||(L-mu+)f+||=||B f+||<=29Lambda||(I-G0)f+||<=r+:=29Lambda p0`.

This is the extra residual factor from nesting; it would be unjustified without the second p0 estimate. The full excited spectral measure of f+ gives

`||G-G+||<=p+:=r+/g`.

It also gives the energy enclosure. Since the spectrum is epsilon or at least 3, `(L-epsilon)(L-3)` is nonnegative spectrally, and its expectation in f+ is `rho+^2-(mu+-epsilon)(3-mu+)`. Therefore

`0<=mu+-epsilon<=d+:=r+^2/g`.

All r/p/d symbols here are explicit uniform upper envelopes. They are not evaluated actual norms or exact enriched ground data. No square-root-of-two vector-distance loss is needed in `B G0=0`; the projector angle supplies the needed component directly.

## 5. Actual own-ground centers, true denominator and all real times

Let x be any normalized complex vector in P0 with `||x-Omega||<=eta=1/100`. From `h<=Lambda/6` and `1/sqrt(1+y)>=1-y/2`, define

`z0=1-29Lambda^2/72 <= |<f0,Omega>|`,
`q0=(11/12)Lambda >= ||(I-G0)Omega||`.

The latter uses `sqrt(29)<11/2`. Both p0 bounds imply

`||(I-G)x||, ||(I-G+)x|| <= b:=q0+p0+eta`.

For the exact full centered heat `E(sigma)=exp[-sigma(L-epsilon)]`, its stationary ground component yields the true denominator

`||E(sigma)x||>=||Gx||>=D:=z0-eta-p0>0`.

This lower bound concerns the actual output, not a Ritz vector norm or a reference-vacuum expectation. Triangle inequalities are valid for arbitrary complex x; real positivity of coefficients is not imposed. Rational normalized one-face real and imaginary preparations are checked explicitly. Outside the declared retained preparation class, initial truncation error would need an additional budget; at zero time the full-input operator-norm error of a zero-extended finite projection is one.

Set `E+(sigma)=exp[-sigma(A+-mu+)]P+`. It uses its own actual ground energy, independently from epsilon. Differentiating `E(t-s)E+(s)x` on the common smooth retained domain and integrating vectorwise gives

`(E(t)-E+(t))x=-int_0^t E(t-s)[B+(mu+-epsilon)P+]E+(s)x ds`.

Finite retained vectors are smooth, their retained evolution is smooth and their L-images are continuous. These facts justify the strong integral; no unbounded operator-norm derivative is assumed. The plus centering term inside the defect survives BP0=0. A scalar reference c differs from the interacting ground since `epsilon<=mu0<c` for positive lambda. An independently rounded center would alter a stationary ground mode by an exponential factor over long times. Such replacements are explicitly outside this theorem.

Contraction and the complete retained ground/excited decomposition give the early bound

`V(t)=(r+ + d+)t+(29Lambda)b(1-exp(-g t))/g`.

Indeed the retained ground part contributes at most r+ to the outside derivative, its complete excited part contributes at most `29Lambda b exp(-g s)`, and the actual scalar center difference contributes at most d+. Nothing assumes P0 evolves autonomously.

Independently, the full and retained spectral decompositions give the late bound

`J(t)=p+ +(2b+p+)exp(-g t)`.

The extra `p+ exp(-g t)` is harmless conservative slack; the two p0 bounds already control both excited components by b. V is increasing and J is decreasing. At the predeclared join T=2, exact arithmetic uses

`V(2)<=2(r+ + d+)+(29Lambda)b/g`,

`J(2)<p+ +(2b+p+)/200`.

The exponential inequality follows from an executed positive 18-term rational Taylor lower sum proving `exp(2g)>200`. Thus every real `sigma>=0` and every real `0<=lambda<=Lambda` obeys

`||E(sigma)x-E+(sigma)x|| / ||E(sigma)x|| <= max(Vbar(2),Jbar(2))/D < 11/5000`.

The authoritative exact fraction is in `heat_certificate/all_time_true_relative_upper`; its decimal is about `0.002159617722188484`. The same numerator is an all-time absolute bound. This is worse than the old graph's `0.000037` guarantee, which is not imported. All continuous-coupling and all-time quantifiers come from the preceding inequalities and spectral arguments, not a sample grid. At zero coupling both exact centered heats agree on the declared retained inputs because K reduces the space; at zero time both act identically on x. These exact zero-error identities supersede slack envelope values.

## 6. Evidence and limits

The standalone standard-library checker reconstructs the graph, oriented words, complete pair masks, exact conditional Haar calculation, all physical basis labels, representation supports, positive Gram, full sparse magnetic action, source residual Gram and spectral weights. It executes discriminating wrong-orientation/Gauss, missing-internal-face, strict-endpoint, missing-branch, metric, duplicate-null, parity, new-input leakage, negative-coupling, old-constant, complex-preparation and center-shift controls. Algebraic controls are not additional physical investigations. No historical checker executes or imports into the new algorithm.

All 42 contract sources plus applicable instructions and method snapshots were copied before production. The reading record distinguishes complete current derivation sources from limited inherited passages and metadata-only bindings. Normal and optimized runs produce identical exact output; the independent freeze binds the report, checker, output and source records before current producer exchange.

The accepted independent scope is this graph's strict initial electric projection, the individually resolved generated enrichment, its exact metric and generator, simultaneous full outside envelope, improved enriched residual bound and conservative all-time true-relative **heat** certificate for the declared preparation class and fixed physical scales. The entire outside cubic Gram, exact enriched ground, numerical heat evaluation, real-time relative control, graph-size uniformity, broader representation-cutoff completeness, canonical/homogeneous matching and a continuum Yang-Mills gap remain unproved. Priority is unverified. AH2 and later goals are unselected by this skeptic; this is only the authorized AH1 independent derivation.
