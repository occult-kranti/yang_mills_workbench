# AH1 pre-contract mathematical review

Planning review only. I read the Penrose AH1 proposal against the inherited
AC1/AC2/X1/X2/Z2/AF2 passages identified below. No new graph enumeration,
AH1 checker, physical calculation or contract was executed. AH2 and later
goals remain unselected; the root agent remains advisor.

Proposal inspected: `research/round28/experts/penrose/ah1-contract-proposal.md`,
SHA-256 `4ab8d06705775d1f2dc80947d9cdaa333ff76deffdfc70129dae3941c9c48ea5`.

**No blocking mathematical flaw was found in the proposed model or heat
template. Before freezing, make the two projector estimates explicit, give an
unambiguous definition of the individually resolved enrichment, and retain the
strict-cutoff and coordinate-center-sign proof obligations.**

## 1. Strict electric cutoff

The proposed `P0=1_[0,9/2)(K)` is consistent with the inherited physical
argument, but the new graph's conclusion must be proved rather than obtained
by changing 21 to 30. The complete proof should retain these steps:

1. Gauge invariance forbids a degree-one vertex in a nonempty active-edge
   support. Each active edge costs at least 3/4. Below 9/2 there are at most five
   active edges.
2. The new graph is simple, bipartite and has girth four. There is no
   five-edge minimum-degree-two bipartite support. Thus the support must be a
   four-cycle; prove every four-cycle is one listed elementary face.
3. At the degree-two vertices of that cycle the invariant intertwiner forces
   equal edge spins. The strict energy bound selects spin 1/2. Its invariant
   intertwiner is unique. Orthogonality and normalized Haar measure then
   identify the vacuum and face characters, with the proposed rank still to
   be verified on the new face list.

The endpoint must remain strict. Six-fundamental-edge channels at energy 9/2,
including the shared-edge singlet products, belong outside P0. They may enter
P+ subsequently. Changing `<9/2` to `<=9/2` would change the initial space and
the Ritz/residual problem. The old reverse X1 twice-spin degree cutoff is a
different cutoff definition, even though its smallest space agrees with the
old strict electric cutoff.

Sources: `research/round24/skeptic/x1-review.md:18-26` gives the complete
small-support exclusion and distinguishes the cutoff definitions;
`research/round24/forward/x1/report.md:41-64` gives physical projections,
domains and compactness; `research/round24/forward/x2/report.md:42-51` states
the admitted low-energy identification, and its lines 110-124 identify the
9/2 and 13/2 shared-edge channels. No new cutoff enumeration was done here.

## 2. Resolve individual channels before taking K reduction

Freeze the candidate functions, unordered pair convention, oriented face words
and shared-edge projection explicitly. The intended construction is the span
of P0 and the K spectral components of each individually named face-product
channel. It is not merely the K-cyclic span of the summed columns
`(I-P0)S phi_p`. K separates electric eigenvalues but cannot separate arbitrary
different vectors within one degenerate electric eigenspace. Replacing the
individual list by summed-column Krylov closure can therefore give a strictly
smaller space.

For edge-disjoint pairs, including pairs meeting only at a vertex, the actual
product is a K eigenvector. That does not require every ambient intertwiner at
its energy. For a common edge, both its Haar spin-zero projection and the
orthogonal spin-one remainder are required. First verify that distinct new
elementary faces share at most one edge. Same-face products retain their scalar
and spin-one character. Ordered duplicate descriptions must either be removed
by a frozen convention or included as exact Gram-null relations.

The proposal appropriately requires the full candidate Gram and quotient. If
null vectors occur, require K and the magnetic coordinate action to preserve
the Gram kernel, then realize the physical quotient. Ordinary transposition or
inversion of a singular candidate Gram cannot replace this step. On an
independent quotient basis, metric self-adjointness determines reverse entries;
the unnormalized triplet weight must remain. The old diagonal Gram and 293-state
rank are comparison data, not new assumptions.

Sources: `research/round26/forward/ac1/report.md`, sections “Actual vectors,
Gram and electric completeness” and “The entire retained matrix is exact”;
`research/round24/forward/x2/report.md:102-124` for the actual channel norms
and electric energies; `research/round26/forward/ac1/check.py:30-55` for the
old candidate labels, pair incidence and metric-weighted matrix convention.

## 3. Center parity is structural, but needs the actual transformation

Specify the central link signs as `+1` on x-directed links, `(-1)^x` on
y-directed links, and `(-1)^(x+y)` on z-directed links, using the integer tail
coordinates and frozen orientations. Verify every new face receives product
sign −1. This is one global assignment of individual central link signs; it is
not simultaneous sign reversal of every link, which would leave a four-edge
face unchanged.

