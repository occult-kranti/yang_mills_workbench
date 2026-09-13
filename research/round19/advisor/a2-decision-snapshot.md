# Round19 A2 advisor decision snapshot

Decision: **accepted**.

This snapshot is the immutable advisor review record paired with `advisor/a2-gate.json`. It uses the corrected final A2 bytes, not the earlier accepted comparison that was superseded by the bounded-perturbation domain correction. The stale accepted and stale rejected records remain preserved under `backward/a2/history/`.

## Evidence reviewed

The accepted A2 contract is `advisor/contract-a2.json`, SHA-256 `ddc4cb6ae18458ae21b0b18afdec346386f5dfcf0e1c1a1b6974a5a072244a8b`, dependent on the accepted A1 gate. The current forward source is `forward/a2/check.py`, SHA-256 `e6d8617a0593d13a711cb63447e1d2d3e32a3c9337efdbc95fe1a2ffac22323e`, with `forward/a2/report.md`, SHA-256 `6fc6b0c4ee95d11e5e1ab8f9b6249ace7b9792728ee93bd919510ce440bc51fb`. Its current saved `results.json` SHA-256 is `43f45abfdc365e1c1f423bfa64b93a4ff3f8386acaed49c139a05521a2e269b9`.

The independent reverse comparison is `backward/a2/comparison/comparison.json`, SHA-256 `f657d610651118b23ef3ed2ea0ad387b936f7979ba77e0950d1779d3c1fe9f71`, with status `accepted` and fourteen passing checks. The final reverse manifest is `ym19-backward-a2-manifest-v4`, status `accepted-backward-a2-after-corrected-domain-source-review`; it records that the earlier `a71ee760...` accepted comparison was superseded and that `a12e117...` rejected the stale domain wording.

An advisor replay from source reproduced the saved current forward output files, backward output and independent comparison byte-for-byte. Normal and optimized A2 outputs are deterministic repetitions of the same exact arithmetic and theorem-admission checks; they are counted once.

## Mathematical result accepted

A2 proves the narrow direct product-representation summable exception described in `contract-a2.json`. In the incomplete infinite tensor product stabilized by the A1 complete-strip/free reference vector `Omega_ref`, define

```text
H_ref = sum_C (H_C - E_C) + sum_free alpha C_e
```

as the closed nonnegative reference form/operator on the finite-excitation form core. The A1 complete-strip input gives the product-sector inequality

```text
q_ref[psi] >= (alpha/8) ||(1-|Omega_ref><Omega_ref|) psi||^2.
```

The omitted-face perturbation is summable:

```text
V = - sum_f nu_f x_f,
||V|| <= beta <= alpha |tau|.
```

The exact dyadic ledger gives selected weight `28/135`, omitted weight `107/135`, total weight `1`, and therefore the sharper default bound `beta/alpha = (1/64)(107/135)`. The final forward/reverse evidence independently reconstructs the nine truncation-tail rows and the closed-form coefficient sums.

The zero trial mean is proved termwise by exhaustive unused free-Haar-factor witness classes: non-xy remainder faces, odd-y xy faces and x-residue-3 separator xy faces. With the default `tau=1/64`, the crude accepted bound is

```text
gap >= alpha(1/8 - 1/64) = 7 alpha / 64.
```

The exact ledger gives the sharper recorded value

```text
gap >= alpha(1/8 - 107/(64*135)) = 973 alpha / 8640.
```

With the frozen example `alpha/E_star=2`, the corresponding exact gap is `973 E_star / 4320`; the crude gap is `7 E_star / 32`, and the common conservative display floor remains `7/64` in `E_star` units.

## Evidence classification

The closed-form product construction, form-domain/core argument, codimension-one spectral projection argument and gauge-invariance/non-vacuity argument are accepted as reviewed written mathematical arguments in the project record. They are not machine-formalized proofs.

The Python evidence exactly verifies the coefficient ledger, tail arithmetic, representative zero-mean witnesses, source/output provenance and admission/mutation controls. It does not, by itself, prove infinite-dimensional domain closure or spectral isolation.

The JSON operator-theorem object records the theorem premises and corrected domain statement. It is an auditable contract artifact, not a formal proof object.

## Corrected domain point

The final source/report now use the corrected bounded-perturbation statement: since `V` is bounded self-adjoint, `H=H_ref+V` is self-adjoint on exactly `D(H_ref)`, and the closed quadratic-form domain is unchanged. The gate does not rely on the earlier incorrect statement that bounded `V` could make `D(H)` differ from `D(H_ref)`.

## What remains open

A2 does not prove convergence of finite clipped restrictions to the product representation. It does not prove homogeneous dense nondecaying stability, dense finite-volume spectral passage, continuum Yang-Mills, or a Clay mass-gap theorem. The double-Fibonacci geometry remains an organizing hypothesis only; no physical role is admitted by A2.

## Advisor consequence

Goal A has produced two accepted narrow results: A1 gives boundary-consistent local clipped components, and A2 gives a direct summable product-representation exception. The original dense/homogeneous parent target remains open. The next goal should move to complete low-energy support and exact complement coupling on the actual two-cube graph, with the original cross-Gram obligation preserved.
