#!/usr/bin/env python3
"""Build the Round33 addendum only after all eight scientific gates exist.

Round33: three research sub-rounds (BA1/BA2, BB1/BB2, BC1/BC2) and the
applications stage (BD1/BD2). --check verifies the recorded source inventory
and PDF digest; it also refuses before the eight gates exist.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ROUND = ROOT / "research/round33"
LOOPS = ("ba1", "ba2", "bb1", "bb2", "bc1", "bc2", "bd1", "bd2")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def collect_sources() -> list[Path]:
    required = []
    for loop in LOOPS:
        gate = ROUND / "advisor" / (loop + "-gate.json")
        if not gate.is_file():
            raise SystemExit("Refusing completed-paper build: missing " + str(gate.relative_to(ROOT)))
        data = json.loads(gate.read_text())
        if not data.get("verdict"):
            raise SystemExit("Missing reviewed verdict: " + str(gate))
        for relative, expected in data.get("bindings", {}).items():
            path = ROOT / relative
            if not path.is_file() or sha(path) != expected:
                raise SystemExit("Scientific gate binding mismatch: " + relative)
            required.append(path)
        required.extend([gate, ROUND / "contracts" / (loop + ".json")])
        for direction in data.get("producers", ("forward", "reverse")):
            folder = ROUND / direction / loop
            required.extend([folder / "report.md", folder / "freeze.json"])
            required.extend(p for p in folder.rglob("*") if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc")
        required.extend(p for p in (ROUND / "skeptic").glob(loop + "*") if p.is_file())
    required.extend(p for p in (ROUND / "experts").rglob("*") if p.is_file() and p.suffix in {".md", ".json"})
    required.append(ROUND / "advisor/roadmap.json")
    required.extend([HERE / "main.tex", HERE / "build.py"])
    required.extend(p for p in HERE.rglob("*.tex") if "tmp" not in p.relative_to(HERE).parts)
    required.extend(HERE.glob("*.py"))
    required.extend(HERE.glob("*.bib"))
    for path in required:
        if not path.is_file():
            raise SystemExit("Missing manuscript dependency: " + str(path.relative_to(ROOT)))
    return sorted(set(required))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Check the recorded source and PDF inventory without rebuilding")
    parser.add_argument("--render", action="store_true", help="Render all pages for visual inspection")
    args = parser.parse_args()
    sources = collect_sources()
    inventory = {str(p.relative_to(ROOT)): sha(p) for p in sources}
    receipt_path = HERE / "build-receipt.json"
    if args.check:
        receipt = json.loads(receipt_path.read_text())
        if receipt["scientific_and_authoring_sources"] != inventory:
            raise SystemExit("Source inventory mismatch")
        if receipt["pdf_sha256"] != sha(HERE / "main.pdf"):
            raise SystemExit("PDF hash mismatch")
        print("Source inventory and PDF digest match")
        return
    env = os.environ.copy()
    env.update({"SOURCE_DATE_EPOCH": "1790035200", "FORCE_SOURCE_DATE": "1", "TZ": "UTC"})
    tmp = HERE / "tmp/pdfs"
    tmp.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "-outdir=" + str(tmp), "main.tex"], cwd=HERE, env=env, text=True, capture_output=True)
    (tmp / "build-output.txt").write_text(proc.stdout + proc.stderr)
    if proc.returncode:
        raise SystemExit(proc.stdout[-8000:] + proc.stderr[-2000:])
    pdf = HERE / "main.pdf"
    pdf.write_bytes((tmp / "main.pdf").read_bytes())
    subprocess.run(["pdftotext", "-layout", str(pdf), str(tmp / "main.txt")], check=True)
    info = subprocess.check_output(["pdfinfo", str(pdf)], text=True)
    (tmp / "pdfinfo.txt").write_text(info)
    receipt = {
        "schema": "hnm-round33-addendum-build-v1",
        "gate_requirement": "All eight Round33 reviewed verdicts (BA1-BD2) and their bindings must exist before manuscript build",
        "source_date_epoch": env["SOURCE_DATE_EPOCH"],
        "scientific_and_authoring_sources": inventory,
        "pdf_sha256": sha(pdf),
        "visual_qa": "Separate qa.json records actual rendered-page inspection; compilation is not visual verification",
    }
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    if args.render:
        subprocess.run(["pdftoppm", "-r", "110", "-png", str(pdf), str(tmp / "page")], check=True)
    print(info)
    print("PDF SHA256", receipt["pdf_sha256"])


if __name__ == "__main__":
    main()
