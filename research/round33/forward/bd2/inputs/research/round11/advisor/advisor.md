# Round 11 advisor: the exact interacting two-square SU(2) operator

Contract: `ym11-two-square-v1`. Date: 9 September 2026. This document derives a finite spatial graph Hamiltonian on an infinite-dimensional physical Hilbert space. It establishes an explicit coupled differential operator, its physical realization, a complete electric spectrum, an exact omitted-degree threshold, and quantitative interacting gap bounds. It makes no mathematical novelty claim and no four-dimensional continuum claim. Numerical certificates and independently executed model checks have separate owners.

## 1. Physical contract and all six Gauss constraints

There are six distinct vertices, labeled TL, TM, TR on the upper row and BL, BM, BR on the lower row. The seven independent oriented links are:

| Link | Source | Target | Role |
|---|---|---|---|
| h1 | TL | TM | upper left |
| h2 | TM | TR | upper right |
| h3 | BL | BM | lower left |
| h4 | BM | BR | lower right |
| vL | TL | BL | left vertical |
| vM | TM | BM | shared vertical |
| vR | TR | BR | right vertical |

The reverse of a link carries its inverse, not an additional group variable. This is an open-boundary planar patch with two squares, not a periodic two-site lattice. There are no charges, matter fields, theta term, gravity, or added mass field. Time is continuous and hbar=1. The Hilbert space before constraints is L²(SU(2)^7, product normalized Haar).

Use T_a=sigma_a/2 and real-parameter skew-adjoint differential operators

\[
 L_e^a f(W_e)=\left.\frac d{ds}f(e^{isT_a}W_e)\right|_0,
 \qquad R_e^a f(W_e)=\left.\frac d{ds}f(W_e e^{isT_a})\right|_0.
 \tag{G1}
\]

The positive link Casimir is C_e=-sum_a(L_e^a)²=-sum_a(R_e^a)². Its spin-j eigenvalue is j(j+1); C_e applied to a fundamental matrix entry gives 3/4 times that entry. Hermitian electric generators can be defined as -iL and -iR, but cross-term signs must then be converted too.

Independent vertex transformations act as W_e -> g_source W_e g_target^-1. The physical space is invariant under the full product SU(2)^6, equivalently the joint kernel of all components of:

| Vertex | Skew Gauss generator |
|---|---|
| TL | L_h1 + L_vL |
| TM | L_h2 + L_vM - R_h1 |
| TR | L_vR - R_h2 |
| BL | L_h3 - R_vL |
| BM | L_h4 - R_h3 - R_vM |
| BR | -R_h4 - R_vR |

There is one independently choosable group transformation at each vertex. The generic orbit dimension is 18: the generic stabilizer is the common discrete center. At singular configurations the stabilizer grows, so one should not claim constant differential rank at every point. A single imposed global conjugation on seven unconstrained links would not impose these six local Gauss laws.

Base both loops at TM and traverse the two squares with the same circulation:

\[
 U=v_Mh_3^{-1}v_L^{-1}h_1,
 \qquad V=h_2v_Rh_4^{-1}v_M^{-1}.
 \tag{G2}
\]

The Hamiltonian is

\[
 H=\alpha K+\lambda_1(1-x)+\lambda_2(1-y),\quad
 K=\sum_{e=1}^7 C_e,\quad
 x=\tfrac12\operatorname{Tr}U,\quad y=\tfrac12\operatorname{Tr}V,
 \quad\alpha>0,\quad0\le\lambda_i<\infty.
 \tag{H1}
\]

The coefficients have energy units; K,x,y are dimensionless. The potentials are bounded between zero and two. Their nonnegativity is used in the simplest tail and variational bounds below.

