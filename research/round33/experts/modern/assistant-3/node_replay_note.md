# The AX2 node radius R', recomputed with Arb, without importing the calculator

Round33 sub-round 3, modern (Penrose/Feynman) lens, research assistant/coder
"assistant-3". **This note counts zero research loops. It admits nothing and
is not a contract, a premise or a gate.** The computation behind it is
`node_replay.py` in this folder (`python3 -B node_replay.py`, self-test PASS,
6/6 checks, byte-identical under `-B -O`). `research/round32/forward/ax2/calculator.py`
is a declared BC2 shared premise and is read here as text, for the formula it
implements, exactly as the BC2 forward report itself does (it too "replays"
the calculator and then gives its own independently-coded cross-check); it
is never imported and never executed by anything in this folder.
`python-flint` (Arb ball arithmetic) is reused by import, as an independent,
already-frozen open-source library, exactly as
`research/round32/tools/arb_crosscheck.py` reuses it (that frozen Round32
tool is itself reused by import elsewhere in this folder, never modified).

## What was recomputed, and how

The AX2 gate (`research/round32/advisor/ax2-gate.json`, `accepted`) states
the radius formula in prose:

> `r=2(D'+D'^2)+51|tau|s/pi^- plus the arithmetic half-width 1/(4*10^40)`

with `D'` the AX1 gate forward tier-(ii) state bound and `s=1`, `|tau|=10^-8`
the single certified node. This note recomputes `r` from that stated formula
in three independent steps, none of which imports the calculator:

1. **`D'` re-derived from the AX1 gate's own stated formula** (not copied
   from the gate's decimal, not imported from any `check.py` or
   `calculator.py`): `J'=29|tau|`, `t_1'=52|tau|/144`, `T'=t_1'/(1-352J')`,
   `eps=2T'+T'^2`, `D'=2 eps(1+eps)/(1+eps^2)`. In exact `Fraction`
   arithmetic this equals the pinned gate rational
   `2425369125199104794263242601250/167893028420061547330293754713793182097`
   (`~1.44459e-8`) bit for bit (`node_replay.py`,
   `D_prime_rederived_from_ax1_gate_formula`).
2. **`k'=51|tau|/4` re-derived from the route-B incidence on `R`**: 7 whole
   stars of weight 7 and 2 single-factor groups of weight 1 on the cover
   `R={0,e_z}`, so `B_N/|tau|=(7*7+2*1)/8=51/8` in `G=H/alpha` units, and
   `k'=2*B_N/|tau|=51/4` (`k_prime_rederived_from_route_b_incidence`),
   matching the AX2 gate's own stated `k'=51|tau|/4`.
3. **The transcendental parts, `1/pi` and `exp(-3s)/4`, enclosed with Arb's
   own built-in `pi()` and `exp()` routines** (`flint.arb.pi()`,
   `flint.arb(...).exp()`) at 256-bit working precision (about 77 decimal
   digits) -- a wholly different numeric code path from the admitted
   calculator's own hand-written Machin-series and alternating-exponential
   Python brackets (`research/round32/forward/av2/calculator.py`'s routines,
   reused unchanged by the AX2 calculator). At 256 bits the resulting ball
   widths are about `10^-77` for `pi` and about `10^-79` for `exp(-3)`
   (`pi_enclosure_arb_builtin`, `exp_minus_3_over_4_enclosure_arb_builtin`),
   far tighter than the `10^-40` grid the gate rounds on.

Combining these with exact `Fraction` arithmetic for the rational parts
gives a rigorous bracket `[radius_lo, radius_hi]` for
`r=2(D'+D'^2)+51|tau|s/pi+arithmetic_half_width` (the "arithmetic
half-width" being half the width of the rigorous `exp(-3s)/4` bracket, the
same role the gate's own `1/(4*10^40)` plays), and `R'_own = up(radius_hi)`
rounds the upper end outward to the nearest `1/10^40`, exactly the gate's
own outward-rounding convention.

## Result: slack is exactly zero

At 256-bit precision, the two Arb enclosures are so much tighter than the
`10^-40` target grid that outward-rounding `radius_hi` to that grid gives

