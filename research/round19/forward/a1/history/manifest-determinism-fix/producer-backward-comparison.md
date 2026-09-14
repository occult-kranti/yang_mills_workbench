# Forward comparison to independent backward A1

The schema-mapped comparison passes: producer and backward evidence agree on the six clipped component types, all 44 phase-count fixtures, the alpha/8 local lower target, E_star scale separation and the Round18 coefficient-reclassification control.

The saved backward `compare.py` result against `forward/a1` is not used for gate review because that helper was written for the pre-contract producer schema and reports stale false negatives on renamed canonical fields. The independent backward `output/results.json` itself has status `passed`.

Remaining before A2 selection: advisor gate review of the producer evidence, backward evidence and this comparison.
