# Round19 advisor feedback log

## A1 first failed comparison preserved

At head `e62886d4cf724557c1884d11e5579bae94e28fcb`, the first independent A1 comparison delivered a real failed result: `research/round19/backward/a1/comparison/comparison.json` has status `producer-incomplete-under-frozen-v1.1`. The rejected producer evidence was the exploratory pre-contract output and omitted the explicit `E_star` register plus all four x phases required by `contract-a1.json` v1.1. This failure is retained as feedback history and is not an A1 acceptance.

## Current advisor blockers

- Canonical forward A1 evidence now includes the missing `E_star` scale register and 44 phase fixtures, but it still needs a revised independent comparison against its canonical schema.
- The first comparator is too shallow for positive admission: exact parsed scale, complete phase-domain checks, independent rational bound reconstruction and mutation controls are required.
- A forward rerun reproduced the scientific outputs but not `source-manifest.json`; the executable writes `report.md: null` while the saved manifest contains a report hash.
- A2 remains unfrozen. The constructive product-representation route should only be contracted after A1 acceptance and after deciding that its domain/essential-spectrum obligations are feasible.
