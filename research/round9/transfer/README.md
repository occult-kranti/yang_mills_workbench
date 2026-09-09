# SU(2) transfer benchmark

This package proves and computes the spectrum of one normalized SU(2) central-convolution operator. It does not construct four-dimensional Yang–Mills or prove the Millennium mass gap.

Run:

```bash
python run_benchmark.py
```

Requirements: Python 3.11+, NumPy, SciPy, Matplotlib. An independent 80-digit reference uses Python's built-in Decimal; no SymPy or mpmath is required.

- `PROOF.md`: derivation, exact spectrum, scope, source reading ledger and missing bridges.
- `su2_transfer.py`: bounded numerical API, independent high-precision series and Haar quadrature.
- `run_benchmark.py`: 92 explicit acceptance gates and reproducible plots/data.
- `retained_failures.py`: executable records of two pre-freeze audit defects and their fixes.
- `output/validation.json`: evaluated checks, numerical examples, environment and source hashes.
- `output/su2_spectra.csv`, `output/su2-spectrum.png`: exact dimensionless rotor energies.
- `output/su2_joint_limits.csv`, `output/su2-joint-limits.png`: three time-scaling paths, showing why regulator positivity alone cannot select a physical continuum gap.

Numerical precision is tested, not interval certified. The full mathematical spectrum is positive for β>0; returned `ratio=None` indicates a value below floating range while its logarithm is retained. β=0 is a separately labeled exact projection. Negative β is accepted only by the explicit counterexample and direct quadrature interfaces.
