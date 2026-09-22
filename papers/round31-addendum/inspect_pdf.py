#!/usr/bin/env python3
"""Record geometry and TeX-reference diagnostics; visual review remains manual."""
from pathlib import Path
import hashlib
import json
import re
import fitz

HERE = Path(__file__).resolve().parent
pdf = HERE / "main.pdf"
log_path = HERE / "tmp/pdfs/main.log"
text = log_path.read_text(errors="replace")
outside = []
page_records = []
with fitz.open(pdf) as doc:
    for number, page in enumerate(doc, 1):
        media = page.rect
        spans = 0
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    spans += 1
                    x0, y0, x1, y1 = span["bbox"]
                    if x0 < -0.1 or y0 < -0.1 or x1 > media.width + 0.1 or y1 > media.height + 0.1:
                        outside.append({"page": number, "bbox": list(span["bbox"]), "text": span["text"]})
        page_records.append({"page": number, "width": media.width, "height": media.height, "text_spans": spans})
overfull = [line for line in text.splitlines() if "Overfull" in line]
undefined = [line for line in text.splitlines() if re.search(r"undefined|Rerun to get|Rerun to get outlines", line, re.I)]
result = {
    "schema": "hnm-round31-addendum-geometry-v1",
    "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
    "page_count": len(page_records),
    "pages": page_records,
    "all_page_geometry_checked": True,
    "geometry": {"out_of_media_text": outside},
    "overfull_warnings": overfull,
    "reference_warnings": undefined,
    "references_resolved": not undefined,
    "visual_review": "not performed by this script",
}
(HERE / "tmp/pdfs/geometry.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
if outside or overfull or undefined:
    raise SystemExit("PDF diagnostics require review")
