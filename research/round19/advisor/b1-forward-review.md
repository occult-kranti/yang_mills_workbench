
# Round19 B1 corrected forward advisor review

Status: **corrected forward and reverse evidence reviewed; B1 gate pending proper final forward-vs-reverse comparison**.

This review supersedes the earlier B1 forward-review text in place because no B1 gate has been issued. It does not accept B1, does not freeze B2, and does not modify `advisor/contract-b1.json`.

## Corrected locked forward evidence inspected

- `forward/b1/check.py` SHA-256 `e3410b3955be695c8ffbdf8062b5904fe9d5be3612c437678574670f5e148f4d`.
- `forward/b1/report.md` SHA-256 `1b6537b7d7f41185fa774549fd143779083efe0b179cedf68b1888c6744e61e7`.
- `forward/b1/output/results.json` SHA-256 `792f2d43ab72de2779a4d4fb6505bb221323497da561e482b2033ac16c6bbde4`.
- `forward/b1/output/channels.json` SHA-256 `29382213b2b3090efe0f8357de9683539cd536ae52f93add0db847da686ffa6c`.
- `forward/b1/output/cross-gram-coefficients.json` SHA-256 `387344ba4108afcf32e21a89a0aff023abc3f8134f1767008a9acd0b959bec33`.
- `forward/b1/output/source-manifest.json` SHA-256 `029e921f28a8f6ba3eb65282d0ad0ccf859bc2c0a02102db9a6b6aa237480439`.
- `forward/b1/optimized-comparison.json` SHA-256 `0ca3a456a9104a675c72843f57ddf9c83d18f0f1cc7e9fd3cc173d4afeea8ace`.

An advisor replay of `python3 -B research/round19/forward/b1/check.py --output NEW_DIR` reproduced the corrected saved forward files byte-for-byte: `results.json`, `graph.json`, `channels.json`, `basis.csv`, `cross-gram-coefficients.json`, `fixture-matrices.json`, `controls.json` and `source-manifest.json`.

## Corrected forward result under review

The forward result uses the actual adjacent two-cube graph with 12 vertices, 20 links and 11 signed faces. It freezes

```text
P = 1_{E_el < 6 alpha}(H0)
```

in the physical SU(2) gauge-invariant spin-network sector, with `E_star`, `alpha/E_star` and `lambda_f/alpha` kept separate from `kappa`, tolerances, volume and Fibonacci labels.

The corrected channel ledger reports:

```text
basis dimension below strict cutoff: 48
vacuum channels: 1
four-edge fundamental cycles: 11
six-edge fundamental cycles: 36
six-edge nonplanar cycles: 32
six-edge planar cycles: 4
seven-edge no-leaf supports rejected by intertwiners: 28
threshold label assignments at E_el = 6 alpha: 99
threshold physical dimension with intertwiner multiplicity: 107
threshold multiplicity distribution: {1: 91, 2: 8}
```

The correction resolves the earlier threshold-count ambiguity. The retained 48-dimensional projector and the Gram computation are unchanged.

The forward proof route remains the appropriate one for the B1 contract: enumerate all no-leaf supports through seven edges, enumerate exact labels `n=1,2,3`, use SU(2) fusion at each active vertex, and exclude `n>=4` because one such link costs `6 alpha` by itself. This addresses the branching/mixed-spin risk that simple-cycle enumeration alone would miss.

The threshold witness is an eight-edge labelled spin-network at exactly `E_el = 6 alpha`, excluded by the strict inequality. The explicit threshold ledger includes eight multiplicity-two degree-four cases; it should be preserved because it demonstrates that threshold counting is not the same as support/assignment counting.

For the cross operator, forward records the exact target

```text
W^*W = P V^2 P - (P V P)^2,
V = - sum_f lambda_f chi_f/2.
```

The sparse coefficient tensor is stored in `cross-gram-coefficients.json` with 867 ordered quadratic coefficients and 230 nonzero `PVP` linear entries. Representative fixture matrices are stored separately. This remains an exact-entry claim, not a row-sum or norm-only substitute.

## Current reverse state inspected

The reverse source/report/output have been revised from their initial limited status. Current observed reverse hashes:

