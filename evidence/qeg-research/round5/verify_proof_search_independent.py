"""Independent acceptance checks for the finite proof-planning implementation.

Run directly. --initial preserves a pre-fix diagnostic snapshot. This script
does not import the production unit-test helpers, and the small optimal-cost
oracle enumerates subset states without using the planner's priority queues.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import random
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from proof_search import ContractError, check_proof, load_library, plan


def atom(name, kind="theorem", verification="manual derivation/review"):
    return dict(id=name, statement=f"Proposition {name} within the fixture scope.",
                scope="review_test", kind=kind, assumption_ids=[],
                verification=verification, source="independent synthetic test", version="review-v1")


def fixture(initial, goals, rule_specs):
    names = set(initial) | set(goals)
    for _, premises, conclusion, _ in rule_specs:
        names.update(premises)
        names.add(conclusion)
    return dict(nodes=[atom(n, "declared_hypothesis" if n in initial else "theorem") for n in sorted(names)],
                rules=[dict(id=rid, premises=list(p), conclusion=q, cost=c,
                            scope="review_test", proof_ref="independent test axiom", review_status="reviewed")
                       for rid, p, q, c in rule_specs],
                initial_facts=list(initial), goals=list(goals), blocked_goals=[])


def subset_oracle(data):
    names = [n["id"] for n in data["nodes"]]
    bits = {n: 1 << i for i, n in enumerate(names)}
    mask = lambda seq: sum(bits[n] for n in set(seq))
    start, goal = mask(data["initial_facts"]), mask(data["goals"])
    inf = float("inf")
    costs = {start: 0}
    for state in sorted(range(1 << len(names)), key=int.bit_count):
        if state not in costs:
            continue
        for r in data["rules"]:
            prem, out = mask(r["premises"]), bits[r["conclusion"]]
            if state & prem == prem and state & out == 0:
                nxt = state | out
                costs[nxt] = min(costs.get(nxt, inf), costs[state] + r["cost"])
    values = [cost for state, cost in costs.items() if state & goal == goal]
    return min(values) if values else None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--initial", action="store_true")
    args = parser.parse_args()
    gates = []

    def record(name, ok, details=None):
        gates.append(dict(id=name, passed=bool(ok), details=details))

    def must_reject(name, data):
        try:
            result = plan(data)
        except ContractError as exc:
            record(name, True, str(exc))
        else:
            record(name, False, dict(unexpected_status=result.get("status")))

    suite = subprocess.run([sys.executable, str(ROOT / "test_proof_search.py")], capture_output=True, text=True)
    record("developer_suite_reexecuted", suite.returncode == 0, suite.stdout + suite.stderr)

    original = json.loads((ROOT / "search_fixture.json").read_text())
    result = plan(original)
    meets = [x for x in result.get("search_trace", []) if x.get("phase") == "bidirectional" and x.get("event") == "first_meeting"]
    meeting = meets[0] if meets else {}
    record("actual_intermediate_bidirectional_meeting",
           bool(meeting) and meeting.get("forward_cost", 0) > 0 and meeting.get("backward_cost", 0) > 0
           and set(meeting.get("backward_goals", [])) <= set(meeting.get("forward_facts", []))
           and set(meeting.get("backward_goals", [])) != set(original["goals"]), meeting)
    prefix = [x.get("event") for x in result["search_trace"] if x.get("phase") == "bidirectional"]
    record("both_frontiers_expanded_before_certificate", "forward_pop" in prefix and "backward_pop" in prefix, prefix[:15])

    integrated = None
    for name, scenario in original.get("scenarios", {}).items():
        if scenario.get("goals") == ["selected_theorem"] and "positive_margin" not in scenario.get("initial_facts", []):
            integrated = (name, scenario, plan(scenario))
            break
    integrated_info = None
    ok = False
    if integrated:
        name, scenario, solved = integrated
        steps = [s["rule_id"] for s in solved.get("certified_proof", {}).get("steps", [])]
        ok = all(r in steps for r in ("PM01", "PM02", "R01")) and steps.index("PM01") < steps.index("PM02") < steps.index("R01")
        ok = ok and "positive_margin" not in solved["initial_facts"] and "selected_theorem" in solved["certified_proof"]["final_facts"]
        integrated_info = dict(scenario=name, status=solved["status"], cost=solved.get("certified_cost"), steps=steps)
    record("selected_constants_connect_to_final_theorem", ok, integrated_info)
    if integrated:
        margin = next(n for n in integrated[1]["nodes"] if n["id"] == "positive_margin")
        record("derived_margin_is_typed_as_theorem", margin["kind"] == "theorem", margin)
        causal = next(n for n in integrated[1]["nodes"] if n["id"] == "causal_tangent")
        wording = causal["statement"].lower()
        record("causal_metadata_records_initial_data_conditions",
               "identical initial" in wording and "zero initial tangent" in wording, causal)
    else:
        record("derived_margin_is_typed_as_theorem", False, "integrated scenario missing")
        record("causal_metadata_records_initial_data_conditions", False, "integrated scenario missing")

    saved = json.loads((ROOT / "search_results.json").read_text())
    saved_ok = saved.get("library_hash") == result["library_hash"] and saved.get("certified_cost") == result.get("certified_cost")
    if integrated:
        saved_combined = saved.get("scenario_results", {}).get(integrated[0], {})
        saved_ok = saved_ok and saved_combined.get("library_hash") == integrated[2]["library_hash"] and saved_combined.get("certified_cost") == integrated[2].get("certified_cost")
    record("saved_results_match_fresh_execution", saved_ok, dict(saved_main_hash=saved.get("library_hash"), fresh_main_hash=result["library_hash"]))

    d = fixture(["L"], ["T"], [("r", ["L"], "T", 1)])
    d["nodes"].append(atom("C", "conjecture", "unverified"))
    next(n for n in d["nodes"] if n["id"] == "L").update(kind="theorem", assumption_ids=["C"])
    must_reject("hidden_conjecture_dependency_rejected", d)
    d = fixture(["A"], ["T"], [("r", ["A"], "T", 1)])
    next(n for n in d["nodes"] if n["id"] == "A").update(kind="theorem", verification="unverified")
    must_reject("unverified_theorem_seed_rejected", d)

    lib = load_library(fixture(["A"], ["T"], [("r", ["A"], "T", 1)]))
    old_hash = lib.library_hash
    try:
        lib.rules["r"] = replace(lib.rules["r"], cost=900)
    except (TypeError, AttributeError, ContractError) as exc:
        record("frozen_library_mutation_rejected", True, str(exc))
    else:
        try:
            replay = check_proof(lib, ["r"])
        except ContractError as exc:
            record("frozen_library_mutation_rejected", True, str(exc))
        else:
            record("frozen_library_mutation_rejected", not replay.passed,
                   dict(old_hash_retained=old_hash == lib.library_hash, checker_passed=replay.passed, cost=replay.cost))

    d = fixture(["A"], ["T"], [("direct", ["A"], "T", 9), ("cheap1", ["A"], "B", 1), ("cheap2", ["B"], "T", 1)])
    r = plan(d)
    record("first_meeting_not_mistaken_for_optimum", r["certified_cost"] == 2,
           dict(first=r.get("first_meeting_candidate_cost"), certified=r["certified_cost"]))

    r = plan(fixture(["A"], ["T1", "T2"], [("lemma", ["A"], "L", 2), ("one", ["L"], "T1", 1), ("two", ["L"], "T2", 1)]))
    record("shared_lemma_costs_once", r["certified_cost"] == 4, r["certified_cost"])

    budget_data = fixture(["A"], ["T"], [("r1", ["A"], "B", 1), ("r2", ["B"], "C", 1), ("r3", ["C"], "T", 1)])
    r = plan(budget_data, max_states=1)
    record("forward_budget_does_not_claim_non_derivability", r["status"] == "incomplete", r["status"])
    r = plan(budget_data, max_backward_states=1)
    record("backward_budget_does_not_invalidate_forward_certificate",
           r["status"] == "proved" and r["certified_cost"] == 3 and r["candidate_search_status"] == "incomplete",
           dict(status=r["status"], candidate=r["candidate_search_status"], cost=r.get("certified_cost")))

    for name, d in [
        ("all_conjuncts_required", fixture(["A"], ["T"], [("r", ["A", "B"], "T", 1)])),
        ("reverse_implication_rejected", fixture(["B"], ["A"], [("r", ["A"], "B", 1)])),
        ("unsupported_cycle_has_no_proof", fixture([], ["A"], [("r1", ["A"], "B", 1), ("r2", ["B"], "A", 1)])),
    ]:
        r = plan(d)
        record(name, r["status"] == "not_derivable", r["status"])

    rng = random.Random(50417)
    mismatches = []
    for case in range(64):
        names = [f"A{i}" for i in range(5)]
        rules = []
        for j in range(8):
            q = rng.choice(names)
            premises = rng.sample(names, rng.randint(1, 3))
            rules.append((f"R{j}", premises, q, rng.randint(1, 7)))
        d = fixture(["A0"] if case % 3 else [], ["A3", "A4"] if case % 2 else ["A4"], rules)
        expected = subset_oracle(d)
        solved = plan(d)
        observed = solved.get("certified_cost") if solved["status"] == "proved" else None
        if observed != expected or solved["status"] not in {"proved", "not_derivable"}:
            mismatches.append(dict(case=case, expected=expected, observed=observed, status=solved["status"]))
    record("independent_exhaustive_subset_oracle_64_libraries", not mismatches, dict(cases=64, mismatches=mismatches))

    modified = copy.deepcopy(original)
    modified["goals"] = ["physical_infinite_quantumgravity"]
    r = plan(modified)
    record("full_theory_stays_explicitly_blocked", r["status"] == "blocked_goal", r["reason"])

    report = dict(scope="Finite Horn search and certificate integrity only; analytical lemmas are not kernel verified.",
                  all_gates_passed=all(g["passed"] for g in gates), gates=gates,
                  source_hashes={p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in
                                 (ROOT / "proof_search.py", ROOT / "search_fixture.json", ROOT / "test_proof_search.py", Path(__file__))},
                  selected_library_hash=result["library_hash"])
    out = ROOT / ("search_independent_review_initial.json" if args.initial else "search_independent_review.json")
    out.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(dict(output=str(out), passed=sum(g["passed"] for g in gates), total=len(gates),
                          failed=[g["id"] for g in gates if not g["passed"]])))
    return 0 if report["all_gates_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
