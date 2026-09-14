# P2 frozen independent preparation

Prepared from contract p2.json, the five frozen instruction inputs, admitted
C1/P1/K1 evidence and the versioned primary source. Neither current P2
producer was inspected. These are independent comparators and acceptance
challenges, not admission of a producer result or selection of Q/R.

## Map and a.e. topology checklist

The tree is exactly edges 0 through 15 and 26, rooted at (0,2,0). Independent
enumeration verifies all 18 vertices are connected by its 17 links, leaving
16 chords. Let h_v be the signed root-to-v tree word and
L_e=h_s g_e h_t^-1. The change of variables

    (g_e)_33 <-> ((g_a)_{a in tree}, (L_e)_{e in chords})

is a smooth bijection. With tree coordinates fixed, each chord change is a
left/right Haar translation of its own g_e; Fubini gives the full normalized
product-Haar identity. The L2 isometry must be based on that measure identity.
For smooth all-vertex invariant F, genuine tree gauge fixing shows that the
transformed function depends only on L and is simultaneous-Ad invariant.
Smooth invariant density and the isometry's closed range then establish
onto identification without evaluating an arbitrary L2 representative on a
measure-zero tree section.

I3 is the isometric cylindrical inclusion of U=L28,V=L27,W=L24. Its adjoint
is integration over the other 13 independent Haar chord variables. Check the
adjoint identity, simultaneous-Ad preservation, constant ground and state.
Never replace that integral by evaluation at identity. These map claims are
separate from operator intertwining.

## Complete electric transport and domain comparator

Define l_e^a by L_e -> exp(t T_a)L_e, and r_e^a by
L_e -> L_e exp(t T_a), where T_a=-i sigma_a/2. For a tree edge k remove it
and let B_k be the component away from the root; epsilon_k is +1 if its
positive edge points into B_k and -1 otherwise. At the tree section its
original electric variation induces

    D_k^a = epsilon_k sum_{e in chords}
            [1_{s(e) in B_k} l_e^a - 1_{t(e) in B_k} r_e^a].

The required full quadratic form and core operator are

    q16[f]/alpha = sum_{e,a} ||l_e^a f||^2 + sum_{k,a} ||D_k^a f||^2,
    H16/alpha = sum_e C_e - sum_{k,a}(D_k^a)^2.

Every one of the 17 cuts and all 16 chord coefficient pairs are retained in
the preparation check output. A chord with both endpoints in B_k contributes
a conjugation derivative; it must not be discarded on general simultaneous
invariants. Individual-link conjugation invariance is a stronger hypothesis.
Signs between left and right derivatives matter even though changing one
whole D_k to its negative leaves its square unchanged.

A derivation must justify the second derivative and transformed form, not
only a first-order coordinate rule. One direct check fixes all tree variables
at identity and varies a single tree edge: h_v changes by exp(epsilon tT)
precisely on B_k, so the entire chord path is the flow of D_k. Gauge
invariance and the Haar identity carry the resulting Casimir sum to the form.

All l/r fields are Haar divergence-free. The form dominates alpha times the
16-chord product Casimir form and has a finite upper multiple by
Cauchy-Schwarz. Each D_k commutes with the product Casimir C0, and its
Peter-Weyl eigenspaces are finite dimensional. Form comparison on these
blocks therefore gives equivalence of graph norms as well as form norms:
the domains are H1 and H2 respectively, intersected with simultaneous-Ad
invariants. This also supplies a graph-core argument. The producer may use
matched compact elliptic theory instead, but must state the actual operator
domain and extend the core equality to it. No scalar appears; both operators
annihilate the constant.

## Selected image and shared tree terms

For selected functions the nonzero cuts are 0,1,2,3,12,13,14,15,26. Write
K_L(S)=-sum_a(sum_{e in S}l_e^a)^2 and analogously K_R(S). The independent
selected operator comparator, before any use of simultaneous-Ad identities,
is

    H_eff/alpha = 3C_U+3C_V+C_W
                  +K_L(V,W)+K_R(V,W)
                  +K_L(U,V,W)+2K_R(U,V,W).

