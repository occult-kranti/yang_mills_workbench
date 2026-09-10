# Closed cube Wilson graph and exact Haar moments

The graph has eight binary-coordinate vertices and twelve positive-coordinate links. Each signed face word is the outward-oriented boundary of one of six squares. The JSON graph records all actual endpoints and traversals. Every link appears in exactly two faces with opposite signs. The resulting two-complex is the closed oriented sphere, not an open planar patch. Link Haar measures are independent and normalized. The finite Wilson exponent is S=sum_f k_f*x_f, x_f=Tr(U_face_f)/2.

Under U_(v,w)->g_v U_(v,w) g_w^-1, each correctly ordered face product transforms by conjugation at its base vertex; its trace is invariant. An inverse traversal is U^-1=U^dagger. Reversing a complete face changes its holonomy to its inverse up to basepoint conjugation and preserves its real SU(2) trace. Removing only one dagger generally destroys endpoint covariance and is a discriminating wrong-model control.

## Character gluing

For SU(2), use chi_n of spin n/2 and dimension d_n=n+1. Expand each central face weight f_f(U)=sum_n a_(f,n)*chi_n(U). Schur orthogonality pairs a representation matrix on a traversed edge with its conjugate on the oppositely traversed neighboring face. Inequivalent labels have zero pairing, so a connected closed surface forces all face labels equal. Each edge contributes1/d_n. Each residual vertex index loop contributes d_n. On this graph V-E=8-12=-4; therefore

integral product_f f_f(U_face_f) dHaar_links = sum_n d_n^-4 product_f a_(f,n).

This formula is first an exact identity for finite character polynomials. For analytic bounded Wilson weights, absolute convergence permits the character expansion and integration; B2 instead uses finite total-degree Taylor polynomials and an explicit global remainder. No asymptotic series is needed.

For x^m=2^-m chi_1^m, the finite coefficients follow the tensor rule chi_1*chi_n=chi_(n+1)+chi_(n-1), with chi_-1=0. It follows that the normalized all-six distinct-face product has Haar mean2^-6*2^-4=1/1024. A nonempty proper subset has at least one degree0 face forcing n=0 and a degree1 face with zero n=0 coefficient, hence its moment vanishes. Independent direct fundamental edge-index contraction yields eight free index loops, twelve factors1/2, and six trace normalizations1/2, again1/1024.

The backward researcher sharpened the proper-subset statement: if any face weight is identically1, it has only a trivial character coefficient. The entire expression then equals the product of the one-face Haar averages of the other five weights. This supplies exact mutual independence of any at-most-five face class observables, including repeated powers, under the untilted edge Haar measure. It is compatible with the nonfactorized six-face effect and is not a claim of six independent face holonomies. For example, <product_f chi_f^2>=1+1/3^4=82/81, whereas the product of the six separate means is1.

## Repeated-face identities and the future Hamiltonian trial space

Write chi_p=Tr(U_face_p)=2x_p. Single-face Haar marginals are Haar; their mean is0 and squared-character mean1. Distinct face characters are orthogonal: <chi_p chi_q>=delta_pq. For every triple p,q,r, including all repeated-index patterns, <chi_p chi_q chi_r>=0. If the three faces are distinct or one appears once, the n=0 factor for that once-occurring face vanishes; if all coincide, chi_1^3 has odd representation labels and no trivial term. Thus for W=-sum_f lambda_f*x_f, every matrix element <chi_p W chi_q>=0.

For the separate electric Hamiltonian H0=alpha*sum_e J_e^2, a simple fundamental square character occupies four distinct edges. Each edge Casimir is3/4, so H0*chi_p=3alpha*chi_p. This eigenfunction statement pertains to the untruncated gauge-invariant Hamiltonian Hilbert space. It does not identify the finite Euclidean Wilson measure with a ground-state measure. These low-degree entries are supplied for a later variational argument, which has not been executed in B1.

## Candidate B2 extension

For exp(k*x), a_n(k)=sum_(j>=0) d_n*k^(n+2j)/[2^(n+2j)*j!*(n+1+j)!]. With a common rational k, the partition uses sum_n d_n^-4*a_n(k)^6. The all-six-face insertion uses sum_n d_n^-4*(a_n'(k))^6, because each face coefficient is differentiated independently before setting them equal. It is not the sixth common-k derivative of Z. Finite total Taylor degree N and |S|<=6|k| supply a single rigorous tail for partition and the bounded insertion. B2 still requires its own advisor gate.
