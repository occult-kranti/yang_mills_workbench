# R1 independent preparation — frozen before producer reading

This is a skeptical comparator, not admission or a ninth completed research loop. Neither current R1 producer has been read. The contract fixes the homogeneous I1/O1 full-link tensor product and initial four-site diagonal. Q2's physical invariant-space gap and positive magnetic compression do not enter. All Hamiltonians below are dimensionless; physical energies acquire the fixed factor delta=alpha/8.

## Initial inverse and domains

Write t=|tau|, M=7t, a=1-28t, r=||v||<=||R_Y||, and n_in(Y) for the number of retained stars contained in Y. Each star projector obeys Q_b<=sum_(x in star)Q_x, and each site belongs to at most four stars. Thus

`|<psi,D_Y psi>| <= 28t <psi,H0_Y psi>`.

This uses the actual initial diagonal D_b=Q_b phi_b Q_b, ||phi_b||<=M. It does not assume D_b positive. Since D_Y is a bounded self-adjoint finite sum, G_Y is self-adjoint on D(H0_Y), with unchanged form domain. D_Y Omega_Y=0 and G_Y>=a H0_Y>=a Q_Y. On the contract interval a>=381/416. Consequently Omega_Y is the unique ground state and the reduced inverse has norm at most 1/a, uniformly in Y and Lambda.

For u=(G_Y|Q_Y)^(-1)v, require all of the following, with no inference of an operator-domain estimate merely from a form estimate:

- `||u||<=r/a`, `||G_Y u||=r`, and `||G_Y^(1/2)u||<=r/sqrt(a)`.
- `||H0_Y^(1/2)u||<=r/a`.
- `u in D(H0_Y)` and `||H0_Y u||<=r[1+M n_in(Y)/a]`, by H0_Y u=v-D_Yu. This explicit graph bound may depend on Y.

The prescribed S=|u><Omega|-|Omega><u| is skew-adjoint, ||S||=||u||, and `[S,G_Y]=-A_Y` on the common operator domain. Direct multiplication fixes the sign: G_Y S=|v><Omega| and S G_Y=-|Omega><v|. In particular ||[S,H0_Y]||=||H0_Yu||, while the norms of H0_Y^(1/2)S and its adjoint counterpart are bounded by r/a.

Extension by identity outside Y preserves D(H0_Lambda); it does not map every exterior Hilbert-space vector into that domain. The local range {Omega_Y,u} and commutation with exterior H0 prove graph-domain preservation for exp(sS). Once this is established, the bounded commutator gives `||H0_Lambda exp(sS)psi|| <= ||H0_Lambda psi||+|s| ||H0_Yu|| ||psi||`. Bounded D_Lambda leaves the same operator and form domains. A full-volume statement must keep these domains before using a formal exponential series.

## Complete boundary comparator

Let C_Y contain every retained star meeting Y but not contained in it, n_cross=|C_Y|. On D(H0_Lambda), the exact defect is

`F_Y=[S_Y,H0_Lambda+D_Lambda]+A_Y=sum_(b in C_Y)[S_Y,D_b]`.

Each declared term has connected support Y union (b+G), cardinality at most |Y|+3, and norm at most 14t r/a. Therefore ||F_Y||<=14t n_cross r/a. Independently of shape, n_cross<=4|Y|-4n_in(Y). No incoming anchor can be dropped merely because it lies outside Y.

For the fixed weight 2^support-cardinality, the contribution at root x is at most `14t(r/a) 2^(|Y|+3) m_Y(x)`, where m_Y(x)=n_cross for x in Y, and m_Y(x)<=min(4,n_cross) outside Y. Hence a conservative weighted bound is `112t n_cross (2^|Y| r)/a`. These are bounds for the indexed declared-star decomposition, without silently regrouping terms on smaller physical face supports.

The exact cube counts, including L=1, are:

| Y | Interior stars | Crossing stars |
|---|---:|---:|
| Origin cube {0,...,L-1}^3 | (L-1)^3 | 3L^2-3L+1 |
| Bulk cube {1,...,L}^3 | (L-1)^3 | 6L^2-3L+1 |

The bulk cube has L^3+3L^2 touching anchors: its own L^3 anchors plus three incoming planes. The origin cube has L^3 touching anchors. Direct independent enumeration checks L=1,...,8 and all 167 connected nonempty subsets of {0,1}^3 inside a larger cuboid, including root multiplicities and union supports.

## Fixed actual SU2 source

For Lambda={0,1}^3, only the origin star is retained; Y={0} contains no full star. The free z-link character v=Tr(g_e)Omega_Y has norm one and h_0 v=6v, since the free fundamental Casimir is 3/4 in units alpha and delta=alpha/8. Thus u=v/6. The selected-strip ground remains unchanged throughout.

Every omitted square has at least two globally free edges; two distinct squares share at most one edge. A free edge different from e proves <Omega,phi_0 v>=0. It also integrates W_f^2 chi(g_e)^2 to 1/4. In a distinct-face cross term, a free edge unique to one face has odd central parity; chi(g_e)^2 remains even even if that edge is e. Hence every cross term vanishes. With all 21 faces retained,

`||phi_0 v||^2=(tau^2/9)(21/4)=7tau^2/12`.

Since D_0 Omega_Lambda=0 and D_0 v=phi_0 v,

`F_Y Omega_Lambda=-phi_0 v/6=(tau/18)sum_f W_f v`,

`||F_Y Omega_Lambda||^2=7tau^2/432`.

This is a strictly nonzero actual-model boundary defect for tau!=0. Only two of the 21 squares touch the chosen physical edge, but the other nineteen still contribute: the source acts on its complete onsite factor, and the projected D_0 has the declared star support. Replacing this sum by the two physically touching faces is a discriminating error, not a valid locality simplification. The source is the prescribed rank-two diagnostic; it is not identified with an O1-generated remainder. No lower bound for all growing Y follows from this singleton example.

## Acceptance challenges and scope

Accept only if both submissions prove the actual initial form comparison, inverse and graph-domain statements; cancel with the specified sign; retain every boundary star; and verify the prescribed source on Haar rather than on a finite-spin surrogate. Reject import of Q2's gap, positivity for signed D, omission of nineteen probe faces, a uniform graph bound justified only by a form inequality, or identification of the diagnostic with the generated residual. At tau=0 the boundary defect must vanish. The separate exact two-level fixture tests the bare/interacting inverse and wrong sign, and is explicitly only a lemma control.

The interacting inverse removes interior retained-D coupling from this local first-order cancellation. Crossing terms and their support-dependent bounds remain. This can refine O2's particular bare-inverse majorant, but proves neither closure nor failure of every subsequent interacting iteration. The initial gap of H0+D is not a gap of H0+D+R, numerical homogeneous stability, a thermodynamic representation result, or a continuum mass gap. R2 remains unselected.

The targeted [primary-source reading](https://arxiv.org/pdf/2108.13907) is recorded in r1-primary-source-map.json. Its evolving-interaction hypotheses and unevaluated small-coupling constant are not imported; the bounds above are direct workbench derivations. Fresh ordinary and optimized preparation outputs agree byte for byte and use runtime guards rather than assert.
