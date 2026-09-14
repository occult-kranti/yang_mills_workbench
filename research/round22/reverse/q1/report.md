# Q1 reverse: correlated magnetic leakage and compressed dynamics

For the actual twenty-face magnetic action, the P2 three-chord image ceases to reduce the Hamiltonian whenever lambda>0. The exact conditional variance is the strictly positive multiplication function

    d(U,W)=19/4+[Tr(UW^-1)/2+x+z]/2,       4 <= d <= 25/4.

The compressed heat evolution first differs from the autonomous compression at second order. This report proves the full conditional moments, closed domains, a vectorwise small-time coefficient and an all-time operator-norm bound. It does not identify the Haar reference with an interacting ground or make an interacting/continuum transfer. Q2 is not selected here.

The fixed contract is the actual 18-vertex, 33-link, 20-face fully gauged SU2 graph, P2 tree T={0,...,15,26}, root (0,2,0), and selected U=L28,V=L27,W=L24. J=J3 and P=JJ* use normalized product Haar, integrating the other 13 chords. H_E=alpha sum_e C_e with fundamental Casimir 3/4, and

    H_lambda=H_E+alpha lambda V_pot,
    V_pot=sum_(p=0)^19 (1-W_p),       W_p=Tr(physical face holonomy)/2.

Here lambda>=0 is a new dimensionless magnetic deformation; a>0, E_star>0, alpha/E_star>0 and hbar>0 remain fixed. Time is the same physical t/hbar throughout. The vector Omega=1 is the normalized Haar reference and electric vacuum only. Current forward/q1 and skeptical Q1 solutions were not read.

## All twenty faces after the genuine tree map

For D_j=L_j, remove tree links from the ordered signed plaquette word in the tree-gauge representative. The result is inside a trace, so root conjugations cancel. J16's unitary map, not a new null-section evaluation on arbitrary L2 functions, transports this bounded multiplication operator. Independent reconstruction gives:

| Face ID | Axes/base | Ordered chord word |
|---|---|---|
| 0 | xy000 | D16 |
| 1 | xy001 | D17 |
| 2 | xy010 | D18 |
| 3 | xy011 | D19 |
| 4 | xy100 | D20 D16^-1 |
| 5 | xy101 | D21 D17^-1 |
| 6 | xy110 | D22 D18^-1 |
| 7 | xy111 | D23 D19^-1 |
| 8 | xz000 | V W^-1 |
| 9 | xz010 | U D25^-1 |
| 10 | xz020 | D29 |
| 11 | xz100 | D30 V^-1 |
| 12 | xz110 | D31 U^-1 |
| 13 | xz120 | D32 D29^-1 |
| 14 | yz000 | D25 W^-1 |
| 15 | yz010 | D25^-1 |
| 16 | yz100 | D16 U D17^-1 V^-1 |
| 17 | yz110 | D18 D29 D19^-1 U^-1 |
| 18 | yz200 | D20 D31 D21^-1 D30^-1 |
| 19 | yz210 | D22 D32 D23^-1 D31^-1 |

Every table entry carries normalized trace 1/2, and all twenty enter V_pot. The checker rebuilds the original edges, paths and signed faces, compares C1's complete signed ledger, and verifies every original/chord trace identity on a noncommuting rational configuration. Evaluating the omitted thirteen chords at identity would give a different action and is not the conditional expectation used here.

## Exact conditional mean, second moment and cross faces

Let E denote Haar integration over the omitted chords. Define

    tau=Tr(VW^-1)/2,  r=Tr(UW^-1)/2,  x=Tr U/2,  z=Tr W/2,
    S=sum_p W_p,     m=20-tau.

Every face other than 8 contains an omitted chord exactly once, so its conditional mean is zero. Thus E[S]=tau and E[V_pot]=m.

Each such face has conditional second moment 1/4: freeze its other matrices and integrate one omitted Haar matrix; its holonomy is Haar. For a pair of different faces, if their omitted-chord sets differ, a chord in their symmetric difference occurs exactly once in the product, killing its integral. The table proves the only coincident nonempty omitted sets occur for faces 9,14,15, all using D25. No probabilistic independence of faces is assumed.

Represent SU2 by unit quaternions u,w,q in R4. Normalized Haar is the rotationally invariant probability on S3; sign symmetry and sum_i q_i^2=1 give E[q_i]=0 and E[q_i q_j]=delta_ij/4. The three shared-chord faces are u dot q, q dot w and q_0. Consequently

    E[W9 W14]=r/4,  E[W9 W15]=x/4,  E[W14 W15]=z/4.                 (1)

