#!/usr/bin/env python3
"""Render every PDF page and report geometric and build issues for visual review."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import fitz
from PIL import Image, ImageDraw

def main():
    p = argparse.ArgumentParser()
    p.add_argument('pdf', type=Path)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    a.output.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(a.pdf)
    records = []
    previews = []
    for i, page in enumerate(doc):
        image_path = a.output / f'page-{i+1:03}.png'
        page.get_pixmap(matrix=fitz.Matrix(1, 1), alpha=False).save(image_path)
        previews.append(image_path)
        outside = []
        for block in page.get_text('dict')['blocks']:
            if block.get('type') != 0:
                continue
            for line in block['lines']:
                for span in line['spans']:
                    x0, y0, x1, y1 = span['bbox']
                    if x0 < -1 or y0 < -1 or x1 > page.rect.width+1 or y1 > page.rect.height+1:
                        outside.append(span['text'])
        text = page.get_text()
        records.append({'page': i+1, 'characters': len(text),
                        'text_outside_page': outside,
                        'unresolved_reference_tokens': text.count('??')})
    sheets = []
    for start in range(0, len(previews), 12):
        sheet = Image.new('RGB', (1800, 2700), '#d6dce1')
        draw = ImageDraw.Draw(sheet)
        for j, path in enumerate(previews[start:start+12]):
            im = Image.open(path).convert('RGB')
            im.thumbnail((570, 625))
            x = (j % 3) * 600 + (600-im.width)//2
            y = (j // 3) * 675 + 30
            draw.text((j%3*600+24, j//3*675+9), f'Page {start+j+1}', fill='black')
            sheet.paste(im, (x,y))
        path = a.output / f'contact-{start+1:03}-{min(start+12,len(previews)):03}.png'
        sheet.save(path)
        sheets.append(str(path))
    log = a.pdf.with_suffix('.log')
    logtext = log.read_text(errors='replace') if log.is_file() else ''
    result = {'scope': 'PDF render, geometry and compilation diagnostics, not mathematical verification',
              'pdf_sha256': hashlib.sha256(a.pdf.read_bytes()).hexdigest(),
              'page_count': len(doc), 'rendered_pages': len(previews),
              'overfull_boxes': len(re.findall(r'Overfull \\[hv]box', logtext)),
              'unresolved_build_warnings': bool(re.search(r'There were undefined|Citation .+ undefined|Reference .+ undefined', logtext)),
              'contact_sheets': sheets, 'pages': records}
    (a.output / 'pdf-diagnostics.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k != 'pages'}, indent=2))
    if any(r['text_outside_page'] or r['unresolved_reference_tokens'] for r in records):
        raise SystemExit('Inspect flagged page geometry/references')

if __name__ == '__main__':
    main()
