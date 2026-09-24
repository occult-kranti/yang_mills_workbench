# Round33 shared tools

These scripts are infrastructure shared by every producer, skeptic and the advisor. They compute no scientific result.

- `freeze.py snapshot|freeze|verify <producer dir>`: snapshot declared contract premises into `inputs/`, replay `check.py` normally and with `-O` into fresh external directories, require byte-identical outputs, and write/verify `freeze.json`.
- `record_gate.py <loop> ...`: write the advisor gate from the skeptic's reviewed statement and limitations with complete evidence bindings. The gate can never widen the reviewed scope.
- `arb_crosscheck.py`: optional independent floating/ball-arithmetic cross-check of exported rational enclosures using python-flint (Arb) and mpmath interval arithmetic. It is an open-source comparison tool, never the admission arithmetic.

Producer protocol: `check.py --output <absolute fresh directory>` must write `results.json` with a non-empty `checks` list of `{id, passed:true, ...}` entries and top-level boolean claim flags (at least `continuum_claim:false`, `uniform_wilson_claim` and `resolved_interaction_shift` where relevant). All admission arithmetic uses exact `fractions.Fraction`; floating numbers are previews only.
- `phrase_scan.py <contract> <files>`: Round32 closing-panel rule R6. Removes the contract's mandatory sentence template as one literal, then scans every clause whole-word for the round's and the contract's forbidden phrasings; a hit is affirmative only when its clause has no explicit negation frame. `record_gate.py` runs it on the supported statement, the decision and the limitations, and also enforces rule R7 (the template must appear as one unbroken span in the supported statement or the decision).
- `freeze_contract.py`: enforces rules R1-R5 and R8 at freeze time (placeholder spans, template field, term-by-term finite-model couplings, no copied provenance/clock/error-term blocks across model families, statement-loop target notes, selected_after notes) and the control mirror.
