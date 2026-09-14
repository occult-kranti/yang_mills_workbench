# Release source and complete-candidate Git-control follow-up

This bounded review adds zero research loops and executes no verification
reruns. The earlier harness, review, development evidence and frozen R2
submission remain unchanged. No root-owned source was edited.

The strengthened final_verify.py has SHA256
`68bd34f9a395d41f0cfba422913ac72352bd31cfbe1eb11b13832c8faeed6924`.
I read it in full and compared its function sources with the previously
reviewed `55946920fcc75bf6d06d81c5ee7fa7c6854640ad219ed9c0aace13f6c8a64419`
version. Only validate_replay_summary and verify changed; the extracted
validate_c2_summary is new. The git_state source segment is byte-identical,
with SHA256 `afd4a218aceb0aa7dd2d7cd860b3db404763181e6e1414b66ce1733233eb25c5`.

## Summary guards reviewed in source

The current and inherited replay rows now bind each check.py and results.json
hash to that loop and direction's admitted gate, in addition to the existing
exact pair order and optimized-mode identity. Current output counts require
actual integers and equal the number of that producer's admitted output
files. Current replay summaries also require the exact admitted-gate map
and integer research_loops_added=0. Inherited pair_comparisons requires an
integer equal to the requested inherited loop count. Unknown replay families
are rejected.

These fields match the actual emitters inspected in Round22 reproduce.py
and Round21 reproduce.py: their source/result hashes have the same meaning,
and the current output count includes every bound output file. The extracted
C2 guard retains the required schema, completed status, unoptimized mode,
preserved failed historical gate and three replay identities, while requiring
integer zero additional loops, integer 34 semantic checks, integer 27 rejected
scientific mutations and the exact Boolean historical-equivalence flag.
Those values match the inspected C2 replay writer. verify invokes the new
guard and the strengthened replay guard at the intended stages.

No blocking source defect was found in this bounded review. This is a source
assessment; the separate skeptic owns the summary mutations and remaining
semantic/build execution. No claim of executing those checks is made here.

## Recorded complete provisional candidate

I read all nine records in release/git-controls/results.json and its source
manifest. Their SHA256 binding is
`5fb0de8196fecb796e91997195141a45d7fed341b3b4a055a7ec39c3808e3a93`.
The candidate identities in that executed record are:

| Item | Identity |
|---|---|
| Candidate commit | `693bf3dd20bed5b4fedab22c5877799f215f6632` |
| Candidate tree | `bbac0f1f512f5477affa42dfa8bd75a9965bd485` |
| Canonical inventory SHA256 | `49ba6ceb4713ab3439fd7385ed78415ff197d4884df1fd828ab87165c5f333ba` |
| Executed verifier SHA256 | `68bd34f9a395d41f0cfba422913ac72352bd31cfbe1eb11b13832c8faeed6924` |
| Executed harness SHA256 | `874626031ddd829a3b554e1c73b9a990eb2fda287df89290341967e632bffb85` |

Read-only Git object inspection confirmed the candidate tree and committed
inventory, verifier, harness and admission hashes in the record. The positive
Git-stage receipt establishes detached clean status, matching inventoried disk
blobs, unchanged anchored history and coverage of 504 changed paths for this
specific candidate.

All nine intended cases are present exactly once: attached HEAD, wrong commit,
wrong tree, ignored inventoried extra, assume-unchanged bytes, skip-worktree
bytes, hidden executable mode, committed historical change and committed
uninventoried change. Each records the exact intended ValueError, a strict
rejected=true flag, equal ordinary/optimized outcomes, clean ordinary status
and an inventory coherent with disk. The hidden-byte and historical cases
record their newly committed fixture inventories and commit/tree pins;
the ignored case reaches the absent-committed-file guard. Thus these outcomes
are not merely dirty-status or stale-inventory rejection.

The root performed this complete-candidate execution; I reviewed its saved
source-bound results without rerunning it. This advances the earlier
development-only status to an executed Git-stage control suite on the named
complete provisional candidate. It does not establish later-candidate
identity, full final verification, remote publication, deployment or live-page
status. The record explicitly claims none of those and preserves zero added
research loops. Later release changes still require the integrator's final
externally pinned verification and publication checks.

The unchanged harness defaults to the earlier verifier pin. Its successful
recorded execution binds the explicit newer pin above; any later invocation
must likewise supply the reviewed --verifier-sha256 value. No historical
harness default or earlier review has been silently rewritten.
