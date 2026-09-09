# Round-six skeptical code audit

Selected 1,438 lines across six original computational files plus existing test/result artifacts; excludes dependencies, Site code, full repository, continuum physics and exhaustive dynamic/path coverage.

The audit found nine concrete implementation or metadata issues. None changes the accepted default finite-model equation contract. The corrected small default fixture reproduces every historical macro diagnostic bit-for-bit. Historical sources were frozen; all repairs live in `round6/code/`.

## What was reproduced and fixed

### C01 — Comparison family centered at the wrong probe amplitude

**Severity/scope:** high for nonzero delayed probe experiments. **Location:** `round4/code/response.py`; historical lines 298, 359.

With probe_amp=0.5, old finite differences were centered at zero; gauge and translated runs also dropped the probe. Old field comparison differed by 0.5002586.

**Impact:** False rejection of a valid tangent and comparison of physically different source histories. Default probe_amp=0 is unaffected.

**Correction:** Center plus/minus runs at probe_amp ± epsilon, retain probe in gauge/translated runs, and mark legacy comparison unavailable when its source cannot match.

**Executable evidence:** `audit_repro.py: nonzero_probe; test_nonzero_probe_preparation_and_centered_difference`. Status: fixed and reproduced.

### C02 — Unvalidated scenario controls yield NaNs or silently select a model

**Severity/scope:** medium. **Location:** `round4/code/response.py`; historical lines 150, 165, 298, 332, 363, 379.

Unknown mode misspelled is accepted; epsilon=0 emits NaN derivative arrays. Empty epsilons fail later at min(); duplicate epsilons collapse in CSV mapping.

**Impact:** Invalid diagnostic output or unintended comparison family; no evidence that accepted historical defaults contain this input defect.

**Correction:** Validate mode, nonfinite source controls, supported gauge flag, nonempty distinct positive finite epsilon values before integration. Also reject incomplete/nonfinite returned state arrays.

**Executable evidence:** `audit_repro.py: zero_epsilon and unknown_mode_accepted; bad-epsilon and mode regressions`. Status: fixed and reproduced.

### C03 — Python optimization can disable mathematical acceptance checks

**Severity/scope:** high for automated acceptance. **Location:** `round5/symbolic_checks.py; round5/coefficient_certificate.py; round5/run_checks.py`; historical lines 8, 9, 50, 51, 32, 37, 46, 23, 33.

A deliberately wrong Bloch identity (+1 defect), executed with python -O, returns exit code 0 and passed:false in historical symbolic code. The old aggregate runner checks only exit code.

**Impact:** A future optimized or inherited PYTHONOPTIMIZE run could be marked successful despite failed checks. The recorded nonoptimized historical run remains valid.

**Correction:** Replace assert acceptance with explicit exceptions; new aggregate runner requires fresh output, semantic success and unchanged source bytes.

**Executable evidence:** `test_historical_assert_mutant_false_success_reproduced and test_symbolic_gate_fails_even_optimized`. Status: fixed and reproduced.

### C04 — Explicit unsafe theorem labels bypass the narrow blacklist

**Severity/scope:** medium for proof metadata integrity. **Location:** `round5/proof_search.py`; historical lines 201, 204, 231, 238.

A declared theorem seed labeled proposed or unresolved is accepted and produces status proved.

**Impact:** Metadata inconsistency can be laundered into a trace. This does not show the accepted fixture has unsafe labels, nor can a text-label check establish theorem truth.

**Correction:** Reject the complete reserved unsafe label set after whitespace normalization. Mathematical rule certification remains an external review obligation.

**Executable evidence:** `audit_repro.py: verification_proposed/conjectural/unsafe/unresolved; test_unsafe_node_verification_rejected`. Status: fixed and reproduced.

### C05 — Referenced proof bytes are absent from the graph hash

**Severity/scope:** medium for reproducibility. **Location:** `round5/proof_search.py`; historical lines 252, 280.

The library hash binds proof_ref strings, not bytes of the referenced theorem and contract documents. A changed document preserves the old library hash.

**Impact:** Stale external derivations could be displayed alongside a valid planning trace. This was a documented planner boundary, now additionally guarded.

**Correction:** New immutable-version evidence manifest binds fixture, planner and local referenced proof files; verify before/after planning, including unchanged manifest digest.

