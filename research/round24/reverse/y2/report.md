# Y2 reverse — reconstructing the actual demodulated endpoint limit

Independent reverse derivation under the frozen Y2 contract, before reading current forward Y2. The conclusion is an **actual scalar limit**, characterized by full regional reference-energy blocks. The blocks have not been assembled numerically. Newton's backward analysis separates sufficient premises; Tesla's phase and loading audit retains all equal-energy channels and the original clock. Historical analogies add no mathematical premises. Independent model-agent review is not outside peer review; scientific novelty remains unverified.

## Target and sufficient premises

Use exactly canonical M/N/U, its fixed complete-strip reference, and U1's bounded invariant rank observable W, extended by identity outside its eight free factors. Put epsilon=1-q,

    T_q=C(hbar/alpha)epsilon^-3, z=C eta in (0,10^-6],
    E=9alpha/2, D_q(z)=exp(i E T_q/hbar) C_q(T_q).

Here C_q is the actual stationary connected autocorrelation, with beta_q^t(W)=exp(-itH_q/hbar) W exp(itH_q/hbar). Fix a,E_star,alpha/E_star,hbar>0 and eta in (0,1). No time generator from another model is imported. The reference phase is a scalar display operation at the same T_q.

To force a limit of D_q, it suffices to establish: (i) fixed finite collars with self-adjoint compact-resolvent reference operators; (ii) bounded q-coefficients converging in norm on each collar; (iii) strong, compact-rescaled-time averaging retaining whole degenerate energy spaces; (iv) the actual W/state/phase identity; and (v) a spatial error tending to zero uniformly in q. Items (i)–(iv) are proved below and item (v) is the accepted Y1 theorem. A global q=1 Hamiltonian, norm averaging, or a closed two-state plane is unnecessary.

Use the **reverse Y1 convention**: F_0 is the eight U1 free factors, J_d is the set of omitted faces incident to complete factors in F_(d-1), and F_d adds every complete owner of those faces. At depths 1,2,3 this gives respectively (factors,links,retained faces)=(35,98,19),(135,297,125),(308,623,327). Forward Y1's internally supported face convention gives different regional operators and is not substituted here.

## Actual finite-factor spectral and gauge premises

The regional Hilbert space is the full L2(SU(2)^(ell_d),Haar), before the reducing gauge restriction. With energies divided by alpha, its reference is

    G_d = sum_(links e) C_e
          - sum_(selected strip faces f) (lambda_f/alpha) x_f
          - sum_(complete strips C) E_C/alpha.

This is precisely the finite sum of the inherited shifted complete-strip operators and free Casimirs. The selected coefficients and strip ground energies remain fixed. Their values need not be diagonalized here. Round19 A1/A2 are consulted for this definition, not for a new dyadic coupling or transferred gap constant.

For completeness, compact resolvent follows directly in the actual untruncated space. Peter–Weyl gives the orthonormal product basis with spins j_e in {0,1/2,1,...}, electric eigenvalues sum_e j_e(j_e+1), and multiplicity product_e(2j_e+1)^2. At a finite electric energy cutoff, each j_e is bounded and there are finitely many labels and matrix indices. Finite-energy spectral projections therefore approximate (1+sum C_e)^-1 in norm. Define its self-adjoint domain by square-summability of electric eigenvalue times the coefficients. The selected finite Wilson potential and scalar subtraction are bounded self-adjoint. Bounded perturbation preserves that operator domain and its closed form domain; the resolvent identity makes the perturbed resolvent compact. Thus G_d has a complete pure-point spectral resolution, finite-dimensional eigenspaces, no finite spectral accumulation, and is nonnegative. This argument neither cuts off spins nor asserts compact resolvent of the infinite tensor sum.

