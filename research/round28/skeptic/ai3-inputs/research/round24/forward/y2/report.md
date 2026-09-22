# Y2 forward — the actual demodulated endpoint has a scalar limit

Independent forward derivation before current reverse Y2. Exactly the canonical M/N/U model and U1 observable are used. Newton's synthesis requires a justified limit of the original functional; Tesla's resonance check retains the entire energy eigenspace and all spatial return channels. Independent model-agent work is not external peer review. The frozen contract and instruction snapshots govern; historical solo and stop notes are superseded by the current authorized team task.

For fixed positive physical scales, eta in (0,1), and 0<z=C eta<=10^-6, the result is

    F_q(z):=exp(i E T_q/hbar) C_q(T_q) -> L(z),
    E=9alpha/2, T_q=C(hbar/alpha)(1-q)^-3.             (Y2.1)

The limiting scalar is characterized by finite-dimensional **whole reference-energy blocks of finite spatial regions**, with an explicit spatial error below. Those blocks are defined by the actual untruncated strip operators; their spectra and matrices have not been numerically assembled. A certified disk for L(10^-6) is given, not a plotted or computed trajectory. Neither a global q=1 Hamiltonian nor operator-norm weak-coupling averaging is assumed or obtained.

## Actual finite-region spectral problem

Use the forward Y1 regions F_k and internally supported omitted faces O_k, including all links of every reference factor. Thus O_0 has one face, O_1 has 20 faces on 98 links/35 factors, and O_2 has 129 faces on 297 links/135 factors. These differ from reverse Y1's 19 and 125 retained faces. Let N_k=|O_k|. On the complete Haar space of E(F_k), define dimensionless operators

    K_k=H_(0,F_k)/alpha,
    A_(q,k)=-(1/24) sum_(f in O_k) q^r_f x_f,
    A_k=-(1/24) sum_(f in O_k) x_f,   r_f=|anchor(f)|_1,
    H_(q,F_k)=alpha(K_k+tau_q A_(q,k)).              (Y2.2)

The complete-strip reference is the sum of its electric Casimirs and the three bounded Wilson potentials, shifted by its own actual ground energy; free factors retain their Casimirs. Round19 A1/A2 supply this identification and the unique reference vacuum and gap. For fixed k, therefore, K_k=D_k+Q_k, where D_k is the sum of the finitely many link Casimirs and Q_k is bounded self-adjoint, including the finite scalar ground-energy subtraction.

Peter–Weyl gives D_k eigenvalues sum_e j_e(j_e+1), j_e in {0,1/2,...}, with multiplicities product_e(2j_e+1)^2. There are finitely many vectors below each finite energy: each spin is bounded by that energy and there are finitely many links. Consequently (D_k-i)^-1 is compact, D_k is self-adjoint on its spectral weighted-square-sum domain, and its finite Peter–Weyl sums are a core. Bounded perturbation preserves this operator domain and the form domain. The resolvent identity makes (K_k-i)^-1 compact as a product of the compact D_k resolvent with a bounded factor. Thus K_k has pure point spectrum of finite multiplicity, tending to infinity; its zero eigenspace is the reference vacuum Omega_k alone. Its ground gap is at least 1/8.

Every link Haar gauge action preserves the Casimir domain. Each Wilson multiplier is gauge invariant, so K_k, A_(q,k), A_k and all K_k spectral projections commute with the actual endpoint gauge actions. Their invariant sector reduces them, retains the vacuum and has compact resolvent as a restriction. This argument does not factor the physical Hilbert space into independent physical factors or remove boundary gauge conditions.

Write P_(k,lambda) for the **entire** eigenprojection at lambda and set

    Abar_k = strong sum_lambda P_(k,lambda) A_k P_(k,lambda).

This bounded self-adjoint direct sum has norm at most M_k=N_k/24: for every vector, square norms sum over orthogonal output sectors and each compression is bounded by M_k. It commutes with the spectral measure and preserves D(K_k), since the same estimate holds with each summand weighted by lambda^2. It is gauge invariant. The reference mean of each omitted face vanishes through its free Haar witness, so Abar_k Omega_k=0. No eigenvectorwise diagonalization that discards off-diagonal entries inside a degenerate eigenvalue is permitted.

## Weak-coupling averaging, including topology and a useful vector bound

Here is the operator argument used, proved for general self-adjoint pure-point K and bounded self-adjoint A of norm at most M. Put Abar=sum_lambda P_lambda A P_lambda. Write ell>0 for the small coupling, distinct from the energy label lambda. At slow time s define

    Z_ell(s)=exp(i s K/ell) exp(-i s(K/ell+A)),
    A_ell(s)=exp(i s K/ell) A exp(-i s K/ell).