For comparison with a declared Kogut–Susskind convention, alpha=g²/(2a) and equal lambda_i=2/(g²a) follow from expanding the fundamental trace in Eq. (1) of Froland–Grabowska–Li. This is convention matching, not scale matching inferred from a finite-graph gap. [Primary two-plaquette source](https://arxiv.org/html/2512.22782v1).

## 2. Tree gauge, quotient coordinates, and exact measure

Choose the spanning tree T={h1,h2,h3,h4,vM}. Starting at TM, independent vertex transformations set all five tree links to identity. The two remaining links then satisfy U=vL^-1 and V=vR. The unspent transformation at the root conjugates U and V simultaneously. Conversely, tree gauge shows that simultaneous-conjugate pairs label exactly the gauge orbits. Iterated Haar invariance in this invertible change of group coordinates integrates out the five tree variables and gives the unitary identification

\[
 \mathcal H_{\rm phys}\simeq L^2(SU(2)^2,dU\,dV)^{\rm Ad,diag}.
 \tag{Q1}
\]

Maximal-tree reduction and the need to resolve the remaining global charge sector are established structures in the literature; our formulas below are derived directly for the stated tree and loop paths. [Grabowska–Kane–Bauer, Sections II–III](https://arxiv.org/html/2409.10610v1).

Write U=xI+i a·sigma and V=yI+i b·sigma. Then

\[
 |a|^2=1-x^2,\quad |b|^2=1-y^2,\quad
 z=\tfrac12\operatorname{Tr}(UV)=xy-a\cdot b.
\]

The physical coordinate set is the compact body

\[
 \Omega=\{(x,y,z):|x|,|y|\le1,
 \ D(x,y,z)=1-x^2-y^2-z^2+2xyz\ge0\}.
 \tag{Q2}
\]

Equivalently (z-xy)² <= (1-x²)(1-y²); these conditions imply |z|<=1. Necessity is Cauchy–Schwarz for a and b. Conversely, any interior-coordinate triple satisfying the inequality supplies two real vectors of the stated lengths with dot product xy-z, hence two SU(2) matrices. If either length vanishes, the inequality forces z=xy and the remaining vector can be chosen freely with its required length. The two vector lengths and their mutual dot product form their Gram matrix. Equal Gram matrices imply an orthogonal map between the vector pairs. A reflection fixing the target pair's span changes an improper map into a proper map, because that span has dimension at most two. Thus the map can be in SO(3) and lifts to SU(2). These three coordinates classify all simultaneous-conjugation orbits, including central or collinear pairs. The quotient is homeomorphic to Omega: the continuous bijection from a compact quotient into this Hausdorff coordinate body is a homeomorphism.

For noncentral loops, t=a_hat·b_hat is uniform on [-1,1] with density 1/2 conditional on x,y. The one-group scalar density is (2/pi)sqrt(1-x²). Set z=xy-sqrt((1-x²)(1-y²))t. Its Jacobian cancels both square roots. Therefore

\[
 d\mu(x,y,z)=\frac2{\pi^2}\,dx\,dy\,dz\quad\hbox{on }\Omega,
 \qquad \int_\Omega d\mu=1.
 \tag{Q3}
\]

The boundary has zero measure, but its physical regularity still matters for the operator. At x=+/-1 or y=+/-1, z=xy and the relative angle is undefined and irrelevant. The coordinate t is not a new field or adjustable coupling; it records an existing gauge-invariant relative orientation. Keeping only x,y loses physical states. For example U=i sigma_3 with V=i sigma_3 or V=i sigma_1 gives the same x=y=0 but z=-1 or z=0.

The following exact rational moments are useful for a polynomial implementation. Let mu_2n=Catalan(n)/4^n, mu_odd=0, and

\[
 J(n,h)=\sum_{r=0}^h(-1)^r{h\choose r}\mu_{n+2r}.
\]

Then

\[
 \langle x^a y^b z^c\rangle=
 \sum_{h=0}^{\lfloor c/2\rfloor}
 \frac{{c\choose2h}}{2h+1}
 J(a+c-2h,h)J(b+c-2h,h).
 \tag{Q4}
\]

This follows by expanding z^c and integrating the independent semicircular scalar coordinates and uniform t. In particular <x²>=<y²>=<z²>=1/4, <xyz>=<x²y²>=1/16. Every finite monomial Gram matrix is strictly positive definite because Omega has nonempty interior.

## 3. Exact shared-link electric operator

In tree gauge, each of the three nonshared links of the left loop contributes C_U and each of the three nonshared links of the right loop contributes C_V. This statement follows by differentiating the unreduced path products, using bi-invariance of the Casimir and then setting the tree links to identity. No gauge fixing is performed before accounting for a derivative's full dependence.

Varying the shared link on its left, vM -> exp(isT_a)vM, gives

\[
 U\longmapsto e^{isT_a}U,\qquad
 V\longmapsto V e^{-isT_a},\qquad
 D_s^a=L_U^a-R_V^a.
\]

Consequently the reduced kinetic operator is exactly

\[
 K=3(C_U+C_V)-\sum_a(L_U^a-R_V^a)^2
 =4(C_U+C_V)+2\sum_a L_U^aR_V^a.
 \tag{K1}
\]

The two derivatives on different groups commute. In Hermitian electric generators the last term is -2 sum E_LU E_RV. Adding a factor of four to this result, or changing the cross-term sign without changing conventions, changes the seven-link Hamiltonian. The positive form representation also gives

\[
 3(C_U+C_V)\le K\le5(C_U+C_V).
 \tag{K2}
\]

The upper bound is the ordinary squared-norm inequality ||L_U f-R_V f||² <= 2||L_U f||²+2||R_V f||². It is not an identification of spectra with independent rotors.

Let q=(x,y,z). The carré-du-champ matrix A_ij=sum_(e,a)(D_e^a q_i)(D_e^a q_j) is

\[
 A=\begin{pmatrix}
 1-x^2 & (z-xy)/4 & 3(y-xz)/4\\
 (z-xy)/4 & 1-y^2 & 3(x-yz)/4\\
 3(y-xz)/4 & 3(x-yz)/4 & 3(1-z^2)/2
 \end{pmatrix}.
 \tag{K3}
\]

Here is a direct check of every type of coefficient. Four links differentiate x and contribute (1-x²)/4 each; the same is true for y. The trace z is the outer perimeter trace: UV=vM(h3^-1 vL^-1 h1 h2 vR h4^-1)vM^-1, so the shared derivative annihilates z, and its six other link contributions each give (1-z²)/4. Only the shared link differentiates both x and y: (D_s x)_a=-a_a/2, (D_s y)_a=+b_a/2, giving A_xy=-(a·b)/4=(z-xy)/4. Each of three left nonshared links gives (y-xz)/4 to A_xz, and the right calculation gives A_yz.

Because the scalar trace is a fundamental matrix coefficient, the drift vector of -K is

\[
 b=\operatorname{div}A=(-3x,-3y,-9z/2).
\]

Thus, with the constant physical measure (Q3),

\[
 Kf=-\operatorname{div}(A\nabla f)
 =-\big[(1-x^2)f_{xx}+(1-y^2)f_{yy}
 +\tfrac32(1-z^2)f_{zz}
 +\tfrac12(z-xy)f_{xy}
 +\tfrac32(y-xz)f_{xz}
 +\tfrac32(x-yz)f_{yz}
 -3xf_x-3yf_y-\tfrac92zf_z\big].
 \tag{K4}
\]

The coefficient of f_ij for i!=j is 2A_ij. This is a frequent source of an extra factor of two. Discriminating polynomial identities are

\[
 K1=0,\quad Kx=3x,\quad Ky=3y,\quad Kz=\tfrac92z,
 \quad K(xy)=\tfrac{13}2xy-\tfrac12z.
 \tag{K5}
\]

The two last identities reject the independent-rotor operator even when that model reproduces both individual one-loop traces. The span of functions of x,y alone is not K-invariant: xy immediately produces z.

Reversing V changes the chosen joint invariant to w=Tr(UV^-1)/2=2xy-z. The physical operator is then obtained by the chain rule under (x,y,z)->(x,y,w), a measure-preserving coordinate change of absolute Jacobian one. One must transform the mixed terms too. Relative loop orientation is therefore compatible with an explicit operator, but it cannot be silently dropped.

## 4. Physical domain and selfadjointness

The differential expression alone does not specify boundary conditions. Its physical definition is inherited from the compact group operator (K1). On full SU(2)^2, (K1) is a smooth uniformly elliptic nonnegative sum of squares, by (K2), and has its usual selfadjoint realization on H²(SU(2)^2). It commutes with simultaneous conjugation. Restrict to that closed invariant subspace and transport it through (Q1)–(Q3).

Equivalently, start with polynomials in x,y,z and close the nonnegative form

\[
 \mathfrak k[f]=\int_\Omega (\nabla\overline f)^T A\nabla f\,d\mu.
 \tag{D1}
\]

The operator associated with this closed form is the physical K. The polynomial spectral proof in the next section establishes essential selfadjointness on the polynomial core and identifies this realization uniquely. In coordinates,

\[
 D(K)=\{f: f(x(U),y(V),z(U,V))\in
 H^2(SU(2)^2)^{\rm Ad,diag}\}.
 \tag{D2}
\]

This intrinsic domain is more precise than an informal condition at the singular boundary of Omega. For a useful boundary check,

\[
 A\nabla D=-D(2x,2y,3z)^T.
 \tag{D3}
\]

Thus A has zero conormal flux on the smooth part D=0. Polynomial integration by parts is consistent with (D1), with no boundary term. One does not impose Dirichlet conditions on f at this boundary: the constant function is an admissible zero-electric-energy state. Nor does a naive pointwise Neumann condition by itself characterize the domain at the singular strata. The inherited group domain handles all such points.

## 5. Complete electric spectrum and an exact polynomial tail threshold

Let P_d be all polynomials in x,y,z of total degree <=d, including P_0=span{1}; write its orthogonal projector also as P_d where the meaning is clear. Its dimension is binomial(d+3,3). Distinct monomials are linearly independent on Omega. Equation (K4) preserves this flag and acts on m_abc=x^a y^b z^c as

\[
 Km_{abc}=\epsilon_{abc}m_{abc}
 +\hbox{terms of strictly lower total degree},
\]

\[
 \epsilon_{abc}=a^2+b^2+\tfrac32c^2+\tfrac12ab
 +\tfrac32c(a+b)+2a+2b+3c.
 \tag{E1}
\]

All terms of the same degree are diagonal in the monomial quotient P_d/P_(d-1). Symmetry of K implies that each orthogonal shell W_d=P_d minus P_(d-1) reduces K: if f is in W_d and g in P_(d-1), <Kf,g>=<f,Kg>=0. The induced map on the quotient is unitarily equivalent to K restricted to W_d. Hence the shell eigenvalues are exactly the numbers (E1) with a+b+c=d, counted with multiplicity. Selfadjointness on each finite shell rules out a hidden Jordan block even if eigenvalues coincide.

Polynomials separate points of the compact quotient, contain constants, and are closed under conjugation. Stone–Weierstrass and density of continuous functions in L² imply their density. Diagonalizing the finite orthogonal shells therefore gives a complete orthonormal eigenbasis of the physical space. The diagonal operator on finite combinations is essentially selfadjoint. The canonical domain is the set of coefficients whose sum of epsilon² times squared modulus is finite. This proves the polynomial-core assertion used above without assuming an unproved spin-network/degree bridge.

For a link-representation interpretation set

\[
 j=(a+c)/2,\quad k=(b+c)/2,\quad\ell=(a+b)/2.
\]

These are precisely nonnegative half-integers satisfying the triangle inequalities and j+k+ell integer. Conversely a=j+ell-k, b=k+ell-j, c=j+k-ell are nonnegative integers. Then

\[
 \epsilon_{abc}=3j(j+1)+3k(k+1)+\ell(\ell+1),
 \qquad d=j+k+\ell.
 \tag{E2}
\]

The degree-two vertices force one spin along each of the two three-link nonshared paths; the shared link carries ell. Each of the two trivalent vertices has a one-dimensional singlet intertwiner exactly when the triangle and parity conditions hold. This independently explains the representation labels and the count. It does not assert that raw monomials themselves are orthogonal electric eigenstates.

For fixed d, rewriting (E1) gives

\[
 \epsilon_{abc}=\tfrac58d^2+2d
 +\tfrac14dc+\tfrac58c^2+c+\tfrac38(a-b)^2.
\]

The minimum occurs at c=0 and a,b as nearly equal as possible. Every c>=1 incurs a cost greater than the largest possible reduction 3/8 in the parity term. Therefore the exact shell minimum is

\[
 m_d=\tfrac58d^2+2d+\tfrac38(d\bmod2),\qquad d\ge0.
 \tag{E3}
\]

It increases strictly with d. In particular the free physical gap is exactly 3alpha, and its first excited eigenspace is span{x,y}, of multiplicity two. Some low electric levels are:

| State or subspace | K eigenvalue |
|---|---:|
| 1 | 0 |
| span{x,y} | 3 |
| z | 9/2 |
| xy-z/4 | 13/2 |
| span{x²-1/4,y²-1/4} | 8 |

These lowest energies agree with the independent two-plaquette calculation's Table 4 after alpha=g²/2 at a=1. Its finite matrix blocks use a different coupled basis, so agreement of these spectral values is the comparison made here; no unchecked equality of differently gauge-fixed intermediate formulas is assumed. [Froland–Grabowska–Li, Appendix C](https://arxiv.org/html/2512.22782v1#A3).

Since m_d tends to infinity and each shell is finite, K has compact resolvent. A degree-D cutoff has the exact omitted-electric threshold

\[
 Q_D K Q_D\ge m_{D+1}Q_D,
 \quad Q_D=1-P_D.
 \tag{E4}
\]

D is maximum polynomial degree, not retained matrix dimension. The latter is binomial(D+3,3). The first omitted degree is D+1.

## 6. Interacting finite-graph theorem and explicit positive bounds

**Theorem F.** For every fixed alpha>0 and finite lambda_i>=0, (H1) is selfadjoint on D(K), has compact resolvent, has one strictly positive normalized ground state, and has a strictly positive physical first gap Delta=E1-E0. E0>=0 and E0>0 if lambda1+lambda2>0.

**Proof.** The potential is bounded and real, so bounded perturbation preserves selfadjointness on D(K) and compact resolvent. Consider also the smooth elliptic realization (K1) on full SU(2)^2. Its heat semigroup is positivity improving on this connected compact space. For bounded real potential, the Feynman–Kac formula, or the positive Trotter product with its elementary upper and lower potential bounds, retains positivity improvement. A compact positivity-improving semigroup has a unique positive ground state; elliptic regularity makes it smooth and everywhere positive. Simultaneous conjugation commutes with H and sends a positive normalized ground state to another one, so uniqueness makes it invariant. It is consequently the ground state in the physical sector. Compact resolvent and simplicity imply a strict first physical gap. Nonnegative terms give E0>=0. If E0=0, the kinetic form vanishes, forcing a constant state by (E3), but the constant has positive potential expectation lambda1+lambda2 whenever that sum is nonzero. QED.

This proof allows excited-state degeneracy, which indeed occurs at lambda1=lambda2=0. It does not import the one-dimensional Sturm–Liouville simplicity argument from one square.

For practical small couplings, min–max and the constant trial state give

\[
 E_1\ge3\alpha,\quad E_0\le\lambda_1+\lambda_2,
 \quad\Delta\ge3\alpha-\lambda_1-\lambda_2.
 \tag{F1}
\]

There is also a conservative explicit positive bound for every finite nonnegative pair:

\[
 \boxed{\displaystyle
 \Delta\ge\frac{243}{625}\,\alpha
 \exp\!\left[-\frac{16(\lambda_1+\lambda_2)}{3\alpha}\right].}
 \tag{F2}
\]

Here is a full proof, including its constants. Divide by alpha and write kappa_i=lambda_i/alpha and L=kappa1+kappa2. On full SU(2)^2 let S=-sum(L_U-R_V)². Its heat semigroup is a probability average of the action (U,V)->(hU,Vh^-1). The central one-group Casimirs commute with this action, so

\[
 e^{-tK}=e^{-3t(C_U+C_V)}e^{-tS}.
\]

The normalized SU(2) Casimir heat kernel has the Peter–Weyl expansion

\[
 p_s(g)=\sum_{n=0}^\infty(n+1)e^{-s n(n+2)/4}\chi_{n/2}(g),
 \quad|\chi_{n/2}(g)|\le n+1.
\]

At s=4, |p4-1|<=r=sum_(n>=1)(n+1)² exp[-n(n+2)]<1/4. An elementary rigorous estimate is 4e^-3<1/5 and, for n>=2, (n+1)²<=4^n and e^-n(n+2)<=e^-4n<(1/50)^n. The remaining series is bounded by sum_(n>=2)(2/25)^n=4/575, and 1/5+4/575<1/4. The two exponential inequalities follow directly from finite Taylor lower sums for e³ and e⁴.

Set t0=4/3. The product heat kernel e^-3t0(CU+CV) is between (3/4)² and (5/4)² everywhere. Probability averaging by e^-t0S preserves both bounds, so the kernel of e^-t0K is between 9/16 and 25/16. The potential W=kappa1(1-x)+kappa2(1-y) obeys 0<=W<=2L. Feynman–Kac yields the positive-kernel inequalities

\[
 e^{-2Lt_0}e^{-t_0K}\le e^{-t_0(K+W)}\le e^{-t_0K}.
\]

Apply them to its positive ground state phi, using e^-t0(K+W)phi=e^-t0e0 phi. The common scalar and integral cancel in the ratio, giving

\[
 \frac{\sup\phi}{\inf\phi}\le\frac{25}{9}\,e^{8L/3}.
\]

For invariant f, the ground-state transform gives

\[
 \langle\phi f,(K+W-e_0)\phi f\rangle
 =\int\phi^2\,\Gamma_K(f)\,d\mu.
\]

Let m=inf phi>0 and M=sup phi. The invariant free Poincare inequality from (E3) is Var_mu(f)<= (1/3) integral Gamma_K(f)dmu. Since variance is the minimum over constants,

\[
 \operatorname{Var}_{\phi^2\mu}(f)
 \le M^2\operatorname{Var}_\mu(f)
 \le\frac{M^2}{3m^2}\int\phi^2\Gamma_K(f)d\mu.
\]

Thus the physical dimensionless gap is at least 3(m/M)², proving (F2). The full group is used to justify smoothness, positive kernels and a ground-state ratio; the Poincare constant 3 is the physical invariant-sector constant. This distinction is essential. The proof was independently examined by the round-11 skeptic, including both exponent factors and the numerical rational prefactor. It is an agent mathematical review, not a proof-kernel or human-peer-review claim.

The bound is deliberately weak at large kappa. It supplies existence with a constant; finite matrix certificates below can give informative numbers. Neither the exponential dependence nor the constant has been optimized.

## 7. Exact finite-to-infinite interacting enclosures

Fix D>=1 and let P=P_D, Q=1-P. Set A=P H P and

\[
 \tau=\alpha m_{D+1},\qquad T=QHQ\ge\tau Q.
 \tag{T1}
\]

The tail inequality uses compression of the nonnegative full potential. One may not add its constant diagonal lambda1+lambda2 to tau while ignoring its offdiagonal terms. Let M=-lambda1 x-lambda2 y. Since K preserves P and constants do not couple the blocks,

\[
 C=PHQ=PMQ,\quad
 CC^*=PM(P_{D+1}-P_D)MP.
 \tag{T2}
\]

The last equality is exact: multiplication by x or y raises total degree by at most one, so QMP is entirely in the next finite shell. Thus the boundary coupling is a finite computable positive matrix, not an estimated infinite residual. It annihilates P_(D-1), and

\[
 CC^*\le(\lambda_1+\lambda_2)^2(P_D-P_{D-1}).
 \tag{T3}
\]

Choose a rational R satisfying the certified strict inequality mu1(A)<R<tau. Define

\[
 B=A-\frac{CC^*}{\tau-R}.
 \tag{T4}
\]

For u in P and v in Q, Young's inequality gives

\[
 2\Re\langle u,Cv\rangle
 \ge-\frac{\|C^*u\|^2}{\tau-R}-(\tau-R)\|v\|^2,
\]

so H>=B direct_sum RQ in quadratic-form order. Since mu1(B)<=mu1(A)<R, min–max gives

\[
 \mu_k(B)\le E_k(H)\le\mu_k(A),\quad k=0,1.
 \tag{T5}
\]

Replacing CC* by the larger right side of (T3) yields a simpler valid lower block. It can be less sharp. Certified finite brackets give

\[
 \ell_1^B-u_0^A\le\Delta\le u_1^A-\ell_0^B.
 \tag{T6}
\]

The first two indices count multiplicity. This matters at zero magnetic couplings and at symmetry-induced excited degeneracies. R must be certified above the first excited retained eigenvalue, not above a floating-point guess. If the lower gap endpoint is nonpositive, this particular enclosure is inconclusive even though (F2) proves positivity.

In a raw monomial basis, compute the rational positive Gram matrix G from (Q4), the symmetric Hamiltonian form matrix, and the rational boundary correction using exact Gram inverses/projectors. Eigenvalue counting is the inertia of H_form-rG, not the ordinary Euclidean eigenvalues of the form matrix. A rational LDL congruence or equivalent exact inertia algorithm must explicitly handle zero pivots, exact endpoints, repeated eigenvalues and the zero-coupling case. No roundoff epsilon is an exact zero policy.

At fixed coefficients, norm(A-B)<=L_phys²/(tau-R), where L_phys=lambda1+lambda2. One can choose a fixed R>3alpha+2L_phys, because a two-dimensional free trial subspace gives mu1(A)<=3alpha+2L_phys for D>=1. For all sufficiently large D, R<tau; the correction then tends to zero as D^-2. Combining (T5) with finite-dimensional min–max stability proves convergence of these upper/lower energy enclosures. Their gap width is at most twice the correction before finite-bracket widths are added. The finite computation has no missing infinite-tail premise when (Q4), (E4), (T2) and the strict R gate are independently replayed.

## 8. Continuous parameters, work, and the alpha limit

Set kappa_i=lambda_i/alpha. The common rescaling is

\[
 H=\alpha h(\kappa_1,\kappa_2),\quad
 E_k=\alpha e_k,\quad\Delta=\alpha\delta.
 \tag{C1}
\]

Remove the scalar (kappa1+kappa2)I, which leaves gaps unchanged. The remaining potential perturbation has norm at most |delta kappa1|+|delta kappa2|. Min–max therefore gives

\[
 |\delta(\kappa)-\delta(\kappa')|
 \le2\big(|\kappa_1-\kappa'_1|+|\kappa_2-\kappa'_2|\big).
 \tag{C2}
\]

A certified point lower bound b controls a rectangle of half-widths r1,r2 by b-2(r1+r2). A finite rectangle cover proves a common positive lower bound on an entire declared compact parameter region only if its exact coverage and every margin are checked. Independently, (F2) gives a closed-form common bound over 0<=kappa_i<=K_i; alpha>=alpha_min>0 then converts it into a physical energy bound. Excited branches need not be differentiable at a crossing; Lipschitz continuity suffices. The ground eigenvalue is simple, so Hellmann–Feynman gives partial E0/partial lambda_i=<1-coordinate_i>.

The common/difference variables make the forward operator and backward bounds share the same quantities:

\[
 \kappa_+=(\lambda_1+\lambda_2)/\alpha,\qquad
 \kappa_-=(\lambda_1-\lambda_2)/\alpha,\qquad
 \kappa_+\ge|\kappa_-|,
\]

\[
 H/\alpha=K+\kappa_+I
 -\tfrac12[\kappa_+(x+y)+\kappa_-(x-y)].
 \tag{C5}
\]

The inverse map is kappa1=(kappa_++kappa_-)/2, kappa2=(kappa_+-kappa_-)/2. The perturbation norm after dropping the scalar is at most max(|delta kappa_+|,|delta kappa_-|), since (|p+q|+|p-q|)/2=max(|p|,|q|). Thus the gap is 2-Lipschitz in the maximum norm of this pair. Exchange of the two loops maps kappa_- to -kappa_- and preserves the full spectrum. The first gap is consequently even in kappa_-, but evenness does not imply differentiability at a degenerate excited level. The work identity becomes dot alpha<K>+dot lambda_sum<1-(x+y)/2>-dot lambda_difference<(x-y)/2>, where lambda_sum=lambda1+lambda2 and lambda_difference=lambda1-lambda2; this is exactly the same coefficient transformation, not an additional driver.

For prescribed differentiable drivers lambda_i(t), the energy/work balance on a sufficiently regular solution of i partial_t psi=H(t)psi is

\[
 \frac d{dt}\langle H(t)\rangle
 =\dot\lambda_1\langle1-x\rangle+\dot\lambda_2\langle1-y\rangle.
 \tag{C3}
\]

If alpha varies, add dot alpha <K>. A sufficient working contract is continuously differentiable finite drivers, alpha bounded below on the finite time interval, a common domain D(K), and a solution with the domain/form regularity that justifies differentiation and finite <K>. Smooth initial states with the smooth group potentials give the usual strong common-domain evolution. An arbitrary L² state does not automatically have a finite energy derivative. A time-dependent coefficient is external support doing work, not energy created by the isolated gauge system. An instantaneous spectral gap does not by itself prove adiabatic following.

Positivity is not uniform as alpha approaches zero at fixed nonzero magnetic coefficients. Here is an explicit same-model check. Write x=cos theta_U,y=cos theta_V. On separately central trial functions the product-Haar unitary uses sin theta_U sin theta_V; C_U+C_V becomes -(partial_U²+partial_V²)/4-1/2. In the physical form space take the two-dimensional span of the products sin(pi theta_U/w)sin(pi theta_V/w) and sin(2pi theta_U/w)sin(pi theta_V/w), supported on [0,w]^2 and extended by zero. Divide by the Haar sine factors when mapping back to the physical functions. They are admissible form states. The product Casimir expectation is at most 5pi²/(4w²)-1/2, and (K2), together with 1-cos theta<=theta²/2, gives

\[
 0<\Delta\le E_1\le\frac{25\pi^2\alpha}{4w^2}
 +\frac{(\lambda_1+\lambda_2)w^2}{2}.
\]

For lambda1+lambda2>0 choose w^4=25pi²alpha/[2(lambda1+lambda2)], provided w<=pi. Thus

\[
 \Delta\le\frac{5\pi}{\sqrt2}\sqrt{\alpha(\lambda_1+\lambda_2)}\to0,
 \quad\frac\alpha{\lambda_1+\lambda_2}\le\frac{2\pi^2}{25}.
 \tag{C4}
\]

At alpha=0 and nonzero lambda sum the Hamiltonian is multiplication by the potential, with spectrum [0,2(lambda1+lambda2)] and no normalizable zero-energy state. Its minimum set has measure zero. At all coefficients zero every state has zero energy. This does not analyze the matched Kogut–Susskind path, on which the magnetic coefficient is not held fixed as alpha changes.

## 9. Common-variable forward/backward map

The frontiers must name the same graph, domain, physical sector, coefficients and spectral indices. Their common objects here are (G2), Omega and mu, the physical K, alpha and kappa1,kappa2, polynomial degree D, tau, the retained Gram/form matrices, R, and the indexed energy brackets.

| Claim sought backward | Exact prerequisite produced forward | Status here |
|---|---|---|
| physical two-loop observable | all six Gauss constraints and tree orbit map | derived Q1–Q3 |
| interacting operator | full link derivatives, shared orientation, physical measure | derived K1–K5 |
| physical selfadjoint Hamiltonian | inherited group domain or polynomial-core closure | derived D1–D3/E1–E4 |
| fixed-coefficient simple ground and gap | compact resolvent plus positive semigroup | proved F |
| all-finite-coupling explicit positive constant | free physical Poincare plus heat/ground-state comparison | proved F2 |
| precise infinite-space E0,E1 brackets | exact Gram matrices, tail, boundary correction, strict R gate | conditional theorem T1–T6 |
| positive common bound on a parameter region | C2 plus exact certified cover, or F2 plus parameter maxima | proved conditional route |
| regulator removal at this fixed graph | polynomial-core density and vanishing correction | proved above |
| positive graph-volume-uniform bound | common growing-graph family and constants independent of size | unresolved |
| common physical continuum energy | spacing/coupling matching and renormalization with controlled observables | unresolved |
| four-dimensional vacuum and correlations | nontrivial continuum limit and reconstruction/axiom obligations | unresolved |
| four-dimensional pure Yang–Mills mass gap | all previous continuum nodes with one physical scale and dense state family | unresolved |

A Horn/A* planner can verify a route through admitted implications; it cannot turn an unresolved volume or reconstruction node into a theorem. Delete the Gauss/orbit premise and the physical-state claim must disappear. Delete the tail theorem or strict R premise and a finite Ritz value must not imply an infinite-space lower bound. Delete the coverage premise and only pointwise certificates remain. Keep the continuum goal present in the graph but underivable.

| Variable | Classification | Meaningful use |
|---|---|---|
| x,y,z; relative t when defined | existing gauge-invariant configuration coordinates | retain relative orientation and endpoint constraints |
| alpha,lambda1,lambda2 | fixed Hamiltonian coefficients during a spectral calculation | compare models in matched units |
| kappa1,kappa2 | dimensionless parameter ratios | common finite-domain gap statements |
| D | representation/polynomial regulator | remove with explicit tail control |
| lambda_i(t),alpha(t) | prescribed external drivers | account for support work |
| rho multiplying only the shared Casimir | optional existing-link anisotropy / wrong-model control | original uniform contract has rho=1 |
| new scalar or gauge-boson mass | changed physical field content | requires a new action and controlled return to pure Yang–Mills |

No adjustable field has been invented to force a gap. The extra continuous coordinate z/t was already present in the physical configuration space.

### Optional shared-link anisotropy, explicitly separate from the uniform contract

Some solver or rejection fixtures may assign the existing shared link the electric coefficient alpha*rho, while retaining alpha on all other six links. Then

\[
 K_\rho=3(C_U+C_V)+\rho S,
 \qquad S=-\sum_a(L_U^a-R_V^a)^2.
 \tag{RHO1}
\]

This is an action-defined coefficient of an existing electric energy, not a new field. The selected anisotropic extension may restrict rho>0. rho=1 is exactly (H1). Mathematically rho=0 remains elliptic through the six nonshared links; excluding it from a selected numerical certificate is not a singularity claim.

Only A_xx,A_yy,A_xy change in (K3): they become (3+rho)(1-x²)/4, (3+rho)(1-y²)/4, and rho(z-xy)/4. A_xz,A_yz,A_zz remain as displayed. The x,y drifts become -3(3+rho)x/4 and -3(3+rho)y/4; the z drift remains -9z/2. The measure and domain are unchanged for finite rho>=0. The monomial electric energies are

\[
 \epsilon_{abc}(\rho)=3j(j+1)+3k(k+1)+\rho\ell(\ell+1),
 \tag{RHO2}
\]

with the same j,k,ell in (E2). For a general positive rational rho the exact first-omitted-shell threshold is alpha times the finite minimum of (RHO2) over a+b+c=D+1. Removing one positive exponent from any later shell decreases the associated j,k,ell coordinatewise and strictly decreases at least one positive-Casimir contribution. Repeating the reduction reaches degree D+1, proving that no later shell falls below this minimum. At rho=1 it reduces to (E3).

The exact physical electric gap for rho>=0 is

\[
 \gamma_\rho=\min\{3(3+\rho)/4,9/2\}.
 \tag{RHO3}
\]

The possible nontrivial single-loop sectors have one of j,k zero and energy at least 3(3+rho)/4. If both j,k are nonzero their three-link contributions alone are at least 9/2, attained at j=k=1/2,ell=0. This proves (RHO3) without relying only on the first polynomial shell. The same heat-kernel proof applies because exp(-t rho S) remains a probability average, so

\[
 \Delta_\rho\ge\frac{81}{625}\alpha\gamma_\rho
 e^{-16\kappa_+/3}.
 \tag{RHO4}
\]

All parameter/source matches in an anisotropic certificate must use its rho in the operator, free threshold, and prefactor. The simpler bound is alpha*gamma_rho-lambda1-lambda2. The parameter Lipschitz results above hold at fixed rho; they do not control changes of the unbounded electric operator when rho varies. The machine-readable rules keep the two domains separate.

## 10. Source depth, limitations, and next discriminating experiments

The source review was targeted and current on the date above. The primary two-plaquette paper was read in selected equation-level sections: original link/Gauss normalization, maximal-tree expression, its two-plaquette Hamiltonian, and its low electric spectrum. The fully gauge-fixed paper was read in selected sections on the residual charge and maximal-tree construction. The original Kogut–Susskind article was inspected at publisher metadata/abstract depth only. No source's numerical code or hardware experiment was executed. The supplied one-square notes and coordinate proof were read directly, but old numerical gate counts were not re-certified in this advisor task.

The arXiv abstract records inspected expose v1 histories for 2512.22782 (28 December 2025) and 2409.10610 (16 September 2024). Their HTML renderings display an additional 24 August 2026 date. We preserve that discrepancy in sources.json and do not invent an arXiv v2 or treat the rendering date as a verified submission revision. An attempted unlisted v2 URL was unavailable. Equation values relevant to the bounded calculation were still directly inspectable.

The original Hamiltonian framework predates this project. [Kogut–Susskind, publisher record](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.11.395). The official Millennium problem remains a distinct unsolved four-dimensional target. [Clay Mathematics Institute](https://www.claymath.org/millennium/yang-mills-the-maths-gap/).

Ranked experiments are recorded in experiments.json. The decisive immediate experiment is an independent unreduced seven-link SU(2) derivative calculation against K4 on nonlinear trace polynomials, with omitted-dagger, cross-sign, and independent-rotor mutations. The solver's exact polynomial Gram/inertia route can then certify retained cases including zero, unequal and stronger magnetic coefficients. Its finite numerical arithmetic must be independently replayed. A complete pointwise finite-graph proof is already available analytically; numerical work is justified by the narrower question of informative enclosures and detecting a wrong physical operator.

The next mathematical extension worth attempting is a third square with its actual link graph and invariant algebra, preserving a common electric normalization and studying how the positivity constants degrade. A few positive finite graphs, a smooth fitted trend, or a renamed coefficient cannot discharge the growing-volume and continuum premises.

## 11. Review state at advisor handoff

The round-11 skeptic independently agreed with the shared-link orientation, every K3 coefficient, K5 low-polynomial identities, the constant Haar density, the heat-kernel/Poincare constants in F2, and the need for the inherited domain. Its exact link-derivative and quotient-moment checks are separate artifacts owned by that reviewer. Their reported pass counts are not adopted as this document's own executed evidence. The solver independently identified the same polynomial representation labels; the argument in Section 5 closes that bridge directly using the degree flag.

The advisor-owned symbolic consistency checks and their raw results are in advisor_checks.py and advisor_checks.json. They check algebraic obligations, not independent physics or a proof assistant formalization. The theorem inventory separates derived proofs from conditional numerical certification and unresolved continuum obligations. This handoff should be read together with the independent solver/verifier verdict before numerical values are promoted.
