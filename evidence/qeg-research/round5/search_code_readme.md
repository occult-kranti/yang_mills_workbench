# Bounded proof planner

`proof_search.py` implements the round-5 finite ground positive Horn search contract. It accepts a frozen JSON library with explicit node records and reviewed rules. Every rule is a conjunction of all listed premises; a forward application adds one conclusion only when every premise is already in the fact set. Backward regression removes one goal conclusion and adds that rule's premises, so it never treats an implication as reversible.

The planner keeps exact immutable fact sets, alternates h=0 forward and backward min-heaps for an incumbent, and records push/pop/frontier events. A backward meeting is only an incumbent candidate. The reported `certified_proof` comes from a separate forward uniform-cost search over exact fact sets, then `check_proof` independently replays every rule, premise and cost. The optimality statement is therefore limited to the supplied finite frozen library and its exact state representation. `incomplete`, `not_derivable` and `blocked_goal` are distinct statuses.

Run the supplied fixture with:

```sh
python proof_search.py search_fixture.json --output search_results.json
python test_proof_search.py
```

The current fixture run has 24 tests passing, status `proved`, certified cost 12, 20 forward certificate states popped, 135 bidirectional backward states popped, and a genuine intermediate first meeting with backward cost 5. The fixture's `derived_margin` scenario separately derives `positive_margin` in cost 2 from selected `b=10`, `N=4` meaning Landau levels `n=0,...,4` (five levels), `K=20`, the reviewed alpha bound, positive exact quadrature, and the digamma identity. Its `full_selected_regulator` scenario removes `positive_margin` from the seed set, derives it with `PM01`/`PM02`, and then reaches `selected_theorem` with certified cost 14; those parameter rules reference `round5/theorem_advisor.md` T17–T20. It does not silently treat the margin as an unexplained seed. Validated node/rule mappings are immutable and every replay recomputes the library hash. It maps the prompt's readable names to the advisor's contract as follows: `finite_model`/`physical_state`/`regular_drive`/`positive_margin`/`smooth_family` are the fixed-model assumptions; `norm`, `Upositive`, `energyidentity`, `coercivity`, `energybound`, `compacttrajectory`, `localwellposed`, `globalwellposed`, `smoothflow`, `causal_tangent`, and `selected_theorem` are the finite-model derived atoms. The target name `selected_theorem` is the fixture's name for the contract's `selected_target`.

Nodes carry scope, kind, assumptions, verification, source and version metadata. Rules require a positive integer cost, explicit premises and conclusion, matching scope, a proof reference and a safe review status. Reviewer labels or prose are metadata only: they are never parsed as mathematical proofs. Numerical evidence and unretained conjectures cannot seed an exact proof. A conjectural branch is labeled `proved_conditional` and retains its conditional assumption IDs.

The implementation validates and checks the finite planning trace. It does not prove the differential inequalities or ODE theorems named by the rule references, certify a continuum regulator limit, establish a universal physical theorem, or optimize over mathematical proof routes absent from the frozen rule library. The explicit `physical_infinite_quantumgravity` target is marked blocked in the fixture and produces `blocked_goal`.
