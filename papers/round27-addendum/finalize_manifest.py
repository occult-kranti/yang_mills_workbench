#!/usr/bin/env python3
"""Bind the visually reviewed addendum and its exact research sources."""
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    pdf = ROOT / "dist/ym-round27-addendum.pdf"
    qa = json.loads((HERE / "pdf-qa.json").read_text())
    if qa.get("visual_review") != "passed" or qa.get("sha256") != digest(pdf):
        raise RuntimeError("Final PDF requires completed, matching visual review")
    sources = [ROOT / "research/round27/SOURCES.md",
               ROOT / "research/round27/advisor/sequence.json",
               ROOT / "research/round27/skeptic/completion-assessment.json",
               ROOT / "papers/draft-01/main.pdf"]
    for loop in ("ai1", "ai2", "ag1"):
        sources += [ROOT / f"research/round27/contracts/{loop}.json",
                    ROOT / f"research/round27/advisor/{loop}-gate.json",
                    ROOT / f"research/round27/skeptic/{loop}.md",
                    ROOT / f"research/round27/skeptic/{loop}.json"]
        for direction in ("forward", "reverse"):
            sources += [ROOT / f"research/round27/{direction}/{loop}/{part}"
                        for part in ("report.md", "output/results.json")]
    for lens in ("newton", "tesla", "jung", "penrose", "feynman"):
        sources += [ROOT / f"research/round27/experts/{lens}/{part}"
                    for part in ("report.md", "sources.json", "final-review.md")]
    sources += [ROOT / "research/round27/skeptic/ag1-independent.json",
                ROOT / "research/round27/skeptic/ag1-independent-derivation.md"]
    files = [p for p in HERE.rglob("*") if p.is_file()
             and not any(x in p.relative_to(HERE).parts for x in ("build", "__pycache__"))
             and p.name != "manifest.json"]
    files += [pdf, ROOT / "dist/ym-round27-discrimination.png", ROOT / "dist/ym-round27-contraction-bounds.png"]
    manifest = {"schema": "ym27-addendum-manifest-v1",
                "scope": "Additive manuscript; Draft01 preserved. Hashes are integrity bindings, not proof certification.",
                "files": {str(p.relative_to(ROOT)):digest(p) for p in sorted(files)},
                "research_sources": {str(p.relative_to(ROOT)):digest(p) for p in sorted(sources)}}
    (HERE / "manifest.json").write_text(json.dumps(manifest, indent=2)+"\n")
    print(json.dumps({"artifacts":len(files), "sources":len(sources)}))


if __name__ == "__main__":
    main()
