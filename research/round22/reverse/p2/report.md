# P2 reverse: exact Haar electric reduction, conditional-family mismatch

The specified maximal tree gives a genuine unitary Haar identification on all 16 chords. Its three-selected-chord isometry has an explicit Haar adjoint, and its image reduces the full electric generator. The complete induced operator is proved below with its form, operator and graph domains. This operator fails the prescribed conditional-family matching test: the training slope gives c=6 alpha, the reserved training curvature requires zeta=0, and the reserved y correlation then disagrees for every finite positive time.

This is the actual fixed 18-vertex, 33-link, all-vertex-Gauss SU2 graph, magnetic coefficient zero, normalized Haar vacuum 1 and T_a=-i sigma_a/2. All statements use fixed a>0, E_star>0, alpha/E_star>0 and hbar>0, common time t/hbar and no volume or regulator limit. c is an energy coefficient, zeta a dimensionless model parameter with |zeta|<1, kappa=0. These are analytic predictions, not measured calibration. No interacting/continuum transfer or scientific priority is claimed. Current forward/p2 and skeptical P2 work were not read.

## Tree, orientations and physical completions

Number edges axis x,y,z first and lexicographic tail second, as in C1. T={0,...,15,26} is connected on all 18 vertices and has 17 edges, hence is a tree. Root r=(0,2,0). Its complementary chord set is

    E\T={16,17,18,19,20,21,22,23,24,25,27,28,29,30,31,32}.

For the ordered signed root-to-v path, h_v is its product, and a chord e:s->t has L_e=h_s g_e h_t^-1. We use g_e -> k_s g_e k_t^-1, so h_v -> k_r h_v k_v^-1 and every L_e -> k_r L_e k_r^-1. The checker independently reconstructs every tree path, endpoint and full signed chord word, checks noncommuting rational-quaternion gauge transformations and rejects a missing endpoint inverse.

Selected physical trace completions are:

| Coordinate | Chord | Signed full-link word for its normalized trace | Distinct links |
|---|---|---|---|
| x | U=L28 | 14-,2+,28+,3-,15+,26- | 6 |
| y | V=L27 | 14-,12-,0+,27+,1-,13+,15+,26- | 8 |
| z | W=L24 | 14-,12-,24+,13+,15+,26- | 6 |

These are simple loops with distinct links. J3 x differs from P1 F9, whose word is 2+,28+,3-,25-. Both give x at the old 30-fixed-link section, but the full physical functions differ: setting only g25 nontrivial changes F9 and leaves J3 x=1. Thus the P1 c=4 alpha fit cannot be reused.

## Full Haar identification and selected adjoint

Keep the 17 original tree coordinates. At each fixed tree assignment, the independent changes g_e -> L_e=h_s g_e h_t^-1 on all 16 chords preserve product Haar. Fubini gives, initially for integrable functions and then for L2,

    dg_all = dg_T dL_16,
    integral |f(L(g))|^2 dg_all = integral |f(L)|^2 dL_16.

A gauge transformation k_v=h_v, with k_r=1, makes each tree link identity and turns each chord into L_e. Every invariant smooth physical function is consequently f(L) for a simultaneously conjugation-invariant f. For L2 equivalence classes use the product-coordinate transformation and invariance under the 17 independent non-root gauge transformations: invariants are independent of the tree variables almost everywhere. The remaining root transformation is simultaneous conjugation. This proves surjectivity without assigning section values to arbitrary L2 representatives.

Therefore J16:H16->Hphys is unitary. I3 embeds H3 into H16 by independence of the other 13 chords, and J3=J16 I3 is an isometry. Its adjoint is I3*J16*, where I3* integrates the other 13 L coordinates with normalized Haar. In particular J3*J3=I, J3 1=1, J3*1=1, and both maps preserve the corresponding integral state. I3* preserves simultaneous conjugation by Haar invariance. No chord is evaluated at identity in this adjoint.

The physical orthogonal projection P=J3 J3* equals Haar integration over the 13 unused ORIGINAL chord links while keeping T and edges 28,27,24. Indeed at fixed tree variables dg_e=dL_e for each integrated link. It commutes with every original link heat semigroup, hence with exp(-t H_E/hbar) and its spectral projections. Gauge invariance is preserved by link Haar integration. Thus the selected image reduces H_E, with no leakage assertion or mere compression assumption.

## Complete electric transport

Define skew-adjoint vector fields

    ell_e,a f(L) = d/ds f(...,exp(s T_a)L_e,...) at s=0,
    rho_e,a f(L) = d/ds f(...,L_e exp(s T_a),...) at s=0.

