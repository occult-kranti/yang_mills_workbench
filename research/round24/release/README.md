# Release verification

Run `verify.py` from a clean detached checkout of the candidate commit, with a fresh absolute output directory outside that checkout:

    python3 -B research/round24/release/verify.py --expected-commit COMMIT_SHA --output /absolute/new/release

The verifier requires exactly the ten reviewed Round24 loop IDs, complete/stop metadata, source-bound figure and presentation reviews, and an unchanged historical research tree. It replays every new producer in normal and optimized modes (40 executions) and all six historical Round23 pairs in both modes (24 executions). Independent admission mutation controls, portable skill method tasks, exact regeneration of the published site, and five site/history test suites are separate checks and add zero research loops.

The output receipt records the tested commit/tree, check results and log hashes. The final receipt and tested tree are included in [PR #8](https://github.com/occult-kranti/yang_mills_workbench/pull/8), making the actual release result distinct from this procedure. The API publication must reproduce that exact Git tree, and the merge must use the verified PR head. A deployment check then compares the served Pages artifacts with the released bytes.

The scientific W1 figure was visually inspected and its source/output hashes are bound. The site tests check real script loading, routes, claims, evidence hashes, history and escaping. A browser-based visual audit was not performed; it must not be inferred from the automated presentation checks. Exact arithmetic supports the written mathematical arguments and does not replace external mathematical peer review or prove the continuum theory.
