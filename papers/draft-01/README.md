# Yang–Mills workbench: first manuscript draft

This is an arXiv-style **first draft**, prepared on 22 September 2026, of the surviving research history through Round26 and the next planned goals. It is not an arXiv submission. Author names and affiliations remain to be supplied.

The two-star marker `**` identifies contributions newly derived, specialized, or implemented within the workbench. Scientific priority is unverified. The paper preserves assumptions, failures, conditional statements, and model boundaries. It does not claim a continuum Yang–Mills construction or mass gap.

## Contents

- `main.tex`, `sections/`, `sources/references.bib`: editable manuscript and bibliography.
- `figures/`: publication figures and plot data/notes.
- `calculators.html`: standalone interactive formula calculators; open in a browser.
- `calculators/`: parameterized Python companions, tests, source records, and instructions.
- `audit/`: independent skeptical checks, contribution ledgers, the complete 121-entry history index, and verification records.
- `build_appendices.py`: rebuilds the historical appendix from the pinned repository.
- `build_contribution_appendix.py`: rebuilds the grouped contribution table from the three audit ledgers.
- `MANIFEST.sha256.json`: exact hashes of every other file in the source bundle.

## Source checkpoint

Repository: https://github.com/occult-kranti/yang_mills_workbench

Commit: `40960f39a3dcaa6b2735d47adaa0e3b40e6a0f02`

Tree: `169b2db4e8017f5c4e783ba5f42e4f96522ad2b1`

The prior exact-tree Round26 release receipt is included with its original scope. Fresh manuscript arithmetic and skeptical checks are separate records. Historical inclusion does not mean every old simulation was rerun. The absence of identifiable Round1/2 packages is explicit.

The compiled draft has 92 pages, six figures, 114 grouped contribution rows, and 121 historical entries. The companion's 194 checks, the skeptic's 158 checks, and the HTML calculator's 15 checks have different scopes and are reported separately. Writer-specific arithmetic checks are documented in their ledgers. Check counts are not numbers of independent proofs or confidence levels.

## Build

Run `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` with a standard TeX Live installation. The bundled `.bbl` permits a LaTeX build without a network bibliography service. All figures are local files. The source uses ordinary article-class LaTeX, not an arXiv-specific proprietary template.

For the calculators, follow `calculators/README.md`. Exact rational outputs, high-precision diagnostics, and double-precision HTML displays have different evidential scopes. The heat companion recomputes the error certificate; the full certified vector evaluator is in the pinned repository.

Optional PDF presentation diagnostics use `audit/inspect_pdf.py` with PyMuPDF and Pillow. The bundled review records the final PDF hash; temporary page renders can be regenerated and are omitted from this source archive.

## Before submission

Complete human authorship and affiliations, review all mathematical claims and attribution, obtain expert external review, and resolve any limitations or priority questions relevant to the intended claims. No permission or endorsement from arXiv or any journal is implied by this draft.
