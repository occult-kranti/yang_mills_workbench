# Release verifier: bounded source repair check

Q2 independent preparation was frozen before this read-only infrastructure
follow-up. Current Q2 producers remain unread. No final release mutation or
new research loop was executed and no root-owned file was changed.
The previous two preparation records remain immutable.

Reviewed full revised final_verify.py SHA256
`e58e0a824fc0cdfe0b4fd5183e5a7c6270533359d0cfbea4e522816439a79605`
and protocol.md SHA256
`a2b2cfed0c4ab38cdb3717a2e26c59877458c1f667ba2051aa6797ad85dfd309`.
Both paths are in research/round22/release.

The two Git findings in release-preparation-followup.md are addressed in
source. git_state explicitly requires symbolic-ref's detached status. For
all inventoried files and the canonical inventory it now reads the actual
committed tree entry, requires a regular blob, recomputes the Git blob hash
from disk bytes and compares the executable mode. This directly joins the
filesystem inventory to the pinned Git tree, independently of clean-status
shortcuts or ignored files. The required external inventory and commit/tree
pins, historical base check and final revalidation remain in place.
This is a source-level repair assessment; the planned attached/ignored/
assume-unchanged/skip-worktree controls still belong in the final mutation
suite after ten gates exist.

One remaining fresh-build guard was identified. The mirror is initially
seeded with every frozen file, including the generated claim map, generated
Round22 data and entire docs tree. Rebuilding and comparing those existing
outputs cannot reject a builder that returns success without writing them.
Moreover, the already reviewed scripts/build_pages.py only removes unwanted
top-level regular files; a copied nested docs artifact survives the build
without a corresponding dist source and still matches the seeded inventory.
These are newly reviewed-candidate guard gaps, not a bypass of an unchanged
external inventory digest.

Before building each generated claim-map/data output, remove only that output
from the external mirror. Before building Pages, start its docs destination
empty. Retain dist's authored static source assets, because those are legitimate
inputs to the Pages builder. Then compare the complete newly generated file
sets and bytes as already intended. Proposed final controls: a no-op claim-map
builder, a no-op current-data builder, a no-op Pages builder and a nested orphan
docs file must fail the corresponding regenerated-output check. No such mutation
has been executed here. Actual reviewed builder sources currently write their
intended outputs; the issue is whether the release check establishes that
regeneration occurred independently of the seeded copies.

Checkpoint prose substance, source interpretation, browser inspection and
remote/deployment provenance retain their explicitly human review boundaries.
No full ten-loop admission or publication approval is claimed by this note.
