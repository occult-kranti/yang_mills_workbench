"""Verify one clean detached Round27 Git tree; keep receipts outside that tree.

This is a targeted release: the six current producers, current skeptic checks,
their source bindings, the new page and nearby UI regressions. It does not rerun
the historical research program or confer external peer review.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
BASE = "9b5a41d"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def inventory(directory):
    require(directory.is_dir(), "missing generated subtree: " + str(directory))
    result = {}
    for path in sorted(directory.rglob("*")):
        require(not path.is_symlink(), "linked file in release subtree: " + str(path))
        if path.is_file():
            result[str(path.relative_to(ROOT))] = digest(path)
    return result


def committed_inventory(relative):
    """Start from the committed file set, so ignored extras cannot be a baseline."""
    expected = git("ls-tree", "-r", "--name-only", "HEAD", "--", relative).splitlines()
    require(bool(expected), "empty committed subtree: " + relative)
    actual = inventory(ROOT / relative)
    require(set(actual) == set(expected), "uncommitted/missing files in subtree: " + relative)
    # The clean-tree precondition establishes tracked-byte equality; the exact
    # set check additionally excludes ignored caches and stale build products.
    return actual


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--expected-commit", required=True)
    parser.add_argument("--expected-tree", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    require(args.output.is_absolute(), "absolute receipt directory required")
    out = args.output.resolve()
    require(not out.exists() and not out.is_relative_to(ROOT), "fresh external receipt directory required")
    require(re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", args.expected_commit), "full commit ID required")
    require(re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", args.expected_tree), "full tree ID required")
    require(git("rev-parse", "HEAD") == args.expected_commit, "candidate commit mismatch")
    require(git("rev-parse", "HEAD^{tree}") == args.expected_tree, "candidate tree mismatch")
    require(git("rev-parse", "--abbrev-ref", "HEAD") == "HEAD", "fresh detached worktree required")
    require(not git("status", "--porcelain", "--untracked-files=all"), "candidate must start clean")
    baseline = git("rev-parse", BASE + "^{commit}")
    changed = git("diff", "--name-only", baseline, "HEAD", "--", "research", "evidence", "papers/draft-01").splitlines()
    require(all(name.startswith("research/round27/") for name in changed),
            "historical science or draft-01 bytes changed since base " + BASE)
    out.mkdir(parents=True)
    checks = []
    receipt = {"status": "running", "commit": args.expected_commit, "tree": args.expected_tree,
               "baseline": baseline, "checks": checks,
               "scope": "exact-tree source integrity, six producer normal/optimized replays, current skeptic reruns, deterministic build and targeted UI",
               "review": "separate model-agent mathematical review; no external peer review or formal continuum proof"}

    def run(name, command):
        result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
        logfile = out / (name + ".log")
        logfile.write_text(result.stdout + result.stderr)
        checks.append({"name": name, "command": command, "exit_code": result.returncode,
                       "log": str(logfile), "log_sha256": digest(logfile)})
        require(result.returncode == 0, "failed " + name + "; see " + str(logfile))
        print(name + ": passed", flush=True)

    try:
        sys.path.insert(0, str(ROOT / "research/round27"))
        import reproduce as admission
        loops = admission.sequence()
        require(len(loops) == 3, "three-loop release required")
        for index, loop in enumerate(loops):
            admission.validate(loop, index + 1, loops[index - 1] if index else None)
        receipt["loops"] = loops
        before_research = committed_inventory("research/round27")
        before_dist = committed_inventory("dist")
        before_docs = committed_inventory("docs")
        for optimized in [False, True]:
            mode = "optimized" if optimized else "normal"
            py = [sys.executable, "-B"] + (["-O"] if optimized else [])
            run("round27-" + mode, py + ["research/round27/reproduce.py", "--output", str(out / ("replay-" + mode))]
                + (["--optimized"] if optimized else []))
            run("admission-mutations-" + mode, py + ["research/round27/test_admission.py"])
        receipt["producer_executions"] = 12
        receipt["new_research_loops"] = 3
        receipt["additional_research_loops_in_release"] = 0
        # Current independent checkers declare fixed, deterministic local JSON
        # destinations. Capture their pre-run bytes and require equality. This
        # runs only their documented entry points, never a historical suite.
        skeptic_runs = []
        for loop in loops:
            skeptic = ROOT / "research/round27/skeptic"
            entrypoints = [(loop + "_independent.py", loop + "-independent.json", "independent")]
            if (skeptic / (loop + "_compare.py")).is_file():
                entrypoints.append((loop + "_compare.py", loop + "-comparison.json", "comparison"))
            review = admission.load("research/round27/skeptic/" + loop + ".json")
            for script_name, output_name, kind in entrypoints:
                script, output = skeptic / script_name, skeptic / output_name
                require(script.is_file(), "missing documented skeptic checker: " + script_name)
                require(output.is_file(), "missing recorded skeptic output: " + output_name)
                require({str(script.relative_to(ROOT)), str(output.relative_to(ROOT))} <= review["bindings"].keys(),
                        "skeptic entrypoint/output not bound by its review: " + script_name)
                expected = output.read_bytes()
                for optimized in [False, True]:
                    mode = "optimized" if optimized else "normal"
                    command = [sys.executable, "-B"] + (["-O"] if optimized else []) + [str(script)]
                    run("skeptic-" + loop + "-" + kind + "-" + mode, command)
                    require(output.read_bytes() == expected, "skeptic output changed: " + script_name + "/" + mode)
                    skeptic_runs.append({"loop": loop, "kind": kind, "optimized": optimized, "results_sha256": digest(output)})
        receipt["skeptic_replays"] = skeptic_runs
        network = ROOT / "research/round27/network.json"
        data = ROOT / "dist/research-round27-data.js"
        require(network.is_file() and data.is_file(), "committed generated Round27 artifacts missing")
        network.unlink()
        data.unlink()
        shutil.rmtree(ROOT / "docs")
        run("round27-build", [sys.executable, "-B", "research/round27/build_site.py"])
        run("pages-build", ["npm", "run", "build"])
        require(inventory(ROOT / "research/round27") == before_research, "Round27 subtree differs after replay/build")
        require(inventory(ROOT / "dist") == before_dist, "dist subtree differs after fresh build")
        require(inventory(ROOT / "docs") == before_docs, "docs subtree differs after fresh build")
        receipt["generated_subtree_file_counts"] = {"round27": len(before_research), "dist": len(before_dist), "docs": len(before_docs)}
        ui_tests = ["test_round27", "test_round26", "test_round25", "test_workbench", "test_ui"]
        ui_tests += [p.stem for p in sorted((ROOT / "tests").glob("*draft*.mjs"))]
        for name in dict.fromkeys(ui_tests):
            script = ROOT / "tests" / (name + ".mjs")
            require(script.is_file(), "required targeted UI test missing: " + name)
            run(name, ["node", str(script)])
        require(not git("status", "--porcelain", "--untracked-files=all"), "verification changed candidate tree")
        require(git("rev-parse", "HEAD") == args.expected_commit and git("rev-parse", "HEAD^{tree}") == args.expected_tree,
                "candidate identity changed during verification")
        receipt["status"] = "passed"
        receipt["clean_before_and_after"] = True
    except Exception as error:
        receipt["status"] = "failed"
        receipt["failure"] = str(error)
        receipt["final_git_status"] = git("status", "--porcelain", "--untracked-files=all")
        raise
    finally:
        path = out / "receipt.json"
        path.write_text(json.dumps(receipt, indent=2) + "\n")
        checksum = digest(path)
        (out / "receipt.sha256").write_text(checksum + "  receipt.json\n")
        print(json.dumps({"status": receipt["status"], "receipt": str(path), "receipt_sha256": checksum}), flush=True)


if __name__ == "__main__":
    main()
