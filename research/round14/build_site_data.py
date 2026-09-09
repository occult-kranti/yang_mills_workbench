#!/usr/bin/env python3
"""Build the recorded two-loop website only from accepted, matching evidence."""
from pathlib import Path
from fractions import Fraction as Q
import csv
import hashlib
import json
import math
import shutil

HERE=Path(__file__).resolve().parent
DIST=HERE.parents[1]/'dist'
def read(p):return json.loads((HERE/p).read_bytes())
def sha(p):return hashlib.sha256((HERE/p).read_bytes()).hexdigest()
def csvrows(p):
    with (HERE/p).open(newline='') as f:return list(csv.DictReader(f))
def decimal(q,digits=27,up=False):
    q=Q(q);scale=10**digits;n=(q.numerator*scale)//q.denominator
    if up and Q(n,scale)<q:n+=1
    sign='-' if n<0 else '';n=abs(n)
    return f'{sign}{n//scale}.{n%scale:0{digits}d}'
def verified_report(path,label,scope):
    r=read(path);count=r.get('check_count',r.get('count'))
    if r.get('status')!='passed' or type(count) is not int or count!=len(r.get('checks',[])):
        raise ValueError('Incomplete report: '+path)
    status_convention=path.startswith('forward/')
    if any((c.get('status')!='passed' if status_convention else c.get('passed') is not True) for c in r['checks']):raise ValueError('Failed check: '+path)
    return {'name':label,'status':f'{count} grouped gates passed','scope':scope}
