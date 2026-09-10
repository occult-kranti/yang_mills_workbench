"""Bounded, auditable Horn proof planning for the round-5 contract.

The planner operates on a frozen finite library of *ground* positive Horn
rules.  It is deliberately a proof planner rather than a theorem prover:
rule metadata is checked, but the mathematical content referenced by a rule
is not re-derived by this module.
"""

from __future__ import annotations

import argparse
import heapq
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence


class ContractError(ValueError):
    """The supplied finite library does not satisfy the search contract."""


class SearchLimit(RuntimeError):
    """Raised internally when an explicit finite resource budget is hit."""


ALLOWED_KINDS = {
    "definition",
    "theorem",
    "declared_hypothesis",
    "numerical_evidence",
    "conjecture",
    "target",
}
SAFE_REVIEW = {"reviewed", "accepted", "kernel_checked", "verified"}
UNSAFE_REVIEW = {"conjectural", "conjecture", "unresolved", "unsafe", "unverified", "proposed", "numeric evidence", "numerical evidence"}


def _require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContractError(f"{label} must be a nonempty string")
    return value


def _string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list):
        raise ContractError(f"{label} must be a JSON list of strings")
    result: list[str] = []
    seen: set[str] = set()
    for item in value:
        item = _require_string(item, f"{label} item")
        if item not in seen:
            result.append(item)
            seen.add(item)
    return result


def _positive_integer(value: Any, label: str) -> int:
    # bool is an int subclass but is not a cost.
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ContractError(f"{label} must be a positive integer")
    # Python integers are finite and exact; converting a large cost to float can overflow.
    return value


@dataclass(frozen=True)
class Node:
    id: str
    statement: str
    scope: str
    kind: str
    assumption_ids: tuple[str, ...]
    verification: str
    source: str
    version: str


@dataclass(frozen=True)
class Rule:
    id: str
    premises: tuple[str, ...]
    conclusion: str
    cost: int
    scope: str
    proof_ref: str
    review_status: str


@dataclass(frozen=True)
class Library:
    nodes: Mapping[str, Node]
    rules: Mapping[str, Rule]
    initial_facts: frozenset[str]
    goals: frozenset[str]
    blocked_goals: frozenset[str]
    conditional_assumptions: frozenset[str]
    library_hash: str

    @property
    def atoms(self) -> frozenset[str]:
        return frozenset(self.nodes)


@dataclass(frozen=True)
class ProofStep:
    rule_id: str
    premises: tuple[str, ...]
    conclusion: str
    cost: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "premises": list(self.premises),
            "conclusion": self.conclusion,
            "cost": self.cost,
        }


@dataclass(frozen=True)
class CheckedProof:
    passed: bool
    final_facts: frozenset[str]
    cost: int
    steps: tuple[ProofStep, ...]
    errors: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "final_facts": sorted(self.final_facts),
            "cost": self.cost,
            "steps": [step.as_dict() for step in self.steps],
            "errors": list(self.errors),
        }


