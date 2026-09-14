# Q1 forward: full magnetic action leaks out of the selected electric image

For the complete twenty-face action, the selected conditional mean is
20-b and its conditional variance is the nonconstant function
K=19/4+(r+x+z)/2, where b=Tr(VW^-1)/2 and r=Tr(UW^-1)/2.
Three correlated faces contribute the cross terms. Exactly 4<=K<=25/4.
Thus every positive magnetic coupling breaks the selected reduction;
the full sixteen-chord unitary equivalence survives. The compressed
evolution differs from its autonomous compression first at second order
on the invariant smooth core, with a separately justified quadratic
operator-norm upper bound. Current opposing Q1 evidence was not read.

## 1. Full action in the actual tree coordinates

Use the admitted P2 unitary J16:H16->Hphys and selected isometry
J=J16 I3:H3->Hphys. H3 consists of simultaneous-Ad invariant functions
of U=L28,V=L27,W=L24 with normalized Haar. P=JJ*, Q=1-P; J* integrates
the other thirteen chords after the full unitary change of variables.
The fixed tree is edges 0,...,15,26, rooted at (0,2,0).

Writing A_e=L_e for omitted chord variables, the full signed face words
after true tree gauge fixing are listed below. Each entry means its
normalized fundamental trace. This follows by substituting
g_e=h_s^-1 L_e h_t and cancelling successive tree transports around
the face, leaving a conjugation at its base, invisible to the trace.
No unused chord is evaluated at identity.

| Face ID | Chord word |
|---|---|
| 0 | A16 |
| 1 | A17 |
| 2 | A18 |
| 3 | A19 |
| 4 | A20 A16^-1 |
| 5 | A21 A17^-1 |
| 6 | A22 A18^-1 |
| 7 | A23 A19^-1 |
| 8 | V W^-1 |
| 9 | U A25^-1 |
| 10 | A29 |
| 11 | A30 V^-1 |
| 12 | A31 U^-1 |
| 13 | A32 A29^-1 |
| 14 | A25 W^-1 |
| 15 | A25^-1 |
| 16 | A16 U A17^-1 V^-1 |
| 17 | A18 A29 A19^-1 U^-1 |
| 18 | A20 A31 A21^-1 A30^-1 |
| 19 | A22 A32 A23^-1 A31^-1 |

The checker reconstructs the entire 18-vertex/33-edge/20-face graph and
compares the original signed words to the admitted C1 ledger. It also
tests these transported traces on a noncommuting full-link fixture,
including all root paths. Let S=sum_p W_p and Vmag=20-S; Vmag is the
operator denoted V in the contract. Each W_p lies in [-1,1], so
0<=Vmag<=40. Both endpoints are attained: all identity links give zero;
the central assignment g_x=I, g_y=(-1)^x I, g_z=(-1)^(x+y) I gives
every plaquette -I and Vmag=40. Consequently ||Vmag||=40.

## 2. Exact conditional moments, including shared faces

Let E3 be Haar conditional expectation given U,V,W, and set
x=Tr U/2, z=Tr W/2, b=Tr(VW^-1)/2, r=Tr(UW^-1)/2.
Only face 8 is independent of omitted variables. Every other word
contains at least one omitted chord exactly once, giving mean zero by
Haar integration. Hence E3 S=b and

    m := E3 Vmag = 20-b.

For p!=8, integrating one such chord gives E3(W_p²)=1/4: its product
with fixed surrounding group elements is Haar, and a normalized SU2
fundamental trace has Haar squared norm 1/4. Face 8 contributes b².
For two distinct faces, an omitted chord appearing in exactly one word
makes the product expectation zero under the Haar symmetry A->-A.
The complete support ledger leaves only pairs (9,14), (9,15), (14,15).
These all share omitted A25. In unit quaternion coordinates u,w,a,
their three traces are u·a, a·w, a0. Since E[a_i a_j]=delta_ij/4,

    E3(W9 W14)=r/4,  E3(W9 W15)=x/4,  E3(W14 W15)=z/4.

This argument counts every one of the 190 distinct-face pairs; finite
quaternion tests accompany the general contraction identity. Therefore

    E3 S²=b²+19/4+(r+x+z)/2,
    E3 Vmag²=(20-b)²+19/4+(r+x+z)/2,
    K := E3 Vmag²-(E3 Vmag)²=19/4+(r+x+z)/2.

In particular, the variance is not the independent-face value 19/4.
At U=W=I it is 25/4. Treating the old static section as an expectation
would also be wrong: at U=V=W=I that section has action zero, whereas
the actual conditional mean is 19.

There is a useful exact positivity identity, with e0=(1,0,0,0):

    K=4+|u+w+e0|²/4.

Unit lengths give 4<=K<=25/4. The upper endpoint occurs at u=w=e0.
For the lower endpoint choose u=(-1/2,sqrt(3)/2,0,0) and
w=(-1/2,-sqrt(3)/2,0,0), so u+w+e0=0. These sharp essential bounds
also hold in the simultaneous-Ad sector: K is invariant and continuous,
and invariant functions supported near either extremal level supply
the corresponding spectral endpoint. They are bounds on a multiplication
operator, not just on a Haar mean. Its Haar expectation is instead
E K=19/4, since E x=E z=E r=0.

## 3. Self-adjoint magnetic deformation and the leakage operator

At fixed positive alpha/E_star, hbar and spacing, and fixed finite graph,
let H_lambda=H_E+alpha lambda Vmag, lambda>=0. The multiplier is bounded,
real, smooth and gauge invariant. Bounded perturbation preserves the
self-adjoint operator domain D(H_E)=H2(SU2^33)∩Hphys; its closed form
domain is the corresponding H1 intersection. Positivity follows from
H_E>=0 and Vmag>=0. The invariant smooth/Peter-Weyl core remains a core,
and is stable under the multiplier and these differential expressions.
Transport by the full unitary is exact:

    J16* H_lambda J16=H16+alpha lambda Vmag(L).

