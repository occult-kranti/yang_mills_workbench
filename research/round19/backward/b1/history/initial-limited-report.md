# Round19 backward B1 preliminary reconstruction

This is an independent reverse/skeptic reconstruction for `advisor/contract-b1.json`.  I wrote this derivation before inspecting any Round19 forward B1 source.  The result is deliberately limited: it reconstructs the strict-cutoff physical-channel inventory on the actual two-cube graph, but it does not certify the full exact cross Gram for the resulting projector.

## Graph and cutoff

The graph is the adjacent two-cube cubical graph with vertices `(x,y,z)`, `x=0,1,2`, `y=0,1`, `z=0,1`.  It has 12 vertices, 20 positive-axis links, and 11 elementary plaquette faces.  The face set includes the shared/internal plaquette; an outer-boundary-only ten-face ledger is not the B1 Hamiltonian.

For a fundamental active link, the electric contribution is

\[
\alpha j(j+1)=\frac{3}{4}\alpha,\qquad j=\frac12.
\]

The strict B1 cutoff `E_el < 6 alpha` therefore permits at most seven fundamental links and excludes every eight-link fundamental support at threshold.  I enumerated every edge subset of size at most seven and retained exactly those with even active degree at every active vertex.  The retained set is exactly:

- the vacuum,
- all 11 four-edge simple cycles, which coincide with the 11 actual elementary faces,
- all 36 six-edge simple cycles.

The retained dimension is therefore 48 under the fundamental simple-cycle classification.  The six-edge cycles are not optional examples: they have energy `9 alpha / 2`, which is strictly below `6 alpha`.  Of the six-edge cycles, 4 are planar rectangles and 32 use all three coordinate axes and are nonplanar by the coordinate-plane test.

## Intertwiner and omitted-channel check

For a nonempty support below eight fundamental links, the even-degree audit returns only connected degree-two cycles.  On a degree-two fundamental SU(2) cycle, adjacent representation labels are forced equal and the two-valent invariant is unique up to scale, so the fundamental simple-cycle channel has multiplicity one.  A higher-spin four-cycle begins at spin one and has energy `8 alpha`, above the strict cutoff.  Disconnected two-plaquette products first use eight fundamental links and sit at the threshold.

The checker also enumerates simple cycles through length eight.  It finds 72 eight-edge cycles.  One explicit threshold witness has mask `0cc0f`, edge count 8 and energy `6 alpha`; it is physical by the same degree-two fundamental-cycle argument, but it is excluded from `P` by the strict inequality.

## Cross-Gram status

The original B1 obligation remains

\[
W^*W=P V^2P-(PVP)^2,
\qquad V=-\sum_f \lambda_f x_f,
\]

with `P` equal to the full strict-cutoff projector above.  Since the independently reconstructed `P` has 48 channels, the Round18 12-by-12 face-only Gram is not an acceptable substitute: it omits 36 channels below the current cutoff.  A scalar norm bound, a row-sum bound, a sampled Ritz matrix, or `PV^2P` without the `(PVP)^2` subtraction also cannot be relabeled as the exact cross Gram.

I have not independently implemented the SU(2) Haar/recoupling calculation for all 48-by-48 exact entries of `PV^2P` and `PVP`.  The B1 gate should therefore treat this backward artifact as `limited-exact-gram-open` unless a later independent exact-entry computation is supplied and compared.

## Controls and accept/reject conditions

The executable controls reject or limit these wrong models:

- dropping a six-edge below-cutoff channel,
- using the Round18 face-only projector for the Round19 cutoff,
- including an `E_el = 6 alpha` threshold channel in `P`,
- replacing the actual graph by an outer-boundary-only face ledger,
- presenting `PV^2P` without the `PVP` subtraction as exact `W^*W`,
- presenting a conservative bound as an exact Gram,
- using kappa, tolerance, volume, Fibonacci index, or `E_star=0` as the physical energy scale,
- promoting a Ritz or sampled matrix gap to a full complement threshold.

My present accept condition for a producer is: concrete graph incidence with 12 vertices, 20 links and 11 signed faces; concrete retained channel masks matching the 48-mask strict-cutoff inventory; a threshold witness at `6 alpha` excluded from `P`; positive physical scale fields with `alpha/E_star` and `lambda_f/alpha` separated; and either an independently checkable exact 48-by-48 cross-Gram ledger or an explicit limited status preserving the exact-Gram obligation.  I reject a 12-channel face-only result, an outer-boundary graph, threshold inclusion, pass-booleans without masks, hash-only provenance, or a bound labeled as exact Gram.
