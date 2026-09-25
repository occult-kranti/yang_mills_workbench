# Round33 scientific addendum

This directory owns a separate manuscript edition, *Round33 research addendum: boundary decay, locality and convergence of the named constructions, certificates for the limit, and applications to related problems*. It does not modify Draft03 or the Round31 and Round32 addenda. The manuscript and PDF are authored from the eight reviewed Round33 gates (BA1-BD2: three research sub-rounds and the applications stage), and the builder refuses to run before all eight gates exist and verifies every gate binding.

Sources: `main.tex` (title, abstract, status and reading guide), `model.tex` (model dictionary, families, Round32 checkpoint, plan), one section per investigation (`decay.tex` BA1, `dynamics.tex` BA2, `locality.tex` BB1, `convergence.tex` BB2, `consequences.tex` BC1, `uniform.tex` BC2, `applications.tex` BD1 and BD2 with the summary table of what transferred and what did not), each quoting its gate's accepted statement and limitations verbatim, then `history.tex` (process history), `limits.tex` (what the record does and does not establish, the obligations state and the ranked roadmap), `contributions.tex` (appendix: contribution and evidence ledger) and `references.tex`. `layout.tex` is shared and unchanged.

```bash
python -B papers/round33-addendum/build.py --render
python -B papers/round33-addendum/build.py --check
```

The sources can be compiled for layout checks without the builder (output stays under the ignored `tmp/`):

```bash
cd papers/round33-addendum && latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=tmp/pdfs main.tex
```

Prerequisites: Python 3, a LaTeX distribution with `pdflatex` and `latexmk`, the packages named in `layout.tex`, and Poppler's `pdftoppm`, `pdftotext` and `pdfinfo`. After a render, run `python -B papers/round33-addendum/inspect_pdf.py` (needs PyMuPDF) and inspect every `tmp/pdfs/page-*.png`. Compilation success alone does not establish visual review.

`build-receipt.json` (schema `hnm-round33-addendum-build-v1`) binds the scientific inputs, manuscript sources and PDF. `qa.json` records the page-image review (geometry schema `hnm-round33-addendum-geometry-v1`). The published copy is `dist/ym-round33-addendum.pdf` (and `docs/ym-round33-addendum.pdf` after the Pages build), byte-identical to `main.pdf`. Intermediate LaTeX and rendered pages under `tmp/pdfs/` are rebuild products, not scientific evidence.