```
R'_own = 1912298807996871790146581299723633/10^40
```

**identical, digit for digit, to the admitted AX2 gate rational**
`R'=1912298807996871790146581299723633/10^40` (`~1.912298808e-7`). The slack
`R'_own - R'` is exactly `0` (`R_prime_recomputed_with_arb_and_slack_to_gate`),
not merely small: at 256 bits, both the calculator's own outward-rounded
Taylor/Machin brackets and this script's Arb brackets resolve the true real
number `r` to far more than 40 correct decimal digits, so both round outward
to the same 40-digit rational. This is a stronger form of the BC2 forward
report's own labelled cross-check in `research/round33/forward/bc2/report.md`
Section 5 (`node_own_reevaluation_cross_check`), which used its own Machin
`pi` and its own `e^{-3}` series bracket rounded outward on `10^-60` and
found a nonzero slack of about `2.7e-41` against the gate `R'` (a valid but
looser bound, because a `10^-60`-precision Taylor bracket for a
transcription of the SAME formula still carries a small excess over the
gate's own `10^-40`-precision bracket at the last retained digit). Using
Arb's built-in routines at 256 bits removes essentially all of that excess,
so the two outward-rounded values coincide exactly.

**This is a comparison, not a tighter admission.** The gate's own `R'` is
not superseded, revised or reproved by this coincidence; `node_values_unchanged`
(BC2's own control) and `certificate_values_unchanged` (BC1's own control)
both require every restated node datum and radius to equal the gate rational
exactly, never a re-derived value "smaller or larger" as the headline, and
this note changes nothing about that rule.

## Does the BC2 restatement change any number? No.

`research/round33/forward/bc2/report.md` Section 5 states the node
certificate for the limit `omega^B_inf` with

```
d = 497870683678639429793424156500617766317/(4*10^40)   (unchanged from AV2/AX2)
R' = 1912298807996871790146581299723633/10^40             (unchanged from AX2)
```

read by hash from the pinned AX2 gate, and its own admitted
`node_replay_equals_ax2_gate` check requires the admitted calculator, replayed
at its fixed design, to return these two rationals (and the recomputed AX1
`D'`) exactly. This note's independent check
(`bc2_restatement_changes_no_number`) confirms, from the admitted
`research/round33/forward/bc2/output/results.json`, that the BC2 packet's own
`datum`, `radius_R_prime` and `D_prime` fields equal `d`, `R'` and the AX1
gate `D'` respectively, bit for bit. So: **the BC2 restatement changes no
number.** It supplies a new *identification* (the limit of the route-B named
construction `FB` is, on every finite region, an AQ1-type subsequential
state of the AX1 construction, so the certificate proved "for every such
state, each separately" applies to the limit with the same constants), never
a new datum, radius or state bound. The only new arithmetic in BC2 Section 5
is a *labelled cross-check* (its own Machin-pi, own `e^{-3}` bracket,
`r_own<=R'` with slack `~2.7e-41`), explicitly not the headline value.

**One clarification, not a discrepancy.** BC1 (`research/round33/forward/bc1/report.md`)
restates a *different* Round32 radius for the zero-selected model's node: the
AV2 gate radius `R=1831967503411879425147166810021607/10^40`
(`~1.83196750341e-7`), not the AX2 `R'` this note recomputes. The two are
close in magnitude but are not the same number and are not restatements of
each other: `R` is the AV2 (zero-selected, patterned-family) certificate's
radius; `R'` is the AX2 (uniform, route-B) certificate's radius, formed from
the AX1 route-B `D'` and the route-B slope `k'=51|tau|/4` (versus AV2's own
zero-selected inputs). BC2's `route_b_not_restated`-style controls (and BC1's
own `route_b_not_restated`) keep the two node certificates from being
cross-applied; this note only recomputes `R'`, the one BC2 restates.

## Scope

This is a numeric cross-check of one closed-form formula already stated in
two admitted Round32 gates and replayed unchanged in an admitted Round33
report. It admits nothing, decides nothing, and changes no verdict. The
four-dimensional Yang-Mills existence and mass-gap problem remains open.
