# Round32 sub-round 1 -- modern (Penrose/Feynman) lens, assistant-1

Status: assistant/coder cross-check tools, per `loop3-signoff.md` section 3.
**These outputs count zero research loops.** They are previews and
cross-checks only: python-flint 0.9 (Arb) and mpmath are independent
open-source rigorous/high-precision libraries used here for comparison,
never for admission. Every number this repository actually admits is
decided by exact `fractions.Fraction` arithmetic in a frozen `check.py`
inside `forward/`, `reverse/` or `skeptic/`; nothing in this directory is
imported by any of those, and nothing here changes a verdict.

Human project author: Hruday N M (BUNZEEY). Run everything with `python3 -B`.

## Files

- `flint_harness.py` (S1): reusable `fmpq_mat`/Arb harness --
  `exact_matrix_from_rows`, `rayleigh_bounds`, `arb_eig_preview`,
  `contains`, plus `to_fmpq`/`from_fmpq` and a pure-`Fraction`
  `rational_sqrt_bracket` (directed rational square roots, independent of
  Arb). Self-test: PASS.
- `flip_parity_k2.py` (S2): the AW1 link-flip parity lemma (exhaustive
  6^3 and 9^3 enumeration, a random-SU(2) numpy fixture) and an
  independent, from-scratch re-derivation of the I1 24-anchored-face-class
  table used to brute-force the AV1 face/owner-set/cover counts. Self-test:
  PASS.
- `window_budget_crosscheck.py` (S3): the AV2 window kernel (`ghat`,
  `M_0`, `M_1`, `M_2`) by mpmath quadrature and Arb ball arithmetic, the
  window radius `E` and crossover `s*`, and the retained Poisson-kernel
  control. Self-test: PASS.
- `results.json`: combined machine-readable output of all three self-tests
  plus the three planning notes below.

```
python3 -B research/round32/experts/modern/assistant-1/flint_harness.py
python3 -B research/round32/experts/modern/assistant-1/flip_parity_k2.py
python3 -B research/round32/experts/modern/assistant-1/window_budget_crosscheck.py
```

All three exit 0 (PASS) as of this writing; each prints its own JSON
report and exits 1 on any failed sub-check.

## S1 results

- 4x4 symmetric rational-matrix self-test: the exact Rayleigh quotient of
  a rational near-eigenvector trial vector (`4.7452812401736715...`)
  lies within `1.12e-6` (the harness's own exact rational residual bound)
  of an Arb-enclosed eigenvalue at 256 bits -- the standard perturbation
  guarantee holds exactly as computed, not merely numerically.
- AV1 tier-(ii) check, `eps = 2t + t^2` at `t = 49/14398580736`
  (AV1's own "t"/"T_self_consistent" value, tau=+1e-8):
  - **Forward**: `D_ii == 2*eps*(1+eps)/(1+eps^2)` holds as an **exact**
    `Fraction` equality (no sqrt is involved; both sides are rational),
    and independently as an Arb-256-bit ball containment. PASS.
  - **Reverse, literal spec check** (`D_ii >= 2*eps/sqrt(1+eps^2)` at the
    *same base* eps): **fails** (`1.139...e-8 < 1.361...e-8`). This is
    not a defect: AV1's reverse producer's admitted tier-ii `D_ii` is a
    *sharper* bound built from its own smaller epsilon
    (`reverse/av1/output/results.json` `tiers.tier_ii.+.epsilon`
    `= 461213409663624001/80984034066839961600000000 ~ 5.695e-9`, the
    82-face-meeting-R restriction), not the fidelity formula evaluated at
    forward's coarser `eps=2t+t^2 ~ 6.807e-9`. The harness reports both
    the literal check (FAIL, explained) and an internal-consistency
    check at reverse's own epsilon (`D_ii >= 2*eps_rev/sqrt(1+eps_rev^2)`,
    PASS) confirming reverse's own directed rounding is sound. The
    overall S1 self-test gates on the internal-consistency check plus the
    exact forward equality, both of which hold, so S1 **PASSES**, with
    the literal-check discrepancy fully documented in `results.json`.

## S2 results

- Exhaustive flip-parity check: 0 failures on 648 plaquettes (6^3) and
  2187 plaquettes (9^3); every plaquette meets `E` in 1 or 3 links, never
  0, 2 or 4 (histogram in `results.json`).
- Random-SU(2) numpy fixture (4^3 lattice, seed fixed): every one of 81
  plaquette Wilson traces flips sign under the `E`-link `-I` flip, and
  every individual link's `tr(U)^2` (a Casimir-invariant, gauge-covariant
  quantity) is unchanged to `<1e-10`.
- Independent from-scratch re-derivation of the I1 24-anchored-face-class
  table (encoded directly from `research/round21/forward/i1/report.md`
  lines 59-66, not imported from AV1) reproduces **every** AV1 number by
  brute force over a fine box: 49 faces per site, 15 owner-set groups
  (multiplicities `1,1,1,1,1,2,2,2,3,3,4,4,4,10,10`), 82 faces meeting
  `R={0,e_z}`, 10 inside `R`, 72 straddling split exactly `42` (one
  outside site) `+ 30` (two outside sites). A concrete `W` (the xz face,
  `r=0,s=0`, block `(0,0,0)`) shares a fine link with exactly **10**
  other faces meeting `R` (reported, no target given in the spec).
