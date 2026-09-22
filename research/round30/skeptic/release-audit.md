# Bounded release-tooling audit

**Final status: passed after the two targeted repairs described below. No blocker remains from this bounded audit.**

This is release QA after the three admitted investigations, not a fourth research loop. Existing frozen producer and skeptical evidence was not edited. Scope: `research/round30/reproduce.py`, `test_admission.py` and `verify_release.py`.

The existing twelve damaging-evidence tests pass and reject their mutations for the expected reasons. I additionally copied the current Round30 tree and all externally bound inherited files into two fresh temporary roots. The unmodified `validate(root, complete=True)` passed in each exact temporary environment before its mutation. Both mutations below were then incorrectly accepted.

## Blocker 1: parent-directory symlink accepted

Within the temporary Round30 tree, rename `skeptic` to `skeptic-storage` and create the relative directory symlink `skeptic -> skeptic-storage`. Leave all file contents and hashes unchanged. The complete validator accepts this tree.

`local()` checks `p.is_symlink()` only on the leaf file, then permits any resolved target inside the root. An internal symlink in a parent component therefore passes, contrary to the evidence-path rule requiring rejection of both parent and leaf symlinks. The producer freeze traversal does not protect reviewer paths from this case.

Required correction: inspect every component between the declared evidence root and the leaf, rejecting any symlink, while retaining the existing traversal/root-escape checks. Add this exact mutation to the damage tests after their passing temporary baseline and require a symlink-specific rejection reason.

Observed result: `{"mutation":"parent-symlink","accepted":true}`.

## Blocker 2: executed-check statuses can be erased

Within a separate passing temporary root, replace every AT3 forward `output/results.json` check dictionary with just its unchanged `id` string. Coherently rebind the manifest, producer freezes, review hashes and gate hashes through the existing `rebind(root, 'at3')`. The complete validator accepts the altered evidence, although all explicit `passed` statuses and diagnostic fields have disappeared.

The check logic explicitly treats any string as valid, while the trusted specification pins only the extracted IDs and claims. All actual Round30 producer checks are dictionaries, so allowing this alternate shape is unnecessary and weakens the intended exact-Boolean admission requirement. A later replay of unchanged producer code would reveal the byte mismatch, but the source-bound admission validator itself currently returns a false positive; it must not claim the malformed executed statuses passed review.

Required correction: require the actual Round30 check-record shape, including dictionary IDs and `passed is True`, before comparing the reviewed IDs. Add this coherently rebound status-erasure mutation, with a specific malformed-check/status rejection reason.

Observed result: `{"mutation":"checks-erase-status","accepted":true}`.

## Release integration

Run the expanded damage suite in both normal and optimized Python from `verify_release.py`; currently it invokes the damage suite only normally. The source uses explicit exceptions, and the optimized run should verify the repaired admission gate rather than assuming its behavior. These changes affect release tooling only. They do not require reopening a scientific contract, changing any admitted mathematical statement, or rerunning an additional research investigation.

At this audit checkpoint the two demonstrated admission defects are blockers to calling the tooling audit passed. No further optional audit expansion is requested.

## Targeted repair verification

The advisor repaired the root-owned tooling without modifying the admitted scientific evidence. `local()` now rejects every lexical evidence-path component that is a symlink. Round30 executed checks must now be dictionaries containing a string ID and the exact Boolean `passed is True`; bare ID strings no longer satisfy the admission schema.

The expanded mutation suite includes status erasure separately for AT1, AT2 and AT3, and the original parent-symlink reproduction. I reran that suite independently in normal Python and with `-O`. Both runs validated their unmodified temporary baselines and rejected all sixteen mutations for their declared specific reasons. The new failures are `Missing or failed executed control status` and `Symlink evidence component`, respectively. This resolves both observed false positives without relying on unrelated missing files or stale hashes.

I also inspected `verify_release.py`: it now executes the damaging-evidence suite in both interpreter modes before the normal and optimized producer replays. This completes the requested bounded tooling audit. The full committed-tree release test, PDF QA and remote publication remain the integrator's separate release gates; this audit does not claim they have run.

Verified tooling hashes at this repair check:

- `research/round30/reproduce.py`: `34f611b31f0afcb5b072c3f354c882d2c6c39cd4c986392162752aa9e189be9a`
- `research/round30/test_admission.py`: `52227876bf113a76243bdf9af3256d132ebce2b1193e483a98c3399d894b5912`
- `research/round30/verify_release.py`: `75450e190a51dc5451cb9f918c620145f3fd8c25fd8cc7fb7cde0e2a273d8834`


## Added browser-evidence release gate

After the preceding repair snapshot, the integrator added recorded-browser QA verification to `verify_release.py`. I inspected this added block. It requires the final three-loop render status, no recorded page errors, a passed visual review, all named current source/download bindings, the seven specified screenshot identities and their inspection records, and all fifteen named current/archive routes with explicit absence of mobile overflow. It verifies every recorded source and screenshot hash and rejects unsafe or symlinked evidence paths. The final release receipt records the QA record hash and checked coverage.

This addition is sound within the declared role of verifying recorded browser evidence; it does not pretend to rerun a browser or independently perform the visual inspections. At the time of this bounded code inspection the final `site-qa-final.json` had not yet been written, so I do not assert that its actual contents or screenshots passed. The new gate correctly fails if that record is absent, incomplete or stale. The integrator's final exact-tree run must execute it after recording the final inspection. No completed mutation test was repeated for this code-only extension. The verifier hash above now identifies the extended version reviewed here.
