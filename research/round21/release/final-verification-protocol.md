# Round21 final release verification

`final_verify.py` verifies the complete ten-loop release. It creates no research gate, changes no producer or historical scientific file, and counts replays as zero new research loops. The original C2 cache-manifest failure remains an expected failure inside the separately reviewed repair wrapper.

## Review and freeze the inventory separately

Finish the source, site build, method/skill updates, decisions and all ten gates first. The completed ledger and admitted gate set must contain exactly `i1,i2,j1,j2,k1,k2,l1,l2,m1,m2`, without duplicates. Both accepted and limited gates are admitted; a limited scientific target remains limited.

Create a **candidate** inventory in a fresh location outside the source tree:

```bash
python -B research/round21/release/final_verify.py inventory --output /tmp/ym21-final-candidate.json
```

The inventory binds this verifier and protocol, the scientific replay driver, AGENTS, README, package metadata, all Round21 material, repository skills, site source/built files, scripts and tests. It also includes every admitted scientific gate input/output and the repaired C2 inventory closure. Interpreter caches and linked paths are rejected. Any new or removed file in a declared infrastructure tree changes the expected file set.

Review the candidate and its printed SHA-256 separately. The verifier never generates fresh expected hashes while validating. The expected digest is an explicit CLI trust input, not a digital signature. A party able to rewrite both the verifier and its reviewed trust input can change the trust boundary.

For a committed release, the reviewed candidate may be copied to the one designated path `research/round21/release/final-inventory.json`. That exact path is excluded from its own file map; its bytes are instead bound by the externally supplied SHA-256. No other source file is excluded for convenience. This avoids a self-hash cycle. Keep final verification outputs outside the source tree; adding them under Round21 would require a new reviewed inventory.

## Execute the exact candidate tree

Run on a clean `git archive` extraction containing the proposed committed tree. Python standard library is sufficient for all required scientific checks; no Git metadata or installed packages are needed in the archive.

```bash
python -B research/round21/release/final_verify.py verify \
  --inventory research/round21/release/final-inventory.json \
  --inventory-sha256 REVIEWED_SHA256 \
  --output /tmp/ym21-final-replay
```

The command checks all gate source/output closures and feedback hashes, then executes fresh normal **and optimized** complete Round21 replays. Each replay executes twenty directional producers and ten independent comparisons; every auxiliary output is checked by `reproduce.py`. Their scientific source/result hashes must agree across modes. It then runs the repaired C2 wrapper once, which validates its independently pinned inventory, preserves the original cache omission failure, executes the actual C2 calculations/comparison, and checks their exact arithmetic and mutations. Finally the complete release inventory is rechecked to detect source drift during execution.

The output contains logs, fresh scientific outputs, the repaired C2 replay and `final-verification.json`. An execution failure writes a failed final record with the diagnostic. A pre-execution inventory mismatch rejects before a replay directory is created. No stored `passed` field substitutes for fresh execution.

## Optional static-site and historical-base checks

Add `--site` to rebuild the site in a complete bound-file mirror under the external output directory. First the actual `research/round21/build_site.py` renderer runs there and must report all ten displayed loop gates verified. Its generated `dist/research-round21.js`, the stylesheet, and `dist/index.html` must match their bound bytes; the whole dist file set is also compared. This rejects stale generated claims or an unreviewed asset change. Then the actual `scripts/build_pages.py` transport builder runs in the mirror and rebuilt docs must match bound docs exactly. Both builders use destinations relative to their source, so the mirror permits executing them without modifying the release. If Node is available, `tests/test_workbench.mjs` runs by default. Node unavailability is recorded explicitly; it is not reported as a passing UI test.

Use repeatable `--site-test tests/NAME.mjs` to select additional or alternative bound Node checks; this implies `--site`. Each test must be in the reviewed inventory. These are static/Node checks, not browser visual verification. A site change or stale docs must be built and reviewed **before** the final inventory is frozen.

In a Git checkout, add `--check-base` to require that all Round19/20 files remain unchanged against `execution.json`'s recorded base commit and that no untracked historical files were introduced. In a Git archive omit this flag; the report says that the base comparison was not requested, while admitted historical hashes and repaired replay remain mandatory. This optional check does not silently claim Git verification when metadata is absent.

## Preflight and structural rejection controls

```bash
python -B research/round21/release/final_verify.py preflight --output /tmp/ym21-preflight.json
python -B research/round21/release/final_verify.py self-test --output /tmp/ym21-final-structural-controls.json
```

Preflight rejects an incomplete nine-loop ledger or a missing M2 gate before any scientific execution. It records the rejection in the fresh external JSON and exits nonzero. Structural controls explicitly reject missing M2, duplicates, an unexpected loop, Boolean counts, counting repairs as loops, unsafe/cache paths and duplicate JSON keys. They are infrastructure controls, not additional research or a substitute for the final clean-tree run.
