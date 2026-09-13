# Round19 backward B1 reconstruction

This is the independent reverse/skeptic reconstruction for `advisor/contract-b1.json`.  The graph, channel enumeration, spin-label exclusion, threshold witness and exact cross Gram were reconstructed before reading Round19 forward B1 source.  The earlier limited note is preserved under `history/initial-limited-*`; it is superseded by the exact epsilon/Haar contraction here.

## Strict-cutoff physical projector

The actual adjacent two-cube graph has vertices `(x,y,z)` with `x=0,1,2`, `y=0,1`, `z=0,1`.  It has 12 vertices, 20 positive-axis links and 11 signed elementary plaquette faces, including the shared internal plaquette.  A ten-face outer-boundary ledger is therefore rejected for B1.

With `alpha/E_star = 2`, the strict cutoff is

\[
E_{\rm el}<6\alpha,\qquad E_{\rm cutoff}/E_\star=12.
\]

For a fundamental link, `j=1/2` costs `3 alpha / 4`.  Exhaustive support enumeration through seven active links gives exactly the vacuum, all 11 four-edge simple cycles, and all 36 six-edge simple cycles.  The four-edge cycles are precisely the actual plaquette boundaries.  The six-edge cycles have energy `9 alpha / 2`, strictly below the cutoff; 4 are planar rectangles and 32 are nonplanar by the coordinate-plane test.

I also ran an explicit spin-network label audit rather than relying only on even fundamental parity.  Every no-leaf support through seven links was enumerated: 11 of size four, 36 of size six and 28 of size seven.  Doubled spins `1,2,3` cover every energetic possibility below `6 alpha`; doubled spin `4` already costs `6 alpha` on one active link.  Vertex invariant tests through valence four leave only the 47 non-vacuum all-fundamental simple cycles.  The seven-edge no-leaf supports are excluded: all-fundamental labels have odd parity at some vertex, while changing one link to integer spin raises the all-half `21 alpha / 4` energy to `13 alpha / 2`, above the cutoff.

A threshold witness exists.  The checker records an eight-edge fundamental cycle with mask `0cc0f`, energy `6 alpha`, unique degree-two fundamental intertwiners and exclusion from `P` by the strict inequality.  Separately, the full equality audit finds 99 support/label assignments at `E_el = 6 alpha`, which become 107 physical threshold channels after vertex-intertwiner multiplicities: 91 assignments have multiplicity one and 8 degree-four assignments have multiplicity two.  Thus a `threshold_channel_count = 99` claim is only correct if it is explicitly an assignment count, not a physical-channel count.

## Exact cross Gram

For the retained 48-channel orthonormal Wilson-loop basis, I computed

\[
W^*W=P V^2P-(PVP)^2,
\qquad V=-\sum_f \lambda_f x_f,
\qquad x_f=\chi_f/2,
\]

as an exact polynomial in the 11 face couplings.  `P` reduces `H0` because the retained channels are complete `H0` eigenspaces below the cutoff.

The contraction uses fundamental spinor indices.  Negative link orientations are converted by

\[
(U^{-1})_{ab}=-\epsilon_{ac}U_{dc}\epsilon_{db}.
\]

Odd link occurrence vanishes.  For two occurrences, Haar integration uses `epsilon epsilon / 2`.  For four occurrences, I use the two invariant tensors `(12)(34)` and `(13)(24)` with Gram matrix `[[4,2],[2,4]]` and inverse `[[1/3,-1/6],[-1/6,1/3]]`.  The resulting epsilon constraint components are summed exactly as rational integers.  The sign convention is checked by one-link identities including `∫(Tr U)^2=1`, `∫(Tr U)^4=2` and `∫Tr(U)Tr(U^{-1})=1`.

The XOR sparsity audit has 115 upper-triangle cubic candidates and 851 upper-triangle unordered-face quartic candidates, with rank-four branch histogram `{0:420, 1:268, 2:96, 3:56, 4:11}`.  The final upper-triangle cross Gram has 222 nonzero matrix entries and 867 ordered quadratic coefficients after expanding off-diagonal `lambda_f lambda_g` terms.  The vacuum row and column vanish after the `PVP` subtraction.

## Controls and producer conditions

The checker rejects dropping a six-edge channel, using the Round18 face-only projector, including the threshold channel, using an outer-boundary graph, omitting the `PVP` subtraction, relabeling a conservative bound as exact Gram, using a bad physical scale, or promoting a Ritz/sample gap to a full complement threshold.

For comparison I require concrete signed graph incidence normalized to the actual two-cube graph, the exact 48 channel masks, threshold exclusion at `6 alpha`, the scale checkpoint `alpha/E_star=2` and `strict_cutoff/E_star=12`, and a full cross-Gram coefficient ledger.  Counts, pass strings and source hashes alone are not mathematical evidence.

## Forward comparison

The schema-adapted comparator accepts the current hash-locked forward B1 output.  It normalizes graph edges by coordinates, checks each face word as an ordered closed path up to cyclic shift and full reversal/inversion, maps channels and faces by canonical masks independent of producer ordering, sums ordered `(face_f, face_g)` rows into the commutative polynomial, and compares the complete cross-Gram coefficient ledger.  It also binds the producer source manifest and runs in-memory mutations for omitted channels, threshold inclusion, signed-incidence damage, changed Gram coefficient, missing `PVP` subtraction, zero scale, wrong cutoff, bound-as-exact and the threshold 99-vs-107 count error.

Canonical comparison for advisor gating is `research/round19/backward/b1/comparison/comparison.json`.  The previous accepted comparison is preserved as `history/comparison-before-normalization-sourcebinding-fix.json`; it is superseded because its normalization doubled independent off-diagonal face coefficients while sorting matrix triangles too early, and its manifest checks admitted omitted entries conditionally.  The repaired comparator aggregates forward coefficients per ordered matrix entry, verifies transpose equality, then compares the canonical upper triangle without an extra face-order factor.  It also rejects antisymmetric matrix-triangle corruption and missing source-manifest source/output entries.  Ordinary and optimized comparison hashes can differ because the comparison JSON records output paths/mode-local independent reconstruction paths; the mathematical checks and source-bound forward bytes are the same.

The final comparator also validates the explicit `E_star` field itself.  It accepts the forward declaration `positive symbolic physical energy reference`, while rejecting `E_star=0`, kappa substitution and Fibonacci-index substitution even when `alpha/E_star=2` and `strict_cutoff/E_star=12` are left unchanged.
