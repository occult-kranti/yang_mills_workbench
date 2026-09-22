# AG1 reverse: the complete one-step selected-source update

Independent derivation from the frozen AG1 contract, before reading current forward AG1. All bound sources and instruction snapshots were frozen in `inputs/` before production. This report studies the actual S1 selected cubic mixing family in G+A. It does not identify G+A with the complete transformed homogeneous Yang–Mills Hamiltonian. The narrower-coupling refinement below was predeclared within this same loop.

## 1. Actual source and the denominator used

On each complete four-factor star Z_b use S1's source

    A_b=|w_b><Omega_b|+|Omega_b><w_b|,
    w_b=-<u_b,v_b>u_b-(||u_b||^2/3)v_b,
    v_b=phi_b Omega_b, u_b=(H0,Z_b|Q_b)^(-1)v_b.

S1 establishes r_b=||A_b||=||w_b||>0 for tau nonzero and r_b<= (4/3)(7/12)^(3/2)|tau|^3. All retained stars use the same homogeneous complete-block source, related by translation/relabeling of identical factors. This unitary equivalence proves r_b=r for every retained anchor, not equality of r to its upper bound. It is unaffected by deleting other stars at a finite boundary: the selected A_b is defined from H0,Z_b, not from that volume's G.

For any finite cuboid with at least one retained star let c_Lambda=max_x #{b:x in Z_b}; 1<=c_Lambda<=4. In the declared indexed support decomposition,

    ||A_Lambda||_2=16 c_Lambda r.                       (R1)

This is an exact interaction-norm formula although r itself is not numerically evaluated. It is the denominator below. The infinite translated family has c=4. A one-star cuboid has c=1; the checker covers both cases. An empty family or tau=0 is identically zero, and ratios by r are then omitted. Define only for upper budgeting

    r_up(M)=(1337/2250)(M/7)^3, M=7|tau|,

using sqrt(7/12)<191/250. No measured or fitted source coefficient is introduced. Both signs are covered without claiming equal spectra of G(tau) and G(-tau).

## 2. Full translated-source filter and auxiliary weight

Keep G=H0+sum_b D_b, D_b=Q_b phi_b Q_b, ||D_b||<=M, on D(H0) in each finite cuboid. T=3 and

    p_T(t)=(1-|t|/T)_+/T,
    h_T(t)=sign(t)(1-|t|/T)_+^2/2,
    R_b=integral p_T(t) alpha_t^G(A_b)dt,
    S_b=-i integral h_T(t) alpha_t^G(A_b)dt.

The strong integrals have ||p_T||_1=1, ||h_T||_1=T/3=1 and h_T'=delta_0-p_T. The complete star difference set contains thirteen anchors. An interior source has twelve crossing stars, each on a seven-factor union; the positive-octant origin has three. The inherited local inverse identity retains F_b=sum_crossing[K_b,D_c], with ||F_b||<=24Mr/(1-M), and gives the actual per-source bound

    ||R_b||/r <=min(1,(24M+2/T)/(1-M))<=2072/2997<0.7

on M<=1/1000. All D_c keep both Q factors and every original face. This per-source statement alone is not a weighted-family contraction.

For arbitrary rho>=2 define ||Phi||_rho=sup_x sum_(X contains x) rho^|X| ||Phi_X||, retaining indexed connected supports. In the bounded D interaction picture around unbounded onsite H0, each order-n word starts with one source star, has at most 13^n n! ordered relative choices, and union size at most 4+3n. Repetitions and attachments to previously added stars remain. At most 4+3n translations of a relative word contain a fixed root. Together with commutator factor (2M)^n and the time simplex, this gives

    orbital order-n norm <=rho^4 r(4+3n)(26M rho^3 |t|)^n. (R2)

Finite boundaries only delete possible anchors. At rho=9/4 put zeta=26M rho^3 T and F(x)=(4-x)/(1-x)^2. Integration yields uniformly

    a=||A||_rho<=4rho^4 r,
    s=||S||_rho<=rho^4 r F(zeta),
    b=||R||_rho<=rho^4 r F(zeta).                      (R3)

For M<=1/1000, zeta<=28431/32000<1. Each omitted positive tail after n=N is bounded explicitly by

    F_>N(x)=x^(N+1)[(3N+7)-(3N+4)x]/(1-x)^2.           (R4)

Thus all orders converge uniformly throughout the interval; this is not a finite-word extrapolation. Strong local integrals retain their complete factor supports. Family bounds are interaction norms; infinite extensive S is not claimed bounded on a Hilbert space.

