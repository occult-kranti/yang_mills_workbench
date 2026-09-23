# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A reproducible research workbench for SU(2) lattice gauge theory (the four-dimensional Yang–Mills existence and mass-gap problem remains open; nothing here claims to solve it). Human author: Hruday N M (BUNZEEY); AI assistance is disclosed. The repository holds (a) a static website with physics calculators, a curriculum and a patent archive, and (b) ~30 numbered research rounds of exact-arithmetic certificates, numerical experiments, mathematical reports and skeptical reviews, plus LaTeX manuscripts.

`AGENTS.md` at the root is the binding research-workflow contract (ownership boundaries, freeze rules, review rules, historical immutability). Read it before touching anything under `research/`. `README.md` is the public summary of every round; its per-round table is the map of what is where.

## Commands

The website needs no build step or packages. Scientific code uses only the standard library (`fractions`, `hashlib`, `json`) except where a round's README names NumPy/SciPy/Matplotlib.

```bash
python3 start.py --no-browser --port 8002      # local static server at http://127.0.0.1:8002/#research
python3 -m unittest test_server tests.test_local_launch   # Python unit tests for the launcher/server
node tests/test_workbench.mjs                   # one UI/interface test (each tests/*.mjs is standalone)
node tests/round31_site.mjs --require-release   # current-round site test; also `npm run test:round31`
python3 scripts/build_pages.py                  # regenerate docs/ (GitHub Pages) from dist/
```

Per-round scientific validation (the pattern is the same for every round since ~22; substitute the round):

```bash
python3 -B research/round31/reproduce.py --complete --validate-only
python3 -B research/round31/reproduce.py --complete --output /absolute/fresh/dir          # replays every producer check.py
python3 -B -O research/round31/reproduce.py --complete --optimized --output /absolute/fresh/dir2
python3 -B research/round31/test_admission.py                                            # damaging-evidence controls
python3 -B research/round31/forward/at6/check.py --output /absolute/fresh/dir3            # one producer alone
```

Replay outputs must be fresh absolute directories outside the checkout (validators refuse otherwise) and must reproduce `output/` byte-for-byte under both normal and `-O` Python. Always run scientific scripts with `-B`; `.pyc` files inside a producer closure fail admission.

LaTeX (`latexmk`, `pdflatex`) and Poppler are needed only to rebuild `papers/*/main.pdf`; they are not required for validation.

## Architecture

### Two layers, one repo

- **Site layer**: `dist/` is the authored static site (`index.html`, `app.js`, `content.js`, per-round `research-roundNN.js` + `-data.js` + `.css`, CSV/JSON/ZIP evidence downloads). `scripts/build_pages.py` copies it to `docs/` with a rewritten base path; GitHub Pages serves `main:/docs`. `content.py`, `specialisms.py`, `learning_program.py`, `patent_*.py`, `research_catalogue.py` generate the JSON/JS content bundles. `start.py` serves `dist/` locally and adds an optional arXiv metadata endpoint.
- **Research layer**: `research/roundNN/` for each cycle; `evidence/qeg-research/round3..7` for the earliest Einstein–QED work; `papers/` for manuscripts (Draft01–03 and round addenda, each with `build.py`, hash manifests and page-QA records); `.codex/skills/` for the advisor/validation method skills and their per-round reference notes.

### Anatomy of a research round (read this before adding one)

Each round is an adaptive cycle of "loops" (investigations) selected one at a time by the advisor:

- `contracts/<loop>.json` — frozen before production (`status: frozen_before_production`, `shared_premises` list, `required`, `controls`, `claim_exclusions`).
- `forward/<loop>/` and `reverse/<loop>/` — two independent producers. Each has `report.md` (the mathematics), `check.py --output <abs fresh dir>` (exact rational checker writing `output/results.json` with a `checks` list of `{id, passed}`), `inputs/` (byte-identical snapshots of every declared premise at its repo-relative path, always including `AGENTS.md` and the contract), and `freeze.json` (SHA256 of every file in the closure).
- `skeptic/<loop>.md` + `<loop>.json` (verdict, `blocking_issues`, `supported_statement`, `limitations`, `bindings`) plus independent derivations/controls and replay receipts.
- `advisor/<loop>-gate.json` (verdict ∈ accepted_within_scope | limited | insufficient, `accepted`, `limitations`, `bindings` hashing all evidence), `selection-<loop>.md`, `findings.json` (synthesis), `admission-spec.json` (trusted reviewed semantics and required check ids), `roadmap.json` (planned-only next goals).
- `experts/<lens>/memo.md` + `sources.json` — Newton/Tesla, Jung/Pauli, Penrose/Feynman methodological lenses with per-source reading depth and provenance.
- `methods/` — frozen copies of the skill instructions the producers used.
- `reproduce.py`, `test_admission.py`, `build_network.py` → `network.json` (extends the previous round's network without editing inherited nodes), `presentation/build_site.py` → `dist/research-roundNN-data.js`, `release/README.md` + `verify_release.py`.

`reproduce.py` cross-checks all of these: findings ↔ gates ↔ admission spec, freeze inventories, premise snapshots, executed check ids, skeptic bindings, and byte-identical replays. `test_admission.py` mutates copies of the evidence and requires the validator to reject each mutation for the expected reason.

### Rules that shape every change

- Historical rounds, gates, frozen snapshots and manuscript PDFs are immutable. `verify_release.py` fails if any file under `research/`, `papers/`, `evidence/` or `.codex/` outside the current round changed. Repairs go in new files with an explicit repair record.
- A loop's producers must not read each other's current work before both are frozen; shared premises must be declared in the contract and snapshotted. Same-author passes are never called independent review.
- Every result names its model (which fixed-lattice family, coupling, selected coefficients, state, physical clock) and its exclusions. A `limited` or `insufficient` verdict is a retained outcome. Loop counts are never a percentage of the continuum problem.
- Exact rational arithmetic decides admission; floating-point results are labelled previews/comparisons. Directed rounding, complete error budgets and full tails are required.
- Website pages display recorded results from source-bound data; they never compute admissions. Renderer tests use explicitly synthetic fixtures.

### Current state

Round31 (AT4–AT6) is the latest merged cycle; `research/round31/HANDOFF.md` and `research/round31/advisor/roadmap.json` hold the ranked, unexecuted next goals (cap-level precision, interaction shift, uniform Hamiltonian, state identification, continuum trajectory). Start any continuation from those two files and `AGENTS.md`.

## Foreign agent configuration

This repository ships `.codex/skills/` (Codex-format skills). Reply `/import` to scan and list what is importable, then `/import --yes=<digest>` to apply it; or run `claude import` from a terminal if `/import` is unavailable here.
