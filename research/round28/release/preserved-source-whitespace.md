# Preserved source whitespace

The final staged `git diff --check` reports one trailing blank line at EOF in
each of these source-bound files:

- `research/round28/experts/jung/triage.md`
- `research/round28/experts/source-survey.md`
- `research/round28/forward/ai3/inputs/research/round28/experts/jung/triage.md`
- `research/round28/reverse/ai3/inputs/research/round28/experts/jung/triage.md`
- `research/round28/skeptic/ai3-inputs/research/round28/experts/jung/triage.md`

These reviewed source bytes and owned snapshots are deliberately unchanged.
Their frozen SHA256 bindings take precedence over cosmetic normalization.
The staged whitespace check is also run excluding only these five exact paths;
no other whitespace finding is accepted by this exception.
This packaging note changes no scientific result or admission.

The separately reviewed administrative portability correction adds two exact
unified-diff records:

- `research/round28/release/ah-portability/ah1/checker.diff`
- `research/round28/release/ah-portability/ah2/checker.diff`

Blank context lines in unified-diff syntax contain the required leading space.
Git's generic whitespace check flags those lines and the trailing context.
The records are preserved exactly because both repair validators reconstruct
and compare the complete diffs. The subsequent staged whitespace check excludes
only these two exact diff-record paths; no checker source is exempted.
