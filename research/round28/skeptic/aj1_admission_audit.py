#!/usr/bin/env python3
"""Independent final AJ1 metadata/arithmetic audit; imports no release evaluator."""
import argparse, hashlib, json, operator
from fractions import Fraction as Q
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
P='research/round28/';PATH=P+'advisor/aj1-admission.json'
H=lambda p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
R=lambda p:json.loads((ROOT/p).read_text())
checks=[]
def need(ok,label):
 if not ok:raise RuntimeError(label)
 checks.append(label)
def ptr(d,p):
 for t in p.split('/')[1:]:
  t=t.replace('~1','/').replace('~0','~');d=d[int(t)] if isinstance(d,list) else d[t]
 return d
def q(v):
 if isinstance(v,dict):
  if set(v)!={'numerator','denominator'} or type(v['numerator']) is not int or type(v['denominator']) is not int or v['denominator']<=0:raise ValueError('invalid rational object')
  return Q(v['numerator'],v['denominator'])
 if type(v) not in (str,int):raise ValueError('invalid rational type')
 return Q(v)
def E(e,d):
 if not isinstance(e,dict) or len(e)!=1:raise ValueError('one operation required')
 k,a=next(iter(e.items()))
 if k=='constant':return q(a)
 if k=='pointer':return q(ptr(d,a))
 if k=='length':return Q(len(ptr(d,a)))
 v=[E(x,d) for x in a]
 if k=='sum':return sum(v,Q(0))
 if k=='product':
  result=Q(1)
  for x in v:result*=x
  return result
 if k=='difference':return v[0]-v[1]
 if k=='quotient':return v[0]/v[1]
 if k=='minimum':return min(v)
 if k=='maximum':return max(v)
 if k=='absolute':return abs(v[0])
 if k=='power':
  if v[1].denominator!=1:raise ValueError('noninteger power')
  return v[0]**int(v[1])
 raise ValueError('unknown operation')
OPS={'eq':operator.eq,'ne':operator.ne,'lt':operator.lt,'le':operator.le,'gt':operator.gt,'ge':operator.ge}
def verify(s,d,label):
 for c in s['semantic_controls']:need(json.dumps(ptr(d,c['pointer']),sort_keys=True)==json.dumps(c['equals'],sort_keys=True),label+' semantic '+c['id'])
 for c in s['rational_relations']:need(OPS[c['op']](E(c['left'],d),E(c['right'],d)),label+' relation '+c['id'])
