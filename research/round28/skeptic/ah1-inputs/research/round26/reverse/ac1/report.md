# AC1 reverse: a 293-state electric closure and a rigorous full omitted map

Independent reverse work, frozen without current forward access. The actual model is the 18-vertex, 33-link, 20-face open (3,3,2) SU(2) graph with every Gauss constraint, L=K+lambda(20-S), S=sum_f x_f and 0<=lambda<=1/100. This is not the homogeneous S/W model or canonical q model. Fixed positive a,E_star,alpha/E_star,hbar and sigma=alpha t/hbar are unchanged. Newton's inverse reconstruction demands the entire map on every input; Tesla's loading test demands both spin branches of a shared edge.

The result is a fully specified 293-state K-reducing space, including every old residual channel, together with a full omitted-map remainder. The evaluated uniform bound worsens from the inherited sqrt(39)lambda/2 to 20lambda. No improvement of numerical accuracy is claimed. The new 293-by-293 magnetic matrix and its new ground eigenvector are not evaluated here, so this is a finite-space construction and conservative analytic certificate, not a completed high-accuracy solver.

## Actual vectors and exact Gram structure

Let P_1 have orthonormal basis Omega=1 and phi_f=2x_f. Inherited Haar calculations identify 210 independent old residual vectors: chi_f=4x_f²-1 (20 spin-one face characters) and eta_fg=4x_f x_g (190 face products). The graph has 128 edge-disjoint face pairs and 62 pairs sharing exactly one edge. Pair center-parity masks are all distinct, nonzero, and distinct from single-face masks. The chi vectors have different integer-spin support and are mutually orthogonal. These observations prove the old Gram matrix is the identity, including pairs meeting only at a vertex.

An eta from a shared-edge pair is not a K eigenvector. Let E_0 and E_1 project its common edge to spin zero and one, respectively. Both commute with all vertex gauge transformations, so the projected vectors are physical. No other spin is possible since 1/2 tensor 1/2=0 direct-sum 1. On the six nonshared edges both branches retain spin 1/2. Thus

    K E_0 eta=(9/2)E_0 eta,
    K E_1 eta=(13/2)E_1 eta,
    ||E_0 eta||²=1/4, ||E_1 eta||²=3/4.          (AC1.R1)

For the norm assertion, independently Haar-average the common edge. After choosing orientations the product is chi(AU)chi(U^-1 B), and its spin-zero component is chi(AB)/2. The two disjoint three-edge paths A,B have independent Haar products. The resulting six-cycle fundamental character has norm one, giving squared norm 1/4. Orthogonal spin decomposition and ||eta||=1 give the remaining 3/4. Orientation reversal preserves these real SU(2) characters. This proof neither assumes shared face holonomies independent nor drops a generated intertwiner.

Define b_fg,0=2 E_0 eta_fg and b_fg,1=(2/sqrt(3))E_1 eta_fg. The branches are normalized and orthogonal, and eta_fg=(1/2)b_fg,0+(sqrt(3)/2)b_fg,1. Different pairs remain orthogonal because edge center parity is unchanged by the projection. These vectors specify their actual intertwiners through orthogonal Casimir projections; one need not pretend that all spin-network intertwiners with the same labels are included. For this cyclic space each branch has exactly one generated vector and it is a K eigenvector. The space is not a complete spin cutoff.

Let P_+ project onto Omega, the 20 phi_f, the 20 chi_f, the 128 edge-disjoint eta_fg, and both branches of each of the 62 shared-edge pairs. Its dimension is

    1+20+20+128+2*62=293.                       (AC1.R2)

The complete K action on these actual vectors is diagonal: energies 0 (one), 3 (20), 8 (20), 6 (128), 9/2 (62), 13/2 (62). Hence P_+ reduces K and its closed operator/form domains. All vectors are smooth invariant polynomials. In particular no hidden K leakage survives on newly retained inputs. Keeping the original 231 vectors without the 62 extra branches would fail this property.

