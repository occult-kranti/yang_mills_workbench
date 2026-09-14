# Round22 release scaffolding: bounded independent review

This is a read-only infrastructure review, adding zero research loops.
No current P2 producer was read. The ten-loop candidate does not yet exist,
so the tests below are prospective rejection tests, not claimed end-to-end
executions. No root-owned file was edited.

Reviewed versions:

| Source | SHA256 |
|---|---|
| release/final_verify.py | e6668eb7d1bd10ea3e1d29ef7f530312b94158b9ca95124647d13549b731e35d |
| release/protocol.md | 70cbb622842a3b8f0b87e929b216c244f64709e42b3a7268a53135ee4e988f46 |
| admission.py | a22759910cf716acca371f936ff55f20eb756d9b5feafb6cb50061640a9f6d72 |
| reproduce.py | b421516be9c65a2222fed611ba8964f1a1679dfb79b09c43f35851e6bed449cc |
| Round21 release/final_verify.py | 4b9f528467effcebe2a68ddff18af2dd1167821aaa2ddcdf93de4b3035a2edc3 |

All paths except the final row are relative to research/round22. The related
admission/replay code was inspected to distinguish missing release checks
from checks already performed by its dependencies.

## Concrete gaps in this scaffold

1. **Canonical inventory identity.** validate() checks the digest of the
   supplied path, while collect() always excludes the canonical in-tree
   final-inventory.json. A valid external copy can therefore be supplied
   while the in-tree excluded file is stale or absent. Either require the
   supplied inventory to be the canonical file or independently require that
   canonical file's bytes to have the externally supplied digest.
2. **Checkpoint content and chronology.** Each skeptical checkpoint currently
   needs only a completed count and passed=true. A minimal object omitting
   reviewed gates, substantive findings and ranking can satisfy that test.
   The ledger's checkpoints are ignored, as are its per-row contract and
   submission hashes. Second-loop dependencies and post-six selection hashes
   provide useful logical ordering, but the final ten-loop audit has no
   comparable exact reviewed-gate closure. Floating counts also satisfy the
   checkpoint equality. Require exact schemas/types, identities, reviewed
   gate sets, ledger bindings and an explicit ordered checkpoint record.
3. **Future roadmap content and dependency.** Three null or empty goals plus
   executed=false satisfy the present roadmap test. It does not bind the
   post-ten audit or its claim map. Require three distinct substantive goals
   with their selection evidence and an exact post-ten review dependency.
   The integrator separately identified a claim-map/roadmap cycle and plans
   to replace the map's future-roadmap embedding with its path. This is the
   integrator's finding, not an independently executed skeptical check.
4. **Git provenance and historical immutability.** The inventory binds the
   selected current files and historical scientific/C2 closure well, but
   recomputing those hashes establishes present consistency, not that all
   historical gates and files equal the verified base. The verifier does not
   inspect a Git tree, parent, index or clean status. A live dirty workspace
   or an export from another tree can be tested under the same protocol
   wording without the script detecting the provenance error. File-byte
   hashes alone also omit Git modes and files outside the collection roots.
   Bind the exact candidate tree and verified base, and verify historical
   immutability against an anchored base rather than only newly collected
   self-consistent hashes. If an archive is used, provide an independently
   checked export/tree receipt; do not assume it contains Git metadata.
5. **Execution/control identity hardening.** Current replay validation counts
   20 rows but does not itself require each loop/direction exactly once.
   Mutation validation counts at least 16 rejected rows without checking
   control identities. The inspected bound replay implementations generate
   the intended rows, so this is a release-summary guard to add, not a claim
   that their present runs are false. Require the exact identity sets and
   verify inherited replay/C2 result semantics before reporting their counts.

The external inventory digest check itself is effective: coherently rebinding
file hashes changes the inventory digest and is rejected under the original
reviewed pin. The deficiencies above concern what a newly reviewed candidate
must establish; they do not bypass an unchanged external pin. Recursive
current/historical collection, cache rejection, dependency hashes, ordinary/
optimized replay, external build mirrors and final source revalidation are
useful existing safeguards.

## Rejection suite for the completed candidate

Run both Python modes on external copies; preserve accepted source evidence.
Test each semantic mutation with all affected internal hashes coherently
rebound in a newly generated candidate, so stale-hash rejection does not
mask the intended predicate. Keep external-pin tests distinct.

| Mutation | Required result |
|---|---|
| Rebind changed source/inventory, retain original reviewed external pin | Reject digest change |
| Supply valid external inventory but alter/delete canonical inventory | Reject canonical identity |
| Remove, duplicate, reorder or append a loop; wrong ledger contract/submission hash | Reject exact execution/binding drift |
| Empty checkpoint, floating count, false/string passed, missing/extra/wrong gate binding | Reject checkpoint semantics |
| Place post-six before P2, omit its ranking, or unlink Q/R selection from it | Reject checkpoint/selection order |
| Empty or duplicate roadmap goals; missing post-ten review/map binding | Reject future selection |
| Alter historical gate/source and coherently rebind present inventories | Reject anchored historical drift |
| Dirty index/worktree, wrong tested tree or base, changed file mode, untracked export discrepancy | Reject provenance mismatch |
| Twenty repeated producer rows or sixteen repeated mutation identities | Reject execution/control identity |
| Source rebuilt claim map, dist or docs differs from frozen bytes | Reject rendering drift |

Control passes should separately establish one canonical clean candidate,
the exact 20 distinct producer pairs in each mode, required unique mutation
identities, and unchanged historical/C2 semantics. Actual publication still
needs separate verified commit/tree, parent, deployment and live-page records.

## Planned repair and checkpoint interface

The integrator acknowledged findings 1-4 and plans corresponding repairs;
those revised sources have not been reviewed here. Future skeptical
checkpoint JSON will use schema ym22-checkpoint-review-v1, integer
completed_research_loops=6 or 10, Boolean passed, an exact loop-ID to gate-SHA
reviewed_gates map, nonempty concrete findings, and continuum_status="open".
Post-six includes ranked_candidates; post-ten includes claim_map_sha256.
This records the agreed interface only. Neither checkpoint has been authored
or admitted by this preparation, and Q/R remain unselected.
