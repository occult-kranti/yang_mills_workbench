# Jung/Pauli lens, Round32 sub-round 2, assistant-2

Pre-registration audits and tests for the lens (`update-1.md` section 5, the three
tests requested after sub-round 1; the calling task). **These outputs count zero
research loops.** Nothing here is a producer, a contract, a gate or a skeptical
review; nothing computed here is read back into any contract, gate or skeptical
review. Human project author: Hruday N M (BUNZEEY); AI-assisted. Standard library
only (`fractions`, `json`, `re`, `pathlib`). Run every script with `python3 -B`.

Read before this work: `research/round32/experts/jung/update-1.md` section 5,
`research/round32/experts/jung/assistant-1/` (reused its `preregistration_audit.py`
structural-check logic, generalised from AV1/AV2 to any contract; re-implemented,
not imported), `research/round32/contracts/aw1.json` and `aw2.json`,
`research/round32/advisor/aw1-gate.json`, `research/round32/forward/aw1/check.py`
and `output/results.json`, `research/round32/reverse/aw1/check.py` and
`output/results.json`, `research/round32/forward/aw2/check.py` and
`output/results.json` (AW2 review pending; provisional), `research/round32/
skeptic/aw1.md` and `aw1.json`, and the draft contracts `research/round32/
contracts/ax1.json`, `ax2.json`, `ay1.json`, `ay2.json`, `az1.json`, `az2.json`.

## Files

- `common2.py` -- shared helpers: `AuditError`/`require`/`expect_rejected`,
  `load_json`/`rat`/`s`/`merge_results` (re-implemented from assistant-1's
  `common.py`, not imported), generic contract loaders for any round-32 contract
  at either `draft` or `frozen_before_production` status, and the closed
  pre-registration vocabularies (`ALLOWED_DIRECTION`, `ALLOWED_REFERENCE_ROUTE`,
  `SUB_LABELS_ALLOWED`, etc.) re-declared from assistant-1's sub-round-1 script.
  Does **not** import `forward/*/check.py`, `reverse/*/check.py`, assistant-1's
  scripts, or any other producer/skeptic module.
- `coupling_rule_chain.py` -- script 1/3.
- `sign_convention_fixture.py` -- script 2/3.
- `preregistration_audit_2.py` -- script 3/3.
- `results.json` -- merged output of all three scripts. Produced by
  `rm -f results.json && python3 -B coupling_rule_chain.py &&
  python3 -B sign_convention_fixture.py && python3 -B preregistration_audit_2.py`.
  Byte-identical under normal and `-O` Python (checked).

## Results

### 1. `coupling_rule_chain.py` -- PASS

Independently replays AW1-gate -> AW2-contract -> AW2-`check.py`'s `tau_AW2`
derivation, without importing any producer/skeptic module:

1. Parses `K_2^+ = 81108864767825329926713064490531229475390625/
   24176936535511801466930759024724079017984` (~3354.80323) from
   `advisor/aw1-gate.json`'s `decision` text, cross-checked against its `accepted`
   text (they agree), and the AW1 cap `10^-8` from the same text.
2. Parses the frozen decade-grid rule from `contracts/aw1.json.parameters.
   aw2_coupling_rule` ("... frozen here, never chosen after K_2 is seen"): grid
   start `10^-8`, bound `1/288`.
3. Applies the rule with its own decade search (not `forward/aw2/check.py`'s
   `aw2_rule`): `K_2^+ * 10^-8 = 33548032294.6.../10^15` (~3.3548e-5) `<= 1/288`
   (~3.472e-3) already at the first grid point, so `tau_AW2 = 10^-8` (the cap).
4. Confirms this equals `contracts/aw2.json.parameters.tau_AW2`'s stated value
   (with the accompanying text correctly describing a rule reference, not a bare
   number: "... evaluated inside check.py from the AW1 gate snapshot") and
   `forward/aw2/output/results.json`'s recorded `headline.tau_AW2` and
   `tau_values`.