Here H16 is the full P2 electric operator with all tree/cross derivatives.
This full equivalence does not imply selected-image reduction.

P2 proves P reduces H_E and preserves its form and operator domains.
Consequently the selected compression is the self-adjoint operator

    A_lambda=J* H_lambda J=H_eff+alpha lambda m,
    D(A_lambda)=H2(SU2^3)∩H3, form domain H1∩H3.

In particular A_lambda>=19alpha lambda. The off-diagonal operator,
initially computed on the core, extends boundedly to

    B_lambda=Q H_lambda J=alpha lambda Q Vmag J,
    B_lambda* B_lambda=(alpha lambda)² M_K,
    J* Vmag Q Vmag J=M_K.

Here M_K is multiplication by the exact conditional variance, because
J*Vmag P Vmag J=M_m². Thus

    4I <= M_K <= (25/4)I,
    ||B_lambda||=5alpha lambda/2,
    ||B_lambda f|| >= 2alpha lambda ||f||.

For every lambda>0 the image is not invariant, indeed every nonzero
selected vector leaks under the bounded magnetic part. This does not
reject other reductions. At lambda=0, B=0 and the exact P2 electric
intertwining and selected semigroup are recovered.

The normalized reference Omega=1 is the electric vacuum and Haar vector,
not an interacting ground. E Vmag=20 and E Vmag²=405, giving
Var(Vmag)=5. Since H_lambda Omega=alpha lambda Vmag, this vector is not
an eigenvector for lambda>0. No scalar shift changes that variance or
the off-diagonal block. In particular the matrix elements below are
Haar-reference compressed evolutions, not asserted stationary interacting
ground correlations.

## 4. Core discrepancy and a separate global norm bound

Define T_lambda(t)=J* exp(-t H_lambda/hbar)J, t>=0. For every invariant
smooth selected f, Jf and f belong to the squares of the relevant
operator domains: the smooth multiplier and elliptic operators preserve
the smooth core. Spectral calculus therefore yields the strong-vector
Taylor expansions and the exact core identity

    J* H_lambda² J f-A_lambda² f=(alpha lambda)² K f.

The zeroth and first coefficients agree, and the first discrepancy is

    [T_lambda(t)-exp(-t A_lambda/hbar)]f
      = (alpha lambda t/hbar)² Kf/2 + o_f(t²).

This is a strong expansion for each such f, not an operator-norm Taylor
claim. It has a strictly positive leading quadratic form for lambda>0.
For the explicit smooth invariant f=1,

    <1,[T_lambda(t)-exp(-t A_lambda/hbar)]1>
      = (19/8)(alpha lambda t/hbar)²+o(t²).

Thus the autonomous compression fails even on this channel. Any
self-adjoint autonomous semigroup agreeing with T would have the same
generator on this core, hence its self-adjoint closure A_lambda, already
excluded by the second coefficient.

For a norm estimate, first justify the complementary diagonal block.
On QHphys let

    C_lambda=H_E|_Q+alpha lambda QVmag Q,
    D(C_lambda)=QD(H_E), form domain QD(H_E^(1/2)).

These are self-adjoint/nonnegative by electric reduction and bounded
positive compression. The block-diagonal D_lambda=J A_lambda J* ⊕ C_lambda
has the common domain D(H_E), is nonnegative, and
H_lambda=D_lambda+W_lambda, where W_lambda has blocks B_lambda and B_lambda*
and zero diagonal. It is bounded with norm 5alpha lambda/2.
All H_lambda and D_lambda semigroups are contractions.

Duhamel follows first by differentiating the relative product on the
common operator domain and then extending the bounded perturbation
integral to all vectors. Substituting it once more, its first-order term
vanishes between P's. With B=B_lambda, A=A_lambda, H=H_lambda, the exact
second-order integral is

    T_lambda(t)-exp(-t A/hbar)
      = hbar^-2 integral_(0<=u<=s<=t)
        exp(-(t-s)A/hbar) B*
        [Q exp(-(s-u)H/hbar) Q] B exp(-uA/hbar) du ds.

The integrals exist as strongly continuous vector-valued integrals;
operator-norm continuity or an operator-norm Bochner integral is not
asserted. Bounding each integrand on vectors by ||B||² and integrating
over the triangle proves, for all t>=0,

    ||T_lambda(t)-exp(-t A_lambda/hbar)||
      <= (25/8)(alpha lambda t/hbar)².

This norm upper bound and the core lower-order coefficient are distinct
results. No operator positivity of the whole time-dependent difference
is inferred from the noncommuting integral. If both generators are
shifted by a common scalar c, the difference is multiplied by
exp(-ct/hbar); K, leakage and the second-order coefficient are unchanged.
The norm bound receives that same factor. A scalar cannot repair closure.

## 5. Scope and evidence

The checker implements an independent signed graph/chord reconstruction,
all pair-support exclusions, the exact quaternion contraction matrix,
correlated-face controls, sharp variance endpoints, Haar-reference
variance, lambda=0 recovery and a finite block identity checking the
second-order/scalar signs. The block fixture is an algebra control, not
the physical dynamics or proof of an infinite-dimensional statement.
The operator/domain arguments above provide those statements. All
contract dependencies and six frozen v4 instruction inputs are bound.

Source notes report actual targeted reading. The nearest checked result
is the admitted P2 pure-electric reduction and the primary tree-transport
identity; the magnetic conditional moments and this selected leakage
are derived for the full actual graph. No interacting ground, homogeneous
stability, physical calibration or continuum theorem follows. Q2 is not
selected or executed. Scientific priority remains unverified.