**Executable evidence:** `test_external_proof_artifact_change_rejected; evidence_guard.py bound_plan`. Status: provenance guard implemented and mutation tested.

### C06 — Exact large integer costs overflow during unnecessary float conversion

**Severity/scope:** low. **Location:** `round5/proof_search.py`; historical lines 61, 67.

Positive integer cost 10**400 raises OverflowError rather than following the documented integer-cost contract.

**Impact:** Input handling defect only; no wrong optimum for accepted ordinary-cost fixtures.

**Correction:** Keep positive Python integer costs exact; remove float conversion.

**Executable evidence:** `audit_repro.py: huge_cost; test_exact_large_integer_cost`. Status: fixed and reproduced.

### C07 — Missing observation windows can be reported as a pass; work window ignores overlapping pump

**Severity/scope:** medium for temporal diagnostics. **Location:** `round4/code/response.py`; historical lines 333, 341.

No pre-probe samples are assigned pre_max=0 and pass; no late samples return infinity. Work constancy is tested after the probe even if the primary pump remains active.

**Impact:** Vacuous causality pass or a false work-identity failure for a permitted pulse arrangement.

**Correction:** Report sample counts and null for unobserved windows; do not pass missing coverage. Begin post-drive work check only after both sources end.

**Executable evidence:** `test_no_causal_samples_does_not_pass_vacuously and test_work_constancy_waits_until_both_sources_stop`. Status: fixed and reproduced.

### C08 — Legacy conditional flag can be mistaken for an unconditional theorem

**Severity/scope:** medium for scientific presentation. **Location:** `round5/proof_search.py`; historical lines 507, 517.

conditional:false means no explicitly retained conjecture, although finite-model hypotheses remain in assumptions.

**Impact:** A UI using only that flag could falsely label the result unconditional.

**Correction:** Emit declared_assumption_ids, conditional_on_declared_assumptions, conjectural_assumptions, conditional_flag_meaning and result_kind. Preserve old fields for compatibility.

**Executable evidence:** `test_declared_conditions_are_distinct_from_conjectures; independently raised by physics skeptic`. Status: clarified and regression tested.

### C09 — Scenario source hash was captured only after the computation

**Severity/scope:** medium for provenance. **Location:** `round4/code/response.py; round5/run_checks.py`; historical lines 342, 351, 23, 24.

Historical source_hash() is evaluated at report assembly, so mid-run changes cannot be distinguished from a run of the reported source.

**Impact:** A general reproducibility gap; all 13 audited historical source/result/contract hashes currently match.

**Correction:** Capture source and imported legacy hashes before scenario execution, compare again before return. Aggregate gate checks its command source before/after execution.

**Executable evidence:** `test_source_changed_during_run_rejected`. Status: guard implemented and mutation tested.

## Measured corrections

| Check | Historical behavior | Round-six behavior |
|---|---|---|
| Nonzero delayed probe: finest derivative discrepancy | 2.9654e-5, stalled | 4.7009e-10 after second-order interval |
| Translated-gauge field difference, same probe | 0.5002586 from mismatched source | 2.7756e-14 |
| Default matched small fixture, every macro array | Reference | Exactly zero maximum difference |
| Wrong symbolic identity under python -O | Exit 0, passed false | Explicit nonzero exit |
| Recorded historical content hashes | 13 references | 13/13 still match |

New targeted regression suite: **18/18 passed**. Unchanged historical proof-planner suite run against the new engine: **24/24 passed**. These are separate checks, not 42 independent proofs of physics.

The finite-difference errors are 4.5900e-8, 5.0235e-9 and 4.7009e-10 for epsilon 0.03, 0.01 and 0.003. The measured ratio is compatible with the intended centered second-order check before a numerical floor. The test uses b=1, n=0, K=3, 12 longitudinal nodes and 61 time samples; it is a preparation regression, not a production refinement.

## Function and line-span review matrix

Each row denotes direct static review of the complete listed function. Nested rows name the important closures separately. This is not a runtime coverage percentage and does not claim that every possible branch was exercised. Module-level declarations and all 1,438 original source lines were also inspected.

### `round4/code/response.py`

SHA-256: `0a197f5b46de8114d790c937059018d21df3f55a436c76067b91c09277035867`. 379 lines.