These terms survive conditionally and generally have nonzero values. They disappear only after further integration over the selected Haar variables. Summing the diagonal terms and twice each off-diagonal pair gives

    E[S^2]=tau^2+19/4+(r+x+z)/2,
    E[V_pot^2]=(20-tau)^2+d,
    d=19/4+(r+x+z)/2.                                              (2)

The checker contracts exact quaternion coordinate polynomials with Haar moments for every one of the 210 unordered face pairs. It checks the resulting polynomial functions modulo the three selected unit-quaternion identities, independently of the preceding omitted-set proof. A nonzero cross-face fixture rejects replacing d by the constant 19/4.

The function is strictly positive with sharp bounds. Writing e0=(1,0,0,0),

    d=4+||u+w+e0||^2/4.                                           (3)

The norm in (3) is at most 3. Its minimum zero occurs at u+w=-e0, for instance u=(-1/2,sqrt(3)/2,0,0), w=(-1/2,-sqrt(3)/2,0,0); the maximum 3 occurs at u=w=e0. Normalized Haar has full support, and d is continuous and conjugation invariant, so these are the essential extrema even on H3. Also

    E_H3[d]=19/4,   E_H3[d^2]=91/4,
    E_Hphys[V_pot]=20, E_Hphys[V_pot^2]=405, Var_Haar(V_pot)=5.       (4)

The d in (2) is a multiplication operator function, not its mean 19/4 or a numerical fixture.

## Closed domains, compression and actual leakage

Each W_p is real with |W_p|<=1. Thus V_pot is smooth bounded self-adjoint multiplication, 0<=V_pot<=40. H_lambda is self-adjoint on exactly D(H_E)=H2(SU2^33)^Gauss, nonnegative for lambda>=0, with closed form domain H1 and form q_E+alpha lambda integral V_pot|f|^2. Bounded perturbation preserves the original invariant polynomial graph core. One direct self-adjointness justification is the resolvent Neumann series for sufficiently large imaginary spectral parameter followed by closedness and symmetry; its bound uses ||alpha lambda V_pot||<=40alpha lambda. The full J16 unitary transports the same form and operator to H16+alpha lambda M_(20-sum W_p) on the P2 H2 domain. Full Hilbert equivalence is preserved.

Since P reduces H_E, the autonomous selected compression is

    A_lambda=J*H_lambda J=H_eff+alpha lambda M_m                  (5)

on D(H_eff)=H2(SU2^3)^Ad, with H1 form domain and invariant polynomial core. It is self-adjoint and nonnegative; indeed m lies in [19,21]. Its construction is legitimate even though the selected image does not reduce H_lambda.

Let Q=I-P. The off-diagonal map, initially on the core and then boundedly extended, is

    B_lambda=Q H_lambda J=alpha lambda Q V_pot J,
    B_lambda* B_lambda=(alpha lambda)^2 M_d.                        (6)

Equation (6) follows from J*V_pot^2 J-(J*V_pot J)^2 and (2). Hence for every f in H3,

    2 alpha lambda ||f|| <= ||B_lambda f|| <= (5/2)alpha lambda||f||,
    ||B_lambda||=(5/2)alpha lambda,
    ||B_lambda 1||^2=(19/4)(alpha lambda)^2.                         (7)

Thus no nonzero selected vector has zero leakage for lambda>0, and this particular selected image does not reduce H_lambda. At lambda=0, B_lambda=0 and the admitted exact electric reduction is recovered for all times.

The Haar reference is not an interacting eigenvector: H_lambda 1=alpha lambda V_pot is nonconstant, and its residual after subtracting its mean energy 20alpha lambda has squared norm 5(alpha lambda)^2. No scalar shift can turn it into an eigenvector. We therefore do not call the matrix elements below stationary interacting correlations or treat their reference vector as the interacting ground.

## First discrepancy and a bound with the unbounded domains retained

Write T_lambda(t)=J*exp(-tH_lambda/hbar)J and E_A(t)=exp(-t A_lambda/hbar). For f in the selected invariant polynomial core, Jf belongs to D(H_lambda^2): H_E and multiplication by V_pot both preserve the physical polynomial core. The same holds for A_lambda. The spectral Taylor formula applied vectorwise gives

    [T_lambda(t)-E_A(t)]f
       = t^2/(2hbar^2) [J*H_lambda^2 J-A_lambda^2]f + o_f(t^2)
       = (alpha lambda t/hbar)^2 M_d f/2 + o_f(t^2).                 (8)

