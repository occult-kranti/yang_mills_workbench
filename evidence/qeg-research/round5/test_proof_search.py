"""Contract tests for the bounded proof planner.

Run with the standard library only: ``python -m unittest -v`` from this
directory (or ``python test_proof_search.py``).
"""

from __future__ import annotations

import copy
import json
import math
import unittest
from dataclasses import replace
from pathlib import Path

from proof_search import ContractError, check_proof, load_library, plan


ROOT = Path(__file__).parent


def node(atom: str, *, scope: str = "finite", kind: str = "theorem", verification: str = "manual derivation/review") -> dict:
    return {
        "id": atom,
        "statement": f"Reviewed atom {atom}.",
        "scope": scope,
        "kind": kind,
        "assumption_ids": [],
        "verification": verification,
        "source": "test fixture",
        "version": "test-v1",
    }


def library(initial: list[str], goals: list[str], rules: list[tuple[str, list[str], str, int]], *, extra_nodes: list[dict] | None = None, blocked: list[str] | None = None) -> dict:
    atoms = set(initial) | set(goals)
    for _, premises, conclusion, _ in rules:
        atoms.update(premises)
        atoms.add(conclusion)
    nodes = [node(atom, kind="declared_hypothesis" if atom in initial else "theorem") for atom in sorted(atoms)]
    if extra_nodes:
        nodes.extend(extra_nodes)
    return {
        "initial_facts": initial,
        "goals": goals,
        "blocked_goals": blocked or [],
        "nodes": nodes,
        "rules": [
            {"id": rid, "premises": premises, "conclusion": conclusion, "cost": cost,
             "scope": "finite", "proof_ref": "test reviewed rule", "review_status": "reviewed"}
            for rid, premises, conclusion, cost in rules
        ],
    }


