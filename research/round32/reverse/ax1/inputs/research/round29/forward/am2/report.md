# AM2 forward: HNM four-site quantitative stability certificate

Human project author: **Hruday N M (BUNZEEY)**. The advisor/panel supplied the proposed route and constants. This independent forward derivation checks the entire implication before reading current reverse or skeptic results. Creation expansions are established methods; scientific priority of this application is unverified.

**Proposed admission:** for every finite I1 complete-factor volume, with its actual selected reference, whole-star omitted interactions and both signs of `|tau|<=10^-8`, the full untruncated Hamiltonian has a unique ground and centered gap at least `alpha/16`. Its physical restriction has the same ground and this lower gap. Every nonempty complete-factor volume has nonzero physical excited vectors; the empty volume has none and its gap exclusion is vacuous. This is an alternative explicit finite-volume theorem, not an evaluation of Yarotsky's named constants or a continuum result.

## 1. Actual model and available inverse

Write the normalized operator on a finite set Lambda of complete 24-link factors as

\[
H=H_0+V,\quad H_0=\sum_{x\in\Lambda}h_x,\quad
h_x\Omega_x=0,\quad h_x\ge Q_x=I-|\Omega_x\rangle\langle\Omega_x|,
\quad V=\sum_{b:b+S\subset\Lambda}\phi_b .
\tag{HNM-AM2.1}
\]

All 21 omitted faces per retained anchor are present, `S={0,e_x,e_y,e_z}`, and `||phi_b||=7|tau|`. The indexed per-site sum is

\[
J:=\max_u\sum_{X\ni u}\|V_X\|\le28|\tau|\le J_0={7\over25000000}.
\tag{HNM-AM2.2}
\]

Here each retained X is its complete four-site star, including incoming anchors. The interaction is bounded in each finite volume, though not uniformly bounded as a global extensive operator. All onsite domains and scalar selected ground subtractions are inherited from I1. No interaction term is deleted.

For a nonempty excitation set M, put `P_M=(tensor_{x in M}Q_x)(tensor_{y outside M}P_y)` and identify its range with the excited factor tensor product. On it `H_M=sum_{x in M}h_x>=|M|`. This is a full-Hilbert-space inequality and needs no extra physical four-link floor. For real `|z|<1/2`,

\[
\|H_M^{-1}\|\le|M|^{-1},\qquad
\|(H_M-z)^{-1}\|\le2|M|^{-1}.
\tag{HNM-AM2.3}
\]

First impose finite-rank full spectral cutoffs of each h_x containing its vacuum. The proof below is finite dimensional and constants do not depend on these ranks. Cutoff removal is proved in Section6.

## 2. Creation algebra and complete anchored estimate

For a vector `c_I in tensor_{x in I}Q_x H_x`, define the identity-extended creation `hat(c_I)=|c_I><Omega_I| tensor I_outside`. Two creations commute: disjoint supports commute by tensor factorization, and overlapping supports have product zero in both orders. The latter follows because the vacuum bra annihilates an excited ket at any common factor, first for simple tensors and then by finite-dimensional linearity. Set

`C=sum_{I nonempty}hat(c_I)`, `||c||_a=max_u sum_{I contains u}||c_I||`.

This is a norm on the finite-dimensional direct sum of coefficient spaces. For collections `c_1,...,c_k`, define

\[
(L_k(c_1,\ldots,c_k))_M
=H_M^{-1}P_M\operatorname{ad}_{C_1}\cdots\operatorname{ad}_{C_k}(V)\Omega_0,
\quad\Omega_0=\bigotimes_x\Omega_x .
\tag{HNM-AM2.4}
\]

We derive, rather than copy, the proposed estimate

\[
\|L_k(c_1,\ldots,c_k)\|_a
\le J L_k^{\rm num}\prod_j\|c_j\|_a,
\qquad L_k^{\rm num}=16\,8^k(1+5k/4).
\tag{HNM-AM2.5}
\]

Fix an indexed interaction V_X, `|X|<=p=4`, and creation supports I_j. Every I_j must meet X: commuting adjoint actions allow a disjoint creation to be moved innermost, where it commutes with V_X. Write `N=union_j I_j`. In any nonzero term, outside X a singly touched factor is excited and a multiply touched factor annihilates the term. Therefore `N\X subset M subset N union X`. There are at most `2^p=16` possible output support sets M, independent of Hilbert dimensions, and `|I_j|<=|M|+p`. The commutator expansion has `2^k` products; each projected product norm is at most `||V_X|| product_j||c_{j,I_j}||`.

