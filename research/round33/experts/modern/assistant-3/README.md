# Round33 sub-round 3 -- modern (Penrose/Feynman) lens, assistant-3

Status: research assistant/coder cross-check tools for BC2 (and the AX2 node
BC2 restates), per the task's instructions, mirroring
`research/round33/experts/modern/assistant-2/` from sub-round 2.
**These outputs count zero research loops.** They are previews and
cross-checks only: `python-flint` (Arb ball arithmetic, FLINT/Arb library)
and `mpmath.iv` (interval arithmetic) are independent, already-frozen
open-source libraries, reused here BY IMPORT (never reimplemented, never
modified) for comparison and computation, never for admission.
`research/round32/tools/arb_crosscheck.py`'s `arb_of`/`iv_of` helpers are
reused by import in `bc2_arb.py` (a shared tool, not a producer `check.py`);
**no producer `check.py` file is ever imported or executed anywhere in this
directory** (none was even read, except by reading the `output/results.json`
and `report.md` files each frozen producer publishes, which is not the same
thing). `research/round33/forward/bd*` and `research/round33/reverse/bd1`
(in production) were never read by anything in this directory. Every number
this repository actually admits for BC2 was already decided by exact
`fractions.Fraction` arithmetic in the frozen
`research/round33/forward/bc2/check.py`, never opened here -- only its
`report.md` (for the closed-form formulas) and `output/results.json` (for
the admitted values, for comparison) are read, together with
`research/round33/contracts/{bc1,bc2}.json`, the BC1/BC2 gates, the Round32
AX1/AX2 gates and `research/round32/forward/ax2/report.md`/`calculator.py`
(read as declared premises, never imported or executed), and this lens's own
`research/round33/experts/modern/bc2-targets-proposal.md`.

Human project author: Hruday N M (BUNZEEY). Run everything with
`python3 -B` (also verified byte-identical under `python3 -B -O`).

## Files

- `bc2_arb.py` -- exact `Fraction` recomputation, from the closed-form
  formulas `research/round33/forward/bc2/report.md` states, of every BC2
  route-B constant: `T_B(rho)=(52 rho/144)/(1-10208 rho)`,
  `K_B=2T_B(64|tau|)`, the split closure `t_0`, `t_W`, `c1`, `c2`, `beta*`,
  the closed-form `S_lambda` at `x=1/8`, `c_site,B=K_B(2+beta* S_lambda)`,
  `C_B=c_site,B(1+q)`, and the `C'_B`, `c'_site,B` union-comparison assembly
  (factor 1); an Arb (256-bit ball)/mpmath.iv independent re-evaluation of
  every one of those same formulas over a wholly different numeric code
  path, checking the admitted exact rational lies inside each ball/interval;
  an exact recomputation of the `tau -> tau/100` scaling ratios; and a
  reconciliation against this lens's own `bc2-targets-proposal.md` Section
  10 previews, with any difference reported explicitly. Self-test: PASS,
  9/9 checks.
