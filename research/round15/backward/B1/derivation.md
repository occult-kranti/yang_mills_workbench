# Independent cube graph and Haar contractions

The model is the oriented boundary of a single cube:8 vertices,12 links and6 faces, with independent normalized SU(2) Haar link variables. A reversed traversal uses the inverse link. Each face observable is x_f=Tr(U_boundary_f)/2. This is a closed two-dimensional surface embedded in three dimensions, not a finite four-dimensional continuum theory.

## Fundamental edge-index verification

For a selected set of distinct faces, expand each trace into a sum of fundamental matrix-index products. Any edge appearing exactly once integrates to zero because the fundamental representation has no invariant vector. If a proper nonempty subset of cube faces is selected, the connected dual-face graph has a cut, hence some boundary edge appears exactly once. Every such face subproduct therefore vanishes.

For all six outward-oriented faces, each edge appears once as U and once as U-dagger. Haar orthogonality is integral U_ab conjugate(U_cd) dU = delta_ac delta_bd/2. The independent algorithm creates four separate color-index positions for each face and joins them only as prescribed by these actual edge pairings. It does not insert an assumed vertex count. The resulting contraction has8 free color sums,12 factors of1/2 from Haar integrations and6 factors of1/2 from normalized traces. Thus the full product expectation is 2^8/(2^12 2^6)=1/1024. The index count is verified from the published signed link words.

## General character gluing and repeated moments

For a class function f_f(U)=sum_r a_f,r chi_r(U), Schur orthogonality on every oriented edge identifies the same representation label across adjacent faces. Connectedness leaves one label r; counting the color loops on this sphere gives d_r^(V-E)=d_r^-4, where d_r=r+1. Therefore the partition integral is sum_r d_r^-4 product_f a_f,r. This is a general graph-matched convolution theorem, not the old two-holonomy d_r^-1 formula transferred without proof.

If at least one face function is the constant1, its sole character coefficient is a_0=1. The shared label must then be0, so the remaining face class functions integrate as a product of their separate Haar means. In particular, any at-most-three distinct face supports in the six-face cube have this factorization, even when a face is repeated. With chi_p=2x_p, Haar E[chi]=0, E[chi^2]=1 and all odd single-trace moments vanish. It follows that E[chi_p chi_q]=delta_pq and E[chi_p x_f chi_q]=0 for all p,q,f, including p=q=f. The vanishing proper DISTINCT-face subproducts by themselves would not prove these repeated identities; the missing-face character argument supplies the stronger premise.

For the electric operator H0=alpha sum_e C_e, the fundamental Wilson-loop function chi_p uses four distinct links and carries spin1/2 on each. The Casimir on each such link is3/4, regardless of traversal orientation. Thus H0 chi_p=3 alpha chi_p. The six chi_p are orthonormal by the previous identity. This is an exact untruncated operator statement on smooth finite Wilson functions, not a numerical Galerkin eigenvalue claim.

## Orientation checks and their meaning

Every edge convention may be reversed if its matrix and all occurrences are transformed consistently. Reversing a whole face sends U_face to U_face^-1 and leaves its real SU(2) trace unchanged. Those changes must pass as invariances. By contrast, changing a single dagger inside one face word breaks the link-path/gauge-transformation cancellation and is tested with explicit noncommuting rational SU(2) matrices. A discriminating wrong-word result is retained rather than assumed.