The common domain D(K) and bounded perturbation identity first give the relative evolution; extension by density yields Z_ell'=-i A_ell Z_ell strongly on every vector. A_ell is strongly continuous, bounded by M, and self-adjoint. All following integrals are vectorwise strong integrals; norm estimates on them do not assert operator-norm Bochner continuity. The strong bounded-generator framework is also covered by Nachtergaele–Sims, arXiv:1410.8174v1, Section 2, Proposition 2.1 and its proof, inspected in this loop. The averaging argument itself is provided here.

Define the primitive R_ell(s)=integral_0^s(A_ell(r)-Abar)dr. On an energy-lambda vector u, its nonresonant components are

    P_mu R_ell(s)u
      = ell [exp(i s(mu-lambda)/ell)-1]
          /[i(mu-lambda)] P_mu A u,   mu!=lambda,
    P_lambda R_ell(s)u=0.                            (Y2.3)

At each fixed S, these tend to zero uniformly for |s|<=S: first restrict the orthogonal sum to finitely many mu, then bound its remaining norm by 2S times the tail norm of Au. Finite spectral sums are dense and ||R_ell(s)||<=2SM, so uniform strong convergence holds for every fixed vector, and uniformly on each compact set of vectors.

Let Zbar(s)=exp(-is Abar) and Z_ell(s,r) be the exact interaction propagator. Duhamel expresses Z_ell(s)-Zbar(s) as -i integral_0^s Z_ell(s,r) R_ell'(r) Zbar(r)dr. Integration by parts, valid with bounded strong derivatives, bounds its action on u by

    ||R_ell(s)Zbar(s)u||
      + M integral_0^s ||R_ell(r)Zbar(r)u||dr
      + integral_0^s ||R_ell(r)Abar Zbar(r)u||dr.     (Y2.4)

The two vector orbits are compact, proving Z_ell(s)->Zbar(s) strongly and uniformly on compact slow-time intervals. The same argument applies at negative times. Adjoints converge strongly uniformly as well: apply the strong difference to the compact orbit Zbar(s)*u in the identity

    ||(Z_ell(s)*-Zbar(s)*)u||
      =||(Zbar(s)-Z_ell(s))Zbar(s)*u||.

No moving unit vector is substituted into this conclusion.

For the actual compact-resolvent K_k, an isolated energy lambda has distance Delta_(k,lambda)>0 from every other energy. Equation (Y2.3), orthogonality and ||A||<=M give the additional bound

    sup_(|s|<=S) ||R_ell(s)P_lambda|| <= 2ell M/Delta_lambda.

Both orbits in (Y2.4) remain in the **whole** lambda eigenspace. For any unit u in that eigenspace,

    sup_(|s|<=S)||(Z_ell(s)-Zbar(s))u||
       <= r_lambda(ell,S)
       :=(2ell M/Delta_lambda)(1+2SM).              (Y2.5)

This is a vector/one-sector bound, not a bound on all excited energies simultaneously. Delta_(k,9/2) exists but is not evaluated here. At lambda=0 we may use Delta_(k,0)>=1/8. No uniform lower bound in k or across all excited Bohr frequencies is claimed.

The q dependence in (Y2.2) is retained. At fixed k, with R_k=sum_(f in O_k)r_f,

    delta_k(q):=||A_(q,k)-A_k||
      <= (1/24)sum_f(1-q^r_f) <=(1-q)R_k/24.       (Y2.6)

Unitary Duhamel bounds the two corresponding Z propagators by |s|delta_k(q) in operator norm. This coefficient replacement is uniform only for the fixed finite sum; it is never applied to the nonsummable global q=1 series.

## U scalar, order, sign, states and original clock

Let psi_k be U1's normalized symmetric pair of six-link characters tensored with the reference vacuum of F_k\F_0. The exact identities are K_k psi_k=(9/2)psi_k, W Omega_k=psi_k, W psi_k=Omega_k, and <Omega_k,W Omega_k>=0. W is still the original rank-two operator on eight free links extended by identity, not a rank-two truncation of K_k or Abar_k.

Put epsilon=1-q, ell=tau_q and

    s_q=alpha tau_q T_q/hbar=C tau_q/epsilon^3,
    rho=8z/7.

The actual rational profile gives tau_q/epsilon^3=3eta(1+q)^2(1+q^2)/P(q), tending to 8eta/7 and bounded by 3eta/2. Hence s_q->rho and s_q<=3z/2. The slow variable is a proof coordinate evaluated at the original diverging T_q; it is not a replacement physical clock.

