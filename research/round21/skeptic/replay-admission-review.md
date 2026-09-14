# Round21 replay admission review

The I1 scientific results remain unchanged. I found concrete release-boundary
defects and repaired only `research/round21/reproduce.py`; the admitted I1 gate,
comparison source and producer sources were preserved.

The prior path helper rejected a symlink only at a file's final component. A
byte-identical source reached through a linked role directory could pass. Gate
paths were read without that check. The amended helper inspects every lexical
parent before resolution, including the gate file, rejects unsupported loop
identifiers, and requires valid lowercase SHA-256 digests.

The earlier replay compared only `results.json`, leaving auxiliary output and
fresh manifests unchecked. It also admitted fresh comparison output based only
on `status=accepted`. The wrapper now requires and checks each producer's
source-manifest input/output closure against the reviewed gate. All fresh
scientific output files, including manifests and controls, must match the gate
and original evidence byte for byte. The complete fresh comparison must match
its reviewed file and contain actual rejecting controls. Top-level result
identity and status types are checked explicitly, and the gate's hash cannot
change during replay. The wrapper never generates a gate or new expected hash.

The frozen `compare-i1.py` also has a narrow standalone limitation: Python tuple
comparison accepts `reverse.passed=1` in place of `True`. I reproduced this
without changing its source. Full replay rejects that forged result through
expected byte/hash comparison and strict status type checking. The frozen
comparator is therefore not a standalone general admission boundary. Later
comparators should use type-preserving canonical comparison, as the advisor
has arranged. This limitation does not alter I1's exact geometry results.

`test_replay_admission.py` creates isolated copies and exercises sixteen
discriminating controls: omitted manifest/input/output/comparison entries,
tampered expected result hash, four linked parent levels, a linked gate file,
invalid loop identifiers, a wrong geometric count with unchanged success
status, an emptied auxiliary control file, and an accepted comparison with
its mutation evidence removed. All sixteen reject under ordinary and optimized
Python, producing identical reports. Fresh ordinary and optimized I1 replays
also pass against the strengthened wrapper.

Run with fresh destinations:

```bash
python -B research/round21/skeptic/test_replay_admission.py --output /tmp/ym21-admission.json
python -B -O research/round21/skeptic/test_replay_admission.py --output /tmp/ym21-admission-opt.json
python -B research/round21/reproduce.py --loops i1 --output /tmp/ym21-replay
```

The inventory is anchored in the reviewed gate and its Git history. This is not
a signature scheme protecting against an attacker authorized to rewrite both
the gate and validator. Frozen gate generation and replay validation remain
separate activities. Administrative gate inventory revisions must preserve
their prior bytes and be reviewed explicitly.
