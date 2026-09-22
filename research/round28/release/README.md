# Round28 admission and release

The selected sequence grows during the investigation. The completed loops must
be its prefix; at most one further selected loop may be active. The first three
goal pairs retain their initial labels. The last two goals cannot be selected
before six reviewed loops. The final release requires exactly five pairs and
ten completed loops; preflight, tests, repairs and replays count as zero loops.

## Current work

```sh
python3 -B research/round28/reproduce.py --preflight ag2
python3 -B research/round28/reproduce.py --validate-only
R28_REPAIR_SHA=f2032dd55e5c2ffce75a76147e20aae8d769f27fdb3db3bcb2a9af7157f18671
python3 -B research/round28/portable_reproduce.py --manifest-sha256 "$R28_REPAIR_SHA" --output /tmp/ym28-fresh-normal
python3 -B -O research/round28/portable_reproduce.py --manifest-sha256 "$R28_REPAIR_SHA" --optimized --output /tmp/ym28-fresh-optimized
python3 -B research/round28/test_admission.py
python3 -B -O research/round28/test_admission.py
```

Preflight reads declared inputs only. The frozen `reproduce.py` preserves its
original prefix and `--loops` interfaces, but its full AH replay is dependent
on the original checkout path. The current portable runner requires all ten
admissions and the explicitly pinned administrative repair. It executes
eighteen original implementations plus the AH1/AH2 reverse portable copies.
Output directories must be new, absolute and outside the repository. Every
fresh complete output must equal its declared stored bytes. Python optimization
never disables admission checks. The [repair approval](../advisor/ah-portability-admission.json)
binds the independent review; the [initial failure](../advisor/ah-portability-failure/)
and [exact source diffs](ah-portability/) remain recorded. Only the actual
portable-script binding is added to each affected result; every original
mathematical value, check, count and auxiliary file stays exact.

## Per-loop admission

The advisor owns frozen contracts, gates and the additive
`advisor/<loop>-admission.json`. Release proposals are separate documents and
confer no scientific admission. The completed gate binds both producer closures,
their current freezes, the skeptical report/JSON and the admission specification.
The skeptical JSON also binds the specification and current producer evidence,
and declares an explicit empty `blocking_issues` list.

The admission specification has schema `ym28-admission-v1`, its loop label,
portable `bindings`, two `producers` entries, and `skeptic_checkers`.
Each producer entry contains:

- `source_manifests` and `instruction_manifests`: exact portable manifest paths.
- `required_snapshots`: the complete snapshot path-to-SHA256 map. It includes
  every declared contract source, the contract itself and all used instructions.
- `adoption_records` and `freeze`: current provenance and immutable freeze paths.
- `binding_field`: `bindings`, `sources`, or AI3 forward's `source_inventory`,
  matching the frozen producer schema. The last convention also requires the
  executed relative `producer_bindings` map; it cannot omit script or manifest.
  AJ1 forward explicitly uses `aj1_provenance_pack` and `input_pack`: result
  provenance binds the executed script, contract and immutable input pack, which
  must bind every source and instruction snapshot through its typed manifests.
- Optional `freeze_binding_field`: `files`, `sha256`, or `bindings`. The default
  preserves the previously admitted producer convention.
- Optional `report_binding`: defaults to `output_and_freeze`. AI3 forward uses
  the explicit `freeze` convention because its report was bound after output.
- `semantic_controls`: stable identities, JSON pointers and exact expected values.
- Optional `rational_relations`: exact typed arithmetic comparisons over recorded
  fields, including complete sum, transport and denominator identities.
- Optional `output_artifacts`: auxiliary JSON basenames, their SHA256 values and
  pointers to those hashes in the producer result. Each artifact is checked
  against disk, the current freeze and gate; declared multi-file outputs reject
  additional files and links, and replay compares every artifact byte for byte.
  AJ1 alone allows explicit `binding: "freeze"` for forward `source-manifest.json`
  and reverse `geometry.json`, whose hashes are not fields of `results.json`.
  Both require specification, gate and direct review bindings. The forward
  manifest must additionally equal `/provenance` through `equals_result_pointer`.
