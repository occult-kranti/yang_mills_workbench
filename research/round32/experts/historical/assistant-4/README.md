# Historical lens (Newton/Tesla) assistant scripts -- Round32 sub-round 4

Human project author: **Hruday N M (BUNZEEY)**. AI-assisted assistant scripts for the
Newton/Tesla historical lens, delivering the three scripted tests requested in
`research/round32/advisor/panel-update-3.md` item 6, historical share: an
independent recomputation of the AY1 padding-family (I1 section 6) contraction
family, a small exact fixed-vector/moving-vector fixture, and an independent
recomputation of `D`/`2D` against the AY1 gate. These scripts and this note
count **zero research loops**: they are cross-checks and previews for the
lens, not a producer, skeptic or advisor artifact, and nothing here is
admission evidence. Nothing here reads or imports `research/round32/forward/
ay1/check.py` or `research/round32/reverse/ay1/check.py`; every geometric,
algebraic and arithmetic construction is re-derived from the frozen contract,
gate and report text, from `research/round21/forward/i1/report.md`, and from
the two producers' exported `output/results.json` (data, never code).

Everything numeric that decides pass/fail is `fractions.Fraction`; no floats
appear in any pass/fail comparison. `mpmath` (arbitrary-precision float) and
`python-flint`'s `Arb` (verified ball arithmetic) are used only as explicitly
labelled numerical cross-checks of the single irrational input in this whole
package -- the bound `exp(1/8)<8/7` -- never as the bound itself and never in
a pass/fail comparison.

Read before writing: `research/round32/advisor/panel-update-3.md` item 6,
`research/round32/advisor/ay1-gate.json`, `research/round32/forward/ay1/
report.md` and `research/round32/reverse/ay1/report.md` (both frozen and
gated), `research/round32/forward/ay1/output/results.json` and
`research/round32/reverse/ay1/output/results.json` (data only),
`research/round32/forward/av1/report.md` and its `output/results.json`,
`research/round21/forward/i1/report.md` section 6, and this lens's
`assistant-1/am2_tiers_exact.py` (an assistant script, not a producer; its
`OMITTED_CLASSES` table and `faces_touching`/`vadd`/`vsub` helpers are
imported and reused, exactly as assistant-3's `uniform_face_count.py` and
`route_b_incidence_table.py` already reused it) and `assistant-3/README.md`,
`results.json`, `j0_contraction_replay.py` for this package's layout and
`results.json`/README conventions.

Run every script with `python3 -B <script>.py` (also confirmed byte-identical
under `python3 -B -O <script>.py` for all three scripts).

## What passed

All three scripts pass (`overall_pass: true` in each, and in the combined
`results.json`).

**`padding_family_contraction.py`.** Independently enumerates, for the I1
all-contained-face boxes with padding on `Lambda_N=[-N,N]^3`, `N=2,3,4`, the
anchor groups of retained faces for both named families:

- **F1** (AQ1 centered whole-star boxes): a whole 21-face star is retained at
  anchor `b` iff `b+S subset Lambda_N` (all-or-nothing); face count
  `168N^3` (`1344`, `4536`, `10752`).
- **F2** (I1 section 6, all-contained-face with padding): each of the 21
  omitted classes at anchor `b` is retained individually iff its own owner
  set is `subset Lambda_N`; face count `28N(2N+1)(3N+1)` (`1960`, `5880`,
  `13104`). The anchor-level classification (full/partial/zero star) gives
  `(64,60,1)`, `(216,126,1)`, `(512,216,1)` full/partial/zero-face anchors at
  `N=2,3,4` -- the single "zero" anchor at each `N` is the corner
  `(N,N,N)`, where every one of the six owner-set types needs a coordinate
  `<=N-1` that fails simultaneously in all three coordinates.
- The padded on-site volume `|B_+|` (`200`, `490`, `972`) is also
  independently re-derived by direct set union, not just cited.
- **Extra boundary faces**: `F2-F1 = 28N(5N+1)` (`616`, `1344`, `2352`),
  derived both by direct box enumeration and algebraically from the two
  closed forms above (`28N(2N+1)(3N+1) - 168N^3 = 28N(5N+1)` reduces exactly,
  since `(2N+1)(3N+1)-6N^2 = 5N+1`).
