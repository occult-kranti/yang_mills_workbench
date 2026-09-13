#!/usr/bin/env python3
"""Build the Round19 paired research view.

The generated browser model is self-contained: it embeds the small reviewed JSON
payload and never fetches data at runtime. If later advisor gates or evidence
manifests are present, this builder preserves them as partial milestones instead
of overwriting the provisional route text.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
ROUND = ROOT / "research" / "round19"
ADVISOR = ROUND / "advisor"
DIST = ROOT / "dist"
CONTENT = ROUND / "site-content.json"
EXCEPTION_LEDGER = ROUND / "exception-ledger.json"
OUTPUT = DIST / "research-paired.js"
OVERVIEW = ROUND / "overview.html"

VALID_STATES = {"pending", "running", "accepted", "limited", "rejected"}
LOOP_IDS = ("A1", "A2", "B1", "B2", "C1", "C2")
REPO = "https://github.com/occult-kranti/yang_mills_workbench"
RESEARCH_BRANCH = "research/round19-paired"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def safe_state(value: Any, default: str = "pending") -> str:
    value = str(value or default).lower()
    return value if value in VALID_STATES else default


def repo_href(repo_path: str) -> str:
    return f"{REPO}/blob/{RESEARCH_BRANCH}/{repo_path}"


def add_or_update_evidence(content: dict[str, Any], item: dict[str, Any]) -> None:
    evidence = content.setdefault("evidence", [])
    key = item["key"]
    for current in evidence:
        if current.get("key") == key:
            current.update({k: v for k, v in item.items() if v is not None})
            return
    evidence.append({k: v for k, v in item.items() if v is not None})


def attach_file_metadata(content: dict[str, Any], key: str, title: str, repo_path: str, state: str, summary: str) -> None:
    path = ROOT / repo_path
    item = {
        "key": key,
        "title": title,
        "state": safe_state(state),
        "repo_path": repo_path,
        "href": repo_href(repo_path),
        "summary": summary,
        "exists": path.exists(),
        "sha256": sha256(path) if path.exists() else None,
    }
    add_or_update_evidence(content, item)


def round19_repo_path(path: str) -> str:
    clean = str(path).lstrip("/")
    if clean.startswith("research/round19/"):
        return clean
    return f"research/round19/{clean}"


def load_exception_ledger(content: dict[str, Any]) -> None:
    if not EXCEPTION_LEDGER.exists():
        return
    data = read_json(EXCEPTION_LEDGER)
    entries = []
    for entry in data.get("entries", []):
        if not isinstance(entry, dict):
            continue
        copied = {k: entry.get(k) for k in ["id", "loop", "status", "failure", "workaround", "equations", "limit"]}
        copied["evidence"] = [
            {
                "label": str(item),
                "repo_path": round19_repo_path(str(item)),
                "href": repo_href(round19_repo_path(str(item))),
            }
            for item in entry.get("evidence", [])
            if item
        ]
        entries.append(copied)
    content["exception_ledger"] = {
        "schema": data.get("schema"),
        "purpose": data.get("purpose"),
        "entries": entries,
        "geometry": data.get("geometry", {}),
        "repo_path": "research/round19/exception-ledger.json",
        "href": repo_href("research/round19/exception-ledger.json"),
        "sha256": sha256(EXCEPTION_LEDGER),
    }
    attach_file_metadata(
        content,
        "exception-ledger",
        "Round19 exception ledger",
        "research/round19/exception-ledger.json",
        "limited",
        data.get("purpose") or "Records failed premises, workarounds, equations and review status.",
    )


def validate_hashes(files: Any) -> tuple[bool, list[str]]:
    if not isinstance(files, dict) or not files:
        return False, ["no source-hash file inventory"]
    problems: list[str] = []
    for rel, expected in files.items():
        if not isinstance(rel, str) or not isinstance(expected, str) or len(expected) != 64:
            problems.append(f"invalid hash record: {rel!r}")
            continue
        candidates = [ROUND / rel, ROOT / rel]
        path = next((candidate for candidate in candidates if candidate.exists()), None)
        if path is None:
            problems.append(f"missing file: {rel}")
            continue
        actual = sha256(path)
        if actual != expected:
            problems.append(f"hash mismatch: {rel}")
    return not problems, problems


def gate_inventory_requirements(files: Any, loop_id: str) -> tuple[bool, list[str]]:
    """Require a complete evidence shape before honoring an accepted gate."""
    if not isinstance(files, dict):
        return False, ["gate inventory is not an object"]
    lower = loop_id.lower()
    paths = [str(path).replace("\\", "/").lower() for path in files]

    def has(*needles: str, suffix: str | None = None) -> bool:
        for path in paths:
            if all(needle in path for needle in needles) and (suffix is None or path.endswith(suffix)):
                return True
        return False

    checks = {
        "contract": has("contract", lower),
        "forward source": has(f"forward/{lower}", suffix=".py"),
        "forward results": has(f"forward/{lower}", "output", suffix="results.json"),
        "forward report": has(f"forward/{lower}", suffix="report.md"),
        "backward source": has(f"backward/{lower}", suffix=".py"),
        "backward results": has(f"backward/{lower}", "output", suffix="results.json"),
        "backward report": has(f"backward/{lower}", suffix="report.md"),
        "backward comparison": has(f"backward/{lower}", "comparison", suffix="comparison.json"),
    }
    missing = [name for name, ok in checks.items() if not ok]
    return not missing, [f"missing required accepted-gate inventory item: {name}" for name in missing]


def summarize_remaining_open(value: Any) -> str | None:
    if isinstance(value, list):
        clean = [str(item) for item in value if item]
        return "Remaining open: " + "; ".join(clean) if clean else None
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def summarize_gate_result(value: Any) -> str | None:
    if isinstance(value, dict):
        preferred = [
            "accepted_gap",
            "spectral_statement",
            "mathematical_result",
            "operator",
            "perturbation_bound",
            "zero_mean",
        ]
        parts: list[str] = []
        for key in preferred:
            item = value.get(key)
            if item:
                label = key.replace("_", " ")
                parts.append(f"{label}: {item}")
        if not parts:
            parts = [f"{str(k).replace('_', ' ')}: {v}" for k, v in value.items() if v]
        return " ".join(parts) if parts else None
    if isinstance(value, list):
        clean = [str(item) for item in value if item]
        return "; ".join(clean) if clean else None
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def summarize_review(value: Any) -> str | None:
    if isinstance(value, dict):
        parts: list[str] = []
        for key, item in value.items():
            if item is None or item == "":
                continue
            label = str(key).replace("_", " ")
            if isinstance(item, bool):
                parts.append(f"{label}: {'yes' if item else 'no'}")
            else:
                parts.append(f"{label}: {item}")
        return "; ".join(parts) or None
    return summarize_gate_result(value)


def merge_advisor_files(content: dict[str, Any]) -> None:
    manifest = ADVISOR / "manifest.json"
    if manifest.exists():
        data = read_json(manifest)
        content.setdefault("meta", {})["advisor_manifest"] = {
            "schema": data.get("schema"),
            "repo_path": "research/round19/advisor/manifest.json",
            "sha256": sha256(manifest),
            "files": data.get("files", {}),
        }
        attach_file_metadata(
            content,
            "advisor-manifest",
            "Initial advisor file manifest",
            "research/round19/advisor/manifest.json",
            "accepted",
            "SHA-256 inventory for the initial Round19 advisor evidence files.",
        )

    initial_review = ADVISOR / "initial-review.md"
    if initial_review.exists():
        attach_file_metadata(
            content,
            "initial-review",
            "Round19 initial advisor review",
            "research/round19/advisor/initial-review.md",
            "accepted",
            "Freezes A1 and keeps later loops gated by evidence.",
        )

    contract = ADVISOR / "contract-a1.json"
    if contract.exists():
        data = read_json(contract)
        content.setdefault("meta", {})["starting_commit"] = data.get("starting_commit")
        content.setdefault("contracts", {})["A1"] = {
            "schema": data.get("schema"),
            "status": data.get("status"),
            "physical_contract": data.get("physical_contract"),
            "fixed_candidate_assignment": data.get("fixed_candidate_assignment"),
            "acceptance_tests": data.get("acceptance_tests", []),
            "falsifying_controls": data.get("falsifying_controls", []),
            "known_not_proved": data.get("known_not_proved", []),
        }
        attach_file_metadata(
            content,
            "contract-a1",
            "Frozen A1 contract",
            "research/round19/advisor/contract-a1.json",
            "accepted",
            "Advisor-frozen contract for the A1 boundary-consistency loop.",
        )

    contract_a2 = ADVISOR / "contract-a2.json"
    if contract_a2.exists():
        data = read_json(contract_a2)
        content.setdefault("contracts", {})["A2"] = {
            "schema": data.get("schema"),
            "status": data.get("status"),
            "goal": data.get("goal"),
            "physical_contract": data.get("physical_contract"),
            "acceptance_tests": data.get("acceptance_tests", []),
            "falsifying_controls": data.get("falsifying_controls", []),
            "open_after_success": data.get("open_after_success", []),
        }

    contract_b1 = ADVISOR / "contract-b1.json"
    if contract_b1.exists():
        data = read_json(contract_b1)
        content.setdefault("contracts", {})["B1"] = {
            "schema": data.get("schema"),
            "status": data.get("status"),
            "goal": data.get("goal"),
            "physical_contract": data.get("physical_contract"),
            "acceptance_tests": data.get("acceptance_tests", []),
            "falsifying_controls": data.get("falsifying_controls", []),
            "non_claims": data.get("non_claims", []),
            "stop_condition": data.get("stop_condition"),
            "target_statement": data.get("target_statement"),
        }

    for loop_id in ("B2", "C1", "C2"):
        lower = loop_id.lower()
        contract_path = ADVISOR / f"contract-{lower}.json"
        if contract_path.exists():
            data = read_json(contract_path)
            content.setdefault("contracts", {})[loop_id] = data
            attach_file_metadata(content, f"contract-{lower}", f"Frozen {loop_id} contract",
                                 f"research/round19/advisor/contract-{lower}.json", "accepted",
                                 data.get("goal") or f"Advisor-frozen {loop_id} execution contract.")

    boundary = ADVISOR / "boundary-classification.json"
    if boundary.exists():
        data = read_json(boundary)
        content.setdefault("partial_milestones", {})["boundary_classification"] = {
            "schema": data.get("schema"),
            "purpose": data.get("purpose"),
            "literal_assignment": data.get("literal_assignment"),
            "component_obligations": data.get("component_obligations", []),
            "sample_count": len(data.get("samples_n_2_to_12", [])),
        }
        attach_file_metadata(
            content,
            "boundary-classification",
            "Preliminary boundary classification",
            "research/round19/advisor/boundary-classification.json",
            "limited",
            "Advisor-side classifier for reachable clipped components; not a scientific gate.",
        )

    load_exception_ledger(content)

    optional_advisor = [
        ("a1-review", "A1 advisor review", "research/round19/advisor/a1-review.md", "limited", "Advisor feedback and equation/code review for A1; gate status is taken only from an advisor gate file."),
        ("a1-review-manifest", "A1 review manifest", "research/round19/advisor/a1-review-manifest.json", "limited", "SHA inventory for the in-progress A1 advisor review."),
        ("feedback-log", "Round19 advisor feedback log", "research/round19/advisor/feedback-log.md", "limited", "Preserves failed comparison history and current A1 blockers."),
        ("source-audit", "Prospective A2 source audit", "research/round19/advisor/source-audit.md", "limited", "Planning audit for A2 source applicability and limits."),
        ("source-audit-manifest", "Prospective A2 source-audit manifest", "research/round19/advisor/source-audit-manifest.json", "limited", "SHA inventory for the planning source audit."),
        ("a2-target-feasibility", "A2 target feasibility note", "research/round19/advisor/a2-target-feasibility.md", "limited", "Conditional target note for a product-representation A2 loop."),
        ("contract-a2", "Frozen A2 contract", "research/round19/advisor/contract-a2.json", "accepted", "Advisor-frozen contract for the direct product-representation A2 loop."),
        ("goal-a-advisor-manifest", "Goal A advisor manifest", "research/round19/advisor/goal-a-advisor-manifest.json", "accepted", "SHA inventory for A1 acceptance and A2 contract selection."),
        ("a2-applicability-review", "A2 applicability review", "research/round19/advisor/a2-applicability-review.md", "limited", "Earlier A2 applicability review preserved as pre-gate history."),
        ("a2-applicability-manifest", "A2 applicability manifest", "research/round19/advisor/a2-applicability-manifest.json", "limited", "Pre-gate A2 applicability inventory on the research branch."),
        ("a2-source-bound-inventory", "A2 source-bound inventory", "research/round19/advisor/a2-source-bound-inventory.json", "accepted", "Accepted A2 source-bound inventory for the final gate."),
        ("post-a-decision", "Post-Goal-A advisor decision", "research/round19/advisor/post-a-decision.json", "accepted", "Records narrow A1/A2 acceptance and advances to B1."),
        ("post-a-roadmap", "Post-Goal-A roadmap", "research/round19/advisor/post-a-roadmap.md", "accepted", "Explains why Goal A remains narrow and why B1 is frozen next."),
        ("provisional-bc-plan", "Provisional B/C plan", "research/round19/advisor/provisional-bc-plan.md", "limited", "Planning notes for later B/C branches."),
        ("contract-b1", "Frozen B1 contract", "research/round19/advisor/contract-b1.json", "accepted", "Advisor-frozen contract for the strict-cutoff two-cube B1 loop."),
    ]
    for key, title, repo_path, state, summary in optional_advisor:
        if (ROOT / repo_path).exists():
            attach_file_metadata(content, key, title, repo_path, state, summary)

    loops = {loop.get("id"): loop for loop in content.get("loops", []) if isinstance(loop, dict)}
    a1 = loops.get("A1")

    forward_results = ROUND / "forward" / "a1" / "output" / "results.json"
    if forward_results.exists():
        data = read_json(forward_results)
        content.setdefault("partial_milestones", {})["forward_a1"] = {
            "schema": data.get("schema"),
            "forward_result": data.get("forward_result"),
            "signed_case_count": data.get("signed_case_count"),
            "phase_fixture_count": data.get("phase_fixture_count"),
            "scale_register": data.get("scale_register"),
            "open_obligations": data.get("open_obligations", []),
        }
        attach_file_metadata(
            content,
            "forward-a1-results",
            "Canonical forward A1 results",
            "research/round19/forward/a1/output/results.json",
            "running",
            "Forward evidence currently reports clipped-component bounds and scale-register fields; it remains ungated.",
        )
        if a1:
            keys = a1.setdefault("evidence_keys", [])
            for key in ["a1-review", "forward-a1-results"]:
                if key not in keys:
                    keys.append(key)
            result = data.get("forward_result")
            if result:
                a1["result"] = f"Forward A1 evidence currently reports: {result}. No A1 advisor gate is accepted yet, and the advisor review still records blockers."

    forward_manifest = ROUND / "forward" / "a1" / "output" / "source-manifest.json"
    if forward_manifest.exists():
        attach_file_metadata(
            content,
            "forward-a1-source-manifest",
            "Forward A1 source manifest",
            "research/round19/forward/a1/output/source-manifest.json",
            "limited",
            "Source/output hashes are recorded; advisor review says source binding must be repaired before acceptance.",
        )
        if a1 and "forward-a1-source-manifest" not in a1.setdefault("evidence_keys", []):
            a1["evidence_keys"].append("forward-a1-source-manifest")

    backward_comparison = ROUND / "backward" / "a1" / "comparison" / "comparison.json"
    if backward_comparison.exists():
        data = read_json(backward_comparison)
        comparison_status = str(data.get("status") or "")
        add_or_update_evidence(
            content,
            {
                "key": "backward-a1-comparison",
                "title": "Backward A1 comparison",
                "state": "rejected" if "incomplete" in comparison_status or "reject" in comparison_status else "limited",
                "repo_path": "research/round19/backward/a1/comparison/comparison.json",
                "href": repo_href("research/round19/backward/a1/comparison/comparison.json"),
                "summary": data.get("accept_reject_conditions", {}).get("current_reject_reason") or "Independent comparison is recorded but does not accept A1.",
                "exists": True,
                "sha256": sha256(backward_comparison),
            },
        )
        content.setdefault("partial_milestones", {})["backward_a1_comparison"] = {
            "schema": data.get("schema"),
            "status": data.get("status"),
            "scope": data.get("scope"),
        }
        if a1 and "backward-a1-comparison" not in a1.setdefault("evidence_keys", []):
            a1["evidence_keys"].append("backward-a1-comparison")

    backward_manifest = ROUND / "backward" / "a1" / "manifest.json"
    if backward_manifest.exists():
        attach_file_metadata(
            content,
            "backward-a1-manifest",
            "Backward A1 manifest",
            "research/round19/backward/a1/manifest.json",
            "limited",
            "Independent backward preliminary manifest with producer rejection preserved.",
        )
        if a1 and "backward-a1-manifest" not in a1.setdefault("evidence_keys", []):
            a1["evidence_keys"].append("backward-a1-manifest")

    a2 = loops.get("A2")
    if a2:
        keys = a2.setdefault("evidence_keys", [])
        for key in ["source-audit", "source-audit-manifest", "a2-target-feasibility", "contract-a2", "goal-a-advisor-manifest", "a2-applicability-review", "a2-applicability-manifest", "a2-source-bound-inventory"]:
            if any(item.get("key") == key for item in content.get("evidence", [])) and key not in keys:
                keys.append(key)
        contract_a2_data = content.get("contracts", {}).get("A2")
        if contract_a2_data:
            a2["state"] = "running"
            a2["title"] = "Product-representation bridge"
            a2["pair"] = "Goal A · product representation"
            a2["scope"] = contract_a2_data.get("goal") or a2.get("scope")
            a2["result"] = "A2 has a frozen contract for a direct product-representation construction. It has no accepted scientific gate yet."
            a2["review"] = contract_a2_data.get("not_parent_goal_completion") or "A2 remains separate from homogeneous dense stability, finite-restriction convergence, continuum Yang-Mills, and Clay mass gap claims."
            remaining = summarize_remaining_open(contract_a2_data.get("open_after_success"))
            if remaining:
                a2["next"] = remaining
        elif (ADVISOR / "source-audit.md").exists():
            a2["review"] = "A prospective A2 source audit is present, but it is planning evidence only."

    b1 = loops.get("B1")
    if b1:
        keys = b1.setdefault("evidence_keys", [])
        for key in ["post-a-decision", "post-a-roadmap", "contract-b1", "provisional-bc-plan"]:
            if any(item.get("key") == key for item in content.get("evidence", [])) and key not in keys:
                keys.append(key)
        contract_b1_data = content.get("contracts", {}).get("B1")
        post_a = ADVISOR / "post-a-decision.json"
        if contract_b1_data:
            b1["state"] = "running"
            b1["title"] = "Strict-cutoff two-cube projector"
            b1["pair"] = "Goal B · strict cutoff and cross Gram"
            b1["scope"] = contract_b1_data.get("goal") or b1.get("scope")
            b1["result"] = "B1 is frozen and running under advisor/contract-b1.json. No B1 advisor gate is accepted yet."
            non_claims = summarize_gate_result(contract_b1_data.get("non_claims"))
            b1["review"] = non_claims or "B1 must enumerate the actual two-cube low-energy physical subspace and compute the exact cross Gram or return a limited gate."
            b1["next"] = contract_b1_data.get("stop_condition") or b1.get("next")
        if post_a.exists():
            decision = read_json(post_a)
            content.setdefault("partial_milestones", {})["post_a_decision"] = {
                "schema": decision.get("schema"),
                "status": decision.get("status"),
                "decision": decision.get("decision"),
                "goal_a_result": decision.get("goal_a_result"),
                "b_plan": decision.get("b_plan"),
                "c_plan": decision.get("c_plan"),
            }

    for loop_id in LOOP_IDS:
        lower = loop_id.lower()
        gate_path = ADVISOR / f"{lower}-gate.json"
        if not gate_path.exists():
            continue
        gate = read_json(gate_path)
        repo_path = f"research/round19/advisor/{lower}-gate.json"
        claimed_state = safe_state(gate.get("status"), "limited")
        inventory = gate.get("files") or gate.get("source_hashes")
        hashes_ok, hash_problems = validate_hashes(inventory)
        complete_ok, complete_problems = gate_inventory_requirements(inventory, loop_id)
        gate_problems = hash_problems + complete_problems
        state = claimed_state
        if claimed_state == "accepted" and gate_problems:
            state = "limited"
            gate = {
                **gate,
                "status": "limited",
                "claimed_status": claimed_state,
                "hash_validation_errors": hash_problems,
                "inventory_validation_errors": complete_problems,
            }
        summary = summarize_gate_result(gate.get("mathematical_result")) or summarize_gate_result(gate.get("result")) or summarize_gate_result(gate.get("summary")) or summarize_gate_result(gate.get("scope")) or f"Recorded advisor gate for {loop_id}."
        if claimed_state == "accepted" and state != "accepted":
            summary = "Gate claimed accepted, but source-hash replay or accepted-gate inventory validation failed; treated as limited until the evidence inventory is repaired."
        add_or_update_evidence(
            content,
            {
                "key": f"gate-{lower}",
                "title": f"{loop_id} advisor gate",
                "state": state,
                "repo_path": repo_path,
                "href": repo_href(repo_path),
                "summary": summary,
                "exists": True,
                "sha256": sha256(gate_path),
                "hashes_ok": hashes_ok,
                "inventory_complete": complete_ok,
                "hash_validation_errors": hash_problems,
                "inventory_validation_errors": complete_problems,
            },
        )
        loop = loops.get(loop_id)
        if loop:
            keys = loop.setdefault("evidence_keys", [])
            if f"gate-{lower}" not in keys:
                keys.append(f"gate-{lower}")
            loop["gate"] = gate
            loop["state"] = state
            if gate.get("scope"):
                loop["scope"] = gate["scope"]
            if claimed_state == "accepted" and state != "accepted":
                loop["result"] = summary
                loop["review"] = "; ".join(gate_problems) or "Accepted gate validation failed."
            else:
                gate_result = summarize_gate_result(gate.get("mathematical_result")) or summarize_gate_result(gate.get("result")) or summarize_gate_result(gate.get("summary"))
                if gate_result:
                    loop["result"] = gate_result
                elif state == "accepted":
                    loop["result"] = summary
                gate_review = summarize_review(gate.get("review")) or summarize_review(gate.get("advisor_review")) or summarize_review(gate.get("evidence_review")) or summarize_review(gate.get("evidence_classification"))
                if gate_review:
                    loop["review"] = gate_review
            remaining = summarize_remaining_open(gate.get("remaining_open") or gate.get("open_obligations") or gate.get("next"))
            if remaining:
                loop["next"] = remaining
        if state == "accepted":
            accepted_prefixes = (f"forward-{lower}", f"backward-{lower}", f"{lower}-source", f"{lower}-review")
            for item in content.get("evidence", []):
                key = str(item.get("key", ""))
                repo_path = str(item.get("repo_path", ""))
                if key.startswith(accepted_prefixes) or f"/forward/{lower}/" in repo_path or f"/backward/{lower}/" in repo_path:
                    if item.get("state") in {"running", "limited", "rejected"}:
                        item["state"] = "accepted"


def validate(content: dict[str, Any]) -> None:
    if content.get("schema") != "ym19-site-content-v1":
        raise SystemExit("site-content.json schema must be ym19-site-content-v1")
    loops = content.get("loops")
    if not isinstance(loops, list) or [loop.get("id") for loop in loops] != list(LOOP_IDS):
        raise SystemExit("loops must be ordered A1, A2, B1, B2, C1, C2")
    for loop in loops:
        loop["state"] = safe_state(loop.get("state"), "pending")
        if not str(loop.get("route", "")).startswith("paired-"):
            raise SystemExit(f"invalid route for {loop.get('id')}")
    for item in content.get("evidence", []):
        item["state"] = safe_state(item.get("state"), "pending")
        if item.get("repo_path") and not item.get("href"):
            item["href"] = repo_href(item["repo_path"])


def js_source(content: dict[str, Any]) -> str:
    payload = json.dumps(content, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return f"""/* Round19 paired research view. Generated by research/round19/build_site.py. */
