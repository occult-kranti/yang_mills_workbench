# Round33 sub-round 2 -- modern (Penrose/Feynman) lens, assistant-2

Status: research assistant/coder cross-check tools for BB1/BB2, per the
task's instructions. **These outputs count zero research loops.** They are
previews and cross-checks only: `python-flint` (Arb ball arithmetic,
FLINT/Arb library), `mpmath.iv` (interval arithmetic) and `sympy` (symbolic
algebra) are independent, already-frozen open-source libraries, reused here
BY IMPORT (never reimplemented, never modified) for comparison and
computation, never for admission.
`research/round32/tools/arb_crosscheck.py`'s `arb_of`/`iv_of` helpers are
reused by import (a shared tool, not a producer `check.py`); **no producer
`check.py` file is ever imported or executed anywhere in this directory**
(none was even read, except by reading the `output/results.json` and
`report.md` files each frozen producer publishes, which is not the same
thing). Every number this repository actually admits for BB1/BB2 was
already decided by exact `fractions.Fraction` arithmetic in the frozen
`research/round33/{forward,reverse}/{bb1,bb2}/check.py` files, never opened
here -- only their `report.md` (for the closed-form formulas) and
`output/results.json` (for the admitted values, for comparison) are read,
together with `research/round33/contracts/{bb1,bb2}.json`, the BA1/BA2
gates, and `research/round33/experts/modern/bb-targets-proposal.md`.

Human project author: Hruday N M (BUNZEEY). Run everything with
`python3 -B` (also verified byte-identical under `python3 -B -O`).

## Files

- `bb1_arb.py` -- exact `Fraction` recomputation, from the closed-form
  formulas each BB1 report states, of both producers' headline `C`,
  `c_site`, the labelled secondary pair and the crude tier (both forward
  `polymer_kp` and reverse `iterated_split`); an Arb/mpmath rigorous
  enclosure of the one shared transcendental input both routes' constants
  ultimately rest on (`e^{1/8}<=8/7`, via `G(R)`, `G'(R)`); a check that the
  forward and reverse headlines agree to the reports' own quoted
  significant digits; and an exact recomputation of every `tau -> tau/100`
  scaling ratio. Self-test: PASS, 11/11 checks.
- `kp_condition.py` -- an independent, freshly-coded (never imported)
  finite-graph brute-force audit of the exploration-tree combinatorial
  lemma (report.md Lemma 4.1/4.2) the forward producer's Kotecky-Preiss
  hypothesis-verification (Proposition 6.2) depends on, on a 5-site chain
  of this script's own choosing; a numeric evaluation, at the forward's own
  declared headline/secondary parameters, of the two genuine KP
  admissibility margins (`a<=2b`, `v<=w`); an explicit statement that the
  KP series bound itself has zero slack by construction (`a:=tau_bar^2`,
  not a separately-derived quantity); and a finding on whether the forward
  report is self-contained on the Kotecky-Preiss consequence it uses (it is
  self-contained on Proposition 6.2, but not on the cited Theorem 6.1
  itself -- see the file's docstring and the note below). **This is a
  preview, not a proof**, and re-derives none of Kotecky-Preiss 1986 /
  Ueltschi 2004's own results. Self-test: PASS, 5/5 checks.
- `bb2_constants.py` -- exact and Arb recomputation of the BB2 state
  constants at the BB1 contract's frozen hypothesis values (forward
  `C'=(64/63)C_h=4/984375`, `c'=2/984375`; reverse `C'=C_h`, `c'=c_h`), of
  `C_dyn` from the admitted BA2 gate values (forward `2K_F1+K_cmp/4`;
  reverse per family `2K_F1`, `2K'_F2`), with an Arb/mpmath re-confirmation
  that the reverse route's rational `E_up(y)` dominates the true
  transcendental `E(y)=2(e^y-1-y)/y^2` at its working point; a `sympy`
  (with a from-scratch pointwise fallback if unavailable) symbolic proof of
  the identity `N^3-10N^2+28N+6 = N(N-5)^2+3N+6` behind the new lemma
  `(5N+1)(r_N-1)<=N^3/4` (`N>=5`), which gives a strictly simpler
  non-negativity argument than the report's own derivative-growth one; and
  a clearly labelled **preview, not a gate**, of the BB2 discharge --
  re-evaluating `C'` and `c'_site` at the BB1 PRODUCERS' own proved values
  (not the contract hypotheses) and reporting the resulting margins.
  Self-test: PASS, 6/6 checks.