For a fixed root u in M, first count terms with u in X. Use inverse bound one, sum X containing u at cost J, and for every collection use `sum_{I:I intersects X}||c_I||<=p||c||_a`. This contributes `2^p(2p)^k J product||c_j||_a`.

Otherwise u lies in at least one I_l; overcount all k choices of l. Since M is nonempty,

`1/|M| <= (p+1)/|I_l|`.

Sum interactions meeting I_l at cost `J|I_l|`, canceling that denominator; sum the remaining collections meeting X at cost `p^(k-1)`, and sum I_l containing u with its anchored norm. This contributes `2^p(2p)^k k(p+1)/p` times the same J product. Adding the two root placements and setting p=4 gives (HNM-AM2.5). All sums are finite; repeated interaction supports and repeated creation histories are counted, not canceled to improve the bound.

The nested commutator is zero for k>2p=8. In each expanded product, one side of V_X would contain at least five creations all meeting the four-site X. Two share a site, so that product is zero. An exact four-qubit algebra fixture gives `ad_C^8(V)Omega=8!|1111>` and `ad_C^9(V)=0`; thus importing a support-three termination at order six would be wrong. This fixture audits the algebra, not a rotor truncation or a numerical spectrum.

## 3. Fixed point, scalar energy and all orders

Because creators commute, `[C,H_0]=-sum_I hat(H_I c_I)` and its next creation commutator vanishes. Thus

\[
e^C(H_0+sV)e^{-C}=H_0-\sum_I\widehat{H_Ic_I}+s e^CVe^{-C}.
\tag{HNM-AM2.6}
\]

All exponential products are finite polynomials: C is nilpotent since nonzero creator products have disjoint nonempty supports. For real `|s|<=1`, `psi(s)=e^{-C(s)}Omega_0` is an eigenvector precisely when

\[
c=s\sum_{k=0}^{8}{L_k(c,\ldots,c)\over k!},\qquad
E(s)=s\langle\Omega_0,e^{C(s)}Ve^{-C(s)}\Omega_0\rangle .
\tag{HNM-AM2.7}
\]

The vacuum coefficient of psi is one, so it never vanishes. The scalar equation is retained even when the original reference vacuum mean of V is zero. All diagonal pieces of V remain inside every commutator and the scalar; this is not an offdiagonal-only model.

The positive all-order majorant and derivative are

\[
G(t)=\sum_{k\ge0}{L_k^{\rm num}t^k\over k!}
=16e^{8t}(1+10t),\quad
G'(t)=16e^{8t}(18+80t).
\tag{HNM-AM2.8}
\]

For R=1/64, `exp(1/8)<8/7`, by comparison of its positive power series with the geometric series (strict already at second order). Hence

\[
G(R)<148/7,\quad G'(R)<352,\quad
J_0G(R)<148/25000000<R,\quad
J_0G'(R)<77/781250,\quad 2J_0G'(R)<77/390625<1.
\tag{HNM-AM2.9}
\]

The multilinear bound proves the ball self-map. Telescoping each k-linear term between two coefficient collections in the radius-R ball yields the Lipschitz bound `J G'(R)`, with all k possible replacements counted. Banach's theorem supplies a unique coefficient solution there. Subtracting the fixed-point equations and absorbing the common Lipschitz factor gives continuity in s. Therefore E(s) is a continuous real eigenvalue branch. At J=0, c=0 and E=0 exactly.

## 4. Excited-sector exclusion: construction alone is not enough

Suppose a second eigenvector phi of `H_0+sV` has eigenvalue `E(s)+z`, real `|z|<1/2`, and is independent of psi. Decompose

`e^{C(s)}phi=b_0 Omega_0+sum_{M nonempty} b_M`, and set `B=sum_M hat(b_M)`.

Then `phi=(b_0+B)psi` because creations commute, and b is nonzero. Subtract the eigenvector equations, conjugate by e^C, and project each nonempty sector. Creation commutation cancels the creation term in (HNM-AM2.6), giving