Write P_(d,r) for the **entire** eigenspace at dimensionless reference energy r. The unique vacuum has r=0; U1's vector psi_d=W Omega_d is normalized and has r=e=9/2. It is the two-character superposition on the eight original free links, tensored with the reference grounds of all other factors. All other vectors at r=e are retained in P_(d,e). In particular, knowing two eigenvectors at e does not identify the rank of P_(d,e).

The vertex Haar pullbacks act by left/right translations on link factors. They preserve the electric domain and commute with its spectral measure; every selected and omitted closed-loop multiplier is invariant. Therefore G_d and its bounded perturbations commute with each finite endpoint gauge group and their spectral projections reduce the invariant sector. Complete-factor closure preserves this statement at the collar boundary. The inherited unique strip ground transforms under a continuous one-dimensional character of a product of SU(2), necessarily trivial; the free constant is invariant. Hence Omega_d and psi_d are invariant. Nothing identifies the physical invariant space with a tensor product of independent physical strip spaces.

Define the bounded dimensionless perturbations

    A_(q,d)=-(1/24) sum_(f in J_d) q^m_f x_f,
    A_d=-(1/24) sum_(f in J_d) x_f, m_f=|anchor(f)|_1,
    M_d=N_d/24, K_d=(1/24) sum_(f in J_d) m_f, N_d=|J_d|.

Then ||A_(q,d)||,||A_d||<=M_d, and

    ||A_(q,d)-A_d|| <= K_d(1-q),                       (R1)

because 1-q^m <= m(1-q) for integers m>=0. A_d is only a finite-collar coefficient limit. Its introduction never sums all q=1 faces globally.

The pinched operator

    Abar_d = strong-sum_r P_(d,r) A_d P_(d,r)           (R2)

is bounded self-adjoint, with norm at most M_d. Indeed the squared norm of its action is the sum over mutually orthogonal output blocks, bounded by M_d^2 times the squared input norm. Its finite partial sums converge strongly. It commutes with all G_d spectral projections, preserves D(G_d), and also respects gauge invariance. Each omitted face has an unused Haar link, so <Omega_d,A_d Omega_d>=0. The vacuum is simple, hence Abar_d Omega_d=0. The excitation block A_(d,e)=P_(d,e) A_d P_(d,e), acting on the full finite-dimensional space P_(d,e)H_d, is a well-defined actual operator, not a fitted matrix.

## Strong averaging with an unbounded reference

Here is the needed theorem and proof. Let G be self-adjoint with compact resolvent, and A bounded self-adjoint, ||A||<=M. Let Abar=sum_r P_r A P_r. For lambda>0 and 0<=s<=S<infinity, set

    Z_lambda(s)=exp(i s G/lambda) exp(-i s(G/lambda+A)),
    A_lambda(s)=exp(i sG/lambda) A exp(-i sG/lambda).

Bounded perturbation on D(G), extended by density, gives the strong integral equation Z'=-i A_lambda Z. The generator is strongly continuous and bounded on all vectors. All subsequent products and integrals are vectorwise. No derivative of an arbitrary bounded observable through G is taken.

Let R_lambda(s)=integral_0^s(A_lambda(u)-Abar)du. On an eigenvector v in P_r H,

    R_lambda(s)v = sum_(t != r)
       lambda[exp(i(t-r)s/lambda)-1]/[i(t-r)] P_t A v. (R3)

This is a Hilbert norm sum over orthogonal output energies. The spectral separation Delta_r=dist(r,spec(G)\{r}) is positive for each fixed r. Consequently, uniformly in s,

    ||R_lambda(s)P_r|| <= 2lambda M/Delta_r.           (R4)

If the complement is empty the primitive is zero and this term is interpreted as zero. Also ||R_lambda(s)||<=2SM. Finite sums of eigenspaces are dense, so (R4), followed by the uniform bound, proves sup_(s<=S)||R_lambda(s)v||->0 for every fixed v. A finite epsilon-net extends this convergence to any compact set of input vectors. It does **not** take a supremum over all spectral energies.

