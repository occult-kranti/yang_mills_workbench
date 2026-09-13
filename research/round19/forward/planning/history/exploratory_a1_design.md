# Round19 forward A1 proposal: clipped restrictions of one infinite strip assignment

This is a bounded forward design, not a completed gate. It audits the Round18 A result and proposes the next Goal A1: replace the complete-strip-only finite scheduling rule by literal restrictions of one infinite coefficient assignment. The Hamiltonian is always the full-link Hamiltonian first; a Gauss-sector conclusion would only follow after a positive full-space bound and the usual uniqueness/invariance argument.

## Audit finding from Round18 A

Round18 A1 proved a finite three-square strip estimate in the full untruncated link Hilbert space. Its useful mechanism was the conditional Haar zero for the bridge in the dressed end-block reference, giving the primary three-face bound

\[
\Delta_{LMR}\ge \alpha\left(\frac34-\max(|\lambda_L|,|\lambda_R|)/\alpha\right)-|\mu|.
\]

For \(|\lambda_L|,|\lambda_R|\le \alpha/2\) and \(|\mu|\le \alpha/8\), this gives \(\Delta_{LMR}\ge \alpha/8\).

Round18 A2 built a finite-volume inhomogeneous summable family from complete strips plus a decaying remainder. It explicitly did **not** give literal finite restrictions of one infinite assignment: the face old `f2:4,0,0` has remainder coefficient in \(B_6\) but cluster coefficient in \(B_8\). That coefficient jump is the next A1 target.

## One infinite assignment

Work on the positive-orthant infinite cubic lattice and restrict to open boxes \(B_n=\{0,\ldots,n-1\}^3\). Every finite box keeps every actual link electric term

\[
H_E(B_n)=\alpha\sum_{e\subset B_n} C_e,\qquad \alpha\ge \alpha_{\min}>0.
\]

For every xy face at base \((x,y,z)\), assign a strip role when

\[
y\equiv0\pmod2,\qquad x\equiv0,1,2\pmod4.
\]

The roles are

| role | x residue | coefficient bound |
|---|---:|---:|
| L | 0 | \(|c_L|\le\alpha/2\) |
| M | 1 | \(|c_M|\le\alpha/8\) |
| R | 2 | \(|c_R|\le\alpha/2\) |

The sign is part of the infinite assignment and is not allowed to change with the volume. All other faces may later receive the same dyadic summable remainder as Round18, but the local clipped-cluster question already has to pass before that extension matters.

This removes the Round18 boundary reclassification: if face \((0,1,4,0,0)\) exists in both \(B_6\) and \(B_8\), it is role L in both restrictions.

## Actual clipped boundary types

For the canonical boxes starting at the origin, nonempty restrictions of an infinite three-face strip are prefixes:

| type | when it occurs at the terminal x boundary | local support | proposed lower bound |
|---|---|---:|---:|
| L | \(n\equiv2\pmod4\) | one actual plaquette | \(\alpha(3/4-1/2)=\alpha/4\) |
| LM | \(n\equiv3\pmod4\) | two adjacent plaquettes | \(\alpha(3/4-5/8)=\alpha/8\) |
| LMR | full interior strip | three adjacent plaquettes | Round18 A1 gives \(\alpha/8\) |

There is no y-clipped xy strip in this box convention, because an xy face with lower y exists only when the y-link completing that face is present. There is no z-clipped xy strip, because the strip lies in a fixed z plane. Non-xy faces, odd-y xy faces and x-separator faces remain outside the strip seed and require a free-link witness if a remainder is added.

For translated finite windows, the same local theorem also covers the suffixes R and MR. The exact local set is therefore the six nonempty contiguous subsets of LMR:

\[
L,
M,
R,
LM,
MR,
LMR.
\]

The non-contiguous LR pattern is not a clipped restriction of a contiguous three-face strip and must be rejected.

## Signed cases and formulas

For any proper clipped subset \(S\ne\{L,M,R\}\), compare with the bare free-link Hamiltonian on the actual links in that clipped support. The constant vacuum is unique, the first full-link excitation costs \(3\alpha/4\), and each Wilson face multiplier has zero Haar-vacuum mean. With

\[
B(S)=\sum_{t\in S}|c_t|/\alpha,
\]

min-max and the vacuum trial give

\[
\Delta_S\ge \alpha\left(\frac34-B(S)\right).
\]

The worst proper clipped case is an end-plus-bridge pair, \(B=1/2+1/8=5/8\), so all proper signed clipped restrictions have \(\Delta_S\ge\alpha/8\). This is independent of signs; zero coefficients are valid signed cases and only improve this local estimate.

For the complete LMR strip, reuse the accepted Round18 A1 mechanism, because the bare norm budget can be \(9/8\). The complete-strip formula is

\[
\Delta_{LMR}\ge \alpha\left(\frac34-\max(|c_L|,|c_R|)/\alpha\right)-|c_M|\ge \alpha/8.
\]

A finite restriction can then take the tensor sum of all disjoint clipped clusters. The reference gap remains at least \(\alpha/8\) because the cluster supports are link-disjoint and free links have gap \(3\alpha/4\). This is still a finite full-space statement; limiting states, limiting dynamics and a spectral gap in the resulting representation remain open.

## Proposed exact checker

`clipped_restrictions.py` is an exact-arithmetic scientific checker for this proposal. It does four things:

1. enumerates all six contiguous clipped types and all \(-,0,+\) signed endpoint cases;
2. checks the proper-clipped formula and the Round18 complete-strip formula against the \(\alpha/8\) local target;
3. materializes canonical boxes \(2\le n\le12\), classifies L, LM and LMR terminal cases, and verifies that every non-strip face still has an actual free Haar witness edge;
4. records the Round18 coefficient-jump witness and rejects non-contiguous LR as a false clipped type.

The script deliberately does not compute a finite representation spectrum. Its evidence is about exact support geometry, coefficient consistency, Haar-vacuum premises and full-link operator inequalities.

## Candidate next gate, still unclaimed

If the advisor freezes this as the A1 contract, the first loop should require an independent reconstruction of the same signed clipped inventory and formulas. Only after that should we add the dyadic remainder back in. Under the same remainder premise as Round18 with \(|\tau|=1/64\), the proposed formal bound would be

\[
\Delta(B_n)\ge \alpha\left(\frac18-\frac1{64}\right)=\frac{7\alpha}{64},
\]

and therefore \(7\alpha_{\min}/64\) in one common physical scale. That second step still needs the free-link witness gate for the new selected-support rule, plus independent review. It does not close the dense homogeneous goal or any infinite-volume/continuum obligation.
