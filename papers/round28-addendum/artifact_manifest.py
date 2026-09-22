#!/usr/bin/env python3
"""Bind the reviewed final Round28 artifact; never promotes scientific results."""
from pathlib import Path
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
MANIFEST = HERE / "artifact-manifest.json"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validated_sources():
    record = json.loads((HERE / "source-manifest.json").read_text())
    if record["draft"] or len(record["loops"]) != 10 or len(set(record["loops"])) != 10:
        raise RuntimeError("Final artifact requires ten distinct admitted gates")
    for name, digest in record["sources"].items():
        path = (ROOT / name).resolve()
        if not path.is_relative_to(ROOT) or sha(path) != digest:
            raise RuntimeError("Source hash mismatch: " + name)
    return record


def current_record():
    sources = validated_sources()
    pdf = ROOT / "dist/ym-round28-addendum.pdf"
    qa = json.loads((HERE / "pdf-qa.json").read_text())
    if qa["draft"] or qa["sha256"] != sha(pdf) or qa["visual_review"] != "passed":
        raise RuntimeError("The final PDF still needs a matching all-page visual review")
    if qa["tex_warnings"] or qa["out_of_page_words"]:
        raise RuntimeError("Unresolved PDF integrity defect")
    if qa.get("visually_reviewed_pages") != list(range(1,qa["pages"]+1)):
        raise RuntimeError("All final pages must be recorded as visually reviewed")
    allowed_suffixes = {".py", ".tex", ".md", ".json", ".png", ".pdf", ".csv"}
    files = [p for p in HERE.rglob("*") if p.is_file() and p != MANIFEST]
    for p in files:
        if p.name != ".gitignore" and p.suffix not in allowed_suffixes:
            raise RuntimeError("Unexpected generated artifact: " + str(p.relative_to(ROOT)))
        if "__pycache__" in p.parts:
            raise RuntimeError("Interpreter cache must not be part of artifact")
    files.append(pdf)
    return {"schema":"ym28-addendum-artifacts-v1", "pdf":str(pdf.relative_to(ROOT)),
            "pages":qa["pages"], "loops":sources["loops"],
            "artifacts":{str(p.relative_to(ROOT)):sha(p) for p in sorted(files)},
            "scope":"Ten reviewed workbench investigations; no percentage of theorem completion."}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check",action="store_true")
    args = parser.parse_args()
    record = current_record()
    if args.check:
        if json.loads(MANIFEST.read_text()) != record:
            raise RuntimeError("Artifact manifest differs from reviewed files")
    else:
        MANIFEST.write_text(json.dumps(record,indent=2)+"\n")
    print(json.dumps({"manifest":str(MANIFEST.relative_to(ROOT)),
                      "artifacts":len(record["artifacts"]),"verified":args.check}))


if __name__ == "__main__":
    main()