def main():
 ap=argparse.ArgumentParser();ap.add_argument('expected_sha');ap.add_argument('--output',default=str(ROOT/(P+'skeptic/aj1-admission-spec-review.json')));args=ap.parse_args()
 S=R(PATH);need(H(PATH)==args.expected_sha,'root approved exact final specification')
 bindings={PATH:H(PATH)}
 for p,h in S['bindings'].items():need(H(p)==h,'final spec binding '+p);bindings[p]=h
 counts={};snapshots={};outputs={}
 for side,s in S['producers'].items():
  prefix=P+side+'/aj1/';d=R(prefix+'output/results.json');before=len(checks);verify(s,d,side);counts[side]=len(checks)-before
  need(bool(ptr(d,s['scope_pointer'])),'actual scope projection '+side)
  snapshots[side]=len(s['required_snapshots'])
  for p,h in s['required_snapshots'].items():need(H(p)==h,side+' required source snapshot '+p)
  fr=R(s['freeze']);fb={(p if p.startswith(P) else prefix+p):h for p,h in fr[s['freeze_binding_field']].items()}
  actual={str(x.relative_to(ROOT)) for x in (ROOT/prefix).rglob('*') if x.is_file() and x!=ROOT/s['freeze']}
  need(set(fb)==actual,'complete all-owned producer closure '+side)
  for p,h in fb.items():need(H(p)==h,side+' complete frozen file '+p)
  if side=='forward':
   need(s['binding_field']=='aj1_provenance_pack','explicit typed forward adapter')
   pack=R(s['input_pack']);outbindings=pack['bindings']
   need(H(s['input_pack'])==d['provenance']['input_pack_sha256'],'forward runtime pack identity')
   need(d['provenance']['input_binding_count']==len(outbindings),'forward runtime pack count')
   need(H(prefix+'check.py')==d['provenance']['checker_sha256'],'forward runtime checker identity')
  else:outbindings=d[s['binding_field']]
  for p,h in outbindings.items():need(not Path(p).is_absolute() and H(p)==h,side+' portable exact runtime binding '+p)
  for p in s['source_manifests']+s['instruction_manifests']+s['adoption_records']:need(p in S['bindings'] or p in fb,'manifest/adoption source closure '+p)
  need(prefix+'report.md' in fb,'report frozen '+side)
  if s['report_binding']=='output_and_freeze':need(prefix+'report.md' in outbindings,'report runtime bound '+side)
  artifacts=s['output_artifacts'];need(set(artifacts)==({'source-manifest.json'} if side=='forward' else {'geometry.json'}),'complete auxiliary declaration '+side)
  actualoutputs={x.name for x in (ROOT/(prefix+'output')).iterdir() if x.is_file()}
  need(actualoutputs=={'results.json'}|set(artifacts),'every producer output declared '+side)
  for name,v in artifacts.items():
   p=prefix+'output/'+name;need(H(p)==v['sha256']==fb[p],'auxiliary frozen bytes '+side+name)
   if 'equals_result_pointer' in v:need(R(p)==ptr(d,v['equals_result_pointer']),'auxiliary exact embedded projection '+side+name)
  outputs[side]=sorted(actualoutputs)
 for s in S['supplemental_evidence']:
  d=R(s['path']);before=len(checks);verify(s,d,s['path']);counts[s['path']]=len(checks)-before
  need(bool(ptr(d,s['scope_pointer'])),'supplemental scope '+s['path'])
  if s.get('binding_field'):
   for p,h in d[s['binding_field']].items():need(H(p)==h,'supplemental source '+p)
 expected={P+'skeptic/aj1_independent.py':2060,P+'skeptic/aj1_post_review.py':1949}
 need({s['script'] for s in S['skeptic_checkers']}==set(expected),'exact two skeptic entrypoints')
 for s in S['skeptic_checkers']:
  need(s['output_mode']=='file' and s['arguments']==['--output','{output}'],'explicit file checker interface '+s['script'])
  need(R(s['output'])['check_count']==expected[s['script']],'expected checker count '+s['script'])
  for p in [s['script'],s['output']]+s['inputs']:need(p in S['bindings'],'checker explicit dependency bound '+p)
 for bad in [True,{'numerator':True,'denominator':1},{'numerator':1,'denominator':0}]:
  try:q(bad)
  except ValueError:need(True,'exact arithmetic rejects bad type '+repr(bad))
  else:need(False,'exact arithmetic type accepted')
 need(json.dumps(True)!=json.dumps(1),'semantic strict Boolean integer distinction')
 need(S['producers']['forward']['scope_pointer']=='/scope' and S['producers']['reverse']['scope_pointer']=='/theorem/scope','actual distinct producer scope schemas')
 limits=R(P+'skeptic/aj1-post-review.json')['limitations']
 need(len(limits)==8 and any(c['pointer']=='/limitations' and c['equals']==limits for x in S['supplemental_evidence'] if x['path']==P+'skeptic/aj1-post-review.json' for c in x['semantic_controls']),'eight scientific limits exactly pinned by specification')
 result={'schema':'ym28-aj1-admission-spec-review-v1','accepted':True,'blocking_issues':[],'specification':PATH,'specification_sha256':H(PATH),'check_count':len(checks),'checks':checks,'semantic_and_rational_counts':counts,'required_snapshot_counts':snapshots,'all_output_artifacts':outputs,'scope':'Independent exact evaluation of final approved semantic projections and rational relations, complete graph auxiliary and both manifests, every frozen closure, typed input pack and repaired local runtime bindings, postreview and preexchange interfaces. No release arithmetic imports and no new scientific investigation.','bindings':bindings}
 Path(args.output).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({'checks':len(checks),'counts':counts,'snapshots':snapshots,'output_sha256':hashlib.sha256(Path(args.output).read_bytes()).hexdigest()}))
if __name__=='__main__':main()