The reference-state demodulated matrix element is exactly

    exp(i E t/hbar)<Omega_k,W beta_(q,k)^t(W)Omega_k>
      =<psi_k,Z_(q,k)(s) W Z_(q,k)(s)* Omega_k>.    (Y2.7)

Indeed U_q(t)=U_0(t)Z(s), Omega_k has reference energy zero, and the left psi_k energy supplies exp(-iEt/hbar). This establishes the adjoint order and the positive demodulation sign before taking any limit. Since Abar_k Omega_k=0, strong convergence of both Z and Z* reduces the limit of (Y2.7) to

    f_k(z)=<psi_k, exp(-i rho B_k)psi_k>,
    B_k=P_(k,9/2) A_k P_(k,9/2)
         acting on Ran P_(k,9/2).                 (Y2.8)

B_k is a genuine finite-dimensional Hermitian matrix **defined by all exact energy-9/2 states**. It includes possible strip excitations and all other equal-energy channels. Its dimension and entries beyond the known U expectation are not computed here. By U1's full parity/selection-rule proof, <psi_k,B_k psi_k>=-1/96 for every k containing the resonant face. Thus the first scalar term has sign +i rho/96=+iz/84.

Let C_(q,k) use the regional Hamiltonian's own unique invariant ground and both connected means, exactly as Y1. Its projector distance d_(q,k) from the reference vacuum tends to zero and is bounded by tau_q N_k/[3(1-eta)]. Changing the state in the Heisenberg raw term costs 2d_(q,k); changing its squared mean costs at most 4d_(q,k). Therefore the limit of exp(iET_q/hbar)C_(q,k)(T_q) is f_k(z) as well.

For completeness, a finite-q error budget following (Y2.5) is

    |exp(iET_q/hbar)C_(q,k)(T_q)-f_k(z)|
      <=6d_(q,k)+r_(9/2)(tau_q,S)+r_0(tau_q,S)
        +2S delta_k(q)+M_k|s_q-rho|,  S=3z/2.     (Y2.9)

For the adjoint vacuum error use ||Z*Omega_k-Omega_k||=||Z Omega_k-Omega_k||. The q replacement costs one |s|delta term for each of Z and Z*. The final slow-time change costs M_k|s_q-rho|. Every term vanishes at fixed k; the unevaluated actual Delta_(k,9/2) prevents treating (Y2.9) as a numerical finite-q tolerance certificate.

No interacting ground phase has been silently dropped. Each stationary centered propagator equals its own Heisenberg correlation, where scalar shifts cancel. The reference-state replacement in that bounded expression is uniform in t. Alternatively the fixed-region ground shift is O(alpha tau_q^2), so its phase at T_q is O(tau_q); the corresponding full-system ground-energy bound is only O(alpha epsilon^3) and cannot justify dropping its phase at this clock.

## Uniform spatial transfer to the actual full scalar

Y1 forward proves, with p=8/3 and 0<=x<1,

    D_k(x)=[(p)_(k+1)/(k+1)!] x^(k+1)/(1-x)^(k+4),
    |F_q(z)-exp(iET_q/hbar)C_(q,k)(T_q)|
       <=D_k(15z)+12 dhat_q,  dhat_q=sigma_q/gbar->0. (Y2.10)

Demodulation has modulus one and changes none of these errors. For x<=15*10^-6, the successive D ratio is

    D_(k+1)(x)/D_k(x)
       =x/(1-x) * (k+11/3)/(k+2) <1,

uniformly bounded away from one; therefore D_k(x)->0. Taking q->1 in the triangle comparison through F_q shows

    |f_k(z)-f_l(z)|<=D_k(15z)+D_l(15z).

This makes the scalars f_k Cauchy. Define L(z)=lim_k f_k(z). Then

    |L(z)-f_k(z)|<=D_k(15z),                       (Y2.11)

and (Y2.9)–(Y2.11), choosing k first and then q near one, prove (Y2.1). This is the uniform-tail transfer of finite-region scalar limits; no simultaneous k(q) rate, global unitary or global averaged Hamiltonian is required. In particular |L(z)|<=1, and the original correlation difference has an actual magnitude limit |C_q(T_q)-C_0(T_q)|->|L(z)-1|. U2's positive lower bound therefore applies to that limit. The full q=1 coefficient series is never formed.

## Certified characterization and discriminating controls

Spectral calculus for the actual self-adjoint B_k gives

    |f_k(z)-1-i z/84| <=rho^2 M_k^2/2.