| Function | Historical lines | Review / evidence boundary |
|---|---:|---|
| `Grid.__init__` | 59–69 | Positive fixed quadrature, gauge node translation; new validation C02. |
| `_validate` | 72–91 | Finite numeric/integer/positive checks; unsupported unrenormalized mode correctly rejected. |
| `bump_integral` | 94–99 | Static source review; covered by owning function/fixture where exercised. |
| `_chi` | 102–104 | Matched b=10 expression reviewed; no global floating-point enclosure or small-b accuracy claim. |
| `_pulse` | 107–111 | Smooth compact pulse and endpoint support inspected. |
| `_initial_state` | 114–125 | Fixed magnetic vacuum and zero amplitude tangent; gauge tangent v=1, deltaK=1. Arbitrary state families are not implemented. |
| `_terms` | 128–137 | Per-mode subtraction and C,D definitions checked against contract and symbolic identities. |
| `_tangent_terms` | 140–147 | Unused helper restricted to source-amplitude deltaK=0; reviewed separately; not an independent solver. |
| `_closures` | 150–165 | Source construction C01/C02. |
| `_closures.drive` | 159–160 | Static source review; covered by owning function/fixture where exercised. |
| `_closures.delta_drive` | 162–163 | Static source review; covered by owning function/fixture where exercised. |
| `_solve` | 168–287 | Nested equations, work, raw diagnostics, NaN completeness checked; current uses u prime. Fixed small baseline equality; no intersample enclosure. |
| `_solve.rhs` | 177–212 | Full quotient derivative, Bloch tangent, q=deltaK-v and work derivative checked against symbolic algebra. |
| `source_hash` | 290–291 | Static source review; covered by owning function/fixture where exercised. |
| `legacy_hash` | 294–295 | Static source review; covered by owning function/fixture where exercised. |
| `run_scenario` | 298–360 | C01,C02,C07,C09; finite differences and gauge are preparation-specific. |
| `write_csv` | 363–379 | Reviewed serialization; duplicate epsilon map overwrite prevented at scenario validation. CSV export itself not rerun. |

### `round3/code/backreaction.py`

SHA-256: `32008bfc4fc3f731ac7ed968006fd58642820e0f421766a1ace022a2d7f08e88`. 305 lines.

| Function | Historical lines | Review / evidence boundary |
|---|---:|---|
| `bump_integral` | 55–61 | Static source review; covered by owning function/fixture where exercised. |
| `_validate` | 64–89 | Static source review; covered by owning function/fixture where exercised. |
| `Grid.__init__` | 93–104 | Static source review; covered by owning function/fixture where exercised. |
| `_chi` | 107–109 | Static source review; covered by owning function/fixture where exercised. |
| `_make_pump` | 112–122 | Static source review; covered by owning function/fixture where exercised. |
| `_make_pump.drive` | 116–120 | Static source review; covered by owning function/fixture where exercised. |
| `_initial_state` | 125–135 | Static source review; covered by owning function/fixture where exercised. |
| `_grid_terms` | 138–148 | Known legacy split-sum cancellation retained intentionally. No new fix retroactively claimed. |
| `run` | 151–290 | Legacy comparator only; all macro keys inspected. No NaN completeness guard in this historical source. No fresh full trajectory acceptance. |
| `run.rhs` | 166–184 | Matched branch compared; unrenormalized removes derivative subtraction consistently. Historical mode is not supported by new response tangent. |
| `write_csv` | 293–301 | Static review only; zip truncates uneven arrays if caller supplies malformed arbitrary result; production result shapes are fixed. |
| `source_hash` | 304–305 | Static source review; covered by owning function/fixture where exercised. |

### `round5/proof_search.py`

SHA-256: `297a9e79f4e2027b651f558ea8a175b6957c429a214225e72892d9633c5f1367`. 595 lines.

