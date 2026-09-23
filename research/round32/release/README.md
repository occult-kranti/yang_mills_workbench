# Round32 release verification

Publication is authorized by the 2026-09-23 user request: execute the ten-investigation expert-panel cycle, push the resulting research and merge to main. This round extends the merged Round31 history (baseline `1a686cd`). The release must preserve all earlier scientific files, the exact Draft03 PDF and the Round31 addendum PDF.

After the tenth skeptical review and gate, regenerate the research network, site data and GitHub Pages files, build the addendum PDF, inspect the rendered pages and the desktop/mobile browser renders. Commit those reviewed sources, then run from a clean checkout:

```sh
python -B research/round32/verify_release.py --baseline 1a686cdf9808aca9b5811dbf23e78bd2be1201f9 --expected-tree <committed-tree-id> --receipt /absolute/fresh/external-receipt.json
```

(Use the full baseline SHA of the Round31 merge commit as recorded in `git log`.) The verifier archives the committed tree, validates all ten evidence admissions, rejects coherent evidence mutations, replays every producer in normal and optimized Python, replays the skeptic programs listed in `skeptic/programs.json`, verifies Round31 integrity, rebuilds network/site/Pages deterministically and verifies the final visual/source inventories. Hashes and fixtures establish provenance and executed controls; they do not replace the mathematical reports or constitute formal verification.

Push the exact verified commit to the research branch, open a pull request to main, inspect its head and mergeability, and merge with that exact expected head SHA. Verify the resulting main tree, Pages deployment and served PDF/data bytes. A failure to merge must leave the branch and pull request reviewable with the actual blocker reported. Credentials stay outside the repository.