## 3. Unbounded domain and the exact nonlinear identity

In a finite cuboid S=sum_b S_b is a bounded skew-adjoint operator. Pairing the filter with domain vectors and integrating by parts gives [S,G]=-A+R weakly. Self-adjointness of G turns this into S D(G) subset D(G) and the bounded commutator identity there. Since ||G S psi||<=||S||||G psi||+||A-R||||psi||, S is bounded on the G graph space; exp(plus/minus S) preserve that domain by their graph-norm series.

Differentiate e^{sS}G e^{-sS} on that domain only after replacing its first commutator by bounded -A+R. Conjugate bounded A separately. The result is

    e^S(G+A)e^-S=G+R+N,
    N=integral_0^1 e^{s ad_S}{s[S,A]+(1-s)[S,R]} ds
      =sum_(n>=1) ad_S^n(nA+R)/(n+1)!.                (R5)

In particular N starts with [S,A+R]/2. The G-only coefficient [S,-A+R]/2 checks the wrong Hamiltonian. No operator-norm BCH series of unbounded G is used; all infinite series in (R5) act on bounded commutators or bounded interactions. The next section supplies the full volume-independent interaction convergence.

## 4. Cardinality loss at every commutator

Set rho=e^kappa and output weight w=e^kappa'>=2. For intersecting supports X,Y, w^|X union Y|<=w^-1 w^|X|w^|Y|. Root the commutator first in X and then in Y; each overlap is assigned to one site of the rooted support. With d=kappa-kappa'>0 and sup_(m>=1) m e^-dm<=1/(ed),

    ||[Phi,Psi]||_w <=[4/(w e d)]||Phi||_rho||Psi||_rho
                       <=[2/(e d)]||Phi||_rho||Psi||_rho. (R6)

This pays both incoming-root cases. For n commutators distribute Delta=log(rho/2)=log(9/8) over n equal losses. Using n!>=(n/e)^n proves

    ||ad_S^n X||_2/n! <=[2||S||_rho/Delta]^n ||X||_rho.

Since Delta>=1/9, a rational sufficient ratio is theta=18||S||_rho. Use its upper bound theta_up=18 B r_up, B=rho^4 F(zeta). If theta_up<1 then every term of (R5), including generated supports, is controlled:

    ||N||_2 <=theta_up/(1-theta_up) (a+b/2)
             <=n_coef r,
    n_coef=theta_up/(1-theta_up)(4rho^4+B/2).            (R7)

The bound uses n/(n+1)<=1 for A and 1/(n+1)<=1/2 for R; it does not retain only the first commutator. At M=1/1000, B<6411, theta_up<2.000*10^-7 and n_coef<0.000662. These rational endpoint bounds cover the whole continuous interval: F'(x)=(7-x)/(1-x)^3>0, r_up increases with M, and each subsequent positive expression increases before its pole.

There is a concrete reason to spend this weight. As an abstract finite-spin diagnostic let Phi=2^-n product_i X_i on n sites, and Psi=sum_i Z_i/2. Each has weight-2 norm one in the declared decomposition, while the commutator has norm n at weight 2. This follows from its squared matrix and the extreme eigenvalue of sum Z_i; the checker verifies n=1 through 5 exactly. It rules out a size-independent same-weight algebra bound for arbitrary interactions. It is not a physical SU(2) simulation or a counterexample to the restricted source theorem.

On the main M<=1/1000 interval, the basic residual budget is ||R||_2<=16r F(624M)<=382.074r, versus actual input 16c_Lambda r. The positive bound supplies no weighted contraction there; this does not prove expansion of the true residual. The one-step full nonlinear estimate is nevertheless uniform and finite.

## 5. Predeclared narrower interval: actual selected-family contraction

For 0<M<=1/10000 split the filtered source into its exact zero-D term and all words containing at least one D. This changes no generator or Hamiltonian. Under free onsite evolution,

    R_b^(0)=|f_T(H0,Z_b)w_b><Omega_b|+adjoint,
    f_T(E)=sinc^2(TE/2).

The actual source lies in Q_b and H0,Z_b|Q_b>=1. Thus ||R_b^(0)||<=4r/T^2=4r/9 by scalar spectral calculus on the rank source. This use of a source-specific vacuum gap does not claim a multiplier norm bound on arbitrary source Bohr frequencies. Its declared support remains Z_b, so its exact-family budget is at most (4/9)||A||_2.

