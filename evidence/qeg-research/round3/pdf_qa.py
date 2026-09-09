#!/usr/bin/env python3
"""Render page overviews and inspect PDF structure; visual acceptance is separate."""
import argparse
import json
from pathlib import Path

import fitz
from PIL import Image, ImageDraw


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--pages", default="")
    args = parser.parse_args()
    target = args.pdf.resolve()
    out = Path(__file__).resolve().parent / "tmp" / "pdfs"
    out.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(target)
    errors, overflow, sparse, thumbnails = [], [], [], []
    markers = ["Equation rendering unavailable", "Table could not be rendered", "Missing figure:", "Unreadable figure:", "\ufffd"]
    for index, page in enumerate(doc):
        txt = page.get_text()
        for marker in markers:
            if marker in txt:
                errors.append({"page": index + 1, "marker": marker})
        for block in page.get_text("dict")["blocks"]:
            x0, y0, x1, y1 = block["bbox"]
            if x0 < -0.5 or y0 < -0.5 or x1 > page.rect.width + 0.5 or y1 > page.rect.height + 0.5:
                overflow.append({"page": index + 1, "bbox": block["bbox"]})
        if len(txt.strip()) < 110 and index > 0:
            sparse.append({"page": index + 1, "text": txt.strip()[:150], "images": len(page.get_images())})
        pix = page.get_pixmap(matrix=fitz.Matrix(0.42, 0.42), alpha=False)
        image = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        thumbnails.append(image)
    sheets = []
    for start in range(0, len(thumbnails), 20):
        group = thumbnails[start:start + 20]
        tw, th = group[0].size
        rows = (len(group) + 3) // 4
        sheet = Image.new("RGB", (4 * (tw + 16), rows * (th + 28)), "#d9dde2")
        draw = ImageDraw.Draw(sheet)
        for j, image in enumerate(group):
            x, y = (j % 4) * (tw + 16) + 8, (j // 4) * (th + 28) + 20
            sheet.paste(image, (x, y))
            draw.text((x, y - 16), f"Page {start + j + 1}", fill="black")
        path = out / f"contact_{start+1:03d}.png"
        sheet.save(path)
        sheets.append(str(path))
    selected = [int(x) for x in args.pages.split(",") if x]
    for number in selected:
        if 1 <= number <= len(doc):
            doc[number-1].get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False).save(str(out / f"page_{number:03d}.png"))
    summary = {"pdf": str(target), "page_count": len(doc), "rendering_error_markers": errors,
               "page_bound_overflows": overflow, "sparse_pages_for_review": sparse,
               "contact_sheets": sheets, "high_resolution_pages_rendered": selected,
               "visual_review_completed": False}
    (out / "automated_pdf_qa.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
