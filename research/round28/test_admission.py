"""Coherent admission attacks against a synthetic portable research fixture.

The fixture has no physical claim. Every attack rebinds current output, freeze,
review and gate hashes, so semantic rejection does not depend on stale digests.
"""
import argparse
import copy
import json
from pathlib import Path
import shutil
import tempfile

from reproduce import BASE, PREFIX, Validator, digest, operand, projection, replay_artifacts, require, semantics


def put(root, name, data):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n" if isinstance(data, (dict, list)) else data)


def fixture(root):
    put(root, "AGENTS.md", "Synthetic frozen instructions.\n")
    put(root, PREFIX + "methods/prospective-guide.md", "Synthetic instructions only.\n")
    cycle = {"schema": "ym28-cycle-v1", "baseline_commit": BASE, "requested_goals": 5,
             "loops_per_goal": 2, "target_new_research_loops": 10,
             "initial_goal_order": [{"goal": goal, "first_loop": pair[0], "second_loop_label": pair[1]}
                                    for goal, pair in [("AG", ["ag2", "ag3"]), ("AI", ["ai3", "ai4"]), ("AH", ["ah1", "ah2"])]],
             "sources": {"AGENTS.md": digest(root / "AGENTS.md")}}
    put(root, PREFIX + "advisor/cycle.json", cycle)
    put(root, PREFIX + "advisor/sequence.json", {"loops": ["ag2"], "target_loops": 10})
    put(root, PREFIX + "advisor/progress.json", {"requested_goals": 5, "target_loops": 10, "completed_loops": ["ag2"], "active_loop": None})
    put(root, PREFIX + "advisor/goal-pairs.json", {"initial_goals": [{"id": x["goal"], "loops": [x["first_loop"], x["second_loop_label"]]} for x in cycle["initial_goal_order"]], "later_goals": []})
    contract_name = PREFIX + "contracts/ag2.json"
    contract = {"schema": "ym28-contract-v1", "loop": "ag2", "sequence": 1, "goal": "AG", "goal_loop": 1,
                "model": "synthetic admission fixture", "frozen_at": "2026-01-01T00:00:00Z", "requirements": ["Retain tested control"],
                "parameters": {"x": "rational fixture"}, "acceptance": "No physical claim",
                "sources": {name: digest(root / name) for name in ["AGENTS.md", PREFIX + "methods/prospective-guide.md", PREFIX + "advisor/cycle.json"]}}
    put(root, contract_name, contract)
    spec = {"schema": "ym28-admission-v1", "loop": "ag2", "bindings": {contract_name: digest(root / contract_name)}, "producers": {}, "skeptic_checkers": []}
    all_bindings = {contract_name: digest(root / contract_name)}
    for side in ["forward", "reverse"]:
        base = PREFIX + f"{side}/ag2/"
        inventory = {**contract["sources"], contract_name: digest(root / contract_name)}
        snapshots = {}
        for origin, expected in inventory.items():
            snapshot = base + "inputs/" + origin
            put(root, snapshot, (root / origin).read_text())
            snapshots[snapshot] = expected
        manifest = base + "inputs/source-inventory.json"
        put(root, manifest, inventory)
        put(root, base + "check.py", "# synthetic fixture; never executed\n")
        put(root, base + "report.md", "No scientific finding.\n")
        bindings = {**inventory, **{name: digest(root / name) for name in [manifest, base + "check.py", base + "report.md"]}}
        result = {"schema": "synthetic-only", "scope": {"full_gap": False}, "controls": {"wrong_coefficient_rejected": True},
                  "budget": {"exact": "1/1000", "decimal": 0.001}, "bindings": bindings,
                  "ratio": {"denominator_lower": "1", "denominator_upper": "3", "numerator_lower": "-3",
                            "numerator_upper": "1", "lower": "-3", "upper": "1", "disjoint": False}}
        put(root, base + "output/results.json", result)
        frozen = {name: digest(root / name) for name in [base + "check.py", base + "report.md", base + "output/results.json"]}
        put(root, base + "freeze.json", {"loop": "ag2", "sha256": frozen})
        spec["producers"][side] = {"source_manifests": [manifest], "instruction_manifests": [], "required_snapshots": snapshots,
            "freeze": base + "freeze.json", "adoption_records": [], "semantic_controls": [
                {"id": "wrong-coefficient", "pointer": "/controls/wrong_coefficient_rejected", "equals": True},
                {"id": "no-full-gap", "pointer": "/scope/full_gap", "equals": False},
                {"id": "ratio-not-disjoint", "pointer": "/ratio/disjoint", "equals": False}],
            "rational_relations": [{"id": "useful-budget", "left": {"pointer": "/budget"}, "op": "lt", "right": {"constant": "7/1000"}}]}
        relations = spec["producers"][side]["rational_relations"]
        relations.append({"id": "strict-ratio-denominator", "left": {"pointer": "/ratio/denominator_lower"},
                          "op": "gt", "right": {"constant": 0}})
        corners = [{"quotient": [{"pointer": "/ratio/numerator_" + n}, {"pointer": "/ratio/denominator_" + d}]}
                   for n in ["lower", "upper"] for d in ["lower", "upper"]]
        for endpoint, operation in [("lower", "minimum"), ("upper", "maximum")]:
            relations.append({"id": "signed-ratio-" + endpoint, "left": {"pointer": "/ratio/" + endpoint},
                              "op": "eq", "right": {operation: corners}})
        all_bindings.update(bindings)
        all_bindings.update(snapshots)
        all_bindings.update(frozen)
        all_bindings[base + "freeze.json"] = digest(root / base / "freeze.json")
    script, output = PREFIX + "skeptic/ag2_independent.py", PREFIX + "skeptic/ag2-independent.json"
    put(root, script, "# synthetic independent checker; not executed\n")
    put(root, output, {"status": "synthetic-only"})
    spec["skeptic_checkers"] = [{"script": script, "output": output, "inputs": ["AGENTS.md"]}]
    admission = PREFIX + "advisor/ag2-admission.json"
    put(root, admission, spec)
    for name in [script, output, admission]:
        all_bindings[name] = digest(root / name)
    report = PREFIX + "skeptic/ag2.md"
    put(root, report, "Synthetic scope: no continuum proof.\n")
    all_bindings[report] = digest(root / report)
    review = {"schema": "ym28-skeptic-v1", "loop": "ag2", "accepted": True, "verdict": "accepted_with_limits",
              "supported": "Synthetic arithmetic fixture only", "limitations": ["No continuum proof"],
              "blocking_issues": [], "bindings": dict(all_bindings)}
    review_name = PREFIX + "skeptic/ag2.json"
    put(root, review_name, review)
    all_bindings[review_name] = digest(root / review_name)
    gate = {"schema": "ym28-gate-v1", "loop": "ag2", "sequence": 1, "goal": "AG", "goal_loop": 1,
            "model": "synthetic admission fixture", "verdict": "accepted_with_limits", "accepted": "Synthetic arithmetic only",
            "limitations": ["No continuum proof"], "bindings": all_bindings}
    put(root, PREFIX + "advisor/ag2-gate.json", gate)
    put(root, PREFIX + "release/admitted.json", {"schema": "ym28-reviewed-admission-pins-v1", "loops": {"ag2": {
        "contract_sha256": digest(root / contract_name), "admission_sha256": digest(root / admission),
        "gate_claim_projection": projection(gate, "gate"), "review_claim_projection": projection(review, "review")}}})


