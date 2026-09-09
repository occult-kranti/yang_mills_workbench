# Causal quantum backreaction — corrective cycle 3

Read `output/pdf/quantum_electromagnetism_gravity_research.pdf` or `report.md`. `astra_solver_prompt.md` is the complete next-solver specification. This is a tested finite-regulator, homogeneous Maxwell–Dirac mean-field model with a static magnetic field. It does not solve the full continuum Einstein–QED problem.

The accepted result is source-off electric-field reversal, approximately `x(50)=-0.03757`. The final run uses 4096 momentum nodes, Landau levels 0–8 and canonical window [-40,40]. Refining 2048→4096 nodes changes the sampled field history by 3.26e-9; a separate levels 0–8→0–12 comparison shifts its endpoint by 5.06e-8. These are measured component changes, not rigorous continuum error bounds.

## Environment and independent checks

Physics computations used Python 3.12.14 and the versions in `requirements.txt`. No pytest, GPU or cloud credentials are required. From the extracted `qeg-research/round3` directory:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python test_backreaction.py
.venv/bin/python independent_checks.py
.venv/bin/python compare_implementations.py
.venv/bin/python gravity_checks.py
.venv/bin/python bosonized_comparator.py
.venv/bin/python empirical_logic_checks.py
.venv/bin/python advisor_checks.py
```

Scripts rewrite their own result JSON files; keep a copy of the archive for comparisons. `advisor_checks.py` also reads the adjacent archived `../retry/curved_sector_results.json`, included here. Four production checks, ten independent verifier gates, four bosonized comparator gates, four empirical groups and 19 symbolic gravitational identities passed. The advisor's stricter **1e-18 absolute benchmark target failed** at approximately 1.82e-18. A successful script exit does not mean every requested precision gate passed.

## Reproduce the final production experiment

This 36,864-mode run is substantially slower and larger than the small checks. Sampled mode trajectories are retained internally. It writes `results/baseline.json` and `.csv`.

```bash
.venv/bin/python run_backreaction.py --experiment baseline \
  --b 10 --target-e 1 --tpump 4 --tfinal 50 \
  --ncut 8 --nk 4096 --kmax 40 --sample-count 251 \
  --rtol 2e-10 --atol 2e-12 --max-step 0.05
```

`results/production_baseline.json` and `.csv` preserve the final recorded data. The driver's inexpensive historical default is 256 nodes; it is **not** the accepted long-time grid. `--experiment convergence` runs the original small-grid scan, not the final refinement sequence. Reproduce the latter by varying the explicit command: K40 with 1024/2048/4096 nodes; K60 with 3072 nodes; and levels through 12 at K40 with 2048 nodes. Save each baseline output before the next command. Recorded parameters and differences are in `resolved_longtime_summary.json` and `fixed_window_refinement.json`.

For a small comparison use `--ncut 2 --nk 32 --kmax 6 --tfinal 8 --sample-count 81 --rtol 2e-12 --atol 2e-14 --max-step .02`. The independent comparison script uses that same regulator with complex spinors instead of Bloch vectors.

Weak-response controls:

```bash
.venv/bin/python run_backreaction.py --experiment control \
  --b 100 --target-e .01 --tpump 20 --tfinal 40 \
  --ncut 8 --nk 256 --kmax 20 --sample-count 401 \
  --rtol 2e-10 --atol 2e-12 --max-step .08
```

Matched, unrenormalized, omitted-matching and sign-reversed matching are explicitly different models. A consistently wrong prescription can conserve its own energy.

## Data and current notation

Theory calls its mode sum S and derivative coefficient D. Code calls them `J0` and `S`; `Sx2` is theory D times x squared. The effective numerator is `Q=J0+Sx2`. The full matter current is `Jmatter=(Fdrive-xprime)/e2`, where `xprime=(Fdrive-e2*Q)/Z`. Refinement metadata retains `Jren` as a legacy alias for Q and separately records Jmatter. Q alone is not the full physical current.

For 2048→4096 nodes, maximum full-current difference is 1.13147e-6 in j/(e m^3) units; numerator difference is 1.12700e-6. Raw norms and occupations are not clipped. Reported maxima depend on output sampling. Historical failed/superseded comparisons remain as evidence: in particular, `production_baseline_converged` is an intermediate K60/3072-node check. Final production files are `production_baseline` and `resolved_nk4096_K40`.

## Research record and report build

`theory.md`, `advisor.md`, `verifier.md` and `gravity.md` contain independent reviews. `sources_challenge.md` and `empirical_logic_checks.py` address patents and detector claims. `ai_methods.md` documents verified AI research techniques; those discovery engines were not executed. Source ledgers record versions, reading depth and access gaps. `validation_summary.json` preserves passed, failed and unresolved gates. Adjacent `../retry` contains archived project-authored material; this report supersedes its broader interpretations.

No complete third-party books or papers are included. Government and patent documents are assessed as claims, not automatic evidence. Geographic research coverage is targeted, not exhaustive.

PDF rebuilding additionally requires Pandoc, Poppler, DejaVu fonts and `requirements-report.txt`; pdflatex is preferred, with a MathText fallback supplied. Physics tests do not need these document tools.

```bash
.venv/bin/python assemble_report.py
.venv/bin/python build_report.py --input report.md \
  --references references.json \
  --output output/pdf/quantum_electromagnetism_gravity_research.pdf
```

`assembly_manifest.json` identifies inputs. `build_package.py` creates the distribution with SHA-256 manifest and CRC verification. File integrity checks do not extend physical validation.
