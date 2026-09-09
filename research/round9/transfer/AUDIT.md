# Transfer-code scope and correction record

Production source and numerical driver were reviewed from inputs through formulas, fallbacks, result fields, test predicates, CSV exports and plot binding. This states review scope, not branch-coverage percentage or certification by a human expert.

| File/function scope | Concrete risks checked | Outcome |
|---|---|---|
| `su2_transfer.py::_validate` | nonreal/nonfinite values; boolean accepted as number; incorrect spin indexing | explicit domain errors; n is dimension 2j+1 |
| `_decimal_series`, `decimal_reference` | positive-tail stopping; denominator cancellation; precision versus interval bounds | adaptive working precision; requested/actual digits recorded; not interval certified |
| `eigenvalue_record` | wrong Bessel order; missing representation factor; subnormal inputs; underflow mistaken for zero | scaled Bessel plus Decimal fallback; null float plus retained log; exact β=0 isolated |
| `log_normalization`, `gap_record` | overflow; near-unit cancellation; unrepresentable positive normalization; physical time units | logarithmic evaluation; tiny values explicitly rejected by float-only interface; positive time required |
| `haar_character_quadrature` | wrong Haar measure; endpoint division; overflow; unresolved oscillatory cancellation | direct sinθ sin(nθ) integral with shifted exponent; finite domain and separate refinement |
| `negative_beta_control` | incorrectly inferring operator positivity from positive kernel | direct negative eigenvalue matched by independent Haar integral |
| `run_checks` | missing gate fields; optimized-away assertions; vacuous collections | normalization error included; explicit exceptions; nonempty evaluated checks |
| CSV/PNG generation | wrong spectral/time variable; plotting artificial fitted mass; stale source | named scales and actual rows; before/after SHA256 binding; PNG visual inspection |

The initial code passed 89 gates but self-review identified two latent/edge defects. See `retained_failures.py` and `output/retained_failures.json` for executable retained evidence and initial hashes. The first was demonstrable cancellation in log Z at β=10⁻¹⁰⁰. The second omitted a recorded normalization error from the acceptance condition; a constructed diagnostic perturbation demonstrates why the omission mattered. Both are corrected. Independent reviewer feedback additionally required explicit rejection/Decimal retention when log Z is itself below floating range.

The final driver passes 92 gates under optimized Python, so acceptance does not disappear with assertions. Its maximum relative discrepancy against direct Haar quadrature is approximately 3.17×10⁻¹³ on the tested cases. This is a finite test result, not a uniform numerical error certificate. The independent skeptic uses a separately written high-precision Haar/Chebyshev calculation and records that review outside this package.

The proof excludes the following invalid transfers: single rotor → full lattice gauge theory; conjugation invariance → independent endpoint gauge invariance; fixed-parameter positivity → uniform continuum gap; pointwise kernel positivity → operator positivity; high-precision reference → formal interval proof. The original mathematical formula and plotted ordinary-parameter spectra were unchanged by the corrections.
