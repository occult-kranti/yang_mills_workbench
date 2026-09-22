# Hruday / HNM Round30 handoff

Exactly **three of three** adaptive investigations are complete. The current edition is `papers/draft-03/`; the preceding Draft02 and Round29 scientific records retain their original bytes. Human project author and direction: **Hruday N M (BUNZEEY)**. AI systems supplied separate model-agent derivations, skeptical checks, coding and editing. This is not external human peer review, formal proof-assistant verification or verified scientific priority.

## Admitted results

| Investigation | Reviewed result | Material limit |
|---|---|---|
| AT1: Hruday same-state Wilson energy certificate | In the actual chosen AQ numerical-cap state, the centered Wilson vector belongs to the physical Hamiltonian domain; its first energy moment is `alpha omega_num(1-W^2)` and its second moment is at most `alpha^2(36+98|tau|)<37alpha^2`. | Fixed lattice and physical scales, either sign of `|tau|<=10^-8`; no equality of second moments or automatic AO/AQ state identification. |
| AT2: Hruday spectral-window and inverse-energy certificate | Unnormalized spectral weight in `[alpha/16,8alpha]` is at least `307992/1984375`. For the reduced inverse form R, `3843876001/47000000000 <= alpha R <= 28462237549/7503125000`. | These bounds do not evaluate the actual response, identify a pole or establish susceptibility. Equal-moment atomic and atomless controls demonstrate incomplete spectral information. |
| AT3: Hruday finite Euclidean readout certificate | The frozen 4097-node design conditionally bounds `I=alpha R`, with exact-data interval width below `1/500`, deterministic per-sample error at most `10^-6`, and explicit quadrature, infinite-time-tail and arithmetic allowances. Abstract A/B output envelopes remain separated by more than `0.004293` under every allowed sample-error vector. | No actual AQ samples or response are computed. Forward arithmetic bins may be arbitrarily wide, with a reported width verdict; reverse bins are capped at `10^-12` for a uniform target guarantee. |

The gate JSON files in `advisor/` give the exact admitted wording and exclusions. Read each prospective contract, both frozen reports and the skeptical review with its executable evidence. AT3's additional omitted-tail diagnostic is a required countercontrol, not another research investigation.

## Adaptive decisions and historical lenses

AT1 was selected from Round29's bounded AT roadmap because its domain and energy identity were missing in the actual AQ state. Its review supplied the premises for AT2. AT2's broad inverse-form bounds and explicit spectral ambiguity motivated AT3's finite-data readout. Both derivation directions were frozen before comparison in every loop. The advisor stopped after the third review.

The selected reading covers Newton's chymical notes and Hermetic transcription, Tesla's patent mechanism and reported esoteric conversations, Jung's early observations and cueing concerns, Pauli archive provenance, Penrose/Feynman methodological sources, and current primary lattice/spectral literature. The ledgers distinguish primary text, scholarly transcription, patent proposals, forum discourse, and inaccessible government/archive leads. This was a bounded source survey, not a claim to have searched every field or read every work. None of the cultural or rumor records is a physical theorem premise.

Established quadrature, spectral calculus, moment bounds and inherited lattice methods retain their attribution. Hruday/HNM labels locate project contributions, statements, equations and quantities. They neither rename prior theorems nor turn every equation into a separate discovery. Existing project skills were sufficient; no prospective method change was needed to complete these three contracts.

## Calculators and data

- `calculators/spectral_certificate.py`: exact rational AT2 certificate with positive alpha and either sign of the admitted tau range.
- `forward/at3/evaluator.py`: conditional exact-rational sample evaluator, including a width verdict for arithmetic bins.
- `reverse/at3/check.py`: independently implemented evaluator and CSV reader with the stricter arithmetic-input contract.
- AT3 CSV outputs: explicitly synthetic 4097-node A/B benchmark enclosures. They are not measurement records or AQ simulations.
- `figures/`: scientific plots drawn from exact formulas or frozen rational endpoints; captions identify floating rendering and actual scope.
- `network.json`: additive current evidence graph, preserving inherited nodes and marking future goals as unexecuted.

The website includes the current manuscript, searchable HNM catalog, evidence network, source ledger, three-loop narrative and interactive AT2 calculator. Browser numbers are labelled floating displays; exact admitted values remain available in the research files.

## Next work is planning only

`advisor/roadmap.json` retains AR state/boundary identification and AS weak-coupling strategy as fundamental open obligations. The next bounded response question, AT4, is to produce one certified actual AQ Euclidean sample or isolate the missing error estimate. It requires state provenance, centering, complete factors, fixed clock, finite-volume/boundary error, representation-cutoff error, solver error and arithmetic error. A valid CSV shape cannot supply those scientific premises. AU's 561-state evaluator and AP's prior-fixed inference remain separate-model tasks.

No fourth investigation is executed. The four-dimensional continuum Yang–Mills existence and mass-gap problem, all-state uniqueness, AO/AQ identification and the AQ particle-pole question remain open. A new continuation should read this handoff, the roadmap and AT3 review, then freeze a new first contract before running it.

## Verification and release

`reproduce.py` checks all three source inventories, contract snapshots, required controls and exact reviewed semantics. `test_admission.py` first validates each unmodified temporary copy, then checks sixteen damaging evidence changes and their specific rejection reasons. Normal and optimized producer replays must reproduce all frozen output bytes. The final `verify_release.py` runs from the clean committed tree and writes its receipt outside the checkout; it also preserves earlier science, rebuilds current presentation assets and checks the bound PDF.

GitHub publication is a separate operation. Automatic approval review blocked a public release-image upload during recovery of the earlier Round29 release. No rejected payload is retried or routed around the review. The exact local release can be reviewed before the required explicit publication approval. Do not infer a successful push or Pages deployment from local build success, uploaded loose blobs or a prepared branch name.
