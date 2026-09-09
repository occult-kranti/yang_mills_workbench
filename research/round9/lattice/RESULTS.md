# Bounded experiment result

The actual four-dimensional SU(2) Wilson sampler passed its deterministic matrix-oracle checks. Six fixed small-lattice chains were completed. Exact finite-measure identities agree with the measured diagnostics under the predeclared gates, while the beta=2.2 plaquette uncertainty remains **insufficient**. No Yang–Mills mass or continuum claim follows from this experiment.

## Measured ensemble

Every chain uses a periodic 2×2×2×2 lattice, 512 warmup sweeps, and 2,048 recorded sweeps. The primary standard error uses 32 batches of 64 consecutive measured sweeps. Values below use those estimates; insufficient entries are displayed to preserve the result, not accepted as precision claims.

| beta | start | mean plaquette | batch SE | tau_int (sweeps) | plaquette uncertainty |
|---:|---|---:|---:|---:|---|
| 0 | cold | 0.00117178 | 0.00186494 | 0.991 | usable |
| 0 | hot | 0.00431660 | 0.00148582 | 1.013 | usable |
| 0.5 | cold | 0.12625085 | 0.00209402 | 1.801 | usable |
| 0.5 | hot | 0.12361646 | 0.00233652 | 2.763 | usable |
| 2.2 | cold | 0.61665834 | 0.00571595 | 16.951 | insufficient |
| 2.2 | hot | 0.61478140 | 0.00515710 | 17.691 | insufficient |

The predeclared autocorrelation threshold is tau_int≤64/5=12.8 sweeps. Both beta=2.2 plaquette series exceed it. Their close hot/cold means therefore do **not** pass a hot/cold agreement gate. The fixed run was not extended or reseeded after seeing this failure.

## Exact identities checked

- At beta=0 the plaquette mean has exact expectation zero and its squared value has exact expectation 1/4. The four chain-specific diagnostics are consistent by the fixed five-SE criterion. The largest absolute score is 2.91 for the beta-zero hot mean. It is retained; no rerun replaced it.
- At beta=0.5 and 2.2, the four chain-specific integrated link identities are consistent. The beta=2.2 Ward observable has a shorter measured autocorrelation time than the plaquette, so it meets its own uncertainty gate. This illustrates that passing one observable's identity does not validate every other observable.
- At beta=0, the Ward residual is algebraically zero and is explicitly labeled trivial.
- Three separate one-matrix rejection samplers generated 20,000 IID values apiece at beta=0,0.5,2.2. Their six mean/second-moment diagnostics agree with the exact Haar/Bessel values under the fixed criterion. These Bessel means are not used as exact interacting-lattice predictions.

## Real defect corrected before sampling

The independent skeptic supplied finite input arrays whose mean/variance computations overflowed and produced NaN/Inf diagnostics. The initial implementation rejected nonfinite inputs but failed to reject all nonfinite *derived* values. The corrected source explicitly rejects nonfinite intermediate mean, variance, batch uncertainty, covariance, autocorrelation and comparison statistic. A deliberately malformed accepted-looking summary with a NaN mean now raises rather than producing a statistical label. The skeptic retained the original source and reproduction evidence separately.

The producer's 12 deterministic test groups cover matrix/quaternion products, the full Wilson action, cold action, 64 random single-link differences, odd/unequal dimensions, gauge invariance, center seams and winding-loop signs, inverse proposals, group norms, exact one-matrix integrals, generator derivatives, input/no-data checks and the overflow regressions. Group norms were never silently projected during evolution; final squared-norm defects were at most 2.23×10^−14.

## Post-run prerequisite gate correction

After the fixed experiment finished, the skeptic found a second defect: the old runner trusted a `successful` flag without requiring a nonempty, current set of tests. A synthetic empty-success record could advance to the sampler. This did not describe the actual run, which executed all 12 test groups, but it was an unsafe future acceptance path. The exact executed producer files are preserved in `results/executed_sources/`, matching the run manifest's original before/after hashes.

The current runner requires all 12 named test groups, zero failures/errors/skips, and hashes binding the deterministic evidence to the current producer code and preregistered contract. `check_evidence_gate.py` rejects seven empty, stale, missing, skipped or failed record mutations and accepts the current valid record. The current deterministic record is saved separately as `deterministic_checks_current.json`; the original record and all stochastic samples remain unchanged. No stochastic rerun was used to tune a result.

## Evidence and limits

`results/experiment_manifest.json` records the contract/source hashes before and after the run, seed list and runtime versions. Those hashes agree and match the preserved executed-source snapshot. The current runner/test files have different hashes because the post-run evidence gate was repaired. CSVs preserve all measurements and sampled warmup traces; final configurations allow independent full-action and gauge checks. `all_diagnostics.json` retains batching sizes 16,32,64 and all statuses. Figures are generated only from those saved data.

This result supports a finite-lattice implementation and highlights an error-budget limitation. It supplies no long-distance correlator, mass-gap estimator, continuum construction or uniform bound. The next preregistered study should improve sampling and measure volume/time-extent dependence before attempting a spectral observable.
