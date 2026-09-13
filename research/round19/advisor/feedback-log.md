# Round19 advisor feedback log

## A1 first failed comparison preserved

At head `e62886d4cf724557c1884d11e5579bae94e28fcb`, the first independent A1 comparison delivered a real failed result: `research/round19/backward/a1/comparison/comparison.json` has status `producer-incomplete-under-frozen-v1.1`. The rejected producer evidence was the exploratory pre-contract output and omitted the explicit `E_star` register plus all four x phases required by `contract-a1.json` v1.1. This failure is retained as feedback history and is not an A1 acceptance.

## Current advisor blockers

- Canonical forward A1 evidence now includes the missing `E_star` scale register and 44 phase fixtures, but it still needs a revised independent comparison against its canonical schema.
- The first comparator is too shallow for positive admission: exact parsed scale, complete phase-domain checks, independent rational bound reconstruction and mutation controls are required.
- A forward rerun reproduced the scientific outputs but not `source-manifest.json`; the executable writes `report.md: null` while the saved manifest contains a report hash.
- A2 remains unfrozen. The constructive product-representation route should only be contracted after A1 acceptance and after deciding that its domain/essential-spectrum obligations are feasible.


## 2026-09-13 A2 closure, manifest refresh and B1 watch

A2 is accepted on the corrected final source/output/comparison bytes. A through-A2 replay found stale advisor bindings for `backward/a2/report.md` and `backward/a2/manifest.json`; the reverse manifest was corrected to `ym19-backward-a2-manifest-v5`, and the advisor preserved the prior gate at `advisor/a2-gate-history-before-manifest-v5-refresh-c15c6e6c0593.json` before refreshing `advisor/a2-gate.json`, `advisor/a2-source-bound-inventory.json` and the post-A dependency inventory. The accepted A2 mathematical result did not change.

Current A2 gate SHA-256: `80c1dc9add22e4d042155017202534fc8ff5e977a445e655d6ada1d90726efe9`.

B1 is now executing under `advisor/contract-b1.json` with no B2 contract frozen. The main advisor watch item is complete exclusion of all physical channels below the strict `E_el < 6 alpha` cutoff. Workers must enumerate four- and six-edge fundamental cycles, but also prove that branching/mixed-spin supports cannot slip below the cutoff. A selected simple-cycle list is not sufficient.


## 2026-09-13 B1 forward review pending comparison

Forward B1 locked source/output is runnable and byte-reproducible from `forward/b1/check.py` SHA `c6e90d66ae3d8bb412d7903b3aa66e028a8277eb7504fb82153f0bc532f7f9e1`. It claims the strict `E_el < 6 alpha` projector has dimension 48: vacuum, 11 four-edge fundamental cycles and 36 six-edge fundamental cycles, with 32 nonplanar six-cycles. It also claims the exact 48-channel cross Gram with 867 ordered quadratic coefficients.

Advisor review is recorded in `advisor/b1-forward-review.md`. B1 is not gated: reverse comparison must still bind stable final reverse bytes, map the forward output schema, independently check the exact Gram, run substantive mutation controls, and correct or rename `threshold_channel_count=99` if it is not a complete physical channel count with intertwiner multiplicities. B2 remains unfrozen.


### B1 threshold count addendum

Root confirmed that forward `threshold_channel_count=99` is a label-assignment count. The complete physical threshold dimension is 107 after intertwiner multiplicities, with multiplicities `{1:91, 2:8}`. This does not affect the strict 48-channel retained projector or Gram mathematics, but forward fields/report must be repaired or renamed before gate.


### B1 corrected forward review after threshold repair

Forward B1 threshold ledger was repaired and replayed byte-for-byte. Current forward source SHA `e3410b3955be695c8ffbdf8062b5904fe9d5be3612c437678574670f5e148f4d`, report SHA `1b6537b7d7f41185fa774549fd143779083efe0b179cedf68b1888c6744e61e7`, results SHA `792f2d43ab72de2779a4d4fb6505bb221323497da561e482b2033ac16c6bbde4`, Gram SHA `387344ba4108afcf32e21a89a0aff023abc3f8134f1767008a9acd0b959bec33`. The corrected ledger distinguishes 99 threshold label assignments from physical threshold dimension 107 with multiplicities `{1:91, 2:8}`. The strict 48-channel projector and 867-coefficient Gram are unchanged.