This contains mixed derivatives. Counting only chord Casimirs or only the
diagonal contributions of these squares changes the operator. On class
functions of one selected variable it gives coefficients 6,8,6 respectively.
On simultaneous-Ad functions the total left and right Casimir agree, which
permits an equivalent simplification but does not remove all cross terms.

Each full D_k preserves cylindrical selected functions. Integration over
unused chord variables kills their l/r derivatives and commutes with the
remaining derivatives. Thus the Haar projection should commute with H16 on
the smooth core. Prove domain preservation and extend this to a reducing
orthogonal projection, giving H_E J3=J3 H_eff on the full operator domain
and exp(-t H_E/hbar)J3=J3 exp(-t H_eff/hbar). Original coordinates provide a
second route: selected holonomies depend only on the tree plus three edges;
the electric sum preserves that cylindrical all-vertex invariant subspace.
A mere compressed quadratic form is insufficient to claim this relation.

## Changed physical completions and fixed-clock reserve

The selected fundamental traces are traces of these signed original words:

| Variable | Tree-completed word | Distinct links | Physical energy |
|---|---|---:|---:|
| x | 14-,2+,28+,3-,15+,26- | 6 | 9 alpha/2 |
| y | 14-,12-,0+,27+,1-,13+,15+,26- | 8 | 6 alpha |
| z | 14-,12-,24+,13+,15+,26- | 6 | 9 alpha/2 |

They have Haar mean zero and variance 1/4. J3 x is not P1 F9: their old
30-fixed-link section values coincide, but their physical loop supports and
electric eigenvalues differ. This is a necessary rejection control against
reusing P1's c=4 alpha clock.

For the declared kappa=0 conditional mobility, direct divergence gives

    A_zeta x = (3/4)x + zeta(x^2-1/4),
    A_zeta y = (3/4)(1+zeta x)y.

The conditional x slope is -3c/(16 hbar), independent of zeta. The new
physical slope is -9 alpha/(8 hbar), so the sole training fit is c=6 alpha.
All |zeta|<1 remain allowed by that slope. The reserved training curvature
then gives, in units alpha^2/hbar^2,

    physical: 81/16,
    conditional: 81/16 + (9/4)zeta^2.

Here E[x^2]=1/4 and E[x^4]=1/8; the orthogonal term x^2-1/4 has squared
norm 1/16. Curvature matching forces zeta=0 without any refit of c. At this
candidate the full reserved y curves at the same physical time are

    physical = exp(-6 alpha t/hbar)/4,
    conditional = exp(-(9/2) alpha t/hbar)/4.

They disagree at every finite positive time. At t_star=hbar/alpha,
conditional minus physical is (exp(-9/2)-exp(-6))/4, strictly between
0.0021575610903939 and 0.0021575610903941 by an independent exact enclosure.
The conditional y slope is already independent of zeta and disagrees at
c=6 alpha, so allowing nonzero zeta cannot rescue the entire reserved curve.
For nonzero zeta, y must not be described as a simple eigenchannel.

Reject omitted mobility drift, use of uncentered complex covariance, zero
variance calibration, a second fit from reserved information, and promotion
of one slope to a semigroup relation. Every complex first-channel coefficient
must be conjugated. The constant ground fixes the scalar normalization.

## Primary-source and scope checks

Targeted recheck: Burbano and Bauer,
[arXiv:2409.13812v2](https://arxiv.org/html/2409.13812v2),
28 September 2024, Appendix C.3.2, Eqs. 273-274, and C.4.1,
Eqs. 275-292; reuse the previously read B.3-B.4.1 and C.1-C.2 conventions.
The present finite connected simple graph satisfies the stated tree setup.
The paper's path-product order differs from the contract's convention, so
derive signs from the actual signed graph. Its electric conjugation identity
requires disjoint transport paths and differentiated links; a crossing case
cannot silently use that identity. The direct cut-flow derivation avoids
such an import. Haar a.e. continuity and the full graph-domain realization
still require the explicit arguments above. Reading is targeted, not a
whole-paper audit; scientific priority remains unverified.

All scales, the graph and the electric endpoint remain fixed. A valid map
and exact induced electric reduction would not establish a match with this
conditional mobility family, physical calibration, an interacting reduction
or a continuum theory. Freeze this preparation before reading either current
producer; await the advisor's both-frozen opening. No six-loop ranking or
Q/R selection is performed here.