def rebind(root):
    """Rebind every mutable evidence envelope; leave reviewed admission pins fixed."""
    for side in ["forward", "reverse"]:
        base = PREFIX + f"{side}/ag2/"
        for suffix, key in [("output/results.json", "bindings"), ("freeze.json", "sha256")]:
            name = base + suffix
            data = json.loads((root / name).read_text())
            if suffix == "output/results.json" and "source_inventory" in data:
                data["source_inventory"] = {path: digest(root / path) for path in data["source_inventory"] if (root / path).is_file()}
                data["producer_bindings"] = {path: digest(root / base / path) for path in data["producer_bindings"] if (root / base / path).is_file()}
            else:
                key = "bindings" if suffix == "freeze.json" and "bindings" in data else key
                data[key] = {path: digest(root / path) for path in data.get(key, {}) if (root / path).is_file()}
            put(root, name, data)
    for name in [PREFIX + "skeptic/ag2.json", PREFIX + "advisor/ag2-gate.json"]:
        data = json.loads((root / name).read_text())
        data["bindings"] = {path: digest(root / path) for path in data["bindings"] if (root / path).is_file()}
        put(root, name, data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--loops", nargs="+")
    args = parser.parse_args()
    count = 0
    with tempfile.TemporaryDirectory(prefix="ym28-coherent-mutations-") as temporary:
        root = Path(temporary)
        baseline = root / "baseline"
        baseline.mkdir()
        fixture(baseline)
        Validator(baseline).validate("ag2")

        def attack(name, mutation, source=None):
            nonlocal count
            current = root / name
            shutil.copytree(source or baseline, current)
            mutation(current)
            rebind(current)
            try:
                Validator(current).validate("ag2")
            except (ValueError, KeyError, TypeError, FileNotFoundError, ZeroDivisionError):
                count += 1
                return
            raise ValueError("coherently rebound invalid evidence admitted: " + name)

        def edit(name, change):
            def action(current):
                data = json.loads((current / name).read_text())
                change(data)
                put(current, name, data)
            return action

        result_name = PREFIX + "forward/ag2/output/results.json"
        attack("failed-control", edit(result_name, lambda d: d["controls"].update(wrong_coefficient_rejected=False)))
        attack("boolean-integer-substitution", edit(result_name, lambda d: d["controls"].update(wrong_coefficient_rejected=1)))
        attack("missing-control", edit(result_name, lambda d: d["controls"].pop("wrong_coefficient_rejected")))
        attack("fake-full-gap", edit(result_name, lambda d: d["scope"].update(full_gap=True)))
        attack("large-budget", edit(result_name, lambda d: d["budget"].update(exact="1")))
        attack("float-only-evidence", edit(result_name, lambda d: d["budget"].pop("exact")))
        attack("ratio-false-positive", edit(result_name, lambda d: d["ratio"].update(disjoint=True)))
        attack("ratio-lower-sign", edit(result_name, lambda d: d["ratio"].update(lower="3")))
        attack("ratio-upper-sign", edit(result_name, lambda d: d["ratio"].update(upper="-1")))
        attack("ratio-zero-denominator", edit(result_name, lambda d: d["ratio"].update(denominator_lower="0")))
        attack("ratio-negative-denominator", edit(result_name, lambda d: d["ratio"].update(denominator_lower="-1")))
        attack("ratio-boolean-endpoint", edit(result_name, lambda d: d["ratio"].update(denominator_lower=True)))
        attack("continuum-promotion", edit(result_name, lambda d: d.update(continuum_proved=True)))
        attack("unreviewed-gate-claim", edit(PREFIX + "advisor/ag2-gate.json", lambda d: d.update(accepted="A physical gap is proved")))
        attack("unreviewed-review-claim", edit(PREFIX + "skeptic/ag2.json", lambda d: d.update(supported="A physical gap is proved")))
        attack("objection-removed-type", edit(PREFIX + "skeptic/ag2.json", lambda d: d.update(blocking_issues="")))
        attack("open-objection", edit(PREFIX + "skeptic/ag2.json", lambda d: d.update(blocking_issues=["missing domain proof"])))
        attack("unreviewed-semantic-rule", edit(PREFIX + "advisor/ag2-admission.json", lambda d: d["producers"]["forward"].update(semantic_controls=[])))
        attack("false-completion-count", edit(PREFIX + "advisor/progress.json", lambda d: d.update(completed_loops=["ag2", "ag3"])))

        def missing_snapshot(current):
            manifest = PREFIX + "forward/ag2/inputs/source-inventory.json"
            data = json.loads((current / manifest).read_text())
            data.pop("AGENTS.md")
            put(current, manifest, data)
            (current / (PREFIX + "forward/ag2/inputs/AGENTS.md")).unlink()
        attack("required-snapshot-coherently-removed", missing_snapshot)

        def cache(current):
            name = PREFIX + "forward/ag2/inputs/__pycache__/dependency.pyc"
            put(current, name, "untracked interpreter artifact")
            action = edit(result_name, lambda d: d["bindings"].update({name: digest(current / name)}))
            action(current)
        attack("cache-admission", cache)

        # AI3's split inventory and post-output report freeze are an explicit
        # convention, not permission to omit an executed script or input.
        split = root / "split-baseline"
        shutil.copytree(baseline, split)
        base = PREFIX + "forward/ag2/"
        data = json.loads((split / result_name).read_text())
        original = data.pop("bindings")
        data["source_inventory"] = {p: h for p, h in original.items() if not p.startswith(base)}
        data["producer_bindings"] = {p[len(base):]: h for p, h in original.items() if p.startswith(base) and p != base + "report.md"}
        put(split, result_name, data)
        frozen = json.loads((split / base / "freeze.json").read_text())
        frozen["bindings"] = frozen.pop("sha256")
        put(split, base + "freeze.json", frozen)
        admission = PREFIX + "advisor/ag2-admission.json"
        data = json.loads((split / admission).read_text())
        data["producers"]["forward"].update(binding_field="source_inventory", freeze_binding_field="bindings", report_binding="freeze")
        put(split, admission, data)
        pins_name = PREFIX + "release/admitted.json"
        pins = json.loads((split / pins_name).read_text())
        pins["loops"]["ag2"]["admission_sha256"] = digest(split / admission)
        put(split, pins_name, pins)
        rebind(split)
        Validator(split).validate("ag2")
        attack("split-missing-script", edit(result_name, lambda d: d["producer_bindings"].pop("check.py")), split)
        attack("split-missing-input-inventory", edit(result_name, lambda d: d["producer_bindings"].pop("inputs/source-inventory.json")), split)
        attack("split-missing-contract-source", edit(result_name, lambda d: d["source_inventory"].pop("AGENTS.md")), split)
        attack("split-unfrozen-report", edit(base + "freeze.json", lambda d: d["bindings"].pop(base + "report.md")), split)
        attack("split-unfrozen-output", edit(base + "freeze.json", lambda d: d["bindings"].pop(base + "output/results.json")), split)

        # A directly reviewed contract supplies a verified dependency chain for
        # checker inputs, while the active script/output still require direct
        # review. This models AI4's admitted AI3 output input without changing
        # any scientific fixture or expanding to arbitrary JSON traversal.
        transitive = root / "contract-input-baseline"
        shutil.copytree(baseline, transitive)
        review_name = PREFIX + "skeptic/ag2.json"
        edit(review_name, lambda d: d["bindings"].pop("AGENTS.md"))(transitive)
        rebind(transitive)
        Validator(transitive).validate("ag2")
        attack("unreviewed-transitive-contract", edit(review_name, lambda d: d["bindings"].pop(PREFIX + "contracts/ag2.json")), transitive)
        attack("unreviewed-active-checker", edit(review_name, lambda d: d["bindings"].pop(PREFIX + "skeptic/ag2_independent.py")), transitive)
        attack("transitive-input-absent-from-gate", edit(PREFIX + "advisor/ag2-gate.json", lambda d: d["bindings"].pop("AGENTS.md")), transitive)

        # Each snapshot case has fresh, internally coherent metadata, including
        # a newly pinned synthetic specification. Thus rejection tests the
        # permitted copy relationship, not a stale manifest/specification hash.
        def snapshot_case(label, accepted=False):
            nonlocal count
            current = root / ("snapshot-" + label)
            shutil.copytree(baseline, current)
            owned = PREFIX + "skeptic/ag2-post-review-inputs/"
            if label == "foreign-inventory":
                owned = PREFIX + "skeptic/ag3-post-review-inputs/"
            manifest = owned + "source-inventory.json"
            original = PREFIX + "skeptic/reviewed-source.json"
            put(current, original, {"synthetic_source": [1, 2, 3]})
            if label == "contract-original":
                original = "AGENTS.md"
            snapshot = owned + original
            if label == "outside-owned-subtree":
                snapshot = PREFIX + "skeptic/ag2-elsewhere/copied.json"
            put(current, snapshot, (current / original).read_text())
            if label == "different-snapshot-bytes":
                put(current, snapshot, {"synthetic_source": [1, 2, 4]})
            expected = digest(current / snapshot)
            entry = {"source": original, "snapshot": snapshot, "sha256": expected}
            if label == "wrong-entry-hash":
                entry["sha256"] = "0" * 64
            inventory = {"loop": "ag3" if label == "wrong-loop" else "ag2", "entries": [entry]}
            if label == "duplicate-copy-entry":
                inventory["entries"].append(dict(entry))
            put(current, manifest, inventory)
            specification = json.loads((current / admission).read_text())
            specification["skeptic_checkers"][0]["inputs"] = [manifest, snapshot]
            specification["bindings"].update({name: digest(current / name) for name in [manifest, snapshot]})
            if label == "inventory-not-spec-bound":
                specification["bindings"].pop(manifest)
            if label == "snapshot-not-spec-bound":
                specification["bindings"].pop(snapshot)
            put(current, admission, specification)
            pins = json.loads((current / pins_name).read_text())
            pins["loops"]["ag2"]["admission_sha256"] = digest(current / admission)
            put(current, pins_name, pins)
            for envelope in [review_name, PREFIX + "advisor/ag2-gate.json"]:
                document = json.loads((current / envelope).read_text())
                document["bindings"].update({name: digest(current / name) for name in [original, manifest]})
                if envelope != review_name:
                    document["bindings"][snapshot] = digest(current / snapshot)
                    if label == "snapshot-not-gate-bound":
                        document["bindings"].pop(snapshot)
                    if label == "inventory-not-gate-bound":
                        document["bindings"].pop(manifest)
                else:
                    if label in {"unreviewed-original", "contract-original"}:
                        document["bindings"].pop(original)
                    if label == "unreviewed-inventory":
                        document["bindings"].pop(manifest)
                put(current, envelope, document)
            rebind(current)
            try:
                Validator(current).validate("ag2")
            except ValueError:
                if accepted:
                    raise
                count += 1
            else:
                require(accepted, "invalid reviewed snapshot chain admitted: " + label)

        for label in ["direct-original", "contract-original"]:
            snapshot_case(label, accepted=True)
        for label in ["foreign-inventory", "wrong-loop", "outside-owned-subtree", "different-snapshot-bytes",
                      "wrong-entry-hash", "duplicate-copy-entry", "inventory-not-spec-bound",
                      "snapshot-not-spec-bound", "snapshot-not-gate-bound", "inventory-not-gate-bound",
                      "unreviewed-original", "unreviewed-inventory"]:
            snapshot_case(label)

        auxiliary = root / "auxiliary-baseline"
        shutil.copytree(baseline, auxiliary)
        artifact_name = base + "output/matrix.json"
        put(auxiliary, artifact_name, {"synthetic": [1, 2]})
        checksum = digest(auxiliary / artifact_name)
        edit(result_name, lambda d: d.update(artifact_sha256={"matrix.json": checksum}))(auxiliary)
        edit(base + "freeze.json", lambda d: d["sha256"].update({artifact_name: checksum}))(auxiliary)
        edit(PREFIX + "advisor/ag2-gate.json", lambda d: d["bindings"].update({artifact_name: checksum}))(auxiliary)
        data = json.loads((auxiliary / admission).read_text())
        data["producers"]["forward"]["output_artifacts"] = {"matrix.json": {"sha256": checksum, "sha256_pointer": "/artifact_sha256/matrix.json"}}
        put(auxiliary, admission, data)
        pins = json.loads((auxiliary / pins_name).read_text())
        pins["loops"]["ag2"]["admission_sha256"] = digest(auxiliary / admission)
        put(auxiliary, pins_name, pins)
        rebind(auxiliary)
        Validator(auxiliary).validate("ag2")
        attack("artifact-unfrozen", edit(base + "freeze.json", lambda d: d["sha256"].pop(artifact_name)), auxiliary)
        attack("artifact-gate-omission", edit(PREFIX + "advisor/ag2-gate.json", lambda d: d["bindings"].pop(artifact_name)), auxiliary)
        attack("artifact-result-hash-changed", edit(result_name, lambda d: d["artifact_sha256"].update({"matrix.json": "0" * 64})), auxiliary)
        attack("undeclared-artifact", lambda current: put(current, base + "output/extra.json", {}), auxiliary)
        attack("artifact-missing", lambda current: (current / artifact_name).unlink(), auxiliary)

        # A replay returning byte-identical results.json but wrong/missing extra
        # files is still not a reproducible multi-file output.
        stored = auxiliary / base / "output"
        def replay_case(label, change):
            nonlocal count
            fresh = root / label
            shutil.copytree(stored, fresh)
            change(fresh)
            try:
                replay_artifacts(fresh, stored, {"matrix.json": checksum})
            except ValueError:
                count += 1
            else:
                raise ValueError("invalid auxiliary replay admitted: " + label)
        replay_artifacts(stored, stored, {"matrix.json": checksum})
        replay_case("fresh-artifact-tampered", lambda fresh: (fresh / "matrix.json").write_text("{}\n"))
        replay_case("fresh-artifact-missing", lambda fresh: (fresh / "matrix.json").unlink())
        replay_case("fresh-extra-output", lambda fresh: (fresh / "extra.json").write_text("{}\n"))
        def link_artifact(fresh):
            (fresh / "matrix.json").unlink()
            (fresh / "matrix.json").symlink_to(stored / "matrix.json")
        replay_case("fresh-linked-output", link_artifact)
        def cached_artifact(fresh):
            (fresh / "__pycache__").mkdir()
            (fresh / "__pycache__/dependency.pyc").write_bytes(b"synthetic cache")
        replay_case("fresh-cache-output", cached_artifact)

        # Missing files and changed source bytes must also be rejected before
        # replay; unlike attacks above this directly exercises basic binding.
        damaged = root / "damaged"
        shutil.copytree(baseline, damaged)
        (damaged / "AGENTS.md").write_text("tampered source\n")
        try:
            Validator(damaged).validate("ag2")
        except ValueError:
            count += 1
        else:
            raise ValueError("tampered scientific source admitted")
    # Exact arithmetic expression grammar must not reinterpret a Boolean,
    # negative or fractional power, or a scalar as a collection.
    for expression in [
        {"power": [{"constant": 2}, {"constant": True}]},
        {"power": [{"constant": 2}, {"constant": -1}]},
        {"power": [{"constant": 2}, {"constant": "1/2"}]},
        {"power": [{"constant": 2}, {"constant": 65}]},
        {"minimum": []}, {"absolute": [{"constant": 1}, {"constant": 2}]},
        {"length": "/scalar"},
    ]:
        try:
            operand({"scalar": "text"}, expression)
        except ValueError:
            count += 1
        else:
            raise ValueError("invalid arithmetic expression admitted")
    validator = Validator()
    _, completed, _ = validator.sequence()
    loops = args.loops or completed
    require(set(loops) <= set(completed), "requested mutation audit precedes completed admission")
    for loop in loops:
        validator.validate(loop)
        spec = validator.load(PREFIX + f"advisor/{loop}-admission.json")
        for side in ["forward", "reverse"]:
            result = validator.load(PREFIX + f"{side}/{loop}/output/results.json")
            semantics(result, spec["producers"][side])
    scoped_mutations = {}
    freeze_mutations = {}
    from release.replay_output_controls import run as replay_output_controls
    replay_mutations = replay_output_controls()["fresh_output_mutations_rejected"]
    from release.aj1_inventory_controls import run as aj1_inventory_controls
    inventory_mutations = aj1_inventory_controls()["inventory_mutations_rejected"]
    from release.aj1_admission_controls import adapter_controls as aj1_adapter_controls, run as aj1_semantic_controls
    adapter_mutations = aj1_adapter_controls()["adapter_mutations_rejected"]
    if "ah2" in loops:
        from release.ah2_admission_controls import run as ah2_controls
        scoped_mutations["ah2"] = ah2_controls(PREFIX + "advisor/ah2-admission.json")["semantic_mutations_rejected"]
    if "aj1" in loops:
        scoped_mutations["aj1"] = aj1_semantic_controls(PREFIX + "advisor/aj1-admission.json")["semantic_mutations_rejected"]
    if "aj2" in loops:
        from release.aj2_admission_controls import run as aj2_semantic_controls
        scoped_mutations["aj2"] = aj2_semantic_controls(PREFIX + "advisor/aj2-admission.json")["semantic_mutations_rejected"]
    if "ak1" in loops:
        from release.ak1_admission_controls import run as ak1_semantic_controls
        from release.ak1_freeze_controls import run as ak1_freeze_controls
        scoped_mutations["ak1"] = ak1_semantic_controls(PREFIX + "advisor/ak1-admission.json")["semantic_mutations_rejected"]
        freeze_mutations["ak1"] = ak1_freeze_controls(PREFIX + "advisor/ak1-admission.json")["freeze_mutations_rejected"]
    if "ak2" in loops:
        from release.ak2_admission_controls import run as ak2_semantic_controls
        scoped_mutations["ak2"] = ak2_semantic_controls(PREFIX + "advisor/ak2-admission.json")["semantic_mutations_rejected"]
    print(json.dumps({"status": "passed", "coherent_and_binding_mutations_rejected": count,
                      "scoped_semantic_mutations_rejected": scoped_mutations,
                      "freeze_namespace_mutations_rejected": freeze_mutations,
                      "typed_inventory_mutations_rejected": inventory_mutations,
                      "provenance_adapter_mutations_rejected": adapter_mutations,
                      "fresh_output_mutations_rejected": replay_mutations,
                      "completed_loops_checked": loops, "new_research_loops": 0,
                      "scope": "synthetic coherent tampering controls plus actual completed-source admission; no synthetic physics evidence"}))


if __name__ == "__main__":
    main()
