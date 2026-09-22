import sys
EXPECTED_FINAL_SHA=sys.argv[1]
import hashlib,json,operator
from fractions import Fraction as F
from pathlib import Path
P='research/round28/'; path=P+'advisor/ah2-admission.json'; H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest(); R=lambda p:json.loads(Path(p).read_text()); S=R(path);checks=[];bindings={path:H(path)}
def need(ok,label):
 if not ok:raise RuntimeError(label)
 checks.append(label)
def ptr(d,p):
 for t in p.split('/')[1:]:
  t=t.replace('~1','/').replace('~0','~');d=d[int(t)] if isinstance(d,list) else d[t]
 return d
def rat(v):
 if isinstance(v,dict):
  if set(v)!={'numerator','denominator'} or type(v['numerator']) is not int or type(v['denominator']) is not int or v['denominator']<=0:raise ValueError('invalid rational encoding')
  return F(v['numerator'],v['denominator'])
 if type(v) not in (str,int):raise ValueError('rational exact type')
 return F(v)
def E(e,d):
 if not isinstance(e,dict) or len(e)!=1:raise ValueError('one operation required')
 k,a=next(iter(e.items()))
 if k=='constant':return rat(a)
 if k=='pointer':return rat(ptr(d,a))
 if k=='length':return F(len(ptr(d,a)))
 v=[E(x,d) for x in a]
 if k=='sum':return sum(v,F())
 if k=='product':
  result=F(1)
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
OPS={'eq':operator.eq,'lt':operator.lt,'le':operator.le,'gt':operator.gt,'ge':operator.ge,'ne':operator.ne}
def verify(s,d,label):
 for c in s['semantic_controls']:need(json.dumps(ptr(d,c['pointer']),sort_keys=True)==json.dumps(c['equals'],sort_keys=True),label+' semantic '+c['id'])
 for c in s['rational_relations']:need(OPS[c['op']](E(c['left'],d),E(c['right'],d)),label+' exact relation '+c['id'])
need(H(path)==EXPECTED_FINAL_SHA,'root-approved exact final specification')
for p,h in S['bindings'].items():need(H(p)==h,'spec binding '+p);bindings[p]=h
counts={};snapshot_counts={}
for side,s in S['producers'].items():
 prefix=P+side+'/ah2/';d=R(prefix+'output/results.json');before=len(checks);verify(s,d,side);counts[side]=len(checks)-before
 need(bool(ptr(d,s['scope_pointer'])),'producer scope projection '+side)
 snapshot_counts[side]=len(s['required_snapshots'])
 for p,h in s['required_snapshots'].items():need(H(p)==h,side+' required source snapshot '+p)
 fr=R(s['freeze']);fb={(p if p.startswith(P) else prefix+p):h for p,h in fr[s['freeze_binding_field']].items()}
 for p,h in fb.items():need(H(p)==h,side+' full frozen binding '+p)
 for p,h in d[s['binding_field']].items():need(H(p)==h,side+' output source binding '+p)
 for p in s['source_manifests']+s['instruction_manifests']+s['adoption_records']:need(p in S['bindings'] or p in fb,'manifest/adoption direct or verified transitive binding '+p)
 need(prefix+'report.md' in fb,side+' report freeze binding')
 if s['report_binding']=='output_and_freeze':need(prefix+'report.md' in d[s['binding_field']],side+' report output binding')
 need(not s.get('output_artifacts',{}),side+' exactly one result file; no omitted auxiliary output')
for s in S['supplemental_evidence']:
 d=R(s['path']);before=len(checks);verify(s,d,s['path']);counts[s['path']]=len(checks)-before
 need(bool(ptr(d,s['scope_pointer'])),'supplemental exact scope '+s['path'])
 if s.get('binding_field'):
  for p,h in d[s['binding_field']].items():need(H(p)==h,'supplemental source '+p)
expected={P+'skeptic/ah2_independent.py':3146,P+'skeptic/ah2_post_review.py':4349}
need({c['script'] for c in S['skeptic_checkers']}==set(expected),'exact independent entrypoints')
for c in S['skeptic_checkers']:
 need(c['output_mode']=='file' and c['arguments']==['--output','{output}'],'explicit file interface '+c['script'])
 need(R(c['output'])['check_count']==expected[c['script']],'accepted checker count '+c['script'])
 for p in [c['script'],c['output']]+c['inputs']:need(p in S['bindings'],'checker dependency pinned '+p)
for mutation in [True,{'numerator':True,'denominator':1},{'numerator':1,'denominator':0}]:
 try:rat(mutation)
 except ValueError:need(True,'invalid exact-rational type/value rejected '+repr(mutation))
 else:need(False,'invalid exact-rational type/value rejected')
need(json.dumps(True)!=json.dumps(1),'semantic Boolean-integer distinction')
need(S['producers']['forward']['scope_pointer']=='/model' and S['producers']['reverse']['scope_pointer']=='/scope','different actual scope projections retained')
result={'schema':'ym28-ah2-admission-spec-review-v1','accepted':True,'blocking_issues':[],'specification':path,'specification_sha256':H(path),'check_count':len(checks),'checks':checks,'semantic_and_rational_counts':counts,'required_snapshot_counts':snapshot_counts,'scope':'Independent exact evaluation of final admission projections and rational relations, all verified direct/transitive source/freeze bindings, all complete loading blocks, both scalar certificate/fixture sets, repaired inventory provenance and both checker interfaces. No import of the release arithmetic evaluator and no new physical investigation.','bindings':bindings}
out=P+'skeptic/ah2-admission-spec-review.json';Path(out).write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'passed','checks':len(checks),'counts':counts,'snapshots':snapshot_counts,'sha256':H(out)}))
