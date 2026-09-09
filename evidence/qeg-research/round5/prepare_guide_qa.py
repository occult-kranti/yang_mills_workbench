#!/usr/bin/env python3
"""Render all PDF pages for a required human/agent visual inspection.

Generates contact sheets and a text/bounds audit. This script does not assert
visual acceptance; write visual_qa.json only after reviewing the images.
"""
import hashlib,json,subprocess
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parent
pdf=ROOT/'output/pdf/bidirectional-proof-dossier.pdf'
out=ROOT/'tmp/guide-qa'; out.mkdir(parents=True,exist_ok=True)
for pattern in ['page-*.png', 'contact-*.png', 'full-*.png']:
    for stale in out.glob(pattern): stale.unlink()
subprocess.run(['/usr/bin/pdftoppm','-r','65','-png',str(pdf),str(out/'page')],check=True)
pages=sorted(out.glob('page-*.png'))
contact=[]
for start in range(0,len(pages),16):
    batch=pages[start:start+16]
    sheet=Image.new('RGB',(1160,1680),'#e5e7eb'); draw=ImageDraw.Draw(sheet)
    for i,path in enumerate(batch):
        im=Image.open(path).convert('RGB'); im.thumbnail((270,382))
        x=(i%4)*290+(290-im.width)//2;y=(i//4)*420+24
        sheet.paste(im,(x,y));draw.text(((i%4)*290+12,(i//4)*420+7),f'Page {start+i+1}',fill='black')
    dest=out/f'contact-{start+1:02d}-{start+len(batch):02d}.png';sheet.save(dest);contact.append(str(dest.relative_to(ROOT)))
reader=PdfReader(pdf)
texts=[p.extract_text() or '' for p in reader.pages]
problems=[]
for i,txt in enumerate(texts,1):
    for token in ['Equation rendering unavailable','Table could not be rendered','[Missing figure:', '[Unreadable figure:','\ufffd']:
        if token in txt:problems.append({'page':i,'token':token})
    if len(txt.strip())<30:problems.append({'page':i,'kind':'very_little_extracted_text','characters':len(txt.strip())})
alltext='\n'.join(texts)
(ROOT/'tmp/guide-qa/extracted.txt').write_text(alltext)
report={'pdf':str(pdf.relative_to(ROOT)),'sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'pages':len(reader.pages),'rendered_pages':len(pages),'contact_sheets':contact,'extracted_text_problems':problems,'outline_entries':len(reader.outline),'visual_review':'pending: inspect contact sheets and selected full-resolution pages'}
(ROOT/'guide_pdf_precheck.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
