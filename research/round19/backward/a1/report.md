# Round19 backward A1: literal boundary restrictions

## Verdict

The independent reconstruction accepts A1 under the frozen `ym19-a1-contract-v1.1` contract. Literal finite restrictions of one fixed selected-face assignment produce only the six contiguous clipped component types `L`, `M`, `R`, `LM`, `MR` and `LMR`, and each has a full-link lower estimate at least `alpha/8` under the frozen coefficient bounds.

This is a finite local restriction result. It does not certify a thermodynamic limiting state, dense homogeneous stability, continuum Yang-Mills, or a Clay mass gap. A2 remains unstarted until the advisor freezes its contract.

## Independent reconstruction

The fixed infinite assignment is on open finite boxes cut from the nonnegative cubic lattice. Every present link carries the same electric coefficient `alpha`. On xy faces with even `y`, the global x residue determines the inherited selected coefficient:

| residue | role | bound |
|---:|---|---:|
| 0 mod 4 | `L` | `|lambda_left| <= alpha/2` |
| 1 mod 4 | `M`/bridge | `|mu| <= alpha/8` |
| 2 mod 4 | `R` | `|lambda_right| <= alpha/2` |
| 3 mod 4 | omitted in A1 | `0` |

A finite window can clip a strip at either side, depending on x-phase. Since residue `3 mod 4` separates selected runs, the only nonempty selected components are `L`, `M`, `R`, `LM`, `MR` and `LMR`. The verifier enumerates `n=2..12` and x-phases `0..3`, then records representative signed words once and exact counts/witness samples for the repeated finite cases.

For a proper clipped component, use the free full-link reference. Its first excitation is `3alpha/4`, and every selected Wilson multiplier has zero Haar-vacuum mean. The one-norm estimate gives

```text
Delta_S >= alpha * (3/4 - sum_{t in S} |c_t|/alpha).
```

The worst proper clipped cases are `LM` and `MR`, with norm budget `1/2 + 1/8 = 5/8`, so the lower estimate is exactly `alpha/8`. Single end faces give `alpha/4`; bridge-only gives `5alpha/8`.

For the complete `LMR` component, the bare norm budget can be `9alpha/8`, so the free reference is insufficient. The independent reconstruction reuses the Round18 A1 dressed-end mechanism: the two end blocks have reference gap at least `alpha(3/4-rho)`, the actual bridge has an untouched Haar link in the dressed reference, and `|mu| <= alpha/8`. With `rho <= 1/2`,

```text
Delta_LMR >= alpha(3/4-rho) - |mu| >= alpha/8.
```

Positive full-link bounds imply unique full ground states for the finite operators. Gauge invariance and the absence of nontrivial continuous one-dimensional characters of `SU(2)^V` put the unique full ground in the Gauss sector before restriction, so the same lower estimate applies to the physical subspace.

## Producer comparison

The final canonical producer comparison is accepted. `compare.py` reads producer source/evidence bytes and does not import producer code or treat producer-backward comparison files as authority. It separates provenance from mathematical comparison.

The accepted comparison checks:

- producer source hash syntax and source bytes;
- `source-manifest.json` against `check.py`, `report.md`, and every declared output file;
- exact positive symbolic `E_star` plus rational positive `alpha_over_E_star` and `alpha_min_over_E_star` fields;
- 54 signed local cases by independent `Fraction` arithmetic from signed coefficients, not producer pass booleans;
- exactly 44 unique phase fixtures for `n=2..12` and x-phases `0..3`;
- phase fixture component counts, component link counts, omitted-face witness counts and witness examples;
- stable literal coefficient for face `(xy,4,0,0)` versus the rejected complete-strip-only reclassification;
- altered-bound and missing-phase mutation controls.

The first comparison against the pre-contract/pre-canonical producer evidence is preserved as `history/first-producer-comparison-v1.1-incomplete.json`. It failed the frozen v1.1 requirements for `E_star` and all-phase coverage. That history is retained separately from the repaired final verdict.

## Falsifiers retained

The backward checker rejects `E_star=0`, Boolean or invalid phase inputs, and withdrawal of the common physical scale. It discriminates the Round18 complete-strip-only non-restriction: face `(xy,4,0,0)` has the same literal selected coefficient in boxes `n=6` and `n=8`, while the complete-strip-only rule changes it from absent/remainder to selected. It also treats missing clipped types and missing free-link zero-mean premises as blockers; without the zero-mean premise the two-face generic estimate is `3/4 - 2*(5/8) < 0`, so the sharper claim cannot pass.

## Executed artifacts

`check.py --output ABS_NEW_DIR` writes a compact `results.json`. Ordinary and optimized executions are byte-identical.

`compare.py --producer SOURCE --evidence OUTPUT --output NEW_DIR` writes `comparison.json`. The final canonical comparison status is `accepted`.

Baseline Round18 replay remains separate and is recorded in `../planning/baseline-reproduction.json`: normal and optimized Round18 reproducers reported `passed`, and the Round18 proof-route replay reported `passed` with 34 routes and 9 proved. Those counts are not added to the Round19 A1 science counts.