To pass from a primitive to dynamics, use the two-parameter propagator Z_lambda(s,u) and Duhamel:

    Z_lambda(s)-exp(-is Abar)
     =-i integral_0^s Z_lambda(s,u) R_lambda'(u)
                         exp(-iu Abar)du.

Integrate by parts in the strong sense on each vector. The upper boundary is R_lambda(s)exp(-is Abar); the lower boundary vanishes. The differentiated left factor is i Z_lambda(s,u) A_lambda(u), and the differentiated right factor is -i Abar exp(-iu Abar). The resulting norms involve R_lambda(u) only on the two compact sets

    {exp(-iu Abar)v:0<=u<=S},
    {Abar exp(-iu Abar)v:0<=u<=S}.

They tend uniformly to zero by the preceding compact-set argument. This proves

    sup_(s<=S)||(Z_lambda(s)-exp(-is Abar))v|| -> 0.   (R5)

For a vector in one fixed energy block the same calculation is quantitative, since Abar and its exponential preserve that whole block:

    sup_(s<=S)||(Z_lambda(s)-exp(-is Abar))P_r||
       <= b_r(lambda,S):=(2lambda M/Delta_r)(1+2SM).   (R6)

Adjoints obey the same column estimate: use
(Z_lambda^*-exp(is Abar))v=Z_lambda^*(exp(-is Abar)-Z_lambda)exp(is Abar)v.
Thus strong convergence of both sides of a conjugation is justified. This is a column norm bound on a fixed complete energy space, not a global operator-norm theorem. The proof also supplies compact-time strong convergence of the adjoints for arbitrary fixed vectors.

For A_q with ||A_q-A||<=delta_q, bounded-generator Duhamel in the same interaction frame adds at most S delta_q to the propagator norm error. This norm estimate applies to a **bounded coefficient difference**, not to R_lambda on the full unit sphere.

## Original clock and actual scalar identity

The canonical profile is b(q)=P(q)/[24epsilon^3(1+q)^2(1+q^2)], P(q)=2+5q+5q^2+6q^3+3q^4, tau_q=eta/[8b(q)]. Put

    lambda=tau_q,
    s_q=alpha tau_q T_q/hbar=C tau_q/epsilon^3
       =3z(1+q)^2(1+q^2)/P(q) -> s_*=8z/7.

The admitted polynomial identity gives 0<s_q<=3z/2. Hence lambda->0 and s_q stays in the fixed interval [0,S], S=3z/2. This is a change of variables for a proof about **T_q itself**. Replacing the experiment by the fixed time C hbar/alpha would instead give s=C tau_q->0 and lose the signal.

Let Z_(q,d)=exp(iT_q H_(0,d)/hbar)exp(-iT_q H_(q,d)/hbar). It is exactly Z_lambda(s_q) with A_(q,d) in place of A. For the reference state, the bounded U1 identity is

    exp(iET_q/hbar)<Omega_d,W beta_(q,d)^(T_q)(W)Omega_d>
       =<psi_d,Z_(q,d) W Z_(q,d)^* Omega_d>.           (R7)

It follows by writing the negative-time Heisenberg conjugation as U_0 Z W Z^* U_0^* and using U_0^*Omega_d=Omega_d and <psi_d,U_0=e^(-iET_q/hbar)<psi_d|. This fixes the adjoint, order and sign. The reference mean of W is zero. Its two regional **stationary** connected means must still be retained when changing state.

Y1 proves a unique invariant regional ground with d_(q,d)=||P_(q,d)-P_0|| <= tau_q N_d/[3(1-eta)]. The raw expectation changes by at most 2d_(q,d) and the squared mean by at most 4d_(q,d). Thus the true regional stationary correlation differs from the reference-state expression in (R7) by at most 6d_(q,d), uniformly in time. Scalar ground-energy shifts cancel in Heisenberg conjugation. No uncanceled ground phase from a single propagator has been discarded.

