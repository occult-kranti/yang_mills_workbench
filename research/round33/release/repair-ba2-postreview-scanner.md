# Repair record: BA2 post-review replay and the round phrase scanner

Date 2026-09-25. Authorized by the user (release decision after the first verification run failed; option 1: replay the BA2 post-review with the scanner bytes it pinned). This record changes no gate, review, checker, contract or recorded output.

## What failed

`research/round33/verify_release.py` replays every program listed in `research/round33/skeptic/programs.json` from the archived committed tree. `research/round33/skeptic/ba2_postreview_check.py` (hash-bound by the BA2 gate) pins the round phrase scanner `research/round33/tools/phrase_scan.py` at the bytes it had when the BA2 review ran: sha256 `028af4c14edbb2fae096a91cb723ccefb036e7550088907ef47062774871f67c` (commit 7c4c344). After sub-round 1 the advisor extended the scanner's round vocabulary by three forbidden phrasings (commit 058cd0b, the panel-update-1 vocabulary alignment), giving sha256 `1c31a4958c4a44144c5d4f256db551385d216b86309eadc54a608c5e2a4ff0e2`; the BC1, BC2, BD1 and BD2 post-review programs (also gate-bound) pin those extended bytes. One file cannot carry both pins, so the BA2 post-review replay stopped at its check `phrase_scan_tool_pinned`. All other 30 skeptic program runs (15 programs, normal and optimized Python) replayed byte-identically from the archived tree.

## Cause

An advisor process error: the scanner was edited in place during the round after a gate-bound program had pinned it. The lesson (never edit a pinned tool in place; add a new versioned file and let later programs pin it) is recorded in the Round33 skill note.

## Repair

- `research/round33/tools/history/phrase_scan-028af4c1.py` holds the exact historical bytes (extracted from commit 7c4c344; sha256 above). The difference from the current scanner is the three added phrasings in its round list only.
- `research/round33/verify_release.py` replays `ba2_postreview_check.py` alone in a separate copy of the archived tree in which `tools/phrase_scan.py` is replaced by those historical bytes, after verifying their hash against the pin; the replay output must still equal the recorded `skeptic/ba2-postreview/` byte for byte, in normal and optimized Python. Every other program runs from the unmodified archived tree. The verifier receipt records, for that program, the substituted tool path, the source of the historical bytes and their sha256.
- The BA2 review, gate, checker and recorded output are unchanged; the BA2 admission does not depend on the scanner (the scanner is a wording tool, and the historical version is a strict subset of the current forbidden list).

## Other records that name the historical bytes

The same in-place edit (commit 058cd0b) left three more records naming bytes that no longer exist at the path they give, found by the pre-merge audit:

- The BA1 and BA2 review records `research/round33/skeptic/ba1.json` and `research/round33/skeptic/ba2.json` (both gate-bound) list `research/round33/tools/phrase_scan.py` with sha256 `028af4c14edbb2fae096a91cb723ccefb036e7550088907ef47062774871f67c` among their bindings.
- `research/round33/skeptic/ba2_check.py` records the same hash as the label `PHRASE_SCAN_MIRRORED_SHA256` and never checks it.

The file at that path now has the extended bytes `1c31a4958c4a44144c5d4f256db551385d216b86309eadc54a608c5e2a4ff0e2`; the bytes those records name are kept at `research/round33/tools/history/phrase_scan-028af4c1.py`. Neither `reproduce.py` nor `verify_release.py` checks the bindings inside review records (only gate bindings), so these stale bindings are recorded here rather than detected. The review records and the checker are left unchanged.
