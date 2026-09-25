# BA2 contract review (skeptic, pre-comparison)

**Standing.** I wrote this from the frozen `contracts/ba2.json` (sha256 `275ba3b0…fcff`, frozen 2026-09-24T21:56:46Z), before reading either BA2 producer. I am a model-agent skeptic with correlated ancestry, not human review. Human author: Hruday N M (BUNZEEY).

My own record seeded this loop:
- my triage (b) proposed the Duhamel route and the loop-1 previews;
- my loop-2 review wrote most of the frozen text, including the corrected reverse route, the padding edit and the brackets.

This review therefore checks the contract against the premises. It is not an independent assessment of the contract's design.

**What I did and did not open.**
- I did not open, list or read `research/round33/{forward,reverse}/{ba1,ba2}/`.
- I ran `find` on the two BA2 `inputs/` folders (file names only) and compared each snapshot with the repository file by sha256. Both producers hold the same 29 files: `AGENTS.md`, the contract and the 27 shared premises. Every snapshot is byte-identical to the repository. The reverse inventory contains no triage, recommendation, prospective-controls, loop-2 review, deliberation, plan, lens file or forward file.

**Verdict: executable as written, with the readings below.** Nothing blocks production.

`ba2_check.py` confirms the frozen facts:

| Item | Value |
|---|---|
| Checks | 95 |
| Controls | 38: the 35 contract ids plus 3 extras, 101 damaging mutations |
| Control mirror | `controls` = `preregistration.controls_required.ids`, 35 = 35 |
| Premises | all 27 shared premises exist |
| Hashes | the NS excerpt sha256 `6a28f4cd…c921` is pinned; the PDF hash it records equals the Round29 binding `501af040…2fba` |
| Gate bindings | the AQ1, AY1 and AY2 reports that the checker parses are bound by their gates |

## Target well-posedness and margins

Every target is a proved-constant-at-most-target comparison. Each has a coefficient that is independent of N, at |θ| ≤ 8 (U = 1), with |τ| = 10⁻⁸ at both signs.

| Target | Route | Derived constant | Margin |
|---|---|---|---|
| comparison 6×10⁻¹¹ (5N+1)N⁻³ | forward, inner F1, Φ with 2268\|τ\| | 2.548785e-11 (closed 3969/155720800000000) | 2.354 |
| | reverse, inner F2, Φ′ with 1323\|τ\| | 1.484692e-11 (closed 9261/623765200000000) | 4.041 |
| Cauchy 2.5×10⁻¹⁰/(N−1), sup over M > N | F1, Φ, star-charged | 1.019514e-10 | 2.452 |
| | F1, Φ, face-charged | 5.947165e-11 | 4.204 |
| | F2, Φ′, face-charged | 3.464281e-11 | 7.217 |
| | F2, Φ′, group-charged | 5.938767e-11 | 4.210 |
| | F2 through F1 (triangle, labelled) | 1.720430e-10 | 1.453 |

- The target form (5N+1)N⁻³ is exactly the crude all-size form: 28N(5N+1) faces × |R| = 2 × at most 3 owners × F(N−1) = N⁻⁴. The margin is therefore the same for every N ≥ 2.
- The exact enumerated distance sums on Λ₂ to Λ₅ are 3.2–4.9% of the crude sum. This is a labelled refinement only.
- The loop-1 previews (2.549e-11 and 2.566e-11) are reproduced. So are the reverse preview (1.485e-11) and the Cauchy preview (1.0195e-10).
- The triangle route through the two limits does not reach the comparison target. That is the loop-2 correction, and it is kept as a labelled weaker bound.

## Numbered readings

1. **Clock.**
   - The time t in Nachtergaele–Sims is the normalized u = θ/8 = δt/ħ with δ = α/8, and NS τ_t^Λ is the evolution T^{F,N}, not the coupling.
   - |θ| ≤ 8 means U = 1.
   - The Round29 source dictionary, a shared premise, writes this normalized time as "s=delta*t/hbar". In Round33, s is the Euclidean clock α t_E/ħ. A packet that labels u as s fails `wrong_delta_alpha_hbar_clock`.
2. **Placement.**
   - H_x = h_x = 8Σ_e C_e goes into NS (44). With the zero-selected triple there is no selected potential.
   - Φ(X) is bounded.
   - F1 on Λ_N is the native restriction of the whole-star Φ.
   - F2 on Λ_N, without padding, is the native restriction of the owner-set Φ′.
   - The padded F2 operator H^(2)_N ⊗ 1 + 1 ⊗ Σ_pad h_x acts on A_{Λ_N} as T^{F2,N} ⊗ 1 exactly.
   - `H^(2)_N` in `parameters.boundary_source` is the AY1 forward (HNM-AY1-F02) operator, which is a premise.
3. **Constants are upper bounds inside a monotone function.**
   - C appears in the denominator of (51). Substituting C ≤ 224 and ‖Φ‖_F ≤ 2268|τ| is valid only because (e^{2‖Φ‖C|t|} − 1)/C and its time integral 2‖Φ‖U²·E(x)/x² (with E(x) = e^x − 1 − x and x = 2‖Φ‖CU) are nondecreasing in C and in ‖Φ‖. A packet should state this.
   - At leading order the coefficient 254016τ²U² does not depend on C. C enters only through the correction of relative size vU/3 ≈ 0.34%.
