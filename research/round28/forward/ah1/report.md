# AH1 forward: complete physical graph extension and conservative heat certificate

Independent forward model-agent production under the frozen AH1 contract. Current reverse AH1 and current skeptical science were not read before this report and checker froze. Shared inherited mathematical premises are not independent physical observations. Newton's reconstruction discipline is used to identify the full state, domain and error; Tesla's loading discipline keeps all fusion branches and every outside column; the Penrose-method lens organizes exact representation and Gram data. No historical-person endorsement or historical analogy enters a proof.

The new open `3 x 2 x 1`-cell graph has **24 vertices, 46 links and 29 faces**. Its strict electric projection has rank **30**. The specified individual-channel enrichment has rank **561**, positive diagonal Haar Gram, and **2,124** nonzero retained magnetic matrix entries. The mathematical exact, independently ground-centered retained heat obeys

`sup_sigma>=0 ||(E(sigma)-E+(sigma))x||/||E(sigma)x||`
`<=3063228992521/1418412601938100 < 0.0022`

for every `0<=lambda<=1/100` and every normalized complex original `P0` input with `||x-Omega||<=1/100`. This is a conservative upper certificate, not an observed error; it is weaker than the old graph's sharper AC2 certificate. No numerical heat exponential is claimed. The complete outside map is bounded rather than expanded into its full cubic Gram.

## 1. Actual geometry, gauge action and closed operators

Vertices are integer triples in `{0,1,2,3} x {0,1,2} x {0,1}`, ordered lexicographically. Links are ordered `(tail,axis)`, oriented in the positive coordinate direction. Faces are ordered `(tail,a,b)` with `a<b`, and the frozen face word follows `+a,+b,-a,-b`. The checker exports each actual signed link word. Independently enumerating four-cycles from the adjacency relation recovers exactly the face list. There are seven internal faces (IDs 5,11,14,15,20,23,24), all included. Connectivity gives cycle rank `46-24+1=23`. This count is not the number of independent Wilson functions in a linear Hilbert-space basis.

For `g=(g_v)` at all vertices, including boundary vertices, use

`U_(v,w) -> g_v U_(v,w) g_w^-1`.

Products along an oriented loop transform by conjugation at its starting vertex. With `W_p=Tr(U_boundary(p))/2`, the full model is

`Hphys=L2(SU(2)^46, normalized product Haar)^SU(2)^24`,
`K=sum_e C_e`, `S=sum_p W_p`, `L=K+lambda(29-S)`.

No tree links are removed. `H=alpha L` and `sigma=alpha t/hbar`; `a,E_star,alpha/E_star,hbar` stay fixed and positive. Lambda is the dimensionless physical coupling, not a fitted time parameter. This is heat/Euclidean evolution, not a real-time theorem.

Product Peter–Weyl blocks have labels `j_e`, Casimir energy `sum_e j_e(j_e+1)` and finite dimensions. Every vertex action preserves each complete label block, so gauge averaging commutes with their projections and with K. The electric operator is self-adjoint on `H2(SU(2)^46) intersect Hphys`, with form domain `H1 intersect Hphys` and smooth invariant Peter–Weyl core. Its product elliptic resolvent is compact, as is its restriction to the reducing physical space. The real smooth invariant multiplier satisfies `0<=29-S<=58`. Thus for nonnegative lambda, L is self-adjoint on `D(K)`, has the same form domain and compact resolvent, and `L>=K`. These operator/domain arguments apply to all representation labels, not only those enumerated below.

## 2. The strict physical cutoff is exactly the vacuum and faces

A nonempty active spin support of a gauge-invariant vector has no degree-one vertex: one nontrivial irreducible representation has no invariant vector. Every active edge costs at least `3/4`. A nonempty finite support of minimum degree at least two contains a cycle. The graph is simple and bipartite with girth four; hence the full electric gap is at least 3, attained by a fundamental square, and the electric zero state is uniquely `Omega=1`.

