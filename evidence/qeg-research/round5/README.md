# Bidirectional proof dossier — research round 5

This package proves a conditional finite-model existence and response theorem, records its edge cases, and supplies a typed map of the larger research problem. It does not claim a complete proof of continuum Einstein–QED or the four surrounding open problems.

Read `guide.md` or the separately supplied PDF first. The accepted theorem and complete tangent equations are in `theorem_advisor.md`; explicit failed inferences are in `proof_critique.md`. `theory_map.json` contains 44 typed nodes with assumptions, reading provenance and next obligations. `research_bridge.md` derives a conditional Bianchi-I constraint-propagation identity and states the unclosed quantum-stress problem. `targeted_solver_prompt.md` specifies the next research cycle.

## Reproduce the checks

Use Python 3.12 or a compatible environment. From this directory:

```sh
python -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python run_checks.py
```

On Windows use `.venv\Scripts\python.exe`. Installation requires normal access to the package index. The original verification environment used Python 3.12.14. No proprietary algebra system or paid model API is required to reproduce these checks.

The standard-library proof planner can run without third-party dependencies:

```sh
python proof_search.py search_fixture.json --output search_results.json
python test_proof_search.py
python verify_proof_search_independent.py
```

The CLI records both additional scenarios embedded in the fixture. The complete selected-regulator scenario removes the positive-margin seed, derives it from the declared parameter/quadrature/special-function premises, and reaches the selected theorem. Cost is a count of reviewed rule applications in this supplied finite library. A successful route is a checked plan, not a proof of its referenced analytical lemmas by a formal kernel.

`symbolic_checks.py` and `counterexamples.py` use SymPy. `coefficient_certificate.py` uses the frozen historical coefficient constructors and exact `Fraction` arithmetic; it reruns no time integration. It checks source hashes before importing those constructors. The enclosing archive preserves the sibling `round3/code` and `round4/code` paths required by the historical import. Do not move only one historical file and expect its relative imports to work.

`run_checks.py` writes new execution logs and results in this extracted directory. Preserve the original archive if comparing later changes. The initial search-review findings intentionally remain as historical records; final acceptance is in `search_independent_review.json` and `validation_run.json`. Hashes identify the code actually reviewed.

## What each check establishes

- Symbolic checks test exact finite-model identities and detect deliberately wrong terms.
- Counterexample checks reject specific invalid generalizations and verify exact rational inequalities.
- Planner tests check conjunctions, retained assumptions, replay, hash integrity, resource limits and finite-library costs.
- Independent search review compares costs against a separately written exhaustive subset oracle on 64 small libraries.
- The coefficient certificate interprets generated floating coefficients as exact rational model inputs. It does not certify transcendental rounding or enclose a computed trajectory.

The conventional global-existence proof also uses mathematical inequalities and standard ODE theorems. Those are written out and reviewed in the dossier; they are not replaced by passing unit tests. No Lean/Isabelle proof was executed.

## Document build

The final PDF is supplied separately. The editable Markdown and assembly scripts are included. Rebuilding the PDF additionally requires ReportLab, Pillow, pypdf, Pandoc, a TeX installation with amsmath/preview, and Poppler. `assemble_dossier.py` builds `guide.md`; `build_guide.py` renders it. PDF build tools are separate from the scientific solver requirements. The saved QA report records the rendered pages inspected for the delivered PDF.

Only project-authored research/code and source metadata are bundled. Referenced papers and books are linked at their primary sources; they are not redistributed in this archive. Historical model files are preserved for reproducibility, not silently edited to agree with a new theorem.