For q in T, let S_q be the component away from the root after cutting q, and let epsilon_q=+1 if q points away from the root, -1 otherwise. Put

    D_q,a = epsilon_q [sum_(chord e:s(e) in S_q) ell_e,a
                       - sum_(chord e:t(e) in S_q) rho_e,a].             (1)

The sums include BOTH occurrences for a chord with both endpoints in S_q, and all 16 chords. They do not retain only cut-crossing chords. At tree identity a left variation exp(sT_a) on q changes h_v to exp(epsilon_q sT_a) exactly when v is in S_q, so the induced chord variation is the flow of (1). Its second derivative is D_q,a^2, with no omitted coefficient derivative. A chord variation gives ell_e,a. Gauge covariance and Ad-invariance of the Casimir carry the summed identities back to arbitrary tree coordinates. Therefore on the invariant smooth core

    H16 = -alpha sum_a [sum_(16 chords e) ell_e,a^2
                        + sum_(17 tree links q) D_q,a^2].             (2)

Equivalently its closed form is

    q16(f)=alpha sum_a [sum_e ||ell_e,a f||^2 + sum_q ||D_q,a f||^2].    (3)

Each field preserves Haar, so there is no scalar/Jacobian term. In particular H16 1=0.

For completeness the domain argument can be given by finite representation blocks, without a formal-coordinate domain inference. Each ell/rho preserves the Peter-Weyl representation labels on each chord; (2) is a positive Hermitian matrix on each finite block and commutes with C0=sum_e C_e. Let n_qe count 0,1,2 endpoint occurrences in (1), m_q=sum_e n_qe, and K= max_e[1+sum_q m_q n_qe]. Cauchy-Schwarz and equality of the left/right gradient lengths give

    alpha q0(f) <= q16(f) <= alpha K q0(f),  q0=<f,C0 f>.              (4)

For this full tree the checker gives K=77. On a C0 eigenblock of eigenvalue lambda, H16's eigenvalues lie in [alpha lambda,alpha K lambda]. Its direct sum is therefore self-adjoint with form domain H1(SU2^16)^Ad and operator domain D(C0)=H2(SU2^16)^Ad. Finite invariant Peter-Weyl sums are a form and graph core. The bounds give graph-norm equivalence, with E_star fixing units. Pullback of a finite invariant Peter-Weyl sum is again a finite invariant Peter-Weyl sum on the full links; conversely the smooth gauge-fixed value of a physical polynomial is a chord polynomial. Thus J16 identifies the two cores. Equality on these cores closes to

    H_E J16=J16 H16,  J16 D(H16)=D(H_E).                              (5)

This also proves the full closed-form transport, not just its symbolic expression.

## The selected generator and its exact domains

On U,V,W only, the nonzero tree fields in (1) are:

| Tree edge | D_q,a on the selected coordinates |
|---|---|
| 0 | ell_V,a |
| 1 | -rho_V,a |
| 2 | ell_U,a |
| 3 | -rho_U,a |
| 12 | -(ell_V,a+ell_W,a) |
| 13 | rho_V,a+rho_W,a |
| 14 | -(ell_U,a+ell_V,a+ell_W,a) |
| 15 | rho_U,a+rho_V,a+rho_W,a |
| 26 | -(rho_U,a+rho_V,a+rho_W,a) |

Edges 4 through 11 give zero here, although they remain present in the full 16-chord form. Let C^ell_A=-sum_a(sum_(j in A)ell_j,a)^2 and C^rho_A analogously. The exact selected operator is

    H_eff/alpha = 3 C_U+3 C_V+C_W
                +C^ell_{VW}+C^rho_{VW}
                +C^ell_{UVW}+2 C^rho_{UVW}.                          (6)

The mixed terms in each square must be retained. Formula (6) and the corresponding sum-of-gradient-squares form act on simultaneous-Ad invariants, with form domain H1(SU2^3)^Ad, operator domain H2(SU2^3)^Ad and invariant polynomial core. The preceding representation-block proof applies with K=16 and lower constant 1. It also proves exact closure of the expression obtained by restricting (2).

Consequently J3 D(H_eff)=D(H_E) intersect ran(J3),

    H_E J3=J3 H_eff,
    exp(-t H_E/hbar) J3=J3 exp(-t H_eff/hbar) for all t>=0.            (7)

J3 is an isometry also for ||f||_G^2=||f||^2+||H f/E_star||^2, and for the form norm. Its adjoint maps D(H_E) to D(H_eff), intertwines there, and contracts the graph norm because P reduces H_E. These assertions concern the induced generator; they do not identify it with the conditional family. Equal scalar shifts cancel in an intertwining defect, and the actual constant grounds fix any proposed added scalar to zero.

