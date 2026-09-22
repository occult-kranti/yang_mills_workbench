# Fresh output inventory repair

The advisor authorized this administrative repair after release review found that
`replay_artifacts` returned immediately for producers declaring no auxiliary
artifacts. Their `results.json` bytes were checked, but undeclared external replay
files and symlinks could escape the output inventory check.

Every producer replay now validates exactly `results.json` plus its declared
auxiliary files before reading the fresh result. The destination, its ancestors
and its contents cannot be symlinks. Escaping paths, cache/environment entries
and nonregular entries are rejected. Existing result and auxiliary byte
comparisons remain in place. No scientific schema, contract, specification,
gate, review or admission pin changed.

`release/replay_output_controls.py` accepts valid single-file and multi-file
outputs and rejects eight mutations: an extra single-file output, linked result,
linked destination, linked ancestor, empty cache directory, missing result,
escaping destination and changed auxiliary bytes. Normal and optimized runs
passed with identical output. The helper is included in the final admission
test entrypoint; no broad suite or scientific producer was rerun for this repair.

The external repair record preserves the exact prior code, diff, commands,
observed outputs and before/after identities. Its receipt SHA256 is
`8727990cb9c811bdf3171329f8af12202c94fa641a040b64e3ca3f35b3b5db24`.
The prior `reproduce.py` SHA256 was
`73ef7f3e06a1597f59ca44db886c83353382e673c846e272b7a1546725f6bdf4`;
the repaired SHA256 is
`581f2b9bcdcbffafd0a096ed07f3400de2f2af98782980638a0ef06b91ab842d`.
All eight existing admission specifications, gates and reviews, plus their
registry, retained their recorded hashes. This work adds zero research loops
and reads no current AK1 mathematics.
