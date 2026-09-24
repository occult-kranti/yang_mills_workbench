# Round32 sub-round 5 -- modern (Penrose/Feynman) lens, assistant-5

Status: assistant/coder cross-check tools, per the sub-round-5 instruction
(panel-update-4 item 7, modern share). **These outputs count zero research
loops.** They are previews and cross-checks only: `numpy`/`scipy` and
python-flint 0.9 (Arb) are independent, already-frozen libraries reused
here BY IMPORT (never reimplemented, never modified) for comparison and
computation, never for admission. The Round11 `two_plaquette.py` solver
module (`research/round11/solver/two_plaquette.py`) and assistant-1's
`flint_harness.py` (a shared tool, not a producer `check.py`) are reused
by import; no producer `check.py` file is ever imported, per instruction.
Every number this repository actually admits for AZ2 was already decided
by exact `fractions.Fraction` arithmetic in the frozen
`research/round32/forward/az2/check.py`, which is never opened or
imported here -- only the ADMITTED `output/results.json` it produced is
read, for comparison. Nothing in this directory is imported by any
`check.py`, and nothing here changes a verdict.

Human project author: Hruday N M (BUNZEEY). Run everything with
`python3 -B`.

## Files

- `finite_graph_two_face_replay.py` -- item 1: an independent replay, at
  cutoff **D=10** (dimension 286, the Round11 two-plaquette graph's "other
  cutoff" beyond the AZ2 gate's own D in {6,8}), of the AZ2 TWO-FACE model
  `H_FG = K - tau_FG(W_1+W_2)`. Rayleigh-Schroedinger perturbation theory
  is carried out from scratch in exact `Fraction` arithmetic, order by
  order (via a regularized-solve deflation of `K`'s one-dimensional null
  space, proved correct here from `K`'s own zero row at index 0, not
  merely assumed), for the admitted two-face model AND, side by side
  (sharing the same regularized kernel, so `tp.solve_exact`'s
  multi-column back-substitution does the work of both models in one
  elimination per order), the skeptic's one-face alternative
  `H(lambda1=tau, lambda2=0)`. Also computes floating (`scipy.linalg.eigh`)
  and Arb (python-flint, one 256-bit inverse-iteration refinement step)
  **previews** -- explicitly NOT `exact_bracket`/`inertia`-based, and
  explicitly not using `tail_lower` -- of `<W_1>` at `tau_FG = +-1/100`,
  D=10, and one single measured `tp.inertia()` call at D=10 for runtime
  budgeting. Self-test: PASS (total wall-clock ~59 s).
- `calculator_records_vs_gates.py` -- item 2: for all 3 entries of
  `research/round32/advisor/calculators.json` (av2, aw2, ax2), verifies
  the `source` and `result_path` files are named in the loop's own gate
  `bindings` with matching live sha256, then checks every leaf value
  under the entry's `record_keys` against the gate's `accepted`+
  `decision` text and the skeptic's `admitted_values`, in three
  explicitly labelled tiers (verbatim substring; numeric-tolerant match,
  for a value reported at different decimal precision/rounding than the
  gate's own prose; and a documented benign-unmatched category for plain
  booleans and bare formula-constant labels). Also verifies all 6
  `research/round32/advisor/figures.json` entries point to existing files
  under `dist/`, and reports (there is nothing to check) that none of
  the six records a `sha256` field. Self-test: PASS.
- `claim_flag_sweep.py` -- item 3: scans all 15 producer `results.json`
  files across the ten Round32 loops (10 forward + 5 reverse, listed
  below) for every top-level boolean field, and checks the sub-round-5
  instruction's flag rules. Self-test: PASS, but **two rules hold only
  modulo a documented, gate-admitted exception each** -- see Findings.
- `results.json` -- combined machine-readable output of all three
  self-tests.

```
python3 -B research/round32/experts/modern/assistant-5/finite_graph_two_face_replay.py
python3 -B research/round32/experts/modern/assistant-5/calculator_records_vs_gates.py
python3 -B research/round32/experts/modern/assistant-5/claim_flag_sweep.py
```

All three exit 0 (PASS) as of this writing; each prints its own JSON
report and exits 1 on any failed sub-check. `calculator_records_vs_gates.py`
and `claim_flag_sweep.py` each run in a few seconds.
`finite_graph_two_face_replay.py` is the slow one, at about 59 seconds
total wall-clock (see the D=10 timing note below); no D=7 fallback was
needed.

## Findings

### 1. `finite_graph_two_face_replay.py` -- D=10 replay

**D=10 timing.** Matrix build (dimension 286) took about 5.5 s (run once
inside `rs_chain`, and again inside each of the two `wilson_preview`
calls and the `inertia` probe -- `tp.matrices` is `lru_cache`d, so only
the first call per process actually rebuilds). The three RS-order
regularized solves (`tp.solve_exact`, two models packed as two RHS
columns per call, sharing one `K_reg` elimination per order) took
**3.06 s, 3.07 s and 3.53 s** for orders 1, 2 and 3 respectively -- far
faster than `exact_bracket`/`inertia`, because it is a single Gaussian
elimination per order rather than a repeated bisection/inertia loop. The
two floating+Arb Wilson previews took about 0.02 s (scipy) + 1.9 s (Arb
inverse iteration) each. The **one measured `tp.inertia()` call at D=10
took 34.07 s** (a second run measured 32.87 s), matching assistant-4's
own extrapolation ("D=10 is roughly 34s per exact_bracket/inertia call")
almost exactly. Total wall-clock for the whole file: **~59 seconds**.
Because the RS-chain route needs no `inertia` calls at all (only three
fast `solve_exact` calls), and the floating/Arb previews needed none
either, **D=10 was comfortably feasible and no D=7 fallback was
needed** -- unlike a full `exact_bracket`-certification route (which
assistant-4 estimated, and this file's single `inertia` measurement
confirms, would cost several tens of seconds PER bracket call, and
several such calls per grid point).

**Exact D=10 results, all matching the admitted AZ2 gate and the
skeptic's independent one-face reading bit-for-bit:**

| quantity | two-face (admitted AZ2) | one-face (skeptic reading, `H(lambda1=tau,lambda2=0)`) |
|---|---|---|
| `a_1` = `d<W_1>/dtau_FG`\|₀ | **1/6** | **1/6** |
| `a_2` (second order, `<W_1>`) | **0** | **0** |
| `E_2` (second order, `E_0`) | **-1/6** | **-1/12** |
| `E_3` (third order, `E_0`) | **0** | **0** |
| `a_3` (third order, `<W_1>`) | **-187/33696** | **-5/864** |

Every one of these ten values is D-stable (identical to the admitted
D=6/D=8 values and the skeptic's independent derivation) at the new
cutoff D=10, confirming the AZ2 report's own claim that the truncation
error of these coefficients is exactly zero for `n<=5` (the polynomial
identity holds in the full space, not merely at the certified cutoffs).
The RS gauge condition `psi_0^T G psi_n = 0` (n=1,2,3) was verified to
hold live for both models at every order, not merely assumed -- a direct
consequence of `K`'s own row 0 being identically zero (`K*1=0` exactly),
proved and checked live in the script, not cited.

**Floating/Arb previews of `<W_1>` at `tau_FG = +-1/100`, D=10** (scipy
generalized `eigh` + one 256-bit Arb inverse-iteration refinement step;
explicitly labelled `preview_only:true`, `exact_bracket_used:false`,
`inertia_used:false`, `tail_lower_used:false`, `certifies_full_graph:
false`): `+1/100` gives `0.0016666611170769602`
(Arb ball mid `0.0016666611170769602`, radius `~1e-77`); `-1/100` gives
the exact negative. Both lie inside the AZ2 gate's own D=8 CERTIFIED
enclosure (`[416665279269240056001922924866860135632819/
250000000000000000000000000000000000000000000,
416665279269240056001922926278290019745987/
250000000000000000000000000000000000000000000]` at `+1/100`, and its
exact negation at `-1/100`) -- a numeric sanity comparison, not a proof,
since this file's own D=10 value is itself only a preview of the
truncated matrix, never a certificate.

**The assistant-4 caveat, honored explicitly.** Per the skeptic's
retained correction of the modern update-4/assistant-4 claims
(`research/round32/skeptic/az2.md` line 219 and
`az2-independent-derivation.md` lines 179, 217): `two_plaquette.
exact_bracket` certifies only the D-TRUNCATED matrix's own Ritz value,
never the full-graph value the AZ2 gate actually certifies, and it does
so WITHOUT using `tail_lower` at all. This file's own floating/Arb
previews make no stronger claim in the first place (they are not even
`exact_bracket`-based); every preview in this file's output carries the
explicit fields `exact_bracket_used:false`, `tail_lower_used:false`,
`certifies_full_graph:false`, and its docstring/caveat text repeats this
distinction verbatim so a later reader cannot mistake a preview here for
a certified enclosure.

### 2. `calculator_records_vs_gates.py`

All 3 `calculators.json` entries (av2, aw2, ax2): `source` and
`result_path` are both named in the loop's own gate `bindings`, and the
live sha256 of both files matches the recorded binding, for all three
entries. Of the values recorded under `record_keys`: av2 8/22 found
verbatim (1 benign unmatched: the boolean `True` for `target_met`), aw2
13/17 found verbatim (0 unmatched: `+tau/144`'s leading `+` sign is the
calculator's own display convention -- the unsigned form `tau/144`
appears verbatim in the gate text), ax2 17/25 found verbatim (1 benign
unmatched: the bare formula-constant label `2s^2` for `M2`, which the
gate's own condensed prose does not requote -- it appears in the
producer's `report.md`, not literally in the gate's `accepted`/
`decision` fields). The remaining values not found verbatim are all
found by a numeric-tolerant match (the gate's prose quotes a shorter,
outward-rounded decimal preview of the same exact value the calculator's
`results.json` reports at full precision -- e.g. `0.012446767091965986`
in the AV2 gate text against the calculator's own
`0.012446767091965985744835603912`). All 6 `figures.json` entries point
to existing files under `dist/`; none of the six records a `sha256`
field, so sha256 verification was not applicable to any of them.

### 3. `claim_flag_sweep.py`

15 producer `results.json` files were scanned (10 forward + 5 reverse:
av1, av2, aw1, aw2, ax1, ax2, ay1, ay2, az1, az2 forward; av1, av2, aw1,
ax1, ay1 reverse). Rules 3, 4 and 5 hold exactly as stated in the
instruction: `uniform_in_N_claimed` is true only for `forward/az1`, with
a nonempty scope string (`"volume-uniform at fixed a, strong bare
coupling"`); `model_is_finite_graph` is true only for `forward/az2`;
`euclidean_node_certified` is true only for `av2` (forward and reverse)
and `forward/ax2`.

**Two discrepancies from a literal reading of the instruction, both
genuine and both gate/contract-documented (not scan bugs, not
concerning):**

1. **`resolved_interaction_shift` is `true` in `forward/aw2/output/
   results.json`**, contradicting a literal "false wherever present"
   reading. This is explicitly required by the frozen AW2 contract
   (`research/round32/contracts/aw2.json`: `"...claim flags
   continuum_claim:false, uniform_wilson_claim:false,
   resolved_interaction_shift:true only if the exclusion holds at the
   cap..."`), admitted by the AW2 gate
   (`research/round32/advisor/aw2-gate.json`: `"...resolved_interaction_
   shift refers to omega(W) only..."`), and explained in the AW2 report
   (`forward/aw2/report.md` line 171: `"Accordingly
   resolved_interaction_shift:true is set, and only because the
   exclusion holds at the cap"`) and the skeptic's review
   (`skeptic/aw2.md` lines 157, 258). Scope: it certifies only that the
   static equal-time Wilson mean's SIGN is excluded from the free
   reference at the cap (`tau=10^-8`); sub-label `static_not_dynamic`;
   it is explicitly not a dynamical, mass-gap, susceptibility or
   centered-correlation claim, and all of THOSE remain false. This
   script's `rule1_must_be_false_wherever_present.documented_true_
   exceptions` records this exception explicitly rather than silently
   passing it or crashing on it.
2. **`uniform_wilson_claim` is `true` not only for AX1 (forward and
   reverse) but also for `forward/ax2`**, contradicting a literal
   "true only for AX1" reading. Also gate/report-documented, not a scan
   bug: AX2's own report states verbatim (`forward/ax2/report.md` line
   79) `"The flag uniform_wilson_claim:true means **only** that the
   model is the uniform fixed-spacing model as labelled"` -- the
   identical scope AX1's own report and gate use. AX1 and AX2 share the
   SAME uniform fixed-spacing Kogut-Susskind model label; the flag is a
   MODEL label, never a scientific-content claim (uniqueness,
   whole-sequence convergence, rate and a Wilson-mean sign certificate
   are separately, and correctly, flagged false for both). This script's
   `rule2_uniform_wilson_claim.true_but_beyond_instructions_AX1_only`
   records this exception explicitly.

No other field, in any of the 15 files, violates any of the five rules.
