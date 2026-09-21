"""Replay frozen producers and verify submitted sources, without trusting status."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("loop")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    need(args.output.is_absolute() and not args.output.exists(), "fresh absolute replay output required")
    need(ROOT not in args.output.parents, "replay outputs must be external to checkout")
    args.output.mkdir(parents=True)
    contract_path = ROOT / "research/round24/contracts" / (args.loop + ".json")
    contract = json.loads(contract_path.read_text())
    summaries = {}
    for direction in ("forward", "reverse"):
        base = ROOT / "research/round24" / direction / args.loop
        submission = json.loads((base / "submission.json").read_text())
        for name, sha in submission["files"].items():
            need(digest(ROOT / name) == sha, "submitted source changed: " + name)
        for name in (*contract.get("dependencies", {}), *contract.get("instruction_inputs", {})):
            need(name in submission["files"], "missing required bound input: " + name)
        need(str(contract_path.relative_to(ROOT)) in submission["files"], "missing contract binding")
        outputs = []
        for mode, flags in (("normal", []), ("optimized", ["-O"])):
            dest = args.output / (direction + "-" + mode)
            run = subprocess.run([sys.executable, "-B", *flags, str(base / "check.py"), "--output", str(dest)],
                                 cwd=ROOT, text=True, capture_output=True)
            need(run.returncode == 0, direction + " replay failed: " + run.stderr)
            for filename in ("results.json", "controls.json"):
                need((dest / filename).is_file(), "missing replay output")
                need((dest / filename).read_bytes() == (base / "output" / filename).read_bytes(),
                     "replay differs from frozen output: " + direction + "/" + filename)
            controls = json.loads((dest / "controls.json").read_text())["controls"]
            need(sum(type(v) is bool and v for v in controls.values()) >= 3, "insufficient boolean controls")
            need(all(type(v) is bool and v for v in controls.values()), "a control is not true boolean")
            outputs.append({"mode": mode, "path": str(dest), "exit_code": run.returncode,
                            "results_sha256": digest(dest / "results.json"),
                            "controls_sha256": digest(dest / "controls.json")})
        summaries[direction] = {"submission_sha256": digest(base / "submission.json"),
                                "source_count": len(submission["files"]),
                                "controls": list(controls), "replays": outputs}
    out = ROOT / "research/round24/skeptic" / (args.loop + "-replay.json")
    out.write_text(json.dumps({"loop": args.loop, "status": "passed",
        "contract_sha256": digest(contract_path), "external_peer_review": False,
        "directions": summaries}, indent=2, sort_keys=True) + "\n")
    print(str(out.relative_to(ROOT)) + ": passed")


if __name__ == "__main__":
    main()
