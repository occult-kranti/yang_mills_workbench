# Physics Observatory — skeptical research review

This review adds eleven detailed result pages to the private Observatory, with an evidence homepage, claim and code audit, typed theory connections, four recorded-data plots, and a falsifiable experiment ledger. The website is the reading interface; this archive contains the equations, source code, independent reviews, failed cases and recorded data behind it.

## Scientific outcome

Four restricted project derivations survived independent skeptical review:

1. An exact finite-window continuous-momentum coefficient and proof of its global maximum.
2. A rational `Z>3/4` certificate for every finite Landau cutoff at fixed `b=10,K=20`, with positive quadrature exact on constants.
3. A proof that the unmodified matching cannot retain a uniform positive coefficient gap when both physical cutoffs are removed cofinally.
4. A positive stationary-vacuum second variation controlling the electric and transformed transverse tangent, with an explicit counterexample to boundedness of the raw tangent.

These are conditional mathematical results in declared reduced models. Their novelty in the published literature has not been established. They do not solve Einstein–QED, supply covariant quantum directional stresses, establish continuum dynamical convergence, or solve the four original black-hole/mixing research problems.

Read `extensions.md`, then `skeptic_review.md` and `claim_verdicts.json`. The earlier finite-model theorem and Bianchi-I constraint derivation are in `../round5/theorem_advisor.md` and `../round5/research_bridge.md`. The theory-map edges distinguish implications from context and unresolved bridges.

## What the audit found

- The core audit inspected all 1,438 historical lines and 50 functions across six selected computational files. Nine defects or metadata gaps were repaired in `round6/code/`; historical files remain unchanged.
- The new coefficient implementation initially reported passing gates. An independent review found seven more issues: prefactor, index, logarithm, cancellation, reference precision, input validation and symbolic domain. Initial and intermediate failures are retained in `advisor_experiment_review.json` and `advisor_review/`.
- A separate science-copy review found six misleading statements. The integrated pages now retain the finite-model commutator/contact connection, use the executed stationary fixture, distinguish fixed canonical from evolving kinetic momentum, state the tangent regularity assumptions, count defect controls correctly and use the right susceptibility sign.

Read `code_audit.md`, `advisor_experiment_review.md`, and `homepage_science_review.md`. The last file records the original defects, not a claim that they remain in the published pages; `integration_review.json` records their disposition.

## Reproduce the calculations

Use Python 3.12 and install the declared packages in an environment of your choice:

```sh
python -m venv .venv
. .venv/bin/activate
python -m pip install -r qeg-research/round6/requirements.txt
python qeg-research/round6/code/run_checks.py
python qeg-research/round6/experiments.py
python qeg-research/round6/advisor_independent_checks.py
python qeg-research/round6/skeptic_checks.py
```

Run from the extracted archive root. The scripts locate their reference files relative to their own paths. Re-execution refreshes result files; keep an untouched copy if you want to compare against the frozen delivered snapshot. Libraries are not vendored into this archive. Source hashes protect evidence provenance, not mathematical truth.

Expected recorded gates:

| Check | Recorded outcome | Scope |
|---|---|---|
| Independent skeptic | 46/46 pass | Exact algebra, rational estimates, independent integration, small matrix dynamics and falsifiers |
| Independent coefficient advisor | 29/29 pass | Values and axis conventions checked against separately built references |
| Core repair regressions | 18 pass | Nonzero-probe comparison, invalid inputs, missing samples, optimized-Python defects, provenance and labels |
| Planner compatibility | 24 pass | Existing finite-rule fixtures and search behavior |
| Symbolic core suite | 16 checks pass | Fourteen identities and two deliberate-defect controls |
| Coefficient integration matrix | 135 comparisons pass | Contracted finite `b,N,K,a` matrix |

Neither passing sampled diagnostics nor arbitrary-precision evaluations are interval enclosures of a full trajectory. The new coefficient experiment is not a new production ODE run.

The nonzero-probe repair uses the identical small fixture `b=1,N=0,K=3,nk=12,tfinal=1.2,samples=61,probe_amp=0.5`. Its historical finite-difference error stalls near `2.965e-5`; corrected errors decrease to `4.701e-10`. The matched default small fixture is bit-for-bit unchanged. Historical production response convergence retains its separate fixed-regulator acceptance and coarse-grid failures.

## Read the plots

- `plot_data/quadrature_refinement.csv`: exact integral versus finite Gauss rules at fixed physical cutoffs; includes coarse errors.
- `plot_data/finite_geometry.csv`: sampled even-kernel geometry and derivative checks.
- `plot_data/tail_behavior.csv`: exact special-function and labeled asymptotic evaluations in `log10(N+1)`; a threshold metadata row is not a plotted data point.
- `code_fix_convergence.csv`: before/after source-center regression. Both axes in the website use explicit logarithmic labels.

Every graph is an illustration of its listed calculation. A cofinal divergence proof uses positivity and thresholds, not extrapolation of a finite plot.

## Next work and stopping rules

The next physical task is common renormalization of current and directional stress for a declared quantum state, followed by its force Ward identity and compatible gravitational evolution. The current finite work identity does not provide that closure. A second bounded branch asks whether a positive time-dependent response energy can be established for a narrowly specified pumped base; the stationary-vacuum result cannot simply be transferred.

`advisor_plan.md` and `advisor_experiment_contract.md` record forward evidence, backward obligations, rejection conditions and computational costs. `targeted_solver_prompt.md` defines the next bounded analytical task. No continuing background swarm or ongoing physical computation is implied by this snapshot.

Primary sources are linked with reading scope in `advisor_sources.json`, `skeptic_sources.json`, and the historical source ledgers. The archive includes project-authored notes and reference links; it is not an exhaustive copy of all existing papers, books, patents or national projects.

The Site build assets and dedicated skills are maintained in the Site’s source repository. `build_hub_data.py` is the integration recipe and expects that companion checkout; it is not required to reproduce the scientific checks above.
