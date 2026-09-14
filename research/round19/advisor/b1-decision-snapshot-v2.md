# Round19 B1 advisor decision snapshot v2

Decision: **accepted**.

This v2 snapshot is the advisor review record for the final `advisor/b1-gate.json`. It replaces no historical files: the pre-E-star gate snapshot is preserved separately, and the earlier comparator weaknesses remain documented in `advisor/b1-forward-review.md`.

## Evidence reviewed

The locked forward source is `forward/b1/check.py`, SHA-256 `e3410b3955be695c8ffbdf8062b5904fe9d5be3612c437678574670f5e148f4d`. Its report is SHA-256 `1b6537b7d7f41185fa774549fd143779083efe0b179cedf68b1888c6744e61e7`, and its accepted `results.json` is SHA-256 `792f2d43ab72de2779a4d4fb6505bb221323497da561e482b2033ac16c6bbde4`. The full cross-Gram coefficient ledger is `forward/b1/output/cross-gram-coefficients.json`, SHA-256 `387344ba4108afcf32e21a89a0aff023abc3f8134f1767008a9acd0b959bec33`.

The independent reverse source is `backward/b1/check.py`, SHA-256 `17289b33c06b29aebedd804a7ad81e589f4707ecb7d521457c379fd11ad3c8eb`; the final schema-aware comparator is `backward/b1/compare.py`, SHA-256 `07cba24804e8872c7bff167ad680ccdbaee925af68a96e6225e5e95132775758`. The reverse report is SHA-256 `7081316475fd532b0dd1584b60b921ec5f54165b9a30610b6e5cc4ca06b17955`, and the final manifest is SHA-256 `fd41febb0b71ce521aa8e775aed9749bf15aa202bb189c0a61115e94bf230203`.

The canonical comparison is `backward/b1/comparison/comparison.json`, SHA-256 `a3c6f685e705e9b05342d4fbed6161fb19a31359946eb69acb324383e90d6e09`, with status `accepted` and twenty-four passing checks. It checks positive `E_star`, `alpha/E_star=2`, `strict_cutoff/E_star=12`, ordered-entry transpose consistency, full cross-Gram polynomial equality, source manifest binding, and genuine mutation controls including zero `E_star`, kappa-as-reference and Fibonacci-as-reference substitutions with ratios unchanged.

Advisor replay reproduced the final comparator byte-for-byte and reproduced the reverse checker output byte-for-byte. The reverse manifest validates with zero file-map mismatches.

Root's independent matrix-mapping audit at `/workspace/scratch/544697acf6a6/b1-matrix-mapping-audit.json`, SHA-256 `4aeafb44dc23437df2962d888e51b6ceaee8622f0dd08a1197b20dd053eeaf2a`, reports 397 full ordered matrix entries, transpose equality and no extra face factor.

## Mathematical result accepted

B1 proves the finite two-cube strict-cutoff projector and exact cross Gram under `advisor/contract-b1.json`. The graph is the actual adjacent two-cube graph with 12 vertices, 20 links and 11 signed plaquette faces, including the shared internal face. The physical scale is recorded with a declared positive `E_star`; no static `kappa`, tolerance, volume or Fibonacci index is used as an energy.

The accepted strict-cutoff physical projector is 48-dimensional:

```text
vacuum: 1
four-edge fundamental cycles: 11
six-edge fundamental cycles: 36
six-edge nonplanar cycles: 32
six-edge planar cycles: 4
```

The proof is not merely simple-cycle enumeration. Forward and reverse enumerate all no-leaf supports through seven links, enumerate energetic labels `n=1,2,3`, apply exact SU(2) fusion/intertwiner tests at active vertices, and exclude `n>=4` because one such link costs `6 alpha` alone. The 28 seven-edge no-leaf supports are excluded by the label/intertwiner audit.

The strict threshold witness is explicit. At `E_el = 6 alpha`, there are 99 support/label assignments and 107 physical threshold channels after intertwiner multiplicities, with multiplicity distribution `{1: 91, 2: 8}`. Those channels are excluded from `P` by strict inequality.

Because the retained channels are complete `H0` eigenspaces below the cutoff, `P` reduces `H0`, and

```text
Q H0 Q >= 6 alpha Q.
```

For `V=-sum_f lambda_f x_f`, B1 computes the exact full cross Gram

```text
W^*W = P V^2 P - (P V P)^2
```

on the 48-channel basis. The final comparison checks ordered matrix entries and transpose consistency before upper-triangle comparison. Accepted counts are 48 basis masks, 222 upper-triangle nonzero cross matrix pairs, 397 full ordered nonzero matrix entries in root's mapping audit, and 867 ordered quadratic coefficients. This is an exact coefficient-ledger result, not a conservative norm bound.

## What remains open

B1 is finite graph work. It does not prove a continuous interacting coefficient box, B2's gap estimate, homogeneous dense stability, limiting spectral passage, continuum Yang-Mills or a physical mass gap. Static C-branch integral checkpoints must still mark physical scale matching open unless a real physical energy match is supplied.
