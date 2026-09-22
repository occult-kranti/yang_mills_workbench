# Reverse I1: reconstruct a sufficient local-stability dictionary

The geometry and a qualitative theorem application pass. The exact local budget is `7|tau|`; the positive coupling threshold remains existential. This is an application of an established theorem to the declared selected-strip reference, with scientific priority unverified. No Round21 forward solution was read during this reconstruction.

## 1. Start from the desired conclusion and list what it requires

The desired claim is a positive fixed-spacing Hamiltonian gap for a nonzero **homogeneous omitted coupling**, uniform over volume at fixed positive `alpha/E_star`. A valid local-stability route needs independent onsite reference factors, a unique onsite vacuum, a uniform positive onsite gap, bounded finite-range perturbations, the source's finite boundary prescription, and an explicit mapping of the infinite limiting state. A global summability bound is neither assumed nor used.

The source is D. Yarotsky, [Quasi-particles in weak perturbations of non-interacting quantum lattice systems](https://arxiv.org/pdf/math-ph/0411042), arXiv:math-ph/0411042v1. Printed pp.2-4 state the definitions and Theorems 1-3; the downloaded PDF hash and byte count are recorded in the bound source dictionary. Full source bytes are retained outside the repository and are not needed by the arithmetic replay. `source-dictionary.json` records individual source locations and paraphrases. The displayed hypotheses and theorem statements were checked; the full cluster expansion was not independently reconstructed.

## 2. Recover independent onsite factors from tail division

For a positively oriented link `(a,i)`, set

\[
b(a)=(\lfloor a_x/4\rfloor,\lfloor a_y/2\rfloor,a_z).
\]

Euclidean division supplies unique remainder coordinates `0<=r_x<4`, `0<=r_y<2`, `r_z=0`. Therefore each link has exactly one owner, and each coarse site owns `4*2*1*3=24` outgoing links. In block zero, the selected strip consists of xy plaquettes at `(0,0,0)`, `(1,0,0)`, `(2,0,0)`. Its distinct links are six x links with `x=0,1,2`, `y=0,1`, and four y links with `x=0,1,2,3`, `y=0`: ten links entirely within the tail block. The remaining fourteen links are two separator x links, four y links on the odd row, and eight z links. Different strips have no shared links. Sharing an endpoint vertex does not spoil factorization of the unreduced link Hilbert space.

The onsite space is `K_b=L2(SU(2)^24)`. With the inherited complete-strip Hamiltonian and its actual ground energy `E_C`, define

\[
h_b={H_C-E_C+\alpha\sum_{e\in F_b}C_e\over\delta},
\qquad\delta=\alpha/8.
\]

Round19 A1/A2 supplies the unique complete-strip vacuum and gap at least `delta` for `|lambda_L|,|lambda_R|<=alpha/2`, `|mu|<=alpha/8`. Every free rotor has unique Haar vacuum and gap `3alpha/4`. A tensor sum of these nonnegative factors has a unique vacuum and gap at least `delta`, so the normalized onsite gap is at least one. Finite tensor sums of nonnegative self-adjoint operators on their natural spectral-sum domain are self-adjoint. Infinite local dimension and unbounded onsite energy are explicitly permitted on source p.2. We do not claim the gauge-invariant Hilbert space itself factors.

The checker verifies the inherited endpoint bound algebra, but does not re-prove the previously accepted strip spectral theorem from scratch. The complete-strip lower bound is `(3/4-max(|lambda_L|,|lambda_R|)/alpha)-|mu|/alpha>=1/8`; the generic bare norm bound for all three faces would instead give `-3/8` and must not replace the dressed argument.

## 3. Reconstruct all interaction supports, including crossing faces

Build a square from its four consecutive vertices and then canonicalize each edge by its positively oriented tail. For a face based at `a` in directions `i<j`, the distinct tail vertices are `a`, `a+e_i`, `a+e_j`. After ownership division every face is supported in `b+S`, where

\[
S=\{0,e_x,e_y,e_z\}.
\]

All phase classes follow from the eight anchor remainders in one `4x2x1` block. The selected faces have support `{0}`; the omitted support multiplicities are:

| Relative support | Number |
|---|---:|
| `{0,e_x}` | 1 |
| `{0,e_y}` | 3 |
| `{0,e_x,e_y}` | 1 |
| `{0,e_z}` | 10 |
| `{0,e_x,e_z}` | 2 |
| `{0,e_y,e_z}` | 4 |

There are `24-3=21` omitted anchored faces. Every one crosses a block boundary; zero omitted faces are wholly contained in one block. Three-site supports really occur. The range has coarse coordinate diameter one but coarse nearest-neighbor graph diameter two. Remainder arithmetic proves completeness for every translate; finite translated fixtures check that proof's implementation.

## 4. Normalize the actual homogeneous interaction

For `W_f=Tr(U_f)/2`, define

\[
\phi_b=-{\alpha\tau\over24\delta}
\sum_{f\in O:\ b(a_f)=b}W_f
=-{\tau\over3}\sum_{f\text{ anchored at }b}W_f.
\]

Each Wilson multiplication operator is bounded self-adjoint with norm one. Therefore `||phi_b||<=7|tau|`. For the common coefficient in the contract this bound is exact: all links equal to the identity give all 21 Wilson values equal to one, and continuity gives positive-Haar-measure neighborhoods arbitrarily near that value. Thus the essential supremum equals `21`, even though the exact identity configuration has measure zero.

The dimensionless number `epsilon=7|tau|` is derived from a local operator norm. It is not an added field, a time scale, a fitted variable, or a summability regulator. Inherited selected couplings and homogeneous omitted couplings remain those of the frozen Hamiltonian.

Source Theorem 1 supplies positive `c1(S),c2(S)` depending only on the fixed range. In particular,

\[
0<|\tau|<\tau_*:={1\over7}\min\left(c_1(S),{1\over2c_2(S)}\right)
\quad\Longrightarrow\quad
\Delta\ge\delta/2=\alpha/16.
\]

This is a nonempty **existential** interval. Neither constant has been evaluated in this loop. It certifies no chosen numerical positive value of `tau`. The physical normalization is `Delta/E_star >= (alpha/E_star)/16`; a uniform physical family needs `alpha/E_star` bounded below. No zero physical scale is admissible.

## 5. Boundaries and the positive orthant

The source Eq.(3) keeps `phi_b` only if the **whole** set `b+S` lies inside the coarse volume. This is distinct from retaining each face according to its actual support. For the domain `{0,e_x}`, the omitted xy separator face based at `(3,0,0)` has actual support `{0,e_x}` and is retained by the latter rule, while its anchor's whole star is not contained in the domain.

For a finite set of coarse sites `B`, pad to a finite `B+` containing `b+S` for every `b in B`. Set each anchor term to the subset of its omitted faces whose actual support is in `B`, and zero all other anchor terms. The same `7|tau|` bound and fixed range apply. Source Theorem 1 is uniform over these inhomogeneous families. Its padded Hamiltonian is the actual-support Hamiltonian on `B` plus decoupled reference sites, so the desired finite-volume gap inherits the source estimate. This finite-boundary proof does not itself show equality of all infinite-volume state limits.

For aligned literal vertex rectangles with side vertex counts `(4N_x,2N_y,N_z)`, all reference strips are complete. The tail-block graph adds only unused terminal outgoing links. Requiring actual plaquette support to lie inside the selected blocks is exactly the literal contained-face rule for these rectangles. The extra links are decoupled free rotors, and removing them preserves the established lower estimate. For arbitrary clipped literal boxes, use each block's retained selected components as its onsite reference; contiguous clipping gives exactly `L,M,R,LM,MR,LMR`. Round19 A1 gives the same `alpha/8` lower estimate for each. Missing graph links can be padded with free spectator rotors, and the same range and norm estimate hold. This is a separate finite-volume application, not a change to the homogeneous infinite interaction.

To apply the source's stated `Z^3` thermodynamic construction to the positive orthant, extend the **coarse** lattice to `Z^3` with independent copies of the onsite reference outside the orthant and set every outside anchor interaction to zero. Inside anchors never reach a negative coordinate, so there is no interacting cross-boundary term. A symmetric exhaustion of `Z^3` factors into the desired positive-orthant whole-star empty-boundary Hamiltonian and spectator sites. Source Theorems 2-3 then give the orthant local-state limit and gapped vacuum generator by restriction to its cyclic orthant sector. This explicitly describes the extension; it does not claim a full-integer-lattice homogeneous gauge model. The state is constructed in its own GNS representation, not presumed to belong to Round19 A2's incomplete product representation.

## 6. Discriminating controls and remaining obligations

The exact checker rejects replacing anchored faces by contained faces (`21` versus `0`), keeping only two coarse sites per face, using `3x2x1` blocks (the strip splits), dropping one omitted face in the budget, equating whole-star and actual-support boundaries, and using the failed bare three-face strip estimate. Normal and optimized Python use explicit exceptions, not removable assertions.

The supported addition is the complete selected-strip local-stability dictionary and the symbolic sufficient interval. Quantitative constant extraction, admission of any explicit nonzero numerical `tau`, unrestricted boundary-limit equivalence, weak-bare-coupling continuation, and a renormalized nontrivial four-dimensional continuum mass remain unresolved. The opposing Fibonacci arrangement is an investigation layout and enters none of these equations.

Reproduce from the repository root:

```bash
python -B research/round21/reverse/i1/check.py --output /tmp/ym21-reverse-i1
python -B -O research/round21/reverse/i1/check.py --output /tmp/ym21-reverse-i1-optimized
```

Both runs produce source-bound `results.json` and `source-manifest.json`. Repeated runs count as one executed research loop, not independent physical evidence.
