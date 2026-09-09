# What this research cycle achieved

Prepared 9 September 2026. This guide documents the advisor workflow, the new causal-response calculation, its failures and repairs, and the next experiments needed at the electromagnetic–quantum–gravity interface. It is an auditable research record with equations and executable specifications. It does not claim a complete solution of the four original open problems.

## Start with the physical meaning

An external source prepares an electric field. Quantum charged matter responds to that field. Its electric current then changes the field, including after the external source stops. The magnetic field in the computed model is held fixed. The geometry is flat; the calculation has not yet supplied the quantum pressures needed to change the geometry consistently.

The new experiment asks a sharper question: if the source amplitude changes slightly, how much does the entire electric-field history change? Instead of subtracting two almost identical runs, one solver evolves the derivative of the field and quantum modes directly. A separate implementation uses complex spinors and small positive/negative source changes to challenge that derivative. Agreement between these implementations is evidence about the specified numerical model.

The field sensitivity is an absolute derivative with respect to source amplitude. It is not divided by the instantaneous field. An ordinary field crossing through zero would otherwise create an artificial infinite ratio. It is also not a measured quantum variance: the connected current fluctuations require a separate correlation calculation.

## The concrete result and its uncertainty

| Test | Observed outcome | Scope |
|---|---|---|
| Independent response controls | 13 of 13 pass | Finite differences, gauge transformation, work, causal support and deliberate defects |
| Production versus independent spinors | 19 of 19 checks pass | Two small configurations, including source-hash and preparation comparisons |
| Maximum field-tangent discrepancy | 1.07e-11 and 3.76e-11 | Full sampled history in the two independent configurations |
| Maximum direct-current discrepancy | 4.00e-11 and 9.28e-11 | Current evaluated with the derivative counterterms |
| Momentum nodes 128 to 256 | Field sensitivity changes by 0.0504 | Underresolved momentum integral |
| Momentum nodes 256 to 512 | Field sensitivity changes by 0.0130 | Still insufficient evidence for acceptance |
| Momentum nodes 512 to 1024 | Field sensitivity changes by 2.16e-10 | Passes the fixed 1e-6 whole-history gate at the specified window |
| Same final refinement, current sensitivity | Change 8.43e-8 | Separate observable; not assigned the field's error |
| Response window and Landau-cutoff removal | Not completed | Remains a finite-regulator result |
| Full quantum noise and metric feedback | Not computed | Necessary future physical dependencies |

The selected larger response calculation has magnetic strength b = 10, levels 0 through 4, canonical momentum window from −20 to 20, source duration 4 and final dimensionless time 20. It is a different experiment from the historical long-time field plot, whose final time is 50. The same graph must not silently combine their settings or error estimates.

These numerical differences are comparisons under selected refinements, not rigorous universal error bounds or statistical confidence intervals. Agreement of two implementations that share the same physical approximation does not validate that approximation against the full quantum theory.

## What the new advisor process actually caught

The source audit found that the previous report described a per-mode cancellation fix which was absent from the delivered solver. The archived source and saved-run hash agree, so the discrepancy belongs to the report. The new code performs the subtraction inside each weighted mode sum and measures its effect against the unchanged historical code. This correction alone does not invalidate the old field reversal.

The new calculation also initially contained two diagnostic defects: a time derivative was replaced by the undifferentiated tangent in the direct current, and several diagnostic arrays were initialized but never populated. Both could permit reassuring output without the intended check. The independent current comparison exposed a large disagreement even when the field derivative agreed closely. The repaired frozen source now passes the independent comparison.

A fourth lesson is numerical: excellent energy conservation did not expose the coarse momentum quadrature. The response required its own refinement sequence. The initially failed finite-difference tests were retained and resolved by decreasing the perturbation size through a second-order convergence regime, without relaxing the acceptance threshold.

The original pre-fix response output was overwritten before an immutable archive was captured. The errata explicitly record this evidence gap. A corrected output is not presented as a preserved original failure. Future cycles should capture failed candidates before any replacement.

## How to use the Observatory

| Page or feature | Start here | What you can learn or do |
|---|---|---|
| Research home | Read the feedback explanation and switch Plain language / Technical | Understand the model, its evidence and open dependencies |
| Computed fields | Select an observable; expand the data table | Inspect the historical field, current, potential and work; export exact plotted CSV |
| Response test | Choose a saved case and response observable | Compare sensitivity, direct current and differentiated work; inspect independent tests and refinement |
| Calculators | Change inputs and predict the direction before calculating | Explore constant two-mode conversion, electromagnetic curvature-source budget and coherent detector noise |
| Four frontiers | Open each question's assumptions and sources | Separate WGC/FL, pair creation, inner horizons and conversion into their required physical contracts |
| Experiment plan | Read the rejection gate and dependencies | Form a falsifiable hypothesis; save a browser-local note and export it |
| Advisor protocol | Read the role and acceptance guide | Reuse the project prompts and learn why a failed gate changes the plan |
| Sources | Search author, topic or document; filter collections | Inspect 109 source records, reading depth, exact links and stated limits |
| Existing learning rooms | Use Study, Explore, Laboratory and Patent research | Continue the mathematical/physics curriculum and historical claim investigations |

The analytic calculators are small idealized models. They do not rerun the Maxwell–Dirac simulation or compute an astrophysical observation. The conversion calculator assumes constant lossless two-mode coefficients. Its phase mismatch is an input, not a newly calculated strong-field QED refractive index. The gravitational calculator reports an electromagnetic source scale; Maxwell stress is traceless, so that number is not the scalar curvature R. The detector calculator assumes coherent fields and ideal balanced detection.

Help dialogs open when requested. Research notes are stored in the current browser, separately from the older study-notebook backup; use the research plan export to preserve them. Plot exports contain saved values, not interpolated scientific predictions. The source ledger distinguishes inspected sections from a claim that an entire paper or repository was reproduced.

## Advisor team, skills and release checks

A fresh methodology agent reviewed original research and official OpenAI/Anthropic sources, handed off the advisor protocol and then finished its assignment. A physics advisor selected and reviewed the response contract. A lower-cost coding agent implemented it, and an independent verifier used a different state representation and deliberate defects. The interface adviser supplied the feature plan and prepared this guide. The integrator owns the actual website changes and release.

Two project skills now describe research-advisor decisions and numerical validation. Both passed structure validation. A bounded, nonblinded forward exercise accepted the finite-response claim and rejected a false inference of gauge breaking from shifting the potential while leaving the regulator window fixed. Six mechanical evidence checks passed. These are reusable project instructions; they do not modify a model's hidden internal prompt or establish general advisor reliability.

The website has automated checks for all eight research views, saved-data mapping, calculator limits and invalid inputs, source filtering, missing data, note escaping, dialog behavior in a simulated DOM, and legacy learning/patent features. The browser preview service was unavailable. Visual layout, real keyboard/focus behavior and responsive rendering therefore remain a release limitation; simulated DOM checks are not described as a completed browser audit. The PDF has its own rendered-page review.

## The next scientific decision

The immediate next physical dependency is a common covariant definition of current, energy and both directional pressures, with the same state and finite counterterms. Its force Ward identity and flat-space limit must be checked before using it in an Einstein evolution. In parallel, response spectra and smeared connected current fluctuations can test whether the mean-field approximation is controlled.

The four larger branches retain their own geometry, initial quantum state, observable and rejection conditions. A homogeneous current cannot be pasted into a charged black-hole horizon or treated as the transverse photon response of a magnetar. The roadmap below specifies those interfaces and the point at which each branch must stop if its assumptions fail.
