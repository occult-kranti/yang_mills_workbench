# Round27 research addendum

This additive manuscript summarizes the selected historical-method source survey and the three Round27 investigations: AI1, AI2 and AG1. Draft01 is preserved unchanged. This is not an arXiv submission; human authorship and affiliations remain to be supplied.

The `**` marker denotes a contribution derived or implemented within this workbench. It does not assert scientific priority, historical-person endorsement, external peer review, a completed homogeneous iteration, or a continuum Yang–Mills mass-gap proof. The expert percentage assessment is **not estimable**; the three-loop task count is separate.

Files:

- `round27-addendum.tex`, `ai2.tex`, `ag1.tex`, `contributions.tex`, `reproduction.tex`: editable LaTeX manuscript.
- `../../dist/ym-round27-addendum.pdf`: final rendered addendum.
- `plot_round27.py`, `figure-data.json`, `../../dist/ym-round27-discrimination.png`, `../../dist/ym-round27-contraction-bounds.png`: exact-output-backed plots and their provenance.
- `build.py`: plot generation, two-pass LaTeX build, page rendering and text/layout checks.
- `pdf-qa.json`: final PDF hash, automated diagnostics and separate visual QA record.
- `finalize_manifest.py`, `manifest.json`: addendum and source-integrity bindings.

From the repository root:

```bash
python3 -B papers/round27-addendum/build.py
```

This requires final Round27 gates, Python with NumPy/Matplotlib/PyMuPDF, `pdflatex`, and `pdftoppm`. It performs no installation. The plot uses rational evidence for its decisions; floating-point values are only for display. The build command does not rerun all physical checks. For fresh scientific replay, follow `research/round27/README.md` or the manuscript's reproduction section.

After any meaningful edit, inspect every newly rendered page in `build/`, address defects, and record the matching final PDF hash and visual review in `pdf-qa.json`. Only then run `finalize_manifest.py`. A successful compile or text extraction does not satisfy visual review. Temporary TeX products and page renders are excluded from the manifest and removed after the authoring review.

The actual model boundary is essential: AG1 is one correction of the inherited cubic-source sector `G+A`. It is not a transformation of the complete original homogeneous Yang–Mills Hamiltonian; any additional terms require their separately stated transport hypotheses. AI2 is a two-hypothesis scalar discrimination at an extreme declared clock and error allowance; all simple ratio certificates on its frozen grid remain insufficient.

The source survey records 55 entries at 54 distinct URLs, with selected passages, abstract-only records and access failures distinguished. No complete-library or exhaustive contemporary-literature claim is made.
