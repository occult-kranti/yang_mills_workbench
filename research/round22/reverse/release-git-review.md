# Independent release Git-stage harness

This is bounded infrastructure work adding zero research loops. Every frozen
reverse/r2 byte is preserved. No root worktree commit or publication was made.
The harness tests the real `release/final_verify.py:git_state`; it does not
call a mocked predicate and does not claim final release admission.

The reviewed verifier SHA256 is
`55946920fcc75bf6d06d81c5ee7fa7c6854640ad219ed9c0aace13f6c8a64419`.
Its imported admission.py SHA256 is
`a22759910cf716acca371f936ff55f20eb756d9b5feafb6cb50061640a9f6d72`.
The release protocol, team protocol, and all three skeptical
release-preparation records were read. The skeptical source assessments
identified the detached-HEAD and hidden-filesystem provenance obligations;
this harness exercises their actual revised predicates.

| Additional reviewed input | SHA256 |
|---|---|
| release/protocol.md | `f375ed8dacc3777164cedac96ae95f8ffd6eb31e394e145e7e2046bc3e26f3db` |
| methods/team-protocol.md | `6249e2ee14901fa6a8cf4dc6e4c98c4190c80e6ee270471eb36826781e02d4a1` |
| skeptic/release-preparation.md | `dfc1377458144081cab47825d434f987b392b7ac999a618bafc74a28f2e673ce` |
| skeptic/release-preparation-followup.md | `08c6aabd2b7b4d33cba2f221bfc465d97c20344fcbdac3f84314ac14f4512715` |
| skeptic/release-preparation-second-followup.md | `e44daf71d02cfee63b50a875daae9a2d6bfabaccce27f5906c51fe534e623e5f` |

These input paths are relative to research/round22. The executed harness
source SHA256 is
`874626031ddd829a3b554e1c73b9a990eb2fda287df89290341967e632bffb85`.

## Isolated execution and intended rejection

`check_release_git.py run` requires an externally supplied candidate path,
exact commit/tree, canonical inventory SHA256, and the reviewed verifier
source SHA256. It first checks inventory-to-disk consistency and requires
the candidate's actual Git stage to pass in ordinary and optimized Python.
This is a prerequisite, not a substitute for validate(), preflight(), the
research replays, build checks, browser review or final release verification.

The candidate is cloned to an independent external bare seed using
`--no-hardlinks`. Each case has a fresh detached clone with a separate
index, configuration, exclude file and references. Its borrowed object store
is the disposable seed, never the original candidate. Fixture commits use
fixed identities and dates, disabled hooks and signing, and no network or
push. Inherited GIT_* environment settings are cleared so an external index
or worktree variable cannot redirect writes into the source repository.

Each untouched clone must independently pass before mutation. A new Python
process loads the unchanged verifier directly from that clone and confirms
that both its ROOT and the actual imported admission module belong there.
Only a ValueError raised by the real git_state call can count as a rejection;
setup/import errors fail the harness. Ordinary and optimized responses must
match exactly. Every mutation must leave ordinary Git status clean and
release inventory file hashes consistent with disk, ensuring that a dirty
status or stale inventory cannot mask the intended predicate.

| Case | Concrete mutation | Required actual rejection |
|---|---|---|
| Attached HEAD | Create a clean branch at the same pinned commit/tree | Detached HEAD required |
| Wrong commit | Supply the real recovered-base commit while keeping the candidate tree pin | Reviewed commit changed |
| Wrong tree | Supply the real recovered-base tree while keeping the candidate commit pin | Reviewed tree changed |
| Ignored inventoried extra | Ignore a new disk file through the clone's exclude file, rebind its inventory hash, and commit only the inventory | Inventoried file absent from committed tree |
| Assume-unchanged bytes | Flag README.md, modify disk bytes, rebind and commit only the inventory; verify the original source blob remains committed | Disk bytes differ from committed blob |
| Skip-worktree bytes | Repeat with skip-worktree, verifying its surviving index flag | Disk bytes differ from committed blob |
| Hidden executable mode | Toggle README.md's owner execute bit and set only this clone's core.fileMode=false | Disk executable mode differs from committed mode |
| Historical committed change | Append a newline to the Round21 release inventory, rebind its release hash and commit both changed files | Historical research changed after recovered base |
| Committed uninventoried path | Commit a new path while keeping it outside the canonical inventory | Changed published path outside reviewed inventory |

The coherent mutations use the new fixture commit/tree pins, so their
rejection is not an old external-pin mismatch. The historical case keeps
all inventoried disk bytes equal to committed blobs, isolating the anchored
history check. The uninventoried case likewise reaches changed-path coverage.
The executable-mode case keeps all bytes unchanged and hides the mode change
only from ordinary Git status. The two index-flag cases explicitly inspect
the flags and confirm the modified source was not accidentally committed.

After all nine cases, the original candidate is checked again in both Python
modes and its complete disk inventory is rechecked. Successful output is a
compact results.json and source-manifest.json. They bind the actual verifier,
admission, canonical inventory and harness source; record every fixture's
commit/tree, coherent inventory digest, exact rejection and both-mode equality;
and explicitly set final_release_admission_claimed=false. Disposable cases
are removed after success unless `--keep-fixtures` is specified. Failures
retain their fixtures and a failure.json for diagnosis.

## Development verification already performed

The harness passed all nine intended rejection cases in both Python modes
on a **reduced Git-stage development fixture**, not the final candidate.
The fixture was based directly on recovered commit
`382e61571b029e198d87abbeec99d88157d3c168`, adding only the reviewed verifier,
its admission module, and a minimal stage inventory. No research, semantic,
checkpoint or build acceptance stage was executed. Its provenance is:

| Item | Value |
|---|---|
| Development commit | `663770a492e93481e1969086cd6bc1deb551875b` |
| Development tree | `49eec7b90c8ae9b9b4004615c2103ece34a5b281` |
| Development inventory SHA256 | `77c917d610030e824c6e675f28bc5f718f04efc7eed88421fdfab84902198956` |
| Development results SHA256 | `84d1486d0c4885e4016411b87bb5be1b5bc4939e59758135803eb8bc1bdac747` |

This establishes that the script and its real Git-stage mutations execute
and discriminate in the intended ways. It does not establish that a completed
ten-loop release candidate is valid. The integrator owns that later run,
its external pins, full verification and publication.

## Final-candidate invocation reserved for the integrator

Run from the reviewed harness with real independently checked values:

```bash
python3 -B research/round22/reverse/check_release_git.py run \
  --candidate /absolute/path/to/detached-candidate \
  --git-commit REVIEWED_40_HEX_COMMIT \
  --git-tree REVIEWED_40_HEX_TREE \
  --inventory-sha256 REVIEWED_64_HEX_INVENTORY_SHA256 \
  --verifier-sha256 55946920fcc75bf6d06d81c5ee7fa7c6854640ad219ed9c0aace13f6c8a64419 \
  --output /absolute/fresh/path/outside-source
```

The harness itself executes both Python modes. A changed verifier source
requires a newly reviewed explicit hash; the current default is pinned.
Semantic, checkpoint and fresh-build mutations are deliberately assigned to
the separate skeptical harness. No final-candidate test, full Git-tree release
admission, remote commit, deployment or live-page result is claimed here.