5. **Grep for the literal `1/100000000`, explained.** A digit-bounded search
   (`(?<!\d)1/100000000(?!\d)`) finds **zero** standalone occurrences in
   `forward/aw2/check.py`. An unbounded substring search does find one raw hit,
   but it lies entirely inside the unrelated literal `1/1000000000` (=10^-9, used
   in an unrelated mutation-fixture tuple at line 1244) as a coincidental
   digit-run collision -- `100000000` (8 zeros) is trivially a substring of
   `1000000000` (9 zeros) -- and the digit-bounded regex correctly excludes it.
   Two occurrences of `Q(1, 10 ** 8)` exist: one is a decimal-string tolerance
   bound in an unrelated cross-check (never assigned to `tau_aw2`), and the other
   is fed, with `provenance='literal'`, into a call wrapped in `rejected(...)` --
   i.e. `check.py`'s own `validate_coupling` is *required* to raise
   `AdmissionError` for exactly this hard-coded literal, and does; a second,
   similar `rejected(...)` call even feeds the contract's own displayed `tau`
   text with `provenance='contract_parameter_text'` and requires that rejected
   too. The sole assignment of the `tau_aw2` variable anywhere in the file is
   `tau_aw2, steps = aw2_rule(K, R)` (`K` read from the hash-verified AW1 gate,
   `R` from the hash-verified AW1 contract rule) -- never a literal.
6. A self-contained rejection test (mirroring, not importing, `check.py`'s own
   discipline) confirms a locally-defined provenance check accepts only the
   rule-derived value and rejects a hard-coded literal (even the numerically
   correct `10^-8`), a value tagged as read straight from contract text, and a
   correctly-provenanced value that violates the rule bound.

A bonus, non-blocking preview cross-checks that the rule is genuinely sensitive to
`K_2^+`: substituting the gate's quoted crude-tier preview (`~7.9375e6`) into the
same rule gives a different, smaller `tau` (matching the skeptic's own remark that
the crude rule "would give `10^-10`, information only").

### 2. `sign_convention_fixture.py` -- PASS

A one-plaquette exact fixture (`model_is_finite_graph: true`, `transfers_to_aq:
false`; a finite graph, not an AQ-state result): the gauge-invariant Hilbert space
of a single SU(2) plaquette in the character basis `chi_j(U)`, truncated at
`j<=1/2` (2 states) and `j<=1` (3 states), plus a bonus `j<=3/2` (4 states) check.
`H_0` is diagonal with exact-integer Casimir eigenvalues `t(t+2)` (`t=2j`; `j=1/2`
gives `3`, matching "energy 3 in alpha units" used throughout this round); `W`
(the Wilson operator, `(1/2)Tr(U)`) is tridiagonal with off-diagonal entries `1/2`
(the exact SU(2) branching coefficient `chi_{1/2}*chi_j = chi_{j+1/2}+chi_{j-1/2}`
against the Haar-orthonormal character basis); the coupling
`V(tau) = -(tau/24) W` under I1.5 is re-derived (not asserted) from second-order
Rayleigh-Ritz on the `j<=1/2` truncation to reproduce the AW1-admitted first-order
coefficient `+tau/144`.

- **Structural flip identity (exact, at every truncation, not just perturbatively).**
  The centre-parity operator `Z = diag((-1)^t)` satisfies `Z H_0 Z = H_0` and
  `Z W Z = -W` as exact matrix equalities, so `Z H(tau) Z = H(-tau)` exactly --
  the one-plaquette analogue of the AW1 flip lemma's `U_E`.
- **Rayleigh-Schroedinger series, order 5, both required truncations plus the
  bonus one.** The `j<=3/2` (4-state) series reproduces, term for term, the
  series independently reported in the AW1 skeptical review (`skeptic/aw1.md`):
  `tau/144 + 0*tau^2 - 5*tau^3/11943936 + 0*tau^4 + 289*tau^5/6604518850560` --
  a strong independent cross-check that this fixture is the same physical model
  already reviewed in this round, not a new one. All three truncations give the
  exact same first-order coefficient `+1/144` and exact zero even-order terms
  (0, 2, 4), i.e. the truncated series is odd to every computed order.
- **`sign(<W>)=sign(tau)` at first order** and **antisymmetry under
  `tau -> -tau`**: both verified exactly at `tau = +-10^-8` (the AW1/AW2 cap) at
  both required truncations (and the bonus one).
- **Damaging mutations rejected**: an even (zero) first-order coefficient claim,
  a wrong-sign-coupling claim, and a non-antisymmetric claim are each rejected at
  every truncation. A trivial (identity) "flip" operator is confirmed to fail the
  flip identity, so the structural check is not vacuous.

### 3. `preregistration_audit_2.py` -- FAIL (five items; genuine findings, not a bug)

