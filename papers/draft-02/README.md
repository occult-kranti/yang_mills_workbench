# Hruday N M (BUNZEEY): integrated gauge-theory research draft

This new edition integrates the complete research body and appendices of Draft01 through Round26, the Round27 and Round28 addenda, and the reviewed Round29 continuation. The historical publications and frozen research evidence remain unchanged.

**Human author:** Hruday N M (BUNZEEY). AI systems assisted research, implementation, checking and editing. There has been no external human peer review, formal proof-assistant verification, journal acceptance or arXiv submission.

The Hruday/HNM naming system identifies project records. It preserves external eponyms, conventional symbols, model boundaries, source attributions and original research IDs. Names do not establish scientific priority. In particular, the primary-source comparison to Shoshauna Gauvin's arXiv:2503.15539v3 identifies overlap in the general homogeneous Wilson/GNS/moment strategy; its SU(3) constants are not transferred to the workbench's SU(2) model.

HNM-C names contributions, HNM-E names equation records, HNM-Q names registered quantities, and HNM-T/HNM-P name admitted scoped theorem statements and propositions. There are zero newly asserted axioms. A `current_extensions` link records a later admitted result beside an unchanged historical limitation; it never enlarges the original gate retroactively.

The four-dimensional continuum Yang–Mills construction and physical mass gap remain open in this project. See the full assumptions, fixed-lattice conditions and negative results before interpreting any estimate.

## Read and reproduce

- `main.pdf` is the integrated manuscript.
- `main.tex`, `sections/`, `addenda/`, `sources/` and `figures/` are its editable sources.
- `registry/hnm-registry.json` maps every contribution, labelled equation and registered quantity to HNM aliases; original identifiers remain available.
- `registry/README.md` is the contribution-name concordance.
- `calculators/hnm_round29.py` evaluates the admitted AM2 budgets and physical-unit conversions with exact fractions. It checks arithmetic conditional on the source model and never extends the accepted coupling cap.
- `calculators.html`, `calculators/` and `audit/` carry forward Draft01's historical companions. Their old review counts and PDF hashes concern that historical draft, not this new edition.
- `pdf-qa.json` and `artifact-manifest.json` describe the integrated edition's current build and visual review.

From the repository root run:

```bash
python3 -B papers/draft-02/build.py
```

The final build requires ten Round29 findings and source-bound gates, then compiles in a temporary directory. It resets visual-review status. `--draft` is an editorial build mode and does not certify release readiness. Standard TeX Live and `latexmk` are required; no dependency is installed by the build. `main.bbl` is included for ordinary offline LaTeX compilation.

The priority table is a qualitative ranking of research usefulness. It is not a numeric discovery score or an estimate of the percentage of Yang–Mills solved. Failed certificates and accepted obstructions remain visible.