- **The 82 faces meeting `R={0,e_z}`** are independently enumerated (reusing
  assistant-1's translation-covariant `faces_touching`), and it is confirmed
  -- as actual `(anchor, class)` face identities, not merely as a matching
  count -- that **both families retain exactly the same 82 faces**, for
  `N=2,3,4` (their owner sets lie in `[-1,1]^2 x [-1,2]`, well inside every
  `Lambda_N`, `N>=2`).
- **Group supports** `|X|<=4` factors, by construction of the star
  `S={0,e_x,e_y,e_z}`, `|S|=4`.
- **The maximal per-site interaction sum** is computed by AM2's own
  definition (`J=max_u sum_{b: u in X_b} ||phi_b||`, crediting each
  *group's* own norm to every site in its actual support, not a per-face
  tally) and independently confirmed to be exactly `28|tau|` (`<=28`,
  attained in the bulk) for both families at `N=2,3,4`; at `|tau|=10^-8`
  this is `J_0=7/25000000`.
- **The AM2 contraction inequalities.** `exp(1/8)<8/7` is re-proved from
  scratch (a 12-term Taylor truncation plus an exact geometric tail bound,
  a different truncation degree from this lens's own assistant-3
  `j0_contraction_replay.py`'s 10 terms for the unrelated AX1/route-B `J_0'`),
  and cross-checked independently with `mpmath` (60 decimal digits) and with
  `python-flint`'s `Arb` (200-bit verified ball arithmetic; both confirm
  `exp(1/8) approx 1.13314845...<8/7 approx 1.14285714...`). Plugging the
  literal rational `8/7` into `G(t)=16e^{8t}(1+10t)`, `G'(t)=16e^{8t}(18+80t)`
  at `t=R=1/64` reproduces `G(R)<148/7` and `G'(R)<352` exactly, and hence
  `J_0 G(R)=37/6250000<1/64` and `2J_0G'(R)=77/390625<1`, matching the
  forward AY1 report's `HNM-AY1-F04` literally.
- **Termination order 8.** AM2's combinatorial argument ("a nested word with
  more than `2p` creations puts at least `p+1` on one side of `V_X`, all
  meeting a `p`-site set, so two overlap") is verified as a *general
  structural fact*, for `p=1,2,3,4`, on an independently constructed
  finite-dimensional commuting-nilpotent creation algebra (`p` disjoint
  single-site raising operators with distinct prime coefficients, and a
  GENERIC dense interaction `V` with distinct random rational entries, so no
  vanishing is an artefact of a special choice of `V`): `C^{p+1}=0`
  identically (pigeonhole: `p+1` singleton generators from only `p` distinct
  labels must repeat one, and the repeated factor kills the term after
  commuting it adjacent), hence `ad_C^k(V)=0` for every `k>=2p+1`, and for
  `p=4` this is confirmed to be **exactly** order 8: `ad_C^8(V)` is nonzero
  and `ad_C^9(V)=0` identically as a full `16x16` operator (not just applied
  to one vector). This is this script's **own** fixture (its concrete
  nonzero value is not `8!`, since it uses generic entries, not the
  forward/reverse `check.py`'s specific internal fixture, which is never
  read); the forward AY1 export's `termination_fixtures` field
  (`four_site_order8: 40320=8!`, `four_site_order9_zero: true`,
  `two_site_order4: 24=4!`, `two_site_order5_zero: true`) is cross-checked
  only for the qualitative, structural pattern (order `2p`, vanishing at
  `2p+1`), which matches for both `p=2` and `p=4`.
- **The reset budget on `R={0,e_z}`.** The 7 incident anchors are
  independently derived as `(0-S) union (e_z-S)` (not asserted), giving
  exactly `{(-1,0,0),(-1,0,1),(0,-1,0),(0,-1,1),(0,0,-1),(0,0,0),(0,0,1)}`,
  matching the forward AY1 export's `incident_anchors` list bit-for-bit; the
  reset budget `2 x 7 x 7|tau| = 98|tau|` reproduces the forward
  (`aq2_reset_R: 98`) and reverse (`padded_reset_R_per_tau: "98"`) exports
  exactly.
- **Cross-checks.** Every quantity above that the forward or reverse AY1
  `output/results.json` also exports (`faces_F1`, `faces_F2`,
  `extra_F2_faces` at `N=2,3`; `B_sites`, `am2_volume_sites`,
  `F2_partial_groups` at `N=2,3`; `faces_meeting_R=82`; `J_0`, `G_R_upper`,
  `self_map`, `exclusion`, `am2_termination_order=8`; the `incident_anchors`
  list; the reset budget `98`) matches bit-for-bit. `N=4` is a genuine
  extension beyond what either producer computed (they went to `N=2,3`
  only); it is checked only against this script's own two independently
  derived closed forms, which already match the producers exactly at
  `N=2,3`.

**`fixed_versus_moving_vector.py`.** A tiny, exact (2-qubit: an "R" register
and an "out" register), explicitly labelled **FIXTURE** illustrating the AY1
control "fixed-vector versus moving-vector" and
`common_enclosing_interval_not_equality`. A unit vector `(a,b)` on the
rational circle (`a=(1-t^2)/(1+t^2)`, `b=2t/(1+t^2)`) parametrises
`delta=eps*(a|1>_R|0>_out+b|0>_R|1>_out)`, `psi=(Omega+delta)/sqrt(1+eps^2)`,
`Omega=|00>`; `eps=1/10` (illustrative, not `tau`). The reduced density
`rho_R(a,b)` and its trace-norm distance to `P_R=|0><0|_R` are computed
exactly (the trace norm of a traceless `2x2` real-symmetric matrix is
`2 sqrt(-det)`, so every comparison is done on the exact rational *square*,
never on a floating square root). A sequence `t_N=1/N`, with sign of `a`
alternating by parity of `N`, gives `delta_N` whose parity subsequences
converge exactly to `eps*(1,0)` (even `N`) and `eps*(-1,0)` (odd `N`), while
the whole sequence does not converge (consecutive `(a,b)`-distances grow
towards `4`, never shrinking to `0`).

- (a) `||rho_R(a_N,b_N)-P_R||_1 <= D=2eps(1+eps)/(1+eps^2)` (`=22/101`,
  `about 0.2178` at `eps=1/10`) holds at every one of the 12 sampled `N`
  (both parities), confirmed exactly.
- (b) The two subsequential limits `rho_even, rho_odd` each satisfy
  `||rho-P_R||_1<=D` (attaining about 91.4% of `D`), and differ from each
  other by `||rho_even-rho_odd||_1<=2D` while attaining about 90.9% of `2D`
  -- "up to the bound", not equal to it, but close.
- (c) `rho_even != rho_odd` and neither equals `P_R`, even though both lie
  in the **same** closed `D`-ball around `P_R`: a common enclosing interval
  is not equality.

**`two_d_independent.py`.** Rebuilds `D` (AV1 forward tier (ii):
`J=28|tau|`, `t1=49|tau|/144`, `T=t1/(1-352J)`, `eps=2T+T^2`,
`D=2eps(1+eps)/(1+eps^2)`) and `2D` from scratch with `Fractions`, and
confirms both equal, bit-for-bit, the exact rationals literally quoted in
the AY1 gate's `accepted` text (`D=585079838465912592144137406066050/
42981220507576537932303142777593983768257`,
`2D=1170159676931825184288274812132100/
42981220507576537932303142777593983768257`, decimal
`about 2.72249057405e-8`), and against the AY1 forward/reverse and the
original AV1 forward `output/results.json` exports (found at 7, 4 and 4
distinct JSON paths respectively, all bit-for-bit equal). The margin
`(1/1250000)/2D approx 29.38485839`, matching the reports' "about 29.38",
and the `tau=10^-8` vs `10^-10` scaling ratio `approx 100.0098` lies in
`[99,101]`.

## What failed

Nothing failed. All three scripts pass, and every cross-check against the
forward and reverse AY1 exports (and, for `two_d_independent.py`, the
original AV1 forward export and the AY1 gate text) passes.

Two implementation pitfalls were caught and fixed while writing this
package, worth recording since they are exactly the kind of silent error the
project's admission process is built to catch:

1. **Per-site sum is a per-GROUP tally, not a per-FACE tally.** A first
   draft of the maximal-per-site-sum check credited a retained face's norm
   only to the specific sites in *that face's own* owner set, giving at
   most `49|tau|/3 approx 16.33|tau|` (the "faces per site" count, used
   elsewhere for `t_1`) rather than AM2's actual definition
   `J=max_u sum_{b: u in X_b} ||phi_b||`, which credits each retained
   *group's* whole norm (`<=7|tau|`) to every site in its support. Fixed by
   crediting each anchor's total retained-face-count-based norm to every
   site in the union of its retained faces' owner sets; this reproduces
   `28|tau|` (attained) for both families, matching both producers exactly.
2. **`G(R)`/`G'(R)` must use the literal rational `8/7`, not a tighter
   independently-proved bound.** Plugging this script's own (tighter,
   12-term) exact bound on `exp(1/8)` into `G(t)` gives a strictly smaller,
   still-valid, but non-matching number. The forward/reverse chain
   deliberately plugs in the clean rational `8/7` to get the named
   `148/7`/`352`; this script now proves `exp(1/8)<8/7` independently
   (licensing the substitution) and then substitutes the literal `8/7`,
   exactly as assistant-3's `j0_contraction_replay.py` already did for the
   unrelated AX1/route-B `J_0'` constants.