The checker differentiates every full chord word through second order under all 99 original link/axis variations using exact quaternion jets. It compares these with the flows (1), checks the full and selected incidence budgets, and rejects removal of tree derivatives. The internal-chord omission control uses the invariant joint channel [Tr(L16 L28^-1)/2]y, with tree14 Casimir values 29/90 and -1/30. An earlier single-trace candidate was nondiscriminating and was replaced; source-review.json records that failed control gate. An additional joint-channel control rejects removal of mixed derivatives: at U=(3/5,4/5,0,0), V=(1/3,2/3,2/3,0), H_eff(xy)/alpha=13/10, whereas retaining only the diagonal 6C_U+8C_V+6C_W gives 21/10.

## Declared slope fit, curvature and full-time holdout

Every selected holonomy is Haar. Thus x,y,z have mean zero and variance 1/4. Each full-link derivative of a simple fundamental loop contributes Casimir 3/4, so the mapped physical eigenenergies are

    E_x=(9/2)alpha, E_y=6alpha, E_z=(9/2)alpha.                        (8)

The same values follow from (6). Center correlations by

    C_AB(t)=<A1,exp(-tH/hbar)B1>-conj(omega(A))*omega(B),

with the first slot conjugate-linear. Formula (7) identifies mapped physical and effective correlations exactly for all bounded selected multiplication observables. On affine complex channels aF+a0 and bF+b0 of a centered eigenchannel F it gives conj(a)b Var(F)exp(-tE/hbar); both independent scalar means cancel.

For the proposed conditional family A_zeta=-div_Haar[(1+zeta x)grad], the closed form is integral(1+zeta x)|grad f|^2. Since |x|<=1 and |zeta|<1, its form domain is H1 and its self-adjoint operator domain is the stipulated H2; smooth invariants are a core and the ground is 1. The vector fields give

    A0 x=3x/4, Gamma(x,x)=(1-x^2)/4, Gamma(x,y)=0,
    A_zeta f=(1+zeta x)A0 f-zeta Gamma(x,f),
    A_zeta x=3x/4+zeta(x^2-1/4),
    A_zeta y=3(1+zeta x)y/4.                                        (9)

The divergence term in (9) is essential. Haar parity, E[x^2]=1/4 and E[x^4]=1/8 give the nonzero designated training slopes

    C_J3x,J3x'(0)=-9alpha/(8hbar),
    C_xx,conditional'(0)=-3c/(16hbar).

Thus c=6alpha, leaving every zeta in (-1,1) unresolved by this slope. No reserved information enters this fit.

The reserved training curvature follows from ||H x||^2 on a smooth vector. Odd x and even x^2-1/4 are orthogonal, and ||x^2-1/4||^2=1/16. At the frozen c,

    physical curvature = (alpha^2/hbar^2)81/16,
    conditional curvature = (alpha^2/hbar^2)(81/16+9 zeta^2/4).        (10)

Exact equality requires zeta=0. This is a restriction from reserved information, not a second fit of c. For that sole candidate, the held-out y channel has full curves

    C_J3y,J3y(t)=exp(-6alpha t/hbar)/4,
    C_yy,conditional(t)=exp(-(9/2)alpha t/hbar)/4.                    (11)

The conditional-minus-physical discrepancy is positive for every finite t>0. At t_star=hbar/alpha it is (exp(-9/2)-exp(-6))/4, with a certified rational enclosure in the checker. Both variances remain nonzero. No admissible zeta fits all reserved data: indeed even before (10), the y initial slope from (9) is independent of zeta and already differs, but (11) explicitly provides the requested full-time test after the curvature restriction. Refitting c=8alpha to y would violate the designated training slope.

The exact electric reduction is admitted as a mathematical target here; matching to this scalar-clock affine-mobility family is rejected. The source of the discrepancy is different physical loop completions and their actual tree contributions, not a change of time or state. Q/R are unselected in this submission.

Targeted primary check: Burbano and Bauer, [arXiv:2409.13812v2](https://arxiv.org/html/2409.13812v2), Appendix C.1-C.2, Eqs. 230-244, states orbit-map conditions; C.3.2, Eqs. 273-274, describes tree variables; C.4.1, Eqs. 275-292, retains electric parallel transport and its Ad-invariant Casimir. We checked the unique-chord and gauge-equivalent-representative hypotheses on this tree. Haar isometry and all domain claims are proved above rather than inferred from a general pointwise section discussion. The path multiplication convention is stated explicitly and verified independently. Reading was targeted, not a full-paper audit, and source coupling constants are not substituted for alpha.
