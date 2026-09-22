"""Additive, explicitly pinned replay of Round28 with two portable AH copies.

The original admission validator, science and outputs remain authoritative and
unchanged. A caller must supply the separately reviewed repair manifest digest.
No output is normalized: each fresh file is compared with frozen expected bytes.
"""
import argparse
import difflib
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
from reproduce import ROOT, PREFIX, Validator, digest, require, replay_artifacts

REPAIR = PREFIX + "release/ah-portability/"
MANIFEST = REPAIR + "manifest.json"
LEGACY_ROOT = Path("/workspace/scratch/9daefcf0521b/yang_mills_workbench")
LOOPS = ("ah1", "ah2")


def repository_origins(validator, loop):
    """Derive exactly the eight historically checked repository originals."""
    inventory = validator.load(PREFIX + f"reverse/{loop}/inputs/instruction-inventory.json")
    ordered = sorted(inventory.items()) if loop == "ah1" else list(inventory.items())
    entries, mapping = [], {}
    for index, (key, entry) in enumerate(ordered):
        origin = Path(entry["origin"])
        if not key.startswith("repo-"):
            require(not origin.is_relative_to(LEGACY_ROOT), "unclassified repository instruction")
            continue  # Installed origins are never opened.
        require(origin.is_absolute() and origin.is_relative_to(LEGACY_ROOT), "foreign repository origin")
        relative = str(origin.relative_to(LEGACY_ROOT))
        require(relative.startswith(".codex/skills/qeg-research-advisor/references/")
                and relative.endswith(".md") and ".." not in Path(relative).parts,
                "unsupported repository instruction path")
        original = validator.source(relative)
        snapshot_name = PREFIX + f"reverse/{loop}/" + entry["snapshot"]
        require(snapshot_name.startswith(PREFIX + f"reverse/{loop}/inputs/instructions/"),
                "foreign instruction snapshot")
        snapshot = validator.source(snapshot_name)
        require(digest(original) == digest(snapshot) == entry["sha256"], "instruction original/copy mismatch")
        require(entry["origin"] not in mapping, "duplicate repository origin")
        mapping[entry["origin"]] = relative
        entries.append({"instruction": key, "index": index, **entry, "repository_path": relative,
                        "original_check": ("repo_instruction_original_" if loop == "ah1" else "repo_instruction_")
                        + f"{index:02}"})
    require(len(mapping) == 8, "all eight repository instructions required")
    return entries, mapping


def transform(original, loop, mapping):
    """Reconstruct the only permitted textual change; no scientific edits."""
    header = "ROOT = Path(__file__).resolve().parents[5]\nHERE = ROOT / " + repr(PREFIX + f"reverse/{loop}")
    header += "\nREPOSITORY_ORIGINS = " + json.dumps(mapping, indent=4, sort_keys=True) + "\n"
    if loop == "ah1":
        replacements = [
            ("HERE = Path(__file__).resolve().parent\nROOT = HERE.parents[3]\n", header),
            ('        if original.is_relative_to(ROOT):',
             '        if e["origin"] in REPOSITORY_ORIGINS:\n            original = ROOT / REPOSITORY_ORIGINS[e["origin"]]'),
            ("    return bindings\n", '    bindings[str(Path(__file__).resolve().relative_to(ROOT))] = sha(Path(__file__).resolve())\n    return bindings\n')]
    else:
        replacements = [
            ("HERE=Path(__file__).resolve().parent\nROOT=HERE.parents[3]\n", header),
            ('        if origin.is_relative_to(ROOT):',
             '        if e["origin"] in REPOSITORY_ORIGINS:\n            origin=ROOT/REPOSITORY_ORIGINS[e["origin"]]'),
            ("    return bindings\n", '    bindings[str(Path(__file__).resolve().relative_to(ROOT))]=sha(Path(__file__).resolve())\n    return bindings\n')]
    result = original
    for old, new in replacements:
        require(result.count(old) == 1, "ambiguous or changed original source transformation")
        result = result.replace(old, new, 1)
    return result