## Agreement with the AY1 gate

Every number independently recomputed here (the 82/616/1344/2352 face
counts and the `28N(5N+1)` formula; `J_0=7/25000000`; `G(R)<148/7`,
`G'(R)<352`, the two contraction rationals `37/6250000` and `77/390625`;
termination order 8; the reset budget `98|tau|`; `D`, `2D` and the margin
`about 29.38`) **agrees exactly** with the AY1 gate
(`research/round32/advisor/ay1-gate.json`, verdict
`accepted_within_scope`, sub-label `uniform_local_closeness_not_uniqueness`)
and with both the forward and reverse AY1 producers' exported
`output/results.json`. No disagreement was found. This package adds, beyond
what the gate itself states: (i) an independent structural proof (not
merely a citation) that the AM2 nested-commutator terminates at exactly
`2p` for general `p`, confirmed at `p=4`; (ii) the anchor-level
full/partial/zero classification and the `N=4` extension of the box
enumeration, beyond the producers' `N=2,3`; (iii) an `mpmath` and a
`python-flint`/`Arb` cross-check of the one irrational step in the whole
AY1 chain; (iv) the small fixed-vector/moving-vector fixture requested by
the assignment, exhibiting the "common enclosing interval is not equality"
phenomenon concretely and exactly.

## Files

