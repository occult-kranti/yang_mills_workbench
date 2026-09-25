# Round33 release verification

Publication is authorized by the 2026-09-24 user request: continue with the next three rounds (three research sub-rounds of two investigations, BA1-BC2) and then apply the admitted solutions and new equations to their related problems (the applications stage, BD1/BD2), push the resulting research and merge to main. This round extends the merged Round32 history (baseline `519a9a2a26201422a8bfa9e3a83f9129b66b8c88`). The release must preserve all earlier scientific files, the exact Draft03 PDF and the Round31 and Round32 addendum PDFs. Historical `research/`, `papers/` and `evidence/` files are immutable outside `research/round33/` and `papers/round33-addendum/`. Skill instructions under `.codex/skills/` and `.claude/skills/` may be added or extended append-only during the round (the verifier requires each changed skill file's baseline bytes to remain a prefix); the frozen copies the producers used stay under `research/round33/methods/`.

After the eighth skeptical review and gate:

1. Regenerate the research network (`python3 -B research/round33/build_network.py`), the site bundle (`python3 -B research/round33/presentation/build_site.py`) and the GitHub Pages files (`python3 -B scripts/build_pages.py`).
2. Build the addendum (`python3 -B papers/round33-addendum/build.py --render`), run `inspect_pdf.py`, inspect every rendered page and record `papers/round33-addendum/qa.json`; copy `papers/round33-addendum/main.pdf` byte-for-byte to `dist/ym-round33-addendum.pdf` (and rebuild Pages so `docs/ym-round33-addendum.pdf` matches).
3. Run the real-browser QA in final mode (`node tests/round33_browser.mjs --final` with `YM_PLAYWRIGHT_MODULE`, `YM_CHROMIUM_EXECUTABLE`, `YM_QA_OUTPUT`, `YM_SITE_FOLDER=docs`), copy its nine screenshots (`home-desktop`, `home-mobile`, `sources-mobile`, `catalog-mobile`, `network-mobile`, `result-mobile`, `subrounds-mobile`, `figures-mobile`, `applications-mobile`) with unchanged bytes into `research/round33/presentation/final-render/`, view every screenshot, and record `research/round33/presentation/site-qa-final.json` with the screenshot keys rewritten to their repository paths, `checkpoint.completed` 8 and a passed `visual_review` listing every inspected screenshot.
4. Record `research/round33/skeptic/programs.json` (independent skeptic programs and their recorded output directories, including an entry for `bd2`).

Commit those reviewed sources, then run from a clean checkout:

```sh
python3 -B research/round33/verify_release.py --baseline 519a9a2a26201422a8bfa9e3a83f9129b66b8c88 --expected-tree <committed-tree-id> --receipt /absolute/fresh/external-receipt.json
```

The verifier archives the committed tree, validates all eight evidence admissions, rejects coherent evidence mutations (normal and optimized Python), replays every producer in normal and optimized Python, replays the skeptic programs listed in `skeptic/programs.json`, verifies Round32 integrity (`research/round32/reproduce.py --complete --validate-only`), rebuilds network/site/Pages deterministically, runs the current Round33 interface test with `--require-release` and the historical Round32 (`--require-release`) and Round31 interface tests, and verifies the final browser/visual record, the addendum build receipt and page QA, and the preserved PDFs. Hashes and fixtures establish provenance and executed controls; they do not replace the mathematical reports or constitute formal verification.

The historical real-browser script `tests/round32_browser.mjs` cannot pass once Round33 owns the home, drafts, catalog and network routes (it waits for `#r32-finding-search` on `hnm-findings`); the same was true of the Round31 browser script after Round32. Its recorded Round32 receipt remains the historical record; the Round32 archive routes are covered by `tests/round33_browser.mjs` (`round32-results`, `round32-az2`).

Push the exact verified commit to the research branch, open a pull request to main, inspect its head and mergeability, and merge with that exact expected head SHA. Verify the resulting main tree, Pages deployment and served PDF/data bytes. A failure to merge must leave the branch and pull request reviewable with the actual blocker reported. Credentials stay outside the repository.

Repair record: the BA2 post-review program pins the round phrase scanner as it stood at its review; the scanner was later extended, so `verify_release.py` replays that one program in a separate tree copy carrying the committed historical bytes (`tools/history/phrase_scan-028af4c1.py`, hash-verified). See `repair-ba2-postreview-scanner.md`.