Reverse now records exact Gram reconstruction, but B1 remains ungated because no accepted final forward-vs-reverse comparison exists. A temporary comparator run still fails on the forward schema with `KeyError: 'mask'`. B2 remains unfrozen; if B1 is accepted, B2 should use the actual full Gram for a continuous box with separate `E1` lower and `E0` upper. The old Round18 `r=3/8` and `R*(3/8)=0.11876245` are benchmarks only; the enlarged face/six-cycle compressed magnetic form must be bounded explicitly.


### B1 comparator ordered-entry hold

B1 gate is held after root found a comparator normalization weakness: the first accepted comparison doubled already-commutative expected `f != g` coefficients and merged producer matrix triangles, checking only the symmetrized form. Reverse must compare ordered entries/transpose explicitly, add an antisymmetric mutation, and fail closed on missing manifest/file entries before the advisor can gate B1 or freeze B2.


## 2026-09-13 B1 accepted and B2 frozen

B1 is accepted in `advisor/b1-gate.json` after the ordered-entry comparator repair. Final comparison SHA `675e94d958bbed18f74117daedc909a53bcc1de864f6829e8bd6526f7571a5d5` has status accepted with 21 checks, ordered-transpose verification, antisymmetric mutation and fail-closed manifest-entry controls. Forward source/results/Gram are `e3410b3955be695c8ffbdf8062b5904fe9d5be3612c437678574670f5e148f4d`, `792f2d43ab72de2779a4d4fb6505bb221323497da561e482b2033ac16c6bbde4`, `387344ba4108afcf32e21a89a0aff023abc3f8134f1767008a9acd0b959bec33`. Reverse comparator/report/manifest are `358868ee334700f47fce0031c208d5dca1f61e14bf208452d1559b7562514ff5`, `420327858cdabcb55926c9e36f6c0f52dfa5b5d60709748f5b50315be3506e27`, `509792fb667965b116acd5fad4169078e0f2a04ca78a8bd2c6a91d12e202b2cf`.

Accepted B1 result: complete 48-dimensional strict `E_el < 6 alpha` physical projector on the actual two-cube graph and exact 48-channel `W^*W=PV^2P-(PVP)^2` cross Gram with 867 ordered quadratic coefficients. Threshold channels at `6 alpha` are excluded; the threshold ledger distinguishes 99 support/label assignments from 107 physical channels after intertwiners.

B2 is now frozen in `advisor/contract-b2.json`. It targets a continuous signed box `|lambda_f| <= alpha/8` using the accepted B1 full Gram, with a separate `E1` lower and `E0` upper. The old Round18 `r=3/8` and `R*(3/8)=0.11876245` remain benchmarks only until rederived with the enlarged 48-channel projector.


## 2026-09-13 B1 accepted after explicit E_star comparator fix

B1 is accepted in `advisor/b1-gate.json` after the final scale-reference comparator repair. Final comparison SHA `a3c6f685e705e9b05342d4fbed6161fb19a31359946eb69acb324383e90d6e09` has status accepted with 24 checks. It now checks the declared positive `E_star` reference directly and rejects zero `E_star`, kappa and Fibonacci substitutions while ratios remain unchanged.

Accepted B1 result: complete 48-dimensional strict `E_el < 6 alpha` physical projector on the actual two-cube graph and exact 48-channel `W^*W=PV^2P-(PVP)^2` cross Gram with 867 ordered quadratic coefficients. Threshold channels at `6 alpha` are excluded; 99 support/label assignments give 107 physical threshold channels after intertwiners.

B2 is frozen in `advisor/contract-b2.json`. It targets a continuous signed box `|lambda_f| <= alpha/8` using the accepted B1 ordered Gram, with separate `E1` lower and `E0` upper. The old Round18 `r=3/8` and `R*(3/8)=0.11876245` remain benchmarks only until rederived with the enlarged 48-channel projector.
## 2026-09-13 B2 gate and C1 contract

B2 accepted after final forward/reverse comparison: finite two-cube continuous coefficient-box certificate with primary r=1/8, rederived r=3/8 benchmark, 7/16 positive control and 1/2 insufficient control. Advisor gate: `advisor/b2-gate.json`. C1 frozen as a static U-V-W chain integral contract with physical scale matching explicitly open: `advisor/contract-c1.json`.