- K_2 tier check: crude tier `1.65e7` correctly fails the `6.9e5` cap
  (margin `0.042`, `<1`); the skeptic's 84-face bound (`1.88e4`, margin
  `36.7`) and the enumerated 49-face triangle tier (`1.10e4`, margin
  `62.7`) both clear the cap with margin `>=10`, matching
  `loop2-response.md`'s own table (`36.9`, `63`) to the precision that
  table itself carries.

## S3 results

- `ghat` (C^2 window) by direct mpmath quadrature (50 digits, split at
  the `x=0` kink) matches the closed form
  `4s^3/(pi(s-i*theta)^3(s+i*theta))` to `<6e-37` at `theta in
  {0, 0.7, 3, -2.3}`, `s=1`; independently, Arb (256 bits) balls built
  from exact rational inputs contain the mpmath value at every one of
  those points.
- Moments by quadrature: `C^2` `M_0=2`, `M_1=4/pi`, `M_2=2s^2` all match
  their closed forms to `<1e-20`. `C^1` sibling: `M_0=4/pi` matches;
  `M_2` is confirmed **divergent** -- the truncated integral over
  `[-L,L]` grows monotonically and by `>5.5x` from `L=10` to `L=1e5`
  (logarithmic growth, consistent with the `theta^-1` large-`theta`
  tail of `theta^2*|ghat_{C^1}|`).
- Negative-atom control: `g_{C^2}(-1) = 5/e` and `g_{C^1}(-1) = 3/e`,
  both exact to `<1e-30`.
- Window radius `E = M_0(D+D^2) + k*M_1` at `tau=1e-8`, `s=1`, with the
  AV1-admitted forward tier-ii `D`: computed (Arb, 256 bits)
  `= 1.8319675034118793e-07`, matching AV1's own recorded
  `av2_feasibility_threshold.F_at_D_ii_upper_preview = 1.8319675e-7`
  from `forward/av1/output/results.json` to `<5e-12`, and clears the
  `1e-6` target with wide margin.
- Crossover `s*` (where `E(s)=1e-6`, solved exactly, then Arb-enclosed):
  `6.2369` -- inside the AV2 contract's stated `~6.1-6.3` band.
- Poisson-kernel retained control: the first moment grows monotonically
  with the log of the cutoff `L` (confirmed divergent, as expected against
  the window's finite first moment). The `D->0` optimized-floor
  reconstruction (`~1.279e-6` at `L*~4.15e6`) matches AT4/AT5's reported
  `~1.2651e-6` to within `1.1%`. The `L=1e4` point figure is reported for
  information only and is **not** used to gate pass/fail: AT4
  (`research/round31`) predates AV2's admitted seven-star Duhamel slope
  `k=49|tau|/4` and used its own round31 slope constant, which this tool
  does not import; matching it exactly would require pulling in AT4's own
  premises, out of scope for a zero-loop preview tool.

## Three planning notes for the lens

**What the finite-graph AZ2 spec needs from these tools.** AZ2
(`loop2-response.md` section 6) is a finite-graph exact-Ritz-vector
calculation (Round11 two-square patch, `D=6/8` cutoffs) whose own
admission stays `Fraction`-only, but S1's `rayleigh_bounds` already
implements exactly AZ2's "exact Rayleigh quotient + directed rational
sqrt residual bound" pattern on a general `flint.fmpq_mat`, so AZ2's
producer can call it directly instead of re-deriving the `sin(theta)`
machinery, and `arb_eig_preview` gives AZ2 its own required "Arb
cross-check: independent `fmpq_mat` rebuild ... `acb_mat.eig` balls"
line item for free, labelled preview. S1's 4x4 self-test is a template
for AZ2's own (larger) matrices before committing to exact rational
inverse iteration.

**How AW1 should use S2.** AW1 needs three things from S2: (i) the
exhaustive flip-parity check plus the SU(2) numeric fixture as an
independent numerical sanity check alongside (never instead of) its own
algebraic argument; (ii) S2's from-scratch re-derivation of the I1
24-class table, which reproduces every one of AV1's frozen face/owner-set
numbers by brute force from the translation rule alone -- a genuinely
second, independent source for AW1's own enumeration control, not a
reformatting of AV1's output; (iii) the `second_order_multiplier_structure`
report, which isolates the 10 owner-set-exactly-`R` faces as the only
candidates whose single-face creation could overlap `W Omega_R` without a
straddling partner -- exactly the set AW1's parity argument needs to show
the mod-2 obstruction kills that overlap, leaving only the
straddling/pair/density terms it must still itemize and bound.

**What the Arb harness can certify versus preview.** Arb (ball
arithmetic) and mpmath interval arithmetic can rigorously *certify
containment*: given an exact rational enclosure already produced by
admitted `Fraction` arithmetic, Arb at high precision (256 bits used
throughout) proves that enclosure brackets the true value of a
transcendental (`pi`, `exp`, `sqrt`, the window's Fourier transforms, the
eigenvalues of a fixed-size symmetric matrix) far more tightly than the
workbench needs, and a failed containment is real evidence of a defect.
What it cannot do is decide admission: an `acb_mat.eig` on
floating-point-derived entries, or a numerical Fourier quadrature, is a
preview/comparison exactly as `research/round32/tools/arb_crosscheck.py`
already states -- it has no role in any `check.py`, and no floating-point
value from mpmath or numpy ever substitutes for the exact rational
arithmetic that alone decides a gate.