The first derivatives coincide with -A_lambda/hbar. Inserting P+Q between the two core Hamiltonians proves the second equality in (8); (6) supplies the positive coefficient. On the explicit core vector 1,

    <1,[T_lambda(t)-E_A(t)]1> = (19/8)(alpha lambda t/hbar)^2+o(t^2),
    ||[T_lambda(t)-E_A(t)]1||/(alpha lambda t/hbar)^2 -> sqrt(91)/4   (lambda>0). (9)

This is already a decisive dynamical defect. There is also an independent bounded-off-diagonal Duhamel argument, which avoids inferring a norm estimate from core Taylor terms. On ran(P) plus ran(Q), let

    G=J A_lambda J* direct-sum C_lambda,
    C_lambda=Q H_E Q+alpha lambda Q V_pot Q on D(H_E) intersect ran(Q),
    K=H_lambda-G.

Because P reduces H_E, G is self-adjoint on D(H_E), nonnegative by its compressed forms, and K is a bounded self-adjoint off-diagonal block with ||K||=||B_lambda||. H_lambda and G have the same domain and contractive heat semigroups.

For domain vectors differentiate the product of their two semigroups on the common domain. The derivative consists only of the bounded K term and extends strongly to all vectors. Integrate vectorwise, then use boundedness and density. Applying the resulting Duhamel identity twice, the term with one K vanishes after compression. With 0<=u<=s<=t the exact remainder is

    T_lambda(t)-E_A(t)
      = hbar^-2 integral_0^t integral_0^s
        E_A(t-s) B_lambda* Q exp(-(s-u)H_lambda/hbar) Q B_lambda E_A(u)
        du ds.                                                     (10)

All integrals here are strong vector integrals; a norm Bochner integral is not assumed. The bounded integrand and contraction estimates imply

    ||T_lambda(t)-E_A(t)|| <= (25/8)(alpha lambda t/hbar)^2,
    ||T_lambda(t)-E_A(t)|| <= 1,                         for all t>=0. (11)

The second inequality follows because both operators are positive contractions. Strong continuity in the rescaled triangle in (10), with bounded-vector domination, upgrades the coefficient to

    [T_lambda(t)-E_A(t)]/(alpha lambda t/hbar)^2 -> M_d/2 strongly
    on every H3 vector as t down to zero, for fixed lambda>0.        (12)

This is not an operator-norm Taylor expansion. Nevertheless (11), the sharp essential maximum of d, and lower semicontinuity of the operator norm under strong convergence imply the scalar norm asymptotic

    ||T_lambda(t)-E_A(t)||/(alpha lambda t/hbar)^2 -> 25/8.           (13)

No exchange with a varying coupling or regulator is used. If T_lambda were an autonomous strongly continuous semigroup, its positive self-adjoint members would have a self-adjoint generator agreeing with A_lambda on its graph core, hence that generator would be A_lambda. Equation (8) contradicts this for lambda>0. This excludes autonomy of this compressed family, not every possible physical reduction.

Scalar terms are retained throughout. A common real shift bI changes both compressed propagators by the same factor exp(-bt/hbar) and leaves B_lambda and M_d unchanged. It therefore preserves the leading coefficient and the failure of closure, while multiplying the bound (11) by that factor if positivity/contraction is lost after shifting. Dropping 20alpha lambda from only one generator already gives an erroneous first derivative. Changing the scalar cannot remove the nonconstant residual in (4).

The exact controls also include an independent finite positive block-matrix check of the second-order compression identity, unequal/common scalar shifts and zero coupling. That fixture checks the block algebra only; the actual SU2 leakage and bounds are established by (1)-(7), not by a finite matrix surrogate.

Closest checked primary result: Burbano and Bauer, [arXiv:2409.13812v2](https://arxiv.org/html/2409.13812v2), Appendix B.3, Eqs. 148-152, supplies the full-link electric/magnetic conventions; Appendix C.4.1, Eqs. 275-278, gives ordered plaquette transport under a genuine maximal tree. We checked the actual twenty signed words rather than substituting a schematic reduced action. The source's orientation and coupling conventions are translated to this frozen contract. Reading was targeted; this is not a full-paper audit or a scientific-priority comparison. Conditional Haar moments and the strong Duhamel bounds above are independently derived.