This is a complete Taylor integral remainder for a real spectral measure; no unbounded K expansion is used. Combining with depth two of (Y2.11), the exact arithmetic checker certifies

    |L(z)-1-i z/84|
       <= D_2(15z)+(1/2)(8z/7)^2(129/24)^2.       (Y2.12)

At z=10^-6 this radius is below 1.89*10^-11, while the imaginary center is 1/84,000,000. Thus (Y2.12) is a useful disk for the **actual** limiting scalar; it is not evaluation of B_2 or its trajectory. The same symbolic inequality is valid throughout the admitted interval.

The checker independently enumerates the complete-factor geometry by expanding physical links and testing finite face candidates; it obtains N_1=20, N_2=129 and their anchor sums for (Y2.6). Exact quaternion Haar moments also check the actual resonant multiplication: ||x_f0 psi+||^2=1/4, whereas its projection on span{phi_X,phi_Y} has squared norm 1/16. The missing norm squared is 3/16. This is an actual unaveraged single-face leakage control, not proof that the full averaged B_k leaks from that plane. The latter question is deliberately left to the whole energy block.

An exact four-state fixture has a three-dimensional degenerate energy block, a within-block edge of strength 1/4, another edge of strength 1/5 to a third state, and an off-energy vacuum edge of strength 1/3. Block averaging retains the first two edges and removes the third. Eigenvectorwise diagonal averaging loses real within-block transitions. A two-state compression loses the additional second-moment contribution 1/25 even after averaging. This fixture refutes an unjustified closure inference; it is not substituted for the actual strip spectrum. Correct U sign, an explicitly wrong demodulation phase, the original tau/epsilon^3 clock, and finite-q coefficient differences are also checked.

For false operator-norm averaging, take the compact-resolvent direct sum K_n=diag(n,n+1/n), n>=2, and A_n=Pauli X on each pair. Every within-pair energy difference is nonzero, so Abar=0. Choose ell_n=1/n and the moving vector in pair n. The relative propagator at slow s=1/4 is then the same nontrivial two-state matrix for all n. Its off-diagonal entry has magnitude at least

    s-s^3/6-s^2/[2(1-s/3)] >1/5.

The first term bounds the real part of the first Dyson integral using cos r>=1-r^2/2; the geometric expression bounds the entire remaining exponential tail. Thus the operator norm cannot tend to zero, despite compact resolvent and the strong theorem. This demonstrates failure of a **general implication**; it does not decide operator-norm averaging for the actual K_k.

Finally the full infinite reference does not inherit finite-region compact resolvent: disjoint free-link yz plaquette characters at anchors (3,1,4n) are orthonormal invariant eigenvectors with the same energy 3alpha, for every n>=0. The checker verifies their disjoint support and energy formula on a prefix; translation and the unused Haar factors prove the infinite statement. This and the divergent number of uniform face coefficients distinguish finite-region operators from an assumed global q=1 Hamiltonian.

All acceptance conditions in check.py use explicit exceptions that remain active under Python -O. The two deterministic outputs contain genuine Boolean controls and exact rational certificates. Replaying normal and optimized modes is validation of this loop, not a new experiment.

## Reading and remaining scope

The contract's M1/M2/U1/U2, both inherited Y1 reports, Y1 review/decision and mandatory method snapshots were read for their named premises. Round19 forward A1/A2 were additionally read for the actual electric-plus-bounded-potential reference construction. Historical Newton/Tesla research snapshots were read as method context, not checked anew as historical primary texts. Relevant live method-reference bytes were preserved under inputs/ before freeze so future skill edits cannot change this evidence. reading.json records source depth and copied-source provenance.

The external primary source inspected here is [Nachtergaele–Sims, arXiv:1410.8174v1](https://arxiv.org/pdf/1410.8174), Section 2 through Proposition 2.1 and its proof, especially vectorwise integration, strong derivatives and Dyson existence. It supports the bounded strong-evolution framework and does not state this canonical scalar limit. The pure-point primitive proof, same-clock state reduction and transfer (Y2.3)–(Y2.12) are the derivation in this report. No scientific-priority claim follows from that attribution; comparison with the full averaging literature is incomplete.

Open obligations include actual block spectra and matrix entries, certified numerical exponentiation beyond the disk, a usable joint spatial/q resource rate, coherent realization of W and long-time laboratory control. There is no homogeneous stability, change of mobility or action, continuum reconstruction, global q=1 generator, or claim that the U two-state plane is invariant. No additional physics loop is executed.

    python3 -B research/round24/forward/y2/check.py --output /absolute/fresh/output