The transformation preserves Haar measure and physical gauge invariance and
commutes with K. Consequently S is odd, original fundamental faces are odd,
and the vacuum and quadratic generated channels are even. Those facts justify
the within-parity retained magnetic zeros after quotienting. They do not by
themselves prove distinct pair masks: four-face relations are even under this
global sign. Pair-mask collisions still need the proposed separate check, and
equal-parity vectors need their actual Haar/representation orthogonality.

Sources: `research/round24/forward/x2/report.md:81-108` gives both the separate
mask tests and the explicit coordinate assignment;
`research/round26/forward/ac1/report.md:25-38` uses it to reconstruct every
retained magnetic entry. The new graph's parity tests remain unexecuted.

## 4. The heat template is valid with two explicit p0 bounds

Before using residuals, prove compactness and min-max isolation for the full
operator and both compressions: second eigenvalues at least 3 and
`0<=epsilon<=mu+<=mu0<=29 lambda<3`. This follows from the proposed positive
interaction only for nonnegative lambda. An actual low Ritz residual alone
does not identify a ground eigenvalue.

The complete residual of f0 must establish **both**

```
||G-G0||<=p0,       ||G+-G0||<=p0.
```

The first uses the full spectral measure. The second uses f0's residual inside
A+. Indeed the individually resolved closure implies `B P0=0`, hence
`L f0 in ran P+` and `(A+-mu0)f0=(L-mu0)f0`. The same residual/gap estimate
therefore applies to the nested compression. With `B f0=0`, this yields

```
||B f+||=||B(I-G0)f+||<=29 Lambda p0.
```

This is the missing explicit implication needed for the proposed r+ envelope.
Use bars or a clear declaration that p0,r+,p+,d+ are uniform upper envelopes,
not evaluated actual norms. The full residual of f+ then gives both
`||G-G+||<=p+` and `0<=mu+-epsilon<=d+` by the same spectral/Temple argument.

With these two p0 bounds the proposed denominator is valid:
`||E(sigma)x||>=||Gx||>=z-eta-p0`, where eta=1/100. Both full and retained
excited components of x are bounded by `b=q0+p0+eta`. This argument works for
complex normalized x without replacing the full-output denominator by a Ritz
norm. The constants z and q0 must be uniform for the newly derived f0.

Strong Duhamel has the defect `B+(mu+-epsilon)P+`, with the displayed plus
sign. Decomposing the retained evolution into its ground and excited pieces
gives the proposed early V. The full and retained spectral decompositions give
the proposed late J; its extra `p+ exp(-g sigma)` is harmless slack when the
two p0 estimates already bound both excited components by b. With D>0, V
increasing and J decreasing, the fixed join yields `max(V(T),J(T))/D`.
Neither `B P0=0` nor zero initial leakage makes P0 autonomous, and the own-ground
centering defect remains at initial time. Exact zero-time/coupling identities
must supersede coarse nonzero envelope values.

Sources: `research/round26/forward/ac1/report.md:41-60` for nesting and the
extra residual factor; its lines 67-88 for V/J and joining;
`research/round24/forward/x2/report.md:178-200` for the full spectral residual
and projector estimates; `research/round24/forward/z2/report.md:128-137` for
the strong Duhamel sign/domain; `research/round26/forward/ac2/report.md`,
sections “Retained evolution loads the new channels gradually” and “Full error,
centering and denominator”, for the separate delayed-loading improvement.

## 5. Dependencies and boundary of this review

The proposed source list covers the mathematical channel, cutoff, domain and
heat premises used above. The old machine-readable AC1 matrix is necessary
comparison context if a new implementation reads it; it cannot define the new
graph's rank or entries. Historical checkers can remain read-only reconstruction
sources. If any are executed by the new producer, add their actual execution
dependencies: both AC1 checkers read `research/round26/contracts/ac1.json`,
both AC2 checkers read `research/round26/contracts/ac2.json`, and their binding
lists may require further files. The reverse checkers additionally bind
`.codex/skills/qeg-research-advisor/references/newton-tesla-project-method.md`.
Concrete reads are at forward AC1 line 72, forward AC2 line 53, reverse AC1
lines 23/49 and reverse AC2 lines 45/77. No historical checker was executed here.

Omitting a numerical heat evaluator is a legitimate scoped choice. If one is
later included, physical omission and numerical error need separate budgets
against the same true denominator, and an uncertain center cannot be
exponentiated indefinitely. Source: `research/round26/forward/af2/report.md:55-65`
and `research/round26/reverse/af2/report.md:50-79`. Old graph accuracy constants
and fixed-coupling numerical results do not transfer to this new graph.

Subject to the clarifications above, I support freezing this bounded AH1 target.
This review proves no new graph rank, Gram, residual constant or heat accuracy.
It selects neither AH2 nor either final goal.
