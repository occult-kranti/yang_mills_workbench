#!/usr/bin/env python3
"""Render current manuscript pages and record geometry, without claiming image inspection."""
from pathlib import Path
import argparse
import hashlib
import json
import fitz
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[3]
PAPER = ROOT / 'papers/draft-03'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def parse_pages(text):
    pages = set()
    for piece in filter(None, text.split(',')):
        if '-' in piece:
            lo, hi = map(int, piece.split('-'))
            pages.update(range(lo, hi + 1))
        else:
            pages.add(int(piece))
    return sorted(pages)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pages', default='auto', help='Physical PDF page numbers, e.g. 1-10,170-220; auto covers all changed and representative old pages')
    parser.add_argument('--dpi', type=int, default=110)
    parser.add_argument('--output', type=Path, default=ROOT.parent / 'draft03-qa-render', help='Transient page images; kept outside the Git source tree by default')
    args = parser.parse_args()
    pdf = PAPER / 'main.pdf'
    qa_path = PAPER / 'pdf-qa.json'
    qa = json.loads(qa_path.read_text())
    if sha(pdf) != qa['pdf_sha256']:
        raise ValueError('QA describes a different PDF')
    labels = json.loads((PAPER / 'build-pages.json').read_text())['all_labels']
    document = fitz.open(pdf)
    total = len(document)
    if args.pages == 'auto':
        # Arabic pagination begins on the physical title page in this manuscript.
        first_history = labels['sec:introduction']
        first_new = min(labels['stmt:AQ2'], labels['sec:round30-overview'])
        end_changed = labels['app:history']
        selected = set(range(1, first_history + 1))
        selected.update(range(first_new - 1, end_changed + 1))
        selected.update(range(labels['app:reproduction'], total + 1))
        selected.update(range(first_history, first_new, 16))
        selected.update([total])
        pages = sorted(selected)
    else:
        pages = parse_pages(args.pages)
    if not pages or min(pages) < 1 or max(pages) > total:
        raise ValueError('Invalid rendering page range')

    geometry = []
    violations = []
    blank = []
    for number, page in enumerate(document, 1):
        words = page.get_text('words')
        if not words:
            blank.append(number)
        boxes = [tuple(word[:4]) for word in words]
        outside = [box for box in boxes if box[0] < -0.5 or box[1] < -0.5 or box[2] > page.rect.width + 0.5 or box[3] > page.rect.height + 0.5]
        if outside:
            violations.append({'page': number, 'boxes': outside})
        geometry.append({'page': number, 'width_pt': round(page.rect.width, 3), 'height_pt': round(page.rect.height, 3),
                         'word_count': len(words), 'out_of_media_words': len(outside)})
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    for number in pages:
        document[number - 1].get_pixmap(dpi=args.dpi, alpha=False).save(out / f'page-{number:03d}.png')

    sheets = []
    thumb_w, thumb_h, gutter = 650, 920, 24
    for offset in range(0, len(pages), 4):
        group = pages[offset:offset + 4]
        sheet = Image.new('RGB', (2 * thumb_w + 3 * gutter, 2 * (thumb_h + 30) + 3 * gutter), '#dce1e6')
        draw = ImageDraw.Draw(sheet)
        for pos, number in enumerate(group):
            image = Image.open(out / f'page-{number:03d}.png').convert('RGB')
            image.thumbnail((thumb_w, thumb_h))
            x, y = gutter + (pos % 2) * (thumb_w + gutter), gutter + (pos // 2) * (thumb_h + 30 + gutter)
            draw.text((x, y), f'Physical PDF page {number}', fill='black')
            sheet.paste(image, (x, y + 25))
        filename = f'sheet-{offset // 4 + 1:03d}.png'
        sheet.save(out / filename)
        sheets.append({'image': str(out / filename), 'sha256': sha(out / filename), 'pages': group})

    qa.update(page_count=total, pages=total, rendered_pages=pages, all_page_geometry_checked=True,
              geometry={'pages_checked': total, 'out_of_media_text': violations, 'blank_pages': blank,
                        'method': 'PyMuPDF word rectangles compared with each PDF MediaBox; layout overlap still requires visual inspection.'},
              rendered_contact_sheets=sheets, rendering_dpi=args.dpi,
              rendering_note='Transient images are reproducible with editorial/pdf_review.py and are not required in the release source bundle.',
              status='rendered_awaiting_visual_review', visual_review='pending',
              inspected_pages=[], full_size_inspected_pages=[],
              coverage='All PDF pages received geometry checks. Listed pages were rendered; this script makes no claim to have visually inspected those images.')
    (PAPER / 'page-geometry.json').write_text(json.dumps({'pdf_sha256': sha(pdf), 'pages': geometry}, indent=2) + '\n')
    qa_path.write_text(json.dumps(qa, indent=2) + '\n')
    print(json.dumps({'pages': total, 'rendered_pages': len(pages), 'contact_sheets': len(sheets), 'out_of_media_pages': len(violations), 'blank_pages': blank}))

if __name__ == '__main__':
    main()
