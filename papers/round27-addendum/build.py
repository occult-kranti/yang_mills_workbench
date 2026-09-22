#!/usr/bin/env python3
"""Compile the additive manuscript; no physics production files are modified."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    sequence = json.loads((ROOT / "research/round27/advisor/sequence.json").read_text())
    if sequence.get("loops") != ["ai1", "ai2", "ag1"]:
        raise RuntimeError("The manuscript requires the final AI1, AI2, AG1 sequence")
    for loop in sequence["loops"]:
        gate = json.loads((ROOT / f"research/round27/advisor/{loop}-gate.json").read_text())
        if gate.get("verdict") not in ("accepted_with_limits", "accepted_within_scope", "limited", "conditional"):
            raise RuntimeError(f"Final scoped gate missing: {loop}")
    subprocess.run([sys.executable, "-B", str(HERE / "plot_round27.py")], cwd=HERE, check=True)
    build = HERE / "build"
    build.mkdir(exist_ok=True)
    env = dict(os.environ)
    env["SOURCE_DATE_EPOCH"] = str(int(datetime(2026,9,22,tzinfo=timezone.utc).timestamp()))
    env["FORCE_SOURCE_DATE"] = "1"
    command = ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error",
               "-output-directory", str(build), "round27-addendum.tex"]
    for _ in range(2):
        result = subprocess.run(command, cwd=HERE, env=env, text=True, capture_output=True)
        (build / "compile-output.txt").write_text(result.stdout + result.stderr)
        if result.returncode:
            raise RuntimeError("LaTeX compilation failed; inspect build/compile-output.txt")
    final = ROOT / "dist/ym-round27-addendum.pdf"
    shutil.copy2(build / "round27-addendum.pdf", final)
    log = (build / "round27-addendum.log").read_text()
    defects = [line for line in log.splitlines()
               if "Overfull" in line or "undefined" in line.lower() or "Missing character" in line]
    if defects:
        raise RuntimeError("Resolve TeX warnings: " + repr(defects))
    for old_page in build.glob("page-*.png"):
        if old_page.stem.removeprefix("page-").isdigit():
            old_page.unlink()
    subprocess.run(["pdftoppm", "-r", "90", "-png", str(final), str(build / "page")], check=True)
    import fitz
    document = fitz.open(final)
    violations = []
    text = ""
    for page in document:
        text += page.get_text()
        for word in page.get_text("words"):
            if word[0] < 0 or word[1] < 0 or word[2] > page.rect.width+.1 or word[3] > page.rect.height+.1:
                violations.append({"page": page.number+1, "word": word[4]})
    if violations or "??" in text:
        raise RuntimeError("PDF text integrity check failed")
    audit = {"schema": "ym27-addendum-pdf-qa-v1", "pages": len(document),
             "pdf": str(final.relative_to(ROOT)),
             "sha256": hashlib.sha256(final.read_bytes()).hexdigest(),
             "tex_overfull_or_undefined_warnings": defects,
             "out_of_page_words": violations,
             "visual_review": "required after the last build; not satisfied by text extraction",
             "render_command": "pdftoppm -r 90 -png dist/ym-round27-addendum.pdf papers/round27-addendum/build/page",
             "rendered_pages": [p.name for p in sorted(build.glob("page-*.png"))]}
    (HERE / "pdf-qa.json").write_text(json.dumps(audit, indent=2)+"\n")
    print(json.dumps({"pdf":str(final),"pages":len(document),"visual_review_required":True}))


if __name__ == "__main__":
    main()
