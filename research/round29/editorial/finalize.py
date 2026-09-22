#!/usr/bin/env python3
"""Bind the final manuscript and actual visual review; never modifies old evidence."""
from pathlib import Path
import argparse,hashlib,json,re
import fitz
def require(condition,message):
 if not condition:raise ValueError(message)
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'papers/draft-02'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--visual-review',required=True);ap.add_argument('--review-coverage',required=True);ap.add_argument('--reviewed-pdf-sha256',required=True);args=ap.parse_args()
 pdf=OUT/'main.pdf';require(sha(pdf)==args.reviewed_pdf_sha256, 'Visual review must match the delivered PDF.')
 review=ROOT/args.visual_review;require(review.exists(), 'Acceptance condition failed: review.exists()')
 findings=json.loads((ROOT/'research/round29/advisor/findings.json').read_text());require(len(findings['loops'])==10, "Acceptance condition failed: len(findings['loops'])==10")
 registry=json.loads((OUT/'registry/hnm-registry.json').read_text());require(registry['contribution_count']==139, "Acceptance condition failed: registry['contribution_count']==139")
 require(len(registry['contributions'])==139, "Acceptance condition failed: len(registry['contributions'])==139")
 for name in ['contributions','equations','quantities','statements']:
  ids=[x['id'] for x in registry[name]];require(len(ids)==len(set(ids)), name)
 require(registry['new_axioms_count']==0 and registry['axioms']==[], "Acceptance condition failed: registry['new_axioms_count']==0 and registry['axioms']==[]")
 by_id={x['id']:x for x in registry['contributions']}
 for item in registry['statements']:
  parent=by_id[item['contribution_id']]
  require(item['id'] in parent['statement_ids'] and item['summary']==parent['application'], "Acceptance condition failed: item['id'] in parent['statement_ids'] and item['summary']==parent['application']")
  source=OUT/'addenda/round29'/f"{item['legacy_id'].lower()}.tex"
  require(r'\label{'+item['manuscript_label']+'}' in source.read_text(), "Acceptance condition failed: r'\\label{'+item['manuscript_label']+'}' in source.read_text()")
  require((ROOT/item['gate']).exists() and item['scope']==parent['limitation'], "Acceptance condition failed: (ROOT/item['gate']).exists() and item['scope']==parent['limitation']")
 for item in registry['contributions']:
  for name in item['source_paths']:require((ROOT/name).exists(), name)
  require(item['limitation'] and item['proof_status'] and item['classification'], "Acceptance condition failed: item['limitation'] and item['proof_status'] and item['classification']")
 for item in registry['equations']:
  text=(OUT/item['source']).read_text();require(r'\label{'+item['legacy_label']+'}' in text, item)
  require(item.get('printed_locator'), item)
  require(not any(c in item['printed_locator'] for c in '{}'), item)
 historical=json.loads((OUT/'historical-inputs.json').read_text())
 for name,digest in historical['sha256'].items():require(sha(ROOT/name)==digest, f'Historical input modified: {name}')
 closeout=json.loads((OUT/'closeout-inputs.json').read_text())
 require(sha(ROOT/closeout['roadmap'])==closeout['sha256'],'Closing roadmap has changed since typesetting.')
 require(closeout['future_goals_executed']==0,'This release must not mark future goals executed.')
 for name,digest in closeout['gate_bindings'].items():require(sha(ROOT/name)==digest,'Closeout gate changed: '+name)
 projection=json.loads((OUT/'figures/round29-dependencies.json').read_text())
 require(sha(ROOT/projection['source'])==projection['source_sha256'],'Dependency figure does not bind the current canonical graph.')
 source=(OUT/'sections/round29-closeout.tex').read_text()
 for forbidden in ['not yet integrated','not a release'] :require(forbidden not in source, 'Acceptance condition failed: forbidden not in source')
 doc=fitz.open(pdf);require(doc.metadata['author']=='Hruday N M (BUNZEEY)', "Acceptance condition failed: doc.metadata['author']=='Hruday N M (BUNZEEY)'")
 coverage_path=ROOT/args.review_coverage
 require(coverage_path.exists(),'Actual visual-review coverage record is required.')
 coverage=json.loads(coverage_path.read_text())
 require(coverage.get('status')=='passed','Visual reviewer has not passed this artifact.')
 require(coverage.get('pdf_sha256')==sha(pdf),'Visual coverage belongs to another PDF.')
 require(coverage.get('page_count')==len(doc),'Visual review page count does not match.')
 reviewed_pages=coverage.get('contact_sheet_pages',[])
 require(len(reviewed_pages)==len(set(reviewed_pages)),'Duplicate visual-coverage page IDs.')
 require(sorted(reviewed_pages)==list(range(1,len(doc)+1)),'Actual contact-sheet review must cover every delivered page.')
 full_size=coverage.get('full_size_pages',[])
 require(bool(full_size) and set(full_size)<=set(reviewed_pages),'Selected full-size review is required.')
 require(bool(coverage.get('method')),'Reviewer must state the actual visual method.')
 text='\n'.join(p.get_text() for p in doc);require('??' not in text, "Acceptance condition failed: '??' not in text")
 outside=[]
 for i,page in enumerate(doc,1):
  for block in page.get_text('dict')['blocks']:
   if block['type']!=0:continue
   for line in block['lines']:
    for span in line['spans']:
     x0,y0,x1,y1=span['bbox']
     if x0<32 or x1>page.rect.width-32 or y0<20 or y1>page.rect.height-20:outside.append({'page':i,'text':span['text'],'bbox':span['bbox']})
 require(not outside, outside[:10])
 qa=json.loads((OUT/'pdf-qa.json').read_text());require(qa['mode']=='final_source_build', "Acceptance condition failed: qa['mode']=='final_source_build'");require(not qa['overfull_warnings'], "Acceptance condition failed: not qa['overfull_warnings']");require(qa['pdf_sha256']==sha(pdf), "Acceptance condition failed: qa['pdf_sha256']==sha(pdf)")
 qa.update(status='passed',visual_review='passed',pages=len(doc),page_count=len(doc),visually_reviewed_pages=reviewed_pages,full_size_reviewed_pages=full_size,visual_review_method=coverage['method'],visual_review_record=args.visual_review,visual_review_record_sha256=sha(review),visual_review_coverage_record=args.review_coverage,visual_review_coverage_sha256=sha(coverage_path),text_boundary_check='all extracted text spans within safe page bounds',historical_inputs_unchanged=True)
 (OUT/'pdf-qa.json').write_text(json.dumps(qa,indent=2)+'\n')
 # Compiler chatter is reproducible scratch, not part of the publication bundle.
 log=OUT/'build-log.txt'
 if log.exists():log.unlink()
 files={}
 for p in sorted(OUT.rglob('*')):
  if not p.is_file() or p.name in ['artifact-manifest.json'] or '__pycache__' in p.parts or p.suffix=='.pyc':continue
  files[str(p.relative_to(ROOT))]=sha(p)
 manifest={'schema':'hnm-integrated-draft02-v1','human_author':registry['human_author'],'scope':'Complete integrated manuscript source/PDF and companions. Historical audit folders retain their historical scope. Hashes establish provenance, not mathematical correctness.','pdf_sha256':sha(pdf),'pages':len(doc),'contributions':139,'equation_aliases':len(registry['equations']),'statement_aliases':len(registry['statements']),'quantity_aliases':len(registry['quantities']),'new_axioms':0,'review_record':args.visual_review,'review_sha256':sha(review),'sha256':files}
 (OUT/'artifact-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(json.dumps({k:v for k,v in manifest.items() if k!='sha256'}))
if __name__=='__main__':main()
