# Einstein-QED variable and closure study - round 7

Start with `research_report.md` or `output/einstein-qed-variable-study.pdf`. The complete equations are in `variable_contract.md`; the expert literature review is in `renormalization_map.md`; objections remain in `skeptic_review.md`.

This snapshot introduces and verifies two separate scalar-coupled reduced models. It also proves a restricted reference-subtraction identity and a bounded-addition obstruction. It does not solve the full Einstein-QED theory or remove its physical ultraviolet-completion questions. The missing common quantum current/stress construction is explicit.

From the extracted archive, install `qeg-research/round7/requirements.txt` in your own environment. Python 3.12 was used; the requirements record the numerical dependency versions. Then run from the round7 directory:

```
python finite_scalar.py
python gravity_sim.py
python independent_checks.py
python validate_simulations.py
python proof_obligations.py
```

The main solvers write JSON summaries and CSV histories beside their source. They fail explicitly when a gate fails. Optimized Python (`python -O`) was checked for the independent validator and root validator; their acceptance checks do not use removable assertions. Inspect semantic status and source hashes, not just process exit codes.

`proof_obligations.py` verifies an immutable reference manifest. If you intentionally edit a referenced scientific file, the old evidence must fail. Review the changed mathematics before authoring a new snapshot with `--freeze`; automatic re-freezing is not verification.

`initial_implementations` preserves the pre-audit drafts. Rounds 3-6 are retained as historical context and required exact references. They may contain intentionally wrong controls or superseded draft code. Use only the commands above for this snapshot. Downloaded papers and proprietary books are not bundled; primary source links and reading-scope records are supplied.

The private Observatory presents recorded simulations. Its plot selectors select completed runs, not new cloud computations. To change continuous scalar parameters and rerun the actual ODE, construct `Params` in `finite_scalar.py` or `Case` in `gravity_sim.py`, keep the stated domain and rerun the corresponding checks. A change in f, quantum preparation, regulator or geometry defines a new test, not a free fit of the old claim.