| Function | Historical lines | Review / evidence boundary |
|---|---:|---|
| `_require_string` | 42–45 | Static source review; covered by owning function/fixture where exercised. |
| `_string_list` | 48–58 | Static source review; covered by owning function/fixture where exercised. |
| `_positive_integer` | 61–67 | C06. |
| `Library.atoms` | 104–105 | Static source review; covered by owning function/fixture where exercised. |
| `ProofStep.as_dict` | 115–121 | Static source review; covered by owning function/fixture where exercised. |
| `CheckedProof.as_dict` | 132–139 | Static source review; covered by owning function/fixture where exercised. |
| `load_library` | 142–265 | AND premises, scopes, assumption retention, statuses, frozen records checked; C04. |
| `_library_hash` | 268–280 | Internal byte-canonical metadata hash correct; external-reference gap C05. |
| `check_proof` | 283–311 | Every required premise is replayed; mutated library hash rejected; no implication reversal. Metadata does not substitute for a proof kernel. |
| `_proof_from_ids` | 314–315 | Static source review; covered by owning function/fixture where exercised. |
| `_forward_uniform_cost` | 318–362 | Positive exact costs and goal-pop optimality reviewed. Scope is supplied finite rule library. Existing 24-test suite rerun on new engine. |
| `_forward_uniform_cost.result` | 330–333 | Static source review; covered by owning function/fixture where exercised. |
| `_bidirectional_candidate` | 365–452 | First meeting is only an incumbent; independent forward pass certifies cost. |
| `_bidirectional_candidate.candidate` | 381–385 | Static source review; covered by owning function/fixture where exercised. |
| `_backward_first_meeting` | 455–494 | Legacy unused helper; statically reviewed, not runtime exercised by current plan path. |
| `plan` | 497–555 | Budget, blocked goal, not-derivable and conditional labels checked; C08. |
| `load_json` | 558–563 | Static source review; covered by owning function/fixture where exercised. |
| `main` | 566–591 | CLI serializes all supplied scenario results. A zero exit means execution succeeded, not every target proved; new acceptance runner checks required statuses. |

### `round5/symbolic_checks.py`

SHA-256: `5855e6e9e1419ed864b4335645aeb5f0821ac88d02fe44326cfb2cd6d1a0d8b7`. 54 lines.

| Function | Historical lines | Review / evidence boundary |
|---|---:|---|
| `zero` | 8–9 | All 16 symbolic identities/mutants inspected and rerun in explicit-failure version; C03. This is not inequality, ODE existence or continuum proof. |

### `round5/coefficient_certificate.py`

SHA-256: `6ac554c1d3dc17cdc413a45bbe9ba510d43ab65c7d819791bfc591f6c08000ea`. 65 lines.

| Function | Historical lines | Review / evidence boundary |
|---|---:|---|
| `main` | 21–61 | Frozen round4/round3 hashes, positive rounded weights/masses, rational mass grouping and bound checked. C03. Certificate encloses rational coefficients, not a floating trajectory/digamma analytic value. |

### `round5/run_checks.py`

SHA-256: `ea450efed24edf33d8d002dc83518c17dd7c552bb044cd4f45f3dae72cf3707d`. 40 lines.

| Function | Historical lines | Review / evidence boundary |
|---|---:|---|
| `main` | 13–37 | C03,C09. Original process output and six source hashes checked; new runner requires fresh semantic result. |

## Claims that remain outside this audit

- The prior accepted trajectory uses 401 reported times at fixed K=20, n=0 through 4. Fixed-window quadrature refinement is distinct from either cutoff removal.
- The historical direct-current derivative discrepancy has its own reported values; the preselected field-tangent refinement threshold is not retroactively a current threshold.
- Pure-gauge validation translates potential and canonical nodes together. A potential shift at fixed nodes is a different finite regulator.
- The tangent solver supports source and gauge families prepared in the fixed vacuum. General initial-state and purity-changing families need a separate implementation contract.
- A constant or finite tangent is not a quantum noise or semiclassical-validity certificate.
- External proof-file hashes establish version integrity. They do not mechanically establish the mathematical correctness of the derivations.

## Reproduce

From the project directory:

```sh
python round6/code/run_checks.py
```

This executes 24 compatibility tests, the new regression suite, explicit-failure symbolic checks, the exact rounded-coefficient bound and the content-bound proof plan. It creates fresh result JSON and rejects failed semantic status even when a process exits zero. Dependencies are the existing NumPy/SciPy environment and SymPy 1.14 (the existing round5/deps directory is supported).

All 13 inspected historical acceptance/validation hashes match in `historical_integrity_results.json`. The new source digests and complete function matrix are in `code_audit.json`. No historical source or result file was rewritten.
