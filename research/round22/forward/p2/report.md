# P2 forward: exact Haar/electric reduction, conditional-family mismatch

P2 repairs the failed section: J16 is unitary onto the physical invariant
Hilbert space, and J3 is an isometry onto a reducing subspace of the pure
electric Hamiltonian. Its induced electric generator includes all tree
derivatives and shared cross terms. The designated slope fixes c=6alpha;
the reserved curvature forces zeta=0, but the reserved y curve still
disagrees. These are separate, exact finite-graph conclusions. No current
opposing P2 evidence was consulted before freeze.

## 1. Actual tree and the new physical completions

Use the frozen 18-vertex, 33-edge graph and the original axis/lexicographic
edge IDs. T={0,...,15,26} is connected with 17 edges and hence is a tree,
rooted at r=(0,2,0). Its 16 chords are 16,...,25,27,...,32. For a signed
root-to-v path p_v let h_v be its ordered group product. With the explicit
gauge convention g_e -> k_s g_e k_t^-1, h_v -> k_r h_v k_v^-1 and

    L_e=h_s g_e h_t^-1 -> k_r L_e k_r^-1.

The checker reconstructs every path and independently compares every
original signed face with the admitted C1 ledger. The selected words are

| Variable | Rooted loop, signed original edge IDs | Distinct links |
|---|---|---|
| U=L28 | 14-,2+,28+,3-,15+,26- | 6 |
| V=L27 | 14-,12-,0+,27+,1-,13+,15+,26- | 8 |
| W=L24 | 14-,12-,24+,13+,15+,26- | 6 |

Consequently J3 x=Tr(L28)/2 is a six-link physical Wilson observable,
different from P1's four-link F9 even though their old section values
coincide. The new completion, not its section value, determines its clock.

## 2. Haar identification, adjoints, state, and topology

Keep all tree variables t=(g_a)_(a in T). For each fixed t, replacing each
chord g_e by L_e=h_s(t)g_e h_t(t)^-1 is a left/right Haar-preserving
change in that independent variable. Fubini therefore gives, for every
integrable test function,

    dg_(33)=dt_(17) dL_(16).

This is a global smooth diffeomorphism of compact products: its inverse
keeps the tree and uses g_e=h_s(t)^-1 L_e h_t(t) on each chord.
The gauge transformation k_v=h_v sets every tree variable to identity
and the chords to L_e. Root gauge remains simultaneous conjugation.
On smooth gauge-invariant functions this proves dependence only on L,
with simultaneous-Ad invariance. Density by gauge-averaged Peter-Weyl
polynomials and the Haar identity extend the identification to all
invariant L2 functions, without evaluating arbitrary representatives on
a null section. Thus J16 f(g)=f(L(g)) is onto and unitary from H16 to Hphys,
and J16 1=1. On the full coordinate product its adjoint integrates the
tree variables; on Hphys it is the unitary inverse.

I3 f(L)=f(L28,L27,L24) is an isometry H3->H16. Its adjoint is

    (I3*F)(U,V,W)= integral_(other 13 chords) F(L) dL_omitted.

Fubini/Jensen prove this contraction, and Haar invariance makes its output
simultaneous-Ad invariant. J3=J16 I3, J3*=I3*J16*, J3*J3=I,
and P=J3 J3* is an orthogonal projection. Both maps preserve constants
and ground means; J3 preserves inner products, variances and complex
centering. Integrating omitted variables is essential: evaluating them
at identity would reproduce P1's unbounded restriction problem.

## 3. Full electric transport, including every tree link

Define left and right vector fields by
ell_e^a f(L)=d/dt f(...,exp(tT_a)L_e,...)|0 and
r_e^a f(L)=d/dt f(...,L_e exp(tT_a),...)|0. Both are skew-adjoint on
product Haar and C_e=-sum_a(ell_e^a)^2=-sum_a(r_e^a)^2.
For tree edge b write eta_b(v)=+1 or -1 if the signed root path to v
uses b, and 0 otherwise. Define the complete first-order field

    D_b^a=sum_(16 chords e)[eta_b(s_e) ell_e^a-eta_b(t_e) r_e^a].