- `backward/b1/check.py` SHA-256 `17289b33c06b29aebedd804a7ad81e589f4707ecb7d521457c379fd11ad3c8eb`.
- `backward/b1/report.md` SHA-256 `4cc74a765584fb6ba218ffc9bd587bfe82c5b7ec59ce4185d226d0a9b2385c02`.
- `backward/b1/output/results.json` SHA-256 `3be3908c17add132c593457de8af65f0009428e6d09df10e853cbd7906bf84a5`.
- `backward/b1/output/cross-gram-status.json` SHA-256 `0f0ee60cb89847ca01a8e6a9f2360c6fd2f395ed0fb8500f8fb6f9f32c016781`.
- `backward/b1/manifest.json` SHA-256 `4e7312ff997b429e86060989745ab5eddb6343d1b6dcff4ef7213660544e9ee4`.

The current reverse report now says the exact epsilon/Haar contraction supersedes the initial limited note. Its output reports retained dimension 48, the same threshold assignment/dimension distinction, exact cross Gram status, 222 nonzero upper-triangle matrix entries and 867 ordered quadratic coefficients. This removes the earlier prose/output conflict, subject to final comparison.

## Remaining gate blocker

There is still no accepted `backward/b1/comparison/comparison.json` final producer-vs-reverse comparison on disk. A temporary advisor run of the current comparator against `forward/b1/output` failed with

```text
KeyError: 'mask'
```

because the comparator still expected channel rows to have `mask`, while the forward channel ledger stores support arrays. This is a comparator/schema issue, not a mathematical rejection of the corrected forward result. The final comparison must normalize forward support arrays to masks and map the forward schema fields correctly:

- graph data from `graph` or `graph.json`, not only `graph_summary`;
- channel data from `channel_classification` and `channels.json`, not only `channel_summary`;
- scale data from `scale_register`, not only `physical_scale`;
- exact Gram entries from `cross-gram-coefficients.json`, not only embedded result fields.

## Regression caution

Do not require equality to the Round18 final 12-channel `W^*W` face block. Enlarging `P` to include six-edge cycles changes `(PVP)^2`, so the face principal block of the final cross Gram can change. The correct regression is that the old `PV^2P` principal face block is unchanged, while the enlarged `PVP` subtraction removes transitions now internal to the 48-dimensional `P`. The difference should be accounted for as a positive Gram contribution of newly retained transitions.

## Controls required before gate

The final independent comparison should run substantive mutation controls, not just name-presence checks. It should alter or withhold graph/channel/Gram data and reject:

- a dropped six-edge or nonplanar below-cutoff channel;
- outer-boundary graph substitution;
- inclusion of an `E_el = 6 alpha` threshold channel in `P`;
- missing `(PVP)^2` subtraction;
- a conservative bound labeled as exact Gram;
- invalid physical scale, including `E_star=0` or `kappa` as energy;
- Ritz/sample gap promotion to a full complement threshold.

## B2 planning constraint if B1 is later accepted

B2 remains unfrozen. If B1 is accepted, the next contract should use the actual full-Gram result to derive a supported continuous coefficient box with an `E1` lower bound and a separate `E0` upper bound. It should keep the prior Round18 `r=3/8` box and old `R*(3/8)=0.11876245` value only as a benchmark until feasibility is checked.

The old Round18 B2 reduction cannot be reused unchanged. The old `P\ominus Omega` block was exactly `3 alpha` because `P` had only the eleven face characters and `PVP` had zero face-face block. The enlarged Round19 projector has faces and six-cycles, with `H0` values `3 alpha` and `9 alpha/2`, and nonzero face-six and six-six compressed magnetic terms. Any coarse two-block B2 comparison must explicitly bound the new compressed magnetic form on `faces ⊕ six-cycles`; it must not promote a Ritz/sample matrix gap.


## Addendum: comparator ordered-entry bug blocks gate

Root found a substantive weakness in the first accepted B1 comparator: `expected_cross_entries` doubled already-commutative `f != g` coefficients while `producer_cross_entries` merged matrix `ij/ji` triangles. Those factors cancel for the symmetric data, but the comparison is then only a symmetrized-form check; an antisymmetric corruption of ordered entries could pass.

B1 must not be gated from that comparison. The reverse comparison needs to remove the expected-side extra factor, aggregate per ordered matrix entry, verify transpose symmetry before any upper-triangle comparison, add an antisymmetric mutation control, and fail closed on missing manifest/file entries. The underlying forward and reverse mathematical entries may remain unchanged, but the gate waits for the corrected canonical comparison.
