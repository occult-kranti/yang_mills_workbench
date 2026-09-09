# Round-6 regulator experiments

Run from the repository root:

```sh
python qeg-research/round6/experiments.py
```

The run writes `experiment_results.json` and three bounded graph datasets:

- `plot_data/finite_geometry.csv` records the exact continuous coefficient and analytic derivative samples.
- `plot_data/quadrature_refinement.csv` records 32, 64, 128, 256 and 512 point Gauss sums against independent adaptive integrals for `b=10,N=4,K=20`.
- `plot_data/tail_behavior.csv` records the fixed-matching full-window tail, with direct digamma rows separated from labeled log-domain asymptotic rows.

The continuous coefficient uses the primitive in E1 and the original density in the independent SciPy reference. The bounded matrix has 135 points over the contract's `b`, `N`, `K` and `a` values. The highest-resolution quadrature error is gated at `2e-10`; coarse errors remain in the results and are not hidden.

The two-node adversary is retained deliberately. At `b=10,N=0,K=20`, aligning a node with `a=K/sqrt(3)` produces a discrete coefficient larger than both its value at zero and the continuous maximum. At `K=200`, the same admissible positive quadrature gives a negative discrete `Z` at that node while the continuous integral remains positive. This rejects transferring the integral maximum theorem to arbitrary discrete grids. It is a grid failure in the finite approximation, not a physical instability or a QED Landau pole.

The Fraction gate reconstructs the exact E6 rational bound and cross-multiplies its strict inequality. The full-window formula is checked independently against a direct finite harmonic sum. The cofinal rows validate the finite E9 lower-bound examples; the asymptotic `log10(N+1)` rows never allocate a mode array or claim an exact threshold beyond floating range. The formal logarithm for the illustrative critical cutoff is a scale estimate only.

This is a finite mathematical coefficient study with fixed matching. It does not run an ODE, certify regulator removal, prove convergence of states or observables, or make a claim about continuum QED or physical instability. Imported round-4/round-5 contract files are hashed in the results; the experiment does not modify them.