- `sota_note.md` -- a short, citation-only placement of BB1/BB2 relative to
  the literature already recorded in
  `research/round33/experts/modern/sources.json` and the committed
  Nachtergaele-Sims excerpt; no scientific-priority claim; three concrete
  reading requests listed instead of any new source fetch.
- `results.json` -- combined machine-readable output of all three scripts'
  self-tests (`all_passed` plus every individual check, under `tools`).

```
python3 -B research/round33/experts/modern/assistant-2/bb1_arb.py
python3 -B research/round33/experts/modern/assistant-2/kp_condition.py
python3 -B research/round33/experts/modern/assistant-2/bb2_constants.py
```

All three exit 0 (PASS) as of this writing; each prints its own JSON report
and exits 1 on any failed sub-check. All three run in a few seconds and
were also verified under `python3 -B -O` (byte-identical output to the
`-B`-only run for all three files).

## Findings

### 1. `bb1_arb.py`

**Every exact rational recomputed here from the reports' own closed-form
formulas equals, exactly (not merely "contains" or "agrees to a few
digits"), the admitted exact rational in the matching producer's
`output/results.json`** -- headline `C` and `c_site`, the labelled
secondary pair, and the crude tier, for both the forward (`polymer_kp`) and
the reverse (`iterated_split`) route, both at the frozen `tau=10^-8` cap.
This was not obvious in advance: the forward route builds `C`, `c_site`
from a mixed-weight KP contraction (`tau_bar`, `kappa_0`, the lattice sums
`S_{2/3}=725`, `S_{1/2}=147`), while the reverse route builds them from a
completely different iterated product-ordering-split recursion (`t_0`,
`t_W`, `beta*`, the lattice sum `S_{1/8}=2169/343` for the headline weight,
`S_{1/2}=147` for the secondary weight) -- yet reconstructing each formula
independently from the reports' own stated equations, in fresh code, and
evaluating it in exact `Fraction` arithmetic reproduces every admitted
number bit-for-bit. The two routes' headline `C` (`8.90511999358e-7`
forward vs `8.90425620114e-7` reverse) and `c_site`
(`8.76811811767e-7` vs `8.76726764420e-7`) agree to 3 significant figures,
with the 4th-digit difference traced exactly to the route-dependent
Lipschitz-in-coefficients factor (`2(1+t)` for the forward's Lemma 2.4 vs
exactly `2`, `eta=0`, for the reverse's Lemma 1.3) -- a real, small,
already-expected difference between two independently proved upper bounds
on the same target, not a discrepancy. Both reports' own `tau -> tau/100`
scaling ratios (forward `~100.647875`/`~1.00150034`; reverse
`~100.638216785`/`~1.00150034215`) are reproduced from the same exact
formulas evaluated at `tau=10^-8` and `tau=10^-10`, with no intermediate
rounding. Arb (256-bit ball) and mpmath interval arithmetic, reused by
import, both confirm the shared `e^{1/8}<=8/7` directed-rounding bound
(`e^{1/8}~1.13315`, safely below `8/7~1.14286`) that both `G(R)<=148/7` and
`G'(R)<=352` rest on, and give a strictly tighter (irrational) independent
enclosure of each, contained inside the admitted rational bounds. No
discrepancy found anywhere in this file.

### 2. `kp_condition.py`

A fresh, independently coded (never imported) finite-graph enumeration on a
5-site chain of this script's own creation-vector norms (distinct from
either producer's own fixtures) confirms Lemma 4.1/4.2's structural claim
-- the sum, over every polymer through a marked site, of the product of
member norms is bounded by `sigma^2` (`sigma` the per-site mixed-weight
sum) -- with margin `~2.53` on this instance. At the forward's own real
declared parameters (`tau_bar~6.68e-7` headline, `~8.40e-6` secondary,
reproduced here exactly, matching `bb1_arb.py`), the two genuine KP
admissibility side-conditions have large margins (`a<=2b`: ~4.5e9
headline, ~2.8e7 secondary; `v<=w`: exactly `1.5` at both pairs), while the
KP series bound itself, `sigma^2<=a`, has **zero slack margin by
construction** -- the forward report defines `a:=tau_bar^2` exactly, so
reporting a numeric "margin" there would misrepresent a definitional
identity as a proved inequality with room to spare. **Self-containment
finding, as requested**: the forward report is self-contained on
**Proposition 6.2** (the verification that its own `a(.)`, `d(.)` satisfy
Theorem 6.1's hypothesis, proved in full from the report's own proved and
brute-force-audited Lemma 4.2), but is **not** self-contained on
**Theorem 6.1** itself (the abstract Kotecky-Preiss cluster-expansion
conclusion), which its own Attribution paragraph states is "cited, not
re-proved and not machine-checked; the primary sources were not
re-inspected in this session" -- and no excerpt of Kotecky-Preiss 1986 or
Ueltschi 2004 is committed anywhere under `research/round33/sources/`
(which holds only the Nachtergaele-Sims excerpt, used by BA2/BB2). This is
a preview and a finite-graph spot-check, not a re-derivation of
Kotecky-Preiss's or Ueltschi's own results, and not evidence for or against
the BB1 gate.

### 3. `bb2_constants.py`

The BB2 forward (`nested_telescoping`) and reverse (`union_comparison`)
state constants at the BB1 contract's frozen hypothesis values are
reproduced exactly: forward `C'=4/984375`, `c'_site=2/984375` (both
`(64/63)` times the BB1 hypothesis constant); reverse `C'=1/250000`,
`c'_site=1/500000` (assembly factor exactly 1 for nested centered cubes).
`C_dyn`, read from the admitted BA2 gate values, is reproduced exactly:
forward `2K_F1+K_cmp/4=78057/622883200000000`; reverse per family
`2K_F1=9261/77860400000000` (route `duhamel_inner_f1`) and
`2K'_F2=1055961408185869563/15240701171875000000000000000` (route
`duhamel_inner_f2`). Arb and mpmath, reused by import, independently
re-confirm the reverse BA2 route's own claim that its rational
`E_up(y)=1+y/3+y^2/(12(1-y/5))` dominates the true, transcendental
`E(y)=2(e^y-1-y)/y^2` at the working point `y=592704*10^-8`, reproducing
the reported `~6.88e-13` gap almost exactly. `sympy` confirms, symbolically,
the identity `N^3-10N^2+28N+6 = N(N-5)^2+3N+6` behind the new Lemma F08
`(5N+1)(r_N-1)<=N^3/4` (`N>=5`): since `N(N-5)^2>=0` and `3N+6>0` for every
`N>=0`, this identity gives a strictly simpler proof of the lemma than the
report's own `g(5)=21`-plus-derivative-growth argument (both are checked
here, and agree). **The BB2 discharge preview** (clearly labelled, not a
gate: neither BB2 producer may read a BB1 producer file under
`reverse_premise_isolation`/`conditional_on_bb1_targets`, so this
re-evaluation at the BB1 producers' own proved values -- both forward's and
reverse's, and the pointwise worse of the two -- is legitimately only
possible outside that isolation, from this lens) shows every combination
(forward/reverse BB1 input times nested-telescoping/union-comparison
assembly) meets both BB2 headline targets, with margins about `4.49x`
larger than the contract-hypothesis-value margins (`~11.05-11.23` for
`C'`, `~5.61-5.70` for `c'_site`, versus `~2.46`/`~2.50` at the hypothesis
values) -- exactly the ratio by which each BB1 producer's own proved
constant already beats its own `C<=1/250000` target. No discrepancy found.