\[
b_M=s(H_M-z)^{-1}P_M[B,e^{C(s)}Ve^{-C(s)}]\Omega_0.
\tag{HNM-AM2.10}
\]

The scalar equation may additionally constrain b_0, but is unnecessary for excluding b!=0. Expanding the remaining commutator keeps all terms through total creation order eight. The shifted inverse multiplies (HNM-AM2.5) by at most two. Treating b as one input and summing the other orders gives

`||b||_a <= 2J G'(R)||b||_a < ||b||_a`, a contradiction.

Thus the branch is simple and no other eigenvalue lies within one half. At s=0 it is the unique lowest eigenvalue; continuous finite-dimensional eigenvalues cannot cross this isolated branch. It remains the ground for every real `|s|<=1`, with full-space gap at least one half. The argument includes tau of either sign and equality at the contracted tau cap. It does not interpret rejection beyond the chosen cap as actual gap failure.

## 5. Gauge and physical sector

Every onsite selected-strip/free-link operator commutes with the original gauge actions at all owned-link endpoints, including heads outside the tail volume. Its unique positive ground is fixed by these actions. Hence P_x,Q_x, every spectral cutoff and H_M commute with gauge actions. The fixed-point map preserves invariant collections; uniqueness gives invariant C and psi. Equivalently the unique full ground is fixed under the finite product of endpoint SU(2) groups. The physical subspace reduces the full Hamiltonian, so the full-space gap restricts to it with the same vacuum.

For a nonempty complete-factor volume, choose a selected square in any factor. The full finite-volume ground is smooth and strictly positive on the connected compact product of link groups, including both signs of its bounded real potential. The gauge-invariant vector `(W_p-<W_p>)Omega_H` is nonzero, is in the operator domain and is orthogonal to the ground. This proves a genuine nonzero physical excited sector. The empty volume is one dimensional and is treated separately.

## 6. Untruncated compact-domain passage

Each actual h_x is an elliptic Casimir sum plus bounded smooth selected potential and a scalar shift on the compact manifold `SU(2)^24`. It is self-adjoint on the Casimir domain and has compact resolvent. Choose increasing full spectral projections Q_(x,N) containing its ground and tending strongly to the identity. They commute with gauge actions. The product cutoff Q_N commutes with H_0, and compressed interactions retain support and do not increase J. The preceding estimates are uniform in N.

Finite tensor products of onsite eigenvectors form a form core for H_0: spectral tails of `||u||²+<u,H_0u>` tend to zero. Since V is bounded in each fixed finite volume, the same union is a form core for `H_0+sV`, after a harmless scalar lower-bound shift. Compact resolvent persists. By min–max, the first two cutoff eigenvalues converge downward to the first two full eigenvalues: form approximation to their finite-dimensional eigenspaces proves the upper limit, while the variational principle gives the lower limit. The uniform cutoff inequality therefore gives `E_1-E_0>=1/2` for the untruncated operator. The same core argument applies on the physical subspace because Q_N commutes with gauge actions; its nonzero sector was established separately.

No infinite-volume bounded global creator, similarity transform or unitary is asserted. The normalized physical energy is restored using the original scalar relation: after actual ground subtraction,

\[
\Delta_{\rm physical}\ge{\alpha\over8}\,{1\over2}={\alpha\over16},
\qquad\Delta/E_\star\ge{\alpha\over16E_\star},
\quad\hbox{frequency threshold }\alpha/(16\hbar).
\tag{HNM-AM2.11}
\]

## Evidence and scope

The exact checker verifies the anchored combinatorial constants, complete four-site termination example, certified exponential enclosure, radius inequalities, shifted-inverse bound, zero/equality cases, scalar/diagonal controls and the I1 J conversion. These audit the analytic proof; passing a polynomial or a finite cutoff alone is not this theorem. The admitted result, if independent review confirms the argument, is a conservative uniform **finite-volume** radius for the complete original I1 family. It does not evaluate Yarotsky's c1,c2, select an infinite-volume state, prove AN's boundary comparison or repair AL's weak-coupling obstruction. Subsequent infinite-volume or continuum claims need their own complete arguments.

Reproduce: `python -B research/round29/forward/am2/check.py --output /absolute/new/output`.
