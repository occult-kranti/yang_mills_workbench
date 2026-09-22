# Round27 reproducibility and exact-tree release

The release verifies exactly the three investigations selected in
`research/round27/advisor/sequence.json`. It is a targeted check of this round,
not a rerun of every historical calculation and not a Yang–Mills proof.

`reproduce.py` checks the required contract, model, claim scope, two producers,
instruction snapshots and skeptical review. It checks every declared SHA256 in
the contract, gate, producer bindings, instruction manifests, producer freeze
files and skeptical review against the actual source. Required evidence cannot
be omitted merely by deleting its hash from a gate. Unsupported machine-readable
continuum-proof flags are rejected. Admission uses explicit exceptions, so
`python -O` does not disable it.

## Explicit gate/review scope reconciliation

Gate and review limitations need not have identical wording. The original AI1,
AI2 and AG1 scientific records are immutable. The verifier binds the exact reviewed
claim projections in `REVIEWED_SCOPES`: the gate's loop, model, verdict, accepted
statement and limitations; and the review's schema, admission boolean, verdict,
supported statement and limitations. The projections use sorted compact UTF-8
JSON. Any changed statement or removed limitation requires a new explicit
reviewed reconciliation. Their complete source files are also hash-checked.

The effective admitted scope is the **conjunction of both lists**. The external
replay receipt preserves every gate and review limitation. AI1's and AG1's lists are equal.
AI2's seven review restrictions are reconciled as follows:

| AI2 skeptical restriction | Gate location / retained admission condition |
| --- | --- |
| All nine simple-ratio comparisons are insufficient | The accepted statement says every simple-ratio comparison remains insufficient. |
| Only the named pair is distinguished; no continuous inverse | First gate limitation. |
| Enormous physical time, tiny extra-error allowance, no feasible apparatus | Second gate limitation gives `2e48 hbar/alpha` and no practical measurement; the complete-disk condition is essential. The review's explicit extra-error restriction remains part of admission. |
| No actual physical calibration | Second gate limitation. |
| No homogeneous generator matching | Fourth gate limitation. |
| No continuum construction or mass gap | Fourth gate limitation. |
| Scientific priority is unverified | Fifth gate limitation. |

The gate additionally requires complete error disks and the new ten-link seed.
Reconciliation does not turn an omitted short-form phrase into a stronger claim.
Mutation checks remove restrictions independently from each side, inflate either
accepted statement, and introduce objections; each must be rejected even under
`-O`. This record changes admission machinery only, not the accepted mathematics.
The independent model-agent reconciliation review is recorded in
`research/round27/skeptic/release-scope-review.json`; admission requires its exact
AI2 claim projections and complete effective limitation list.

## Replay and release commands

Every producer is executed with its documented `--output` interface into a fresh
absolute external directory. Its `results.json` must match the committed bytes.
The full release runs all six producers normally and with `-O` (12 executions).
Independent skeptic checkers use their documented fixed JSON output paths; both
interpreter modes must leave those files byte-identical. Replays and mutation
checks are verification work, not additional research loops.
The release also reruns each available, review-bound `*_compare.py` entry point
against its fixed `*-comparison.json` output (including AI2's 248 post-exchange
checks and recorded producer replay inputs).

For a targeted working-copy replay while later loops are still being researched:

```sh
python3 -B research/round27/reproduce.py --loops ai1 --output /tmp/ym27-ai1-fresh
python3 -B research/round27/test_admission.py --loops ai1
```

After the advisor has committed the complete candidate, create a **new detached
worktree** at that exact full commit. Run the verifier from that worktree, with
the full commit and tree IDs from `git rev-parse HEAD` and
`git rev-parse 'HEAD^{tree}'`:

```sh
python3 -B research/round27/release/verify.py \
  --expected-commit FULL_COMMIT_ID \
  --expected-tree FULL_TREE_ID \
  --output /tmp/ym27-release-fresh
```

The verifier refuses relative/existing/internal receipt directories, an attached
branch, mismatched IDs or a dirty worktree. Historical `research` outside Round27,
`evidence`, and all of `papers/draft-01` must be unchanged from base `9b5a41d`.
It deletes the generated Round27 data, network and `docs` only in this disposable
worktree, reruns `build_site.py` and `npm run build`, then compares the complete
Round27, `dist` and `docs` file sets and bytes with their clean committed baseline.
It runs Round27, Round26, Round25, workbench and general UI tests, plus any
draft-specific JavaScript tests present. The final worktree must remain clean.

The external receipt records the exact tested commit/tree, command vectors,
exit codes and hashed logs, producer and skeptic counts, subtree file counts,
and any failure. `receipt.sha256` authenticates the receipt bytes. The receipt
is not written back into its own tested tree: doing so would create an untested
commit and self-reference. Publication should push the exact verified commit;
any subsequent code or evidence change requires a new candidate verification.

If an authenticated GitHub API creates a commit with the same tested Git tree
but different author, committer or message metadata, the new commit ID is a
different release identity. Fetch it, confirm the full tree ID, create a fresh
detached worktree at that remote commit, and rerun this verifier using its own
full commit and tree IDs. The verifier supports either commit because it checks
both supplied IDs against the actual checkout. A matching tree alone does not
turn the earlier receipt into a receipt for the new commit. Preserve the remote
candidate's external receipt and use that exact reviewed tree for the merge.

Hashes certify source identity, not mathematical truth. Separate model-agent
reviews are correlated computational assistance, not historical-person approval
or external peer review. The continuum construction, uniform gap and physical
matching remain governed by the reports' explicit limitations.