All other words are already included in (R2). At original weight 2 let x=208MT=624M. Integrating the positive tail with ||p_T||_1=1 gives

    ||R-R^(0)||_2 <=16r [F(x)-4].

Combining this with (R1) and (R7), with c_Lambda>=1, gives the actual chosen-decomposition bound

    ||R+N||_2/||A||_2
       <=4/9+[F(x)-4]/c_Lambda+n_coef/(16c_Lambda)
       <=gamma(M):=4/9+F(x)-4+n_coef/16.              (R8)

At M=1/10000, x=39/625, B<120.741, theta_up<3.766*10^-12, n_coef<6.133*10^-10, and

    gamma(M)<=0.923602617555<0.93.                    (R9)

The displayed decimal upper bound is backed by the exact rational value in the output. Positive-coefficient monotonicity proves the inequality continuously down to M=0; at zero both sides are zero before division. For both signs of nonzero tau, r is positive by S1 and cancels legitimately. Crucially, (R8) divides by 16c_Lambda r, not by 64r_up. The unevaluated source upper bound is used only to bound the extra factor of r in the nonlinear correction.

This is contraction of the one actual selected family in this constructed original-weight decomposition. It is not a numerical contraction theorem for an unspecified full original remainder. Uniformity includes one-star and boundary-deleted cuboids; larger c_Lambda only improves the certificate.

## 6. Scalar, source and reference-diagonal bookkeeping

Keep every generated connected support X and a self-adjoint representative K_X of R+N. Filter/BCH terms can be symmetrized on the same support without increasing their norm. Define the local reference projector P_X=|Omega_X><Omega_X|, Q_X=I_X-P_X, and

    c_X=<Omega_X,K_X Omega_X>,
    A'_X=P_X K_X Q_X+Q_X K_X P_X,
    D'_X=Q_X(K_X-c_X I_X)Q_X,
    K_X=c_X I_X+A'_X+D'_X.                           (R10)

The complete indexed support X remains assigned even to c_X I_X. The three separate norm costs are at most ||K_X||, ||K_X|| and 2||K_X||; their summed bookkeeping costs at most 4||K_X||. D'_X is diagonal only relative to the reference vacuum/complement split, not every excited spectral block of G. In particular the new mixing family obeys ||A'||_2<=||R+N||_2 and inherits (R8). The scalar is a reference expectation, not an exact interacting ground energy. Its finite-volume sum may be extensive.

Updating the reference diagonal by D' changes the next inverse, domains and source hypotheses. Higher supports and the consumed rho-to-2 weight budget cannot be silently reset for the next iteration. Therefore this one-step contraction does not close changed-diagonal induction.

## 7. Additional actual remainder E and validation

If the original transformed Hamiltonian is G+A+E, the exact equation is

    e^S(G+A+E)e^-S=G+R+N+e^S E e^-S.

Given a complete bound e_star=||E||_rho as an additional premise, the same all-order loss proof gives

    ||e^S E e^-S||_2<=e_star/(1-theta_up).             (R11)

The source extraction in (R10) costs no more than this, but no e_star is invented or fitted. For example contraction of the full new mixing source would additionally require gamma||A||_2+e_star/(1-theta_up)<||A||_2. No such inventory or inequality is established for the complete original E here.

The exact checker binds all snapshots, enumerates star crossings and incoming/repeated words, verifies positive tails and filter moments, and tests both signs, tau=0 and the actual finite-volume denominator multiplicities. An independent rational two-level algebra fixture verifies every full G+A coefficient through degree nine, exposes omitted residual and G-only errors, and reconstructs scalar/mixing/diagonal pieces at each order. It separately retains nonzero E transport coefficients. These finite matrices diagnose algebra; the complete-block domain and all-order support proofs above establish the physical scoped result.

Run `python3 -B research/round27/reverse/ag1/check.py --output /absolute/fresh/directory`; optimized Python must reproduce the same deterministic result. Source bounds, report, checker and frozen instruction inventory are hashed. This is the third and final authorized physics loop. No AG2 or AI3 is executed. The remaining full-Hamiltonian remainder, all-stage induction, homogeneous numerical gap, physical matching and four-dimensional continuum construction remain open. Scientific priority is unverified.

All displayed operators and filter times use the inherited dimensionless G units. Physical energies multiply by delta=alpha/8, with fixed positive lattice spacing, E_star, alpha/E_star and hbar. T=3 is a proof-filter duration, not either canonical observation time or an experimentally measured frequency.
