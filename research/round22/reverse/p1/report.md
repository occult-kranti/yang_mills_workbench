# P1 reverse: the section fails as a Hilbert and electric-generator map

The frozen P1 section is not closable in L2, fails even continuity in the electric graph norm, does not preserve the Haar state, and cannot intertwine the declared generators for any c. Its designated training slope uniquely gives c=4 alpha. At this clock the held-out correlation is wrong at every positive time. These are failures of this particular map and proposed clock; physical calibration and other reductions remain open.

All statements concern precisely the finite electric endpoint in contract p1.json: 18 fully gauged vertices, 33 links, magnetic coefficient zero, normalized product Haar states and constant vacuum. H_E=alpha sum_e C_e on the declared invariant H2 domain, and H_c=c(C_U+C_V+C_W) on its invariant H2 domain. T_a=-i sigma_a/2 fixes C_fund=3/4. E_star, alpha/E_star>0, hbar>0, a>0 and graph volume stay fixed. kappa=zeta=0. No conclusion transfers to interacting J2, homogeneous O, continuum Yang–Mills or a measured clock calibration.

The derivation below was completed without reading current forward/p1 or skeptical P1 work. The inherited C1 ledger is an explicitly shared contract premise, independently reconstructed here. The checker uses only Python standard libraries; finite checks support the proofs and do not replace them.

## Actual graph and section

Order positive edges by axis x,y,z, then by lexicographic tail (x,y,z). For each ordered axis pair xy,xz,yz, order admissible face bases lexicographically. A face based at v with axes a,b has signed word

    (v,a)+, (v+e_a,b)+, (v+e_b,a)-, (v,b)-.

This gives 12 x links, 12 y links, 9 z links, and 8 xy, 6 xz, 6 yz faces. The checker reconstructs all vertices, endpoints and 20 signed face words, comparing each field with C1. Active edges are exactly 28=U, 27=V and 24=W. The nonconstant restrictions are:

| Face | Active word | Normalized trace |
|---|---|---|
| 8 xz000 | V W^-1 | t |
| 9 xz010 | U | x |
| 11 xz100 | V^-1 | y |
| 12 xz110 | U^-1 | x |
| 14 yz000 | W^-1 | z |
| 16 yz100 | U V^-1 | w |
| 17 yz110 | U^-1 | x |

The remaining 13 faces restrict to 1. Thus the inherited nonconstant action is 3x+y+z+w+t; this static statement alone identifies no generator.

A spanning tree of the connected graph has 17 links, leaving E-V+1=16 loop variables with residual simultaneous root conjugation. The subgraph of the 30 fixed links is itself connected and has 13 cycles. A spanning tree chosen within it fixes 17 gauge links; the other 13 fixed links impose conditions on genuine loop holonomies. For example F0 can have arbitrary fundamental trace physically, but its section is always 1. Consequently this section is not a gauge representative of every physical configuration. This reasoning does not assume a uniform quotient dimension at configurations with stabilizers.

The smooth restriction does land in smooth simultaneous-conjugation invariant functions: applying the same vertex gauge transformation h at all 18 vertices preserves every fixed identity and conjugates all three active links. This pointwise core map is the only map established by the static prescription.

## Explicit domain obstruction and state defect

Let Q_p denote the oriented face holonomy, and let chi_n be the spin n/2 character, dimension d=n+1. Products of independent Haar links make every Q_p Haar. The character formula chi_n(cos theta)=sin((n+1)theta)/sin theta and Haar class measure (2/pi)sin^2 theta dtheta show

    integral chi_n = 0 (n>=1), integral |chi_n|^2 = 1, chi_n(I)=n+1.

These identities also follow by Schur orthogonality. Therefore f_n=chi_n(Q_0)/(n+1) consists of gauge-invariant smooth core functions, ||f_n||=1/(n+1)->0, while R f_n=1. This is precisely a nonclosability sequence for R:L2_phys -> L2_cond. No bounded extension, nor any closed operator extension agreeing on the smooth core, exists. The state already fails on F0=chi_1(Q_0)/2: omega_phys(F0)=0 and omega_cond(RF0)=1.

There is also a sequence converging in the source electric graph norm, with no appeal to a trace theorem. The following constant-section faces are pairwise edge-disjoint:

| Face | Signed edge word |
|---|---|
| F0 xy000 | 0+,16+,2-,12- |
| F1 xy001 | 1+,17+,3-,13- |
| F13 xz120 | 10+,32+,11-,29- |

Set psi_n=(n+1)^-3 product_{p=0,1,13} chi_n(Q_p). Edge disjointness makes their holonomies independent Haar, even though some vertices may be shared. Each link Casimir acts on the spin-n/2 matrix entries, including inverse links, with eigenvalue n(n+2)/4. Thus

    ||psi_n||^2=d^-6, R psi_n=1,
    H_E psi_n=3 alpha n(n+2) psi_n.