def payload_relation(original, portable, script, script_hash):
    require(set(portable) == set(original), "portable result fields changed")
    require(set(portable["bindings"]) == set(original["bindings"]) | {script},
            "only the executed portable-script binding may be added")
    require(script not in original["bindings"], "portable script is not an additive binding")
    require(portable["bindings"][script] == script_hash, "executed portable script not bound")
    require(all(portable["bindings"][name] == value for name, value in original["bindings"].items()),
            "original result bindings changed")
    for key in original:
        if key != "bindings":
            require(portable[key] == original[key] and type(portable[key]) is type(original[key]),
                    "original result payload changed: " + key)
    # Canonical JSON equality distinguishes Boolean/integer and all nested types.
    expected = dict(original)
    expected["bindings"] = {**original["bindings"], script: script_hash}
    require(json.dumps(portable, sort_keys=True) == json.dumps(expected, sort_keys=True),
            "typed complete result payload changed")


def validate_repair(validator, manifest_sha256):
    require(digest(validator.source(MANIFEST)) == manifest_sha256, "repair manifest identity changed")
    manifest = validator.load(MANIFEST)
    require(manifest.get("schema") == "ym28-ah-portability-manifest-v1", "repair manifest schema")
    require(type(manifest.get("new_research_loops")) is int and manifest["new_research_loops"] == 0,
            "administrative repair changed loop count")
    require(set(manifest.get("substitutions", {})) == set(LOOPS), "undeclared producer substitution")
    validator.hashes(manifest["bindings"])
    require(manifest["bindings"].get(PREFIX + "portable_reproduce.py") == digest(validator.source(PREFIX + "portable_reproduce.py")),
            "executed runner not manifest-bound")
    require(manifest["bindings"].get(PREFIX + "reproduce.py") ==
            "6ebf9b5116aba99cae5432796b890745872d7785d1bdedd8afee17d2a517b5fd", "original validator changed")
    require(manifest["bindings"].get(PREFIX + "release/admitted.json") ==
            "5280e49631cdabf646edc1ff3e494a59ddb513ebbb96a0a102f3e551a7ade078", "original registry changed")
    for loop in LOOPS:
        record = manifest["substitutions"][loop]
        original_script = PREFIX + f"reverse/{loop}/check.py"
        portable_script = REPAIR + f"{loop}/check.py"
        original_output = PREFIX + f"reverse/{loop}/output/results.json"
        portable_output = REPAIR + f"{loop}/expected/results.json"
        require(record["original_script"] == original_script and record["portable_script"] == portable_script
                and record["original_output"] == original_output and record["portable_output"] == portable_output,
                "undeclared replacement interface")
        require(record["instructions"] == PREFIX + f"reverse/{loop}/inputs/instruction-inventory.json",
                "undeclared replacement instruction inventory")
        entries, mapping = repository_origins(validator, loop)
        require(record["repository_origins"] == entries, "incomplete or unsupported repository-origin map")
        original_text = validator.source(original_script).read_text()
        expected_text = transform(original_text, loop, mapping)
        require(validator.source(portable_script).read_text() == expected_text, "portable source exceeds exact repair")
        diff_name = REPAIR + f"{loop}/checker.diff"
        expected_diff = "".join(difflib.unified_diff(original_text.splitlines(True), expected_text.splitlines(True),
                                                    fromfile=original_script, tofile=portable_script))
        require(validator.source(diff_name).read_text() == expected_diff, "repair diff differs from actual source")
        original = validator.load(original_output)
        portable = validator.load(portable_output)
        payload_relation(original, portable, portable_script, digest(validator.source(portable_script)))
        require(original["check_count"] == record["original_check_count"] == (320 if loop == "ah1" else 717),
                "original check count changed")
        for entry in entries:
            require(original["checks"].get(entry["original_check"]) is True, "original repository check omitted")
        spec = validator.load(PREFIX + f"advisor/{loop}-admission.json")
        artifacts = {name: value["sha256"] for name, value in spec["producers"]["reverse"].get("output_artifacts", {}).items()}
        expected_dir = validator.source(portable_output).parent
        replay_artifacts(expected_dir, validator.source(original_output).parent, artifacts)
        required = {original_script, portable_script, original_output, portable_output, diff_name,
                    PREFIX + f"reverse/{loop}/inputs/instruction-inventory.json"}
        required.update(REPAIR + f"{loop}/expected/" + name for name in artifacts)
        require(required <= set(manifest["bindings"]), "repair evidence missing manifest binding")
        validator.hashes(portable["bindings"])
    return manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest-sha256", required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--optimized", action="store_true")
    parser.add_argument("--validate-only", action="store_true")
    parser.add_argument("--repair-only", action="store_true", help="proposal verification: only the two replacement scripts")
    args = parser.parse_args()
    validator = Validator()
    _, completed, _ = validator.sequence(complete=True)
    admissions = {loop: validator.validate(loop) for loop in completed}
    manifest = validate_repair(validator, args.manifest_sha256)
    if args.validate_only:
        print(json.dumps({"status": "validated", "original_admissions": completed, "repair_manifest_sha256": args.manifest_sha256,
                          "substitutions": ["ah1/reverse", "ah2/reverse"], "new_research_loops": 0}))
        return
    require(args.output is not None and args.output.is_absolute(), "absolute output directory required")
    require(not any(p.is_symlink() for p in [args.output, *args.output.parents]), "linked output path")
    out = args.output.resolve()
    require(not out.exists() and not out.is_relative_to(ROOT), "fresh external output required")
    out.mkdir(parents=True)
    receipt = {"schema": "ym28-portable-replay-receipt-v1", "status": "running", "optimized": args.optimized,
               "repair_only": args.repair_only, "original_admissions_validated": completed, "new_research_loops": 0,
               "runner_sha256": digest(Path(__file__)), "repair_manifest_sha256": args.manifest_sha256,
               "checks": []}
    try:
        for loop in completed:
            for side in ("forward", "reverse"):
                replacement = side == "reverse" and loop in LOOPS
                if args.repair_only and not replacement:
                    continue
                script = REPAIR + f"{loop}/check.py" if replacement else PREFIX + f"{side}/{loop}/check.py"
                stored_name = REPAIR + f"{loop}/expected/results.json" if replacement else PREFIX + f"{side}/{loop}/output/results.json"
                stored = validator.source(stored_name)
                destination = out / f"{loop}-{side}"
                command = [sys.executable, "-B"] + (["-O"] if args.optimized else []) + [
                    str(validator.source(script)), "--output", str(destination)]
                result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
                log = out / f"{loop}-{side}.log"
                log.write_text(result.stdout + result.stderr)
                entry = {"loop": loop, "side": side, "portable_replacement": replacement, "command": command,
                         "script_sha256": digest(validator.source(script)), "exit_code": result.returncode, "log_sha256": digest(log)}
                receipt["checks"].append(entry)
                require(result.returncode == 0, "producer failed: " + str(log))
                evidence = next(x for x in admissions[loop]["producer_evidence"] if x["side"] == side)
                replay_artifacts(destination, stored.parent, evidence["output_artifacts"])
                fresh = destination / "results.json"
                require(fresh.read_bytes() == stored.read_bytes(), "complete producer replay differs: " + loop + "/" + side)
                entry["results_sha256"] = digest(fresh)
                entry["output_artifacts"] = evidence["output_artifacts"]
        require(sum(x["portable_replacement"] for x in receipt["checks"]) == 2, "replacement count changed")
        require(len(receipt["checks"]) == (2 if args.repair_only else 20), "producer execution count changed")
        receipt["status"] = "passed"
    except Exception as error:
        receipt["status"] = "failed"
        receipt["failure"] = str(error)
        raise
    finally:
        path = out / "receipt.json"
        path.write_text(json.dumps(receipt, indent=2) + "\n")
        (out / "receipt.sha256").write_text(digest(path) + "  receipt.json\n")
        print(json.dumps({"status": receipt["status"], "producer_executions": len(receipt["checks"]), "receipt_sha256": digest(path)}))


if __name__ == "__main__":
    main()
