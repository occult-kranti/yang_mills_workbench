# Manifest determinism repair history

The archived `output/` and `output-optimized/` directories contain the prior forward A1 generated evidence. Their `source-manifest.json` files were not acceptable for gate review because `check.py` originally emitted `report.md: null`; the saved manifest had then been repaired outside the generator. The current `check.py` now reads `report.md` during generation and emits the report hash deterministically.

`replay-output/` is a clean replay after the repair. It matches the canonical `output/` directory byte-for-byte for `results.json`, `component_templates.json`, `controls.json`, `phase_counts.csv` and `source-manifest.json`.
