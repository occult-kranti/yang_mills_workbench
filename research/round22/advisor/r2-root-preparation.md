# R2 independent advisor preparation

Prepared after the R2 contract and before reading either current producer or current skeptical preparation. This is advisor analysis, not a producer submission or an additional research loop. It must still be compared with the independent proofs after both freeze.

Let k=28|tau|<=35/416 and g=1-k>=381/416. On the actual product-reference incomplete tensor product, H0 is the positive tensor sum and H0>=Q. Local finite-excitation tensors with suitable onsite spectral cutoffs give a form core. For each actual retained star, D_b=Q_b phi_b Q_b, ||phi_b||<=7|tau| and D_b Omega=0. For all form vectors, the absolute sum of diagonal form contributions is at most7|tau| sum_b ||Q_b psi||^2 <= k <psi,H0 psi>. Polarization and Cauchy–Schwarz on the sums give a sesquilinear form bounded by k||H0^(1/2)phi||||H0^(1/2)psi||. Thus the infinite form is well-defined on D(H0^(1/2)). Its sum with the bare closed form is closed by equivalent form norms; its associated G obeys gH0<=G<=(1+k)H0, with unique vacuum and complementary gap g. This does not by itself prove D(G)=D(H0).

On Q, the form defines bounded self-adjoint K with norm at most k after sandwiching by H0^(-1/2). The form calculation against arbitrary test vectors shows
u=H0^(-1/2)(1+K)^(-1)H0^(-1/2)v
belongs to D(G) and Gu=v. Since k<1, expand in u_n=H0^(-1/2)(-K)^nH0^(-1/2)v. Each Hilbert and H0^(1/2) norm is at most r k^n. The Neumann tail after index L is at most r k^(L+1)/g in each norm. These conclusions also apply in every finite cuboid with the same constants.

## Local support and the response operator graph

H0^(-1/2), with value zero at the vacuum, preserves vectors supported on a finite set S with exterior vacuum. Every disjoint D_b annihilates such a vector, including its strip ground. Only stars meeting S act, there are at most4|S|, and each is contained in S^(1). The form sandwich on this local subspace is consequently a finite sum of bounded D_b between bounded inverses. Induction gives support(u_n) subset Y^(n), and |Y^(n)|<=|Y|(2n+1)^3 in the positive octant. This statement concerns vectors, not global vacuum projections as elements of the quasilocal operator algebra.

For n=0, H0u_0=v. For n>=1 the local finite sum and bounded H0^(-1) imply u_n=-H0^(-1)D u_(n-1), so
||H0u_n|| <= |Y|(2n-1)^3 k^n r.
This proves each term lies in D(H0), without using the false global domain inference from form equivalence. For L>=0 define a=2L+1 and
F_L(k)=k^(L+1)[a^3/(1-k)+6a^2 k/(1-k)^2+12a k(1+k)/(1-k)^3+8k(1+4k+k^2)/(1-k)^4].
It equals sum_(n>L)(2n-1)^3 k^n. The H0 graph tail is at most r[k^(L+1)/g+|Y|F_L(k)] if graph norm is taken as ||w||+||H0w||. Closedness gives u in D(H0); this is a theorem about these local-source responses, not D(G)=D(H0) on all vectors. k=0 and r=0 are handled separately with every tail zero.

If Lambda contains Y^(L), finite and infinite coefficients agree through n=L: each step that creates coefficient n uses stars wholly in Y^(n), so there is no missing boundary star through that order. Embed finite coefficients by the exterior vacuum. Both tails have the same majorants, hence ||u_Lambda-u|| and its H0^(1/2) norm are at most2r k^(L+1)/g, and the graph difference is at most twice the graph-tail bound. The unbounded bare tensor sum agrees with the finite tensor sum on these embedded local vectors. This is actual finite-volume response convergence in the fixed representation.

## Source-sector test

For finite Lambda, S_vac=|u_Lambda><Omega_Lambda|-adjoint preserves D(G_Lambda) and [S_vac,G_Lambda]=-A_vac by direct rank-two multiplication. With the fixed local source, A_vac=A_Y tensor P_ext, whereas the R1 source is A_Y tensor I. Thus the exact remaining operator is A_Y tensor(I-P_ext). On psi=Omega_Y tensor chi_ext Omega_ext, with the contract's free z-character at coarse e_x, ||psi||=1 and the remaining vector is v_Y tensor chi_ext Omega_ext of norm1. This is independent of tau, because it compares the exact rank-two cancellation once the inverse exists. At tau=0 it can also be checked directly from the two free energies6 and the local source; the residual is already nonzero. Norm(A_Y tensor(I-P_ext))=r whenever the exterior has an excited vector. Infinite vacuum rank-two projectors likewise do not become local identity extensions through norm convergence of u.

For a separate boundary-action control, R1 gives ||D v||^2=7tau^2/12 for the origin singleton embedded in a sufficiently large cuboid, with D summing all retained stars. Thus the first inverse coefficient is nonzero for tau!=0 by injectivity of H0^(-1) on Q. Setting it to zero by retaining only stars interior to the singleton is invalid. This uses the admitted actual SU2 result, not a surrogate matrix.

## What the collar weight proves and does not prove

For Y={0}, |Y^(n)|=(n+1)^3. The specified geometric majorant b_n=r k^n is summable in n when k<1. For any r>0,k>0,mu>0 the volume-weighted upper term r exp(mu(n+1)^3)k^n tends to infinity: its logarithm has positive cubic leading coefficient and only a linear negative term. Hence this particular upper certificate cannot establish the O2 positive-volume-weight interaction norm. Actual coefficient norms are bounded above by b_n; no lower divergence statement follows. A different connected-support decomposition, sharper estimates or cancellations remain possible. The global rank-two source distinction already blocks interpreting this vector series as the desired full local-operator homological step.

## Source reading boundary

Root checked Gerald Teschl, Mathematical Methods in Quantum Mechanics, second edition (2014), author PDF370pages, printed pp174–176: definition6.41, Theorem6.24 statement/proof, Theorem6.25 statement/proof and equation6.44. The closed-form and sandwiched-inverse method is established. Here the actual absolute form sum, numerical k, local support, response graph bounds and source-sector control are derived above. No global operator-domain equality, later-diagonal stability or continuum result is imported. Scientific priority is unverified.

Source: https://www.mat.univie.ac.at/~gerald/ftp/book-schroe/schroe2.pdf
