#!/usr/bin/env python3
"""Build only admitted Round28 chapters; intermediate PDFs remain in scratch."""
from datetime import datetime, timezone
from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ROUND = ROOT / "research/round28"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def tex(text):
    replacements = {"\\":r"\textbackslash{}", "&":r"\&", "%":r"\%", "$":r"\$",
                    "#":r"\#", "_":r"\_", "{":r"\{", "}":r"\}", "~":r"\textasciitilde{}",
                    "^":r"\textasciicircum{}", "–":"--", "—":"---", "≤":r"$\le$", "≥":r"$\ge$"}
    return "".join(replacements.get(c,c) for c in str(text))


def admitted():
    sequence = json.loads((ROUND / "advisor/sequence.json").read_text())["loops"]
    if len(sequence) != len(set(sequence)):
        raise RuntimeError("Duplicate loop in sequence")
    records = []
    for loop in sequence:
        path = ROUND / f"advisor/{loop}-gate.json"
        if not path.exists():
            continue
        gate = json.loads(path.read_text())
        if gate.get("verdict") not in {"accepted_with_limits", "accepted_within_scope", "limited", "conditional"}:
            raise RuntimeError("Unsupported gate verdict: " + loop)
        if gate.get("loop") != loop or not gate.get("bindings"):
            raise RuntimeError("Incomplete gate: " + loop)
        for name, expected in gate["bindings"].items():
            p = (ROOT / name).resolve()
            if not p.is_relative_to(ROOT) or sha(p) != expected:
                raise RuntimeError("Gate source mismatch: " + name)
        records.append((loop, path, gate))
    return records


