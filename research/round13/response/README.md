# Scalar susceptibility benchmark

This directory studies the regular response of the finite measure
`dμ ∝ exp(κ x) sqrt(1−x²) dx`, with `x ∈ [−1,1]`.

The derived equation is `κ u′ + 3u = κ(1−u²)`, where `u′ = Var(x)` and
`u′(0)=1/4`. Read [response.md](response.md) for assumptions, proof, rejected
closures, initialization bounds, numerical results and the next obligations.

From this directory:

```bash
python3 -m pip install -r requirements.txt
python3 -B response_checks.py
python3 -B -O response_checks.py --output output_optimized
```

Each run performs 100 producer checks and writes JSON, CSV, PNG and SVG evidence.
The optimized run repeats the same scope and verifies that its gates survive
`python -O`. It does not create another 100 independent checks. Typical runtime
is a few seconds. Python 3.12.14, NumPy 2.3.5 and SciPy 1.17.0 were used for the
recorded run; the exact versions actually used are saved in `results.json`.

`initialization_bounds.json` contains exact rational bounds on the analytic
launch polynomial. The remaining ODE calculations use floating arithmetic and
provide numerical diagnostics, not certified endpoint intervals. The separate
round13 moments module supplies exact rational moment enclosures.

The Bessel comparison and the compact scalar equation are known identities used
as an independently reproducible benchmark. No novel solution of the
four-dimensional Yang–Mills problem is claimed.