### 4. `sota_note.md`

Places BB1's marginal-locality result next to the closest external
boundary-decay theorem on file (Yarotsky J. Stat. Phys. 118 (2005), read
only as a search summary) and next to the Kotecky-Preiss/Ueltschi cluster-
expansion machinery the forward producer's own polymer route builds on
(with the same "structure transfers, no constant transfers" finding this
lens's own `bb-targets-proposal.md` already recorded); places BB2's
`O(1/N)` correlation-function rate against the Nachtergaele-Sims committed
excerpt and against the *exponential*-clustering literature on file
(Nachtergaele-Sims math-ph/0506030, Hastings-Koma), explaining precisely
why that stronger rate does not apply here (this project's Lieb-Robinson
function `F(r)=(1+r)^-4` is polynomial, not exponentially weighted). No
scientific-priority claim is made anywhere in the note; three concrete
full-text reading requests are listed instead of fetching anything new.

## Scope note

Every check in this directory is a **comparison or a symbolic/numeric
re-derivation** of a quantity already admitted by a Round33 gate, already
published as an admitted `output/results.json` value, or already stated as
a closed-form formula in a frozen `report.md`. None of it is a research
loop, none of it is evidence, and none of it changes any BA1, BA2, BB1 or
BB2 verdict. The four-dimensional Yang-Mills existence and mass-gap problem
remains open.