Below energy `9/2` at most five edges are active. A four-edge support must be a four-cycle. A five-edge minimum-degree-two simple bipartite support is impossible: it has at most five active vertices; with at most four vertices it has at most four bipartite edges, while the only possible five-vertex partition supporting five edges is `(2,3)`, and deleting one edge from `K_(2,3)` leaves a degree-one vertex. The checker also exhausts these finite abstract bipartitions. Multiple components cannot evade this argument, since each would require at least four edges.

Every four-cycle is an enumerated elementary face. At its bivalent vertices, the invariant intertwiner forces equal spins around the cycle and is unique. The strict energy bound `4j(j+1)<9/2` selects `j=1/2`. Haar normalization gives orthonormal functions `phi_p=2W_p`, one per face, orthogonal to Omega and one another. Consequently

`P0=1_[0,9/2)(K)=span{Omega,phi_0,...,phi_28}`, rank 30.

The endpoint is excluded. Six-edge fundamental loops and the shared-edge spin-zero channels below have energy exactly `9/2`; they enter the enrichment, not P0. This electric cutoff is distinct from the historical total twice-spin degree cutoff even where their smallest old spaces happened to agree.

## 3. Complete individually resolved enrichment and exact Gram

Resolve each actual `Q0 S phi_p` into individual face-product channels before taking electric spectral components. This convention specifies the following span; it need not be the smaller cyclic space generated by the summed columns alone, and need not contain every intertwiner of its ambient electric shells.

For distinct faces put `X_pq=W_p W_q`. On a shared edge let `E_e` be Haar averaging in that edge, the spin-zero orthogonal projection. Define `X_s=E_e X_pq`, `X_t=X_pq-X_s`. Because the common edge carries `1/2 tensor 1/2=0 direct-sum 1`, these are all generated branches. Haar averaging commutes with both endpoint gauge actions. Face reversal leaves the SU(2) trace unchanged, so orientations can be aligned to write the common-edge product as `chi(AU)chi(U^-1 B)` without a phase ambiguity. Haar integration gives its spin-zero part `chi(AB)/2`. The two remaining three-edge paths use disjoint link variables; their products are independent Haar variables. Hence the spin-zero part of `4X_pq` has norm squared `1/4`; its orthogonal spin-one remainder has norm squared `3/4`.

The actual rational-coordinate basis is:

| Function | Count | Norm squared | K eigenvalue |
|---|---:|---:|---:|
| Omega | 1 | 1 | 0 |
| `phi_p=2W_p` | 29 | 1 | 3 |
| `chi_p=4W_p^2-1` | 29 | 1 | 8 |
| `d_pq=4W_p W_q`, no shared edge | 310 | 1 | 6 |
| `s_pq=8X_s`, shared edge | 96 | 1 | 9/2 |
| `t_pq=8X_t`, shared edge | 96 | 3 | 13/2 |

Among edge-disjoint pairs, 64 meet only at a vertex and 246 have disjoint vertices. A vertex-only intersection does not introduce an extra electric action: each of the eight distinct links has spin 1/2, so the product is an eigenvector of energy 6. Other invariant tensors can share those electric labels, but remain outside this specifically generated span. Shared pairs have six nonshared fundamental links and common-edge spin zero or one, giving energies `6(3/4)` and `6(3/4)+2`. The checker confirms every pair intersection has at most one common edge and records its signs in both face words.

All 406 two-face parity masks are nonzero and distinct; none is a single-face mask. The checker also exhausts triple and four-distinct-face masks. These actual mask facts, under independent central flips of individual links, prove orthogonality between distinct pair channels and between them and the old sector. They remain valid after the shared-edge spectral projection. Within a shared pair the two branches are orthogonal electric eigenspaces. Spin-one face characters have distinct nonzero integer representation supports, so they are mutually orthogonal and orthogonal to Omega; nonzero half-integer parity separates them from every two-face channel. Thus the Gram is **exactly diagonal and positive**, with 96 weights 3 and 465 weights 1. Its kernel is zero and its quotient rank is 561. No diagonal-Gram assumption or numerical eigenvalue cutoff is used to infer this result.

All basis vectors are smooth invariant polynomials and K eigenvectors. Their finite span therefore reduces K on its operator and form domains even though it does not exhaust complete electric shells. Call its orthogonal projection P+, and `Q+=I-P+`. The physical block domain is `ran P+ direct-sum Q+D(K)`. All projections and norms below refer to this actual Gram.

