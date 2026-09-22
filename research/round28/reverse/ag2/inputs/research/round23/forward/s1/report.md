# S1 forward — actual cubic local source and a boundary-complete partial inverse

The frozen O1 cubic word has a provably nonzero actual SU2 vacuum source at every nonzero tau. Its identity-extended interior inverse is bounded and preserves the actual operator domain. The exact full-volume defect retains three crossing stars at the origin, each on a connected seven-site union, with an explicit O(|tau|^4) upper bound. This does **not** solve the full all-sector source equation: a spectral solvability and all-order connected-support argument remain absent. The S target is limited; the source and partial-inverse statements below are proved.

This independent forward derivation uses only the frozen S1 contract and inherited sources. Current Round23 reverse/skeptic solutions were not read. No S2 has been selected or executed by this worker.

## 1. The generated source, including its nonvanishing proof

Use the actual complete24-link I1 block spaces and origin star Y={0,e_x,e_y,e_z}. H=H0,Y is the nonnegative unbounded tensor-sum operator, H>=Q, with unique product ground Ω. Set v=phi_0 Ω, u=H_Q^-1 v, a=<u,v>, s²=||u||², sigma=||v||=sqrt(7/12)|tau|. The inherited inverse gives u in D(H), Hu=v, u perpendicular Ω. At tau≠0 the actual Haar variance makes v≠0, so a>0 and s²>0 by positive spectral calculus. Define S=|u><Ω|-adjoint and A=|v><Ω|+adjoint exactly as O1.

The frozen operator

C=(1/2)[S,[S,phi_0]]-(1/6)[S,[S,A]]

is one actual n=2 repeated-anchor term of the convergent O1 remainder. Both factorials and repeated anchors are retained. This identifies a genuine term in the declared decomposition; it does not identify it with the total cubic coefficient or full remainder. All these commutators are of bounded operators, so C is bounded self-adjoint. Write b=<u,phi_0 u>, which is real. Direct multiplication gives

    ad_S²(phi_0) Ω = -3a u + 2b Ω - s² v,
    ad_S²(A) Ω = -3a u - s² v,
    w=Q C Ω = -a u -(s²/3)v,
    <u,w> = -(4/3)a s² < 0,                         (1)
    <Ω,C Ω>=b.

Thus r=||w|| is strictly positive at every nonzero frozen tau. These statements concern the actual infinite-dimensional Hilbert space, without a representation cutoff or a numerical inverse. They also give

    r <= (4/3)s² sigma <= (4/3)sigma³,
    ||C|| <= 2s² M +(2/3)s² sigma,  M=7|tau|.      (2)

The exact O2 split is C=b I+A_gen+Q(C-bI)Q, A_gen=|w><Ω|+adjoint. It retains the scalar, local mixing and centered diagonal on declared Y. Tau=0 gives all zero. Reversing tau changes u,v,w,C sign according to degrees1,1,3,3; a,s² stay even. No scalar, coupling or clock is fitted.

## 2. Interior inverse and unbounded domain

Only the origin anchor has its complete star contained in Y. Thus G_Y=H+D_0 with D_0=Q phi_0 Q and ||D_0||<=M. On the form domain, |D_0| in quadratic-form sense is bounded by M Q<=M H. Consequently

    (1-M)H <= G_Y <= (1+M)H,
    D(G_Y)=D(H),  G_Y|Q >= g_Y=1-M>0.             (3)

The operator-domain equality follows from bounded perturbation, independently of the form inequality. The frozen interval gives M<=35/1664 and g_Y>=1629/1664. Define z=(G_Y|Q)^-1 w and K_Y=|z><Ω|-adjoint. Then

    ||z||<=r/g_Y,   z in D(H),
    ||H z||=||w-D_0 z||<=r/g_Y,
    [K_Y,G_Y]=-A_gen on D(H).                     (4)

The commutator sign follows G_Y K_Y=|w><Ω| and K_Y G_Y=-|Ω><w|. Extending K_Y by identity on the complementary tensor factors does not regularize them. It preserves D(H0,Lambda): exterior spectral projections commute with K_Y, and the local bounded commutator with H gives H0 K_Y=K_Y H0+[H,K_Y]. Its H0 graph norm is bounded by 2r/g_Y. Therefore exp(±theta K_Y) preserves that domain by its Banach-space exponential and inverse. In finite volume G_Lambda differs from H0,Lambda by a bounded operator, giving the same common domain. None of this constructs an infinite global unitary.

## 3. Exact crossing terms and useful first-step connected sums

For every finite cuboid containing Y, keep only complete retained stars, and let B_Lambda(Y)={c: Z_c meets Y, Z_c not contained in Y, Z_c subset Lambda}. On D(H0,Lambda), the exact identity is

    [K_Y tensor I,G_Lambda]+A_gen tensor I
       = E_Y = sum_(c in B_Lambda(Y)) [K_Y,D_c].   (5)

