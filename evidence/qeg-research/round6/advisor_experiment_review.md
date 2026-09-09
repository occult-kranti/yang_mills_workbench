# Independent advisor review of the coefficient implementation

Final review, 9 September 2026. **Accepted for the stated mathematical experiment and tested numerical domain.** All seven initially observed findings were repaired and reviewed. The final coefficient source has 351 lines and 26 top-level functions; the advisor read the complete file and compared its substantive formulas with independent derivations. This is not a claim that every representable floating-point input has an error enclosure.

Final source SHA-256:

`30396dbff23ade9aa7f5bf7e912571ff0e2e2a8029e5e663b65862915ddfc013`

The initial implementation reported all conventional gates green, but the independent review found the following problems. Its original source is retained under `advisor_review/experiments_initial_observed.py`, with hash `ba8fa923b28fc4fa9d0b75fe0e566417806a3a5a573d96c075fe8d407bbd8915`.

| ID | Observed defect | Final correction and independent evidence |
|---|---|---|
| ADV-E01 | The cofinal integral already included a factor 1/4, but its outer coefficient included another one | Correct `b/(4π²)` measure; six independent lower-bound comparisons pass |
| ADV-E02 | The graph's `log10(N+1)` coordinate used `ψ(N+2+z)` | Correct shifted argument; eight values agree with independent high-precision digamma references |
| ADV-E03 | Natural logarithm was stored under a base-10 label; remainder text omitted an argument shift | Correct base-10 scale and explicit disclosure of omitted shifted-argument terms; no interval-bound claim |
| ADV-E04 | Subtracting saturated primitives returned zero for positive representable coefficients | Adaptive precision; independent rescaled direct integrals confirm six held-out potentials, including `a=10^30` |
| ADV-E05 | The reference called mpmath at implicit default precision | Explicit working-precision context; advisor independently uses 90 working digits and normalizes very small integrands before quadrature |
| ADV-E06 | Boolean potentials were accepted; numeric strings failed later with TypeError | Explicit ValueError for booleans, strings, NaN and infinity |
| ADV-E07 | Symbolic check assumed positive y while advertising a real-y primitive | y declared real and M positive separately; regenerated symbolic identity passes |

The cancellation repair was tested twice. A first fixed-100-digit workaround resolved `a=10^3,...,10^7` but still returned zero at `a=10^30`, where the correct coefficient is about `2.5330295910584443×10^-150`. That intermediate failure remains in the JSON audit. The final adaptive-precision version resolves it. The advisor's tiny-integral reference is rescaled before integration, because an absolute quadrature stopping tolerance alone can give misleading relative accuracy for such small numbers.

The final independent runner passes **29/29 checks**. It tests actual values against separately constructed integrals and sums, validates the axis convention, checks rejection behavior and verifies that the published result hash matches the source reviewed. The implementation's conventional gates also pass. Its 135-point integration matrix, finite Gauss refinement, exact rational certificate and coarse-grid counterexamples remain separately visible in `experiment_results.json`.

This acceptance supports the new coefficient formulas, numerical illustrations and the corrected plot datasets. It does not test an ODE trajectory, prove continuum regulator removal, provide interval-certified floating results or identify a physical ultraviolet pole. The broad fixed-matching obstruction is established analytically; finite plotted examples only illustrate it.

The separate core-code repair graph was reviewed as a diagnostic comparison. On its identical nonzero delayed-probe fixture, the historical central-difference error stays near `2.97×10^-5`; the corrected curve decreases from `4.59×10^-8` to `4.70×10^-10`. That supports correction of the nonzero-probe center, while the archived default zero-center result retains its own historical scope.

Reproduce this independent review with:

```sh
python qeg-research/round6/advisor_independent_checks.py
```

`advisor_experiment_review.json` supplies the issue history, final dispositions and frozen output hashes; `advisor_independent_results.json` supplies every check and its actual evidence.
