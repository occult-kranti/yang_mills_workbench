# E1 forward: literal aligned boxes with a declared energy origin

Let Λ_N have vertices `{0,...,N}³`, all internal nearest-neighbor links,
and every face whose four links are internal. Keep the actual fixed inherited
A1 coefficients: selected xy faces have left/end, bridge, right/end bounds
`|λ_L|,|λ_R|≤α/2`, `|μ|≤α/8`, including zero and signed values; omitted faces have
`ατ/(24*2^(x+y+z))`. No interaction coefficient depends on N. Lattice spacing
a is fixed and has length units. α and E_star are fixed positive energies.

## The full-factor aligned subsequence

Choose N=4m+3. A selected strip anchored `(4i,2j,z)` has x support
from 4i to 4i+3 and y support from 2j to 2j+1. The allowed anchors are
`0<=i<=m`, `0<=j<=(N−1)/2`, `0<=z<=N`; they fit exactly. Conversely,
every selected horizontal or vertical link inside Λ_N maps to one of those
anchors by D1's explicit factor-assignment rule. Because N is odd, no upper
y boundary clips a row; because N=3 modulo 4, no upper x boundary clips a
strip. All other links are complete free factors. This proves the property
for all m≥0, rather than extrapolating from four fixtures.

There are `3N(N+1)²` links, `3N²(N+1)` faces, and

\[
B_N=\frac{(m+1)(N+1)^2}{2}
\]

complete ten-link strips. Thus free links number `3N(N+1)²−10B_N`,
selected faces number 3B_N, and omitted faces number `3N²(N+1)−3B_N`.

## Orientation-specific omitted weight

The three anchor ranges are genuinely different:

| Orientation | Anchor coordinates |
|---|---|
| xy | x,y<N; z≤N |
| xz | x,z<N; y≤N |
| yz | y,z<N; x≤N |

Write `g_k=2(1−2^(−k))`,
`a_N=(28/15)(1−16^(−(m+1)))`, and
`b_N=(4/3)(1−4^(−(N+1)/2))`. The total retained weight and selected
weight give the exact omitted ledger

\[
W_N=\frac{g_N^2g_{N+1}}8-\frac{a_Nb_Ng_{N+1}}{24},\qquad
T_N=\frac{107}{135}-W_N\downarrow0.
\]

Every anchor retained by a smaller box keeps its old coefficient. Positivity
and exhaustion of the omitted-face set prove the tail limit. Summing an
all-three-coordinate anchor cube gives a different ledger and is rejected.

## Original operator, scalar subtraction, and exact lift

On the literal box's full link space define its original unshifted operator

\[
H_{box,N}=\sum_{C\subset\Lambda_N}H_C
+\sum_{e\in F_N}\alpha C_e+V_{box,N},\qquad
c_N=\sum_{C\subset\Lambda_N}E_C.
\]

If all strips have the same inherited coefficients, `c_N=B_NE_strip`;
the sum formula remains valid without that simplification. Subtracting c_N
changes the energy origin, not any interaction. The box factors and exterior
reference factors split exactly, so on the A2 representation

\[
(H_{box,N}-c_N)\otimes I+I\otimes H_{ref,out}
=H_{ref}+V_{box,N}.
\]

D1 and D2 therefore apply with `ε_N=α|τ|T_N`,
`β_N=α|τ|W_N`, `g_N^energy=α/8−β_N`, provided
`α|τ|107/135<α/8`. For nonreal physical energy z the resolvent error is
at most `ε_N/|Im z|²`. The shifted ground-energy error is at most ε_N,
the ground-projector error at most `min(1,ε_N/g_N^energy)`, and the
expectation error of bounded A at most twice that times `||A||`.

Adding c_N back preserves all ground vectors and spectral gaps. It does not
preserve the absolute ground energy or a resolvent evaluated at the same z.
In particular, convergence of unshifted energies is not asserted. If a strip
interaction is nonzero, the constant Haar trial has zero energy but is
not annihilated by H_C (the distinct plaquette characters are orthogonal);
positivity of H_C would contradict that combination, so E_C<0. Under the
additional assumption of identical nonzero strip coefficients, a growing
number of strips supplies a divergent negative scalar origin. All-zero
strip coefficients instead give E_C=0; the theorem permits both cases.

## Limits and checks

The checker enumerates full literal link and face sets at N=3,7,11,15;
verifies every strip link; checks counts and exact dyadic sums; and applies
the accepted quantitative bounds. At N=4 the full-factor assertion fails.
Countercontrols also execute the wrong anchor ranges, dropping the exterior
generator (the D1 escaping excitation), a nonzero scalar shift at fixed z,
and a zero physical reference. Ordinary and optimized outputs agree.

This proves a literal aligned subsequence after explicit scalar subtraction
and the exact exterior-reference embedding. Arbitrary boundary phases remain
for E2. Fixed spacing, summable omitted weights and the chosen representation
remain premises; neither homogeneous nor continuum Yang–Mills follows.
