# Physics Observatory: Yang–Mills connection and skeptical review

The related unsolved $1 million problem is Yang–Mills existence and mass gap. The exact target is pure nonabelian quantum-field existence in four dimensions for every compact simple gauge group, plus a positive physical mass gap. Clay's current status and the official formulation are linked in advisor-dossier.md. The finite QED and scalar-gravity work does not solve it.

This review includes three repaired implementation/acceptance defects, reproduced finite-model evidence, a new delayed scalar-response grid study, exact finite-volume and spectral counterexamples, two conditional spectral lemmas and a finite proof-rule replay. The site has dedicated pages for the results and an inventory linking previous derivations.

## Run the downloadable package

Use Python 3.10 or newer with NumPy, SciPy and Matplotlib. The recorded environment used Python 3.12, NumPy 2.3.5 and Matplotlib 3.10.8. Source hashes are recorded separately from results. Install compatible packages in your own environment if necessary:

```bash
python -m pip install numpy scipy matplotlib
python reproduce.py
python reproduce.py --full
```

The first command pair runs the new diagnostics, original-failure/fixed-behavior regressions, delayed response study and the frozen conditional proof replay. `--full` also copies the archived dependencies into `corrected-run/`, applies the two explicitly revised solver files there, and reruns the finite/gravity suites and root validator. Historical `evidence/` files stay unchanged. Newly generated data overwrite corresponding new run outputs only.

SymPy is required for the separate archived symbolic checker. It was unavailable during this audit: 21 independent numerical checks were rerun; 21 symbolic checks were explicitly blocked. Historical symbolic results remain historical. Do not relabel a missing import or a skipped branch as a passing check.

## Package map

- `gap-output/`: exact free lattice and positive spectral-mixture diagnostics, 57 checks, three CSVs, two static figures and derivations.
- `skeptic-output/`: three original defect reproducers, two corrected sources, 13 regressions, new scalar-response study, manifests and audit notes.
- `evidence/qeg-research/`: recovered textual scientific source/data dependencies from the previous delivered archive. PDFs and large binary artifacts remain available from the historical Observatory download.
- `proof/`: conventional spectral proof, frozen source binding, 8-rule and 7-rule derivations and failed unsupported routes. This planner is not a mathematical proof kernel.
- `site-review/`: exact page source, content data and interface-check report for this update.

## New numerical evidence

The original and corrected default runs produced ten byte-identical CSV files. The changes repair coefficient matching, overflowed diagnostic rejection and vacuous gravity-result acceptance; they do not change those default sampled trajectories.

For the finite delayed source at fixed b=10, K=20, inclusive ncut=1, g=0.1, nu=0.5 and epsilon=5e-5, the field-response discrepancy is 2.87154e-4 at 64→128 momentum nodes and 1.38903e-6 at 128→256. The latter meets the predeclared 2e-5 working scale. This is adjacent-grid evidence at fixed physical cutoffs, not a rigorous total-error bound.

The exact spectral mixture C(t)=1e-12 exp(-0.1t)+exp(-t) has an early effective-mass plateau near 1 although its lowest overlapping mass is 0.1. For positive spectral measures, effective mass bounds that threshold from above. A channel can also have zero overlap with a lighter physical state. Uniform spectral lower bounds require additional premises that remain open in Yang–Mills.

The periodic free scalar plot uses only the lowest nonzero-momentum mode. The massless zero mode is explicitly excluded; this quantity is not the full massless finite-volume gap.

## Evidence boundaries

The code and conventional proofs establish restricted statements under their stated assumptions. Independent agent critique is not credentialed human peer review. Numerical convergence differences are not rigorous enclosures. The current quantum energy and directional stress needed to join the finite QED and gravity branches remain unresolved. No proposed goal is silently promoted to a premise in the new proof library.

Interface verification uses VM-render/event tests and hosted-asset checks. Real-browser layout and keyboard testing were not performed in this turn.