Apply (R5) to (R7), including its adjoint. Since Abar_d Omega_d=0 and W Omega_d=psi_d, the result is

    exp(iET_q/hbar) C_(q,d)(T_q) -> f_d(z),
    f_d(z)=<psi_d,exp[-i(8z/7) A_(d,e)]psi_d>.        (R8)

This characterizes the actual finite-collar limit through the whole r=e block. Its small-z derivative is +i/84 because U1 gives <psi_d,A_d psi_d>=-1/96 for every d>=1. It does not give a sine law or a two-by-two evolution.

For clarity, an explicit sufficient regional scalar error is

    6d_(q,d)+b_e(tau_q,S)+b_0(tau_q,S)
      +2S K_d(1-q)+M_d|s_q-s_*|.                    (R9)

Here b_r is (R6), using actual G_d separations. Delta_0>=1/8 is inherited; Delta_e>0 follows from compact resolvent but has **not** been numerically computed. Therefore (R9) is a proved formula with an unevaluated spectral constant, not a furnished finite-q numerical rate. It still tends to zero at every fixed collar, which is all the limit transfer needs. The full finite-dimensional matrix A_(d,e), its multiplicity and any trajectory also remain unevaluated.

## Passing from finite collars to the full canonical scalar

Reverse Y1 gives, for all q in (0,1),

    |D_q(z)-exp(iET_q/hbar)C_(q,d)(T_q)|
      <= B_d(15z)+6(d_q+d_(q,d)),                    (R10)
    B_d(x)=sum_(n=d+1)^infinity (n+1)(n+2)x^n/2
      =x^(d+1)[(d+2)(d+3)-2(d+1)(d+3)x
                     +(d+1)(d+2)x^2]/[2(1-x)^3].

The full d_q=O(epsilon^(3/2)) and each fixed regional d_(q,d)=O(epsilon^3). For fixed d,k, take q->1 in the triangle inequality through the same D_q. Equation (R8) gives

    |f_d(z)-f_k(z)| <= B_d(15z)+B_k(15z).

Since 15z<1 and B_d(15z)->0, the regional scalars are Cauchy. Define f(z)=lim_d f_d(z). Then

    |f(z)-f_d(z)|<=B_d(15z),
    limsup_(q->1)|D_q(z)-f(z)|<=2B_d(15z).

Finally let d increase. This proves the requested actual full scalar limit

    lim_(q->1-) exp(iET_q/hbar) C_q(T_q)
      = f(z)=lim_(d->infinity)
          <psi_d,exp[-i(8z/7)P_(d,e)A_dP_(d,e)]psi_d>. (R11)

In the exponential the compressed matrix acts on P_(d,e)H_d. No convergence of these matrices on a global Hilbert space is asserted. The proof takes q->1 at fixed d, and only then d->infinity; the uniform spatial error authorizes this conclusion. Increasing d as a function of q in the uncomputed constants of (R9) is not justified.

## Certified characterization and discriminating controls

The actual limit is bounded in modulus by one, since every f_d is a unitary matrix element of a unit vector. Passing to the limit in U2's full connected remainder gives the independently certified disk

    |f(z)-1-i z/84| <= R(z),
    R(z)=(44/9)(80z/7)^2/(1-80z/7)^5.                (R12)

At z=10^-6, the center is 1+i/84000000 and R(z)<6.39*10^-10. The actual unknown complex f lies in this disk; this is an enclosure, not a plotted or computed trajectory. The error in using the exact but unevaluated depth-two f_2 is B_2(15z)<3.4*10^-14. As already certified in U2, |f(z)-1|>=z/84-R(z)>z/168 throughout the stated interval. Exact rational arithmetic checks the cap and the monotonic ratio arguments cover the interval.

The checker independently reconstructs the actual reverse collars and their coefficient budgets. It also computes exact or controlled **abstract** fixtures, which test proof obligations without replacing the lattice:

