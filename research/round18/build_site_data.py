#!/usr/bin/env python3
"""Publish six-loop content only after complete independently reviewed gates."""
from pathlib import Path
from fractions import Fraction as F
import csv,hashlib,json,math,sys
HERE=Path(__file__).resolve().parent;DIST=HERE.parents[1]/'dist'
sys.path.insert(0,str(HERE/'advisor'))
from freeze_gate import verify
LOOPS=('a1','a2','b1','b2','c1','c2')
def read(path):return json.loads((HERE/path).read_bytes())
def raw(path):return (HERE/path).read_text()
def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def number(v):return float(F(v))
def plot_from_csv(plots,key,path,title,xlabel,ylabel,xfield,series,caption):
    source=HERE/path;name='next-'+key+'.csv';(DIST/name).write_bytes(source.read_bytes())
    with source.open(newline='') as f:rows=list(csv.DictReader(f))
    if not rows:raise ValueError('Empty accepted plot data '+key)
    result=[]
    for label,field,transform in series:
        points=[]
        for row in rows:
            value=number(row[field]) if field else 0.0
            if transform=='log10':value=math.log10(value)
            points.append([number(row[xfield]),value])
        if not all(math.isfinite(v) for pair in points for v in pair):raise ValueError('Nonfinite plot '+key)
        result.append({'name':label,'points':points})
    plots[key]={'title':title,'xLabel':xlabel,'yLabel':ylabel,'csv':'/'+name,'caption':caption,'series':result}
    return len(result)