def prepare(records, draft):
    index_path = HERE / "loops/index.json"
    index = json.loads(index_path.read_text()) if index_path.exists() else {}
    for loop, _, _ in records:
        if loop not in index or not (HERE / f"loops/{loop}.tex").is_file():
            raise RuntimeError("Reviewed manuscript chapter not yet supplied: " + loop)
    status = ("Interim draft: " if draft else "Final scoped record: ") + f"{len(records)} of 10 requested investigations have included advisor gates."
    (HERE / "status.tex").write_text(r"\begin{center}\small\textbf{"+tex(status)+r"} Task completion is distinct from theorem completion.\end{center}"+"\n")
    (HERE / "admitted-loops.tex").write_text("".join(r"\input{loops/"+loop+"}\n" for loop,_,_ in records)
                                             or "No new mathematical result is included before its scoped gate.\n")
    rows = []
    for loop,_,gate in records:
        item = index[loop]
        rows.append(" & ".join(tex(x) for x in [loop.upper(), item["result"], item["application"], item["limitation"]])+r" \\ \addlinespace"+"\n")
    table = r"""\begingroup\small
\begin{longtable}{@{}>{\raggedright\arraybackslash}p{13mm}>{\raggedright\arraybackslash}p{52mm}>{\raggedright\arraybackslash}p{35mm}>{\raggedright\arraybackslash}p{48mm}@{}}
\toprule Loop & Admitted contribution & Possible application & Remaining limitation \\
\midrule\endhead
""" + "".join(rows) + "\\bottomrule\n\\end{longtable}\n\\endgroup\n"
    if not rows:
        table = "No accepted contribution rows are present in this interim scaffold.\n"
    (HERE / "scope-table.tex").write_text(table)
    sources = {"research/round28/experts/source-survey.md":sha(ROUND / "experts/source-survey.md"),
               "research/round28/experts/sources.json":sha(ROUND / "experts/sources.json"),
               "research/round28/advisor/cycle.json":sha(ROUND / "advisor/cycle.json"),
               "research/round28/advisor/sequence.json":sha(ROUND / "advisor/sequence.json")}
    supplement_path = ROUND / "experts/source-supplement.json"
    supplement = json.loads(supplement_path.read_text())
    for relative in ("experts/source-supplement.json", "experts/source-supplement.md",
                     "experts/feynman/stability-source-deepening.md",
                     "experts/feynman/stability-source-deepening-sources.json"):
        path = ROUND / relative
        sources[str(path.relative_to(ROOT))] = sha(path)
    for binding in supplement["input_bindings"]:
        path = (ROOT / binding["path"]).resolve()
        if not path.is_relative_to(ROOT) or sha(path) != binding["sha256"]:
            raise RuntimeError("Supplement source mismatch: " + binding["path"])
        sources[binding["path"]] = binding["sha256"]
    for loop,path,gate in records:
        sources[str(path.relative_to(ROOT))] = sha(path)
        for name,digest in gate["bindings"].items():
            if name in sources and sources[name] != digest:
                raise RuntimeError("Inconsistent source binding: " + name)
            sources[name] = digest
    # Final retrospective scope and planning are separate from the scientific
    # gates and the frozen exploratory reading counts. Bind their exact inputs.
    if len(records) == 10:
        closeout_paths = (
            "advisor/panel-progress.json", "advisor/roadmap.json",
            "advisor/problem-status-check.md", "network.json",
            "experts/panel-closeout/assessment.json",
            "experts/panel-closeout/assessment.md",
            "experts/panel-closeout/final-sources.json",
        )
        for relative in closeout_paths:
            path = ROUND / relative
            name = str(path.relative_to(ROOT))
            digest = sha(path)
            if name in sources and sources[name] != digest:
                raise RuntimeError("Inconsistent closeout binding: " + name)
            sources[name] = digest
        closeout = json.loads((ROUND / "experts/panel-closeout/final-sources.json").read_text())
        for binding in closeout["bindings"]:
            name, digest = binding["path"], binding["sha256"]
            path = (ROOT / name).resolve()
            if not path.is_relative_to(ROOT) or sha(path) != digest:
                raise RuntimeError("Closeout source mismatch: " + name)
            if name in sources and sources[name] != digest:
                raise RuntimeError("Inconsistent closeout source: " + name)
            sources[name] = digest
    provenance = {"schema":"ym28-addendum-sources-v1", "draft":draft,
                  "loops":[r[0] for r in records], "target_loops":10,"sources":sources,
                  "reading_counts":{
                      "initial":json.loads((ROUND / "experts/sources.json").read_text())["counts"],
                      "supplement_at_creation":supplement["combined_counts_at_creation"],
                      "with_additive_supplement":supplement.get(
                          "combined_counts_after_topology_reading",
                          supplement["combined_counts_at_creation"])}}
    (HERE / "source-manifest.json").write_text(json.dumps(provenance,indent=2)+"\n")
    bound = [p for p in HERE.rglob("*.tex") if p.name != "build-metadata.tex"]
    identity = hashlib.md5("".join(sha(p) for p in sorted(bound)).encode()).hexdigest()
    (HERE / "build-metadata.tex").write_text(r"\pdfinfoomitdate=1"+"\n"+r"\pdfsuppressptexinfo=15"+"\n"+r"\pdftrailerid{<"+identity+"><"+identity+">}\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft", action="store_true")
    args = parser.parse_args()
    records = admitted()
    if not args.draft and len(records) != 10:
        raise RuntimeError(f"Final build needs exactly ten admitted gates; found {len(records)}")
    if any(loop == "ag3" for loop,_,_ in records):
        subprocess.run([sys.executable,"-B",str(HERE / "plot_figures.py")],check=True)
    if any(loop == "ah1" for loop,_,_ in records):
        subprocess.run([sys.executable,"-B",str(HERE / "plot_ah1.py")],check=True)
    prepare(records,args.draft)
    work = Path(tempfile.mkdtemp(prefix="ym-round28-addendum-"))
    env = dict(os.environ)
    env["SOURCE_DATE_EPOCH"] = str(int(datetime(2026,9,22,tzinfo=timezone.utc).timestamp()))
    env["FORCE_SOURCE_DATE"] = "1"
    command = ["pdflatex","-interaction=nonstopmode","-halt-on-error","-file-line-error",
               "-output-directory",str(work),"main.tex"]
    for _ in range(2):
        result = subprocess.run(command,cwd=HERE,env=env,text=True,capture_output=True)
        (work / "compile-output.txt").write_text(result.stdout+result.stderr)
        if result.returncode:
            raise RuntimeError("LaTeX failed; see " + str(work / "compile-output.txt"))
    log = (work / "main.log").read_text()
    warnings = [line for line in log.splitlines() if any(x in line for x in ("Overfull", "undefined", "Missing character"))]
    if warnings:
        raise RuntimeError("Resolve TeX warnings: " + str(warnings))
    pdf = work / "main.pdf"
    if not args.draft:
        pdf = ROOT / "dist/ym-round28-addendum.pdf"
        shutil.copy2(work / "main.pdf",pdf)
    subprocess.run(["pdftoppm","-r","90","-png",str(pdf),str(work / "page")],check=True)
    import fitz
    document = fitz.open(pdf)
    violations = []
    full_text = ""
    for page in document:
        full_text += page.get_text()
        for word in page.get_text("words"):
            if word[0]<0 or word[1]<0 or word[2]>page.rect.width+.1 or word[3]>page.rect.height+.1:
                violations.append({"page":page.number+1,"word":word[4]})
    if violations or "??" in full_text:
        raise RuntimeError("PDF integrity check failed")
    rendered = sorted(work.glob("page-*.png"),key=lambda p:int(p.stem.split("-")[-1]))
    qa = {"schema":"ym28-addendum-pdf-qa-v1","draft":args.draft,"pages":len(document),
          "pdf":str(pdf if args.draft else pdf.relative_to(ROOT)),"sha256":sha(pdf),
          "tex_warnings":warnings,"out_of_page_words":violations,"visual_review":"required",
          "render_command":"pdftoppm -r 90 -png <pdf> <scratch>/page",
          "rendered_pages":[p.name for p in rendered]}
    record = work / "pdf-qa.json" if args.draft else HERE / "pdf-qa.json"
    record.write_text(json.dumps(qa,indent=2)+"\n")
    print(json.dumps({"pdf":str(pdf),"pages":len(document),"draft":args.draft,
                      "qa":str(record),"render_directory":str(work)}))


if __name__ == "__main__":
    main()