(() => {{
 'use strict';
 const old=window.ResearchObservatory,H=window.ResearchHub;
 if(!old||!H)return;
 const EMBED={payload};
 const D=window.OBSERVATORY_PAIRED&&typeof window.OBSERVATORY_PAIRED==='object'?window.OBSERVATORY_PAIRED:EMBED;
 window.OBSERVATORY_PAIRED=D;
 const esc=H.escape||((v)=>String(v??'').replace(/[&<>\"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#39;'}}[c])));
 const safe=(value)=>{{const s=String(value??'');if(/^(?:[.][.]\\/|[.]\\/|\\/)?[a-zA-Z0-9][a-zA-Z0-9._/#?=&%+/\\-]*$/.test(s)&&!s.includes('..//'))return esc(s);try{{const u=new URL(s);return u.protocol==='https:'&&!u.username&&!u.password&&!s.includes(String.fromCharCode(92))?esc(u.href):'#';}}catch{{return '#';}}}};
 const states=new Set(['pending','running','accepted','limited','rejected']);
 const list=(x)=>Array.isArray(x)?x.filter(v=>v!==null&&v!==undefined):[];
 const state=(x)=>states.has(String(x||'').toLowerCase())?String(x).toLowerCase():'pending';
 const pages={{home:'Round19 home','paired-a1':'A1 · Boundary clusters','paired-a2':'A2 · Representation bridge','paired-b1':'B1 · Projector inventory','paired-b2':'B2 · Finite spectral bound','paired-c1':'C1 · Integrated cluster','paired-c2':'C2 · Certified static integral','paired-roadmap':'Paired roadmap','paired-review':'Evidence review'}};
 const a=(r,t)=>`<a href="#research/${{esc(r)}}">${{esc(t)}}</a>`;
 const badge=(s)=>`<span class="paired-badge ${{esc(state(s))}}">${{esc(state(s))}}</span>`;
 const eq=(xs)=>`<div class="paired-eq" aria-label="Mathematical statement">${{list(xs).map(x=>`<div>${{esc(x)}}</div>`).join('')}}</div>`;
 const panel=(title,body,cls='')=>`<section class="hub-panel paired-panel ${{esc(cls)}}"><h2>${{esc(title)}}</h2>${{body}}</section>`;
 const table=(heads,rows)=>`<div class="hub-table-wrap"><table class="hub-table paired-table"><thead><tr>${{heads.map(h=>`<th scope="col">${{esc(h)}}</th>`).join('')}}</tr></thead><tbody>${{rows.map(r=>`<tr>${{r.map(c=>`<td>${{c}}</td>`).join('')}}</tr>`).join('')}}</tbody></table></div>`;
 const title=(main,deck)=>`<header class="hub-header paired-header"><p class="hub-kicker">${{esc(D.meta?.kicker||'Yang–Mills Workbench · Round19')}}</p><h1>${{esc(main)}}</h1><p class="hub-deck">${{esc(deck||D.meta?.summary||'')}}</p></header>`;
 const routeLoop=(route)=>list(D.loops).find(loop=>loop&&loop.route===route);
 const evidenceMap=()=>new Map(list(D.evidence).map(item=>[item.key,item]));
 const evLink=(item)=>item?`<a href="${{safe(item.href||item.repo_path)}}" target="_blank" rel="noopener noreferrer">${{esc(item.repo_path||item.title)}}</a>`:'—';
 const statusText=()=>{{const accepted=list(D.loops).filter(loop=>state(loop.state)==='accepted').length;return `${{accepted}} accepted loop gate${{accepted===1?'':'s'}} recorded; current Round19 state: ${{state(D.meta?.status)}}.`;}};
 function loopRows(){{return list(D.loops).map(loop=>[`<strong>${{esc(loop.id)}}</strong><br>${{badge(loop.state)}}`,`${{a(loop.route,loop.title)}}<p>${{esc(loop.pair)}}</p>`,`<p><span class="paired-forward">Forward:</span> ${{esc(loop.forward_title)}}</p><p><span class="paired-reverse">Reverse:</span> ${{esc(loop.reverse_title)}}</p>`,esc(loop.next)]);}}
 function spiral(){{
  const loops=list(D.loops),cx=520,cy=360,phi=(1+Math.sqrt(5))/2;
  const cardPos=[{{x:56,y:46}},{{x:714,y:46}},{{x:42,y:314}},{{x:728,y:314}},{{x:56,y:586}},{{x:714,y:586}}];
  const labels={{A1:['Boundary-consistent','local clusters'],A2:['Product-representation','bridge'],B1:['Projector','inventory'],B2:['Finite spectral','bound'],C1:['Integrated-cluster','discriminator'],C2:['Certified static','integral']}};
  const cardSub=(id)=>id==='C1'||id==='C2'?'Static κ; physical matching open':'E★ and common α scale.';
  const position=(u,side)=>{{const theta=-2.95+.86*u;const r=100*Math.pow(phi,(theta+2.95)/(Math.PI/2));const t=side==='forward'?theta:Math.PI-theta;return {{x:cx+Math.cos(t)*r,y:cy+Math.sin(t)*r}};}};
  const curve=(side)=>{{const pts=[];for(let k=0;k<150;k++){{const u=k/149*5.05;const p=position(u,side);pts.push([p.x,p.y]);}}return pts.map((p,i)=>(i?'L':'M')+p.map(v=>v.toFixed(1)).join(' ')).join(' ');}};
  const pairs=loops.map((loop,i)=>{{const f=position(i,'forward'),r=position(i,'reverse'),card=cardPos[i]||{{x:60,y:60+i*110}};return {{loop,i,f,r,card}};}});
  const pairLines=pairs.map(p=>`<line class="paired-scale" x1="${{p.f.x.toFixed(1)}}" y1="${{p.f.y.toFixed(1)}}" x2="${{p.r.x.toFixed(1)}}" y2="${{p.r.y.toFixed(1)}}"/>`).join('');
  const leaders=pairs.map(p=>{{const mx=(p.f.x+p.r.x)/2,my=(p.f.y+p.r.y)/2,tx=p.card.x+(p.card.x<cx?270:0),ty=p.card.y+59;return `<path class="paired-leader" d="M${{mx.toFixed(1)}} ${{my.toFixed(1)}} L${{tx.toFixed(1)}} ${{ty.toFixed(1)}}"/>`;}}).join('');
  const nodes=pairs.map(p=>`<a class="paired-node-link" href="#research/${{esc(p.loop.route)}}" aria-label="Open ${{esc(p.loop.id)}} paired loop"><g class="paired-node ${{esc(state(p.loop.state))}}"><circle class="forward" cx="${{p.f.x.toFixed(1)}}" cy="${{p.f.y.toFixed(1)}}" r="18"><title>${{esc(p.loop.id)}} forward derivation: ${{esc(p.loop.forward_title)}}</title></circle><text class="paired-node-id" x="${{p.f.x.toFixed(1)}}" y="${{(p.f.y+1).toFixed(1)}}">${{esc(p.loop.id)}}</text><circle class="reverse" cx="${{p.r.x.toFixed(1)}}" cy="${{p.r.y.toFixed(1)}}" r="18"><title>${{esc(p.loop.id)}} reverse reconstruction: ${{esc(p.loop.reverse_title)}}</title></circle><text class="paired-node-id" x="${{p.r.x.toFixed(1)}}" y="${{(p.r.y+1).toFixed(1)}}">${{esc(p.loop.id)}}</text></g></a>`).join('');
  const cards=pairs.map(p=>{{const lines=labels[p.loop.id]||[String(p.loop.title||p.loop.id).slice(0,24),String(p.loop.pair||'paired loop').slice(0,24)];return `<a class="paired-card-link" href="#research/${{esc(p.loop.route)}}" aria-label="Open ${{esc(p.loop.id)}}: ${{esc(p.loop.title)}}"><g class="paired-card ${{esc(state(p.loop.state))}}" transform="translate(${{p.card.x}} ${{p.card.y}})"><rect width="270" height="124" rx="18"/><circle class="forward" cx="26" cy="28" r="8"/><circle class="reverse" cx="48" cy="28" r="8"/><text class="paired-card-id" x="70" y="29">${{esc(p.loop.id)}} · ${{esc(state(p.loop.state))}}</text><text class="paired-card-title" x="20" y="56"><tspan x="20" dy="0">${{esc(lines[0])}}</tspan><tspan x="20" dy="22">${{esc(lines[1]||'')}}</tspan></text><text class="paired-card-line" x="20" y="104">${{esc(cardSub(p.loop.id))}}</text></g></a>`;}}).join('');
  const fallback=`<div class="paired-spiral-fallback"><p>Text fallback: A and B spectral nodes track E★ and common α. C nodes are static κ integrals with physical matching open.</p><ol>${{pairs.map(p=>`<li><strong>${{esc(p.loop.id)}}:</strong> ${{esc(p.loop.forward_title)}} / ${{esc(p.loop.reverse_title)}} State: ${{esc(state(p.loop.state))}}.</li>`).join('')}}</ol></div>`;
  return `<figure class="paired-spiral"><svg viewBox="0 0 1040 760" role="img" aria-labelledby="paired-spiral-title paired-spiral-desc"><title id="paired-spiral-title">Round19 paired expansion and reverse reconstruction nodes</title><desc id="paired-spiral-desc">Approximate opposing golden logarithmic spirals, not exact Fibonacci arcs. The formula organizes paired research nodes only; no Round19 physical test of the geometry is recorded. A and B use spectral scale checkpoints; C marks static κ with physical matching still open.</desc><rect class="paired-sky" width="1040" height="760" rx="30"/><path class="paired-path forward" d="${{curve('forward')}}"/><path class="paired-path reverse" d="${{curve('reverse')}}"/>${{pairLines}}${{leaders}}<circle class="paired-center" cx="${{cx}}" cy="${{cy}}" r="48"/><text class="paired-center-label" x="${{cx}}" y="${{cy-7}}">E★ &gt; 0</text><text class="paired-center-sub" x="${{cx}}" y="${{cy+17}}">spectral checkpoint</text>${{nodes}}${{cards}}</svg><figcaption>${{esc(D.geometry_hypothesis?.limit)}}</figcaption>${{fallback}}</figure>`;
 }}
 function evidenceRows(keys){{const by=evidenceMap();return list(keys).map(k=>by.get(k)).filter(Boolean).map(item=>[badge(item.state),esc(item.title),esc(item.summary),evLink(item)]);}}
 const ledgerState=(status)=>{{const s=String(status||'').toLowerCase();if(s.includes('accepted')||s.includes('corrected'))return 'accepted';if(s.includes('pending')||s.includes('investigation')||s.includes('review'))return 'running';if(s.includes('reject')||s.includes('failed'))return 'rejected';return 'limited';}};
 const ledgerLinks=(entry)=>list(entry.evidence).map(item=>`<a href="${{safe(item.href)}}" target="_blank" rel="noopener noreferrer">${{esc(item.label)}}</a>`).join('<br>')||'—';
 const ledgerFormulae=(entry)=>{{const equations=entry&&entry.equations&&typeof entry.equations==='object'?entry.equations:{{}};const rows=Object.entries(equations).map(([k,v])=>`<tr><th scope="row">${{esc(k.replaceAll('_',' '))}}</th><td><code class="paired-formula">${{esc(v)}}</code></td></tr>`).join('');return rows?`<table class="paired-formula-table"><tbody>${{rows}}</tbody></table>`:'<p>No formula recorded.</p>';}};
 function exceptionLedger(){{const L=D.exception_ledger;if(!L||!Array.isArray(L.entries)||!L.entries.length)return '';const rows=L.entries.map(entry=>[`${{badge(ledgerState(entry.status))}}<br><strong>${{esc(entry.loop||'—')}}</strong><br><span class="paired-ledger-status">${{esc(entry.status)}}</span>`,`<strong>${{esc(entry.id)}}</strong><p>${{esc(entry.failure)}}</p>`,`<p>${{esc(entry.workaround)}}</p>${{ledgerFormulae(entry)}}`,`<p>${{esc(entry.limit)}}</p>${{ledgerLinks(entry)}}`]);const geom=L.geometry&&typeof L.geometry==='object'?`<p class="paired-ledger-note">Geometry role: ${{esc(L.geometry.role||'organizing aid')}}. Physical hypothesis: ${{esc(L.geometry.physical_hypothesis||'untested')}}. ${{esc(L.geometry.admission_rule||'')}}</p>`:'';return panel('Exception ledger',`<p>${{esc(L.purpose||'Failed premises, workarounds, equations and evidence status are recorded here.')}}</p>${{geom}}${{table(['Status and scope','Failed premise','Workaround and equations','Limit and evidence'],rows)}}<p><a href="${{safe(L.href)}}" target="_blank" rel="noopener noreferrer">Open exception-ledger.json</a></p>`);}}
 function home(){{return title(D.meta?.title||'Round19 paired research',D.meta?.summary)+panel('Branch-only publication state',`<p>This Round19 view is prepared on the research branch for review. It does not claim a live Round19 GitHub Pages URL.</p><p><a href="${{safe(D.meta?.repository)}}" target="_blank" rel="noopener noreferrer">Open research/round19-paired branch</a></p>`)+panel(D.geometry_hypothesis?.title||'Paired expansion model',`<p>${{esc(D.geometry_hypothesis?.claim)}}</p>${{spiral()}}`,'paired-hero')+panel('Six paired loop nodes',table(['Loop','Question','Paired expansion nodes','Next gate'],loopRows()))+panel('Common physical scale',table(['Symbol','State','Meaning','Current record'],list(D.unit_contract).map(u=>[esc(u.symbol),badge(u.state),esc(u.meaning),esc(u.record)])))+panel('Current evidence state',`<p>${{esc(statusText())}}</p>`+table(['State','Artifact','Scope','Evidence link'],evidenceRows(list(D.evidence).map(x=>x.key))))+panel('History',`${{a('review18-home','Round18 six-loop snapshot')}} · ${{a('review17-home','Earlier Round17 snapshot')}}`);}}
 function loopPage(route){{const loop=routeLoop(route);if(!loop)return old.render(route);return title(`${{loop.id}} · ${{loop.title}}`,loop.pair)+panel('Scope',`<p>${{esc(loop.scope)}}</p>${{eq(loop.math)}}`)+panel('Results',`<p>${{esc(loop.result)}}</p>`)+panel('Review',`<p>${{esc(loop.review)}}</p>`+(evidenceRows(loop.evidence_keys).length?table(['State','Artifact','Scope','Evidence link'],evidenceRows(loop.evidence_keys)):''))+panel('Next',`<p>${{esc(loop.next)}}</p>`);}}
 function roadmap(){{return title('Paired roadmap at one physical scale','Each loop is a gate with its own evidence record. Later contracts remain provisional until the prior evidence chooses them.')+panel('Forward and reverse expansion sequence',spiral(),'paired-hero')+panel('Route contract',table(['Loop','State','Forward derivation','Reverse reconstruction'],list(D.loops).map(loop=>[`${{a(loop.route,loop.id)}}<br>${{badge(loop.state)}}`,esc(loop.pair),esc(loop.forward_title),esc(loop.reverse_title)])))+panel('Next actions',table(['State','Action'],list(D.next_steps).map(x=>[badge(x.state),esc(x.item)])));}}
 function review(){{const limits=list(D.review?.limits),contracts=D.contracts&&typeof D.contracts==='object'?D.contracts:{{}};const contractRows=Object.entries(contracts).map(([id,c])=>[esc(id),badge(c.status==='frozen'||String(c.status||'').startsWith('frozen')?'running':c.status),esc(c.goal||c.schema||'Recorded contract'),String(list(c.acceptance_tests).length),String(list(c.falsifying_controls).length)]);const gateKeys=list(D.evidence).filter(x=>/^gate-/.test(x.key||'')).map(x=>x.key);return title('Evidence review and limits',D.review?.summary||'Round19 evidence is still being gathered.')+panel('Recorded evidence',table(['State','Artifact','Scope','Evidence link'],evidenceRows(list(D.evidence).map(x=>x.key))))+panel('Advisor gates',gateKeys.length?table(['State','Gate','Scope','Evidence link'],evidenceRows(gateKeys)):'<p>No advisor gates are recorded.</p>')+panel('Frozen contracts and controls',contractRows.length?table(['Loop','Contract state','Goal or schema','Acceptance tests','Falsifying controls'],contractRows):'<p>No contracts are available.</p>')+exceptionLedger()+panel('Limits',`<ul>${{limits.map(x=>`<li>${{esc(x)}}</li>`).join('')}}</ul>`);}}
 function render(route='home'){{if(route==='review18-home')return `<div class="research-shell hub m8 paired19"><p class="hub-limit">Historical Round18 snapshot. ${{a('home','Current Round19 paired view')}}</p>${{old.render('home')}}</div>`;if(!Object.hasOwn(pages,route))return old.render(route);const body=route==='home'?home():route==='paired-roadmap'?roadmap():route==='paired-review'?review():loopPage(route);return `<div class="research-shell hub m8 paired19"><nav class="hub-nav paired-nav" aria-label="Round19 paired research navigation">${{Object.entries(pages).map(([r,t])=>`<a href="#research/${{r}}" ${{r===route?'aria-current="page"':''}}>${{esc(t)}}</a>`).join('')}}</nav>${{body}}<footer class="hub-foot paired-foot">${{a('review18-home','Round18 history')}} · ${{a('paired-review','Round19 evidence review')}} · <a href="${{safe(D.meta?.repository)}}" target="_blank" rel="noopener noreferrer">Open repository</a></footer></div>`;}}
 function afterRender(){{const r=(location.hash.split('/')[1]||'home');if(Object.hasOwn(pages,r)||r==='review18-home')document.title=(pages[r]||'Round18 history')+' · Yang–Mills Workbench';else old.afterRender();}}
 window.ResearchPaired={{render,spiral,data:D}};
 window.ResearchObservatory={{...old,render,afterRender}};
}})();
"""


def html_escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def script_escape(value: str) -> str:
    return value.replace("</script", "<\\/script")


def overview_html(content: dict[str, Any], paired_js: str) -> str:
    paired_css = (DIST / "research-paired.css").read_text(encoding="utf-8") if (DIST / "research-paired.css").exists() else ""
    branch_url = f"{REPO}/tree/{RESEARCH_BRANCH}"
    title_text = html_escape(content.get("meta", {}).get("title") or "Round19 paired research")
    base_css = """
:root{color-scheme:light;--paper:#fff;--line:#d7dfe8;--muted:#51687a}*{box-sizing:border-box}body{margin:0;background:#071526;color:#12263a;font:16px/1.55 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}a{color:#1d5f82}a:focus{outline:3px solid #f1ae47;outline-offset:3px}.standalone-top{background:#06111f;color:#dcecf8;border-bottom:1px solid rgba(177,213,235,.22);padding:18px clamp(16px,4vw,42px)}.standalone-top h1{margin:.25rem 0;font:clamp(1.7rem,3vw,2.6rem)/1.1 Georgia,serif;color:#fff}.standalone-top p{max-width:950px;margin:.35rem 0;color:#c5d8e7}.branch-note{display:inline-block;margin:.35rem 0 .65rem;padding:7px 11px;border:1px solid rgba(241,174,71,.55);border-radius:999px;background:rgba(241,174,71,.12);color:#ffe0a3;font-size:.9rem}.branch-note a{color:#fff0c9}.standalone-main{padding:24px clamp(12px,3vw,36px) 44px}.hub-header h1{font:clamp(2.1rem,4vw,3.7rem)/1.05 Georgia,serif;margin:.2rem 0 .75rem}.hub-kicker{margin:0 0 .35rem;text-transform:uppercase;letter-spacing:.08em;font-size:.78rem;font-weight:800}.hub-deck{font-size:1.05rem;max-width:980px}.hub-nav{display:flex;gap:4px;flex-wrap:wrap;margin:0 0 18px}.hub-nav a{padding:9px 12px;border:1px solid rgba(177,213,235,.28);text-decoration:none;border-radius:999px}.hub-table-wrap{overflow:auto}.hub-table{border-collapse:collapse;width:100%;min-width:720px}.hub-table th,.hub-table td{border-bottom:1px solid var(--line);padding:11px 12px;text-align:left;vertical-align:top}.hub-table th{font-size:.82rem;text-transform:uppercase;letter-spacing:.05em;color:#40566a}.hub-panel{border-radius:22px}.hub-limit{border-radius:14px}.history-fallback ul{margin-top:.4rem}.history-fallback li{margin:.25rem 0}.history-fallback a{color:#ffe0a3}.noscript{margin:18px clamp(16px,4vw,42px);padding:12px 14px;background:#fff8e9;border-left:4px solid #f1ae47}
"""
    fallback_js = f"""
window.ResearchHub={{
 escape(value){{return String(value??'').replace(/[&<>\"']/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','\"':'&quot;',"'":'&#39;'}}[c]));}},
 safeURL(value){{try{{const u=new URL(String(value??''), location.href);return u.protocol==='https:'?u.href:'#';}}catch{{return '#';}}}}
}};
window.ResearchObservatory={{
 render(route='home'){{
  const live='https://occult-kranti.github.io/yang_mills_workbench/#research/';
  const links=['home','next-bridge','next-summable','next-complement','next-spectrum','next-gram','next-two-link','next-team','next-review'];
  const e=window.ResearchHub.escape;
  const list=links.map(r=>`<li><a href="${{live}}${{r}}" target="_blank" rel="noopener noreferrer">Round18 ${{e(r)}}</a></li>`).join('');
  return `<section class="hub-panel paired-panel history-fallback"><h2>Historical research route</h2><p>This standalone branch artifact does not embed the legacy megabyte research bundles. Open the existing live Round18 route instead.</p><ul>${{list}}</ul></section>`;
 }},
 afterRender(){{}}
}};
"""
    router_js = """
(() => {
 const main=document.getElementById('main');
 function route(){
  const hash=location.hash.replace(/^#/, '');
  const parts=hash.split('/').filter(Boolean);
  if(parts[0]==='research') return parts[1] || 'home';
  return parts[0] || 'home';
 }
 function render(){
  const r=route();
  main.innerHTML=window.ResearchObservatory.render(r);
  window.ResearchObservatory.afterRender();
  const current=main.querySelector('.paired-nav a[aria-current="page"]');
  if(current) current.scrollIntoView({block:'nearest',inline:'nearest'});
 }
 window.addEventListener('hashchange', render);
 render();
})();
"""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Standalone branch artifact for Round19 paired Yang-Mills research routes.">
<title>{title_text} · Branch artifact</title>
<style>{base_css}\n{paired_css}</style>
</head>
<body>
<header class="standalone-top">
<span class="branch-note">Branch-only review artifact · not published on GitHub Pages · <a href="{branch_url}" target="_blank" rel="noopener noreferrer">research/round19-paired</a></span>
<h1>{title_text}</h1>
<p>This self-contained HTML file is generated from the Round19 branch model so the new routes can be inspected before any main-branch or Pages merge. It does not claim a live Round19 publication URL.</p>
</header>
<noscript><p class="noscript">JavaScript is required to switch among the embedded Round19 routes in this standalone artifact.</p></noscript>
<main id="main" class="standalone-main" tabindex="-1"></main>
<script>{script_escape(fallback_js)}</script>
<script>{script_escape(paired_js)}</script>
<script>{script_escape(router_js)}</script>
</body>
</html>
"""


def main() -> None:
    content = read_json(CONTENT)
    merge_advisor_files(content)
    validate(content)
    DIST.mkdir(parents=True, exist_ok=True)
    paired_js = js_source(content)
    OUTPUT.write_text(paired_js, encoding="utf-8")
    OVERVIEW.write_text(overview_html(content, paired_js), encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)} and {OVERVIEW.relative_to(ROOT)} with {len(content.get('loops', []))} loop routes and {len(content.get('evidence', []))} evidence records")


if __name__ == "__main__":
    main()
