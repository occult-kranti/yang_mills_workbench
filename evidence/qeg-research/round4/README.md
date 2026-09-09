# Causal response research — reviewed cycle 4

Read `guide_overview.md` first, followed by `physics_acceptance.json`, `response_contract.md`, and `response_advisor_review.md`. The full PDF is available separately and from the private Physics Observatory. The research package retains round3 evidence as history; round4 records the source/report mismatch and new corrections.

This is a finite-regulator, flat, homogeneous Maxwell–Dirac mean-field experiment at fixed magnetic background. The new result is a checked source-amplitude derivative, not a complete quantum-noise test, a removed continuum regulator or a gravitational solution.

## Reproduce the numerical evidence

Tested with Python 3.12.14, NumPy 2.3.5 and SciPy 1.17.0. Install `round4/requirements.txt` in your own environment if needed. Preserve the sibling `round3/code/backreaction.py`: the new implementation imports its constants and uses the unchanged code for the legacy comparison.

From the extracted `qeg-research` directory:

```bash
python round4/compare_response_production.py
python round4/verify_response.py
python round4/response_run.py
python round4/compare_response_production.py
```

The first command checks the delivered saved arrays and source hashes without rerunning the ODEs. The next two regenerate the independent and production results. The production suite includes central-difference families and the 1024-node final case, so it is substantially more expensive than the first command. Rerunning overwrites working results; copy the package to a new experiment directory first to retain the delivered evidence.

`response_results.json` holds the actual full sampled traces. `response_results.csv` is the long-format companion. `response_verification_initial.json` preserves the finite-difference gate failure. `advisor_errata.json` separately records the pre-fix diagnostic failure for which the original full output was not archived. The final source hash is recorded in `physics_acceptance.json`; an edit requires a new source hash, new comparison and new acceptance record.

The PDF renderer additionally uses ReportLab and a TeX/Poppler environment. Its source is included for audit; installing those optional document dependencies is not required for the numerical solver. The delivered website is maintained separately in its registered source repository; this package contains the research artifacts rather than a second checkout of the website.

## Reuse the advisor workflow

`advisor_pipeline.md` defines roles, handoffs, claim types, evaluator gates and retirement rules. `targeted_solver_prompt.md` is the specification for the next reasoning-engine run. `advisor_skill_forward_test.md` records two bounded nonblinded exercises; it is not a general agent-performance benchmark. `physics_completion_roadmap.md` retains all four original physics branches and their remaining dependencies.

New source ledgers record exact URLs, access dates, inspected sections and limits. Full papers and books are not bundled; follow their publisher, author or open-access links. `round3/references.json` preserves the broader historical/source collection.

No agents run continuously from the website. Notes and explanation preferences are browser-local. The browser preview was unavailable in this environment, and the release record distinguishes simulated DOM/Worker tests from real browser QA.
