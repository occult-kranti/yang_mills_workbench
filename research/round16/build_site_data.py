#!/usr/bin/env python3
"""Build the scientific dashboard only from accepted, source-bound records."""
from pathlib import Path
from fractions import Fraction as Q
import csv,hashlib,json,math,shutil,sys
HERE=Path(__file__).resolve().parent;DIST=HERE.parents[1]/'dist'
sys.path.insert(0,str(HERE/'advisor'));from freeze_gate import verify

def read(path):return json.loads((HERE/path).read_bytes())
def raw(path):return (HERE/path).read_text()
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def decimal(value,up=False,digits=28):
    q=Q(value);scale=10**digits;n=q.numerator*scale//q.denominator
    if up and Q(n,scale)<q:n+=1
    sign='-' if n<0 else '';n=abs(n)
    return f'{sign}{n//scale}.{n%scale:0{digits}d}'
def write_csv(name,rows):
    with (DIST/name).open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)

def main():
    gates=[verify(HERE/'advisor'/(loop+'-gate.json')) for loop in ('loop1','loop2')]
    p=read('proof_results.json')
    if p['status']!='passed':raise ValueError('Proof replay absent')
    independent=read('backward/integration/review.json')
    if independent['status']!='passed':raise ValueError('Independent integration absent')
    for file,digest in independent['reviewed_source_sha256'].items():
        if sha(HERE/file)!=digest:raise ValueError('Stale independent integration '+file)
    collection=read('forward/loop2/output/collection.json');primary=collection['refinement'][-1]
    low,high=map(Q,primary['difference_interval'])
    if primary['status']!='target-met' or low<=0 or high-low>Q(1,10**12):raise ValueError('Primary target incomplete')
    plots={};csvhash={}
    rows=[{'degree':r['degree'],'difference_lower':r['difference_interval'][0],'difference_upper':r['difference_interval'][1],'width':r['width'],'log10_width':math.log10(Q(r['width']).numerator)-math.log10(Q(r['width']).denominator),'status':r['status']} for r in collection['refinement']]
    write_csv('shared-refinement.csv',rows)
    plots['refinement']={'title':'Total error of the shared-face difference','xLabel':'Total Taylor degree N','yLabel':'log10 exact interval width','csv':'/shared-refinement.csv','caption':'Both action-dependent numerator and normalization tails are included. Degrees0,6,12 miss the requested width;18,24 pass. Connecting lines only guide the eye.',
        'series':[{'name':'Exact total width','points':[[r['degree'],r['log10_width']] for r in rows]},{'name':'Width target1e-12','points':[[r['degree'],-12] for r in rows]}]}
    graph=read('forward/loop1/graph.json');shared=next(i for i,f in enumerate(graph['faces']) if f['region']=='shared')
    fixtures={r['id']:r['certificate'] for r in collection['fixtures']};baseline=fixtures['omitted_shared']['enclosures']['expectation'];bmid=sum(map(Q,baseline))/2
    rows=[]
    for name in ('negative_shared','omitted_shared','half_shared','full_shared'):
        cert=fixtures[name];lo,hi=map(Q,cert['enclosures']['expectation']);rows.append({'fixture':name,'shared_coupling':cert['couplings'][shared],'lower':str(lo),'upper':str(hi),'midpoint':str((lo+hi)/2),'omitted_midpoint':str(bmid)})
    write_csv('shared-coupling.csv',rows)
    plots['coupling']={'title':'Same observable under four shared-face couplings','xLabel':'Shared action coefficient κ_s','yLabel':'All-eleven trace expectation','csv':'/shared-coupling.csv','caption':'Outer coefficients stay1/8. Points are midpoints of exact degree24 enclosures, whose widths are too small to resolve here. Lines are not a proved interpolation or monotonicity statement.',
        'series':[{'name':'Recorded expectation','points':[[float(Q(r['shared_coupling'])),float(Q(r['midpoint']))] for r in rows]},{'name':'Omitted-action baseline','points':[[float(Q(r['shared_coupling'])),float(Q(r['omitted_midpoint']))] for r in rows]}]}
    rows=read('advisor/scale-output/review.json')['rows'];write_csv('shared-energy-scale.csv',rows)
    plots['scale']={'title':'Same dimensionless gap, different physical scales','xLabel':'Vertex extent n of an open cubic box','yLabel':'Free physical gap in common energy units','csv':'/shared-energy-scale.csv','caption':'Exact free-box spectra: Δ(K_n)=3. The sequence proof, not sampled points, establishes3/n→0 for α_n=1/n.',
        'series':[{'name':'Fixed α=1','points':[[r['n'],float(Q(r['fixed_free_gap']))] for r in rows]},{'name':'Shrinking α=1/n','points':[[r['n'],float(Q(r['shrinking_free_gap']))] for r in rows]}]}
    plots['volume']={'title':'The global norm estimate still deteriorates','xLabel':'Vertex extent n','yLabel':'Sufficient lower bound, energy units','csv':'/shared-energy-scale.csv','caption':'At fixed α=1 and |λ/α|=1/100. Negative values mean this estimate is insufficient; they are not an interacting gap measurement.',
        'series':[{'name':'3−P(n)/100','points':[[r['n'],float(Q(r['global_norm_lower']))] for r in rows]},{'name':'Zero','points':[[r['n'],0] for r in rows]}]}
    for name in {p['csv'].lstrip('/') for p in plots.values()}:csvhash[name]=sha(DIST/name)
    # Verify the serialized display against exact CSV values, using independent reads.
    bindings={'refinement': [('degree','log10_width'),('degree',None)],'coupling':[('shared_coupling','midpoint'),('shared_coupling','omitted_midpoint')],'scale':[('n','fixed_free_gap'),('n','shrinking_free_gap')],'volume':[('n','global_norm_lower'),('n',None)]}
    checked=0
    for key,fields in bindings.items():
        data=list(csv.DictReader((DIST/plots[key]['csv'].lstrip('/')).open()))
        for index,(x,y) in enumerate(fields):
            points=plots[key]['series'][index]['points']
            expected=[[float(Q(row[x])),float(Q(row[y])) if y else (-12 if key=='refinement' else 0)] for row in data]
            if any(abs(a-b)>8e-15*max(1,abs(a),abs(b)) for aa,bb in zip(points,expected) for a,b in zip(aa,bb)) or len(points)!=len(expected):raise ValueError('Plot/CSV mismatch '+key)
            checked+=1
    (HERE/'data-checks.json').write_text(json.dumps({'status':'passed','plot_series_checked':checked,'csv_sha256':csvhash,'scope':'Serialized plot values checked against saved CSV input; display rounding only, not independent physics.'},indent=2)+'\n')
    documents={'contract':raw('advisor/contract.md'),'feedback':raw('advisor/feedback-log.md'),'gates':json.dumps(gates,indent=2),
        'graph':raw('forward/loop1/derivation.md'),'independent1':raw('backward/loop1/derivation.md'),
        'loop2':raw('advisor/loop2-contract.md')+'\n\n'+raw('forward/loop2/derivation.md'),
        'independent2':raw('backward/loop2/derivation.md'),'scale':raw('advisor/energy_scale.md')+'\n\n'+raw('backward/loop1/derivation.md'),
        'sources':raw('advisor/source-audit.md'),'roadmap':raw('next-roadmap.md'),'readme':raw('README.md')}
    documents['proof']=json.dumps({**p,'routes':{n:{**r,'result':{k:v for k,v in r['result'].items() if k not in ('search_trace','frontier')}} for n,r in p['routes'].items()}},indent=2)
    steps=[
      {'id':'L1.1 Geometry','forward':'Construct all signed link and face words.','backward':'Independently rebuild endpoints, faces, incidence and rank.','outcome':'12V20E11F; four incidence3 links; outer10 is a different action.'},
      {'id':'L1.2 Admissibility','forward':'Enumerate center parity and character moments.','backward':'Independent GF2 and exact link-index contractions.','outcome':'2,048 subsets; only four center-even supports; amplitudes separately computed.'},
      {'id':'L1.3 Shared amplitude','forward':'Two disk convolutions and three-character fusion.','backward':'256 full fourth-Haar projector branches, including negative terms.','outcome':'Repeated shared insertion1/524288; wrong projectors rejected.'},
      {'id':'L1.4 Energy convention','forward':'Use the declared finite physical graph spectrum.','backward':'Independent edge/face counts, scale sequence and scope critique.','outcome':'Conditional scale bridge proved; free shrinking-scale counterexample retained.'},
      {'id':'L2.1 Coefficients','forward':'Factorial series and separate eleven insertions.','backward':'Polynomial projection using Catalan Haar moments.','outcome':'All required coefficient arrays and changed-action fixtures replayed.'},
      {'id':'L2.2 Complete error','forward':'Total-degree truncation, Jensen normalization and quotient difference.','backward':'Reconstruct every numerator, denominator and difference bound.','outcome':'Primary positive difference passes; coarse insufficient cases retained.'}]
    feedback=[{'finding':'All-eleven Haar product vanishes.','action':'Use a repeated insertion for the new amplitude, then a finite-action difference.','limit':'Center parity alone cannot compute a nonzero amplitude.'},
      {'finding':'Omitted shared interaction does not give a zero observable baseline.','action':'Keep the same observable and enclose both expectations.','limit':'The result is for the two specified actions.'},
      {'finding':'Cached public coefficient dictionaries could be changed by a caller.','action':'Return a defensive copy and reject Boolean substitutions before cache lookup.','limit':'Source hashes alone do not protect mutable in-memory data.'},
      {'finding':'Common energy-scale wording was too broad.','action':'State it as a condition for this inference from a common dimensionless lower bound.','limit':'The interacting uniform lower bound is still missing.'}]
    next_items=[{'goal':'Original uniform physical threshold — open','forward':'Derive local decomposition, relative bounds and overlap constants.','backward':'Require an explicit per-interaction threshold, common domains and energy units.','gate':'No extensive plaquette budget or unevaluated source constant.'},
      {'goal':'Finite physical trial extension — planned','forward':'Derive eleven-character Gram and Hamiltonian matrices.','backward':'Pair E0 upper bound with a separate full E1 lower bound.','gate':'No trial-matrix gap used as full-gap lower bound.'},
      {'goal':'Next nontrivial intertwiner graph — planned','forward':'Choose geometry beyond the three-disk scalar contraction.','backward':'Reconstruct new invariant projectors and dimension factors.','gate':'Actual graph first; no generic positivity assumption.'}]
    routes=[{'name':n,'status':r['result']['status'],'steps':r['result'].get('certified_cost')} for n,r in p['routes'].items()]
    reviews=[]
    for g in gates:
        reviews += [{'name':g['loop']+' producer','outcome':str(g['producer_checks'])+' gates passed','scope':'Author checks; ordinary and optimized counted once.'},{'name':g['loop']+' independent verifier','outcome':str(g['independent_checks'])+' gates passed','scope':'Separate derivation/arithmetic and rejecting controls; shared model assumptions.'}]
    reviews += [{'name':'Advisor scale implementation','outcome':'37 checks passed','scope':'Independently reviewed within the118 first-loop checks; not an extra independent panel.'},{'name':'Independent proof admission review','outcome':str(independent['checks_count'])+' checks passed','scope':'Frozen semantics, fresh arithmetic, actual meetings and blocked open premises.'}]
    failures=[{'finding':r['finding'],'action':r['action'],'limit':r['limit']} for r in feedback]
    data={'version':'16.1','loops_completed':2,'scientific_roles':3,'metrics':{
      'geometry':'12 vertices,20 links,11 faces; the shared plaquette is included once.',
      'haar':'The exact new mixed moment is1/524288. The all-eleven Haar product vanishes.',
      'parity':'The face-to-edge matrix has GF2 rank9 and nullity2; its four closed supports are independently checked.',
      'integral':f'At outer1/8, the shared1/8 versus0 effect is enclosed in[{decimal(low)}, {decimal(high,True)}]. Exact width≈{float(high-low):.6g}; target1e−12.',
      'integralEquation':'O=∏_(all11)x_f\nD=E_(outer1/8,shared1/8)[O]−E_(outer1/8,shared0)[O]\nD∈['+decimal(low)+', '+decimal(high,True)+']\nThe exact fractions and separate expectation intervals are in the certificate.',
      'scale':'H_N=α_N K_N rescales gaps by α_N. Free cubic boxes n≥2 with α_n=1/n have gap3/n→0.'},
      'gates':gates,'plots':plots,'csv_sha256':csvhash,'documents':documents,'steps':steps,'feedback':feedback,'next':next_items,'routes':routes,'reviews':reviews,'failures':failures,'sources':read('advisor/sources.json'),
      'network':{'nodes':[{'id':'advisor','label':'Advisor–skeptic','status':'Freeze and challenge the contract','x':430,'y':40,'route':'shared-team'},
       {'id':'forward1','label':'Forward · Loop1','status':'Graph and disk convolution','x':185,'y':135,'route':'shared-graph'},
       {'id':'backward1','label':'Backward · Loop1','status':'Independent Haar projector','x':675,'y':135,'route':'shared-haar'},
       {'id':'gate1','label':'Loop1 accepted','status':'Matched comparison selected','x':430,'y':225,'route':'shared-team'},
       {'id':'forward2','label':'Forward · Loop2','status':'Coefficients and total tails','x':185,'y':320,'route':'shared-integral'},
       {'id':'backward2','label':'Backward · Loop2','status':'Polynomial Haar reconstruction','x':675,'y':320,'route':'shared-review'},
       {'id':'gate2','label':'Loop2 accepted','status':'Next physical obligations retained','x':430,'y':430,'route':'shared-roadmap'}],
       'edges':[{'from':a,'to':b} for a,b in [('advisor','forward1'),('advisor','backward1'),('forward1','gate1'),('backward1','gate1'),('gate1','forward2'),('gate1','backward2'),('forward2','gate2'),('backward2','gate2')]]}}
    (HERE/'site-data.json').write_text(json.dumps(data,indent=2,allow_nan=False)+'\n')
    (HERE/'current_roadmap.json').write_text(json.dumps({'finite_subproblem':'completed in declared scope','original_uniform_goal':'open','continuum_goal':'open','next':next_items},indent=2)+'\n')
    (DIST/'research-shared-data.js').write_text('window.OBSERVATORY_SHARED='+json.dumps(data,ensure_ascii=False,separators=(',',':'),allow_nan=False)+';\n')
    for target,source in [('research-round16-certificates.json','forward/loop2/output/collection.json'),('research-round16-graph.json','forward/loop1/graph.json')]:shutil.copyfile(HERE/source,DIST/target)
    print(json.dumps({'status':'passed','loops':2,'pages':8,'plots':len(plots),'series':checked}))
if __name__=='__main__':main()
