# Research drafts

[Open the drafts page](https://occult-kranti.github.io/yang_mills_workbench/#research/drafts).

Locally, run `python3 start.py --no-browser` from the repository root and open
http://127.0.0.1:8001/#research/drafts.

## Round27 addendum — 22 September 2026

**Readout identification and a complete selected-source correction.**

[Read the PDF](../dist/ym-round27-addendum.pdf) ·
[Editable source, figures and build instructions](round27-addendum/README.md) ·
[Three-loop evidence](../research/round27/README.md).

The addendum records AI1, AI2 and AG1, their current research/source comparisons,
and the panel's unresolved proof obligations. It leaves Draft01 unchanged.
The one-step contraction is a selected-model result; no continuum solution or
percentage of the final proof is claimed.

## Draft 01 — 22 September 2026

**Certified finite-model gauge calculations: spectral bounds, local corrections,
Wilson readouts, and controlled heat evolution.**

- [92-page PDF](draft-01/main.pdf)
- [Editable LaTeX](draft-01/main.tex) and [build instructions](draft-01/README.md)
- [Reproducibility ZIP](../dist/ym-draft-01-source.zip)
- [Standalone calculators](../dist/ym-draft-01-calculators.html)
- [Skeptic mathematical review](draft-01/audit/skeptic-review.md)
- [Final compiled-text review](draft-01/audit/skeptic-compiled-review.md)
- [Contribution catalog](draft-01/audit/contribution-catalog.json)

This is the exact draft delivered for author review, based on research commit
`40960f39a3dcaa6b2735d47adaa0e3b40e6a0f02`. It covers the surviving Rounds3–26
and plans for AG/AH/AI. The 114 contribution rows and 121 historical entries
are audit units, not counts of discoveries. The double stars mark workbench
contributions; scientific priority remains unverified. Human authorship is
pending and no arXiv submission has been made.

The original archive is unpacked into `draft-01/` without changing its source
bytes. `MANIFEST.sha256.json` binds the archived files. The added `main.pdf`
matches the downloadable PDF. `drafts.json` records the public asset hashes.
The publication does not change accepted research evidence or add physics loops.

To build the editable source:

```bash
cd papers/draft-01
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

The source bundle documents which checks were freshly executed and which
historical calculations were reviewed without a full production replay.
The four-dimensional Yang–Mills construction and mass gap remain open.
