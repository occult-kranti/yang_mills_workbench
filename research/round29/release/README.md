# Round29 committed-release checks

The release path verifies a **committed Git tree in a clean linked worktree**. It writes every replay, disposable mutation, reviewer output, site rebuild and receipt outside that checkout. The external receipt identifies the tested commit and tree; subsequent changes require a new receipt.

## Admission contract

`admission.py` checks the gate, independent review, both frozen producer inventories, source manifests, copied prospective contracts, declared result controls and reviewed scope. `admission-contract.json` records explicitly reviewed control names and result flags for each loop. AM2 also recomputes the rational self-map, contraction and shifted-resolvent budgets and checks their strict inequalities.

The specification records integrity of the accepted scope and limitations. It is not a semantic truth oracle for arbitrary English, a theorem prover, or a claim to solve continuum Yang–Mills. The separate mathematical reports and independent skeptical reviews remain necessary.

The common skeptic replay helper is already bound transitively by the relevant independent-review JSON. The validator checks that binding and direct local reviewer imports. It does not rewrite earlier gates.

`reproduce.verify()` calls `validate_loop(root, loop, gate=gate, row=row)`. Initial gate recording may use `require_spec=False`: it still requires transitive inventories, counterpart review and true discriminating controls, but a new loop's reviewed semantic specification must be registered before final release. Prior registered specifications are always enforced.

## Mutation checks

```bash
python3 -B research/round29/release/test_admission.py --complete --output /absolute/external/admission.json
```

Each mutation uses a disposable copy. Cases remove a bound source, omit a counterpart or a required check, set a discriminating control false, remove a required control, alter the recorded limitations, or remove the reviewer's counterpart binding. Hashes are coherently updated through producer manifest, freeze, reviewer record and gate for semantic mutations. AM2 also tests a nonstrict resolvent cap and a false infinite-volume claim.

The trusted validator and reviewed semantic specification remain fixed in these attacks. No local validator can defend against replacing both its trusted code and the external receipt that is claimed to bind it.

## Final release

After all ten reviewed loops, complete manuscript, PDF visual review and rebuilt site are committed, create a fresh detached linked worktree at that commit. Run inside that worktree:

```bash
python3 -B research/round29/release/release_verify.py \
  --baseline <commit-before-round29> \
  --expected-tree <release-tree-id> \
  --receipt /absolute/external/round29-release.json
```

The verifier performs these bounded checks:

1. Validate all ten source-bound admissions and preserve protected earlier scientific/artifact bytes against the named baseline.
2. Replay all twenty producers normally and with Python optimization into fresh external output directories, matching the complete recorded output inventory and every output byte, including source manifests.
3. Require the mutation suite to reject coherently rebound bad evidence.
4. Run every independent skeptical validator in an external archive of the committed tree and match its recorded check output. These validators may perform their own additional producer replays.
5. Rebuild the current source-bound site and GitHub Pages assets in that archive; compare `dist/` and `docs/` byte for byte and run current integration checks.
6. Bind the final PDF to `pdf-qa.json`, check every page's text geometry and unresolved references, confirm the human author, inspect the recorded visual-review path, and match both downloadable PDF copies.
7. Confirm the source checkout stayed clean and write the external receipt with repository-relative source paths.

Rendered browser checks are recorded by `tests/round29_browser.mjs` and actual visual inspection in `presentation/site-qa-final.json`, with final screenshots and rendered source hashes. The release helper validates that record against the committed bytes; it does not rerun the browser. PDF visual inspection is recorded separately by the named expert review. Programmed geometry or route checks do not replace visual inspection. These are release operations and add **zero research loops**.
