# Round31 scientific addendum

This directory owns a separate manuscript edition. It does not modify Draft03.
The completed manuscript and PDF are authored from the three reviewed Round31
gates; the builder refuses to run before AT4, AT5 and AT6 gates exist.

After scientific closeout:

```bash
python -B papers/round31-addendum/build.py --render
python -B papers/round31-addendum/build.py --check
```

Prerequisites are Python 3, a LaTeX distribution with `pdflatex` and `latexmk`,
the packages named in `layout.tex` (including Latin Modern fonts, microtype,
AMS math, geometry, booktabs, longtable, enumitem, fancyhdr and hyperref), and
Poppler's `pdftoppm`, `pdftotext` and `pdfinfo` commands. The diagnostic helper
`inspect_pdf.py` additionally requires the Python package PyMuPDF (`fitz`).
After a render, run `python -B papers/round31-addendum/inspect_pdf.py` for
geometry/reference diagnostics and visually inspect every `tmp/pdfs/page-*.png`.
Compilation and diagnostic success alone do not establish visual review.

`build-receipt.json` binds the scientific inputs, manuscript sources and PDF.
`qa.json` records actual page-image review. Intermediate LaTeX and rendered
pages are under `tmp/pdfs/`; they are rebuild products, not scientific evidence.
The exact build source inventory includes every authoring `.py` file, including
the PDF diagnostic helper. The QA record additionally records helper and
rendered-page digests to detect drift after inspection.

The PDF skill's create marker was run successfully once on 2026-09-22 before
the first authoring command, with one expected PDF output. Do not repeat it
for subsequent edits in this artifact operation.
