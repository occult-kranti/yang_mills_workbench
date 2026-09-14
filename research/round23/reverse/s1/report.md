# S1 reverse — an actual cubic source and the full-operator boundary

The frozen cubic O1 term has an exactly identified, nonzero actual SU(2) vacuum-mixing source for every nonzero allowed tau. Its initial interacting **interior** inverse is a bounded graph-domain-preserving local operator. Extending that inverse by identity leaves the explicitly supported crossing commutators. A global vacuum inverse addresses a different source. The full all-sector local-source inverse and useful all-order connected-support sum remain **unresolved**; the positive initial ground gap does not establish them.

This independent derivation uses the frozen S1 contract and inherited reports. The advisor's shared choice of a cubic same-anchor term came from forward preparation and is disclosed in the contract. No current forward or skeptic solution was read. This is one executed research loop, not an all-stage stability construction.

## 1. Recover the generated source from its defining expression

Use the homogeneous full-link O1/R model on the positive coarse octant, with its actual 24-link onsite factors and selected-strip/free reference. For the origin star `Y={0,e_x,e_y,e_z}`, put

`v=phi_0 Omega`, `u=(H0_Y|Q)^(-1)v`, `c=<u,v>`, `beta=||u||^2`,

`S=|u><Omega|-|Omega><u|`, `A=|v><Omega|+|Omega><v|`, `D=Q phi_0 Q`.

Thus `phi_0=A+D`, `D Omega=0`, `H0_Y u=v`, and `<Omega,u>=<Omega,v>=0`. These are actual Hilbert-space vectors, not truncated spin states. The inherited independent-Haar argument is also checked against the actual link geometry: each of the 21 omitted faces has at least two free links; each distinct pair has an unmatched independent free link. Conditional Haar invariance gives `<W_f^2>=1/4`, while all 210 distinct-face cross moments vanish. Hence

`||v||^2=7 tau^2/12`.

For the contract's genuine indexed O1 term

`C=(1/2)[S,[S,phi_0]]-(1/6)[S,[S,A]]`,

calculate its source without substituting a diagnostic vector. Since

`S^2=-|u><u|-beta P`, `phi_0 u=c Omega+D u`,

we obtain

`Q S^2 phi_0 Omega=-c u`,
`Q S phi_0 S Omega=c u`,
`Q phi_0 S^2 Omega=-beta v`.

Consequently `Q ad_S^2(phi_0)Omega=-3c u-beta v`. Replacing phi_0 by A gives the same Q component; the D contribution is purely vacuum in this expression. Applying the two frozen BCH coefficients yields

\[
\boxed{w:=QC\Omega=-c u-\frac{\beta}{3}v.}\tag{1}
\]

There is no assumption about `<u,D u>` being zero. Its vacuum contribution drops because the target is Q C Omega. Keeping the `1/6` term is essential; omitting it changes the source by a factor 3/2.

For nonzero tau, v is nonzero and positivity of the reduced inverse gives `c=<u,H0_Y u>>0`, with beta positive. Therefore

\[
\boxed{\langle v,w\rangle=-c^2-\frac\beta3\|v\|^2<0.}\tag{2}
\]

This proves a nonzero actual source without replacing its true energy denominators. It also gives `||w|| >= (c^2+beta||v||^2/3)/||v||`. Because the bare gap is at least one,

`||u||<=||v||`, `c<=||v||^2`, `beta<=||v||^2`,

so

\[
\|w\|\le\frac43\|v\|^3
 =\frac43(7/12)^{3/2}|\tau|^3.\tag{3}
\]

At tau zero all quantities vanish; changing tau's sign reverses w. This degree-three indexed term is not the full resummed O1 remainder, and its nonzero mixing does not prevent other indexed terms from canceling it in a grouped remainder. The contract selected this term itself.

The coefficients c and beta are calculated source observables, both dimensionless in the frozen normalization, and homogeneous of degree two in tau. They are not adjustable physical fields or fitted constants. Equation (1) is an exact project derivation from the known commutator construction; scientific priority is unverified.

## 2. Interior inverse and actual graph domain

Only the anchor zero star is wholly contained in Y. Define

`G_Y=H0_Y+D_0`, `D_0=Q_Y phi_0 Q_Y`, `g_Y=1-7|tau|`.

