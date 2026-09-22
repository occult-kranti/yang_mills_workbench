# I1 forward: a complete strip-cell stability dictionary

Status: frozen forward derivation, before comparison with the reverse researcher. The current reverse files were not read. The arithmetic below verifies the frozen formulas and their phase fixtures; the infinite geometry argument is given explicitly and does not follow from finite enumeration.

## 1. Fixed model and equations frozen before execution

The link space is the full, untruncated product of normalized Haar spaces `L²(SU(2))`. The physical energy reference satisfies `E_star>0`, `alpha>0`, and `alpha/E_star` is fixed. Spatial spacing is fixed. Set `delta=alpha/8`. The selected xy faces have even y and x residues 0,1,2 modulo 4, with the inherited endpoint and bridge bounds. Every other elementary face has the same nonzero coefficient `nu=alpha*tau/24`. The dimensionless `tau` is the actual omitted interaction coefficient relative to alpha; the norm `epsilon` below is a derived bound. No extra physical coefficient is introduced.

For `b=(i,j,k)` in the positive coarse orthant, define

\[
T_b=\{(4i+r,2j+s,k):0\le r<4,\ 0\le s<2\},
\quad \pi(x,y,z)=(\lfloor x/4\rfloor,\lfloor y/2\rfloor,z).
\tag{I1.1}
\]

The block owns all three positively oriented links whose tail belongs to `T_b`, irrespective of the endpoint's block. The frozen conclusions to check are

\[
24=10+14,\qquad 24-3=21,\qquad
S=\{0,e_x,e_y,e_z\},\qquad
\epsilon=\sup_b\|\phi_b\|=7|\tau|.
\tag{I1.2}
\]

Equality in the last equation is for the homogeneous omitted coupling on a complete anchor block. Its upper bound remains valid after clipping or deleting faces.

## 2. Complete ownership and reference factors

Euclidean division gives unique `i,r` with `x=4i+r`, `r=0,1,2,3`, and unique `j,s` with `y=2j+s`, `s=0,1`. The z tail coordinate is itself k. Hence every positive link belongs to one and only one block. This proves ownership for the entire orthant.

The selected strip at `(4i,2j,k)` consists of the three xy faces with x offsets 0,1,2. Its x links have tails `(r,s)`, `r=0,1,2`, `s=0,1`, giving six links; its y links have tails `(r,0)`, `r=0,1,2,3`, giving four. These ten tails all belong to `T_b`. Conversely every selected face belongs to exactly this strip. Consequently no reference strip is split between sites, and two strips cannot share a link.

The fourteen remaining links in a block are two x separator links at `r=3`, four y links at `s=1`, and eight z links. Their endpoints may cross the block boundary; this does not change ownership or their being individual free-link reference factors.

Using the inherited complete-strip gap, define the onsite operator

\[
h_b={H_{\mathrm{strip},b}-E_{\mathrm{strip},b}
             +\alpha\sum_{e\in F_b}C_e\over\delta}.
\tag{I1.3}
\]

The strip ground state is unique with gap at least delta. Each free Casimir has unique Haar vacuum and gap `3alpha/4=6delta`. Tensor addition gives a unique onsite vacuum, nonnegative self-adjoint `h_b`, and `h_b >= I-P_b`. The Hilbert space is infinite dimensional and the onsite operator is unbounded; both are admitted by the source theorem. This step inherits, rather than re-proves, the local strip estimate in [A1](../../../round19/forward/a1/report.md) and the reference construction in [A2](../../../round19/forward/a2/report.md).

## 3. Every face support, including crossing faces

For an elementary face at p in directions `a<c`, the four positive link tails are `p,p+e_a,p+e_c,p`. Thus its coarse support is precisely

\[
\operatorname{supp}_B(f)=\{\pi(p),\pi(p+e_a),\pi(p+e_c)\}.
\tag{I1.4}
\]

There is no tail at `p+e_a+e_c`; inserting that vertex as a link owner would use the wrong geometry. Increasing x by one crosses a coarse boundary exactly at `r=3`; increasing y crosses exactly at `s=1`; increasing z always crosses. These three facts exhaust every translation and phase, including arbitrarily large coordinates. The table derives all 24 anchored face classes:

