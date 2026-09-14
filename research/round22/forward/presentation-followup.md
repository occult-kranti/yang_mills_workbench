# Presentation repair follow-up

No concrete implementation blocker remains from the bounded presentation
review. This follow-up adds zero research loops and changes no scientific
submission or shared source. The full ten-loop build, generated-data tests,
Pages synchronization and browser layout audit remain unperformed here.

## Reviewed repairs

- **Historical navigation:** `dist/research-round22.js:48–52` now supplies
  `round21-contributions`, translates generic home/contribution/journey links
  inside archived content, and keeps current-return links outside that
  translation. Delegated Round21 pages receive the same treatment. Lines
  57–60 clean up the old journey and set historical alias titles directly.
  The actual archived renderers pass the new navigation checks.
- **Executed handlers:** the new block at `tests/test_round22.mjs:54–96`
  runs `afterRender`, chapter focus and both motion preferences, preserves
  the application hash, checks initial/input/change calculator readouts,
  verifies the historical title and exercises cleanup/delegation. I executed
  that exact block against the current `dist` renderer and real Round21/
  journey renderer files: it passed. The unused Round22 scientific-data
  load in this isolated fixture was replaced in memory with an empty
  object; this was not a generated release-data or full-suite run.
- **Gate comparisons:** test lines 34–37 now hash actual gate-file content
  and compare status, claim, scope, equations, target verdict, next premise
  and independence. Isolated checks using the eight existing admitted gates
  passed, and sixteen deliberately altered claim/hash cases rejected.
  Final generated-data equality still awaits the ten-loop build.
- **Shared validation:** both builders now call `loop_metadata` from
  `presentation_schema.py`, which requires nonempty prose and at least
  three nonempty string steps. `build_site.py:26` also validates exactly
  three distinct, unexecuted future goals. The eight concrete rejection
  controls in `release/check_presentation_schema.py` passed in fresh normal
  and optimized runs. Their outputs were byte-identical and matched the
  existing `presentation-schema-checks.json` exactly.
- **Small concurrent additions:** the calculator explicitly states C=1,
  matching its evaluator. The horizontally scrolling model table is now a
  labelled, focusable region. Neither change alters a scientific claim.

Evidence URLs deliberately remain repository paths on `main`, with exact
gate hashes and inventories identifying the reviewed bytes. Immutable-commit
URLs are not claimed. This documented provenance choice is not treated as
an outstanding implementation defect.

## Reviewed bytes and remaining release work

| File | SHA256 |
|---|---|
| dist/research-round22.js | 9e2b305f8257bf87b2bd5a2ff0738cdfbc752d4dfd5976e6bb731da6274db900 |
| tests/test_round22.mjs | 431959d157e97012af187946d4eef9bc9a12156a18b3871795031a55999f402e |
| research/round22/presentation_schema.py | d137ae1b69440eb87cd14e97659e699e89b0456090628e1b6cf52f72a03f6680 |
| research/round22/release/presentation-schema-checks.json | 75cce4cbce9c35d5b8eec673a48d1f33f27483e139aa5a1040db50c56b2f8dcd |

At inspection, the repair record matched its other six changed-source
hashes but retained the renderer hash from before the C=1/table-region
additions. The advisor acknowledged this and will refresh that record to
the reviewed renderer hash above. This is remaining release bookkeeping,
not evidence that the current renderer failed a check.

After the final scientific admission, execute the full builders and Node
suite on the real ten-loop data and synchronized assets, as already planned.
This follow-up does not count those pending checks as passed. Frozen R1
remains unchanged; no R2 work was performed.