def load_library(data: Mapping[str, Any]) -> Library:
    """Validate and normalize a JSON-compatible finite rule library."""
    if not isinstance(data, Mapping):
        raise ContractError("library must be a JSON object")

    raw_nodes = data.get("nodes")
    if not isinstance(raw_nodes, list) or not raw_nodes:
        raise ContractError("nodes must be a nonempty JSON list")
    nodes: dict[str, Node] = {}
    for index, raw in enumerate(raw_nodes):
        if not isinstance(raw, Mapping):
            raise ContractError(f"nodes[{index}] must be an object")
        node_id = _require_string(raw.get("id"), f"nodes[{index}].id")
        if node_id in nodes:
            raise ContractError(f"duplicate node id: {node_id}")
        kind = _require_string(raw.get("kind"), f"nodes[{index}].kind")
        if kind not in ALLOWED_KINDS:
            raise ContractError(f"unsupported node kind {kind!r} for {node_id}")
        nodes[node_id] = Node(
            id=node_id,
            statement=_require_string(raw.get("statement"), f"nodes[{index}].statement"),
            scope=_require_string(raw.get("scope"), f"nodes[{index}].scope"),
            kind=kind,
            assumption_ids=tuple(_string_list(raw.get("assumption_ids"), f"nodes[{index}].assumption_ids")),
            verification=_require_string(raw.get("verification"), f"nodes[{index}].verification"),
            source=_require_string(raw.get("source"), f"nodes[{index}].source"),
            version=_require_string(raw.get("version"), f"nodes[{index}].version"),
        )
    for node in nodes.values():
        missing = set(node.assumption_ids) - set(nodes)
        if missing:
            raise ContractError(f"node {node.id} has missing assumption ids: {sorted(missing)}")

    raw_rules = data.get("rules")
    if not isinstance(raw_rules, list):
        raise ContractError("rules must be a JSON list")
    rules: dict[str, Rule] = {}
    for index, raw in enumerate(raw_rules):
        if not isinstance(raw, Mapping):
            raise ContractError(f"rules[{index}] must be an object")
        rule_id = _require_string(raw.get("id"), f"rules[{index}].id")
        if rule_id in rules:
            raise ContractError(f"duplicate rule id: {rule_id}")
        premises = tuple(_string_list(raw.get("premises"), f"rules[{index}].premises"))
        if not premises:
            raise ContractError(f"rules[{index}].premises must contain at least one atom")
        conclusion = _require_string(raw.get("conclusion"), f"rules[{index}].conclusion")
        cost = _positive_integer(raw.get("cost"), f"rules[{index}].cost")
        scope = _require_string(raw.get("scope"), f"rules[{index}].scope")
        proof_ref = _require_string(raw.get("proof_ref"), f"rules[{index}].proof_ref")
        review_status = _require_string(raw.get("review_status"), f"rules[{index}].review_status").lower()
        if review_status in UNSAFE_REVIEW or review_status not in SAFE_REVIEW:
            raise ContractError(f"rule {rule_id} lacks a safe reviewed inference certificate")
        refs = set(premises) | {conclusion}
        missing = refs - set(nodes)
        if missing:
            raise ContractError(f"rule {rule_id} has missing atom ids: {sorted(missing)}")
        if nodes[conclusion].scope != scope:
            raise ContractError(f"rule {rule_id} scope does not match conclusion {conclusion}")
        if nodes[conclusion].kind == "numerical_evidence":
            raise ContractError(f"rule {rule_id} cannot conclude numerical evidence as an exact atom")
        if nodes[conclusion].kind != "conjecture" and nodes[conclusion].verification.lower().strip() in UNSAFE_REVIEW:
            raise ContractError(f"rule {rule_id} conclusion {conclusion} has no mathematical verification certificate")
        mismatched = sorted(p for p in premises if nodes[p].scope != scope)
        if mismatched:
            raise ContractError(f"rule {rule_id} mixes scopes: {mismatched}")
        inherited_assumptions = set(premises)
        for premise in premises:
            inherited_assumptions.update(nodes[premise].assumption_ids)
        dropped = set(nodes[conclusion].assumption_ids) - inherited_assumptions
        if dropped:
            raise ContractError(f"rule {rule_id} silently drops conclusion assumptions: {sorted(dropped)}")
        rules[rule_id] = Rule(rule_id, premises, conclusion, cost, scope, proof_ref, review_status)

    initial_raw = data.get("initial_facts", data.get("initial_fact_ids"))
    goals_raw = data.get("goals", data.get("target_ids", data.get("target")))
    initial_facts = frozenset(_string_list(initial_raw, "initial_facts"))
    goals = frozenset(_string_list(goals_raw, "goals"))
    if not goals:
        raise ContractError("goals must contain at least one atom")
    blocked_goals = frozenset(_string_list(data.get("blocked_goals", []), "blocked_goals"))
    conditional = frozenset(_string_list(data.get("conditional_assumptions", []), "conditional_assumptions"))
    for label, values in (("initial_facts", initial_facts), ("goals", goals), ("blocked_goals", blocked_goals), ("conditional_assumptions", conditional)):
        missing = values - set(nodes)
        if missing:
            raise ContractError(f"{label} has missing atom ids: {sorted(missing)}")
    for node_id in conditional:
        if nodes[node_id].kind != "conjecture":
            raise ContractError(f"conditional assumption {node_id} is not a conjecture node")
    for node_id in initial_facts:
        kind = nodes[node_id].kind
        if kind in {"numerical_evidence", "target"}:
            raise ContractError(f"{node_id} cannot seed an exact proof (node kind {kind})")
        if kind == "conjecture" and node_id not in conditional:
            raise ContractError(f"conjecture {node_id} requires an explicit conditional assumption")
        if kind != "conjecture" and nodes[node_id].verification.lower().strip() in UNSAFE_REVIEW:
            raise ContractError(f"{node_id} cannot seed an exact proof without verified theorem metadata")
        undisclosed = set(nodes[node_id].assumption_ids) - set(initial_facts) - set(conditional)
        if undisclosed:
            raise ContractError(f"seed {node_id} has undisclosed assumptions: {sorted(undisclosed)}")
    if not conditional <= initial_facts:
        raise ContractError("conditional assumptions must also be retained as initial facts")
    # A rule touching a conjecture is legal only inside a conditional branch.
    for rule in rules.values():
        conjectural = {p for p in rule.premises if nodes[p].kind == "conjecture"}
        if nodes[rule.conclusion].kind == "conjecture":
            conjectural.add(rule.conclusion)
        if conjectural - conditional:
            raise ContractError(f"rule {rule.id} launders conjectural atoms without retained assumptions")

    # The contract uses a frozen-library hash in every checker report.  Hash
    # canonical validated records, excluding any caller-supplied hash.
    canonical = {
        "nodes": [vars(nodes[k]) for k in sorted(nodes)],
        "rules": [vars(rules[k]) for k in sorted(rules)],
        "initial_facts": sorted(initial_facts),
        "goals": sorted(goals),
        "blocked_goals": sorted(blocked_goals),
        "conditional_assumptions": sorted(conditional),
    }
    import hashlib

    library_hash = hashlib.sha256(json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return Library(MappingProxyType(nodes), MappingProxyType(rules), initial_facts, goals, blocked_goals, conditional, library_hash)


def _library_hash(library: Library) -> str:
    """Recompute the frozen-library digest before trusting a replay."""
    canonical = {
        "nodes": [vars(library.nodes[k]) for k in sorted(library.nodes)],
        "rules": [vars(library.rules[k]) for k in sorted(library.rules)],
        "initial_facts": sorted(library.initial_facts),
        "goals": sorted(library.goals),
        "blocked_goals": sorted(library.blocked_goals),
        "conditional_assumptions": sorted(library.conditional_assumptions),
    }
    import hashlib

    return hashlib.sha256(json.dumps(canonical, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def check_proof(library: Library, rule_ids: Sequence[str], goals: Iterable[str] | None = None) -> CheckedProof:
    """Replay a rule sequence independently of the search implementation."""
    current = set(library.initial_facts)
    if _library_hash(library) != library.library_hash:
        return CheckedProof(False, frozenset(current), 0, (), ("library hash mismatch; frozen rule library was mutated",))
    steps: list[ProofStep] = []
    errors: list[str] = []
    total = 0
    for index, rule_id in enumerate(rule_ids):
        if rule_id not in library.rules:
            errors.append(f"step {index}: unknown rule {rule_id}")
            continue
        rule = library.rules[rule_id]
        if rule.review_status not in SAFE_REVIEW:
            errors.append(f"step {index}: rule {rule_id} is not reviewed")
        missing = set(rule.premises) - current
        if missing:
            errors.append(f"step {index}: rule {rule_id} missing premises {sorted(missing)}")
        # Keep valid redundant applications in the trace, as the contract
        # permits, and charge their actual rule cost.
        if not missing:
            current.add(rule.conclusion)
            total += rule.cost
            steps.append(ProofStep(rule.id, rule.premises, rule.conclusion, rule.cost))
    target = set(library.goals if goals is None else goals)
    missing_target = target - current
    if missing_target:
        errors.append(f"final facts miss target atoms {sorted(missing_target)}")
    return CheckedProof(not errors, frozenset(current), total, tuple(steps), tuple(errors))


def _proof_from_ids(library: Library, ids: Sequence[str]) -> CheckedProof:
    return check_proof(library, ids)


def _forward_uniform_cost(library: Library, max_states: int, trace: list[dict[str, Any]]) -> dict[str, Any]:
    start = library.initial_facts
    counter = 0
    heap: list[tuple[int, tuple[str, ...], int, frozenset[str], tuple[str, ...]]] = [(0, (), counter, start, ())]
    best: dict[frozenset[str], tuple[int, tuple[str, ...]]] = {start: (0, ())}
    popped: list[tuple[frozenset[str], int, tuple[str, ...]]] = []
    # Keep generated candidates as well as popped states.  The bidirectional
    # incumbent may notice a generated expensive route before the cheaper
    # route is popped; only the independent certificate may call a route
    # optimal.
    discovered: list[tuple[frozenset[str], int, tuple[str, ...]]] = [(start, 0, ())]

    def result(status: str, **extra: Any) -> dict[str, Any]:
        popped_keys = {facts for facts, _, _ in popped}
        frontier = [(facts, cost, path) for facts, (cost, path) in best.items() if facts not in popped_keys]
        return {"status": status, "popped": popped, "discovered": discovered, "best": best, "frontier": frontier, "trace": trace, **extra}

    while heap:
        cost, path_key, _, facts, path = heapq.heappop(heap)
        if best.get(facts) != (cost, path_key):
            continue
        if len(popped) >= max_states:
            return result("incomplete")
        popped.append((facts, cost, path))
        trace.append({"phase": "forward", "event": "pop", "cost": cost, "facts": sorted(facts), "rule_ids": list(path)})
        if library.goals <= facts:
            checked = _proof_from_ids(library, path)
            if not checked.passed or checked.cost != cost:
                raise ContractError(f"internal forward proof replay mismatch: {checked.errors}")
            return result("proved", proof=checked)
        for rule in sorted(library.rules.values(), key=lambda r: r.id):
            if rule.conclusion in facts or not set(rule.premises) <= facts:
                continue
            new_facts = frozenset(set(facts) | {rule.conclusion})
            new_cost = cost + rule.cost
            new_path = path + (rule.id,)
            old = best.get(new_facts)
            candidate = (new_cost, new_path)
            if old is None or candidate < old:
                best[new_facts] = candidate
                counter += 1
                heapq.heappush(heap, (new_cost, new_path, counter, new_facts, new_path))
                discovered.append((new_facts, new_cost, new_path))
                trace.append({"phase": "forward", "event": "push", "cost": new_cost, "facts": sorted(new_facts), "rule_id": rule.id})
    return result("not_derivable")


def _bidirectional_candidate(library: Library, max_forward: int, max_backward: int, trace: list[dict[str, Any]]) -> dict[str, Any]:
    """Interleave h=0 forward and regression frontiers for an incumbent.

    This pass is intentionally separate from the exact forward certificate.
    A meet is accepted as a candidate immediately, even when a cheaper route
    may still be in either heap.
    """
    seq = 0
    f_heap: list[tuple[int, tuple[str, ...], int, frozenset[str], tuple[str, ...]]] = [(0, (), seq, library.initial_facts, ())]
    b_heap: list[tuple[int, tuple[str, ...], int, frozenset[str], tuple[str, ...]]] = [(0, (), seq, library.goals, ())]
    f_best: dict[frozenset[str], tuple[int, tuple[str, ...]]] = {library.initial_facts: (0, ())}
    b_best: dict[frozenset[str], tuple[int, tuple[str, ...]]] = {library.goals: (0, ())}
    f_seen: list[tuple[frozenset[str], int, tuple[str, ...]]] = []
    b_seen: list[tuple[frozenset[str], int, tuple[str, ...]]] = []
    f_popped = b_popped = 0

    def candidate(facts: frozenset[str], fc: int, fp: tuple[str, ...], goals: frozenset[str], bc: int, bp: tuple[str, ...]) -> dict[str, Any]:
        ids = fp + tuple(reversed(bp))
        checked = check_proof(library, ids)
        trace.append({"phase": "bidirectional", "event": "first_meeting", "forward_cost": fc, "backward_cost": bc, "cost": checked.cost, "forward_facts": sorted(facts), "backward_goals": sorted(goals), "rule_ids": list(ids), "checker_passed": checked.passed})
        return {"status": "candidate" if checked.passed else "invalid_candidate", "candidate": checked, "forward_states": f_popped, "backward_states": b_popped}

    while f_heap or b_heap:
        if not f_heap:
            direction = "backward"
        elif not b_heap:
            direction = "forward"
        else:
            # Deterministic h=0 tie break: forward expands first.
            direction = "forward" if (f_heap[0][0], 0) <= (b_heap[0][0], 1) else "backward"
        if direction == "forward":
            cost, path_key, _, facts, path = heapq.heappop(f_heap)
            if f_best.get(facts) != (cost, path_key):
                continue
            if f_popped >= max_forward:
                return {"status": "incomplete", "forward_states": f_popped, "backward_states": b_popped}
            f_popped += 1
            f_seen.append((facts, cost, path))
            trace.append({"phase": "bidirectional", "event": "forward_pop", "cost": cost, "facts": sorted(facts), "rule_ids": list(path)})
            for goals, bc, bp in b_seen:
                if goals <= facts:
                    return candidate(facts, cost, path, goals, bc, bp)
            for rule in sorted(library.rules.values(), key=lambda r: r.id):
                if rule.conclusion in facts or not set(rule.premises) <= facts:
                    continue
                new_facts = frozenset(set(facts) | {rule.conclusion})
                new_cost = cost + rule.cost
                new_path = path + (rule.id,)
                old = f_best.get(new_facts)
                if old is None or (new_cost, new_path) < old:
                    f_best[new_facts] = (new_cost, new_path)
                    seq += 1
                    heapq.heappush(f_heap, (new_cost, new_path, seq, new_facts, new_path))
                    trace.append({"phase": "bidirectional", "event": "forward_push", "cost": new_cost, "facts": sorted(new_facts), "rule_id": rule.id})
                    for goals, bc, bp in b_seen:
                        if goals <= new_facts:
                            return candidate(new_facts, new_cost, new_path, goals, bc, bp)
        else:
            cost, path_key, _, goals, path = heapq.heappop(b_heap)
            if b_best.get(goals) != (cost, path_key):
                continue
            if b_popped >= max_backward:
                return {"status": "incomplete", "forward_states": f_popped, "backward_states": b_popped}
            b_popped += 1
            b_seen.append((goals, cost, path))
            trace.append({"phase": "bidirectional", "event": "backward_pop", "cost": cost, "goals": sorted(goals), "rule_ids": list(path)})
            for facts, fc, fp in f_seen:
                if goals <= facts:
                    return candidate(facts, fc, fp, goals, cost, path)
            for q in sorted(goals):
                for rule in sorted(library.rules.values(), key=lambda r: r.id):
                    if rule.conclusion != q:
                        continue
                    new_goals = frozenset((set(goals) - {q}) | set(rule.premises))
                    if new_goals == goals:
                        continue
                    new_cost = cost + rule.cost
                    new_path = path + (rule.id,)
                    old = b_best.get(new_goals)
                    if old is None or (new_cost, new_path) < old:
                        b_best[new_goals] = (new_cost, new_path)
                        seq += 1
                        heapq.heappush(b_heap, (new_cost, new_path, seq, new_goals, new_path))
                        trace.append({"phase": "bidirectional", "event": "backward_push", "cost": new_cost, "goals": sorted(new_goals), "rule_id": rule.id})
                        for facts, fc, fp in f_seen:
                            if new_goals <= facts:
                                return candidate(facts, fc, fp, new_goals, new_cost, new_path)
    return {"status": "exhausted", "forward_states": f_popped, "backward_states": b_popped}


def _backward_first_meeting(library: Library, forward_states: list[tuple[frozenset[str], int, tuple[str, ...]]], max_states: int, trace: list[dict[str, Any]]) -> dict[str, Any]:
    counter = 0
    start = library.goals
    heap: list[tuple[int, tuple[str, ...], int, frozenset[str], tuple[str, ...]]] = [(0, (), counter, start, ())]
    best: dict[frozenset[str], tuple[int, tuple[str, ...]]] = {start: (0, ())}
    popped = 0
    while heap:
        cost, path_key, _, goals, path = heapq.heappop(heap)
        if best.get(goals) != (cost, path_key):
            continue
        if popped >= max_states:
            return {"status": "incomplete", "trace": trace, "states": popped}
        popped += 1
        trace.append({"phase": "backward", "event": "pop", "cost": cost, "goals": sorted(goals), "rule_ids": list(path)})
        matches = [(f, fc, fp) for f, fc, fp in forward_states if goals <= f]
        if matches:
            # Preserve generated order: this is deliberately only the first
            # incumbent.  It may be more expensive than the certified route.
            f, fc, fp = matches[0]
            candidate_ids = fp + tuple(reversed(path))
            checked = _proof_from_ids(library, candidate_ids)
            trace.append({"phase": "backward", "event": "first_meeting", "cost": fc + cost, "forward_cost": fc, "backward_cost": cost, "forward_facts": sorted(f), "backward_goals": sorted(goals), "rule_ids": list(candidate_ids), "checker_passed": checked.passed})
            return {"status": "candidate", "candidate": checked, "forward_cost": fc, "backward_cost": cost, "forward_facts": f, "backward_goals": goals, "trace": trace, "states": popped}
        for q in sorted(goals):
            for rule in sorted(library.rules.values(), key=lambda r: r.id):
                if rule.conclusion != q:
                    continue
                new_goals = frozenset((set(goals) - {q}) | set(rule.premises))
                if new_goals == goals:
                    continue
                new_cost = cost + rule.cost
                new_path = path + (rule.id,)
                old = best.get(new_goals)
                candidate = (new_cost, new_path)
                if old is None or candidate < old:
                    best[new_goals] = candidate
                    counter += 1
                    heapq.heappush(heap, (new_cost, new_path, counter, new_goals, new_path))
                    trace.append({"phase": "backward", "event": "push", "cost": new_cost, "goals": sorted(new_goals), "rule_id": rule.id})
    return {"status": "exhausted", "trace": trace, "states": popped}


def plan(library_or_data: Library | Mapping[str, Any], *, max_states: int = 100_000, max_backward_states: int | None = None) -> dict[str, Any]:
    """Run bounded bidirectional planning and exact forward certification."""
    library = library_or_data if isinstance(library_or_data, Library) else load_library(library_or_data)
    if _library_hash(library) != library.library_hash:
        raise ContractError("library hash mismatch; frozen rule library was mutated")
    if isinstance(max_states, bool) or not isinstance(max_states, int) or max_states <= 0:
        raise ContractError("max_states must be a positive integer")
    if max_backward_states is None:
        max_backward_states = max_states
    if isinstance(max_backward_states, bool) or not isinstance(max_backward_states, int) or max_backward_states <= 0:
        raise ContractError("max_backward_states must be a positive integer")

    common: dict[str, Any] = {
        "library_hash": library.library_hash,
        "initial_facts": sorted(library.initial_facts),
        "goals": sorted(library.goals),
        "assumptions": sorted(library.initial_facts),
        # Legacy conditional flag means retained conjectures only, not absence of model assumptions.
        "conditional": bool(library.conditional_assumptions),
        "conditional_flag_meaning": "retained conjectural assumptions only",
        "declared_assumption_ids": sorted(atom for atom in library.initial_facts if library.nodes[atom].kind == "declared_hypothesis"),
        "conditional_on_declared_assumptions": any(library.nodes[atom].kind == "declared_hypothesis" for atom in library.initial_facts),
        "conjectural_assumptions": sorted(library.conditional_assumptions),
        "result_kind": "checked finite Horn trace under listed premises",
        "conditional_assumptions": sorted(library.conditional_assumptions),
        "optimality_scope": "least cost over the supplied finite frozen ground rule library and exact fact-set states; h=0",
        "limits": {"forward_states": max_states, "backward_states": max_backward_states},
    }
    if library.goals & library.blocked_goals:
        blocked = sorted(library.goals & library.blocked_goals)
        common.update({"status": "blocked_goal", "reason": "target explicitly marked unresolved/blocked in the supplied library", "blocked_goals": blocked, "blocked_subgoals": blocked, "missing_inference_certificates": [f"no reviewed sufficient rule was supplied for {atom}" for atom in blocked], "search_trace": []})
        return common

    trace: list[dict[str, Any]] = []
    bidirectional = _bidirectional_candidate(library, max_states, max_backward_states, trace)
    certificate_trace: list[dict[str, Any]] = []
    forward = _forward_uniform_cost(library, max_states, certificate_trace)
    trace.extend(certificate_trace)
    if forward["status"] == "incomplete":
        common.update({"status": "incomplete", "reason": "forward exact-state budget exhausted", "candidate_search_status": bidirectional["status"], "search_trace": trace, "forward_states_popped": len(forward["popped"]), "backward_states_popped": bidirectional.get("backward_states", 0)})
        return common
    common["search_trace"] = trace
    common["forward_states_popped"] = len(forward["popped"])
    common["backward_states_popped"] = bidirectional.get("backward_states", 0)
    common["candidate_search_status"] = bidirectional["status"]
    common["frontier"] = [
        {"facts": sorted(facts), "cost": cost, "rule_ids": list(path)}
        for facts, cost, path in forward.get("frontier", [])
    ]
    if forward["status"] == "not_derivable":
        common.update({"status": "not_derivable", "reason": "not derivable in this finite rule library"})
    else:
        certified: CheckedProof = forward["proof"]
        common.update({
            "status": "proved_conditional" if library.conditional_assumptions else "proved",
            "certified_cost": certified.cost,
            "certified_proof": certified.as_dict(),
            "optimality_certificate": "independent forward uniform-cost goal pop",
        })
        if bidirectional.get("status") == "candidate":
            candidate: CheckedProof = bidirectional["candidate"]
            common["first_meeting_candidate"] = candidate.as_dict()
            common["first_meeting_candidate_cost"] = candidate.cost
            common["first_meeting_was_certified_optimal"] = candidate.passed and candidate.cost == certified.cost
    return common


def load_json(path: str | Path) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ContractError("top-level JSON must be an object")
    return data


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("library", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--max-states", type=int, default=100_000)
    parser.add_argument("--max-backward-states", type=int)
    args = parser.parse_args(argv)
    try:
        data = load_json(args.library)
        result = plan(data, max_states=args.max_states, max_backward_states=args.max_backward_states)
        scenarios = data.get("scenarios")
        if isinstance(scenarios, Mapping):
            result["scenario_results"] = {
                name: plan(scenario, max_states=args.max_states, max_backward_states=args.max_backward_states)
                for name, scenario in scenarios.items()
                if isinstance(name, str) and isinstance(scenario, Mapping)
            }
    except (ContractError, OSError, json.JSONDecodeError) as exc:
        print(f"proof_search: {exc}", file=sys.stderr)
        return 2
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
