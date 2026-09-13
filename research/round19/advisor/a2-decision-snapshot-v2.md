# Round19 A2 advisor decision snapshot v2

Decision: **accepted**.

This v2 snapshot refreshes only the source-bound inventory after the reverse final-message hash correction. It preserves the prior gate snapshot at `advisor/a2-gate-history-before-manifest-v5-refresh-c15c6e6c0593.json` and does not change the accepted A2 mathematical scope.

## Refresh reason

A through-A2 replay detected stale bindings in the previous advisor gate for two files only: `backward/a2/report.md` and `backward/a2/manifest.json`. The reverse agent then wrote `ym19-backward-a2-manifest-v5`, status `accepted-backward-a2-current-disk-hash-corrected`, recording that the final comparison binds the actual forward source hash `e6d8617a...` and that earlier stale comparison/report hashes remain history.

Current corrected reverse hashes:

```text
backward/a2/report.md    32b6b6343a01ca5621aa4937314af41b5d894778965c3bed68b6ac6fe114c63c
backward/a2/manifest.json 0d5e10a8ea1f87ac8315e41db45cfd5d58eae942198d2c1d76a107628b84f901
```

The independent comparison remains `f657d610651118b23ef3ed2ea0ad387b936f7979ba77e0950d1779d3c1fe9f71` with status `accepted` and fourteen passing checks. Forward source/output bytes remain bound to the corrected domain-equality theorem text.

## Mathematical result retained

A2 remains accepted only as the direct product-representation summable exception: `H_ref` has product-sector gap `delta=alpha/8`; the bounded self-adjoint omitted-face perturbation satisfies `||V|| <= beta <= alpha|tau|`; the exact omitted weight is `107/135`; and with `tau=1/64` the accepted gap is at least `7alpha/64` by the crude bound and `973alpha/8640` by the exact ledger.

The corrected domain statement remains part of the gate: since `V` is bounded self-adjoint, `H=H_ref+V` is self-adjoint on exactly `D(H_ref)`, with the closed form domain unchanged.

## Evidence classification retained

The domain/core/spectral-projection/gauge discussion is a reviewed written mathematical argument, not a machine-formal proof. Python exactly verifies arithmetic, source/output provenance and admission/mutation controls. The operator-theorem JSON records premises and theorem text; it is not a proof object.

## Open claims retained

A2 still does not prove finite clipped-restriction convergence, homogeneous dense nondecaying stability, dense limiting spectral passage, continuum Yang-Mills, or a physical role for double-Fibonacci geometry.
