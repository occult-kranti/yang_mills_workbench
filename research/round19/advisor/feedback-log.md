# Round19 advisor feedback log

## A1 first failed comparison preserved

At head `e62886d4cf724557c1884d11e5579bae94e28fcb`, the first independent A1 comparison delivered a real failed result: `research/round19/backward/a1/comparison/comparison.json` has status `producer-incomplete-under-frozen-v1.1`. The rejected producer evidence was the exploratory pre-contract output and omitted the explicit `E_star` register plus all four x phases required by `contract-a1.json` v1.1. This failure is retained as feedback history and is not an A1 acceptance.

## Current advisor blockers

- Canonical forward A1 evidence now includes the missing `E_star` scale register and 44 phase fixtures, but it still needs a revised independent comparison against its canonical schema.
- The first comparator is too shallow for positive admission: exact parsed scale, complete phase-domain checks, independent rational bound reconstruction and mutation controls are required.
- A forward rerun reproduced the scientific outputs but not `source-manifest.json`; the executable writes `report.md: null` while the saved manifest contains a report hash.
- A2 remains unfrozen. The constructive product-representation route should only be contracted after A1 acceptance and after deciding that its domain/essential-spectrum obligations are feasible.


## 2026-09-13 A2 closure, manifest refresh and B1 watch

A2 is accepted on the corrected final source/output/comparison bytes. A through-A2 replay found stale advisor bindings for `backward/a2/report.md` and `backward/a2/manifest.json`; the reverse manifest was corrected to `ym19-backward-a2-manifest-v5`, and the advisor preserved the prior gate at `advisor/a2-gate-history-before-manifest-v5-refresh-c15c6e6c0593.json` before refreshing `advisor/a2-gate.json`, `advisor/a2-source-bound-inventory.json` and the post-A dependency inventory. The accepted A2 mathematical result did not change.

Current A2 gate SHA-256: `80c1dc9add22e4d042155017202534fc8ff5e977a445e655d6ada1d90726efe9`.

B1 is now executing under `advisor/contract-b1.json` with no B2 contract frozen. The main advisor watch item is complete exclusion of all physical channels below the strict `E_el < 6 alpha` cutoff. Workers must enumerate four- and six-edge fundamental cycles, but also prove that branching/mixed-spin supports cannot slip below the cutoff. A selected simple-cycle list is not sufficient.
