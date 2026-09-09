"""Export actual computed records and attributed research for the Observatory."""
from pathlib import Path
import json, hashlib, math
R=Path(__file__).resolve().parent
OLD=R.parent/'round3'
def read(p):return json.loads(p.read_text())
base=read(OLD/'results/production_baseline.json')
m=base['macro'];e2=base['constants']['e2']
full_j=[(f-(f-e2*(s+d))/z)/e2 for f,s,d,z in zip(m['Fdrive'],m['J0'],m['Sx2'],m['Z'])]
data={
 'meta':{'date':'2026-09-09','baseline_scope':'Recorded finite-regulator mean field; fixed magnetic background, no metric evolution.','source_hash':base['provenance']['solver_sha256']},
 'baseline':{'parameters':base['parameters'],'diagnostics':base['diagnostics'],'macro':{k:m[k] for k in ['s','x','a','Fdrive','Z','Wexact','Wdrive','energy_work_residual','max_r2_error']},'full_current':full_j},
 'convergence':read(OLD/'results/resolved_longtime_summary.json'),
 'refinement':read(OLD/'results/fixed_window_refinement.json'),
 'weak':read(OLD/'results/weak_b100_summary.json'),
 'bosonized':read(OLD/'results/bosonized_comparator.json'),
 'gravity':read(OLD/'gravity_checks.json'),
 'prior_verification':read(OLD/'implementation_comparison.json'),
 'sources':[], 'documents':{}, 'response':None,'response_verification':None,
 'errata':[{'id':'R4-E01','title':'A claimed cancellation fix was absent','detail':'The previous report said the current was summed after subtracting each mode. The delivered source instead added two large totals. Its source hash matches the recorded data, so this is a report/source mismatch. The new response code uses the stable mode integrand and compares its effect without rewriting historical evidence.'}]
}
for key,item in read(OLD/'references.json').items():data['sources'].append({'id':key,'category':'Physics & prior methods',**item})
for fn,cat,prefix in [('advisor_sources.json','Advisor methods','ADV-'),('response_sources.json','Current physics','P3-'),('ux_sources.json','Interface inspiration','UX-')]:
 if (R/fn).exists():
  rec=read(R/fn)
  if isinstance(rec,dict) and isinstance(rec.get('records'),list):rec=rec['records']
  entries=rec.items() if isinstance(rec,dict) else ((v.get('id',str(i)),v) for i,v in enumerate(rec))
  for key,item in entries:
   if isinstance(item,dict):data['sources'].append({**item,'id':prefix+str(key),'category':cat})
for name in ['advisor_pipeline.md','response_contract.md','response_advisor_review.md','ux_spec.md','physics_completion_roadmap.md','response_verifier.md','advisor_skill_forward_test.md','guide_overview.md','targeted_solver_prompt.md']:
 if (R/name).exists():data['documents'][name]=(R/name).read_text()
for key,fn in [('response','response_results.json'),('response_verification','response_verification.json'),('response_comparison','response_production_comparison.json'),('physics_acceptance','physics_acceptance.json'),('advisor_errata','advisor_errata.json'),('advisor_skill_test','advisor_skill_forward_test.json')]:
 if (R/fn).exists():data[key]=read(R/fn)
if data.get('advisor_errata'):
 data['errata']=[{'id':e['id'],'title':e['id'].replace('ERR-','').replace('-',' ').title(),'detail':' '.join(filter(None,[e.get('observation'),e.get('correction'),e.get('inference_limit'),e.get('archive_limit')]))} for e in data['advisor_errata']['errors']]
out=R/'site_data.json';out.write_text(json.dumps(data,ensure_ascii=False,allow_nan=False)+'\n')
print(json.dumps({'sources':len(data['sources']),'baseline_samples':len(m['s']),'response_included':data['response'] is not None,'bytes':out.stat().st_size}))