class ProofSearchTests(unittest.TestCase):
    def test_main_fixture_proves_target_and_reports_counts(self) -> None:
        with (ROOT / "search_fixture.json").open(encoding="utf-8") as handle:
            result = plan(json.load(handle))
        self.assertIn(result["status"], {"proved", "proved_conditional"})
        self.assertTrue(result["certified_proof"]["passed"])
        self.assertEqual(result["certified_cost"], 12)
        self.assertGreater(result["forward_states_popped"], 0)
        self.assertGreater(result["backward_states_popped"], 1)
        meeting = next(item for item in result["search_trace"] if item.get("event") == "first_meeting" and item.get("phase") == "bidirectional")
        self.assertGreater(meeting["backward_cost"], 0)
        self.assertNotEqual(meeting["backward_goals"], ["selected_theorem"])
        self.assertEqual(result["optimality_certificate"], "independent forward uniform-cost goal pop")

    def test_selected_parameter_margin_is_derived_in_second_fixture(self) -> None:
        with (ROOT / "search_fixture.json").open(encoding="utf-8") as handle:
            data = json.load(handle)
        result = plan(data["scenarios"]["derived_margin"])
        self.assertEqual(result["status"], "proved")
        self.assertEqual(result["certified_cost"], 2)
        self.assertEqual([step["rule_id"] for step in result["certified_proof"]["steps"]], ["PM01", "PM02"])

    def test_full_selected_regulator_derives_margin_then_target(self) -> None:
        with (ROOT / "search_fixture.json").open(encoding="utf-8") as handle:
            data = json.load(handle)
        scenario = data["scenarios"]["full_selected_regulator"]
        self.assertNotIn("positive_margin", scenario["initial_facts"])
        result = plan(scenario)
        self.assertEqual(result["status"], "proved")
        self.assertEqual(result["certified_cost"], 14)
        self.assertEqual(
            [step["rule_id"] for step in result["certified_proof"]["steps"]],
            ["PM01", "PM02", "R01", "R02", "R03", "R04", "R05", "R06", "R07", "R08", "R09", "R10", "R11", "R12"],
        )

    def test_conjunction_requires_all_premises(self) -> None:
        result = plan(library(["A"], ["T"], [("r", ["A", "B"], "T", 1)]))
        self.assertEqual(result["status"], "not_derivable")

    def test_reverse_implication_is_not_allowed(self) -> None:
        result = plan(library(["B"], ["A"], [("r", ["A"], "B", 1)]))
        self.assertEqual(result["status"], "not_derivable")

    def test_cycle_without_seed_is_not_support(self) -> None:
        result = plan(library([], ["B"], [("ab", ["A"], "B", 1), ("ba", ["B"], "A", 1)]))
        self.assertEqual(result["status"], "not_derivable")

    def test_duplicate_initial_facts_are_set_semantics(self) -> None:
        result = plan(library(["A", "A"], ["B"], [("r", ["A"], "B", 2)]))
        self.assertEqual(result["status"], "proved")
        self.assertEqual(result["certified_cost"], 2)
        self.assertEqual(result["initial_facts"], ["A"])

    def test_cost_ties_are_deterministic(self) -> None:
        data = library(["A"], ["T"], [("z_rule", ["A"], "T", 2), ("a_rule", ["A"], "T", 2)])
        result = plan(data)
        self.assertEqual(result["status"], "proved")
        self.assertEqual(result["certified_cost"], 2)
        self.assertEqual(result["certified_proof"]["steps"][0]["rule_id"], "a_rule")

    def test_first_meeting_candidate_is_not_automatically_optimal(self) -> None:
        # A direct route costs nine, while the two-step route costs two.  The
        # independent exact-state forward certificate must report two.
        result = plan(library(["A"], ["T"], [("direct", ["A"], "T", 9), ("cheap1", ["A"], "B", 1), ("cheap2", ["B"], "T", 1)]))
        self.assertEqual(result["certified_cost"], 2)
        self.assertTrue(result["first_meeting_candidate"]["passed"])
        self.assertGreaterEqual(result["first_meeting_candidate_cost"], 2)

    def test_costs_are_replayed_from_frozen_rules(self) -> None:
        lib = load_library(library(["A"], ["T"], [("r", ["A"], "T", 7)]))
        checked = check_proof(lib, ["r"])
        self.assertTrue(checked.passed)
        self.assertEqual(checked.cost, 7)

    def test_mutated_sequence_fails_independent_checker(self) -> None:
        lib = load_library(library(["A"], ["T"], [("r1", ["A"], "B", 1), ("r2", ["B"], "T", 1)]))
        checked = check_proof(lib, ["r2", "r1"])
        self.assertFalse(checked.passed)
        self.assertTrue(any("missing premises" in error for error in checked.errors))

    def test_unknown_ids_rejected_before_search(self) -> None:
        data = library(["A"], ["T"], [("r", ["A"], "T", 1)])
        data["rules"][0]["premises"] = ["MISSING"]
        with self.assertRaises(ContractError):
            load_library(data)

    def test_missing_review_certificate_rejected(self) -> None:
        data = library(["A"], ["T"], [("r", ["A"], "T", 1)])
        data["rules"][0]["review_status"] = "unresolved"
        with self.assertRaises(ContractError):
            load_library(data)

    def test_nonpositive_and_nonfinite_costs_rejected(self) -> None:
        for bad in (0, -1, math.nan, math.inf, True):
            with self.subTest(cost=bad):
                data = library(["A"], ["T"], [("r", ["A"], "T", bad)])
                with self.assertRaises(ContractError):
                    load_library(data)

    def test_scope_mutation_rejected(self) -> None:
        data = library(["A"], ["T"], [("r", ["A"], "T", 1)])
        data["nodes"] = [dict(item, scope=("continuum" if item["id"] == "T" else item["scope"])) for item in data["nodes"]]
        with self.assertRaises(ContractError):
            load_library(data)

    def test_conjecture_cannot_be_laundered_as_exact_seed(self) -> None:
        data = library(["C"], ["T"], [("r", ["C"], "T", 1)])
        data["nodes"] = [dict(item, kind="conjecture", verification="unverified") if item["id"] == "C" else item for item in data["nodes"]]
        with self.assertRaises(ContractError):
            load_library(data)

    def test_seed_cannot_hide_unretained_conjectural_assumption(self) -> None:
        data = library(["L"], ["T"], [("r", ["L"], "T", 1)])
        data["nodes"].append(node("C", kind="conjecture", verification="unverified"))
        data["nodes"] = [dict(item, assumption_ids=["C"]) if item["id"] == "L" else item for item in data["nodes"]]
        with self.assertRaises(ContractError):
            load_library(data)

    def test_unverified_theorem_cannot_be_an_exact_seed(self) -> None:
        data = library(["A"], ["T"], [("r", ["A"], "T", 1)])
        data["nodes"] = [dict(item, verification="unverified") if item["id"] == "A" else item for item in data["nodes"]]
        with self.assertRaises(ContractError):
            load_library(data)

    def test_library_mappings_are_immutable_and_hash_checked(self) -> None:
        lib = load_library(library(["A"], ["T"], [("r", ["A"], "T", 1)]))
        with self.assertRaises(TypeError):
            lib.rules["r"] = replace(lib.rules["r"], cost=900)  # type: ignore[index]
        mutated = replace(lib, rules={**lib.rules, "r": replace(lib.rules["r"], cost=900)})
        checked = check_proof(mutated, ["r"])
        self.assertFalse(checked.passed)
        self.assertIn("library hash mismatch", checked.errors[0])

    def test_conjectural_branch_is_explicitly_conditional(self) -> None:
        data = library(["C"], ["T"], [("r", ["C"], "T", 1)])
        data["nodes"] = [dict(item, kind="conjecture", verification="unverified") if item["id"] == "C" else item for item in data["nodes"]]
        data["conditional_assumptions"] = ["C"]
        result = plan(data)
        self.assertEqual(result["status"], "proved_conditional")
        self.assertTrue(result["conditional"])

    def test_explicit_blocked_goal_status(self) -> None:
        data = library([], ["Q"], [], blocked=["Q"])
        result = plan(data)
        self.assertEqual(result["status"], "blocked_goal")

    def test_resource_limit_is_incomplete(self) -> None:
        data = library(["A"], ["T"], [("r1", ["A"], "B", 1), ("r2", ["B"], "C", 1), ("r3", ["C"], "T", 1)])
        result = plan(data, max_states=1)
        self.assertEqual(result["status"], "incomplete")

    def test_shared_lemma_is_paid_once_and_reused(self) -> None:
        data = library(["A"], ["T1", "T2"], [("lemma", ["A"], "L", 2), ("one", ["L"], "T1", 1), ("two", ["L"], "T2", 1)])
        result = plan(data)
        self.assertEqual(result["status"], "proved")
        self.assertEqual(result["certified_cost"], 4)
        self.assertEqual(result["certified_proof"]["steps"][0]["rule_id"], "lemma")

    def test_full_theory_fixture_is_blocked(self) -> None:
        with (ROOT / "search_fixture.json").open(encoding="utf-8") as handle:
            data = json.load(handle)
        data["goals"] = ["physical_infinite_quantumgravity"]
        result = plan(data)
        self.assertEqual(result["status"], "blocked_goal")


if __name__ == "__main__":
    unittest.main(verbosity=2)