- `admissibility.py` -- exact and Arb checks of the route-B disc self-map
  and contraction `29 rho G(R)<=1/64`, `29 rho G'(R)<1` at the headline disc
  `rho=64|tau|` and at the split-weight disc `rho=1024|tau|`; the route-B
  maximal disc radius `7/274688` and the resulting maximal admissible split
  weight `2734375/1073` at the cap; and the rejection of the route-A
  extremes (`29/1792 > 1/64`, with a further check that route A's own
  per-site coefficient 28 makes that same radius exactly saturate route A's
  own `q=1/64`, which is why the BA1/BB1 producers chose it, and why route
  B's larger per-site sum pushes it just outside admissibility). Self-test:
  PASS, 5/5 checks.
- `node_replay.py` -- the computation behind `node_replay_note.md`: `D'` and
  `k'=51|tau|/4` re-derived fresh from the AX1 gate's own stated formula and
  the route-B incidence on `R` (never imported from any calculator or
  `check.py`); the AX2 gate's radius formula
  `r=2(D'+D'^2)+51|tau|s/pi+arithmetic_half_width` recomputed with Arb's own
  built-in `pi()` and `exp()` routines (independent of the admitted
  calculator's own hand-written Machin/Taylor Python brackets) at 256-bit
  precision, rounded outward on the gate's own `10^-40` grid; and a
  bit-for-bit check that BC2's own admitted `datum`, `radius_R_prime` and
  `D_prime` fields equal the AX1/AX2 gate rationals. Self-test: PASS, 6/6
  checks (`R_prime_recomputed_with_arb_and_slack_to_gate` finds slack
  exactly `0`).
- `node_replay_note.md` -- the write-up of `node_replay.py`'s findings: what
  was recomputed and how, the (zero) slack against the gate `R'`, an
  explicit answer to "does the BC2 restatement change any number" (no), and
  a clarification that BC1 restates a *different* Round32 radius (the AV2
  gate's `R`, for the zero-selected model) than the one this note recomputes
  (the AX2 gate's `R'`, for the uniform route-B model BC2 restates).
- `results.json` -- combined machine-readable output of all three scripts'
  self-tests (`all_passed` plus every individual check, under `tools`).

```
python3 -B research/round33/experts/modern/assistant-3/bc2_arb.py
python3 -B research/round33/experts/modern/assistant-3/admissibility.py
python3 -B research/round33/experts/modern/assistant-3/node_replay.py
```

All three exit 0 (PASS) as of this writing; each prints its own JSON report
and exits 1 on any failed sub-check. All three run in a few seconds and were
also verified under `python3 -B -O` (byte-identical output to the `-B`-only
run for all three files).

## Findings

### 1. `bc2_arb.py`

**Every exact rational this script recomputes from the BC2 report's own
closed-form formulas equals, exactly, the admitted exact rational in
`research/round33/forward/bc2/output/results.json`** -- `K_B=13/27941256`,
`t_0=13/1799816256`, `t_W=26/3148137`, `c1`, `c2`, `beta*`,
`S_lambda=2169/343`,
`C_B=2326328761843649826272217312701707175/2461302090348550272620124432958434944821248`
and
`c_site,B=35789673259133074250341804810795495/38457845161696098009689444264975546012832`,
and the union-comparison `C'_B=C_B`, `c'_site,B=c_site,B`. Arb (256-bit
ball) and mpmath interval arithmetic, applied to the same formulas through a
wholly different arithmetic code path (directed-rounding ball/interval
division and multiplication, never `fractions.Fraction`), contain every one
of these admitted rationals; because every BC2 route-B constant except the
shared `e^{1/8}<=8/7` input is purely rational in `tau` (BC2 uses the
already-rational bounds `G(R)=148/7`, `G'(R)=352` throughout, never
re-deriving them), the Arb/mpmath balls have essentially zero width at 256
bits, so containment is a strong, non-trivial cross-check of the algebra
transcription, not merely a numeric coincidence. The one place a genuine
transcendental enters is confirmed separately: Arb and mpmath both
re-confirm `e^{1/8}<=8/7` (the same directed-rounding bound BA1/BB1/AM2 use)
and the resulting tighter irrational enclosures of `G(R)`, `G'(R)` sit
inside the admitted rational bounds `148/7`, `352`, exactly as
`assistant-2/bb1_arb.py` already found for the zero-selected model's
analogous quantities.

**Reconciliation with this lens's own `bc2-targets-proposal.md` Section 10:**
no difference found. Every constant this script recomputes was already
previewed there, as the identical exact fraction: `K_B` in Section 10.2;
`t_0`, `t_W`, and the `iterated_split` column's `C_B`, `c_site,B` fractions
in Section 10.3 (verbatim substrings of the proposal file, checked directly);
the admissibility numbers of Section 10.1 (see `admissibility.py` below);
the `tau -> tau/100` scaling ratios of Section 10.7. The proposal's Section
10.3 also lists a `polymer_kp` preview column
(`C_B~9.452589e-7`, `c_site,B~9.307164e-7`); the BC2 contract requires
`iterated_split` only (`polymer_kp` needs a committed Ueltschi excerpt as a
declared premise, which is not present), so the producer used
`iterated_split` and the `polymer_kp` column was never exercised -- an
unused labelled alternative route, not a discrepancy.

### 2. `admissibility.py`

Every admissibility inequality the BC2 report states in Section 0
(`HNM-BC2-F01`, `HNM-BC2-F02`) is reproduced exactly, in both `Fraction` and
independent Arb-ball arithmetic: the headline disc self-map
`1073/2734375<1/64` and contraction `2552/390625<1` at `rho=64|tau|`; the
split-weight disc self-map `17168/2734375<1/64` and contraction
`40832/390625<1` at `rho=1024|tau|`; the route-B maximal disc radius
`rho_max=7/274688` and the resulting maximal admissible split weight
`W_max=2734375/1073` at the cap (`1024<=2548.35`, so `W=1024` is admissible
with room to spare); and the rejection of the route-A extremes, which both
reduce to `29*(148/7)/37888=29/1792>28/1792=1/64`. One extra fact this
script adds, not stated as such in the BC2 report: route A's *own* per-site
coefficient is 28, not 29, and `28*(148/7)/37888` equals `1/64` **exactly**
-- so `tau_star=1/37888` is precisely the radius at which route A's own disc
self-map saturates route A's own rate `q=1/64` (which is presumably why the
BA1/BB1 producers chose that radius), and route B's larger per-site sum
`J'=29|tau|` pushes the very same radius just outside admissibility, by
exactly the factor `29/28`. No discrepancy with the admitted values or with
this lens's own Section 10.1 previews.

### 3. `node_replay.py` / `node_replay_note.md`

`D'` and `k'=51|tau|/4` are re-derived fresh from the AX1 gate's own stated
formula and the route-B incidence on `R` (7 stars, 2 single groups), never
imported from `research/round32/forward/ax2/calculator.py` or any
`check.py`, and match the pinned gate rationals exactly. The AX2 gate's
radius formula `r=2(D'+D'^2)+51|tau|s/pi+arithmetic_half_width` is then
recomputed with Arb's own built-in `pi()` and `exp()` routines at 256-bit
precision -- a numerically independent path from the calculator's own
hand-written Machin-series and alternating-exponential Python brackets --
and rounded outward on the gate's own `10^-40` grid. **The result,
`R'_own=1912298807996871790146581299723633/10^40`, is identical, digit for
digit, to the admitted AX2 gate `R'`: the slack is exactly `0`**, tighter
than the BC2 forward report's own labelled cross-check (which used its own
`10^-60`-precision Machin/series brackets and found a small nonzero slack
`~2.7e-41`, still a valid but looser bound). This is a comparison, not a
tighter admission: the gate's `R'` is not superseded, and `node_values_unchanged`
still requires exact equality, never a re-derived headline. **The BC2
restatement changes no number**: BC2's own admitted `datum`, `radius_R_prime`
and `D_prime` fields equal the AX1/AX2 gate rationals bit for bit, confirmed
directly from `research/round33/forward/bc2/output/results.json`. One
clarification recorded in the note: BC1 restates a *different* Round32
radius (the AV2 gate's `R=1831967503411879425147166810021607/10^40`, for the
zero-selected model) than the one this note recomputes (the AX2 gate's `R'`,
for the uniform route-B model BC2 restates) -- close in magnitude, not the
same certificate, and never cross-applied.

## Scope note

Every check in this directory is a **comparison or an independent
re-derivation** of a quantity already stated as a closed-form formula in a
frozen `report.md`, already admitted by a Round32 or Round33 gate, or
already published as an admitted `output/results.json` value. None of it is
a research loop, none of it is evidence, and none of it changes any BA1,
BA2, BB1, BB2, AX1, AX2, BC1 or BC2 verdict. The four-dimensional Yang-Mills
existence and mass-gap problem remains open.