| Orientation and phase | Count | Relative support | Role |
|---|---:|---|---|
| xy: r=0,1,2; s=0 | 3 | `{0}` | selected |
| xy: r=0,1,2; s=1 | 3 | `{0,e_y}` | omitted |
| xy: r=3; s=0 | 1 | `{0,e_x}` | omitted |
| xy: r=3; s=1 | 1 | `{0,e_x,e_y}` | omitted |
| xz: r=0,1,2; s=0,1 | 6 | `{0,e_z}` | omitted |
| xz: r=3; s=0,1 | 2 | `{0,e_x,e_z}` | omitted |
| yz: r=0,1,2,3; s=0 | 4 | `{0,e_z}` | omitted |
| yz: r=0,1,2,3; s=1 | 4 | `{0,e_y,e_z}` | omitted |

Each face support has at most three blocks. Their union for a whole anchor group is the four-site star S. Its coarse l-infinity diameter is 1 and l-one diameter is 2. The support does not require the full eight-corner cube. All 21 omitted faces cross a block boundary. Counting only faces contained in one block therefore gives zero and discards the entire homogeneous perturbation.

## 4. Exact local budget; the global sum is a different quantity

Group the omitted faces by their anchor block, each face once:

\[
\phi_b=-{\nu\over\delta}\sum_{f:\pi(\operatorname{base}f)=b,\ f\notin\mathrm{selected}}W_f
       =-{\tau\over3}\sum_{f\in O_b}W_f,\qquad
W_f=\tfrac12\operatorname{Tr}(U_f).
\tag{I1.5}
\]

The normalized SU(2) trace is real and bounded by one. There are 21 summands, so `||phi_b||<=7|tau|`. At the identity configuration all 21 Wilson traces equal one. Continuity and full support of finite-product Haar measure imply that the essential supremum attains the same limit, giving equality. This is an operator norm statement on the full local link Hilbert space; it is not an expectation in the reference vacuum.

For N complete anchor blocks, the absolute interaction budget is `7N|tau|`. It diverges with N when tau is nonzero. A2's globally bounded summable perturbation argument cannot apply to this homogeneous interaction. The source local-stability theorem uses the supremum over anchor groups instead. This distinction preserves the homogeneous target rather than replacing it with a decaying profile.

## 5. Exact theorem dictionary and available conclusion