4. **Brackets.** `preregistration.scaling_brackets_per_constant` ([9500,10500]) governs; see defect D1.
5. **Cauchy quantifier.** The Cauchy estimate is sup over M > N. The N+1 in `observable.id` is only a special case (D3).
6. **Tier and route.**
   - Every constant carries tier `polynomial_lieb_robinson` and a route `duhamel_inner_f1` (Φ, 2268|τ|) or `duhamel_inner_f2` (Φ′, 1323|τ|), from plan.json's `tier_label_rule` (D7).
   - The inner F2 evolution can also be bounded with the padded anchor-grouped interaction Ψ_N(b+S) = φ_b^(Λ_N) on B_+, which gives 2268|τ|. That is valid, but only if it is stated. It reproduces the forward number and removes the reverse's constant difference.
7. **Identification on every local A.**
   - The whole-sequence scope in the gate fields names B(H_R) with the rate.
   - The AQ1 §4 rerun (stationarity on the quasi-local algebra) needs T^{F2,N}_θ(A) → T_θ(A) for every local A, not only for A in B(H_R). The same Duhamel sum with R replaced by a finite Y supplies this.
   - A packet that identifies the F2 limit only on B(H_R) has not closed O6.
8. **Fine-unit conversion.** "Converted to fine units" (required item 2) is a display only. The nearest owner (0,0,N) lies N−1 coarse z-steps from e_z, and a coarse z-step is one fine step a. No constant uses fine units, and no fm reading is allowed (D4).
9. **Theorem 4.1.** Quote the statement with (77) verbatim and cite it as "Section 4". The section title contains the contract-forbidden phrasing "the thermodynamic limit", which trips the negation-aware scan when quoted affirmatively (D8).
10. **Common limit.** `common_limit_claimed:false` concerns states (BB2). `dynamics_limit_identified_claimed:true` concerns the automorphism group.
11. **Both signs.** Every bound depends on |τ| only. The −τ value replays the same formula; it is not a second confirmation.
12. **Exponential instance.** It is optional and labelled, and it carries no admission weight. Its constants are C_{F_μ} ≤ 224 and ‖Φ‖_{F_μ} ≤ e^{2μ}·2268|τ|. Citing (53) with the polynomial F is rejected.
13. **Window.** The bound is nondecreasing in U, so the value at U = 1 covers every |θ| ≤ 8.

## Defects (none blocks production)

- **D1. Bracket inconsistency.**
  - `new_control_semantics.duhamel_tau_order_quadratic` still reads [9900,10100].
  - The preregistered bracket is [9500,10500], and its own note says that [9900,10100] "would reject a valid bound".
  - The valid form (x²/2)e^x has ratio 10101.10 with the exact exponential, and 976463275/96664 ≈ 10101.62 with e^x ≤ 1/(1−x). A forward producer using that form fails the stale bracket.
  - Reading 4 applies. The checker accepts that ratio as a positive fixture.
- **D2. Semantics coverage is 31 of 35.**
  - `cross_coupling_comparison_rejected` and `gate_fields_topic_specific` are new in Round33, and no frozen contract defines them. This breaks the plan rule "new_control_semantics for each control id not defined in an earlier frozen contract".
  - `full_original_wilson_cover` and `topology_named` are Round32 ids that no contract ever defined.
  - My loop-2 item BA2-N2 gave all four texts, but they were not applied, and producers do not receive loop2-review.json.
  - At post-comparison I will accept any reading consistent with those names and BA2-N2.
- **D3. `observable.id` names the N to N+1 difference.** The target and item 4 say sup over M > N, and the contract itself says that an N to N+1 bound is not a Cauchy estimate.
- **D4. Required item 2 against the metric.** It asks for the distance "converted to fine units", while `parameters.metric` says "no coarse-to-fine conversion enters any constant" and `decay_rate_in_N_not_a` rejects length-scale readings. Reading 8 applies.
- **D5. `parameters` has no N_0 field and no clock field.**
  - N ≥ 2 appears in the model and target prose. The clock appears in `window` and `preregistration.clock`.
  - The semantics of `parameters_declare_metric_weights_window` ("w=e^mu, e^beta … absence blocks the freeze") are copied from BA1. Read literally, they would have blocked this freeze.
- **D6. Notation.**
  - Required item 4 still writes the evolution as `tau^{F,M}_theta`; BA2-N1 was applied only partly.
  - Item 3 writes both b(N) and B(N).
- **D7. The route vocabulary is only in plan.json.** `duhamel_inner_f1` and `duhamel_inner_f2` live there, and no producer receives plan.json. The contract's `tier_mixing_rejected` names the interaction (Φ or Φ′) instead of a route. Reading 6 maps one to the other.
- **D8. Verbatim quotation against the forbidden phrasing.** The excerpt's Theorem 4.1 heading contains "the thermodynamic limit". Reading 9 applies.

## Control mirror

All 35 contract ids are executed as damaging mutations in `ba2_check.py`, each with the reason string it must be rejected for. Positives are accepted, including a `limited` packet that names its dominating term and the modern-form ratio 10101.6.

Three extra controls:
- `lr_constant_substitution_monotone`;
- `mandatory_sentence_once`;
- `error_terms_itemized`.

`reverse_premise_isolation` runs on the contract-derived inventory. The actual inventories were recorded by name and hash, as described above. Report contents are checked only at post-comparison.
