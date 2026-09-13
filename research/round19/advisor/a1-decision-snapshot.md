# Round19 A1 advisor decision snapshot

Decision: **accepted**.

This snapshot is the immutable advisor review record for `advisor/a1-gate.json`. It replaces no earlier feedback history. The earlier failed comparison remains recorded under `backward/a1/history/` and in the mutable advisor feedback log; the accepted gate relies on the repaired canonical evidence.

## Evidence reviewed

The canonical forward source is `forward/a1/check.py`. A fresh advisor replay of this executable reproduced the saved `results.json`, `component_templates.json`, `controls.json`, `phase_counts.csv` and `source-manifest.json` byte-for-byte. The optimized/replay comparison records identical normal, optimized and replay hashes, and verifies that the manifest binds both `check.py` and `report.md`.

The independent backward source is `backward/a1/check.py`, with source/evidence comparison in `backward/a1/compare.py`. A fresh advisor replay reproduced the saved backward `results.json` and final `comparison.json` byte-for-byte. The final comparison has status `accepted`, fourteen checks, zero mathematics failures and zero provenance failures.

## Mathematical result accepted

For the fixed infinite SU(2) rotor coefficient assignment in `contract-a1.json`, finite open boxes inherit coefficients face by face instead of waiting for complete strips. Across `n=2..12` and all four x-phase offsets, the only reachable selected clipped components are `L`, `M`, `R`, `LM`, `MR` and `LMR`. The forward and reverse implementations independently classify the phase domain and reconstruct the exact local bounds.

Proper clipped components use the free full-link reference and exact zero Haar means, giving

```text
Delta_S/alpha >= 3/4 - sum_{t in S} |c_t|/alpha.
```

The worst proper clipped components are `LM` and `MR`, each with lower estimate `1/8`. The complete `LMR` component uses the dressed-end bridge estimate

```text
Delta_LMR/alpha >= 3/4 - max(|lambda_L|, |lambda_R|)/alpha - |mu_M|/alpha >= 1/8.
```

The common physical scale is recorded with `E_star > 0`; `alpha/E_star`, `alpha_min/E_star`, coupling ratios, volume and phase are kept separate. The accepted result is a finite local boundary-consistent component theorem and its Gauss-sector passage after full-link uniqueness/gauge invariance. It does not prove thermodynamic spectral convergence, homogeneous dense stability, continuum Yang-Mills, or the Clay mass gap.

## Controls reviewed

The accepted comparison does not trust producer pass booleans alone. It checks source provenance, exact scale fields, all 44 phase pairs without duplicates, independently recomputed rational local bounds, independent phase fixture counts/edge counts/witness counts, stable restriction witness for face `(xy,4,0,0)`, altered-bound rejection and missing-phase rejection. Backward controls also reject zero or Boolean `E_star`, invalid phases, missing clipped components, missing zero-mean premise and common-scale withdrawal.

## Advisor consequence

A2 is now justified as a second Goal A loop, but only as a separate direct product-representation/summable-exception contract. The A1 gate does not complete the parent dense homogeneous goal.
