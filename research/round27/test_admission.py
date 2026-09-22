"""Targeted malicious/missing-evidence controls; safe under python -O."""
import copy
import argparse
import json
from pathlib import Path
import tempfile

import reproduce as admission


def reject(action):
    try:
        action()
    except (ValueError, KeyError, TypeError, FileNotFoundError):
        return
    raise ValueError("invalid evidence was admitted")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--loops", nargs="+", help="Explicit targeted gates during unfinished research")
    args = parser.parse_args()
    count = 0
    full = (admission.sequence() if (admission.R / "advisor/sequence.json").exists()
             else sorted(p.stem[:-5] for p in (admission.R / "advisor").glob("*-gate.json")))
    loops = args.loops or full
    admission.require(set(loops) <= set(full) and len(set(loops)) == len(loops), "invalid targeted loops")
    admission.require(bool(loops), "no gates available")
    for index, loop in enumerate(loops):
        gate = admission.load(admission.ROUND + f"advisor/{loop}-gate.json")
        contract = admission.load(admission.ROUND + f"contracts/{loop}.json")
        review = admission.load(admission.ROUND + f"skeptic/{loop}.json")
        admission.validate(loop)
        effective = admission.review_agreement(gate, review, loop)
        admission.require(set(gate["limitations"] + review["limitations"]) <= set(effective),
                          "reconciled scope discarded a restriction")
        if loop == "ai2":
            scope_review = admission.load(admission.ROUND + "skeptic/release-scope-review.json")
            for key, value in [("status", "PENDING"), ("gate_claim_projection", "0" * 64),
                               ("preserves_all_restrictions", False), ("effective_limitations", effective[:-1])]:
                bad = copy.deepcopy(scope_review); bad[key] = value
                reject(lambda: admission.scope_reconciliation(bad, effective)); count += 1
        for which in ["gate", "review"]:
            for key in ["limitations", "accepted" if which == "gate" else "supported"]:
                bad = copy.deepcopy(gate if which == "gate" else review)
                bad[key] = bad[key][:-1] if key == "limitations" else "The continuum problem is solved."
                reject(lambda: admission.review_agreement(bad if which == "gate" else gate,
                       bad if which == "review" else review, loop)); count += 1
        for blockers in [["unresolved norm hypothesis"], "", None, {}]:
            bad = copy.deepcopy(review); bad["blocking_issues"] = blockers
            reject(lambda: admission.review_agreement(gate, bad, loop)); count += 1
        bad = copy.deepcopy(review); bad["accepted"] = False
        reject(lambda: admission.review_agreement(gate, bad, loop)); count += 1
        for suffix in [f"contracts/{loop}.json", f"skeptic/{loop}.json",
                       f"forward/{loop}/check.py", f"reverse/{loop}/report.md",
                       f"forward/{loop}/output/results.json", f"reverse/{loop}/inputs/source-inventory.json"]:
            bad = copy.deepcopy(gate)
            bad["bindings"].pop(admission.ROUND + suffix)
            reject(lambda: admission.metadata(bad, contract, loop)); count += 1
        for key, value in [("model", ""), ("limitations", []), ("limitations", "none"),
                           ("verdict", "solved_yang_mills"), ("accepted", True),
                           ("continuum_gap_proved", True), ("network_dependencies", [])]:
            bad = copy.deepcopy(gate); bad[key] = value
            reject(lambda: admission.metadata(bad, contract, loop)); count += 1
        for key in ["model", "sources", "acceptance", "requirements", "parameters", "frozen_at"]:
            bad = copy.deepcopy(contract); bad.pop(key)
            reject(lambda: admission.metadata(gate, bad, loop)); count += 1
        bad = copy.deepcopy(contract); bad["sources"].pop("AGENTS.md")
        reject(lambda: admission.metadata(gate, bad, loop)); count += 1
        if index:
            bad = copy.deepcopy(contract)
            bad["sources"].pop(admission.ROUND + f"advisor/{loops[index - 1]}-gate.json", None)
            reject(lambda: admission.metadata(gate, bad, loop, previous=loops[index - 1])); count += 1
        for direction in ["forward", "reverse"]:
            base = admission.ROUND + f"{direction}/{loop}/"
            result = admission.load(base + "output/results.json")
            for removed in ["scope", "bindings"]:
                bad = copy.deepcopy(result); bad.pop(removed)
                reject(lambda: admission.producer_metadata(bad, contract, loop, direction)); count += 1
            for removed in [admission.ROUND + f"contracts/{loop}.json", "AGENTS.md", base + "check.py"]:
                bad = copy.deepcopy(result); bad["bindings"].pop(removed)
                reject(lambda: admission.producer_metadata(bad, contract, loop, direction)); count += 1
            bad = copy.deepcopy(result); bad["continuum_claim"] = True
            reject(lambda: admission.producer_inventory(bad)); count += 1
            bad_bindings = copy.deepcopy(result["bindings"])
            bad_bindings[base + "check.py"] = "0" * 64
            reject(lambda: admission.hashes(bad_bindings)); count += 1
            bad_gate_bindings = copy.deepcopy(gate["bindings"])
            bad_gate_bindings[base + "output/results.json"] = "0" * 64
            reject(lambda: admission.hashes(bad_gate_bindings)); count += 1
    reject(lambda: admission.hashes({})); count += 1
    reject(lambda: admission.hashes({"../outside": "0" * 64})); count += 1
    reject(lambda: admission.reject_continuum_promotion({"claims": {"continuum_proven": True}})); count += 1
    # Exercise missing files, altered bytes, absent snapshots, and linked paths
    # in a synthetic root, without touching any historical or accepted artifact.
    original_root = admission.ROOT
    with tempfile.TemporaryDirectory(prefix="ym27-admission-mutations-") as temp:
        try:
            admission.ROOT = Path(temp)
            origin = admission.ROOT / "AGENTS.md"
            origin.write_text("frozen instructions\n")
            expected = admission.digest(origin)
            admission.hashes({"AGENTS.md": expected})
            origin.write_text("altered instructions\n")
            reject(lambda: admission.hashes({"AGENTS.md": expected})); count += 1
            origin.unlink()
            reject(lambda: admission.hashes({"AGENTS.md": expected})); count += 1
            origin.write_text("frozen instructions\n")
            linked = admission.ROOT / "linked.md"; linked.symlink_to(origin)
            reject(lambda: admission.source("linked.md")); count += 1
            base = admission.ROUND + "forward/ai1/inputs/"
            inventory = admission.ROOT / base / "source-inventory.json"
            inventory.parent.mkdir(parents=True)
            # A coherently hashed inventory may still omit mandatory contract
            # or instruction snapshots. Hash equality alone cannot admit it.
            (inventory.parent / "AGENTS.md").write_bytes(origin.read_bytes())
            inventory.write_text(json.dumps({"AGENTS.md": expected}))
            reject(lambda: admission.snapshots("ai1", "forward", {"AGENTS.md": expected})); count += 1
        finally:
            admission.ROOT = original_root
    print(json.dumps({"status": "passed", "loops": loops, "rejected_mutations": count,
                      "scope": "missing dependencies, changed source/output bytes, absent model/scope, snapshot omissions and continuum inflation"}))


if __name__ == "__main__":
    main()
