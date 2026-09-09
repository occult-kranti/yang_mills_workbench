# Locality branch — round 13

`locality.md` states and proves one conditional finite-spacing theorem for bounded gauge-invariant local observables on nested open Kogut–Susskind lattices. The result treats unbounded link Casimirs through a support-preserving interaction picture and uses a graph-independent plaquette-chain bound. It does not assert a ground-state gap or a continuum construction.

Run the exact standard-library diagnostics:

```bash
python3 locality_checks.py
python3 -O locality_checks.py --output output_optimized
```

`output/results.json` identifies the executed source SHA-256 and every gate. Four CSV files contain exact rational bound endpoints and separately labeled decimal display values. The script performs exact graph enumeration and bound diagnostics; it does not simulate the actual many-link evolution.

Optional figures require Matplotlib:

```bash
python3 plot_locality.py
```

The plot uses the recorded rational endpoints without adding a floor or replacing a missing result. `sources.json` records primary sources, exact versions, reading scope and transfer limits. Parent integration and the independent skeptic supply publication acceptance separately.
