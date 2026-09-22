"""Admit and replay only the three Round27 investigations.

Source integrity and deterministic replay are necessary reproducibility checks,
not a proof of the reports' mathematical claims or of continuum Yang--Mills.
All admission checks remain active under ``python -O``.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
ROUND = "research/round27/"
R = ROOT / ROUND

# Explicit semantic admission records, reviewed against the reports. These are
# hashes of the stated projections (below), not a heuristic text-equivalence
# algorithm. AI2's gate groups the review's seven limitations into five clauses
# and its accepted statement. Admission retains BOTH lists; see release README.
REVIEWED_SCOPES = {
    "ai1": {
        "gate": "95ee8ec677d086298cb0ab6ea770902eb5116b22abf1da00f450c53f7bfdbb2d",
        "review": "d5418cb5c9f31e9d12271caaa3cb80be6087c713526bbfab61229c721311bad5",
    },
    "ai2": {
        "gate": "fa4b5043163b36f0e01af61e02dd9b7917c3ed78c528251c9f5917d879a2fe8f",
        "review": "029e9e3fc6a077aca91c7dc18e267c94b607526ab58112d86f65c5cda8cee81d",
    },
    "ag1": {
        "gate": "ee4d5e79ae5e3ecfe218386a9aca4d26d4a148d4dabff71bc3a15bf939addd83",
        "review": "42f6f6a35bfe4c2306eb7cf4588c4bc3a86a56199e2f6fd2d18fd42bcb9a2127",
    },
}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source(name):
    require(isinstance(name, str) and bool(name), "missing source name")
    relative = Path(name)
    require(not relative.is_absolute() and ".." not in relative.parts, "unsafe source path: " + name)
    path = ROOT / relative
    require(path.is_file() and path.resolve().is_relative_to(ROOT), "missing source: " + name)
    require(not any(p.is_symlink() for p in [path, *path.parents] if p.is_relative_to(ROOT)),
            "linked source path: " + name)
    return path


def load(name):
    value = json.loads(source(name).read_text())
    require(isinstance(value, dict), "JSON object required: " + name)
    return value


def hashes(bindings):
    require(isinstance(bindings, dict) and bool(bindings), "empty source bindings")
    for name, expected in bindings.items():
        require(isinstance(expected, str) and re.fullmatch(r"[0-9a-f]{64}", expected),
                "invalid SHA256: " + str(name))
        require(digest(source(name)) == expected, "changed source: " + name)


def text_field(obj, key):
    require(isinstance(obj.get(key), str) and bool(obj[key].strip()), "missing " + key)


def text_list(obj, key):
    value = obj.get(key)
    require(isinstance(value, list) and bool(value)
            and all(isinstance(x, str) and bool(x.strip()) for x in value), "missing " + key)


def reject_continuum_promotion(value):
    """Reject unsupported machine-readable promotion, without guessing prose intent."""
    if isinstance(value, dict):
        for key, item in value.items():
            name = key.lower().replace("-", "_")
            promotion = name in {"solved_yang_mills", "yang_mills_solved", "clay_problem_solved"}
            promotion = promotion or ("continuum" in name and any(
                token in name for token in ["claim", "solved", "proved", "proven", "established"]))
            if promotion:
                require(item is False or item is None, "unsupported continuum flag: " + key)
            reject_continuum_promotion(item)
    elif isinstance(value, list):
        for item in value:
            reject_continuum_promotion(item)


def sequence():
    record = load(ROUND + "advisor/sequence.json")
    loops = record.get("loops")
    require(isinstance(loops, list) and len(loops) == 3 and len(set(loops)) == 3,
            "exactly three distinct loops required")
    require(loops[:2] == ["ai1", "ai2"] and all(re.fullmatch(r"[a-z]+[1-9][0-9]*", x) for x in loops),
            "unexpected loop sequence")
    reject_continuum_promotion(record)
    return loops


def metadata(gate, contract, loop, index=None, previous=None):
    require(gate.get("schema") == "ym27-gate-v1", "gate schema")
    require(contract.get("schema") == "ym27-contract-v1", "contract schema")
    require(gate.get("loop") == loop == contract.get("loop"), "loop identity")
    if index is not None:
        require(gate.get("sequence") == index == contract.get("sequence"), "loop order")
    for obj in [gate, contract]:
        text_field(obj, "model")
        reject_continuum_promotion(obj)
    for key in ["frozen_at", "acceptance"]:
        text_field(contract, key)
    text_list(contract, "requirements")
    require(isinstance(contract.get("parameters"), dict) and bool(contract["parameters"]), "parameter domain missing")
    require(isinstance(contract.get("sources"), dict) and bool(contract["sources"]), "contract dependencies missing")
    require("AGENTS.md" in contract["sources"], "contract instruction dependency missing")
    if previous:
        require(ROUND + f"advisor/{previous}-gate.json" in contract["sources"], "adaptive predecessor missing")
    require(gate.get("verdict") in {"accepted_with_limits", "accepted_within_scope", "limited", "conditional"},
            "unsupported gate verdict")
    text_field(gate, "accepted")
    text_list(gate, "limitations")
    require(any("continuum" in item.lower() for item in gate["limitations"]), "continuum limitation missing")
    text_list(gate, "network_dependencies")
    required = {ROUND + f"contracts/{loop}.json", ROUND + f"skeptic/{loop}.json", ROUND + f"skeptic/{loop}.md"}
    for direction in ["forward", "reverse"]:
        required.update(ROUND + f"{direction}/{loop}/{suffix}" for suffix in
                        ["check.py", "report.md", "output/results.json", "inputs/source-inventory.json"])
    require(isinstance(gate.get("bindings"), dict) and required <= gate["bindings"].keys(),
            "gate missing required contract, review or producer dependency")


def producer_inventory(result):
    text_field(result, "schema")
    text_field(result, "scope")
    reject_continuum_promotion(result)
    bindings = result.get("bindings")
    require(isinstance(bindings, dict) and bool(bindings), "producer bindings missing")
    return bindings


def producer_metadata(result, contract, loop, direction):
    bindings = producer_inventory(result)
    base = ROUND + f"{direction}/{loop}/"
    required = {ROUND + f"contracts/{loop}.json", base + "check.py", base + "report.md", *contract["sources"]}
    require(required <= bindings.keys(), "producer missing contract/source dependencies")
    return bindings


def claim_projection_digest(record, kind):
    fields = (["loop", "model", "verdict", "accepted", "limitations"] if kind == "gate"
              else ["schema", "accepted", "verdict", "supported", "limitations"])
    projection = {key: record.get(key) for key in fields}
    return hashlib.sha256(json.dumps(projection, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False).encode()).hexdigest()


def review_agreement(gate, review, loop):
    require(review.get("accepted") is True, "skeptical admission missing")
    blockers = review.get("blocking_issues", [])
    require(isinstance(blockers, list) and not blockers, "unresolved/malformed skeptical objection")
    text_list(review, "limitations")
    require(any("continuum" in item.lower() for item in review["limitations"]), "review continuum limitation missing")
    reject_continuum_promotion(review)
    require(loop in REVIEWED_SCOPES, "claim/scope reconciliation not yet reviewed: " + loop)
    for kind, record in [("gate", gate), ("review", review)]:
        require(claim_projection_digest(record, kind) == REVIEWED_SCOPES[loop][kind],
                "changed reviewed " + kind + " claim or limitations: " + loop)
    # This is a conjunction of admitted restrictions, not permission to discard
    # a review restriction just because the shorter gate uses different words.
    return list(dict.fromkeys(gate["limitations"] + review["limitations"]))


def scope_reconciliation(record, effective):
    require(record.get("schema") == "ym27-skeptic-release-scope-v1" and record.get("status") == "ACCEPTED",
            "AI2 scope reconciliation not admitted")
    require(record.get("gate_claim_projection") == REVIEWED_SCOPES["ai2"]["gate"]
            and record.get("review_claim_projection") == REVIEWED_SCOPES["ai2"]["review"],
            "AI2 reconciliation claim identity changed")
    require(record.get("preserves_all_restrictions") is True and record.get("effective_limitations") == effective,
            "AI2 reconciliation omitted a restriction")


def snapshots(loop, direction, bindings):
    base = ROUND + f"{direction}/{loop}/"
    name = base + "inputs/source-inventory.json"
    inventory = load(name)
    covered = set()
    if "entries" in inventory:
        entries = inventory["entries"]
        require(isinstance(entries, list) and bool(entries), "empty snapshot entries")
        for entry in entries:
            require(isinstance(entry, dict), "malformed snapshot entry")
            origin, snapshot, expected = entry.get("source"), entry.get("snapshot"), entry.get("sha256")
            require(isinstance(snapshot, str) and snapshot.startswith(base + "inputs/"), "foreign snapshot")
            hashes({origin: expected, snapshot: expected})
            require(bindings.get(origin) == expected, "unbound snapshot origin: " + str(origin))
            covered.add(origin)
    else:
        hashes(inventory)
        for origin, expected in inventory.items():
            hashes({base + "inputs/" + origin: expected})
            require(bindings.get(origin) == expected, "unbound snapshot origin: " + origin)
            covered.add(origin)
    require({"AGENTS.md", ROUND + f"contracts/{loop}.json"} <= covered,
            "required instruction/contract snapshot missing")
    return inventory


def validate(loop, index=None, previous=None):
    contract = load(ROUND + f"contracts/{loop}.json")
    gate = load(ROUND + f"advisor/{loop}-gate.json")
    metadata(gate, contract, loop, index, previous)
    hashes(contract["sources"])
    hashes(gate["bindings"])
    review = load(ROUND + f"skeptic/{loop}.json")
    effective = review_agreement(gate, review, loop)
    if loop == "ai2":
        scope_reconciliation(load(ROUND + "skeptic/release-scope-review.json"), effective)
    hashes(review.get("bindings"))
    for direction in ["forward", "reverse"]:
        base = ROUND + f"{direction}/{loop}/"
        result = load(base + "output/results.json")
        bindings = producer_metadata(result, contract, loop, direction)
        hashes(bindings)
        snapshots(loop, direction, bindings)
        freeze_path = ROOT / base / "freeze.json"
        if freeze_path.is_file():
            freeze = load(base + "freeze.json")
            if "files" in freeze:
                hashes({base + name: value for name, value in freeze["files"].items()})
            elif "sha256" in freeze:
                hashes(freeze["sha256"])
            else:
                require(False, "current freeze source inventory missing: " + base)
        # A producer may execute bound Python helpers; their own explicit source
        # inventories are checked above. The reports retain theorem assumptions.
    return gate


def run_command(command, logfile):
    run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
    logfile.write_text(run.stdout + run.stderr)
    record = {"command": command, "exit_code": run.returncode,
              "log": str(logfile), "log_sha256": digest(logfile)}
    require(run.returncode == 0, "failed command; see " + str(logfile))
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--optimized", action="store_true")
    parser.add_argument("--loops", nargs="+", help="Targeted pre-release replay; full release always runs the final sequence")
    args = parser.parse_args()
    require(args.output.is_absolute(), "absolute output required")
    out = args.output.resolve()
    require(not out.exists() and not out.is_relative_to(ROOT), "fresh external output required")
    full = sequence() if (R / "advisor/sequence.json").exists() else None
    loops = args.loops or full
    require(bool(loops), "final sequence missing")
    require(len(set(loops)) == len(loops), "duplicate replay request")
    if full:
        require(set(loops) <= set(full), "replay outside final sequence")
    else:
        require(args.loops is not None and all(re.fullmatch(r"[a-z]+[1-9][0-9]*", x) for x in loops),
                "explicit targeted loops required before sequence exists")
    out.mkdir(parents=True)
    records = []
    for loop in loops:
        pos = full.index(loop) if full else None
        gate = validate(loop, None if pos is None else pos + 1, None if not pos else full[pos - 1])
        for direction in ["forward", "reverse"]:
            dest = out / f"{loop}-{direction}"
            command = [sys.executable, "-B"] + (["-O"] if args.optimized else []) + [
                str(R / direction / loop / "check.py"), "--output", str(dest)]
            record = run_command(command, out / f"{loop}-{direction}.log")
            expected = R / direction / loop / "output/results.json"
            require((dest / "results.json").read_bytes() == expected.read_bytes(),
                    "fresh producer bytes differ: " + loop + "/" + direction)
            records.append({**record, "loop": loop, "direction": direction,
                            "results_sha256": digest(expected),
                            "gate_sha256": digest(R / "advisor" / f"{loop}-gate.json"),
                            "effective_limitations": review_agreement(gate, load(ROUND + f"skeptic/{loop}.json"), loop)})
    receipt = {"status": "passed", "optimized": args.optimized, "new_research_loops": 0,
               "loops_replayed": loops, "producer_executions": len(records), "checks": records,
               "scope": "source/snapshot integrity and byte-identical deterministic producer replay; no continuum claim"}
    (out / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"status": "passed", "producer_executions": len(records),
                      "receipt_sha256": digest(out / "receipt.json")}))


if __name__ == "__main__":
    main()