- `padding_family_contraction.py` -- independent box enumeration (`N=2,3,4`)
  of the F1/F2 padding families, the `28N(5N+1)` extra-face formula, the
  same-82-faces-meeting-`R` check, the maximal per-site sum `28|tau|`, the
  AM2 contraction inequalities (with `mpmath`/`Arb` cross-checks of
  `exp(1/8)<8/7`), the termination-order-8 structural fixture, and the
  reset budget `98|tau|`; cross-checked bit-for-bit against the forward and
  reverse AY1 exports.
- `fixed_versus_moving_vector.py` -- the tiny exact fixed-vector/moving-
  vector fixture (2 qubits, `Fractions`): the per-`N` density bound, two
  subsequential limits differing by up to `2D`, and "common enclosing
  interval is not equality".
- `two_d_independent.py` -- independent recomputation of `D`/`2D` from the
  AM2/AV1 tier-(ii) formula, checked bit-for-bit against the AY1 gate's
  quoted rationals and against the AY1/AV1 forward and reverse exports, plus
  the margin against `1/1250000` and the `tau`-scaling control.
- `results.json` -- combined pass/fail and full raw output from all three
  scripts.

## How to run

```bash
python3 -B research/round32/experts/historical/assistant-4/padding_family_contraction.py
python3 -B research/round32/experts/historical/assistant-4/fixed_versus_moving_vector.py
python3 -B research/round32/experts/historical/assistant-4/two_d_independent.py
```

Each script is standalone, prints its own JSON report to stdout, and exits 0
iff its `overall_pass` is `true`. All three were also run under
`python3 -B -O` and produced byte-identical stdout.