At tree identity, varying g_b=exp(tT_a) sends each chord to
exp(t eta_b(s_e)T_a)L_e exp(-t eta_b(t_e)T_a); hence its first and
second derivatives are D_b and D_b^2. At general tree coordinates the
Lie algebra basis is rotated by the common prefix adjoint. That prefix
does not depend on the varied tree edge; the orthogonal adjoint rotation
leaves the sum of squares unchanged. Equivalently the Casimir is gauge
invariant, so the computed equality at tree identity extends to every
configuration. Chord variation contributes its own C_e. Thus, on the
invariant smooth core, the complete transported operator and form are

    H16=alpha[sum_(16 chords) C_e-sum_(17 tree b,a)(D_b^a)^2],
    q16[f]=alpha[sum_(e,a)||ell_e^a f||²+sum_(b,a)||D_b^a f||²].

This retains every original electric term, including when a tree edge
occurs on both endpoint paths and generates a conjugation derivative.
The source paper's conventions are translated through these explicit
path/vector-field definitions rather than by copying a sign formula.

The chord sum is elliptic, while the extra sum is nonnegative. Smooth
coefficients on the compact product give a closed form with domain H1
and a self-adjoint operator with domain H2, intersected with H16.
Simultaneous conjugation reduces the form and operator. Smooth invariant
Peter-Weyl polynomials form a core. The coordinate diffeomorphism above
preserves H1 and H2 with equivalent Sobolev norms; the form identity
and closure prove J16 H16=H_E J16 on the actual operator domains.
This is not a formal coordinate expression alone.

## 4. The selected image reduces, and its exact generator

Every D_b is a constant linear combination of fields on individual chord
variables. On I3 f, fields on omitted variables annihilate the function;
the remaining coefficients never depend on those variables. Moreover
Haar integration over omitted variables commutes with retained fields
and kills their own left/right derivatives by integration by parts.
Thus the selected projection commutes on the smooth core with H16.
The same decomposition makes mixed form terms between the image and
its orthogonal complement zero: any omitted derivative integrates to
zero, and every retained derivative commutes with that integration.
Closure proves reduction of the closed form, operator and spectral
calculus. In particular, with Heff below,

    J3 D(Heff)=D(H_E) intersect ran(J3),
    H_E J3=J3 Heff,   J3* H_E=Heff J3* on D(H_E),
    exp(-t H_E/hbar)J3=J3 exp(-t Heff/hbar), t>=0.

The graph norms (||f||²+||Hf/E_star||²)^(1/2) agree exactly under J3,
and so do the closed-form norms. The domain of Heff is H2(SU2^3)∩H3;
its form domain is H1∩H3. No smoothing of arbitrary vectors is needed.

Here is the complete selected tree contribution (one row per term;
edges 4 through 11 each give zero on this selected image):

| Tree edge | D_b on U,V,W |
|---|---|
| 0 | ell_V |
| 1 | -r_V |
| 2 | ell_U |
| 3 | -r_U |
| 4,...,11 | 0 |
| 12 | -ell_V-ell_W |
| 13 | r_V+r_W |
| 14 | -ell_U-ell_V-ell_W |
| 15 | r_U+r_V+r_W |
| 26 | -r_U-r_V-r_W |

Writing K_L(S)=-sum_a(sum_(j in S)ell_j^a)^2 and analogously K_R,

    Heff/alpha=3C_U+3C_V+C_W+K_L(VW)+K_R(VW)
               +K_L(UVW)+2K_R(UVW).

This formula holds even before restricting the three-variable operator
to simultaneous-Ad invariants. Its expanded single-variable coefficients
are 6C_U+8C_V+6C_W, with cross terms

    -2[ell_U·ell_V+ell_U·ell_W+2ell_V·ell_W
        +2r_U·r_V+2r_U·r_W+3r_V·r_W].