Every D_c retains all21 omitted faces and both Q_c factors. Disjointness uses complete factor support, never incidence of one physical probe link. A nonnegative anchor meeting the origin Y must be 0,e_x,e_y or e_z. The first is interior; the other three are crossing if their stars are retained. Each crossing union Y union Z_c is connected and has exactly7 sites. Therefore

    ||E_Y|| <= 6 M r/g_Y,
    ||E_Y||_mu <= 6 exp(7mu) M r/g_Y.             (6)

The second bound uses the indexed decomposition in (5), and is a single-source weighted root sum. It is uniform in the containing cuboid, with missing boundary stars only decreasing it. Substitution of (2) makes its unweighted right side at most 56(7/12)^(3/2)|tau|^4/(1-7|tau|). This is an upper certificate, not an actual nonzero defect evaluation for this cubic source.

For clarity on a family, translate this same single-star construction to each retained b, with r_* an upper bound on its source norm. In the interior, the possible relative anchors are S-S: zero, ±e_i and e_i-e_j for i≠j, exactly13. Twelve are crossing; all meet in one site, and the union has7 sites. For a fixed root, at most4 source stars contain it, each with12 crossing choices; assigning the root to the other star contributes at most another48 indexed pairs. Retaining this harmless overcount gives

    ||sum_(b,c crossing) [K_b,D_c]||_mu
       <=192 exp(7mu) M r_*/g_Y.                 (7)

This is a finite connected-support one-step interaction certificate at any fixed mu>0, with no weight loss. It preserves ordered pair multiplicity. It is **not** a convergent all-order inverse or a later-diagonal contraction. Connected addition of further stars would give |support|<=4+3n, but their coefficient sums and solvability must actually be proved; this support cardinality alone supplies no geometric series.

## 4. Actual exterior-sector discrimination

The R2 global vacuum inverse on finite Lambda constructs a rank-two K_vac whose commutator cancels A_gen tensor P_ext. This differs from the frozen source A_gen tensor I_ext. For a cuboid large enough, choose the actual free z-link with physical tail (8,0,0), owned by coarse2e_x outside Y. Its fundamental character chi=Tr(g_e) has Haar mean zero and squared norm one. Let eta be this character times the unchanged exterior strip/free vacuum. Then

    (A_gen tensor P_ext)(Ω_Y tensor eta)=0,
    (A_gen tensor I_ext)(Ω_Y tensor eta)=w tensor eta,
    ||(A_gen tensor (I-P_ext))(Ω_Y tensor eta)||=r>0. (8)

This is an exact actual-Haar test. The character's zero mean and unit second moment follow SU2 character orthogonality; they also follow E[q0]=0 and E[q0²]=1/4 for the uniform unit quaternion since Tr(g)=2q0. No product-ground hypothesis for the full Hamiltonian H0+D+R is introduced. If there is no exterior, or tau=0, this discriminant is zero; those are valid exceptions.

## 5. What prevents promotion to a full operator inverse

Suppose a bounded K preserves D(G_Lambda) and [K,G_Lambda]=-A_gen tensor I holds there. For two eigenvectors of the same energy E, taking their matrix element gives

    E_G({E})(A_gen tensor I)E_G({E})=0.           (9)

For unequal energies the formal inverse divides by their difference. Even a positive ground-to-excited gap leaves possible coincident or arbitrarily close excited energies; it supplies no general bounded inverse of this commutator on arbitrary sources. A three-level exact lemma fixture G=diag(0,1,1), A=|1><2|+adjoint has gap1 and a forbidden block, proving this logical insufficiency. It does **not** show that the actual cubic source has a forbidden block for actual G. Equation(9)'s actual-model test remains open, as does a bounded connected-support full solution. The present work proves neither impossibility nor existence of that full solution.

A possible next target is a regulated commutator inverse with an explicit retained zero/low-frequency residual, applied to this fixed genuine source; its regulator must be a declared proof parameter and its connected-support/weight limit must be checked. Another legitimate target is the actual excited-sector spectral obstruction in a controlled invariant sector. The advisor must select S2 after review, not treat either as already executed.

## Evidence and scope

The standard-library checker independently verifies rank-two algebra with a rational three-level control, exact interior inversion, wrong sign, a crossing commutator, cubic parity, zero coupling, complete star intersections and indexed unions. A symmetric quaternion design integrates precisely the first and second moments used in (8); it is not a full Haar discretization. Matrix fixtures are algebra tests only. The actual source nonvanishing and domain proofs above do not rest on sampled matrices.

Primary-source reading is recorded in source-notes.md. The source extraction and constants are project derivations within the specified model; scientific priority is unverified. Physical energies are delta=alpha/8 times the displayed normalized quantities, with fixed positive a,E_star,alpha/E_star,hbar. The full homogeneous numerical gap, later-diagonal iteration, physical calibration, canonical endpoint dynamics and four-dimensional continuum construction remain open.

Reproduce into a fresh directory:

    python3 -B research/round23/forward/s1/check.py --output /absolute/new/s1-forward
    python3 -B -O research/round23/forward/s1/check.py --output /absolute/new/s1-forward-O
