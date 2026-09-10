# Loop1: actual adjacent-cube geometry and a mixed Haar contraction

## Scope and graph

Take vertices(x,y,z) with x=0,1,2 and y,z=0,1. The20 independent positive-coordinate links carry normalized SU(2) Haar variables. Eleven distinct square faces appear once: the shared square at x=1, five outer faces of the left cube, and five outer faces of the right cube. The JSON contract records each oriented edge and signed face word. The four shared-square edges are incident on three faces; the other16 edges have incidence2. Removing the internal face leaves a10-face sphere with the same12vertices and20edges. This outer action differs from the full11-face Wilson action.

The finite Euclidean exponent is sum_f k_f*x_f, x_f=Tr(U_face_f)/2. Coefficients k_f are dimensionless action coefficients; no Hamiltonian, physical time or electric energy scale is supplied by this integral. Representation labels and polynomial degrees are algorithmic or algebraic indices, not new physical fields. The derivation applies known Haar integration and SU(2) representation theory to this finite complex; no novelty or infinite-volume theorem is asserted.

## Disk reduction and its dimension factors

Fix the four link variables on the shared square and write their boundary holonomy H. Removing that shared face from each cube leaves a simply connected five-face disk. Its eight remaining links are disjoint from the other disk's eight remaining links. Conditional on the shared boundary, these two integrations therefore factorize into disk kernels; they are not eleven independent face integrations.

For SU(2) spin n/2, let chi_n be its character and d_n=n+1.

Our coefficient convention is a_n=integral f(U)chi_n(U)dU, since characters are orthonormal, and f=sum_n a_n chi_n. Thus f=chi_1 has a_1=1. A convention that instead expands f=sum_n d_n*fhat_n*chi_n has fhat_n=a_n/d_n; the two conventions cannot be mixed. Appending an extra dimension to our coefficient integral would incorrectly give a_1=2 for f=chi_1. The normalization fixture and raw polynomial character orthogonality checks distinguish that error.

The elementary convolution identity is

integral chi_n(AU)chi_m(U^-1 B)dU = delta_nm*chi_n(AB)/d_n.

It follows directly from the fundamental matrix coefficient orthogonality for unitary irreducible representations. Tree gauge fixing within a disk and successive merging of its five face weights require four such character convolutions. Internal gauge-tree variables have normalized integral1. Thus for finite class-function weights f_f(U)=sum_n a_(f,n)chi_n(U),

K_left(H) = sum_n [product_(f in left5) a_(f,n)/d_n^4] chi_n(H),

and the right disk has the corresponding formula with m and H^-1. Equivalently, the left disk has four interior vertices and eight internal edges; their color-index factors d_n^(4-8) give the same d_n^-4. The boundary character remains unnormalized. This counting is tied to the actual disk geometry; it does not assert the entire higher-incidence complex has the old single-surface d^-4 rule.

The four shared boundary links are independently Haar before inserting their weights. Their ordered product H is Haar: successive multiplication or gauge fixing of a boundary tree leaves one Haar holonomy and normalized gauge volumes. Since SU(2) characters are real and satisfy chi_m(H^-1)=chi_m(H),

integral K_left(H)K_right(H^-1)f_shared(H)dH
=sum_(n,m,k) [product_left a_(f,n)/d_n^4]
                 [product_right a_(f,m)/d_m^4] a_(shared,k) N_(n,m)^k.

Here N_(n,m)^k is1 exactly when |n-m|<=k<=n+m and n+m+k is even, and0 otherwise. The SU(2) tensor product is multiplicity free; integrating its character product extracts the trivial representation. These facts provide the new shared-edge coupling. For finite character polynomials every sum is finite. Extending to a Wilson exponential needs either an explicitly justified convergent series or a finite Taylor polynomial plus total remainder; that is reserved for Loop2.

## Exact reference and mixed moments

For a normalized trace x=chi_1/2, its only character coefficient is a_1=1/2. The complete11-trace product has n=m=k=1 and N_(1,1)^1=0, so its Haar mean is0. A separate link-center argument gives the same obstruction: each shared edge occurs three times, and multiplying that one Haar link by-1 changes the integrand sign.

If only one cube's six faces carry x, the other disk is constant and forces its label0. The remaining coefficient is2^-6*d_1^-4=1/1024. If the outer10 faces carry x and the shared face is constant, n=m=1,k=0 and the answer is(2^-5*d_1^-4)^2=2^-18.

For the genuinely mixed repeated-face insertion, use x_shared^2=(chi_0+chi_2)/4. Both allowed shared labels0 and2 have fusion multiplicity1, so

E0[(product_outer10 x_f)*x_shared^2] =2^-18*(1+1)/4 =2^-19.

Likewise inserting chi_2(shared)=4x_shared^2-1 gives2^-18. Missing the k=2 fusion channel would incorrectly halve the first mixed result. Replacing all labels by a single common n would also fail these graph-specific checks. The backward researcher independently checks the mixed result using the full four-index Haar projector on the shared edges, without this disk oracle.

## Complete center-parity map

For each of the2^11 distinct-face subsets, record the mod2 sum of selected face incidences at every edge. If any edge has odd incidence, its Haar center transformation forces the moment to vanish. The face-to-edge incidence matrix has rank9 over GF(2), hence kernel dimension2. Its four closed subsets are empty, left cube boundary, right cube boundary and outer boundary; their relation is outer=left XOR right. Direct fundamental index contractions on these closed surfaces give the exact nonzero moments above. Whole-face reversal preserves the real SU(2) trace and can orient each selected sphere consistently before pairwise index gluing.

## Validation and recorded implementation correction

Exact graph incidence, closed words, character moments and parity constraints are separate from floating matrix diagnostics. Matrix checks compare explicit quaternion multiplication with ordinary complex2x2 matrix products, gauge transforms at all12vertices, complete face reversal, and a deliberately incorrect single dagger. A determinant/unitarity check validates each sampled SU(2) matrix before it is used. A changed whole face orientation should pass as an invariance; a broken single-link word must produce a resolved gauge defect.

The first public character-power helper returned its cached mutable dictionary. A caller could modify that result and change later moments without changing source bytes: the left-cube mean changed from1/1024 to1/16 in the retained preacceptance failure. The corrected public helper validates input before cache lookup and returns a copy. Regression checks must preserve the expected moment after attempted result mutation and reject Boolean input even after an integer cache entry exists.
