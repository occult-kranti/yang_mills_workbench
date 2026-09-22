# AK1 freeze path convention

Both frozen AK1 `freeze.json` records use `files` with repository-relative
keys. The older `files` convention prepended the producer directory, so the
initial proposal validation rejected a doubled source path. The advisor
approved an explicit `freeze_path_base: "repository"` for AK1 `files` only.
Other loops retain the previous default; `sha256` and `bindings` conventions
are unchanged.

The extension requires every key inside the current producer's owned directory,
ordinary safe repository paths and matching file hashes. Its key set must equal
every owned file except the exact top-level freeze itself. Nested input freeze
records remain included. The current frozen totals are 85 forward files and 65
reverse files; future commentary belongs outside those frozen directories.
No scientific bytes, admission specification or existing pin was rewritten.

Both actual producer closures pass. Sixteen in-memory controls, eight per
direction, reject wrong or unknown namespaces, a foreign producer path,
traversal, absolute paths, missing input freeze metadata, a missing owned
checker and a changed source hash. Normal and optimized controls have identical
output. The first test-only selector assumed the forward input freeze was
nested; its failure is preserved, and the selector was corrected to the actual
top-level `inputs-current-freeze.json`. No producer was executed for this repair.

The external receipt preserves the initial namespace rejection, test-only
selector failure, prior code, diff and all observed commands/results. Its SHA256
is `32c0b3564dd63d2e8fe53acb9852cfdac69e1903f48d26d1fd518fdfa4df8ff6`.
The `reproduce.py` digest changed from
`581f2b9bcdcbffafd0a096ed07f3400de2f2af98782980638a0ef06b91ab842d`
to `6ebf9b5116aba99cae5432796b890745872d7785d1bdedd8afee17d2a517b5fd`.
The eight admitted-loop registry and both current producer
freeze/checker/report/result identities remained unchanged. This administrative
repair adds zero research loops and supplies no mathematical result.