def main():
    gate1=read('advisor/loop1_gate.json');gate2=read('advisor/loop2_gate.json')
    for g in (gate1,gate2):
        if g.get('status')!='accepted within declared finite-model scope':raise ValueError('Missing loop gate')
        for p,h in g['source_sha256'].items():
            if sha(p)!=h:raise ValueError('Changed accepted source: '+p)
    certs=read('forward/loop2_output/certificates.json')
    independent=read('backward/loop2_output/independent_certificate_review.json')
    if independent['collection_sha256']!=sha('forward/loop2_output/certificates.json'):raise ValueError('Stale independent certificate review')
    if certs['producer_source_sha256']!=sha('forward/loop2_certificate.py'):raise ValueError('Producer changed')
    central=read('central-certificate.json')
    if central!=next(c['certificate'] for c in certs['certificates'] if c['id']=='central_N32'):raise ValueError('Central selection changed')
    lo,hi=map(Q,central['enclosures']['covariance']);width=hi-lo
    if not 0<lo<=hi or width>Q(1,10**12):raise ValueError('Target failed')
    proof=read('proof_results.json')
    if proof.get('status')!='passed' or proof['arithmetic']['frozen_sha256']['central-certificate.json']!=sha('central-certificate.json'):
        raise ValueError('Missing current proof replay')
    docs={'protocol':'advisor/two-loop-protocol.md','forward1':'forward/loop1.md','forward2':'forward/loop2.md',
          'backward1':'backward/backward.md','backward2':'backward/loop2.md','advisor':'advisor/advisor_checks.py',
          'forwardchecks':'forward/output/results.json','verification':'backward/loop2_output/independent_certificate_review.json',
          'gate2':'advisor/loop2_gate.json','readme':'README.md','roadmap':'next-roadmap.md','sources':'advisor/source-audit.md'}
    documents={k:(HERE/p).read_text() for k,p in docs.items()}
    # Full search trace stays in the archive; dialog retains every library, meeting and final certificate.
    compact={**proof,'routes':{n:{**r,'result':{k:v for k,v in r['result'].items() if k not in ('search_trace','frontier')}} for n,r in proof['routes'].items()},
             'trace_note':'The dialog omits expansion traces/frontier; complete proof_results.json is in the research archive.'}
    documents['proof']=json.dumps(compact,indent=2)
    sources=[]
    for path in ['advisor/sources.json','forward/loop1_sources.json','backward/sources.json']:
        for s in read(path)['sources']:
            if not any(v['url']==s['url'] for v in sources):sources.append(s)
    reviews=[verified_report(*args) for args in [
      ('forward/output/results.json','Loop1 forward producer','196 producer gates include direct/reduced numerical comparisons; not an independent reviewer.'),
      ('backward/output/oracle_results.json','Loop1 backward character oracle','Independent tensor-power Haar construction, including1000 exact monomial comparisons.'),
      ('advisor/advisor_checks.json','Advisor mathematical transfer','Formal polynomial identity and pinned legacy certificate transfer; reviewed independently below.'),
      ('forward/loop2_output/results.json','Loop2 exact producer','Producer replay, signed fixtures, refinement and adversarial input controls.'),
      ('backward/loop2_output/independent_certificate_review.json','Independent exact certificate review','Character reconstruction of all23 certificates, strict semantics and source binding.'),
      ('backward/loop2_output/verifier_boundary_review.json','Independent verifier boundary review','Source/cache/collection boundary and mutation checks.'),
      ('backward/loop2_output/advisor/independent_advisor_review.json','Independent advisor review','Set-partition cumulant formula and independently recomputed outward rational rounding.'),
      ('proof_adapter_tests.json','Advisor proof adapter tests','All128 premise subsets checked against separate forward saturation; actual two-front meetings and ordered replay.')]]
    adapter=read('backward/loop2_output/proof/independent_proof_adapter_review.json')
    if adapter['status']!='passed':raise ValueError('Missing independent adapter review')
    reviews.append({'name':'Independent proof admission review','status':f"{adapter.get('check_count',adapter.get('count'))} grouped gates passed",'scope':'Reattempts original forged-record and rule-mutation attacks; independently checks search outcomes.'})
    curves=csvrows('forward/output/covariance_curves.csv')
    shutil.copyfile(HERE/'forward/output/covariance_curves.csv',DIST/'team-covariance.csv')
    qrows=csvrows('forward/output/quadrature_refinement.csv')
    shutil.copyfile(HERE/'forward/output/quadrature_refinement.csv',DIST/'team-quadrature.csv')
    refinement=[]
    for item in certs['certificates']:
        c=item['certificate']
        if item['id'].startswith('central_N'):
            w=Q(c['width']);refinement.append({'degree':c['degree'],'width':str(w),'log10_width':math.log10(w.numerator)-math.log10(w.denominator),'status':c['status']})
    refinement.sort(key=lambda r:r['degree'])
    with (DIST/'team-certificate.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['degree','width','log10_width','status']);w.writeheader();w.writerows(refinement)
    plots={
      'covariance':{'title':'Recorded covariance under the declared deformation','xLabel':'η (dimensionless action coefficient)','yLabel':'Cov(x,y)','csv':'/team-covariance.csv',
        'caption':'Floating1D conditional integration; exact solvable slice shown separately. The tangent is local and false factorization is a deliberately wrong control.',
        'series':[{'label':label,'points':[[float(r['eta']),float(r[key])] for r in curves]} for key,label in [('covariance_1_2','k₁=1, k₂=2'),('covariance_0_0','k₁=k₂=0'),('tangent_1_2','η=0 tangent at(1,2)'),('false_factorization','False factorization')]]},
      'quadrature':{'title':'Coarse grids can fail regular integrals','xLabel':'Nodes per integration dimension','yLabel':'log₁₀ max moment discrepancy','csv':'/team-quadrature.csv',
        'caption':'Floating discrepancies against128-node1D reference; positive observed values only. A discrepancy is not a rigorous error bound.',
        'series':[{'label':label,'points':[[int(r['nodes']),math.log10(float(r['max_moment_difference']))] for r in qrows if (r['k1'],r['k2'],r['eta'],r['method'])==key and float(r['max_moment_difference'])>0]} for key,label in [(('100','100','100','marginal'),'Strong positive:1D'),(('100','100','-100','direct'),'Competing fields:3D'),(('1','2','1','direct'),'Moderate:3D')]]},
      'certificate':{'title':'Exact covariance enclosure narrows with Taylor degree','xLabel':'Taylor degree N','yLabel':'log₁₀ exact interval width','csv':'/team-certificate.csv',
        'caption':'Widths come from rational endpoints, including the exponential and denominator errors. N4 is inconclusive; the1e−12 target is a declared gate, not a fitted value.',
        'series':[{'label':'Exact interval width','points':[[r['degree'],r['log10_width']] for r in refinement]}, {'label':'Requested width1e−12','points':[[r['degree'],-12] for r in refinement]}]}}
    if any(not s['points'] for p in plots.values() for s in p['series']):raise ValueError('Empty plot series')
    collaboration={'nodes':[
      {'id':'contract','label':'Advisor: shared contract','owner':'Advisor–skeptic','status':'frozen','x':430,'y':40,'route':'team-map'},
      {'id':'forward1','label':'Forward: exact Haar reduction','owner':'Forward researcher','status':'loop1 complete','x':190,'y':130,'route':'team-loop1'},
      {'id':'backward1','label':'Backward: required certificate','owner':'Backward researcher','status':'loop1 complete','x':670,'y':130,'route':'team-loop1'},
      {'id':'gate1','label':'Advisor: bound7 and next target','owner':'Advisor–skeptic','status':'loop1 accepted','x':430,'y':220,'route':'team-loop1'},
      {'id':'forward2','label':'Forward: rational calculation','owner':'Forward researcher','status':'loop2 complete','x':190,'y':310,'route':'team-loop2'},
      {'id':'backward2','label':'Backward: independent replay','owner':'Backward researcher','status':'loop2 complete','x':670,'y':310,'route':'team-loop2'},
      {'id':'gate2','label':'Advisor: finite result accepted','owner':'Advisor–skeptic','status':'loop2 accepted; full theory open','x':430,'y':400,'route':'team-review'},
      {'id':'next','label':'Next bounded research contract','owner':'All three roles','status':'planned; not executed','x':430,'y':510,'route':'team-roadmap'}],
      'edges':[{'from':a,'to':b} for a,b in [('contract','forward1'),('contract','backward1'),('forward1','backward1'),('forward1','gate1'),('backward1','gate1'),('gate1','forward2'),('gate1','backward2'),('forward2','backward2'),('forward2','gate2'),('backward2','gate2'),('gate2','next')]]}
    roadmap=[
      {'id':'L1','owner':'All three','status':'completed','forward':'Derive conditional integrals, exact baseline and response.','backward':'Reconstruct Haar moments and bound a normalized covariance.','gate':'Both formulas match; singular limits treated; eta1/4 perturbative sign remains inconclusive.'},
      {'id':'L2','owner':'All three','status':'completed','forward':'Compute exact Taylor moments and all normalization errors.','backward':'Recompute23 certificates via characters; challenge proof admission.','gate':'Central width<=1e−12 and positive; missing-premise routes blocked; changed bytes rejected.'},
      {'id':'NEXT-A','owner':'Forward + backward; advisor gate','status':'planned','forward':'Cover η∈[1/8,1/4] at k₁=k₂=1 with exact point enclosures and proved |C′|≤2 transport.','backward':'Demand a complete rational interval cover with strictly positive cell margins.','gate':'Every cell, endpoint, normalization and Lipschitz error checked. A missed cell fails the target.'},
      {'id':'NEXT-B','owner':'Forward geometry; backward oracle','status':'planned','forward':'Specify a larger Wilson graph and derive actual shared-link Haar integrals.','backward':'Require matched graph/action/measure before transferring any old moment identity.','gate':'Independent low-degree exact moments and wrong-orientation controls; no assumed factorization.'},
      {'id':'NEXT-C','owner':'Advisor source audit + spectral review','status':'open','forward':'Retrieve the applicable full stability proof and propagate explicit combinatorial/norm constants.','backward':'Require an actual positive threshold for the exact Hamiltonian and boundary assumptions.','gate':'No substitution of a Langevin gap or guessed existential constant; source access gaps stay explicit.'},
      {'id':'CONTINUUM','owner':'All three; future research','status':'open','forward':'Construct compatible volume, observable and scale limits with a matched physical state.','backward':'Demand nontrivial continuum theory, reconstruction axioms and a common physical spectral threshold.','gate':'Finite static covariance and a chosen extra mass cannot seed missing generator or continuum premises.'}]
    (HERE/'current_roadmap.json').write_text(json.dumps({'team_size':3,'completed_loops':2,'items':roadmap},indent=2)+'\n')
    feedback=[
      {'loop':'1','from':'Forward → backward','challenge':'A raw-moment bound26 is valid but unnecessarily loose.','decision':'Center the fourth cumulant; independently verify the improved bound7.'},
      {'loop':'1','from':'Backward → forward','challenge':'A floating exponential in the remainder prevents an entirely rational certificate.','decision':'Use a successive-term geometric tail; derive Jensen Z>=1.'},
      {'loop':'1','from':'Advisor → both','challenge':'The sufficient sign bound at(1,1,1/4) contains zero.','decision':'Freeze this point as the second-loop target with width<=1e−12 and positive lower endpoint.'},
      {'loop':'2','from':'Backward → forward','challenge':'Nested True can compare equal to integer1 in Python metadata.','decision':'Strict recursive type checks; preserve the failed certificate mutation.'},
      {'loop':'2','from':'Backward → advisor','challenge':'Forged pass records and mutable rules bypass proof admission.','decision':'Fresh independent arithmetic replay at library construction; immutable revalidated rule semantics.'},
      {'loop':'2','from':'Advisor → next contract','challenge':'A certified point still gives no parameter interval or physical time decay.','decision':'Plan exact coverage next; keep generator and continuum obligations separate.'}]
    failures=[
      {'finding':'Derived field exceeded a reused helper domain.','action':'Use the derived-field range and preserve original failing fixture.','limit':'Floating evaluation domain; finite analytic formula unchanged.'},
      {'finding':'Coarse quadrature missed the declared tolerance.','action':'Retain coarse failures and independent node refinements.','limit':'Agreement remains numerical, not a total error theorem.'},
      {'finding':'Huge exact integers exceeded safe JSON serialization limits.','action':'Compact earlier variance endpoints outward by exact rational floor/ceiling; independently verify containment.','limit':'No floating proof endpoints or disabled interpreter safeguard.'},
      {'finding':'Cached calls bypassed Boolean degree validation; nested Boolean aliased integer metadata.','action':'Validate before cache and recursively match canonical types.','limit':'Original code and failure records retained.'},
      {'finding':'Degree4 did not establish the covariance sign.','action':'Preserve insufficient output and refine the declared Taylor degree.','limit':'Failure of this bound is not evidence of zero covariance.'},
      {'finding':'Proof library trusted a forged replay and mutable rules.','action':'Replay arithmetic again at admission; freeze and revalidate rule semantics.','limit':'Still a finite conventional-proof planner, not a formal theorem kernel.'}]
    a=read('advisor/advisor_checks.json')
    for plot in plots.values():
        for series in plot['series']:series['name']=series.pop('label')
    data={'round':14,'team_size':3,'completed_loops':2,'collaboration':collaboration,'feedback':feedback,'roadmap':roadmap,'reviews':reviews,'failures':failures,'sources':sources,'documents':documents,'plots':plots,
      'metrics':{'central_equation':f"At k₁=k₂=1, η=1/4:\n{decimal(lo)} ≤ Cov(x,y) ≤ {decimal(hi,up=True)}\nExact certificate degree N={central['degree']}",
       'central_summary':f"At(1,1,1/4), a degree{central['degree']} exact rational certificate proves positive covariance with interval width {float(width):.6g}. The independent character verifier reconstructs all23 stored certificates.",
       'loop1_summary':f"196 producer gates;17 direct/reduced fixtures; maximum moment difference {read('forward/output/results.json')['maximum_independent_moment_difference']:.6g}. The separate backward oracle has79 grouped gates including1000 exact monomial comparisons."},
      'perturbative':[{'eta':r['eta'],'display':f"[{r['lower_display']:.8g}, {r['upper_display']:.8g}] (rounded display)",'status':r['status']} for r in a['perturbative_intervals']],
      'certificates':[{'label':r['id']+' · '+str(r['certificate']['parameters']),'degree':r['certificate']['degree'],'summary':r['certificate']['status']+f"; width {float(Q(r['certificate']['width'])):.5g}"} for r in certs['certificates']],
      'routes':[{'name':n,'status':r['result']['status'],'cost':r['result'].get('certified_cost')} for n,r in proof['routes'].items()]}
    (DIST/'research-team-data.js').write_text('window.OBSERVATORY_TEAM = '+json.dumps(data,ensure_ascii=False,allow_nan=False)+';\n')
    shutil.copyfile(HERE/'forward/loop2_output/certificates.json',DIST/'research-round14-certificates.json')
    print(json.dumps({'status':'built','pages':6,'plots':len(plots),'certificates':len(certs['certificates']),'routes':len(proof['routes'])}))
if __name__=='__main__':main()
