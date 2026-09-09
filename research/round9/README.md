# Yang–Mills research: finite nonabelian models and proof obligations

Reviewed 9 September 2026. The four-dimensional Yang–Mills existence and mass-gap problem remains unsolved. This package contains finite-model derivations, exact counterexamples, implemented experiments and an independently challenged proof-obligation map. These are project replications and rederivations of mathematical mechanisms, with no claim of literature novelty.

## Read in this order

1. `advisor/advisor.md`: the full finite Haar identity hierarchy, uniqueness characterization, counterexamples, literature objections, conditional transfer stability and next proof obligations.
2. `lattice/MATHEMATICAL_CONTRACT.md` and `lattice/RESULTS.md`: actual four-dimensional SU(2) Wilson implementation, parameters, stochastic evidence and its limits.
3. `transfer/PROOF.md`: exact central-convolution spectrum, physical-time scaling and the distinction from a gauge-projected interacting transfer matrix.
4. `skeptic/REVIEW.md`: independent mathematical and source-level audit, found defects and retained failures.
5. `proof_results.json`: actual two-front search and separate certificate replay. No route in the admitted library reaches the Millennium target.
6. `integration-review.md`: checks performed on the integrated delivery and remaining limitations.

## Reproduce

Python 3.11+, NumPy, SciPy and Matplotlib are required. Decimal high-precision references use the standard library; SymPy and mpmath are not required.

```bash
python reproduce.py
```

This executes deterministic tests, exact spectral benchmarks, rational counterexamples, diagonal stability fixtures and the proof planner. It does not automatically repeat stochastic sampling. To inspect the original raw data and independently recompute its diagnostics from the full package:

```bash
python skeptic/audit_theorems_and_data.py
```

To run the finite lattice experiment again:

```bash
python lattice/test_lattice.py
python lattice/run_experiments.py
python lattice/plot_experiments.py
```

That is a fresh sampling run. Preserve a copy of the original package before overwriting output. The original run used six chains at beta=0,0.5,2.2, each with 512 warmup and 2048 measured sweeps. The beta=2.2 plaquette uncertainty and hot/cold comparison were **insufficient** because autocorrelation exceeded the preregistered threshold. Do not reinterpret them as passed mass-gap evidence.

## Two archive sizes

The full downloadable research artifact includes original raw CSVs, final configurations and rendered figures. The compact website download includes source, exact benchmark CSVs, aggregate lattice diagnostics, original manifests and proof/audit records; it omits bulky raw chain/one-plaquette histories, final configurations and PNG/SVG figures. Those omitted files are reproducible from the recorded seeds and can be inspected in the full artifact. `skeptic/audit_theorems_and_data.py` requires the full raw-data package and will reject missing data.

## Known scope boundaries

- SU(2) alone does not cover every compact simple group required by the prize.
- The finite complete Schwinger–Dyson family characterizes its Gibbs law; finitely sampled residuals do not supply that complete family.
- The group-convolution rotor spectrum is not a glueball spectrum. Independent endpoint gauge projection on a lone open link leaves constants only.
- Strong-coupling fixed-spacing theorems do not automatically reach the weak-coupling continuum trajectory.
- The conditional transfer bound requires a common Hilbert space, shared vacuum and a correct operator-norm estimate with physical-time scaling. These have not been established for a Yang–Mills renormalization comparison.
- No continuum quantum construction, uniform physical mass-gap bound or complete Einstein–QED closure is supplied.

The broader Physics Observatory retains earlier research, sources, guides and learning pages. Historical tests retain their historical labels; they were not all rerun in this round.