The finite local D_0 is bounded and annihilates Omega. Since `Q_Y<=H0_Y`,

`|<psi,D_0 psi>|<=7|tau|<psi,H0_Y psi>`.

Thus `G_Y>=g_Y H0_Y>=g_Y Q_Y`, and its operator domain is exactly `D(H0_Y)` by bounded self-adjoint perturbation. On the frozen interval, `g_Y>=1629/1664>0`. Set

`z=(G_Y|Q_Y)^(-1)w`, `L_Y=|z><Omega_Y|-|Omega_Y><z|`.

Then `z in D(G_Y)=D(H0_Y)`, `G_Y z=w`, and

\[
\|L_Y\|=\|z\|\le\|w\|/g_Y,\qquad
[L_Y,G_Y]=-A_{\rm gen},\quad
A_{\rm gen}=|w\rangle\langle\Omega_Y|+\text{adjoint}.\tag{4}
\]

The first commutator identity holds on the operator domain and extends boundedly. No premise that an arbitrary local bounded source preserves this domain is needed: the inverse places z in it. The range of L_Y lies in the domain; its exponential preserves the local domain, as does its inverse.

In a finite containing cuboid Lambda, extend L_Y by the identity on the exterior. Nonnegative commuting local/exterior Hamiltonians give

`D(H0_Lambda)=D(H0_Y) intersect D(H0_ext)`.

L_Y preserves the first domain and commutes with exterior spectral projections, so it preserves their intersection. It does not regularize an arbitrary exterior vector into this domain. All finitely many retained D_b are bounded, hence `D(G_Lambda)=D(H0_Lambda)`. Boundedness of the first commutator also bounds L_Y on the H0 graph norm, so its exponential and inverse preserve the full domain. This is a finite-volume operator-domain statement. R2's infinite form construction does not establish equality of its global operator domain with D(H0), and no such equality is asserted here.

## 3. Crossing defect and connected-support accounting

All stars disjoint from Y commute with L_Y. The exact full-volume identity is

\[
[L_Y\otimes I,G_\Lambda]
=-A_{\rm gen}\otimes I+
\sum_{\substack{B_b\cap Y\ne\varnothing\\B_b\not\subset Y\\B_b\subset\Lambda}}
 [L_Y,D_b].\tag{5}
\]

Each summand retains the declared connected support `Y union B_b`. For the origin star in the positive octant, the possible crossing anchors are exactly `e_x,e_y,e_z`; each union has seven sites. Boundary truncation retains only those whose complete stars lie in Lambda. In a bulk translate, the 13 possible meeting displacements are `G-G`; after deleting the identical star there are 12 crossings, including nine anchors with at least one coordinate below the seed anchor. These incoming crossings cannot be removed by a physical probe-link incidence argument.

With `ell=||L_Y||`, every term satisfies

`||[L_Y,D_b]||<=14|tau| ell`.

For this one origin generator, the full defect therefore has norm at most `42|tau| ell`. Its interaction norm at weight mu is at most `42 exp(7mu)|tau|ell`, in the declared decomposition. This is an upper bound; it is not a lower certificate that the actual defect is nonzero.

For a family of translated seeds with common bound ell, keep **ordered** crossing pairs. There are 12 relative displacements and, for each pair union, seven translations putting a fixed root in that union. Consequently the root multiplicity is at most 84, with finite boundaries only reducing it. Thus

\[
\|E\|_\mu\le1176 e^{7\mu}|\tau|\ell.\tag{6}
\]

At mu=log 2 its coefficient is 150528; the single-origin coefficient is 5376. These constants refer to distinct declared decompositions and are not interchanged. They include repeated indexed unions when different ordered pairs generate the same set.

More generally, a nested word that can be nonzero must attach each new star to the accumulated union, which may grow by at most three sites. Its support obeys `|Y_n|<=4+3n`. This connected-word fact does not by itself sum the multiplicities or control the inverse of the full operator commutator. It removes the need to assign a whole cubic collar to each individual word, while leaving the all-order analytic estimate open. An all-order inversion is not established by the finite checks through word depth three.

## 4. Excited exteriors and the necessary resonance condition

