# Round33 sub-round 1 -- modern (Penrose/Feynman) lens, assistant-1

Status: research assistant/coder cross-check tools, per
`research/round33/experts/modern/loop2-response.md` section 3 (items 1-3).
**These outputs count zero research loops.** They are previews and
cross-checks only: `python-flint` (Arb ball arithmetic, FLINT/Arb library)
and `mpmath.iv` (interval arithmetic) are independent, already-frozen
open-source libraries, reused here BY IMPORT (never reimplemented, never
modified) for comparison and computation, never for admission.
`research/round32/tools/arb_crosscheck.py`'s `arb_of`/`iv_of` helpers are
reused by import (a shared tool, not a producer `check.py`); no producer
`check.py` file is ever imported anywhere in this directory, per
instruction. Every number this repository actually admits for BA1/BA2 was
already decided by exact `fractions.Fraction` arithmetic in the frozen
`research/round33/{forward,reverse}/{ba1,ba2}/check.py` files, which are
never opened or imported here -- only the ADMITTED `output/results.json`
files they produced, and `research/round33/advisor/{ba1,ba2}-gate.json`,
are read, for comparison. BB1 has **no** contract, loop or `check.py` in
this sub-round; `bb1_previews.py` reproduces an advisory preview
(`research/round33/experts/modern/bb-targets-proposal.md` section 7), not
an admitted result. Nothing in this directory is imported by any
`check.py`, and nothing here changes a verdict.

Human project author: Hruday N M (BUNZEEY). Run everything with
`python3 -B` (also verified under `python3 -B -O`).

## Files

- `weighted_contraction_arb.py` -- BA1 item 1 (loop2-response.md section 3.1):
  Arb/mpmath rigorous enclosures of the weighted contraction inequalities
  `J_0 w G(R) <= R` (self-map) and `J_0 w G'(R)` (Lipschitz constant), at
  the two weights BA1 actually certifies (`w=64` headline, `w=390625/148`
  floor); of the two analytic-disc radii `rho=64|tau|` and `rho=1/37888`
  used by the reverse route's Schwarz-lemma `K = 2 T(rho)`,
  `T(rho)=t_1(rho)/(1-28 rho G'(R))`; and a cross-read of
  `research/round33/advisor/ba1-gate.json` plus both producers'
  `output/results.json` headline/floor entries. Every admitted exact
  rational bound is confirmed to contain the independently (Arb ball /
  mpmath interval, both converted to *exact* rationals via their dyadic
  `man_exp()`/`_mpf_` representations, not decimal-string slack) computed
  value -- for the disc route, both from the admitted `G'(R)<=352`
  (reproducing the reverse's `K=49/111790368` and `K=49/2018304`
  byte-for-byte) and from the strictly tighter raw Arb/mpmath `e^{1/8}`
  ball (giving a numerically smaller, still-contained, independent value).
  Self-test: PASS, 10/10 checks.
- `ba2_directed_reconciliation.py` -- BA2 item 2 (loop2-response.md
  section 3.2): reproduces the admitted forward closed form
  `K_cmp = 254016 tau^2/(1-338688|tau|) = 3969/155720800000000` and the
  admitted reverse closed form
  `K'_cmp = 148176 tau^2 E_up(592704|tau|) = 452554889222515527/
  30481402343750000000000000000` exactly in `Fraction` arithmetic; encloses
  the never-admitted modern loop-1 preview
  `M = 3969 tau^2 theta^2 e^{127008|tau||theta|}` rigorously with Arb and
  mpmath; derives and checks the exact closed-form identity
  `M/K_cmp = e^x(1-x/3)` at `x=127008|tau||theta|=3969/390625` (both
  numbers share the same prefactor `254016 tau^2` and differ only in how
  they bound the Duhamel exponential remainder), confirming the BA2
  skeptic's recorded ~0.67% gap attribution
  (`research/round33/skeptic/ba2-independent-derivation.md` section 9);
  recomputes the exact `tau -> tau/100` ratios for both admitted routes
  (both fall inside the contract's `[9500,10500]` bracket); and checks the
  reverse producer's own `E_up(y) >= E(y)` claim at its working point with
  a rigorous Arb/mpmath enclosure of `E(y)=2(e^y-1-y)/y^2`. Self-test:
  PASS, 7/7 checks.
- `bb1_previews.py` -- BB1 item 3 (loop2-response.md section 3.3, targets
  from `research/round33/experts/modern/bb-targets-proposal.md` section 7):
  from the GATED BA1 constants only (`K_rev`, `K_fwd`, and BA1's own
  `T(rho)` tier-rule identity re-derived and cross-checked in
  `weighted_contraction_arb.py`), previews (labelled, not evidence) the
  BB1 marginal-locality constant `C` on both proposed routes -- iterated
  split (`C_split = 2(dbar_0+dbar_ez)(1+2 t_bar)(1+eta_str)`,
  `eta_str = 32 T_star/(1-32 T_star)`) and polymer/KP
  (`C_poly = 2(dbar_0+dbar_ez)(1+t_bar)(1+eta_far)`,
  `eta_far = e^{2a}*4T_KP*S(qW_c)/(1-4T_KP)`, `a=1/1000`) -- at `q=1/64`,
  with the far-support shell sum `S(x)=sum_{d>=1}(24d^2+8d+2)x^{-d}` summed
  in exact closed form and only `e^{2a}=e^{1/500}` enclosed with Arb/mpmath.
  Confirms the proposal's worst-case `C ~ 1.754e-6` (the split route on the
  reverse BA1 input) and the proposed `4x10^-6` target's margin `~2.28`,
  together with the proposal's own note that a `2x10^-6` target would have
  margin only `~1.14` ("do not freeze it"). Self-test: PASS, 8/8 checks.