## 4. Every retained magnetic entry and every outside column

Assign central link signs `+1` on x links, `(-1)^x` on y links and `(-1)^(x+y)` on z links, using integer tail coordinates. The product on every new face is -1. This transformation preserves Haar and gauge invariance, commutes with K, and sends S to -S. Omega and all new channels are even; fundamental faces are odd. It proves same-parity magnetic entries vanish. It does not prove pair-mask independence: that was checked separately above. Flipping every link instead leaves a four-edge face unchanged and fails this test.

The complete old columns are the exact multiplication identities

`S Omega=(1/2)sum_p phi_p`,
`S phi_p=(1/2)Omega+(1/2)chi_p`
`         +(1/2)sum_(q no shared edge) d_pq`
`         +(1/4)sum_(q shared edge)(s_pq+t_pq)`.

There are no other odd retained functions. Therefore these columns, same-parity zeros, and metric self-adjointness determine **every** retained magnetic entry. If M is the diagonal Gram and `S_ij` are coordinate coefficients, `M_i S_ij=M_j S_ji`. In particular the coefficient from an unnormalized triplet back to either face is `3/4`, not `1/4`. The output stores all 2,124 directed nonzero entries and the defining zero rule for the remaining 312,597 entries; a dense list of zeros is unnecessary. K is the listed diagonal matrix, and `A+=P+LP+` is its sum with `29lambda I-lambda S_ret`.

For every retained basis function `b_j`, define its full outside column exactly by

`B b_j=-lambda [S b_j-sum_i b_i <b_i,S b_j>/M_i]`.

This is the actual Haar projection of the full polynomial product. K reduction gives `B=Q+LP+=-lambda Q+SP+`. The old column identities prove `B P0=0`. For **every** complex retained unit vector, simultaneously,

`||B||<=lambda||S||<=29lambda`.

Thus all newly retained input columns and all unretained intertwiners are charged together; the bound neither sums separate column norms incorrectly nor discards return paths. It is not the exact outside norm or an evaluated cubic outside Gram. B is nonzero at positive coupling: multiplication of `chi_p` by its matching W_p has normalized spin-3/2 face-character coefficient `1/2`. That character has electric energy 15, outside this enrichment; other faces give zero overlap by parity. Hence `<chi_(3/2,p),B chi_p>=-lambda/2`. Zero old columns do not mean autonomous retained evolution.

The code exports exact generator actions on vacuum, normalized real and imaginary original-face preparations, a face difference, and an unnormalized triplet coordinate. Its optional rational real/imaginary vector interface evaluates any retained coordinate vector in the same metric. This is a generator action, not a heat evaluator.

## 5. Original Ritz ground and complete physical residual

Here m=29. Put

`w=(sqrt(9+m lambda^2)-3)/2`, `h=lambda/[2(3+w)]`,
`mu0=m lambda-w`, `Z=1+m h^2`,
`f0=(Omega+h sum_p phi_p)/sqrt(Z)`.

The exact P0 compression has vacuum diagonal `m lambda`, face diagonal `3+m lambda`, and vacuum/face entries `-lambda/2`. Its bright two-dimensional block gives the displayed ground and its dark eigenvalues are `3+m lambda`. Relations `w(3+w)=m lambda^2/4` and `2h(3+w)=lambda` verify its eigen-equation. At lambda zero use `w=h=mu0=0`.

For `F=S^2-m/4`, exclusive-edge conditional Haar integration gives `<W_p^2 W_q^2>=1/16` for every distinct pair, including shared edges. This is not a claim that all face holonomies are jointly independent. All odd-parity patterns vanish, and the checked distinct-face masks exhaust the remaining fourth-moment possibilities. Thus

`<S^2>=m/4`, `<S^4>=(3m^2-m)/16`,
`||F||^2=m(2m-1)/16=1653/16`.