| # | item | result |
|---|---|---|
| 1 | AW1 structural pre-registration audit | PASS |
| 2 | AW2 structural pre-registration audit | PASS |
| 3 | AW1 forward `results.json` contains every AW1 control id | PASS (30/30) |
| 4 | AW1 reverse `results.json` contains every AW1 control id | PASS (30/30) |
| 5 | AW2 forward `results.json` contains every AW2 control id | PASS (23/23) |
| 6 | AW1 gate `accepted` == skeptic `aw1.json.supported_statement` | PASS |
| 7 | AW1 gate `limitations` == skeptic `aw1.json.limitations` | PASS |
| 8 | AX1 structural pre-registration audit | **FAIL** |
| 9 | AX2 structural pre-registration audit | **FAIL** |
| 10 | AY1 structural pre-registration audit | PASS |
| 11 | AY2 structural pre-registration audit | **FAIL** |
| 12 | AZ1 structural pre-registration audit | **FAIL** |
| 13 | AZ2 structural pre-registration audit | **FAIL** |
| . | AW2 gate == skeptic (deferred) | `not_yet_applicable` (no `advisor/aw2-gate.json` or `skeptic/aw2.json` yet; not counted toward pass/fail) |

**AW1/AW2 (frozen): clean.** Every pre-registration field present with an allowed
value, `controls_required.ids == controls` byte-for-byte (30/30 and 23/23), the
closed five-label `sub_labels_allowed` vocabulary verbatim, `error_terms_itemized`
non-empty with the frozen `error_terms_rule` text, both AW1 producers' and AW2's
single producer's `results.json` cover every control id, and the AW1 gate's
`accepted`/`limitations` are byte-identical to `skeptic/aw1.json`'s
`supported_statement`/`limitations`. No AV2-style mirror gap.

**All six drafts: `controls_required.ids == controls`, byte-for-byte, in every
one** (28/28, 24/24, 19/19, 15/15, 18/18, 19/19) -- no repeat of the AV2 mirror
gap anywhere. But five of the six hit one of three distinct, previously
unregistered pre-registration schema/vocabulary gaps, each tied to a genuinely
new model shape that sub-round 1's template (as validated by assistant-1's
script, and consistent with the lens's own loop-1 `recommendation.json`, whose
`R32-J5-DICTIONARY` goal pair used `direction: "statement-only"`) did not
anticipate:

1. **Symbolic (tau-proportional) selected triple -- AX1, AX2.**
   `preregistration.selected_triple_alpha_units` is
   `['tau/24','tau/24','tau/24']`, a formula in `tau` at every entry, not an
   exact-rational constant like AV1/AW1's `['0','0','0']`. This fails the closed
   schema's strict rational-only parse. It is a legitimate model need (route B's
   uniform coefficient `nu = alpha*tau/24` scales with `tau` by construction,
   per `ax1.json`'s own model text), not an authoring error -- but the schema has
   not been extended to accept a formula-valued triple. **AX1 has already frozen
   (`status: frozen_before_production`) while this audit was being run**, with
   the gap unresolved; per AGENTS.md this is repaired by record (in the AX1
   gate), not by silently editing the frozen contract, the same pattern as the
   AW1 item-3 sign-shorthand defect and the AV2 mirror gap.
2. **Undeclared direction `'statement+skeptic'` and `observable.reference_route:
   'n/a'` -- AY2, AZ1.** Both fields are internally consistent within each
   contract (top-level and `preregistration` agree), so this looks like a
   deliberate, consistently-named convention for the newly-introduced "statement
   loop" type (named in parallel with `'single+skeptic'`) rather than a typo --
   but it is not in the closed vocabularies this audit inherits from sub-round 1.
   This task's materials do not include `loop2-response.md`/`loop3-signoff.md`
   section 2 verbatim, so whether it is a signed-off amendment cannot be
   confirmed here.
