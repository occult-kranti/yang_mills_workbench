# Reproducible mathematical companions

These standalone Python calculators reproduce selected equations and scalar
certificate arithmetic from the Yang–Mills workbench. They are a paper companion,
not a replacement for the original proofs or its full 293-state heat solver.
No network access or repository checkout is needed after dependencies are installed.

All source references are pinned to repository commit
`40960f39a3dcaa6b2735d47adaa0e3b40e6a0f02`.
`source_data/source_manifest.json` records exact source paths, URLs and SHA-256
hashes. `source_data/heat_scalar_inputs.json` contains the small scalar inputs
extracted from the original output; no untracked research dependency is imported.

## Install and run

Use Python 3.11 or later (tested with Python 3.12).

```bash
cd calculators
python -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python ym_calculators.py --help
python test_calculators.py --output output/test-results.json
python -O test_calculators.py --output output/test-results-optimized.json
python run_examples.py
python make_figures.py --output ../figures
```

The final command writes five publication figure pages, their individual PDF and
PNG files, curve CSVs, captions and hashes. `network.pdf` is a separate optional
inventory chart; `network_structure.pdf` draws all 158 nodes and 260 directed
edges from the actual audited schema. Their grouping layout has no physical
metric meaning. `figure_atlas.pdf` contains the five primary figure pages.

The calculator emits JSON to stdout or to `--output`. Decimal inputs such as
`0.01` and fraction strings such as `1/100` are supported. Global options
`--precision` and `--output` precede the subcommand. Each subcommand has `--help`.

```bash
python ym_calculators.py --output output/jacobi.json jacobi --ratio 10 --alpha 1 --dimension 24 --refine
python ym_calculators.py --output output/static.json static --kappa 2 --moments 6
python ym_calculators.py --output output/series.json series --degree 7 --epsilon 1/100
python ym_calculators.py --output output/window.json window --q 999/1000 --eta 1/2 --ell 1 --beta 1/2 --gamma 1
python ym_calculators.py --output output/gaussian.json filter --kind gaussian --M 35/1664 --duration 4 --omega 0
python ym_calculators.py --output output/triangle.json filter --kind triangle --M 1/1000 --duration 3 --omega 1/10
python ym_calculators.py --output output/wilson.json wilson --z 1/1000000
python ym_calculators.py --output output/heat.json heat --cap 1/100 --eta 1/100 --sigma 13/5
python ym_calculators.py --output output/heat-certificates.json heat-certificates
```

For fixed support use `window --L 2`. Omitting `--L` uses
`L=max(1,floor(ell*(1-q)^(-beta)))`; at `beta=0`, this correctly retains the
integer floor of `ell`.

## Precision, exact arithmetic and scope

Fraction-valued JSON strings are exact rational arithmetic. Decimal-valued
diagnostics use mpmath at 70 working decimal digits by default, configurable
from 30 to 200. A working precision is not an interval accuracy guarantee.
Plot rendering converts reviewed curve values to binary floats; accompanying
CSVs retain the high-precision values used to produce the curves.

The Python API initializes mpmath to at least 70 digits at import and exposes
`configure_precision(digits=70)` to explicitly set its process-wide context.
The CLI uses the same 70-digit default. Downstream arithmetic performed by the
caller is subject to the caller's current precision. For example:

```python
import ym_calculators as ym
ym.configure_precision(80)
budget = ym.filter_budget("triangle", "1/1000", "3", "0")
print(budget["operator_residual_over_r_rational_upper"])  # 2072/2997
```

