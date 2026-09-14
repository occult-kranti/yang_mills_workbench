# Round19 B1 advisor decision snapshot

Decision: **accepted**.

This snapshot is the immutable advisor review record for `advisor/b1-gate.json`. It accepts the corrected B1 canonical bytes, not the earlier schema-mismatch or symmetrized-comparator attempts. The previous comparator weakness is preserved in `advisor/b1-forward-review.md`; the final gate relies on `backward/b1/comparison/comparison.json` SHA-256 `675e94d958bbed18f74117daedc909a53bcc1de864f6829e8bd6526f7571a5d5`.

## Evidence reviewed

The locked forward source is `forward/b1/check.py`, SHA-256 `e3410b3955be695c8ffbdf8062b5904fe9d5be3612c437678574670f5e148f4d`. Its report is SHA-256 `1b6537b7d7f41185fa774549fd143779083efe0b179cedf68b1888c6744e61e7`, and its accepted `results.json` is SHA-256 `792f2d43ab72de2779a4d4fb6505bb221323497da561e482b2033ac16c6bbde4`. The full cross-Gram coefficient ledger is `forward/b1/output/cross-gram-coefficients.json`, SHA-256 `387344ba4108afcf32e21a89a0aff023abc3f8134f1767008a9acd0b959bec33`.

The independent reverse source is `backward/b1/check.py`, SHA-256 `17289b33c06b29aebedd804a7ad81e589f4707ecb7d521457c379fd11ad3c8eb`; the schema-aware comparator is `backward/b1/compare.py`, SHA-256 `358868ee334700f47fce0031c208d5dca1f61e14bf208452d1559b7562514ff5`. The reverse report is SHA-256 `420327858cdabcb55926c9e36f6c0f52dfa5b5d60709748f5b50315be3506e27`, and the manifest is SHA-256 `509792fb667965b116acd5fad4169078e0f2a04ca78a8bd2c6a91d12e202b2cf`.

An advisor replay reproduced the corrected forward output byte-for-byte. A separate advisor replay of the reverse checker reproduced the saved reverse output byte-for-byte. A fresh replay of the final comparator reproduced the canonical comparison byte-for-byte, with status `accepted` and twenty-one passing checks. The reverse manifest file map validates against current disk bytes.

Root's independent matrix-mapping audit at `/workspace/scratch/544697acf6a6/b1-matrix-mapping-audit.json`, SHA-256 `4aeafb44dc23437df2962d888e51b6ceaee8622f0dd08a1197b20dd053eeaf2a`, also reports that 397 full ordered matrix entries agree, transposes are equal, and no extra face-pair factor is present. This audit supports the final comparator repair but is not a Round19-relative gate file.

## Mathematical result accepted

B1 proves the finite two-cube strict-cutoff projector and exact cross Gram under `advisor/contract-b1.json`. The actual graph has 12 vertices, 20 links and 11 signed plaquette faces, including the shared internal face. The physical scale is recorded with `E_star > 0`, `alpha/E_star=2`, and strict cutoff `E_el < 6 alpha`; no static `kappa`, tolerance, volume or Fibonacci index is used as an energy.

The accepted strict-cutoff physical projector is 48-dimensional:

```text
vacuum: 1
four-edge fundamental cycles: 11
six-edge fundamental cycles: 36
six-edge nonplanar cycles: 32
six-edge planar cycles: 4
```

The proof is not only a simple-cycle list. Forward and reverse enumerate all no-leaf supports through seven links, enumerate energetic labels `n=1,2,3`, apply exact SU(2) fusion/intertwiner tests at active vertices, and exclude `n>=4` because one such link costs `6 alpha` alone. The 28 seven-edge no-leaf supports are excluded by the label/intertwiner audit.

The strict threshold witness is explicit. At `E_el = 6 alpha`, there are 99 support/label assignments and 107 physical threshold channels after intertwiner multiplicities, with multiplicity distribution `{1: 91, 2: 8}`. Those channels are excluded from `P` by strict inequality; the gate does not use the earlier ambiguous `threshold_channel_count=99` wording.

Because the retained channels are complete `H0` eigenspaces below the cutoff, `P` reduces `H0`, and the complement threshold is

```text
Q H0 Q >= 6 alpha Q.
```

For `V=-sum_f lambda_f x_f`, B1 computes the exact full cross Gram

```text
W^*W = P V^2 P - (P V P)^2
```

on the 48-channel basis. The final comparison checks the full ordered matrix and transpose consistency before upper-triangle comparison. The accepted normalized counts are 48 basis masks, 222 upper-triangle nonzero cross matrix pairs, 397 full ordered nonzero matrix entries in root's mapping audit, and 867 ordered quadratic coefficients. This is an exact coefficient-ledger result, not a conservative norm bound.

## Controls reviewed

The final comparison has twenty-one passing checks and thirteen substantive mutation controls. It rejects omitted below-cutoff channels, threshold inclusion, signed-incidence damage, altered Gram coefficients, antisymmetric matrix-triangle perturbation, missing `PVP` subtraction, zero scale, wrong cutoff scale, bound-as-exact Gram, threshold assignment/physical-count confusion, missing source-manifest check hash, missing required output entry and wrong required output hash.

## What remains open

B1 is a finite actual two-cube graph result. It does not prove a continuous interacting coefficient box, B2's gap estimate, homogeneous dense stability, finite-volume limiting spectral passage, continuum Yang-Mills or a physical mass gap. The full Gram now makes a B2 finite-graph coefficient-box proof possible, but B2 must be a separate loop with its own gate.