The cross terms are real dynamics. At U=V=-i sigma_1 and W=I, xy=0
but Heff(xy)/alpha=-3/2; a diagonal-only Casimir model gives zero.
The checker obtains this from the full 33-link second derivatives as
well as from the independently constructed tree incidence form.
All displayed operators annihilate 1; any proposed additive scalar must
respect the specified ground energy and hence is zero (equal common
shifts cancel). The ground state is constant by ellipticity/connectedness.

## 5. Training and reserved predictions

Distinct-edge Casimir action on the three explicit loops gives

    Heff x=(9alpha/2)x,  Heff y=6alpha y,  Heff z=(9alpha/2)z.

Haar means are zero and each variance is 1/4. The exact spectral formulas
therefore follow on these core eigenvectors at the common physical clock.
For the declared conditional family, with kappa=0, |zeta|<1,

    A_zeta=(1+zeta x)(C_U+C_V+C_W)-zeta Gamma(x, .),
    Gamma(x,x)=(1-x²)/4,
    A_zeta x=3x/4+zeta(x²-1/4),
    A_zeta y=(3/4)(1+zeta x)y.

These follow directly by divergence/Leibniz and the normalized Casimir.
The gradient-of-mobility term is retained. Its positive closed form has
domain H1 and operator domain H2 because 1-|zeta|<=1+zeta x<=1+|zeta|.
Normalized Haar remains the constant ground state. Haar moments
E[x²]=1/4, E[x⁴]=1/8, and odd moments zero give the training slopes

    -hbar C_phys,x'(0)=9alpha/8,
    -hbar C_cond,x'(0)=3c/16.

Only these nonzero slopes are fitted: c=6alpha, with all |zeta|<1 still
possible. This differs from P1's c=4alpha for its different completion.
The first reserved datum is the training-channel curvature. Spectral
calculus gives hbar² C_f''(0)=||H f||² for these smooth vectors, so

    hbar² C_phys,x''(0)/alpha²=81/16,
    hbar² C_cond,x''(0)/alpha²=81/16+(9/4)zeta².

The reserved curvature matches only at zeta=0. For nonzero zeta the
nonnegative extra term is an exact mismatch, not a numerical tolerance.
After that restriction, the second reserved channel gives

    C_phys,y(t)=exp(-6alpha t/hbar)/4,
    C_cond,y(t)=exp(-9alpha t/(2hbar))/4.

For every finite t>0 their conditional-minus-physical difference is
positive. At t_star=hbar/alpha it equals

    [exp(-9/2)-exp(-6)]/4
      in (0.00215756109039398701827449,
          0.00215756109039398701827450).

The checker encloses exp(-1/2) by exact alternating rational sums and
uses powers nine and twelve with outward interval subtraction. Even
before using the curvature, the y initial slope is 3c/16 for every zeta,
versus physical 3alpha/2; with the fixed c=6alpha these differ by 3alpha/8.
Thus no remaining zeta can yield equality of its entire curve. Refitting
c=8alpha from y would violate the already fitted x slope. No reserved
datum is used to refit c.

For complex affine channel multiples a f+a0 and b f+b0, both means
are subtracted and the displayed centered formula is multiplied by
conjugate(a)b. Every matched physical/Heff correlation agrees exactly
by the isometry and semigroup identity; the failures above concern the
separate conditional family, not the map.

## 6. Evidence and limits

The executable controls independently reconstruct all paths and electric
incidences, use exact rational quaternion second-order jets to test every
tree-link sign on every chord, check a nonzero shared-derivative witness,
and reject identity evaluation, missing tree terms/drift, the old P1
clock, curvature-blind identification, and a held-out refit. The full
Haar, domain and spectral statements are proved above; finite fixtures
are not substitutes for them. Source notes identify targeted reading
and the direct Haar argument that supplies the L2 assertion.

The result is a finite pure-electric invariant-subspace identification
and an exact conditional-family obstruction. All physical scales, volume
and spacing remain fixed. There is no measured calibration, interacting
J2/O transfer, continuum limit or physical mass-gap conclusion. Q/R are
unselected until review. Scientific priority is unverified.
