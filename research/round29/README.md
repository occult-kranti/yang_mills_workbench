# Round29 — Hruday / HNM continuation

Human author and project direction: **Hruday N M (BUNZEEY)**. Research, code, review and drafting used AI assistance. The independent model-agent passes share model ancestry and inherited sources; they are not external human peer review or formal proof checking.

This continuation starts from GitHub main commit `20774936cac18a12b93463dda7388846862f40dc`. The authorized research cycle has five goal pairs and ten investigations. Each second investigation is selected from the preceding frozen derivations and independent skeptical review. The last two goals are selected only after the first three pairs are reviewed. Replays, editorial repairs, literature searches and release checks add no investigations.

The current authoritative results and limitations are in [advisor/findings.json](advisor/findings.json). [advisor/plan.json](advisor/plan.json) records the selection rules. A `limited` or `insufficient` verdict is a retained research outcome, not a successful proof of its original target. Counts of investigations, equations and contribution aliases are not percentages of the Clay problem solved.

## Read the current work

- [Complete authored Draft02](../../papers/draft-02/main.pdf), integrating the earlier draft and Round27–29 addenda.
- [HNM naming registry](../../papers/draft-02/registry/hnm-registry.json), with source paths, legacy labels, units, limitations and qualitative priority ranks.
- [Current website](https://occult-kranti.github.io/yang_mills_workbench/) and [research network](network.json).
- [Primary-source assessment](experts/assessment.md), including the requested Gauvin preprint and Clay problem statement.
- [Substack draft](sharing/substack.md) and [Reddit draft](sharing/reddit.md). These are prepared texts, not published posts.

The current presentation uses Hruday/HNM names for project constructions and document aliases. Established theorem names, source authors and standard notation retain their attribution. Historical frozen reports, contracts and gates retain their original bytes. Project naming does not establish scientific priority; no new axioms are asserted.

## Completed cycle

All ten investigations are reviewed: nine accepted within scope and the limited AM1 transfer audit preserved. AM2 gives the explicit finite-volume certificate; AQ1/AQ2 construct a numerical-cap fixed-lattice state with physical gap at least alpha/16 and Wilson variance above 1/5. The separate AO2 energy identity remains tied to the older conditional orthant state. See the [handoff](HANDOFF.md) and [five unexecuted future goals](advisor/roadmap.json).

## Inspect one investigation

For a loop such as `am2`, read `contracts/am2.json`, the two independently frozen reports under `forward/am2/` and `reverse/am2/`, the independent review in `skeptic/am2.md`, and the advisor decision in `advisor/am2-gate.json`. Input copies, manifests, exact controls and result files accompany each report. Review records distinguish the analytic proof from the finite executable fixtures that test its coefficients, geometry and counterexamples.

## Reproduce

Run from the repository root. Use new absolute output directories outside the checkout:

```bash
python3 -B research/round29/reproduce.py --validate-only
python3 -B research/round29/reproduce.py --complete --output /tmp/hnm-round29-normal
python3 -B -O research/round29/reproduce.py --complete --optimized --output /tmp/hnm-round29-optimized
```

`--complete` requires exactly ten reviewed investigations. It refuses incomplete cycles, altered frozen inputs, missing independent review and changed required controls. The normal and optimized runs must reproduce the complete frozen output inventory and every byte, including manifests. A result marked `passed` certifies these recorded checks; it does not prove every mathematical premise by computation.

The [release guide](release/README.md) describes the final clean-commit check, transitive source bindings, deliberately corrupted-evidence tests, historical preservation, exact website rebuild and final PDF verification. Python assertions are not used as acceptance gates.

To rebuild the current presentation after regenerating the manuscript and registry:

```bash
python3 -B research/round29/build_network.py
python3 -B research/round29/build_site.py --require-complete
python3 scripts/build_pages.py
node tests/round29_site.mjs
```

Each finding keeps its exact finite or infinite model, boundary prescription, physical clock and coupling conditions. A fixed-spacing gap or a conditional local-state theorem is not a construction of four-dimensional continuum Yang–Mills theory.
