# Final paper check in the exact-tree release

The release verifier now runs
`python -B papers/round28-addendum/artifact_manifest.py --check` through its
recorded command runner before rebuilding generated network/site files. A
nonzero result fails the release and appears in its external receipt.

The existing paper checker requires a non-draft source record naming ten distinct
loops, matching declared source hashes, the final PDF's matching hash and a
passed visual-review record listing every page. It rejects recorded TeX warnings,
out-of-page words and unexpected/cache artifact files, and compares the complete
current artifact manifest. It checks the recorded visual review; it does not
perform a new visual inspection or recompile the PDF.

A focused AST check verified the exact interpreter/arguments, one invocation,
placement before generated-file deletion, and the shared failure/receipt path.
No final paper check, producer replay or broad test suite was executed during
this wiring change. The bound `reproduce.py` and paper checker are unchanged.
The external wiring receipt SHA256 is
`ccde3c3eb6369c6f18f995e41bff0118c1fc3a50680f4b40f8a0949e5dbda7b8`.
This implementation work adds zero research loops.