The inspected primary source is [Yarotsky, arXiv:math-ph/0411042v1, November 11, 2004, definitions and Theorems 1–3, pp. 2–4](https://arxiv.org/pdf/math-ph/0411042); Section 2's expansion discussion was also read. The source states the stability theorems and refers to preceding works for complete proofs. It does not evaluate its range-dependent constants in the inspected statements. This work checks applicability; it does not re-prove the cluster expansion.

| Source premise | This model | Status |
|---|---|---|
| Sites in an integer lattice | Coarse index b; explicit orthant embedding below | Matched |
| Arbitrary, possibly infinite-dimensional site space | 24 link Haar factors | Matched |
| Nonnegative self-adjoint onsite operator | Shifted strip plus free Casimirs, divided by delta | Matched using inherited strip theorem |
| Unique onsite vacuum and gap at least one | Equation I1.3 | Matched |
| Bounded self-adjoint interaction on one fixed finite translate | Real Wilson multiplication, support `b+S` | Matched |
| Small supremum of interaction norms | `epsilon=7|tau|` | Exact formula, qualitative smallness only |
| Empty boundary defined by the full translate | Equation I1.6 below | Matched explicitly |
| Numerical constants `c1(S),c2(S)` | Existential in checked source | Unevaluated |

For the theorem's constants, the sufficient symbolic regime is

\[
0<|\tau|<\tau_*:={1\over7}\min\{c_1(S),[2c_2(S)]^{-1}\}.
\]

Then the source spectral estimate, restored to physical units, gives

\[
\Delta/E_\star\ \ge\ {\alpha\over8E_\star}
       (1-7c_2(S)|\tau|)\ >\ {\alpha\over16E_\star}>0.
\]

These formulas specify an existential nonzero interval. They do not certify any numerical tau, including tau=1/64. `1/7` and `alpha/16` are evaluated arithmetic factors, not evaluated stability constants. No fitted constant can close this missing premise.

## 6. Boundaries and the positive orthant

For a finite set B of coarse blocks, the source empty-boundary Hamiltonian is

\[
\widehat H_B=\sum_{b\in B}h_b+
       \sum_{b:b+S\subseteq B}\phi_b.
\tag{I1.6}
\]

It includes all outgoing links owned by B, even if their heads are outside B. The anchor group is dropped unless the entire four-site star is present. Thus it can drop a face whose actual two- or three-site support is contained in B. For instance `B={0,e_z}` contains ten actual omitted faces anchored at 0, but contains no whole S translate and therefore retains none in Equation I1.6.

An all-actual-support-contained block prescription has the same qualitative finite-volume bound by padding. For each b in B let `phi_b^(B)` retain only faces whose actual support is contained in B, put all other anchor groups to zero, and take `B_plus = union_{b in B}(b+S)`. Each retained group is now admitted by the source empty boundary on `B_plus`; its norm is at most `7|tau|`. All padded reference sites decouple, so their tensor sum with the desired B Hamiltonian has gap equal to the minimum of the desired gap and the padded onsite gaps. The theorem bound is at most one in normalized units, so it bounds the desired gap as well. This legitimately uses a different admissible perturbation family for each finite B, with uniform range and norm.

To use a source stated on `Z³` for the actual positive orthant, extend the site family to negative coarse sites with arbitrary copies of a gapped reference site and set every interaction anchored outside the positive orthant to zero. Because S has only nonnegative offsets, no retained interaction meets the negative-site system. Exhaust symmetric coarse cubes in this decoupled extended model. Their ground states factor into the positive-orthant source boundary model and negative dummy vacua. The source local-state limit therefore restricts to an orthant limit. The orthant cyclic subspace is reducing for the limiting generator, so its gap bound is inherited. This construction does not claim a translation-invariant homogeneous extension across the coordinate planes, and it does not identify the homogeneous ground-state representation with A2's incomplete tensor product.

## 7. Literal vertex boxes: finite-gap transfer with a distinct state-limit obligation

A literal rectangular vertex box retains a link only when both endpoints are present. Even an aligned box generally differs from a full tail-block box: some outgoing links are absent, and links on a top vertex face can lie in an additional partially populated tail block. Padding full tail blocks with unchanged h_b does not by itself establish equality with this literal graph.

There is nevertheless a finite-volume transfer using the inherited clipped-component theorem. For each literal vertex box V, give site b precisely the retained links whose tails lie in `T_b`. Each retained selected strip component still belongs to one site. Intersection with a rectangular x interval leaves one of `L,M,R,LM,MR,LMR`, or no face; y and z intersections either keep the selected face row/layer or remove it. Every remaining link is free relative to this selected reference. By A1, each nonempty component has gap at least delta and a unique ground state. Their tensor sum supplies an admissible volume-dependent onsite `h_b^(V)`; empty sites may be one-dimensional.

Retain every literal omitted face once at its tail anchor. Its coarse support remains inside `b+S`, and at most 21 such faces occur at one anchor. Apply the padding construction to these site spaces and these clipped face groups. The constants depend on S, not on site dimensions or the number of sites, so this gives the same existential finite-volume gap bound for literal rectangular boxes and every lower/upper phase, using A1 as a premise. The code verifies representative clipped graphs and exact support preservation; the rectangular-intersection argument supplies general completeness.

This finite-volume transfer does not prove that every literal-box thermodynamic state limit equals the source-boundary orthant state. For that claim one needs boundary-independence estimates for the homogeneous local interaction. The summable E2 argument cannot simply be copied because its absolute tail no longer tends to zero.

## 8. Checks, contribution and remaining target

The standard-library checker derives link ownership, phase support classes and rational normalization, and materializes shifted literal boxes. Wrong-model controls distinguish split-strip blocking, missing crossing faces, diagonal-corner ownership, wrong energy normalization, incorrect source boundary retention and a claimed uniform global norm. The output binds the frozen contract, this report, code and inherited premises by SHA-256; no cache or generated environment file is admitted.

Reproduce from the repository root:

```bash
python -B research/round21/forward/i1/check.py --output research/round21/forward/i1/replay-output
```

The new project contribution is an exact, complete selected-strip blocking dictionary and its boundary-aware theorem application, including the sharp anchor norm. Scientific priority is unverified. The stability theorem and tensor/padding arguments are established tools applied here. The numerical coupling interval, equality of alternative homogeneous thermodynamic boundary limits, matched continuum limit and continuum Yang–Mills mass gap remain unresolved. I2 has not been executed or chosen by this researcher.
