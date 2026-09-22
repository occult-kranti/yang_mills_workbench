# Calculator and figure review

The standalone companion passes **194 checks**, with byte-identical normal and
optimized Python result JSON. All **nine documented CLI examples** execute.
The exact AC2, AF1 and AF2 scalar arithmetic agrees with the pinned source
outputs. The original 293-coordinate solver was **not** rerun or copied into
this companion.

The source checkout is pinned to
`40960f39a3dcaa6b2735d47adaa0e3b40e6a0f02`. SHA-256 comparisons verified all
17 consulted source files against the saved source manifest. Runtime code has
no dependency on that checkout: the small imported scalar and graph-structure
datasets are bundled under `calculators/source_data/` with explicit provenance.

## Delivered implementation

- `calculators/ym_calculators.py`: parameterized CLI for one-square Jacobi
  diagnostics, static SU(2) response/moments, exact local-series launch bounds,
  finite-support windows, Gaussian and triangular filters, actual Wilson
  endpoints, and 293-state scalar heat certificates.
- `calculators/test_calculators.py`: explicit exceptions, including 47 exact
  arithmetic checks, 86 high-precision diagnostics, 27 API input rejections,
  4 CLI rejections, 16 boundary controls, 10 wrong-model controls, 3 scope
  controls and 1 direct API precision control.
- `calculators/run_examples.py`: executes the nine documented parameterized
  examples and preserves their JSON outputs.
- `calculators/make_figures.py` and `make_network.py`: reproducible PDF/PNG
  figures, curve CSVs, graph node/edge CSVs, metadata and hashes.
- `calculators/README.md` and `requirements.txt`: domains, units, limitations,
  installation instructions and exact reproduction commands.

Direct API import and CLI both start at 70 decimal working digits. The API
exposes `configure_precision`; the CLI accepts `--precision` from 30 to 200.
Working precision does not establish an interval error enclosure. Exact
certificate calculations use `fractions.Fraction`, integer square-root
enclosures and positive rational exponential witnesses.

## Mathematical and implementation checks

The exact source budgets are `626/1629` for the Gaussian origin source and
`2072/2997` for the translated-family triangular source. The crossing counts
remain distinct (three and twelve). At the triangular boundary `192MT=1`,
inverse finiteness is distinguished from failure of the positive residual
series certificate. At `M=0`, source ratios are omitted.

For AC2, the companion recomputes the true denominator `7127/7200`, early join
bound `457097/12600000000`, late join bound `2441/78400000`, and all-time
physical relative certificate `457097/12472250000`. AF1 and AF2 center,
polynomial, projector, rounding, tail and full relative constants match the
pinned JSON exactly. The early polynomial factor two and AF1 exponential
prefactor each receive a rational verification.

Independent finite face enumeration checks the support formula for three
small complete cubes. Static quadrature checks Bessel response and moment
identities, including origin values and negative coupling. Wilson spectral
weights reproduce all displayed moments through order six. Deliberate wrong
closures and single-frequency models are rejected. Boolean/nonfinite inputs,
excluded coupling/time endpoints and incorrect preparation classes are
rejected at the public interfaces.

These finite checks corroborate implementation; they do not replace the
source reports' all-parameter or infinite-dimensional proofs. The Jacobi
truncation and its refinement remain numerical diagnostics. The heat input
class remains the original normalized `P21` vacuum ball; `P21` uses the
strict electric cutoff `K<9/2`, while `P293` is a residual-generated
enlargement. Physical omission and numerical approximation remain separate.

## Figures and visual checks

The five primary figure pages are `jacobi_static`, `support_window`,
`filter_budgets`, `wilson_endpoints`, and `heat_certificates`, each in PDF and
PNG. They are collected in the five-page `figure_atlas.pdf`. The separate
`network.pdf` is an inventory chart and `network_structure.pdf` is the actual
directed evidence graph.

The graph audit confirms **158 unique nodes**, **260 directed edges**, and no
dangling references. All nodes and edges are drawn. Solid, dashed and dotted
edges distinguish 240 recorded dependencies, 8 review selections and 12
proposed transfers. Historical round groupings and current node kinds govern
the layout; coordinates have no physical or theorem-strength meaning. Open
and planned nodes are explicitly retained as such.

All seven PNGs were visually inspected for readable axes, legends, captions,
scope labels and clipping. PDF parsing confirmed one page per individual
figure and five pages in the atlas. Figure CSVs expose evaluated curve rows;
the network's full node and edge lists are also exported. Exact rational
heat constants accompany the plotted floating display values.

## Executed commands

Commands were executed using the supplied CPython 3.12.14 runtime, with
mpmath 1.3.0, NumPy 2.3.5 and Matplotlib 3.10.8. These are the portable forms,
run from the `calculators` directory:

```bash
python test_calculators.py --output output/test-results.json
python -O test_calculators.py --output output/test-results-optimized.json
python run_examples.py
python make_figures.py --output ../figures
```

Machine-readable review details are in `audit/calculator-review.json`.
Full checks are in `calculators/output/test-results.json`; optimized results
are byte-identical. Companion author checks, root integration review and
separate skeptical review are different activities; none is external peer
review. No full homogeneous inverse, physical clock calibration, graph-size
uniformity, continuum construction or Yang–Mills mass-gap result is claimed.