| Command | Quantity and domain | Evidence class and limits |
|---|---|---|
| `jacobi` | Character compression: diagonal `alpha*n*(n+2)+lambda`, neighboring entries `-lambda/2`; `alpha>0`, `lambda/alpha>=0`, `2<=N<=160` | High-precision finite matrix diagnostic. The optional `N` to `2N` comparison is not a tail enclosure. The inherited gap floor `0.999999*alpha` applies only to `0<=lambda/alpha<=10` and is not proved by this code. |
| `static` | `Z=2 I1(kappa)/kappa`, `u=I2/I1`, with exact removable-origin values; normalized Haar moments | Numerical Bessel versus independent quadrature checks. Static `kappa` is not a time-generator coupling. No floating ODE trajectory is certified. |
| `series` | Odd local regular response polynomial, exact residual and launch bound, `0<epsilon<=1/2` | Rational coefficients and a sufficient nonnegativity witness. The resulting bound controls only the local launch value. |
| `window` | `B(q)`, `tau`, complete tail-cube budget, state and dynamical terms; `0<q,eta<1` | High-precision evaluation of source-proved upper-bound formulas. Strict sufficient support/time region is `beta<1`, `gamma<3(1-beta)`. Failing it does not prove actual nonconvergence. |
| `filter` | Gaussian origin source (three crossing stars) or triangle translated family (twelve); `0<=M<=35/1664`, positive duration | Conservative source residual bound is rational. Triangle weighted finiteness is reported only when `192*M*T<1`. `M=0` is an exact zero-source exception; no residual/source ratio is reported. No exact inverse or weighted contraction is inferred. |
| `wilson` | Actual multiplier endpoint formulas and moment/norm distinctions, `0<=z<=1e-6` | Exact limiting formulas evaluated numerically in the admitted clock range. Finite-`q` errors are not included. The elementary endpoint is constant one. |
| `heat` | AC2 early and late physical omission upper bounds, `0<=cap<=0.01`, `0<=eta<=0.01`, `sigma>=0` | A budget calculator, not a vector solver. Inputs must be normalized vectors in the original `P21` vacuum ball. `P21` is the strict electric cutoff `K<9/2`; `P293` is a residual-generated enlargement, not a complete spectral cutoff. |
| `heat-certificates` | Exact AC2, AF1 and AF2 scalar calculations at the published points | Rational recomputation from pinned scalar inputs. Checks the residual/isolated-minimum arithmetic and rational projector inequality, without rebuilding the 293-state matrix or its full vectors. |

## Main exact checks

At the published caps this companion independently recomputes:

```text
AB2 Gaussian source bound:          626/1629 < 77/200
AE2 triangular source bound:        2072/2997 < 7/10
AE2 positive-series radius:         192MT = 72/125 < 1
AC2 true output denominator:        7127/7200
AC2 early absolute join bound:      457097/12600000000
AC2 late absolute join bound:       2441/78400000
AC2 all-time physical relative:     457097/12472250000 < 0.000037
```

Positive rational Taylor sums verify the exponential tail comparisons; no
floating exponential is used to certify those inequalities. Every exported
AF2 scalar field is compared exactly with the pinned source result. The
physical omission term and the numerical evaluator term remain separate.

The test runner also rejects invalid endpoints, nonfinite values and Boolean
substitutions; enumerates actual small tail-cube face sums independently of
the closed formula; checks the triangular convergence boundary; discriminates
the wrong zero-variance scalar closure, wrong single-frequency Wilson models,
and copying rank-operator norms to actual multiplication observables.

All gates raise explicit exceptions and remain active under Python `-O`.
The normal and optimized runs are replays of the same checks, not independent
experiments. All present companion code and tests share an author; no external
peer review is asserted. Finite sampled checks corroborate implementation;
the source reports supply the infinite-dimensional hypotheses and proofs.

## Reproduce the original 293-state heat vectors

To reconstruct every fusion channel, all 1,088 directed sparse magnetic entries,
the diagonal Gram (231 weights one and 62 weights three), and the complete
exported heat vectors, use the original pinned repository. These operations
are intentionally not represented by the companion scalar budget calculator.

```bash
git clone https://github.com/occult-kranti/yang_mills_workbench.git
cd yang_mills_workbench
git checkout 40960f39a3dcaa6b2735d47adaa0e3b40e6a0f02
python3 -B research/round26/forward/af1/check.py --output /absolute/fresh/af1
python3 -B research/round26/forward/af2/check.py --output /absolute/fresh/af2
```

Keep the complete checkout: the original checkers bind and read their frozen
reports, exact compression and historical source files. The commands above
are the source workflow, not a claim that this companion independently
reran the full solver. See the pinned Round26 README for whole-release replay.

No model here establishes a homogeneous all-step inverse, calibrated physical
clock, graph-size uniform approximation, four-dimensional continuum theory,
or Yang–Mills mass gap.