## The entire new omitted map and its remainder

Let Q_+=I-P_+, A_+=P_+LP_+ on the retained space. For every basis vector b_j above, including all 272 new vectors, define its actual omitted column by

    T_+ b_j=-lambda Q_+ S b_j
      =-lambda [S b_j-sum_(i=1)^293 b_i <b_i,S b_j>].  (AC1.R3)

This exact formula specifies every column by finite Haar polynomial integrals. It retains all generated intertwiners outside P_+; it is not a list of one favorable output channel. The entire remainder has the rigorous bound

    T_+=Q_+LP_+=-lambda Q_+SP_+,
    ||T_+||<=lambda||S||<=20lambda.                   (AC1.R4)

For every unit complex coefficient vector c in C^293, the sum of all omitted columns has squared norm at most 400lambda². This follows from the actual multiplication inequality |S(g)|<=20 and orthogonal projections, so omitted channels cannot escape the bound. It is a bound on their complete sum, not 293 separate bounds wrongly combined without correlations. At the cap the full norm is at most 1/5. This remainder is explicitly conservative: the enlarged full omitted Gram matrix has not been computed.

For every old retained input, however, (AC1.R3) vanishes exactly: S Omega lies in the face space, and S phi_f lies in the old retained space plus all 210 residual channels now contained in P_+. Thus

    T_+ P_1=0.                                      (AC1.R5)

This is an actual structural improvement for the original preparation class. It does not imply T_+=0, autonomous 293-state dynamics, or a smaller all-input norm. New inputs have new omitted channels. Exact evaluation would involve at most 20*293=5860 raw face-times-input products before projection, and 85849 magnetic matrix entries before symmetry. The scalar graph/closure checks executed here cost only graph enumeration and rational arithmetic; they are not advertised as evaluation of those unevaluated matrix entries.

## Same-clock scope and true denominator

For A_+'s genuine ground mu_+, the variational nesting gives epsilon<=mu_+<=mu_21. Therefore delta_+=mu_+-epsilon is bounded by the old complete-residual Temple upper bound delta_old. Define E=e^-sigma(L-epsilon) and E_+=e^-sigma(A_+-mu_+)P_+. Both are contractions. The common smooth finite input domain and strong Duhamel identity give

    ||(E-E_+)x|| <= sigma(20lambda+delta_old)||x||,
              x in range P_+.                        (AC1.R6)

This is a finite-window absolute estimate for the mathematical exact new compression, not an evaluated matrix-exponential implementation. Its physical clock is the original sigma. At lambda=0 the full retained error is exactly zero, as P_+ reduces K and both ground shifts vanish; use that identity directly.

For the same normalized original preparation class x in P_1 with ||x-Omega||<=eta=1/100, retain the inherited actual ground projector G and old Ritz ground f_21. Its true output satisfies

    ||E(sigma)x|| >= |<f_21,Omega>|-eta-p_old=:a_eta>0.

This is the unchanged actual denominator, bounded uniformly below by 0.9898 on the frozen range. Dividing (AC1.R6) by a_eta gives a valid same-input relative certificate, but it is worse than the inherited Z2 certificate and grows with the window. No all-time relative improvement follows without the new matrix, ground data and sharper complete residual. At time zero the retained physical error is exactly zero. Every center shift is kept; initial physical leakage cancellation (AC1.R5) is not falsely equated with zero derivative of the separately centered heat error.

## Disposition

The exact actual K closure, 293-dimensional Gram structure, complete symbolic omitted map and rigorous full remainder are accepted as the proposed scoped result. The parent accuracy goal remains open. The checker reconstructs graph masks and every branch count, verifies all K energies and the original omitted-map Gram from rational branch squared weights, and checks the zero-coupling and bound-scope exceptions. Full Hilbert space/intertwiner completeness is not claimed; only this generated K-reducing span is complete. No physical scale calibration, large-volume theorem, continuum conclusion or scientific priority is inferred.