- Optional `structural_validator`: the explicitly allowed AH1 generated-span
  verifier, with schema/path/SHA256. Its helper must be directly bound by the
  final specification, skeptical review and gate.

Rational expression operands are `pointer`, `constant`, collection `length`,
`sum`, `product`, binary `difference`/`quotient`, `minimum`, `maximum`, unary
`absolute`, or `power` with an integer exponent in `[0,64]`. Boolean and float
operands are rejected. AI3's exact rational strings exceed Python's usual digit
limit; a finite 100000-digit ceiling accommodates its source-bound arithmetic.

Optional `supplemental_evidence` entries bind additive post-freeze interpretation
records to both gate and review and apply the same semantic checks. `scope_pointer`
explicitly identifies a record's scope or meaning field. For AG3 these preserve
the passive embedding comparison: the main active ceiling is weaker than
`81/256`; the narrow ceiling is smaller, with no established comparison against
the actual uncorrected lower-weight norm.

Flat and known nested forward bindings are supported. Freeze `files` maps use
producer-relative names; freeze `sha256` maps use repository-relative names.
Explicit freeze `bindings` maps likewise use repository-relative names.
Coverage follows freeze → output bindings → manifests → snapshots, so thin
freezes must still reach all active inputs. External installed-skill origins are
provenance only: release uses the committed instruction snapshots, never mutable
machine-specific installation files. Caches, links and escaping paths are rejected.

AJ1's typed forward source inventory requires identical complete source/copy
maps and exact contract coverage. Its eleven repository instruction entries
duplicate already verified copies; they are checked without counting twice.
Six typed installed resources retain their precise `skill://flora-skills/...`
locators as external provenance. Only this explicit format admits those locators;
legacy instruction formats retain the absolute-origin requirement. No external
locator is opened during admission or release. AJ1 reverse's original external
instruction reads are preserved in its administrative repair archive. The current
checker reads owned copies, with exact scientific-payload and geometry equality.

Gate/review wording may differ. After separate review, append the immutable
contract/admission digests and exact gate/review claim-projection digests to
`release/admitted.json`. The effective scope retains both limitation lists.
There is no automatic registration command: a newly present gate is not by itself
authorization to expand the trusted admission registry.

AG2's adapter uses actual rational output identities. The forward reference-gap
expression includes the original diagonal inside its `kappa`; the reverse output
records that original `4M` separately. Both conventions are checked explicitly.
Finite algebra diagnostics remain separate from full-space arguments.

AI3 preserves both distinct arithmetic conventions, all ten failed ratio cells
and the earlier successful scalar cell. Its proposal reconstructs each exact
center, complete physical budget, positive denominator, all-corner interval,
reverse shared-error interval and signed margin through pointers. It does not
copy long endpoint fractions into the admission specification. The post-review
record and additive Tesla clarification retain the distinction between smaller
width and endpoint containment; neither interval is silently treated as a sharp
physical joint-error set. Ordinary degree-eight arithmetic removes the material
finite-grid cubic floor; the proved all-order factor is a further retained
refinement, without ratio success on this grid. The retained failed pre-freeze
skeptic snapshot is historical evidence, never a passing active entrypoint.

AI4 checks the continuous parameter bounds and analytic recurrences supporting
every band separately from its ten fixed parameter fixtures. The admission
rules preserve each producer's distinct collar-count and state envelopes,
charge the growing quadratic averaging term, and distinguish inner-root
rounding from a final scalar-error floor. Fixture depths above six use proved
count envelopes; they do not claim newly enumerated collars. The additional
scalar allowances shrink with the candidate parameter. AI4 needs no increase
to the exponent grammar: its fixed large powers are products of bounded powers.