The inherited R2 global-vacuum construction can solve a rank-two equation with source `A_gen tensor P_ext`. The desired source here is `A_gen tensor I_ext`. Choose a free z-link character at a coarse site outside Y, for example the block at `2e_x`, and let `xi=chi_f Omega_ext`. Its normalized Haar factor gives `<Omega_ext,xi>=0` and `||xi||=1`, preserving the selected-strip ground. Then

`(A_gen tensor P_ext)(Omega_Y tensor xi)=0`,

`(A_gen tensor I_ext)(Omega_Y tensor xi)=w tensor xi`.

The squared mismatch is exactly `||w||^2`, strictly positive by (2). This is an actual SU(2) exterior-state test. The full physical state completion is retained; a local probe coordinate is not substituted for an entire factor.

For a bounded graph-preserving solution `[L,G]=-A`, every pair of vectors in the same energy eigenspace must satisfy `<psi,A eta>=0`. Indeed the commutator matrix element is `(E-E)<psi,L eta>=0`. In finite volume this gives the necessary condition

\[
P_E A P_E=0\quad\text{for every energy E}.\tag{7}
\]

For distinct eigenvalues the formal coefficient is `L_mn=-A_mn/(E_n-E_m)`. An actual inverse further needs a bounded divided-difference operator in the chosen class, graph-domain control, and a useful interaction-support estimate. A positive vacuum gap controls the vacuum-to-excited denominators only. It supplies none of these bounds between arbitrary excited energies. Degeneracy and small excited-energy differences must be addressed explicitly.

The checker constructs a two-qubit **generic inference falsifier**, with H0 diagonal `(0,1,1,2)` and an excited-sector offdiagonal D between the second and fourth basis vectors. Let `t=1/10`, `d=t/(1-t^2)=10/99`. G has the exact eigenvector `(0,1,0,-t)` with energy `98/99`, while the identity-extended source `X tensor I` has normalized expectation `-20/101` there. G has a unique zero vacuum and a positive gap. Its source therefore cannot be a commutator with G. This rejects the inference that ground positivity alone supplies the all-sector inverse. It does **not** prove a nonzero equal-energy block for the actual SU(2) G and actual generated source. That physical-model obstruction is unresolved.

## 5. Checks, reading depth and next missing premise

The exact Fraction checker tests the frozen BCH source against independent finite matrices with noncommuting D, the correct interior inverse sign, zero and both coupling signs, actual omitted-face Haar geometry, crossing anchors and ordered root counts. It rejects deletion of the `1/6` BCH term, the opposite inverse sign, the vacuum-projector substitution, and a universal excited-sector inverse. Finite matrix fixtures are algebra checks, not SU(2) spectral approximations. Explicit exceptions retain checks under Python optimization.

Primary-source scope is inherited: I2/O1 checked Yarotsky's [primary theorem and fixed-point setup](https://arxiv.org/pdf/math-ph/0411042), while R1/R2 checked [unbounded-interaction Lie-Schwinger domains](https://arxiv.org/pdf/2108.13907) and [Teschl's closed-form representation](https://www.mat.univie.ac.at/~gerald/ftp/book-schroe/schroe.pdf). This loop read the inherited reports and I2 checker; it did not reread these complete primary proofs or extract their unspecified stability constants. Equations (1)–(7) are derived directly above. No novelty comparison sufficient for scientific priority has been completed.

A useful S2 candidate is a filtered full-source inverse with a disclosed retained resonance error, proved graph domains and connected-support weights. It must target the actual A_gen tensor I and report an error that survives its regulator limit if resonant components remain. Alternatively S2 could seek an actual-G equal-energy matrix element or a sharper structured operator estimate. These are proposals only; S2 belongs to the advisor after S1 review.

All energies here are dimensionless until multiplied by `delta=alpha/8`; lattice spacing a, E_star, alpha/E_star and hbar remain positive and fixed. The inverse construction does not fit a clock. Tau remains the inherited homogeneous action coefficient. This result supplies neither the full homogeneous numerical gap, later-diagonal iteration, physical calibration, canonical endpoint dynamics, nor a four-dimensional continuum theory.

Reproduce with `python3 -B research/round23/reverse/s1/check.py --output /tmp/ym23-reverse-s1-fresh` and an independently fresh `python3 -O -B` run. Source and output hashes are bound in the manifest and frozen submission.
