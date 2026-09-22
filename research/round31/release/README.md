# Round31 release verification

Publication is authorized by the 2026-09-22 user request: execute three reviewed investigations, push the resulting research and merge to main. This round extends the already merged Round29–30 history. The release must preserve all earlier scientific files and the exact Draft03 PDF.

After all three skeptical reviews, regenerate the research network, addendum download, site data and GitHub Pages files. Inspect the final PDF pages and real desktop/mobile browser renders. Commit those reviewed sources, then run from a clean checkout:

```sh
python -B research/round31/verify_release.py --baseline eb3d61f0a047caa5931b2d0793de68b45d71a547 --expected-tree <committed-tree-id> --receipt /absolute/fresh/external-receipt.json
```

The verifier archives the committed tree, validates all three evidence admissions, rejects coherent evidence mutations, replays six producers in normal and optimized Python, verifies historical Round30 integrity, rebuilds network/site/Pages deterministically and verifies the final visual/source inventories. Hashes and fixtures establish provenance and executed controls; they do not replace the mathematical reports or constitute formal verification.

Push the exact verified commit to the research branch. Create a pull request to main, inspect its head and mergeability, and merge with that exact expected head SHA. Verify the resulting main tree, Pages deployment and served PDF/data bytes. A failure to merge must leave the branch and pull request reviewable with the actual blocker reported.

Credentials stay outside the repository and website. GitHub Pages publishes `main:/docs`. Release receipts are external to the tested source tree so they cannot recursively change their own tree ID. The merge and live deployment status are reported separately from source verification.
