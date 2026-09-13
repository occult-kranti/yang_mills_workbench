# B2 preliminary advisor review

Status: provisional mathematical review only. This is not a B2 gate and does not freeze C1.

## Evidence inspected

I inspected the current reverse/skeptic B2 preliminary artifacts and the frozen B2 contract. Forward B2 and a final forward-vs-reverse comparison are still pending, so the loop cannot be accepted from this review alone.

Inspected files:

- `advisor/contract-b2.json`
- `methods/round19-lessons.md`
- `backward/b2/check.py`
- `backward/b2/report.md`
- `backward/b2/output/results.json`
- `backward/b2/output/block-certificate.json`
- `backward/b2/output/pvp-linear.json`
- `backward/b2/self-comparison/comparison.json`

## Mathematical assessment

The reverse preliminary route is feasible and matches the frozen B2 contract shape. It uses the accepted 48-state B1 projector, writes `R=P\ominus\Omega` with dimension 47, keeps the 11 face states at electric level `3 alpha`, keeps the 36 six-cycle states at electric level `9 alpha/2`, and uses `QH0Q >= 6 alpha`. It does not reuse the old Round18 constant `3 alpha` block for all of `P\ominus\Omega`.

For a signed coefficient box `|lambda_f| <= r alpha`, the recorded row bounds are

\[
a(r)=3-2r,\qquad d(r)=6-11r,\qquad w(r)=\frac{19}{4}r^2.
\]

These agree with the inspected exact row data and root's independent tensor audit: the maximum `RVR` row coefficient is `2`, the maximum accepted B1 cross-Gram row coefficient is `19/4`, and the `r=3/8` value gives `a=9/4`. The Schur/min-max lower-bound function is therefore

\[
R(r)=\frac{9-13r-\sqrt{100r^2-54r+9}}{2},
\]

with positivity from `a,d>0` and

\[
(3-2r)(6-11r)-\frac{19}{4}r^2
=18-45r+\frac{69}{4}r^2>0.
\]

The smaller positive root is

\[
r_* = \frac{30-2\sqrt{87}}{23}\approx 0.493271386687929.
\]

Thus the required `r=1/8` box is comfortably certified, the Round18 benchmark `r=3/8` is rederived under the enlarged 48-state projector rather than assumed, the `r=7/16` control is still positive, and the same certificate is insufficient at `r=1/2`.

The direction of the spectral comparison is correct in the preliminary report: on `\Omega^\perp`, the Schur complement gives an `E1` lower bound, while the vacuum Rayleigh quotient gives the separate upper bound `E0 <= 0`. A positive `E1` lower bound then yields `lambda_1 - lambda_0 >= E1_lower - E0_upper` with `E0_upper=0` in this finite-graph statement.

## Current repair status and remaining gate checks

1. The reverse preliminary output now uses outward decimal intervals for the radical and range displays. This resolves the earlier label issue where a field called `lower_bound_decimal` was rounded to nearest; final artifacts should preserve outward-safe display.
2. The final B2 gate must wait for forward B2 bytes and a final independent comparison against the forward producer. The current self-comparison is useful for admission controls, but it cannot substitute for the paired forward/reverse agreement required by the method.
3. The final comparison should preserve the same B1 lessons: declared positive physical `E_star` must be checked directly; kappa/Fibonacci substitutions must fail even with ratios present; matrix/row data must be reconstructed rather than accepted from pass booleans; and missing manifest entries must fail closed.
4. The full parameter range should be described as the range certified by this finite row-bound Schur argument. It is not a physical gap closure result and does not advance the dense, limiting, or continuum goals.

## Provisional decision

B2 appears mathematically viable with the stronger continuous range `0 <= r < (30-2 sqrt(87))/23` under the inspected row-bound certificate, including the required `r=1/8` box and the `r=3/8` benchmark. I would not gate B2 until the final forward/reverse comparison independently reproduces the exact row envelopes, scale checks, source bindings, mutation controls, and outward-safe endpoint displays.
