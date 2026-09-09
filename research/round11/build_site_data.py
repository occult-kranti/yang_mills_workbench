#!/usr/bin/env python3
"""Publish recorded scientific evidence only after source/acceptance checks."""
from pathlib import Path
from fractions import Fraction as F
import csv,json,hashlib,math,shutil
from proof_routes import checked_inputs
HERE=Path(__file__).resolve().parent
DIST=HERE.parents[1]/'dist'
def read(rel):return json.loads((HERE/rel).read_text())
def rows(rel):
    with (HERE/rel).open() as f:return list(csv.DictReader(f))
def digest(rel):return hashlib.sha256((HERE/rel).read_bytes()).hexdigest()
def source_check(record,mapping):
    if not isinstance(record,dict) or set(record)!=set(mapping):raise ValueError('Incomplete source binding')
    for key,rel in mapping.items():
        if record[key]!=digest(rel):raise ValueError('Stale review source: '+rel)
def build():
    manifest,_=checked_inputs();proof=read('proof_results.json')
    if proof['status']!='passed' or proof['manifest']!=manifest:raise ValueError('Proof replay is stale')
    study=read('solver/output/validation.json');edge=read('solver/output/edge_tests.json')
    core=read('skeptic/final_normal_results.json');audit_proof=read('skeptic/proof_audit_results.json');audit_drive=read('skeptic/dynamic_audit_results.json')
    for report in (study,edge,core,audit_proof,audit_drive):
        if report.get('status')!='passed':raise ValueError('An independent or producer gate remains incomplete')
    source_check(study['source_hashes'],{name:'solver/'+name for name in ('two_plaquette.py','run_study.py','test_solver.py')})
    source_check(audit_drive['reviewed_source_hashes'],{name:'solver/'+name for name in ('two_plaquette.py','run_study.py','test_solver.py')})
    source_check(audit_proof['reviewed_hashes'],{name:name for name in manifest['sha256']})
    if core['source_sha256']!=digest('solver/two_plaquette.py') or edge['source_sha256']!=core['source_sha256']:raise ValueError('Stale core evidence')
    inventory=read('advisor/theorem_inventory.json')
    if inventory['advisor_sha256']!=digest('advisor/advisor.md'):raise ValueError('Stale theorem inventory')
    docs={name:(HERE/path).read_text() for name,path in {'advisor':'advisor/advisor.md','solver':'solver/README.md','skeptic':'skeptic/REVIEW.md','readme':'README.md'}.items()}
    collection=read('solver/output/stationary_certificates.json');cover=read('solver/output/continuous_rectangle_certificate.json')
    docs['rectangle']=json.dumps(cover,indent=2)
    docs['routes']=json.dumps({'scope':proof['scope'],'arithmetic':proof['arithmetic'],'routes':{name:{'status':v['result']['status'],'cost':v['result'].get('certified_cost'),'certificate':v['result'].get('certified_proof'),'library':v['library']} for name,v in proof['routes'].items()}},indent=2)
    docs['checks']=json.dumps({'study':study,'edges':edge,'core_review':core,'proof_review':audit_proof,'dynamic_review':audit_drive},indent=2)
    dynamics=read('solver/output/dynamic_summary.json');docs['dynamics']=json.dumps({'study':dynamics,'independent':audit_drive},indent=2)
    certificates=[]
    for i,c in enumerate(collection['certificates']):
        key='certificate-'+str(i);docs[key]=json.dumps(c,indent=2)
        certificates.append({'id':str(i),'document':key,'label':f"D={c['degree']}, α={c['alpha']}, λ₁={c['lambda1']}, λ₂={c['lambda2']}, ρ={c['rho']}",
          'display':f"Approximate gap: [{float(F(c['gap'][0])):.15g}, {float(F(c['gap'][1])):.15g}]\nExact lower: {c['gap'][0]}\nExact upper: {c['gap'][1]}\nRetained dimension {c['dimension']}; all omitted degrees controlled.",'status':c['status']})
    conv=rows('solver/output/stationary_convergence.csv');sweeps=rows('solver/output/parameter_sweep.csv');history=rows('solver/output/dynamic_history.csv')
    for source,target in [('stationary_convergence.csv','two-convergence.csv'),('parameter_sweep.csv','two-sweeps.csv'),('dynamic_history.csv','two-drive.csv')]:shutil.copyfile(HERE/'solver/output'/source,DIST/target)
    plots={'convergence':{'title':'Matched coefficients: α=ρ=1, λ₁=2, λ₂=3','xLabel':'Maximum polynomial degree D','yLabel':'Physical gap in the stated energy unit',
       'series':[{'name':label,'points':[[int(r['degree']),float(r[field])] for r in conv if r[field]!='']} for field,label in [('gap_Ritz_estimate','Ritz estimate (not a gap bound)'),('gap_certified_lower','Exact lower enclosure'),('gap_certified_upper','Exact upper enclosure')]],'csv':'/two-convergence.csv','caption':'Missing certificate endpoints are omitted, never replaced by zero. D=2,3,4 have exact full-space enclosures; the connected Ritz values are numerical comparisons.'},
      'drive':{'title':'Both prescribed magnetic couplings supply energy','xLabel':'Time, α=1','yLabel':'Energy / accumulated external work','series':[{'name':label,'points':[[float(r['t']),float(r[field])] for r in history]} for field,label in [('energy','State energy'),('integrated_work','Independently integrated work')]],'csv':'/two-drive.csv','caption':'Recorded degree-4 DOP853 evolution. Near energy-work agreement does not prove representation convergence.'}}
    sweepkeys=[]
    for axis,label in [('alpha','α (electric energy coefficient)'),('lambda1','λ₁ (left magnetic coefficient)'),('lambda2','λ₂ (right magnetic coefficient)'),('rho','ρ (dimensionless shared-link weight)')]:
        key='sweep_'+axis;sweepkeys.append(key);data=[r for r in sweeps if r['axis']==axis]
        plots[key]={'title':'Vary '+label,'xLabel':label,'yLabel':'Numerical gap estimate','series':[{'name':'Degree-4 Ritz estimate','points':[[float(r['value']),float(r['gap_Ritz_estimate'])] for r in data]}],'csv':'/two-sweeps.csv','caption':'Only this coefficient varies from baseline (α,λ₁,λ₂,ρ)=(1,1,2,1). This curve does not carry a rigorous gap interval.'}
    for p in plots.values():
        if not all(s['points'] and all(math.isfinite(v) for q in s['points'] for v in q) for s in p['series']):raise ValueError('Missing/nonfinite recorded plot')
    reports=[{'name':'Independent full core audit','status':f"{core['gate_count']} gates passed",'scope':core['reviewed_scope']},
      {'name':'Independent proof-wrapper audit','status':f"{audit_proof['gate_count']} gates passed",'scope':'Source binding, exact coverage, schema and withheld-premise controls.'},
      {'name':'Independent dynamic oracle','status':f"{audit_drive['gate_count']} gates passed",'scope':audit_drive['scope']},
      {'name':'Solver edge/mutation tests','status':f"{len(edge['checks'])} checks passed",'scope':'Normal and optimized Python report the same test outcomes; repetitions are not added to the count.'},
      {'name':'Stationary/drive study','status':f"{len(study['gates'])} gates passed",'scope':'Exact stationary certificates, parameter sweeps and declared finite-evolution checks.'},
      {'name':'Four-dimensional mass gap','status':'OPEN','scope':'No graph-volume-uniform or matched continuum theorem.'}]
    nodes=[{'id':c['claim_id'],'kind':'declared contract' if c['claim_id'] in ('graph_contract','parameter_domain') else c['status'],'statement':c['statement'],'assumption_ids':c['dependencies']} for c in inventory['claims']]
    routes=[{'name':name,'summary':v['result']['status']+(f" · {v['result']['certified_cost']} reviewed rules" if v['result']['status']=='proved' else '')} for name,v in proof['routes'].items()]
    sources=[{'title':s['title'],'url':s['url'],'use':' '.join(s['claims_used']),'depth':s['reading_depth']+' '+' '.join(s['limitations'])} for s in read('advisor/sources.json')['sources']]
    last=dynamics['dop853'][-1]
    payload={'documents':docs,'certificates':certificates,'plots':plots,'sweepKeys':sweepkeys,'nodes':nodes,'routes':routes,'sources':sources,'reports':reports,
      'rectangle':{'summary':'Exact arithmetic and analytic tail/continuity bounds certify every real point of [0,2]² at α=ρ=1.',
        'display':'Exact dimensionless lower: '+cover['gap_lower']+'\n≈'+str(float(F(cover['gap_lower'])))+'\nConservative scaled statement: Δ≥0.96 α\nFor ρ=1, α>0 and 0≤λ₁/α,λ₂/α≤2.'},
      'dynamics':{'summary':f"Degree-4 energy {last['final_energy']:.13g}; independently integrated work {last['final_work']:.13g}. Maximum work residual {last['work_max']:.3g}. Independent degree-3 raw-monomial RK45 agrees with the orthonormal implementation to {audit_drive['diagnostics']['state_difference_Haar_norm']:.3g} in Haar state norm.",
        'limit':f"Degree 3→4 changes the state by {dynamics['D3_to_D4_state_difference']:.8g}. This is a diagnostic difference; the full dynamic truncation error remains unbounded."}}
    (DIST/'research-two-plaquette-data.js').write_text('window.OBSERVATORY_TWO_PLAQUETTE='+json.dumps(payload,ensure_ascii=False,allow_nan=False,separators=(',',':'))+';\n')
    print(json.dumps({'certificates':len(certificates),'theories':len(nodes),'plots':len(plots),'sources':len(sources)}))
if __name__=='__main__':build()
