# Round19 backward C1 reconstruction

This is the independent backward C1 reconstruction from the frozen `advisor/contract-c1.json` and accepted B2 gate.  It reconstructs the actual 2×2×1 four-cube graph, freezes all links except three vertical links, derives the seven affected face traces from signed face words, and computes the normalized static integral

\[
\frac{\mathbb E[O\exp(\kappa S)]}{\mathbb E[\exp(\kappa S)]},
\qquad \kappa=1/64.
\]

This is a static mathematical checkpoint only.  The common κ is not `E_star`, not a physical energy/time scale, and does not close the common physical-scale matching issue.  Fibonacci/static labels remain organizational unless a later gate supplies a physical scale argument.

The active links are the z-axis links `U=(1,1,0)`, `V=(1,0,0)`, and `W=(0,0,0)`.  The reconstructed graph has 18 vertices, 33 edges, and 20 faces.  Exactly seven faces touch an active link; the other thirteen are constant and cancel only in this normalized conditional quotient.  The signed words reduce to

\[
S=3x+y+z+w+t,
\]

where `x=Tr(U)/2`, `y=Tr(V)/2`, `z=Tr(W)/2`, `w=Tr(UV†)/2`, and `t=Tr(VW†)/2`.  The checker constructs the action polynomial from the graph-derived coefficient dictionary `{x:3,y:1,z:1,w:1,t:1}`.

The observable is kept unchanged from the U–V branch:

\[
O=\frac{(4x^2-1)^3(4w^2-1)}{81}.
\]

The checker uses two exact routes for every monomial needed through Taylor degree 8.  The first is the SU(2) character-fusion formula with the dimension divisors `(i+1)(k+1)`.  The second conditions on the common V variable and expands S³ coordinate moments as polynomials in `y`; no division by sine factors occurs, so the `y=±1` endpoints are regular.  Explicit endpoint polynomial fixtures are stored in `results.json`.

The unweighted common-V discriminator is

\[
\mathbb E[xzwt]=1/64.
\]

If the V variable is incorrectly resampled independently between the U–V and V–W branches, the same expression gives 0, so the primary model must retain the shared V dependence.  The checker also verifies that dropping the true outer `Z_U(V)` weight changes the exact κ² partition coefficient.

The Taylor/remainder ladder is degrees `0,2,4,6,8`, with maximum moment degree 16.  The remainder bound uses `|S|≤7`, `|O|≤1`, and, for actual `M=|κ|7=7/64<1/2`, the geometric tail

\[
\sum_{n>N}\frac{M^n}{n!}
\le \frac{M^{N+1}}{(N+1)!(1-M)}.
\]

The interval routine rejects negative remainder radii and any partition lower bound with `Z-R≤0`.  At degree 8, the normalized κ=1/64 interval is

\[
[0.000000792445966,\;0.000000792445981],
\]

with exact rational endpoints in `intervals.json`; the width is below `1e-12`.  The signed fixture at `κ=-1/64` is stored separately to catch false evenness.

The freeze-W regression sets `W=I`, so `z=1` and `t=y`, giving `S=3x+2y+w+1`.  The checker verifies the exact coefficient convolution

\[
[e^{\kappa(S_{old}+1)}]_n=\sum_{m\le n}\frac{[e^{\kappa S_{old}}]_m}{(n-m)!}
\]

for both numerator and partition through degree 8.  Thus the constant `+1` contributes a common `exp(κ)` factor that cancels analytically in the normalized quotient, recovering the old two-link expression with `S_old=3x+2y+w`.

The standard comparison interface is

```bash
python3 research/round19/backward/c1/compare.py --producer SOURCE --evidence OUTPUT --output NEW_DIR
```

Self-comparison has been run in normal and optimized modes.  Both accept with 25 checks.  The comparator reruns the independent checker, compares graph counts, active coordinates, affected signed words, constant-face ledger, full moment table, coefficient rows, interval ladders, freeze-W regression, and source-manifest bindings.  Mutation controls reject wrong graph counts, wrong active U coordinate, omitted affected/constant faces, a changed noncommuting V–W signed word, hard-coded/malformed S, altered observable, independent-V primary substitution, changed moment divisor effect, degree-6 truncation as final, false evenness at negative κ, missing freeze regression, κ/Fibonacci physical-scale substitutions, and missing source/output manifest entries.


Additional pre-lock repairs were applied after root review.  The signed-κ regression now requires disjoint exact positive/negative κ enclosures and records an odd Taylor-coefficient witness; it no longer compares dictionaries that differ merely by the stored κ label.  The independent-V control is derived as `E[xw] * E[zt] = 0`, rather than assigned.  The signed-word ledger remains the graph baseline, and an additional exact quaternion fixture distinguishes `Tr(UV†)/2` and `Tr(VW†)/2` from wrong sign-flipped products on explicit noncommuting unit quaternions.  Public API validation controls execute bool, negative, wrong-dimension exponent, bool/negative degree, bool κ, and wrong κ inputs and require exceptions.


## Final forward comparison

Forward C1 final lock received from root:

- `research/round19/forward/c1/check.py`: `4142058ec3f797cb04e05056ad811499592b0a74cc1758c3c3fef2aa3bf6145c`
- `research/round19/forward/c1/report.md`: `46d8a730b2967eab685934a8eb19c442d4767d3f9c2977641f5124ce7f997454`
- `research/round19/forward/c1/output/results.json`: `b366c2d50c6198a81a6603e48129177b87b5000ec44252b9f9d6c53f66a1451c`
- `research/round19/forward/c1/output/source-manifest.json`: `99a0746ae28b8778afab67f41621cd955c04391dbe30a6aa07594cd60dd18d54`

The canonical comparison commands are:

```bash
python3 research/round19/backward/c1/compare.py --producer research/round19/forward/c1 --evidence research/round19/forward/c1/output --output research/round19/backward/c1/comparison
python3 -O research/round19/backward/c1/compare.py --producer research/round19/forward/c1 --evidence research/round19/forward/c1/output-optimized --output research/round19/backward/c1/comparison-optimized
```

Both accept.  The comparison canonicalizes moment exponents as `(x,y,z,w,t)` vectors rather than relying on list order or producer row order.  It compares exact coefficient rows through degree 8 and validates each producer interval from the declared partial numerator, partial partition, and declared tail radius.  The declared tail must be at least the independent geometric tail, the quotient denominator lower bound must be positive, the interval endpoints and width must recompute exactly, and the degree-8 width must meet `1e-12`.  This accepts different valid interval radii while rejecting forged or overlapping-only interval evidence.

The freeze-W comparison checks the exact coefficient identity for the old `3*x+2*y+w` expression and the analytic cancellation of the common `exp(kappa)` factor.  The outer-weight check distinguishes the true κ² partition coefficient `13/8` from the dropped-`Z_U` model coefficient `3/8`.
