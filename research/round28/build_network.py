#!/usr/bin/env python3
"""Build the additive evidence graph from reviewed gates and reading records."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "research/round28"


def read(path, default=None):
    return json.loads(path.read_text()) if path.is_file() else default


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(require_complete=False):
    inherited = read(ROOT / "research/round27/network.json")
    graph = json.loads(json.dumps(inherited))
    nodes, edges = graph["nodes"], graph["edges"]
    ids = {node["id"] for node in nodes}
    aliases = read(BASE / "advisor/network-aliases.json")["aliases"]
    summaries = read(BASE / "advisor/summaries.json", {})
    selected = read(BASE / "advisor/sequence.json")["loops"]
    completed = read(BASE / "advisor/progress.json")["completed_loops"]
    require(completed == selected[:len(completed)], "completed order is not a selected prefix")
    if require_complete:
        require(len(completed) == 10, "ten reviews required for final graph")

    def node(item):
        require(item["id"] not in ids, "duplicate node " + item["id"])
        ids.add(item["id"])
        nodes.append(item)

    def edge(source, target, kind, label):
        require(source in ids and target in ids, "unknown graph endpoint: " + source + " -> " + target)
        item = {"from": source, "to": target, "type": kind, "label": label}
        if item not in edges:
            edges.append(item)

    node({"id": "r28-methods", "title": "Round28 source, mechanism and skeptical review",
          "kind": "premise", "status": "methodological",
          "summary": "Modern model-agent perspectives motivate explicit questions and controls; evidence and proofs determine scientific admission.",
          "detail": "Historical names denote methodological lenses. Source reading, independent implementations, skeptical review and physical observations are distinct. Literature edges express review influence or a proposed transfer, never an unexplained physical premise.",
          "sources": ["research/round28/methods/prospective-guide.md", "research/round28/experts/source-survey.md"],
          "route": "round28-sources"})

    survey = read(BASE / "experts/sources.json")
    supplement = read(BASE / "experts/source-supplement.json", {})
    reading_records = []
    for ledger in (survey, supplement):
        for binding in ledger.get("input_bindings", []):
            require(digest(ROOT / binding["path"]) == binding["sha256"], "changed survey source")
        reading_records.extend(ledger.get("reading_records", []))
    require(len({item["record_id"] for item in reading_records}) == len(reading_records),
            "duplicate attributed reading record")
    for item in reading_records:
        record = item["original_record"]
        title = record.get("title") or record.get("claim_used") or item["recorded_urls"][0]
        use = next((record[key] for key in ("application", "application_status", "admitted_use", "proposed_use", "workbench_inference", "record_vs_interpretation", "claim_used", "explicit_scope_observation") if record.get(key)), "See the attributed reading ledger for scope.")
        if not isinstance(use, str):
            use = json.dumps(use, ensure_ascii=False)
        source_id = "r28-source-" + item["record_id"].lower()
        node({"id": source_id, "title": title, "kind": "literature", "status": "source-reviewed",
              "summary": use,
              "detail": "Category: " + item["category"] + ". Lens: " + item["lens"] + ".\nReading depth: " + item["reading_depth"] + "\nChange: " + item["change_status"] + ". " + item["change_status_basis"] + "\nThis reading record is not an admitted physical theorem premise.",
              "sources": item["recorded_urls"] + [item["source_ledger"]], "route": "round28-sources"})
        edge(source_id, "r28-methods", "review-selection", "Attributed source review; scope and controls only")

    for loop in completed:
        gate_path = BASE / f"advisor/{loop}-gate.json"
        gate = read(gate_path)
        require(gate and gate.get("accepted"), "missing reviewed gate")
        for path, expected in gate["bindings"].items():
            require(digest(ROOT / path) == expected, "changed gate binding: " + path)
        summary = summaries.get(loop)
        require(summary is not None, "missing reviewed presentation: " + loop)
        loop_id = "r28-" + loop
        sources = [f"research/round28/{side}/{loop}/report.md" for side in ("forward", "reverse")]
        sources += [f"research/round28/skeptic/{loop}.md", f"research/round28/advisor/{loop}-gate.json"]
        node({"id": loop_id, "title": loop.upper() + " · " + summary["title"], "kind": "loop", "status": "limited",
              "summary": gate["accepted"], "detail": "\n".join(gate["limitations"]), "sources": sources,
              "route": "round28-" + loop, "model": gate["model"]})
        edge("r28-methods", loop_id, "review-selection", "Contract, independent derivations and skeptical gate")
        for context in summary.get("context_dependencies", []):
            context_id = aliases.get(context["id"], context["id"])
            require(context_id in ids, "unknown review context " + context_id)
            require(isinstance(context.get("reason"), str) and context["reason"].strip(),
                    "review context needs its specific role")
            edge(context_id, loop_id, "review-selection", context["reason"])
        for influence in summary.get("reading_influences", []):
            source_id = "r28-source-" + influence["record_id"].lower()
            require(source_id in ids, "unknown reading influence " + source_id)
            require(isinstance(influence.get("reason"), str) and influence["reason"].strip(),
                    "reading influence needs its specific methodological role")
            edge(source_id, loop_id, "review-selection", influence["reason"])
        for dependency in gate.get("network_dependencies", []):
            dependency = aliases.get(dependency, dependency)
            if dependency not in ids and "r28-" + dependency in ids:
                dependency = "r28-" + dependency
            dependency_node = next((old for old in nodes if old["id"] == dependency), None)
            require(dependency_node is not None, "unresolved dependency " + dependency)
            kind = "review-selection" if dependency_node["kind"] == "open" else "proven-dependency"
            edge(dependency, loop_id, kind, "Reviewed model premise" if kind == "proven-dependency" else "Previously planned question executed within stated scope")
        for index, equation in enumerate(summary.get("equations", []), 1):
            equation_id = loop_id + "-eq" + str(index)
            node({"id": equation_id, "title": equation["label"], "kind": "equation", "status": "proved-in-model",
                  "summary": equation["expression"], "equation": equation["expression"],
                  "detail": equation.get("scope", "Use the exact model and limitations of the reviewed loop. Scientific priority is unverified."),
                  "sources": sources, "route": "round28-" + loop})
            edge(loop_id, equation_id, "proven-dependency", "Equation within the admitted model and scope")

    roadmap = read(BASE / "advisor/roadmap.json", {})
    for item in roadmap.get("next_goals", []):
        next_id = "r28-next-" + item["id"].lower()
        node({"id": next_id, "title": item["id"] + " · " + item["title"], "kind": "open", "status": "planned",
              "summary": item["target"], "detail": "Planned after the ten-loop review; no additional investigation executed.",
              "sources": ["research/round28/advisor/roadmap.json"], "route": "round28-roadmap"})
        for dependency in item.get("dependencies", []):
            edge(dependency, next_id, "proposed-transfer", "Next unproved research target")

    require(nodes[:len(inherited["nodes"])] == inherited["nodes"], "changed inherited graph nodes")
    require(edges[:len(inherited["edges"])] == inherited["edges"], "changed inherited graph edges")
    output = BASE / "network.json"
    output.write_text(json.dumps(graph, indent=2, ensure_ascii=False) + "\n")
    return {"nodes": len(nodes), "edges": len(edges), "reviewed_loops": completed,
            "reading_nodes": len(reading_records), "sha256": digest(output)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    print(json.dumps(build(args.require_complete), sort_keys=True))