The independent channel decomposition has F coefficient `1/4` on every spin-one, singlet and triplet coordinate, and `1/2` on every edge-disjoint product. Summing their actual metric weights gives the same norm. It retains all channels. Correspondingly the full old-to-new `Q0 S P_face` Gram has diagonal `m/4`, off-diagonal `1/4`, bright eigenvalue `(2m-1)/4=57/4`, and dark eigenvalue `(m-1)/4=7`; the code recovers it from every new matrix row.

The full, actual residual is

`(L-mu0)f0=-2lambda h F/sqrt(Z)`,
`rho0^2=1653 lambda^2 h^2/[4(1+29h^2)]`.

These are exact functions of lambda. The following barred quantities are **uniform upper envelopes**, not evaluated actual residuals. Since `h<=lambda/6`, `sqrt(1653)<41`, and `sqrt(29)<11/2`, set at `Lambda=1/100`

`g=3-29Lambda=271/100`,
`rho0_bar=41Lambda^2/12`, `p0_bar=rho0_bar/g`.

Positivity L>=K, compactness and min-max imply the second full/compressed eigenvalues are at least 3. Vacuum trial and nesting give

`0<=epsilon<=mu+<=mu0<=29lambda<3`.

This isolates the unique full ground G, original Ritz ground G0 and enriched Ritz ground G+ **before** using residual estimates. A small residual alone is not the isolation argument.

## 6. Both projector comparisons and the enriched residual

The complete full spectral measure of f0 gives `||G-G0||<=rho0/(3-mu0)<=p0_bar`. Also `L f0` lies in ran P+ by the complete old-column closure, so its residual inside A+ is the same vector: `(A+-mu0)f0=(L-mu0)f0`. The separately isolated compressed spectrum therefore gives the second, distinct estimate

`||G+-G0||<=p0_bar`.

Let f+ be the normalized exact ground of A+. With `B f0=0`,

`rho+=||(L-mu+)f+||=||Bf+||`
`      =||B(I-G0)f+||<=29Lambda p0_bar=:rho+_bar`.

The full spectral residual and Temple argument then give

`||G-G+||<=p+_bar=rho+_bar/g`,
`0<=mu+-epsilon<=d+_bar=(rho+_bar)^2/g`.

For the energy estimate, integrate `(E-epsilon)(E-3)>=0` against f+'s full spectral measure: its expectation equals `rho+^2-(mu+-epsilon)(3-mu+)`. Every required second moment exists because f+ is a finite smooth polynomial. This explicitly bounds the full physical residual; an internal compressed residual would be zero and would not establish this claim.

## 7. All-time physical heat bound on the original preparation class

Take normalized complex `x in ran P0` with `||x-Omega||<=eta=1/100`. The original Ritz formulas give the uniform bounds

`z=1-29Lambda^2/72 <= |<f0,Omega>|`,
`q0_bar=(11/12)Lambda >= ||(I-G0)Omega||`.

The first follows `(1+u)^(-1/2)>=1-u/2`, the second from `sqrt(29)h`. The **two** projector comparisons yield

`||E(sigma)x||>=||Gx||>=D=z-eta-p0_bar>0`,
`||(I-G)x||, ||(I-G+)x|| <= b=q0_bar+p0_bar+eta`.

Here `E=exp[-sigma(L-epsilon)]`, while `E+=exp[-sigma(A+-mu+)]P+`. The denominator is the true full output, not a Ritz norm or fitted floor. Both full and retained centered excited gaps are at least g.

For finite smooth retained initial vectors, the vector-valued fundamental theorem gives the exact strong Duhamel identity

`(E(t)-E+(t))x=-integral_0^t E(t-s)[B+(mu+-epsilon)P+]E+(s)x ds`.

The finite retained evolution stays in the common operator domain and `L E+(s)x` is continuous. No unbounded operator-norm derivative or norm-Bochner assertion is needed. The full E inside the integral retains outside evolution and returns. Its plus centering defect is essential. Decomposing the retained evolution into its ground and excited pieces proves the increasing early bound

`V(t)=(rho+_bar+d+_bar)t+(29Lambda)b(1-exp(-gt))/g`.

Independent full and retained spectral decompositions give the decreasing late bound

`J(t)=p+_bar+(2b+p+_bar)exp(-gt)`.

