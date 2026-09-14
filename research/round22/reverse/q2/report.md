# Q2 reverse: exact projected memory with actual channel spectra

The actual magnetic projection has an exact Volterra equation and Schur resolvent, with complementary electric lower bound 3alpha. On the frozen channels f0=1 and f1=2x, the leading magnetic kernel has seven electric energies and a nonzero off-diagonal entry. Explicit full-selected-Hilbert operator errors are cubic in lambda and uniform in delay in absolute norm; the self-energy error stays bounded as z decreases to zero. No autonomous two-channel or three-chord closure follows.

All statements use the frozen Q2 graph, P2 J=J3, P=JJ*, Q=I-P and Q1 H_lambda=H_E+alpha lambda Vmag with all twenty faces. The tree, root, selected U28,V27,W24 and complete physical observable Jf1 remain fixed. a,E_star,alpha/E_star,hbar and graph volume are fixed positive scales. lambda is dimensionless, delay s is time, and z>0 is a resolvent energy. The bounds hold for all lambda>=0, in particular throughout the requested 0<=lambda<=1/100. f0 is the Haar electric reference, not the interacting ground. No scalar fit, current opposite-producer reading, R1 work, homogeneous or continuum transfer occurs.

## The actual complementary electric spectrum and domains

Use the full physical Peter-Weyl decomposition into edge spins j_e and vertex invariant tensors. Every nontrivial irrep has Casimir j_e(j_e+1)>=3/4. In an admissible nonconstant spin assignment, a vertex cannot have exactly one incident nontrivial irrep: its tensor product with the other trivial factors contains no invariant vector. Hence the subgraph of nontrivial edges has no degree-one vertex and contains a cycle. The actual graph is simple and bipartite, and has a four-edge face, so its girth is four. Therefore every nonconstant admissible spin assignment has energy at least 4(3/4)alpha=3alpha. The all-trivial block is the one-dimensional constant ground. Summing the exact representation blocks gives

    H_E >= 3alpha (I-|1><1|) on the physical form domain.             (1)

This proof uses all gauge constraints, no external representation's gap and no numerical spin cutoff. Since J1=1, ran(Q) is orthogonal to the constant. C0=H_E restricted to ran(Q) thus has lower bound 3alpha. It is sharp: the nonzero physical face W0 lies in ran(Q), by its zero selected conditional mean, and H_E W0=3alpha W0.

By P2/Q1, Q reduces H_E, Q preserves its H2 operator/H1 form domains, and 0<=Vmag<=40. Consequently

    C_lambda=C0+alpha lambda QVmagQ >= 3alpha,
    D(C_lambda)=QD(H_E),  D(q_C)=QD(H_E^(1/2)).                      (2)

The bounded perturbation preserves self-adjointness and the invariant polynomial core projected by Q. In particular

    ||exp(-s C_lambda/hbar)|| <= exp(-3alpha s/hbar),
    ||(C_lambda+z)^-1|| <= (3alpha+z)^-1.                           (3)

The full and selected blocks are H_lambda on the original physical H2 domain and A_lambda=H_eff+alpha lambda(20-tau) on selected H2, with H1 forms. Here tau=Tr(VW^-1)/2. Under the unitary splitting Hphys=JH3 direct-sum QHphys,

    H_lambda = [[A_lambda, B_lambda*],[B_lambda,C_lambda]],
    D(H_lambda)=D(A_lambda) direct-sum D(C_lambda),
    B_lambda=alpha lambda B1,   B1=QVmagJ.                           (4)

The admitted exact Q1 multiplier gives B1*B1=M_d, d=19/4+(r+x+z_W)/2, 4<=d<=25/4, so ||B1||=5/2. Here r=Tr(UW^-1)/2 and z_W=Tr W/2; z_W is distinguished from the resolvent energy z. Both off-diagonal blocks in (4) are bounded. No magnetic reducing-image assumption is made.

## Exact projected Volterra and Schur relations

For initial f in D(A_lambda), u(t)=T_lambda(t)f and v(t)=Qexp(-tH_lambda/hbar)Jf lie in their respective block domains, because the full semigroup preserves D(H_lambda). The block equations and v(0)=0 give the strong variation-of-constants identity

    v(t)=-hbar^-1 integral_0^t exp(-(t-r)C_lambda/hbar) B_lambda u(r) dr.

With K_lambda(s)=B_lambda*exp(-s C_lambda/hbar)B_lambda, substitution yields

    u'(t)=-A_lambda u(t)/hbar
          +hbar^-2 integral_0^t K_lambda(t-r)u(r) dr.                (5)

Its mild form, valid on every selected vector by density and bounded strong vector integration, is

    T_lambda(t)=exp(-t A_lambda/hbar)
       +hbar^-2 integral_0^t ds integral_0^s dr
          exp(-(t-s)A_lambda/hbar) K_lambda(s-r) T_lambda(r).         (6)