3. **AZ2's `selected_triple_alpha_units='n/a (finite graph)'` (a string, not a
   3-list) and `tau.value='grid'` (not a rational; it evaluates a declared grid
   `tau_FG_grid=['1/1000','1/100','1/10']`).** Notably, `ALLOWED_MODEL_ID_PREFIXES`
   already includes `'FG('` and `ALLOWED_REFERENCE_ROUTE` already includes
   `'own_finite_graph'` -- both correctly used by AZ2 -- so the schema partially
   anticipated a finite-graph loop, but `selected_triple_alpha_units` and
   `tau.value` were not given a parallel accommodation. A softer, non-blocking
   note: AZ2's `state_provenance` is still the `AQ1_centered_whole_star_
   subsequence...` boilerplate rather than the `finite_graph_ground...` prefix
   the schema separately anticipates for this case; it passes only because the
   closed list is a permissive OR.

Full per-field, per-contract detail (including the exact reasons each field
failed) is in `results.json`.

## Three planning notes for the lens about sub-round 3

**1. What to freeze in AX1/AX2: the symbolic-triple schema gap needs a sign-off
note before AX2 is frozen (AX1 already froze with it unresolved).** This audit
found `preregistration.selected_triple_alpha_units = ['tau/24','tau/24','tau/24']`
in both AX1 and AX2, which fails the closed schema's rational-only parse used
successfully by AV1/AW1's numeric `['0','0','0']`. Since AX1 has already frozen
carrying this gap, the AX1 gate should record it explicitly (repair by record,
per AGENTS.md, not a silent contract edit) and, if the same pattern is wanted for
AX2, either (a) register an explicit formula-valued-triple variant of the schema,
naming exactly which formulas are allowed (e.g. `"tau/24"` per component, tied to
the contract's own `uniform_selected_coefficient_over_alpha` parameter text so it
cannot silently drift to a different formula), or (b) keep the field itself
numeric by reporting the *evaluated* triple at the frozen cap (`1/2400000000` per
component at `tau=10^-8`) with the formula kept only in `parameters`, the same
separation AV1/AW1 already use between `parameters` (prose) and `preregistration`
(machine-checked). Either way, this should be decided once, in writing, before a
second uniform-model sub-round repeats the same gap.

**2. The uniform label: keep enforcing it exactly as update-2.md section 3
specifies, and extend the same discipline to AZ1's continuum-trajectory
statement.** `update-2.md` already registers that AX1/AX2's model text must read
"uniform Kogut-Susskind SU(2) at fixed spacing and strong bare coupling," never
"weak coupling" or "continuum," both of which are explicit `claim_exclusions` in
`ax1.json`/`ax2.json`; `ax1.json`'s model line already states this ("Not weak
coupling, not continuum"), and `ax2.json` inherits the same exclusions. This
audit's structural pass confirms both contracts' `preregistration.claim_
exclusions` carry the full template set verbatim. The same discipline matters
for AZ1 (`continuum-trajectory statement`): its own text already states the
uniform label is strong-coupling-only and that "no number is a fraction of the
continuum problem" (required item 5), and its `controls` list carries
`uniform_label_strong_coupling` and `loop_count_not_fraction` -- keep both
controls' semantics unchanged when AZ1 leaves draft, and grep its eventual
`report.md`/`results.json` for "weak coupling" exactly as update-2.md section 5
item 3 proposes for AX1/AX2's own reports.

**3. The J_0 re-freeze as a pre-registered constant: verify it is genuinely
frozen as a formula-with-proof, not a number chosen after the fact, before AX1's
producers rely on it.** `ax1.json.parameters.J0_resolution` already states
Resolution R1 (`J_0'=29/10^8`) with its two exact contraction inequalities
(`J_0'*148/7 = 1073/175000000 < 1/64` and `2*J_0'*352 = 319/1562500 < 1`) and
names Resolution R2 (capping `|tau|<=7/725000000`) as an excluded, not-selected
alternative -- exactly the "named and excluded in advance" pattern this round's
pre-registration rule requires, and the control `j0_resolution_declared` exists
precisely to reject a producer reusing the old `J_0=7/25000000` at `tau=10^-8`
instead. Since AX1 is now frozen, the concrete follow-up test (already requested
for a future assistant-3 in `update-2.md` section 5, item 2) is to recompute both
inequalities as exact rationals independently and confirm rejection when the old
`J_0` is substituted -- do this before AX1's producers' `check.py` is written, not
after, the same "before production" timing this sub-round 2 audit itself follows.

## Reproducing

```bash
cd research/round32/experts/jung/assistant-2
rm -f results.json
python3 -B coupling_rule_chain.py
python3 -B sign_convention_fixture.py
python3 -B preregistration_audit_2.py   # exits 1: the findings above are real, not a script bug
```

Byte-identical under `python3 -B` and `python3 -B -O` (checked for all three
scripts and the merged `results.json`).

Note: this repository is a live, concurrently-advancing workbench. AX1 moved from
`status: draft` to `status: frozen_before_production` while this audit was being
written; `preregistration_audit_2.py` reads each of AX1/AX2/AY1/AY2/AZ1/AZ2 at
whatever status is currently on disk (recorded per contract in `results.json`'s
`preregistration_audit_2.contracts_audited` and in the "observed contract
statuses" finding) rather than assuming `draft`, since freezing a contract does
not by itself validate its pre-registration fields.