The extra decaying p+ term is harmless slack; both excited components already have bound b. The contract's fixed join T=2 gives `max(V(2),J(2))/D` for every nonnegative time. For an entirely rational outward calculation use `1-exp(-2g)<=1`; 32 positive Taylor terms prove `exp(2g)>225`. These inequalities are analytic and uniform, not time-grid interpolation.

| Uniform quantity | Exact envelope |
|---|---:|
| `rho0_bar` | `41/120000` |
| `p0_bar` | `41/325200` |
| `rho+_bar` | `1189/32520000` |
| `p+_bar` | `1189/88129200` |
| `d+_bar` | `1413721/2865961584000000` |
| True denominator D | `193136341/195120000` |
| Early absolute bound at join | `3063228992521/1432980792000000` |
| Late absolute bound at join | `611537/3304845000` |
| All-time relative bound | `3063228992521/1418412601938100` |

The early bound dominates, giving approximately `0.002159618`, and the same absolute numerator bounds the error on all times. The cap envelopes cover every lambda in the continuous interval because each underlying estimate used `lambda<=Lambda` and a uniform spectral separation. At time zero the exact error on this initial class is zero. At zero coupling P+ reduces the full K and both grounds have energy zero, so exact agreement holds at every time. These identities supersede coarse positive cap envelopes. Ground-null inputs outside the preparation class are not admitted; full-input zero-time error of a zero-extended finite projection is one.

## 8. Executed checks, provenance and limits

Before scientific work, all 42 contract sources, the contract and six used instruction references were copied and hash-verified: 49 original snapshots. The original preflight manifest, initial format adapter and canonical `inputs/source-inventory.json` are preserved. The latter maps each origin to its owned snapshot and hash. Historical checker files are read-only context; this new standard-library implementation imports or executes none of them. The unchanged contract supersedes historical solo/stop wording in inherited instructions for this authorized independent team loop.

Executed checks reconstruct all geometry and cycle masks, pair incidence, Gram and electric branches, sparse magnetic coefficients and their metric adjoints. Rational noncommuting SU(2) quaternion fixtures check every face's gauge invariance; missing inverse orientations and wrong endpoint gauge action yield nonzero discrepancies. Missing internal faces, endpoint inclusion, missing either shared branch, old dimensions/constants, and wrong triplet metric are rejected. A deliberately duplicated face has the exact null vector `(1,-1)`; both actions descend through that relation, whereas assigning it an identity Gram fails. The actual basis has zero kernel. A new spin-3/2 outside witness rejects confusing `BP0=0` with `B=0`.

Controls also reject using negative-coupling vacuum shift as a positive interaction, the scalar reference as the Ritz ground (its bright characteristic determinant is `-29/40000` at the cap), and an uncertain scalar center as exact for unbounded times. For the latter, time times center error one amplifies a ground factor beyond the rational lower bound `65/24>2`. The own-ground defect sign, true initial class, zero coupling and zero-time injections are retained. Real and imaginary preparations `(159999 Omega+800 phi_0)/160001` and `(159999 Omega+800 i phi_0)/160001` are exactly normalized with vacuum distance squared `4/160001<1/10000`. Generator actions on these and the new triplet are executed. Explicit exceptions remain active under optimized Python.

The report proves domain, full-Hilbert and continuous-parameter statements; finite controls test their concrete coefficients and reject specified wrong substitutions. Neither a Boolean control nor a finite enumeration substitutes for those proofs. Normal and optimized fresh output equality and source hashes are recorded in the final freeze. Rational certificate and generator actions have no rounding allowance; an implemented heat vector would need its own numerical budget, divided by the same D, before a full-vector claim.

Accepted scope: one complete new-graph cutoff/channel/Gram/generator construction, a simultaneous full outside envelope, improved enriched-ground residual certificates and a conservative exact-semigroup all-time relative bound. No whole ambient-shell completion, cubic outside Gram evaluation, numerical heat evaluator, real-time relative theorem, volume-uniform result, homogeneous/canonical map, mass calibration or continuum Yang–Mills theorem is supplied. Scientific priority remains unverified. AH2 and the final two goals are not selected or executed here.
