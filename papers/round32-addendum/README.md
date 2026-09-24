# Round32 scientific addendum

This directory owns a separate manuscript edition. It does not modify Draft03 or the Round31 addendum. The manuscript and PDF are authored from the ten reviewed Round32 gates; the builder refuses to run before all ten gates exist.

```bash
python -B papers/round32-addendum/build.py --render
python -B papers/round32-addendum/build.py --check
```

Prerequisites: Python 3, a LaTeX distribution with `pdflatex` and `latexmk`, the packages named in `layout.tex`, and Poppler's `pdftoppm`, `pdftotext` and `pdfinfo`. After a render, run `python -B papers/round32-addendum/inspect_pdf.py` (needs PyMuPDF) and inspect every `tmp/pdfs/page-*.png`. Compilation success alone does not establish visual review.

`build-receipt.json` binds the scientific inputs, manuscript sources and PDF. `qa.json` records the page-image review. Intermediate LaTeX and rendered pages under `tmp/pdfs/` are rebuild products, not scientific evidence.
