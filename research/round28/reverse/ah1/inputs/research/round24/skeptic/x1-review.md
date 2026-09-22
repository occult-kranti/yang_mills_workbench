# X1 independent skeptic review

Verdict: **accepted for the two distinctly stated finite-graph approximation
theorems and the assembled 21-state compression; practical higher-cutoff
evaluation remains limited**. Both submissions were frozen before review.
This is independent model-agent review of shared premises, not external peer
review. The T graph is not the homogeneous S/W model or canonical U/V model.

## Projection, domain and actual sector

Both projections retain whole Peter-Weyl representation blocks before/after
commuting gauge averaging. They therefore preserve all 18 Gauss constraints,
reduce the actual electric operator and preserve its operator and form domains.
Bounded invariant magnetic multiplication leaves the self-adjoint domain
unchanged. Finite rank follows from bounded representation labels, not from
removing the exterior of an arbitrary small matrix.

The cutoffs are different: forward uses total kinetic energy `<R`; reverse
uses total twice-spin degree `<=N`. Both independently identify the 21-state
vacuum-plus-20-faces subspace at their small cutoff. A nonempty invariant active
support must contain a cycle. The grid is simple bipartite with girth four;
four-edge supports are square cycles with a unique invariant intertwiner and
equal spins. A five-edge minimum-degree-two bipartite support is impossible.
The stated strict energy cutoff or degree-four cutoff therefore excludes
every other label class. Actual face/cycle enumeration and all ordered triple
parity tests agree.

Haar normalization gives vacuum/face magnetic coefficients `-lambda/2`,
face diagonal `3+20lambda`, and no triple-face term. The spin-one character
on a matching face is a normalized excluded physical state and couples with
coefficient `-lambda/2`. Thus this actual compression has leakage for positive
lambda. Its two-dimensional symmetric block is autonomous only inside the
finite compression. Reverse additionally justifies strict Galerkin ground
energy error through this nonzero coupling of the finite ground to an excluded
state. The positive variational correction is not an observed trajectory.

## Forward theorem: delayed full-input operator norm

The block heat equations include the full excluded block and its return path.
The scalar magnetic term is removed only in the off-diagonal bound
`||B||<=20lambda`; it remains in diagonal energies. Nonnegativity gives heat
contractions and an excluded kinetic lower bound R. The Schur equation has the
correct negative self-energy sign and yields the stated energy-error bound.
The separate excited-P and Q ground components give the claimed projection
distance estimate.

Separate exact ground centering is carried through the finite interval and
large-time projection comparison. Splitting at T proves full operator-norm
convergence uniformly for every heat time `sigma>=tau>0`, including after
compression by J. R increases only after T is chosen to control the late-time
tail. At zero time the finite-rank positive compression has exact norm error
one, so tau cannot be silently set to zero. Real-time smoothing is not claimed.

The optional finite-matrix coefficient perturbation bound is valid when
`2kappa<g` and each interpolated matrix is centered by its own exact simple
ground. The ground-ground derivative vanishes; mixed and excited blocks give
the stated sufficient `4kappa/(g-2kappa)` bound. Independent energy rounding
on an unbounded time interval instead causes growth or ground loss, as the
report correctly demonstrates. A matrix-function evaluation error must still
be separately certified.

## Reverse theorem: retained inputs on a finite window

The square multiplier raises total degree by at most four. Consequently every
Dyson path below the first excluded order agrees on the declared retained input
class; all remaining paths, including exit-and-return paths, lie in the bounded
tail. Scalar `20lambda` is retained and cancels only the permitted uncentered
tail prefactor. The factorial tail bound is uniform on the stated finite window.

The actual ground's Neumann reconstruction uses the true electric gap, bounded
perturbation and actual scalar `20lambda-epsilon>=0`. Its degree-growth rule
gives an excluded ground tail. Rayleigh-Ritz then yields the ground-energy
error with a positive denominator. The separately centered approximation
includes that error; it is not replaced by the vacuum trial energy. Initial
time and zero coupling have exact zero error on retained inputs, consistent
with the full-input obstruction.

These two theorems have different input classes, cutoffs and time sets. Their
numerical budgets cannot be combined or their constants treated as estimates
of the same approximation. In particular the high-cutoff `R=1024` full-input
bound below 0.002 and `N=20` vacuum-window bound below `10^-6` establish
sufficient existence budgets. Neither corresponding large matrix was assembled.

## Replay, limits and X2 recommendation

Both normal and optimized replays reproduce frozen outputs exactly. All source
hashes, dependencies and instruction snapshots verify, with at least three true
Boolean controls per producer. `x1-replay.json` records those bindings. Actual
graph, Haar coefficient, spin-one leakage, phase/centering, cutoff and zero-time
controls are substantive; the arithmetic bounds use rational enclosures.

The useful next X2 target is certified evaluation of an actually assembled
manageable physical sector, with rigorous omitted-channel and centering error,
or an actual boundary-residual estimate that materially reduces the required
cutoff. A graph-physical matrix should be built and evaluated rather than a
large cutoff merely assigned. State the initial class and heat interval before
execution, retain leakage, and expose when the resulting error is inconclusive.
No practical high-accuracy solver, homogeneous-volume statement, physical
calibration or continuum result is admitted by X1.
