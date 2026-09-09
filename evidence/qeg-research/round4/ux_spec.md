# Research home and experimental workspace: UX specification

Prepared 9 September 2026. Scope: the existing Physics Observatory, its round-three report, final production output and recorded validation gates. This is an implementation specification; browser interaction tests remain the builder’s responsibility.

## 1. Product purpose and research honesty

The home page should answer three questions immediately: what question are we investigating, what was actually calculated, and what must happen next? Use the title **“How quantum matter changes fields—and how gravity enters.”** Lead with: “Explore a tested model in which an electric field creates a quantum current, and that current changes the field. Follow the evidence toward a future calculation in evolving spacetime.” Below it, display **“Restricted model tested · full Einstein–QED problem open.”** Avoid an overall percentage solved: mathematical progress has no defensible denominator.

Retain the Observatory’s cream paper, navy header, blue actions and serif headings. Add Research as the first primary navigation item and default route, preserving all existing Study, subject, history and patent pages. Inside Research, use a compact secondary navigation: Overview, Results, Demonstrations, Evidence, Experiments, Advisor. Keep sources and downloads available in the home guide and evidence section. At narrow widths, wrap this navigation; do not force a horizontal swipe to discover a feature.

## 2. Home placement and explanation layers

Place a two-column introduction above the fold: the question and two actions on the left, a small saved electric-field history on the right. Actions are **“Inspect the computed result”** and **“Start with the physical picture.”** The figure caption states the model, dataset and source-off time. Its default trace comes from `round3/results/production_baseline.csv`, never the historically named `production_baseline_converged` intermediate file.

Below the introduction, provide a numbered three-step guide: understand the feedback, inspect a result and its tests, choose a falsifiable next experiment. Follow it with one card for every implemented feature. Every card contains what it does, how to use it, what its output means, and an explicit link. A short “Plain language” paragraph remains visible; “Technical details” expands locally to reveal equations, units, assumptions and source references. This preserves context better than moving every explanation into a popup.

Use a persistent status vocabulary: **Recorded computation**, **Analytic demonstration**, **Proposed experiment**, **Unresolved**, **Superseded result**. Explain these once in the guide and repeat the appropriate badge beside each output. Saved numerical results are read-only; changing an educational slider must not alter their label or provenance.

## 3. Results, plots and useful combinations

The result explorer loads the final 4096-node, levels 0–8, canonical-window ±40 run. Plot electric field against dimensionless time, with a zero line and a source-off marker at s=4. Provide toggles for the source, energy-work residual and regulator comparison in separate panels, avoiding unrelated quantities on a shared axis. The field ends near −0.03757 at s=50; this is a finite-model output, not a measurement or a continuum certificate.

A caption should explain that the source first drives the field, then the evolving quantum current changes it after the source has stopped. The technical disclosure names x=eE/m², s=mt, the finite regulator, common subtraction and magnetic matching. Do not label `J0+Sx2` as the full physical current: the recorded README distinguishes the effective numerator from the reconstructed current.

A second plot compares fixed-window 2048 and 4096 histories or their pointwise difference. Show the measured maximum sampled field difference, 3.26×10⁻⁹, alongside the distinct Landau-level endpoint change, 5.06×10⁻⁸. These numbers do not combine automatically into a confidence interval. The strict 10⁻¹⁸ benchmark target remains visibly failed. Each plot has a text description, units, named line styles, accessible data table, and CSV download. The current SVG renderer already offers tables; improve it rather than replacing the application wholesale.

Browser demonstrations should be fast, bounded analytic calculations: coherent two-mode conversion, electromagnetic support scales, or a prescribed-field benchmark approved by the physics reviewer. Place prediction prompts above controls: “What happens when phase mismatch increases?” Then permit immediate comparison with resonance. Explain that the lossless constant-matrix conversion formula is not a magnetar calculation. Link each demonstration to a corresponding evidence card and proposed experiment; this connects learning to the research programme without suggesting equivalent model scope.

## 4. Evidence, sources, experiments and advisor

The four-front map has one card per original problem: charged de Sitter discharge, curved-space pair creation, Cauchy-horizon evolution, and photon–graviton conversion. Each links assumptions → equation → existing evidence → next discriminating test. Show shared dependencies such as a common current/stress subtraction, while recording incompatible geometries. A homogeneous flat model cannot provide a charged-horizon endpoint.

The source browser supports text, research-front and reading-depth filters. A record includes source version/date, direct primary link, inspected sections, associated claims and access limits. “Abstract inspected” and “derivation reproduced” are separate fields. A government programme or patent stays a source category, not an evidence rating. On zero matches, display an explicit empty state with Reset filters. Cached source records retain their date; no automatic “latest research” claim.

Experiment cards contain hypothesis, null/comparator, parameter range, observables, rejection gate, dependencies and current status. Prioritize directional stress closure and quantum-response validity, then curved integration. Permit local notes and export where implemented. A checkbox records the user’s review; it cannot change “proposed” to “validated.”

The advisor view explains the operating pipeline and supplies the downloadable protocol. Render actual roles, bounded tasks, evidence handoffs and acceptance rules. Describe it as a documented research workflow unless a live execution service genuinely exists. A role card is not a running agent, and a static page must not display invented live statuses. Display the date and provenance of the last review.

## 5. Popups, accessibility and failure behavior

Use one requested evidence dialog for long source/derivation detail. Its trigger sits beside the relevant claim and reads “Inspect evidence,” not a vague information icon. Open only on click or keyboard activation; never on first visit, timer or hover. Use native `dialog.showModal()`, a visible Close button, an associated title and a focusable heading for long content. Escape closes it; Tab stays inside. On close restore focus to the invoker, or a logical section heading if that element has disappeared. Avoid nested dialogs and close a dialog before navigating to another route. These behaviors follow the [W3C dialog pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/).

Numeric fields require finite values, explicit units and per-model domains. Empty strings are not zero. Reject overflow, NaN, forbidden negative lengths and unsupported model ranges beside the relevant field. Handle resonance and zero coupling analytically; do not divide by zero. Keep invalid input visible for correction. Do not silently clip occupation values or failed diagnostics. Missing/invalid saved data produces “Result data unavailable” with a download/retry path, never an invented curve. Downloads must reference the selected data, not a stale prior view.

Test 320-pixel layout, 200% zoom, keyboard navigation, reduced motion, route refresh, Back/Forward, dialog focus restoration, storage failure, corrupt imports, empty filters, malformed arrays, nonmonotonic times, missing units and repeated parameter changes. Keep focus indicators and status text; color alone cannot encode scientific status. Announce completed calculations politely, rather than every slider movement.

## 6. Verified inspiration and implementation boundary

Three primary inspirations inform the design. [PhET’s research programme](https://phet.colorado.edu/en/research) supports iterative, inquiry-oriented simulation design; borrow focused controls and prediction/feedback loops, not a claim that our interface has undergone equivalent learner studies. [Observable Plot’s accessibility documentation](https://observablehq.com/plot/features/accessibility) distinguishes plot and mark descriptions; apply those semantics to the existing SVG renderer with a table alternative. [Jupyter Book’s execution documentation](https://jupyterbook.org/stable/execution/) distinguishes executed, cached and interactive outputs; adopt that provenance clarity without installing a remote kernel. These are design adaptations, not claims of accessibility certification or adoption of those products.