AH1's named structure verifier reconstructs all physical vertices, oriented
links, face words, Gauss incidence, pair masks, individually resolved basis
channels, Gram metric, Casimir energies and retained magnetic coefficients.
Exact sparse dictionary equality checks every nonzero and every structural
zero, including newly retained input columns. This verifies the admitted finite
construction; it does not replace the analytic cutoff, domain, full outside-map
or all-time heat proofs. The reverse producer's graph/basis/magnetic artifacts
are separately bound and replayed. The helper's independent skeptical mutation
audit is retained; its source bytes are immutable after that audit.

AI4's all-band admission checks follow its new coordinate induction, continuous
parameter estimates, spatial recurrence and growing-collar averaging bounds.
Finite geometry checks use the seven already admitted collars; no further
collar is enumerated. Exactly ten declared parameter fixtures check complete
physical sums, denominator reserves, candidate intervals and shrinking scalar
tolerances. Different face-count and state ceilings remain separately bound.
The shared `39/40` coefficient is checked against each exact proved coefficient
in additive reviewed evidence. Neither the all-band quantifier nor fixed-error
robustness is inferred from fixture success. Large fixed-fixture powers are
products of powers with exponents at most 64; the expression limit is unchanged.

The synthetic mutation fixture is not research evidence. It changes failed
controls, target claims, numerical budgets and required snapshots while rebinding
output, freeze, review and gate hashes. Rejection therefore tests more than stale
digests. The reviewed contract/specification/scope pins remain the trust boundary.

## Final exact-tree release

After all ten loops, commit the complete candidate and create a new detached
worktree at its full commit ID. From that disposable worktree run:

```sh
python3 -B research/round28/release_verify.py \
  --expected-commit FULL_COMMIT_ID \
  --expected-tree FULL_TREE_ID \
  --output /tmp/ym28-release-fresh
```

The verifier requires a clean start and finish, baseline
`a7f4b8dd42ce0f31f2442c068815f6d1f75ade1a`, unchanged historical scientific
research/evidence and unchanged existing papers. It runs the twenty current
producer entries normally and optimized (forty executions: eighteen original
scripts and two reviewed portable copies per mode), the independently pinned
portability audit in both modes, the declared current skeptic entrypoints in
both modes, and the admission mutations. Before rebuilding
the generated site, `artifact_manifest.py --check` verifies the final paper's
source manifest, PDF, all-page QA record and artifact bindings; it does not
rerender the PDF. The generated-site rebuild runs
`build_network.py --require-complete`, the isolated `tests/round28_build.py`
builder controls, then `build_site.py --require-complete` and the Pages build.
It compares whole committed subtrees byte for byte and runs
`tests/round28_site.mjs --release`, Round27 and workbench UI checks. Historical suites are
not replayed.

Skeptic entries specify script/output paths, input dependencies, `output_mode`
(`file`, `directory` or `fixed`) and an argument vector. Fresh interfaces use
exactly one `{output}` argument. Commands use argument arrays, never a shell.
Fixed-output checkers must leave their recorded output byte-identical.
Active checker scripts and outputs require direct skeptical review bindings.
A checker input may instead follow the directly reviewed, pinned contract's
source map; its exact hash must match the file and gate closure, and the
admission's producer manifests preserve the contract source snapshots. Arbitrary
gate-only or historical-JSON dependencies do not establish skeptical review.
An input may also be an exact owned copy in a same-loop skeptic input inventory.
That inventory must be directly reviewed and specification/gate-bound; the
original must already be reviewed directly or through the contract, and the
copy must match its hash and be specification/gate-bound. This one-copy rule
does not authorize recursive historical inventory traversal.

The external receipt records tested commit/tree, commands, statuses and log
digests. `receipt.sha256` binds its bytes. Do not commit it into its own tested
tree. If a GitHub API operation creates another commit with identical tree bytes,
fetch that commit and verify its own full commit/tree IDs in a fresh worktree.
Publish the verified identity; any later change needs a new receipt.

No successful validator, numerical fixture or model-agent review establishes
external peer review, a physical observation, or a continuum Yang–Mills proof.
