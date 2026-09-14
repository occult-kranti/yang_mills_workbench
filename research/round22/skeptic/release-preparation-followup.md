# Release verifier follow-up, interrupted for Q1 review

Bounded read-only infrastructure review; zero research loops. Q1 preparation
was frozen and neither Q1 producer was read during this review. The advisor
opened both-frozen Q1 review before this follow-up completed; scientific review
now takes priority. No root-owned source was edited and no final release
mutation or ten-loop execution is claimed.

## Reviewed versions

| Source | SHA256 |
|---|---|
| release/final_verify.py | 272a127c7246caaa91baf855ced4a267ad7cd1b24751ec944214365e46bd2590 |
| release/protocol.md | 99833cca01f899a9eaac5f85f7762e2249619d2f90d00df790aeea750a4a3e50 |
| admission.py | a22759910cf716acca371f936ff55f20eb756d9b5feafb6cb50061640a9f6d72 |
| reproduce.py | b421516be9c65a2222fed611ba8964f1a1679dfb79b09c43f35851e6bed449cc |
| build_claim_map.py | 8bfc5b54b23624d84d54b2b11eee772412050d67515e998963f86bc8b1b29a64 |
| build_site.py | 3bfb859c7d133c52417656408b24e21e3527aa3f16e4c3ca469e3616f96f6be7 |
| ../../scripts/build_pages.py | 9f532aa5b6fc90738d18ba6d33ca294bcec1f0e32e6a168531d0b6fb6c5c2e14 |

Paths are relative to research/round22 except the explicitly traversed script.
The initial release-preparation.md is unchanged.

## Repairs visible in source

Canonical in-tree inventory bytes must match the externally pinned file.
Exact loop order, ledger contract/submission/checkpoint bindings, exact reviewed
checkpoint gate sets, integer counts, Boolean passed flags and actual claim-map
hash are now checked. Q/R selection binds six-loop feedback; three distinct
future goals require substantive named fields and bind post-ten feedback.
The claim map references the future roadmap by path, avoiding the former cycle.
Exact current/inherited replay identities, unique admission control identities,
and historical C2 semantic summaries are now checked. The recovered base is
hard-pinned to 382e61571b029e198d87abbeec99d88157d3c168, which the read-only
Git resolution of 382e615 confirms. Commit/tree identity, clean status, ancestry,
historical changed paths and changed-file inventory coverage are inspected.
These are source-review assessments, not a completed final admission.

## Concrete remaining Git gaps

1. git_state does not check whether HEAD is detached. A clean branch at the
   supplied commit/tree satisfies its predicates, despite the protocol requiring
   a detached worktree. Check symbolic-ref status explicitly or narrow the
   claimed machine-enforced guarantee.
2. Clean Git status and exact HEAD identity do not prove that every inventoried
   filesystem byte is present in that Git tree. collect includes ignored files
   under its roots, while git status omits them; such a file can be inventoried
   and executed/copied but absent from the tested/published commit. Likewise,
   tracked paths marked assume-unchanged or skip-worktree can carry modified disk
   bytes without ordinary status exposing them. The current hash collection
   binds disk bytes and git_state binds HEAD, but no predicate joins those two
   identities. Require every inventory entry, including canonical inventory,
   to be a regular blob in the specified tree with exactly matching content;
   retain the external reviewed tree identity for mode coverage. This matters
   even when all internally regenerated inventory hashes are consistent.

Proposed isolated final controls: an attached clean candidate; an ignored,
inventoried extra file absent from HEAD; and a tracked source modified after
setting assume-unchanged or skip-worktree. Supply coherent newly reviewed
candidate inventory hashes so rejection must come from provenance, not stale
hashes. These controls have not been executed here. The unchanged external
inventory pin still correctly rejects coherent rebinding under the old pin.

Additional source-review boundary: checkpoint findings accept any nonempty
string/dictionary, and ranked_candidates only requires a list of length two.
This cannot establish substantive review content; the actual four-way checkpoint
must still be read. No claim is made that the existing checkpoint is defective.
Final mutation testing, Git-tree export validation and publication/deployment
checks remain for the completed ten-loop candidate.