- `results.json` -- combined machine-readable output of all three
  self-tests (`all_passed` plus every individual check, per file).

```
python3 -B research/round33/experts/modern/assistant-1/weighted_contraction_arb.py
python3 -B research/round33/experts/modern/assistant-1/ba2_directed_reconciliation.py
python3 -B research/round33/experts/modern/assistant-1/bb1_previews.py
```

All three exit 0 (PASS) as of this writing; each prints its own JSON report
and exits 1 on any failed sub-check. All three run in a few seconds and
were also verified under `python3 -B -O` (byte-identical pass/fail
outcome; the `-O` flag strips `assert` statements, none of which carry
side effects that the reported checks depend on).

## Findings

### 1. `weighted_contraction_arb.py`

The BA1 producers' own directed-rounding enclosure, `e^{1/8} <= 8/7`
(quoted verbatim in both `check.py` files' `exact_arithmetic_admission`
note), is confirmed valid by two independent rigorous computations: Arb
(256-bit ball, `1.13314845...+/-5e-77`) and mpmath interval arithmetic give
the same 16-digit value, both safely below `8/7 ~ 1.142857` (slack
`~0.0097`, i.e. `8/7` is a deliberately loose but perfectly safe bound).
Multiplying through by the admitted `G(R)=(37/2)e^{1/8}` and
`G'(R)=308e^{1/8}` reproduces the admitted `G(R)<=148/7` and `G'(R)<=352`
exactly when using the `8/7` bound, and gives a strictly tighter,
independently-computed value (`G(R)~20.963`, `G'(R)~349.01`, both below
the admitted `21.143`/`352`) when using the raw Arb/mpmath ball. Both the
weighted self-map/Lipschitz pair (`w=64`: `148/390625`, `2464/390625`;
`w=390625/148`: `1/64`, `77/296`) and the two analytic-disc `K` values
(`49/111790368` headline, `49/2018304` floor) are reproduced **exactly**
via BA1's own `T(rho)=49 rho/144/(1-28 rho G'(R))`, `K=2T(rho)` identity
when `G'(R)=352` is used, and are contained with margin when the tighter
Arb/mpmath `G'(R)` ball is used instead. A bonus check re-derives the
forward producer's own published `T_w` field
(`49/223580736` headline, `49/4036608` floor) exactly from the same
tier-rule identity with `w` in place of a disc radius -- an independent
confirmation that BA1's two routes (`analytic_disc`, `weighted_norm`) rest
on the same underlying self-consistency inequality. Reading
`research/round33/advisor/ba1-gate.json` and both producers'
`output/results.json` confirms all four admitted numbers (`49/111790368`,
`2734375/12204185915601`, `49/2018304`, `708203125/43148545682688`) appear
verbatim in the gate's `decision` text. No discrepancy found.

### 2. `ba2_directed_reconciliation.py`