The rightmost factor is the full compressed T_lambda. It cannot be replaced by exp(-r A_lambda/hbar) in this exact equation. Formula (6) uses the complementary C semigroup inside K; this is a different ordering from Q1's symmetric double-Duhamel formula containing the middle full-H semigroup. Equations (3)-(4) make all finite-time integrals bounded strong vector integrals without assuming operator-norm continuity at zero.

For z>0 define the bounded positive self-energy

    Sigma_lambda(z)=B_lambda*(C_lambda+z)^-1B_lambda.

Eliminating the complementary component of (H_lambda+z)(Jf+q)=Jg gives q=-(C_lambda+z)^-1B_lambda f, and therefore

    J*(H_lambda+z)^-1J
       =[A_lambda+z-Sigma_lambda(z)]^-1.                            (7)

The sign is minus. The Schur operator is self-adjoint on D(A_lambda). Completing the block quadratic form, or minimizing it over q in the complementary form domain, shows it is at least zI. In detail the minimum of the form of H_lambda+z at fixed f equals the Schur form and is >=z||f||^2. The minimizing q above is in D(C_lambda), so the block elimination is domain-safe. Thus the inverse in (7) is bounded by 1/z. Also

    Sigma_lambda(z)=hbar^-1 integral_0^infinity
                          exp(-zs/hbar)K_lambda(s) ds,              (8)

where (3) ensures absolute norm integrability after vectorwise spectral integration. The zero-coupling kernel and self-energy are zero, recovering the full P2 electric identities.

## Actual finite spectral calculation for the two frozen channels

The channels are orthonormal: E[x]=0, E[x^2]=1/4. Set F=Jf1=Tr L28, the six-link loop with ordered word

    14-,2+,28+,3-,15+,26-.

For the nineteen faces other than 8, E[W_p|selected]=0, so

    B1 f0=-sum_(p!=8) W_p,    B1 f1=-sum_(p!=8) F W_p.               (9)

All W_p are exact eigenvectors at 3alpha. Distinct faces are orthogonal and remain so under H_E: flipping the center sign of one original link commutes with H_E and gauge invariance, and distinguishes their edge-parity patterns. The same argument distinguishes F W_p and F W_q for every p!=q, because the common F parity cancels in their comparison. This is stronger than asserting that their original Haar inner product happens to vanish.

The complete original-edge intersection of a face with the F loop is a single consecutive path of length m, or is empty. Independent signed graph reconstruction gives:

| Shared path length m | Face IDs, excluding 8 | Count |
|---|---|---|
| 0 | 4,5,6,7,11,13,14,18,19 | 9 |
| 1 | 0,1,10,12,16,17 | 6 |
| 2 | 2,3 | 2 |
| 3 | 9,15 | 2 |

When m=0, the edge supports are disjoint: F W_p is an eigenvector at (15/2)alpha with squared norm 1/4. When m>0, collapse the shared path to its Haar product p, the rest of the F loop to r, and the rest of the face to q. These products use disjoint original edge sets, so they are independent Haar. Reverse a full trace orientation where needed; trace reality makes the function

    g=F W_p=2(p dot r)(p dot q).

Its shared-path spin-zero and spin-one components are exactly

    g0=(r dot q)/2,   g1=g-g0,
    ||g0||^2=1/16,   ||g1||^2=3/16,   <g0,g1>=0.                   (10)

For a derivation, average the shared p using E[p_i p_j]=delta_ij/4. On its quadratic polynomial, the SU2 Casimir is

    C_p=-(Delta_p-D_p^2-2D_p)/4,  D_p=sum_i p_i partial_(p_i),

so C_p g0=0 and C_p g1=2g1. The two other path factors remain fundamental. Every edge in a given path contributes the same path Casimir, including inverse orientations. Therefore the two energies are

    epsilon_low=(3/4)(10-2m),   epsilon_high=epsilon_low+2m,          (11)

in units of alpha. Intermediate independent-spin assignments on the consecutive shared path do not occur: the function depends on that path only through its product. Equations (10)-(11) exhibit actual eigenvectors. They prove closure of the finite spectral orbit needed here; they are not a truncated matrix approximation to the full Hilbert space.

For the off-diagonal channel, center parity allows only the ordered pairs of faces (9,15) and (15,9): their symmetric-difference edge support is precisely the six-link F loop. To verify both magnitude and sign, set p=g2 g28 g3^-1, r=g14 g26 g15^-1 and q=g25. Then F=2p dot r, W9=p dot q, W15=r dot q. Each surviving triple Haar integral is

    <W9,F W15>=<W15,F W9>=1/8.

Both signs in (9) cancel, giving off-diagonal weight 1/4 at energy 3alpha. It is not zero and is not an adjustable coefficient.

Define the following exact symmetric matrix weights W_epsilon:

