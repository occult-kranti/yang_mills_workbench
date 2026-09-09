# Reproducible numerical examples

`reproduce.py` contains three small, offline textbook benchmarks. They are numerical demonstrations, not replications of a source paper. The script uses SciPy's production algorithms and writes all output only to the directory named with `--output`.

```bash
python reproduce.py --experiment all --output ./example-output
# or: python reproduce.py --experiment oscillator --output ./oscillator-output
```

Install the packages listed in `requirements.txt` with `python -m pip install -r requirements.txt`. The script records the actual Python, NumPy, SciPy, and Matplotlib versions in `metrics.json`; no package version is assumed here.

The damped oscillator solves `x'' + 2γx' + ω₀²x = 0` with `solve_ivp` and compares displacement to the underdamped analytic solution. Length is metres, time seconds, and angular frequency radians per second.

The infinite quantum well discretizes `−ℏ²/(2m) d²/dx²` on a uniform 1D grid and calls `scipy.linalg.eigh_tridiagonal` for the lowest three energies. It compares grids with 100, 200, and 400 interior points to the analytic levels. Width is 1 nm, mass is the electron mass, and energies are eV in CSV/plots (the Hamiltonian is assembled in SI joules).

The diffusion example evolves a unit-amplitude mode `u(x,0)=sin(πx/L)` with homogeneous zero boundaries using a sparse finite-difference Laplacian and `scipy.sparse.linalg.expm_multiply`. Position is metres, time seconds, and the field is dimensionless. The exact continuum mode decay is `exp(−Dπ²t/L²)`. The numerical mode amplitude uses a discrete projection normalized by the initial mode’s squared norm.

Each experiment emits a CSV, a PNG, and the combined run emits `metrics.json`. Built-in physical checks fail with a nonzero exit status if solver error or well-grid convergence falls outside the expected threshold. Matplotlib uses the noninteractive `Agg` backend, and no network access is needed.
