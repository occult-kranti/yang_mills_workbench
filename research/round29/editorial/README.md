# Draft02 editorial integration

These scripts create a new integrated manuscript without changing frozen historical sources or gates.

1. `build_integrated.py` starts from the entire Draft01 source and Round27/28 addenda. It is a reset step for the new edition, not a routine compile.
2. `integrate_round29.py` (requires Pandoc) admits only loops present in the advisor's findings and checks every bound source. It retains each full forward report plus the final common gate and every limitation. Current mathematical results are never inferred from missing records.
3. `finish_editorial.py` applies current authorship, attribution, source comparisons, independently repaired registry taxonomy and equation joins, then regenerates priority/naming appendices.
4. `python3 -B papers/draft-02/build.py` compiles in a temporary directory, verifies ten final gates and resolves every citation/reference. `--draft` is only an editorial mode.
5. Render and inspect the PDF. `finalize.py` takes the real completed visual-review record and the exact reviewed PDF hash. It checks the author metadata, complete aliases, source paths, unchanged historical inputs, final roadmap/network bindings, text bounds and zero overfull warnings before writing the artifact manifest. Pass both `--visual-review research/round29/experts/pdf-review.md` and `--review-coverage research/round29/experts/pdf-review.json`, plus the exact `--reviewed-pdf-sha256`. Coverage comes from the independent reviewer’s actual page list, never a fabricated default.

Hruday/HNM names are project aliases. There are no newly invented axioms. Semantic HNM-T/HNM-P aliases identify admitted scoped statements even where the source uses prose instead of formal LaTeX theorem environments. They preserve each gate's hypotheses and limitations. Classification describes the result type; source/proof status and limitations remain separate. The `current_extensions` join points from an unchanged historical conclusion to a later admitted result, without changing the older gate.

The independent naming/data review caught and repaired an overbroad generic-status classifier, eight section labels initially mistaken for equation labels, 13 omitted AG2 equation labels, and unjoined Round27 equations. Corrections are additive to this new edition; historical records are unchanged.

After ten admissions and the final canonical network refresh, run `python3 -B research/round29/editorial/render_network.py`, then regenerate the integrated text so the final dependency projection is included. The figure preserves external attribution and explicitly aggregates all ten continuum scope-boundary edges. Its JSON companion binds the source graph.

Run `closeout.py` after the advisor writes the post-ten `roadmap.json`; it binds that exact five-goal decision and its ten gates. All current-edition acceptance checks raise explicit exceptions, including under Python optimized mode. Historical copied calculators/audits remain unchanged.