| epsilon | (00) | (01)=(10) | (11) |
|---|---|---|---|
| 3 | 19/4 | 1/4 | 1/8 |
| 9/2 | 0 | 0 | 1/8 |
| 6 | 0 | 0 | 3/8 |
| 15/2 | 0 | 0 | 9/4 |
| 8 | 0 | 0 | 9/8 |
| 17/2 | 0 | 0 | 3/8 |
| 9 | 0 | 0 | 3/8 |

These positive matrix weights give the full requested leading matrices at every s>=0 and z>0:

    [K_lead(s)]_ij=(alpha lambda)^2 sum_epsilon
                         (W_epsilon)_ij exp(-epsilon alpha s/hbar),
    [Sigma_lead(z)]_ij=(alpha lambda)^2 sum_epsilon
                         (W_epsilon)_ij/(epsilon alpha+z).          (12)

Here K_lead and Sigma_lead denote compressions of the full leading operators to span{f0,f1}, not an autonomous two-dimensional evolution. At s=0 their dimensionless kernel matrix is [[19/4,1/4],[1/4,19/4]], consistent with the actual Q1 multiplier. The 00 channel alone is one exponential, whereas the 11 channel contains all seven energies. Its first energy moment is 285/8, versus 57/4 in the reference channel. Both the off-diagonal and the nonconstant delay dependence reject a scalar reference replacement.

## Full-Hilbert remainder bounds and their regime

Define the full leading operators, before any channel compression,

    K_lambda^(2)(s)=(alpha lambda)^2 B1*exp(-s C0/hbar)B1,
    Sigma_lambda^(2)(z)=(alpha lambda)^2 B1*(C0+z)^-1B1.

Their norms are bounded by (25/4)(alpha lambda)^2 exp(-3alpha s/hbar) and (25/4)(alpha lambda)^2/(3alpha+z). The perturbation C_lambda-C0=alpha lambda QVmagQ is bounded by 40alpha lambda, and both generators have lower bound 3alpha. Differentiating the relative semigroup product first on the common domain, then extending its bounded derivative and integrating strongly, gives

    ||exp(-s C_lambda/hbar)-exp(-s C0/hbar)||
       <=40alpha lambda (s/hbar) exp(-3alpha s/hbar).

The bounded resolvent identity gives the analogous difference bound 40alpha lambda/(3alpha+z)^2. Sandwiching with B1 proves the explicit full-H3 operator errors

    ||K_lambda(s)-K_lambda^(2)(s)||
       <=250 alpha^3 lambda^3 (s/hbar) exp(-3alpha s/hbar),
    ||Sigma_lambda(z)-Sigma_lambda^(2)(z)||
       <=250 alpha^3 lambda^3/(3alpha+z)^2.                         (13)

The first quantity has units energy squared; the second has units energy. With u=alpha s/hbar, the first is 250alpha^2 lambda^3 u exp(-3u). It is uniformly at most [250/(3e)]alpha^2 lambda^3 for all delays, while the second is uniformly at most (250/9)alpha lambda^3 for all z>0. At lambda<=1/100 these become alpha^2/(12000e) and alpha/36000. The small-z bounds extend to the complementary inverse at z=0 because of (2); no uniform small-z bound on the FULL compressed resolvent in (7) is asserted. Nor is uniform relative accuracy at arbitrarily late delay inferred from the absolute kernel bound. There is no operator-norm time Taylor claim.

These estimates hold naturally for every lambda>=0, so the declared weak interval is included without a Neumann assumption. Positivity also gives Sigma_lambda(z)<=Sigma_lambda^(2)(z) in operator order; this is a self-energy inequality, not an order assertion for differences of noncommuting heat semigroups. Compression to the fixed two orthonormal channels cannot increase any error in (13).

A common scalar shift b of H,A,C leaves B unchanged and sends K(s) to exp(-bs/hbar)K(s), Sigma(z) to Sigma(z+b), and the full resolvent at z to the original full resolvent at z+b. Statements requiring positive z are used with z+b>0. Shifting only A or omitting the complementary energy shift is inconsistent. The independently executed positive noncommuting block fixture rejects the wrong Schur sign and a Volterra formula omitting returns, and checks consistent scalar shifts and lambda=0. It tests block algebra; the graph-specific spectrum is proved by (9)-(12).

Closest checked primary source: Burbano and Bauer, [arXiv:2409.13812v2](https://arxiv.org/html/2409.13812v2), Appendix B.3-B.4, Eqs. 134,145-155 and160-168, states the product Haar/Peter-Weyl electric structure and vertex invariant tensors. We checked the actual no-charge/girth hypotheses rather than importing a gap from another model. Path ordering and the twenty-face transport remain those checked in P2/Q1. Reading was targeted, not a full-paper audit. The finite path recoupling, exact channel weights, block identities and quantitative remainder constants are independently derived here; scientific priority is unverified.
