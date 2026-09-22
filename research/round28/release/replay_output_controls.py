"""Small synthetic controls for universal fresh producer output validation."""
import json
from pathlib import Path
import shutil
import sys
import tempfile

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from reproduce import digest, replay_artifacts


def run():
    rejected = []
    with tempfile.TemporaryDirectory(prefix="ym28-replay-output-") as temporary:
        root = Path(temporary)
        stored = root / "stored"
        stored.mkdir()
        (stored / "results.json").write_text('{"synthetic":true}\n')
        replay_artifacts(stored, stored, {})

        def attack(label, change, artifacts=None):
            fresh = root / label
            shutil.copytree(stored, fresh)
            destination = change(fresh) or fresh
            try:
                replay_artifacts(destination, stored, artifacts or {})
            except ValueError:
                rejected.append(label)
            else:
                raise ValueError("invalid fresh output accepted: " + label)

        def extra(fresh):
            (fresh / "extra.json").write_text('{}\n')

        def linked_result(fresh):
            (fresh / "results.json").unlink()
            (fresh / "results.json").symlink_to(stored / "results.json")

        def linked_destination(fresh):
            shutil.rmtree(fresh)
            fresh.symlink_to(stored, target_is_directory=True)

        def linked_ancestor(fresh):
            link = root / "linked-parent"
            link.symlink_to(root, target_is_directory=True)
            return link / fresh.name

        def empty_cache(fresh):
            (fresh / "__pycache__").mkdir()

        def missing_result(fresh):
            (fresh / "results.json").unlink()

        def escaping_path(fresh):
            return fresh / ".." / fresh.name

        attack("single-extra-file", extra)
        attack("single-linked-result", linked_result)
        attack("single-linked-destination", linked_destination)
        attack("single-linked-ancestor", linked_ancestor)
        attack("single-empty-cache", empty_cache)
        attack("single-missing-result", missing_result)
        attack("single-escaping-path", escaping_path)

        (stored / "matrix.json").write_text('{"synthetic":[1,2]}\n')
        artifacts = {"matrix.json": digest(stored / "matrix.json")}
        replay_artifacts(stored, stored, artifacts)

        def tampered_auxiliary(fresh):
            (fresh / "matrix.json").write_text('{}\n')

        attack("auxiliary-byte-mismatch", tampered_auxiliary, artifacts)
    return {"status": "passed", "valid_output_controls": 2,
            "fresh_output_mutations_rejected": len(rejected), "controls": rejected,
            "new_research_loops": 0, "producer_executions": 0,
            "scope": "Synthetic output files only; no scientific or admission claims."}


if __name__ == "__main__":
    print(json.dumps(run(), sort_keys=True))