In the dimensionally defined graph norm ||f||_G^2=||f||^2+||H_E f/E_star||^2,

    ||psi_n||_G^2 = d^-6 + 9(alpha/E_star)^2 n^2(n+2)^2/d^6
                  <= d^-6 + 9(alpha/E_star)^2/d^2 -> 0.

R is not closable even when its source core is endowed with this graph norm: its image still converges to the nonzero constant. The representation index varies only test functions; it does not change a physical regulator, graph, energy unit or coupling.

## The core equation already fails

For each actual elementary fundamental face, every one of its four distinct link Casimirs contributes 3/4, whatever its orientation. Hence H_E F_p=3 alpha F_p. Differentiation is performed on the full smooth function before restriction. On F0,

    R H_E F0=3 alpha, while H_c R F0=H_c 1=0.

The L2_cond norm of this defect is 3 alpha for every c>0. No scalar adjustment repairs it: applying (H_E+lambda_E) and (H_c+lambda_c) to the constant core vector first requires lambda_E=lambda_c, after which the same defect remains. The stipulated zero-energy grounds separately fix both shifts to zero.

The number of fixed electric derivatives lost by restricting first is four for F0, three for F9 and two for F16. Replacing the full 33-link electric sum by the active-link sum before differentiating changes the operator. No unbounded commutator, unsanctioned differentiation of a semigroup vector or unsupported domain exchange is used: all these identities hold directly on invariant Peter-Weyl polynomials in the declared domains.

## Designated training slope and reserved full time

For the inner product conjugate-linear in its first argument use

    C_AB(t)=<A Omega, exp(-t H/hbar) B Omega>-conj(omega(A))*omega(B).

Both F9 and F16 have mean zero, variance 1/4 and physical energy 3 alpha. Conditionally x and w have mean zero and variance 1/4: U and UV^-1 are Haar. The energies are 3c/4 for x, and 3c/2 for w, since both U and V contribute to the latter. These are core eigenvectors, so their spectral semigroup formulas hold for all t>=0 without extra domain assumptions.

The nonzero designated slopes are

    C_F9,F9'(0) = -3 alpha/(4 hbar),
    C_xx'(0)    = -3 c/(16 hbar).

Their equality fixes c=4 alpha uniquely. This value is frozen before consulting the held-out channel; no data calibration is claimed. As an eigenchannel the training correlation then agrees at all times, but only its slope was used to choose c.

At the same physical time t, the reserved channel gives

    C_F16,F16(t)=exp(-3 alpha t/hbar)/4,
    C_ww(t)    =exp(-6 alpha t/hbar)/4.

Their difference is strictly positive for every finite t>0, vanishes at t=0, and tends to zero as t tends to infinity. At t_star=hbar/alpha it is (exp(-3)-exp(-6))/4. The checker encloses this value with exact rational Taylor remainders and supplies a decimal rational enclosure. Refitting c=2 alpha to w would break the designated x slope, and is disallowed. At the fitted clock the F16 core defect is -3 alpha w, with squared norm 9 alpha^2/4.

For complex channels A=aF+a0 I, B=bF+b0 I with a centered eigenchannel F, the centered correlation is conj(a)b Var(F) exp(-tE/hbar); the two constant means cancel exactly. The checker changes both complex constants and rejects omission of either centering or the adjoint. This prevents the real training fixtures from silently masking a wrong correlation convention.

## A justified next repair, not an executed new loop

The finite maximal-tree change of variables retains all 16 chord holonomies. Successive Haar-invariant changes of variables separate the 17 tree gauge variables; gauge-invariant functions then have exactly their product-Haar L2 norm on the 16 holonomies, with residual simultaneous conjugation. This offers a genuine Hilbert identification. Because the fixed-edge subgraph is connected, its spanning tree can be selected so the three active edges are chords. Haar integration over the other 13 chord variables, in place of evaluating them at identity, defines a state-preserving L2 contraction by Jensen and Fubini and preserves simultaneous conjugation. This repairs the identified measure obstruction. It does not prove that the three-variable image is invariant under the transformed electric generator, or that its compression equals H_c. The transformed generator, its domain and any further fit/holdout would have to be selected and examined after P1 review. P2 is not selected here.

Targeted primary check: Burbano and Bauer's [general-graph gauge formulation](https://arxiv.org/html/2409.13812v2), Appendix B.3–B.4, Eqs. 148–155, records the invariant Lie-algebra normalization, link Casimir electric sum and Peter-Weyl Hilbert structure. Appendix C.3.2, Eqs. 273–274, gives maximal-tree loop variables. Appendix C.4.1, Eqs. 275–280, distinguishes Hilbert equivalence from the required Hamiltonian relation and displays parallel transport in electric transformations. These passages support the setup and proposed repair; the graph-specific obstruction, constants and clock discrepancy above are independently derived. The source's coupling convention is not substituted for contract alpha.
