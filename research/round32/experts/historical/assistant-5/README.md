# Historical lens (Newton/Tesla) assistant scripts -- Round32 sub-round 5

Human project author: **Hruday N M (BUNZEEY)**. AI-assisted assistant scripts for the
Newton/Tesla historical lens, delivering the historical share of the two scripted
tests requested in `research/round32/advisor/panel-update-4.md` item 7: an
independent replay of the eleven AZ1 dictionary identities, the cap, the
toy-trajectory crossover indices and the lattice-unit floor (test 1), and a
whole-round consistency sweep of every contract, gate, producer export and
skeptic verdict across all ten Round32 loops (test 2, the "whole-round sweep
of every contract's control mirror, every gate's fields and every
results.json claim flag" named in the panel update). These scripts and this
note count **zero research loops**: they are cross-checks and previews for
the lens, not a producer, skeptic or advisor artifact, and nothing here is
admission evidence. Nothing here reads or imports any producer `check.py`,
any reverse `check.py`, or any skeptic `*_check.py`/`*_postreview_check.py`;
every identity, hash and table entry is re-derived or recomputed in this
package's own code from the frozen contracts, gates and the producers'
exported `output/results.json` (data, never code).

Everything numeric that decides pass/fail is `fractions.Fraction`, plain
`int`, or exact string/value equality (`hashlib.sha256` for the binding
check); no floats appear in any pass/fail comparison anywhere in this
package. `mpmath` (arbitrary-precision float) and `python-flint`'s `Arb`
(verified ball arithmetic) are used only as explicitly labelled numerical
cross-checks of the one irrational input in the whole package -- `sqrt(6)`
in the lattice-unit floor -- never as the bound itself and never in a
pass/fail comparison.

Read before writing: `research/round32/advisor/panel-update-4.md` item 7,
`research/round32/advisor/az1-gate.json` and `research/round32/forward/az1/
report.md` (frozen and gated), `research/round32/forward/az1/output/
results.json` (data only) and its `headline`, `research/round32/contracts/
az1.json`; for the sweep, `research/round32/contracts/<loop>.json`,
`research/round32/advisor/<loop>-gate.json`, every producer's
`research/round32/{forward,reverse}/<loop>/output/results.json`, and
`research/round32/skeptic/<loop>.json` for all ten loops AV1..AZ2, plus
`research/round32/advisor/admission-spec.json` and `research/round32/
advisor/findings.json`; and this lens's `assistant-4/README.md`,
`results.json` for this package's layout and `results.json`/README
conventions.

Run every script with `python3 -B <script>.py` (also confirmed byte-identical
under `python3 -B -O <script>.py` for both scripts, and byte-identical on
repeated plain reruns).

## What passed

Both scripts pass (`overall_pass: true` in each, and in the combined
`results.json`).

### `dictionary_replay.py`

Independently verifies, by **two separate routes**, exactly the eleven
identities the AZ1 gate binds and headline lists (`alpha/16=g^2/(32a)`,
`tau=96/g^4`, `alpha*lambda*a^2=1`, `r=4/g^4`, `alpha*tau/24=lambda`,
`(alpha/8)*(tau/3)=lambda`, `7*tau=672/g^4`, `tau/144=2/(3g^4)`,
`(alpha/8)/2=g^2/(32a)`, `a*alpha/16=g^2/32`, `tau*g^4=96`):

- **Route A (Fractions).** All eleven identities, plus the two rescaling
  invariances, are checked as exact `fractions.Fraction` equalities on an
  independent 5x7 grid of `(a,g)` values (`a` in `{2/5,3,17,1/9,250}`, `g`
  in `{1/3,2,9,1234,5/7,777,1/1000}`, none of them the AZ1 forward check's
  own grid values) crossed with two independent rescaling factors `c`
  (`{7/3,11}`) -- 245 identity evaluations in all -- and all hold exactly.
- **Route B (rational-function identity).** A small multivariate
  integer-polynomial dict class is written from scratch in this file
  (never imported from any producer) over the Laurent-cleared variables
  `u=g^2`, `a` and `c`; `alpha`, `lambda`, `tau`, `r` and the gap are each
  represented as an honest `num_poly/den_poly` ratio, and every identity is
  checked by literal integer cross-multiplication
  (`LHS_num*RHS_den == RHS_num*LHS_den`, coefficient by coefficient) --
  true for *every* value of the variables, not merely at sampled points.
  `tau` and `r` are not merely asserted equal to `96/g^4` and `4/g^4`; they
  are *derived* here from the AL1 primary definitions
  (`tau=24*lambda/alpha`, `r=lambda/alpha`) and then cross-multiplied
  against those literal targets, so the derivation itself is replayed, not
  only its consequence. The rescaling invariances (`alpha(ca)=alpha(a)/c`,
  `lambda(ca)=lambda(a)/c`, `gap(ca)=gap(a)/c`, `tau(ca)=tau(a)` recomputed
  through the *rescaled* `alpha`/`lambda` ratio rather than asserted, and
  `r(c*alpha,c*lambda)=r`) are checked the same way. All 17 Route-B checks
  (11 identities + `tau`/`r` derivations + 5 rescalings, less the one
  identity duplicate) pass.
- **The cap.** `g^4=96/tau` at `tau=1/10^8` gives exactly `9600000000`,
  matching the AZ1 headline's `g4_at_cap`.
- **The toy-trajectory crossovers**, independently, by **two integer
  methods** (no floats, no `Fraction` -- every target/threshold pair here
  is already an exact `int`): (i) an integer fourth root via two nested
  `math.isqrt` calls (`isqrt(isqrt(n))`) with an exact correction loop,
  used to seed a bounded local search on the exact integer inequality
  `n**4*threshold > target`, and (ii) an independent direct linear scan
  `n=1,2,...` checking that same exact inequality. Both methods agree with
  each other and reproduce the AZ1 gate's four indices exactly: `g_0^4=
  9.6x10^9` gives `n*=2` (cap) and `n*=132` (AL1 bridge `g^4>=32`);
  `g_0=1000` gives `n*=4` and `n*=421`.
- **The lattice-unit floor** `a*Delta>=g^2/32>=1250*sqrt(6)`. `a*Delta=
  g^2/32` is itself identity 10 (`a*alpha/16=g^2/32`, since `Delta=
  alpha/16` at fixed `a`). An independently constructed directed
  (rounded-down) rational lower bound for `sqrt(6)`, built from
  `math.isqrt(6*10^80)` (a floor, hence certified as a lower bound, never
  an upper one, and checked rigorously as an exact `Fraction` inequality
  `bound^2<=6`, not merely numerically), gives `1250*sqrt(6)_lower =
  24494897427831780981972840747058913919659/
  8000000000000000000000000000000000000` (decimal preview
  `3061.8621784789725`), matching the AZ1 headline's own directed value
  `19595917942265424785578272597647131/
  6400000000000000000000000000000` (decimal `3061.86217847897...`) to the
  precision both report; the two fractions need not be bit-identical
  (different precision `k` was used to build each), only both independently
  certified valid lower bounds for the same irrational target, which they
  are. Also confirmed exactly: at the admitted-regime boundary
  `g^4=9600000000`, `(g^2/32)^2=g^4/1024=9375000` exactly (an integer),
  which is exactly `1250^2*6`, so the floor is attained (not merely
  approached) at that boundary. `mpmath` (60 decimal digits) and
  `python-flint`'s `Arb` (200-bit verified ball arithmetic) independently
  confirm `sqrt(6)~=2.449489742783178...` and `1250*sqrt(6)~=
  3061.862178478972...`, both labelled previews only.
- **Cross-checks against the AZ1 gate.** The eleven-identity list, the cap,
  all four crossover indices, and both directed-lower-bound properties of
  the lattice floor match the AZ1 forward `output/results.json` `headline`
  bit-for-bit (identity list, `g4_at_cap`, all four `n*` values); the exact
  `n*` values and the `1250*sqrt(6)`/cap wording are also confirmed present
  literally in the gate's `decision` and `accepted` text.

### `round_consistency_sweep.py`

For all ten Round32 loops (AV1, AV2, AW1, AW2, AX1, AX2, AY1, AY2, AZ1,
AZ2), reads `research/round32/contracts/<loop>.json`,
`research/round32/advisor/<loop>-gate.json`, every producer's
`output/results.json` (`forward` for all ten; `reverse` additionally for
AV1, AV2, AW1, AX1, AY1, matching each loop's own `producers` list in
`admission-spec.json`), and `research/round32/skeptic/<loop>.json`, and
checks:

| # | check | result |
|---|---|---|
| (a) | gate `verdict` and `accepted` text equal `admission-spec.json` and `findings.json` entries | **10/10 pass**, both fields, both cross-references |
| (b) | every claim flag in the admission spec's per-direction `claims` dict equals the producer `results.json` value | **all 15 direction-entries, every flag, pass** (0 mismatches) |
| (c) | every `results.json` has `continuum_claim`, `scientific_priority_verified`, `resolved_interaction_shift` all `false` | **1 documented exception**: `forward/aw2/output/results.json` has `resolved_interaction_shift: true` -- see "What failed / discrepancies" below; every other of the 15 producer exports across all ten loops has all three flags `false` |
| (d) | contract `preregistration.controls_required.ids` equals contract `controls` | **1 documented exception**: AV2's `controls` (24 ids) contains `c1_window_preview_only`, absent from `controls_required.ids` (23 ids); all other nine loops match exactly, list-for-list |
| (e) | every gate's `bindings` sha256 hashes match the working tree | **913/913 bindings checked across all ten gates, 0 mismatches, 0 missing files** |
| (f) | sub-labels used in gates are in that loop's contract `preregistration.sub_labels_allowed` | **10/10 pass**: AZ1's `sub_label` is `null` (reported explicitly, not treated as a failure); AY1/AY2 carry `uniform_local_closeness_not_uniqueness`; AZ2 carries `sign_certified_finite_graph`; AY2 and AZ2 additionally carry `secondary_sub_labels: ["static_not_dynamic"]`; every one of these five distinct labels is in the (identical, five-entry) `sub_labels_allowed` list every one of the ten contracts carries under `preregistration`; the top-level `contract.sub_labels_allowed` field is `null` in all ten contracts (noted, not a defect: the operative list lives only under `preregistration`) |
| (g) | gate `sequence` runs 1..10 in loop order, `subround==(sequence+1)//2` | **10/10 pass**: AV1/AV2 sequence 1/2 subround 1, AW1/AW2 sequence 3/4 subround 2, AX1/AX2 sequence 5/6 subround 3, AY1/AY2 sequence 7/8 subround 4, AZ1/AZ2 sequence 9/10 subround 5 |

Bonus (read, not required by the six lettered checks): every skeptic
`verdict` (`research/round32/skeptic/<loop>.json`) matches its gate's
`verdict` -- `accepted_within_scope` for all ten, both files, for all ten
loops.

The script's own `overall_pass` requires every row to pass **and** that
every mismatch anywhere in the sweep be exactly one of the two documented
exceptions below (the same style `research/round32/skeptic/av2_check.py`
itself already uses for the AV2 case:
`need(set(contract['controls'])-set(mirror)=={'c1_window_preview_only'}, ...)`)
-- a sanity test (run once, with the exception allowlists emptied in a
throwaway copy, then discarded) confirmed the script does correctly fail
(`overall_pass: false`, 2 unexpected mismatches reported) when the two
known exceptions are not allow-listed, so the pass is not vacuous.

## What failed / discrepancies found

Nothing in this package's own arithmetic failed: both scripts pass, and
every cross-check against the AZ1 gate and the whole-round record passes.
The sweep did surface, and correctly classify, the round's own **two
pre-existing, non-blocking discrepancies** -- both already known and
recorded in the round itself, neither introduced by this package, and
both explicitly out of scope for repair here (historical rounds, gates and
frozen contracts are immutable per `AGENTS.md`):

1. **AW2's `resolved_interaction_shift` is `true`, not `false`.** Task
   item (c) as literally worded expects `false` in every `results.json`;
   AW2 (`Hruday sign-certified enclosure of the Wilson mean at the AW1-frozen
   coupling`) is precisely the loop that *does* certify a sign for the
   interaction shift, and the AW2 gate's own `admission-spec.json` entry
   independently lists `resolved_interaction_shift: true` in its `claims`
   dict -- so this is not a bug, and check (b) (claims match the admission
   spec) passes for it cleanly; it is only a counterexample to the flat
   universal wording of item (c) taken alone, and the sweep script reports
   it explicitly as a `documented_exception` rather than silently passing
   or silently failing.
2. **AV2's contract has a pre-registration mirror gap.** `contracts/
   av2.json`'s `controls` list has 24 entries; its
   `preregistration.controls_required.ids` has only 23, omitting
   `c1_window_preview_only` (the C^1 calculator-preview control, contract
   item 10 / `new_control_semantics.c1_window_preview_only`). This is the
   AV2 gate's own already-recorded "non-blocking clerical defect": both AV2
   producers implemented the control anyway (`forward/av2/check.py:916`,
   `reverse/av2/check.py:1404`, both present in their `output/results.json`
   `checks`), the frozen contract is deliberately not amended per
   `AGENTS.md`'s immutability rule, and `freeze_contract.py` was updated
   after this freeze to reject such a mismatch going forward (see
   `research/round32/advisor/av2-gate.json`, `research/round32/advisor/
   admission-spec.json`, `research/round32/skeptic/av2.md`,
   `research/round32/skeptic/av2_check.py`, `research/round32/advisor/
   panel-update-1.md`, and the Jung lens's own
   `research/round32/experts/jung/assistant-1/README.md` and
   `results.json`, which first found it in sub-round 1). This package's
   sweep re-finds and reports it independently from the contract JSON
   directly (not by reading any of those prior notes' prose), confirming
   the gap is still exactly, and only, `c1_window_preview_only`.

No other mismatch of any kind (verdict, accepted text, claim flag, binding
hash, sub-label, sequence/subround) was found anywhere across all ten
loops, both directions where applicable, and all 913 hash-bound files.

## Agreement with the AZ1 gate and the whole round

Every number `dictionary_replay.py` independently recomputes -- the eleven
identities (both by exact `Fraction` grid and by integer polynomial
cross-multiplication, with `tau` and `r` *derived*, not assumed), the cap
`g^4=9600000000`, all four toy-trajectory crossover indices (`n*=2, 132`
for `g_0^4=9.6x10^9`; `n*=4, 421` for `g_0=1000`, each by two independent
integer methods), the lattice-unit floor `1250*sqrt(6)~=3061.862...`
(independently bracketed, and shown attained exactly at the boundary), and
the five rescaling invariances -- **agrees exactly** with the AZ1 gate
(`research/round32/advisor/az1-gate.json`, verdict `accepted_within_scope`,
`sub_label: null`) and with the AZ1 forward producer's exported `headline`.
`round_consistency_sweep.py` confirms the whole round's ten gates,
contracts, producer exports and skeptic verdicts are mutually consistent
end to end, up to the two pre-existing, already-documented, non-blocking
exceptions listed above, both of which the sweep detects, names precisely,
and cross-references to the round's own prior record rather than treating
as new findings.

## Files

- `dictionary_replay.py` -- independent replay of the eleven AZ1 dictionary
  identities (Fraction grid + integer polynomial cross-multiplication,
  with `tau`/`r` derived from the AL1 primary definitions), the cap
  `g^4=9600000000`, the four toy-trajectory crossover indices (integer
  fourth root via `isqrt` twice, plus an independent direct scan), the
  lattice-unit floor `a*Delta>=g^2/32>=1250*sqrt(6)` (directed `sqrt(6)`
  bracket via `isqrt`, `mpmath`/`Arb` cross-checked previews only), and the
  five rescaling invariances; cross-checked bit-for-bit / textually against
  the AZ1 gate and forward export.
- `round_consistency_sweep.py` -- whole-round sweep of all ten Round32
  loops' contracts, gates, producer exports and skeptic verdicts against
  `admission-spec.json` and `findings.json`, emitting a per-loop pass/fail
  table for checks (a)-(g) plus a bonus skeptic-verdict cross-check, and
  classifying the two pre-existing documented exceptions found.
- `results.json` -- combined pass/fail and full raw output from both
  scripts.

## How to run

```bash
python3 -B research/round32/experts/historical/assistant-5/dictionary_replay.py
python3 -B research/round32/experts/historical/assistant-5/round_consistency_sweep.py
```

Each script is standalone, prints its own JSON report to stdout (and, for
`round_consistency_sweep.py`, the human-readable table also to stderr),
and exits 0 iff its `overall_pass` is `true`. Both were also run under
`python3 -B -O` and produced byte-identical stdout, and re-run twice
produced byte-identical stdout both plain and under `-O`.
