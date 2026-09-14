# C2 clean-checkout admission repair

This is a reproducibility repair for the already accepted static C2 integral
theorem. It contributes **zero research loops** and no new physical theorem.
No Round19 or Round20 historical source, output, gate or manifest is edited.

## Preserved defect

The original command `python -B research/round19/reproduce.py --from-loop c2
--through c2 --output /tmp/fresh-c2-history` verifies every preceding gate before
running C2. It fails because the historical C2 gate lists
`backward/c2/history/pre-round20-validator-audit/__pycache__/compare.cpython-312.pyc`.
That untracked cache is absent from the repository. The other 294 distinct
historical file entries exist and match their hashes. Its original expected hash
is retained in the new inventory. Each repaired replay executes the old command
and requires precisely this failure before proceeding under the new admission.

The current comparator does not import the archived comparator or its cache.
Both archived Python source files remain bound. The exclusion is for this one
specific path in the **new** inventory; no blanket cache skip is permitted.

## New admission boundary

`build_inventory.py` generated a candidate, without admitting it or changing any
validator. Review verified the required C1 modules actually imported by C2, all
producer-declared scientific inputs, all expected output files, all six original
Round19 gates and the original replay specification. The union is 298 files.

The reviewed inventory SHA-256 is
`a3dbec14652f4b5b3c024fe8e9e125c5845fe410e0869178321fe333ee6c764b`.
That digest was pinned separately in `replay_c2.py`. Validation never regenerates
expected hashes. Deleting an inventory entry, changing an expected output hash
or modifying a scientific source cannot be made acceptable by a saved `passed`
flag. Symlinks are rejected at the inventory and every source path component.

This is a repository review trust anchor, not a digital signature or protection
against an adversary allowed to rewrite the validator and its review gate.
The Round21 advisor must bind the final repair code before admitting the release.

## Execution and arithmetic checks

Fresh C2 forward output matches all nine historical output files byte for byte;
the reverse output matches all eight. The independent comparator is executed
against the **fresh** forward output and freshly regenerates reverse evidence.
Every comparison field equals the historical comparison except its two absolute
path fields, which are checked against the actual input locations. This retains
34 comparison checks and 27 discriminating mutations. Both ordinary and
optimized Python replays pass; optimized re-execution adds no research loop.

The wrapper additionally reconstructs the exact degree-eight primary inequality
from Taylor coefficients using independent rational arithmetic. It checks the
zero endpoint coefficients, coefficient/moment factorial normalization, exact
exponential upper bound, positive numerator coefficient and the `1/2048` target
margin. It verifies semantic fixture inventories, strict Boolean types and the
static physical-scope statement. Acceptance is not inferred from exit status or
stored success flags alone.

The arithmetic still concerns
`F(kappa) >= kappa^2/2048` on `|kappa| <= 1/8`, with the separate certified
asymmetry range `0 < kappa <= 1/64`. Neither is a Hamiltonian gap or an energy/time
scale identification. A failed crude certificate at `1/6` does not falsify
positivity. These inherited inference boundaries must remain in later summaries.

## Reproduction

Run each command with a fresh output destination:

```bash
python -B research/round21/release/replay_c2.py --output /tmp/c2-review-normal
python -B -O research/round21/release/replay_c2.py --optimized --output /tmp/c2-review-optimized
python -B research/round21/release/test_admission.py --replay-minimal-checkout --output /tmp/c2-admission-controls.json
python -B -O research/round21/release/test_admission.py --output /tmp/c2-admission-controls-optimized.json
```

The full control command copies **only** the 298 admitted historical files and
the new wrapper/inventory into an isolated checkout, and executes C2 there. This
checks that the inventory covers actual execution dependencies and does not
rely on an ambient cache or unlisted file. Its directory is temporary; its full
replay metadata is saved in the control report.

Eighteen admission controls remove required scientific modules or coefficients,
alter an imported module, tamper with expected hashes or inventory completeness,
insert unsupported exclusions, substitute byte-identical symlinks, and forge
success metadata around an incorrect coefficient or Boolean count. Each must
produce an actual rejecting exception. They never mutate historical files.

## Limitations

Replaying exact arithmetic and checking source identity does not formalize the
written proof in a proof assistant or establish literature priority. The release
repair cannot strengthen C2's physical scope. It restores a reproducible route
to its existing evidence while preserving the original manifest defect.
