# Hruday N M (BUNZEEY): integrated gauge-theory research draft

This edition carries forward the complete Draft02 manuscript: Draft01 through Round26, the Round27 and Round28 addenda, and the reviewed Round29 continuation. It adds exactly three reviewed Round30 investigations, complete forward and reverse derivations, their source comparisons, and the updated research priorities. The historical publications and frozen research evidence remain unchanged.

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
- `calculators/hnm_round30.py` evaluates the admitted AT2 spectral-window and inverse-energy bounds with exact fractions. It preserves the actual unknown response and rejects parameters outside the declared energy/coupling range.
- `calculators.html`, `calculators/` and `audit/` carry forward Draft01's historical companions. Their old review counts and PDF hashes concern that historical draft, not this new edition.
- `pdf-qa.json` and `artifact-manifest.json` describe the integrated edition's current build and visual review.

From the repository root run:

```bash
python3 -B research/round30/editorial/integrate.py
python3 -B papers/draft-03/build.py
```

Integration requires precisely three completed Round30 reviews and the post-cycle roadmap. It preserves each gate's actual verdict; a limited result or an obstruction still counts as a completed investigation. The build validates the inherited ten Round29 gates and the three Round30 gates, then compiles in a temporary directory. It resets visual-review status. `--draft` is an editorial build mode and does not bypass scientific review or certify release readiness. Standard TeX Live, `pandoc` and `latexmk` are required; no dependency is installed by these scripts. `main.bbl` is included for ordinary offline LaTeX compilation.

`round30-inputs.json` binds the current gate, report, review, source-ledger and roadmap inputs. The other input manifests and the carried `audit/` files describe historical editions. Only the top-level current `pdf-qa.json` and `artifact-manifest.json` certify the present PDF and disclose its actual visual-review coverage.

The priority table is a qualitative ranking of research usefulness. It is not a numeric discovery score or an estimate of the percentage of Yang–Mills solved. Failed certificates and accepted obstructions remain visible.

The original paper source keeps HNM-C contribution identities separate from HNM-E equation aliases. Both independent derivation directions receive equation locators, while the new contribution count remains three. HNM-Q aliases for `L`, `c`, `b`, `T`, `h`, `N` and `epsilon` identify proof choices, protocol design variables or data-error assumptions; they are not new physical constants.
