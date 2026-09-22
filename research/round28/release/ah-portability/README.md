# Proposed AH1/AH2 administrative portability correction

The original AH1 and AH2 reverse checkers decide whether to check a recorded
repository instruction by comparing its original absolute path with the current
checkout root. The first detached release exposed that location-dependent branch.
The advisor decision and complete failed-run evidence remain separately bound.

The full checker copies in `ah1/check.py` and `ah2/check.py` change only the root
and original-data directory declarations, the eight-entry repository-origin map,
the branch resolving those originals to the current checkout, and one additional
binding identifying the portable checker actually executed. Each `checker.diff`
is the complete textual difference. The additive runner reconstructs that exact
transformation from the frozen original source and instruction inventory; any
additional source edit is rejected. External installed origins are never opened.

AH1 retains all 320 checks and AH2 all 717. The complete expected results retain
every original value and binding, adding exactly the portable-checker binding.
AH1's basis, graph and magnetic sidecars remain byte-identical. The initial four
normal/optimized runs from a fresh unrelated checkout are recorded in
`relocated-replay-evidence.json`; they are administrative verification, not new
experiments or research loops. Nothing is removed from fresh outputs or normalized
before comparison. Original science, reports, outputs, gates, admission metadata,
the ten-entry registry and `reproduce.py` remain unchanged.

`manifest.json` binds the original admission evidence, this proposal, both copied
scripts, exact expected files, complete diffs, the advisor decision/failure record
and the additive `research/round28/portable_reproduce.py` runner. The caller must
supply its full digest through `--manifest-sha256`; final release integration is
subject to independent skeptical acceptance and the advisor's explicit pin.

The runner first validates all ten original admissions. It then uses the original
implementation for eighteen producer entries and only these two declared reverse
copies. Complete fresh file sets, safe paths, all result bytes and every auxiliary
file are checked. `--repair-only` is a disclosed proposal-verification mode that
executes only the two copied scripts; final release must omit it. `--validate-only`
checks the original admissions and complete repair without executing producers.

No release verifier or general release documentation is changed by this proposal.
Independent mutation review and a new exact-tree release remain required.