def main():
    gates=[verify(HERE/'advisor'/(loop+'-gate.json')) for loop in LOOPS]
    proof=read('proof_results.json')
    review=read('backward/integration/results.json')
    if proof.get('status')!='passed' or review.get('status')!='passed':raise ValueError('Proof or independent integration incomplete')
    for file,sha in review['reviewed_source_sha256'].items():
        if digest(HERE/file)!=sha:raise ValueError('Stale independent integration '+file)
    content=read('content.json')
    if [s['id'].lower() for s in content.get('solutions',[])]!=list(LOOPS):raise ValueError('All six detailed solutions required')
    plots={};count=0
    count+=plot_from_csv(plots,'bridge-amplitude','forward/a1/output/mu-scan.csv','A bridge with zero dressed-reference mean','Signed bridge ratio μ/α','Sufficient finite gap lower bound / α','mu_over_alpha',[('Dressed zero-mean bound','improved_lower',None),('Generic perturbation bound','generic_lower',None)],'Same three-square strip at α=1 and end ratios1/2. The whole primary interval is established by the analytic inequality; these exact samples illustrate it. Zero/negative lower estimates are insufficient, not measured gap closure.')
    count+=plot_from_csv(plots,'summable-volume','forward/a2/output/volume.csv','An explicit inhomogeneous family','Vertex extent n','Sufficient physical gap lower bound at α=1','n',[('Exact finite-budget bound','finite_gap_lower',None),('Common all-volume bound','uniform_common_gap_lower',None),('Generic common bound','generic_uniform_lower',None)],'Specified spatially decaying remainder and complete strip boundary rule, α=αmin=1. Exact finite ledgers give the first curve; the all-volume proof gives7/64 independently of sampled boxes. This family is not literally all restrictions of one infinite coefficient assignment.')
    count+=plot_from_csv(plots,'homogeneous-budget','forward/a2/output/volume.csv','Why the summable estimate does not transfer','Vertex extent n','Total homogeneous remainder norm budget / α','n',[('Unchanged coefficient on every remaining face','homogeneous_remainder_norm_budget',None)],'The same finite graphs with coefficient α/64 on every remaining face have a growing sum-of-norms budget. This invalidates use of the summable remainder hypothesis; it is not evidence that their physical gaps vanish.')
    configure_later_plots(plots)
    count=sum(len(p['series']) for p in plots.values())
    csvhash={p['csv'].lstrip('/'):digest(DIST/p['csv'].lstrip('/')) for p in plots.values()}
    documents={'plan':raw('advisor/initial-plan.md'),'feedback':raw('advisor/feedback-log.md'),'post-a':raw('advisor/post-a-roadmap.md'),'sources':raw('advisor/source-audit.md')+'\n\n'+raw('advisor/physical-matching-supplement.md'),'roadmap':raw('next-roadmap.md')+'\n\n'+raw('advisor/next-roadmap-supplement.md'),'readme':raw('README.md'),'report':raw('report.md')}
    for loop in LOOPS:
        documents[loop+'-contract']=raw('advisor/'+loop+'-contract.md')
        documents[loop+'-forward']=raw('forward/'+loop+'/report.md')
        documents[loop+'-backward']=raw('backward/'+loop+'/report.md')
        documents[loop+'-gate']=raw('advisor/'+loop+'-gate.json')
    compact={**proof,'routes':{name:{**r,'result':{k:v for k,v in r['result'].items() if k not in ('search_trace','frontier')}} for name,r in proof['routes'].items()}}
    documents['proof']=json.dumps(compact,indent=2)
    extra=read('presentation-data.json')
    data={**content,**extra,'status':'accepted','version':'18.1','loops_completed':6,'scientific_roles':3,'advisory_decisions':2,'gates':gates,'plots':plots,'csv_sha256':csvhash,'documents':documents,
          'routes':[{'target':name,'status':r['result']['status'],'steps':r['result'].get('certified_cost')} for name,r in proof['routes'].items()]}
    # Check serialization independently of the source-writing operation.
    encoded=json.dumps(data,ensure_ascii=False,allow_nan=False,separators=(',',':'))
    if json.loads(encoded)!=data:raise ValueError('Data serialization mismatch')
    (HERE/'site-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    (DIST/'research-next-data.js').write_text('window.OBSERVATORY_NEXT='+encoded+';\n')
    (DIST/'research-round18-proof.json').write_text(json.dumps(compact,indent=2)+'\n')
    (HERE/'data-checks.json').write_text(json.dumps({'status':'passed','plot_series_checked':count,'csv_sha256':csvhash,'loop_gates':len(gates),'scope':'Accepted exact data converted only for display; scientific checks are separately recorded.'},indent=2)+'\n')
    print(json.dumps({'status':'passed','loops':6,'solutions':6,'plots':len(plots),'documents':len(documents)}))

def configure_later_plots(plots):
    plot_from_csv(plots,'spectral-box','forward/b2/output/coupling.csv','A full finite-graph spectral bound','Maximum coefficient ratio r','Sufficient physical gap lower bound / α','r',[('Full E1 with vacuum trial','R_lower',None),('All eleven magnitudes equal r: star trial','instance_gap_lower',None)],'The whole signed eleven-dimensional box r≤3/8 is established analytically on the fixed two-cube graph. The second curve additionally fixes every coefficient magnitude to αr; its stronger value is not a uniform lower bound for every unequal vector having the same maximum. Exact samples outside the selected box remain visible as insufficient. These curves are lower-bound formulas, not measured gaps; their radical intervals do not bound the actual gap from above.')
    configure_conditional_plots(plots)

def configure_conditional_plots(plots):
    plot_from_csv(plots,'conditional-precision','forward/c2/output/refinement.csv','Complete normalized-integral error','Taylor degree','log10 exact interval width','degree',[('All six weights: normalized width','width','log10')],'Primary κ=1/64, with exact numerator and partition tails and a positive denominator floor. The frozen target is width≤10^−12. Degrees0/2 do not resolve sign; degrees4/6 resolve positivity but fail width; degree8 meets both.')
    source=HERE/'forward/c2/output/weights.csv';name='next-conditional-weights.csv';(DIST/name).write_bytes(source.read_bytes())
    with source.open(newline='') as stream:rows=list(csv.DictReader(stream))
    series=[]
    for d,label in [('2','All six weights'),('1','One V-only weight omitted'),('0','Both V-only weights omitted')]:
        selected=[r for r in rows if r['V_only_coefficient']==d]
        points=sorted([[number(r['kappa']),number(r['lower'])] for r in selected])
        if len(points)!=3 or [p[0] for p in points]!=[-1/64,0.0,1/64] or not all(math.isfinite(v) for p in points for v in p):raise ValueError('Incomplete signed conditional plot')
        series.append({'name':label,'points':points})
    plots['conditional-weights']={'title':'The omitted weights change the same observable','xLabel':'Signed static coefficient κ','yLabel':'Normalized joint expectation: exact lower endpoint','csv':'/'+name,'series':series,'caption':'Degree8 enclosures for the same two-link observable at κ=−1/64,0,+1/64. Each curve changes only the declared V-only action coefficient. Segments connect these three recorded points; they are not a certified continuous interpolation. The independent exact comparison establishes that the nonzero-coupling intervals are disjoint.'}

if __name__=='__main__':main()