* On energies (0,1,1,1), a rational self-adjoint A couples the vacuum to the first excited vector and links all three excited vectors. Energy pinching removes the vacuum transition but keeps the entire three-state excited block. For v=(e_1+e_2)/sqrt(2), its mean is -1/4. Diagonal-only pinching falsely gives zero. Omitting the third excited channel lowers the second moment from 17/144 to 1/16, losing exactly 1/18. A rational Taylor enclosure at s=1/10 certifies the resulting scalar difference and the sign of its imaginary part. This is a fixture, not the U1 matrix.
* Compact resolvent alone does not give norm averaging. On direct sums of two-dimensional blocks take G_n=diag(n^2,n^2+1/n), and A_n the swap. Abar=0, ||A||=1. At lambda_n=1/n and s=1 the nth interaction-picture block has off-diagonal magnitude sin(sqrt(5)/2)/(sqrt(5)/2)>=19/24. Thus ||Z_(lambda_n)(1)-I||>=19/24 for all n although (R5) holds on each fixed vector. The bound uses sin x/x>=1-x^2/6 at x=sqrt(5)/2. Neither a global ground gap nor compact resolvent separates all excited Bohr frequencies uniformly.
* At a quarter reference period C_0=-i, correct phase removal gives 1 and the opposite sign gives -1. The fixture's negative coupling produces a positive imaginary first response; taking the adjoint reverses it. These controls check sign, phase and ordering.
* Pointwise spatial approximation alone cannot transfer limits: a_d(q)=q^d tends to zero as d->infinity at every fixed q<1, while its q->1 limit is one at every fixed d. Along q=1-d^-2, a_d(q)>=1-1/d. The actual B_d(15z) is uniform and excludes this failure mechanism.
* All finite link spaces remain infinite dimensional, since a single retained Haar link has arbitrarily large j with nonzero multiplicity. A finite number of factors or an isolated finite-rank energy block is not a finite-spin approximation of its full dynamics.

The executable rejects excluded parameter endpoints, booleans masquerading as rationals, a zero physical reference, missing or changed frozen inputs, symlink source paths, and non-fresh output directories with explicit exceptions. Checks remain active under Python -O. It imports no other research implementation and writes exactly results.json and controls.json to the specified new output directory.

## Provenance, scope and reproduction

All contract-declared dependencies and instruction snapshots were read and are hash-bound. The actual complete-strip definition was additionally inspected in Round19 forward A1/A2; Round17/18 A2 and the M1 contract were consulted as model-identification background, without transferring their coefficients. The Y1 reverse checker/submission were inspected only for output/packaging conventions. Supplemental live method guidance is captured in immutable local input snapshots; frozen contract methods govern this evidence. The reading record lists the exact sources and depth.

Primary technical reading: Nachtergaele–Sims, arXiv:1410.8174v1, Section 2, strong vector integrals and Proposition 2.1 including its Dyson proof, supports the bounded strongly continuous interaction-picture framework. Burgarth–Facchi–Gramegna–Yuasa, arXiv:2111.08961v2, Theorem 3's hypotheses and block formula and Remark 4 were inspected as related prior-method context. Their stated finite-spectral bounded-reference norm theorem is not imported as an infinite pure-point result. Equations (R3)–(R6) supply the necessary proof here. A preliminary Davies search was an unused lead; no open-system Markovian theorem is assumed. No exhaustive literature or priority review is claimed.

The established contribution is the stated strong averaging application and scalar spatial-limit construction for this canonical observable. Actual block diagonalization, useful computed excited-energy separations, a finite-q numerical averaging rate, a trajectory, laboratory implementation, full limiting dynamics, the nonzero homogeneous theory and continuum Yang–Mills remain outside the result.

    python3 -B research/round24/reverse/y2/check.py --output /absolute/new/y2-reverse
    python3 -B -O research/round24/reverse/y2/check.py --output /absolute/new/y2-reverse-optimized

The two executions must agree byte for byte. They validate this one Y2 loop and add no research loop.
