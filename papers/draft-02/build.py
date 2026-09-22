#!/usr/bin/env python3
"""Rebuild the additive manuscript in an isolated temporary directory."""
from pathlib import Path
import argparse,hashlib,json,re,shutil,subprocess,tempfile
def require(condition,message):
 if not condition:raise ValueError(message)
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def group(text,start):
 """Read one balanced TeX group; explicit AMS tags add nested braces."""
 require(text[start]=='{', "Acceptance condition failed: text[start]=='{'");depth=0
 for i in range(start,len(text)):
  if text[i] in '{}':
   backslashes=0;j=i-1
   while j>=0 and text[j]=='\\':backslashes+=1;j-=1
   if backslashes%2:continue
  if text[i]=='{':depth+=1
  elif text[i]=='}':
   depth-=1
   if depth==0:return text[start+1:i],i+1
 raise ValueError('Unbalanced LaTeX auxiliary group')
def label_numbers(aux):
 numbers={}
 for match in re.finditer(r'\\newlabel\{([^}]+)\}\{',aux):
  payload,_=group(aux,match.end()-1)
  if not payload.startswith('{'):continue
  value,_=group(payload,0)
  while value.startswith('{'):
   inner,end=group(value,0)
   if end!=len(value):break
   value=inner
  numbers[match[1]]=value
 return numbers
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--draft',action='store_true');args=ap.parse_args()
 findings=ROOT/'research/round29/advisor/findings.json'
 if not args.draft:
  require(findings.exists(), 'Final ten-loop findings are required; --draft is editorial only.')
  data=json.loads(findings.read_text());loops=data['loops'];require(len(loops)==10, 'Acceptance condition failed: len(loops)==10')
  for x in loops:
   gate=ROOT/'research/round29/advisor'/f"{x['id'].lower()}-gate.json"
   require(gate.exists(), f'Missing gate {gate}')
   gate_data=json.loads(gate.read_text())
   for name,digest in gate_data['bindings'].items():
    path=ROOT/name;require(path.exists() and sha(path)==digest, f'Source binding mismatch: {name}')
  require('editorial integration checkpoint' not in (HERE/'sections/round29.tex').read_text(), "Acceptance condition failed: 'editorial integration checkpoint' not in (HERE/'sections/round29.tex').read_text()")
 registry=json.loads((HERE/'registry/hnm-registry.json').read_text())
 require(registry['human_author']=='Hruday N M (BUNZEEY)', "Acceptance condition failed: registry['human_author']=='Hruday N M (BUNZEEY)'")
 with tempfile.TemporaryDirectory(prefix='hnm-draft02-') as tmp:
  work=Path(tmp)/'paper';shutil.copytree(HERE,work,ignore=shutil.ignore_patterns('main.pdf','main.bbl','__pycache__','*.pyc','artifact-manifest.json','pdf-qa.json'))
  proc=subprocess.run(['latexmk','-pdf','-bibtex','-interaction=nonstopmode','-halt-on-error','main.tex'],cwd=work,capture_output=True,text=True)
  (HERE/'build-log.txt').write_text(proc.stdout+proc.stderr)
  if proc.returncode:raise RuntimeError((proc.stdout+proc.stderr)[-6000:])
  log=(work/'main.log').read_text()
  bad=[s for s in log.splitlines() if ('undefined' in s.lower() and ('reference' in s.lower() or 'citation' in s.lower())) or 'multiply defined' in s]
  require(not bad, bad)
  shutil.copy2(work/'main.pdf',HERE/'main.pdf');shutil.copy2(work/'main.bbl',HERE/'main.bbl')
  aux=(work/'main.aux').read_text();numbers=label_numbers(aux)
  for e in registry['equations']:e['printed_locator']=numbers.get(e['legacy_label'])
  require(all(e['printed_locator'] for e in registry['equations']), "Acceptance condition failed: all(e['printed_locator'] for e in registry['equations'])")
  require(all(not any(c in e['printed_locator'] for c in '{}') for e in registry['equations']), "Acceptance condition failed: all(not any(c in e['printed_locator'] for c in '{}') for e in registry['equations'])")
  (HERE/'registry/hnm-registry.json').write_text(json.dumps(registry,indent=2,ensure_ascii=False)+'\n')
  qa={'status':'rendering_required','mode':'editorial_draft' if args.draft else 'final_source_build','pdf_sha256':sha(HERE/'main.pdf'),'references_resolved':True,'overfull_warnings':[x for x in log.splitlines() if 'Overfull' in x],'contributions':len(registry['contributions']),'equation_aliases':len(registry['equations']),'human_author':registry['human_author']}
  (HERE/'pdf-qa.json').write_text(json.dumps(qa,indent=2)+'\n')
  print(json.dumps(qa))
if __name__=='__main__':main()