The admitted forward (`3969/155720800000000`) and reverse
(`452554889222515527/30481402343750000000000000000`) BA2 dynamics-
comparison coefficients are reproduced exactly from their published closed
forms. The never-admitted modern loop-1 preview
(`3969 tau^2 theta^2 e^{127008|tau||theta|} ~ 2.566e-11`) is rigorously
enclosed with Arb and mpmath and matches the loop2-response.md
hand-evaluation to its quoted digits. **The 0.67% gap is confirmed and
independently re-derived**, not merely re-quoted: since the modern and
forward-admitted forms share the identical prefactor `254016 tau^2` and
differ only in which upper bound they use for the Duhamel exponential
remainder (`e^x-1-x <= (x^2/2)e^x` for modern, `<= (x^2/2)/(1-x/3)` for
forward/skeptic), the ratio reduces to the *exact* closed form
`M/K_cmp = e^x(1-x/3)` at `x=127008|tau||theta|=3969/390625`. Evaluating
this with Arb/mpmath gives `1.00679097 <= ratio <= 1.00679097` (both
libraries agree to the displayed digits), i.e. a `+0.6791%` gap -- matching
the BA2 skeptic's own reconciliation
(`research/round33/skeptic/ba2-independent-derivation.md` section 9:
`~1.0067939`, `+0.679%`/`0.675%`) to four significant figures, via a route
derived independently of that file (only its section-9 heading and figures
were read for comparison, not its derivation). The `tau -> tau/100`
ratios are reproduced exactly: forward `1953058850/194651 ~ 10033.644`,
reverse `38176688920663121234473000000/3810205403940325763421973 ~
10019.588` (this second value is the reverse producer's own report.md
quote for `K_cmp`'s own ratio; the BA2 skeptic's independent-derivation
table lists a slightly different `15624691300/1559413 ~ 10019.598`
labelled `"closed"` for a *combined* "reverse comparison and F2 Cauchy"
row -- a small, already-labelled and non-blocking distinction between two
different admitted quantities' ratios, not a discrepancy in either one).
Both ratios fall inside the contract's `[9500,10500]` bracket. Finally,
the reverse producer's own claim that its rational `E_up(y)` dominates the
true `E(y)=2(e^y-1-y)/y^2` at its working point `y=9261/1562500` is
confirmed with a rigorous Arb/mpmath enclosure of `E(y)`, reproducing the
reported `~7e-13` gap (`6.876e-13` computed here) almost exactly.

### 3. `bb1_previews.py`

BB1 has not been produced or gated in this sub-round; this file previews
`bb-targets-proposal.md` section 7's own numbers from the GATED BA1
constants, adding one independent Arb/mpmath enclosure (of `e^{2a}` in the
polymer route, the proposal's only transcendental quantity) that the
proposal itself did not carry a directed-rounding certificate for. All of
`t_bar=49/14398580736`, `T_star=49/4036608`, `eta_str=49/126095`, both
`C_split` values, the far-support shell sum
`S(390625/18944)=99977074261152768/51346528044814241`, and the
nested-telescoping `C'=50395032919/28283157234960930` are reproduced
**exactly** in `Fraction` arithmetic (`S` in particular sums to a closed
rational form via the standard `sum d r^d`/`sum d^2 r^d` geometric-
derivative identities, so no Arb enclosure is needed for it at all). The
polymer route's `eta_far` and `C_poly` values, which do need `e^{2a}`, are
rigorously enclosed and both agree with the proposal's quoted previews to
the quoted precision. **The proposal's headline claim is confirmed**: the
worst-case `C` over both routes on the reverse BA1 input (the split
route's `1.753963e-6`) is about `1.754e-6`, giving a margin of `~2.28`
against the proposed `4x10^-6` target -- and, as the proposal itself
flags, a `2x10^-6` target would have margin only `~1.14` (not technically
violated by this preview, but thin enough that the proposal is right to
decline freezing it). No discrepancy found; all reproduced numbers match
`bb-targets-proposal.md` to its own quoted precision.

## Scope note

Every check in this directory is a **comparison** (an independently
computed Arb ball, mpmath interval, or exact `Fraction` value found to lie
inside, or agree closely with, a number already admitted by a Round33 gate
or already published as a labelled advisory preview). None of it is a
research loop, none of it is evidence, and none of it changes any BA1, BA2
or (not-yet-existing) BB1 verdict. The four-dimensional Yang-Mills
existence and mass-gap problem remains open.
