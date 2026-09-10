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
    source=HERE/path;name='six-'+key+'.csv';(DIST/name).write_bytes(source.read_bytes())
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
    count+=plot_from_csv(plots,'local-obstruction','forward/a1/output/small_t.csv','The full relative-bound shortcut fails','k, where t=2⁻ᵏ','log₁₀(|magnetic energy| / free energy)','k',[('Exact physical trial ratio','ratio','log10')],'Fixed α=1 and λ=1/2. The analytic 1/|t| formula proves divergence; the exact samples illustrate it. No interacting gap is measured.')
    count+=plot_from_csv(plots,'sparse-volume','forward/a2/output/volume.csv','A uniform bound for the sparse family','Vertex extent n','Sufficient physical gap lower bound','n',[('Sparse block bound','sparse_lower',None),('Global norm estimate','global_physical_norm_lower',None)],'Same sparse Hamiltonian family at α=1 and ρ=1/2. Negative global estimates are insufficient bounds, not negative physical gaps. The general proof establishes the constant1/4; sampled volumes check its implementation.')
    count+=plot_from_csv(plots,'finite-coupling','forward/b1/output/coupling.csv','The improved dense finite bound','Common ratio |λ|/α','Sufficient gap lower bound / α','r',[('Twelve-state lower estimate','improved_lower',None),('Previous global estimate','global_lower',None)],'Both curves are sufficient lower estimates for the fixed eleven-face graph. Connecting lines only guide the eye. Exact analysis gives the improved threshold12/43; negative or zero values do not establish gap closure.')
    configure_later_plots(plots)
    count=sum(len(p['series']) for p in plots.values())
    csvhash={p['csv'].lstrip('/'):digest(DIST/p['csv'].lstrip('/')) for p in plots.values()}
    documents={'plan':raw('advisor/revised-plan.md'),'feedback':raw('advisor/feedback-log.md'),'post-a':raw('advisor/post-a-roadmap.md'),'sources':raw('advisor/source-audit.md'),'roadmap':raw('next-roadmap.md'),'readme':raw('README.md'),'report':raw('report.md')}
    for loop in LOOPS:
        documents[loop+'-contract']=raw('advisor/'+loop+'-contract.md')
        documents[loop+'-forward']=raw('forward/'+loop+'/report.md')
        documents[loop+'-backward']=raw('backward/'+loop+'/report.md')
        documents[loop+'-gate']=raw('advisor/'+loop+'-gate.json')
    compact={**proof,'routes':{name:{**r,'result':{k:v for k,v in r['result'].items() if k not in ('search_trace','frontier')}} for name,r in proof['routes'].items()}}
    documents['proof']=json.dumps(compact,indent=2)
    extra=read('presentation-data.json')
    data={**content,**extra,'status':'accepted','version':'17.1','loops_completed':6,'scientific_roles':3,'advisory_decisions':2,'gates':gates,'plots':plots,'csv_sha256':csvhash,'documents':documents,
          'routes':[{'target':name,'status':r['result']['status'],'steps':r['result'].get('certified_cost')} for name,r in proof['routes'].items()]}
    # Check serialization independently of the source-writing operation.
    encoded=json.dumps(data,ensure_ascii=False,allow_nan=False,separators=(',',':'))
    if json.loads(encoded)!=data:raise ValueError('Data serialization mismatch')
    (HERE/'site-data.json').write_text(json.dumps(data,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    (DIST/'research-six-data.js').write_text('window.OBSERVATORY_SIX='+encoded+';\n')
    (DIST/'research-round17-proof.json').write_text(json.dumps(compact,indent=2)+'\n')
    (HERE/'data-checks.json').write_text(json.dumps({'status':'passed','plot_series_checked':count,'csv_sha256':csvhash,'loop_gates':len(gates),'scope':'Accepted exact data converted only for display; scientific checks are separately recorded.'},indent=2)+'\n')
    print(json.dumps({'status':'passed','loops':6,'solutions':6,'plots':len(plots),'documents':len(documents)}))

def configure_later_plots(plots):
    plot_from_csv(plots,'adjoint-amplitude','forward/b2/output/amplitude.csv','A trial component repairs the finite endpoint','η as a fraction of6/3817','Sufficient physical gap lower bound / α','eta_fraction_of_endpoint',[('Exact Rayleigh-based lower bound','gap_lower_over_alpha',None)],'The Hamiltonian stays at λ_p/α=12/43. All samples are valid physical trial states. The whole open interval0<η<6/3817 is proved positive; zero or negative lower estimates do not show gap closure.')
    plot_from_csv(plots,'conditional-precision','forward/c2/output/refinement.csv','The complete conditional error budget','Taylor degree N','log₁₀(exact contrast enclosure width)','degree',[('Numerator and partition remainder','width','log10')],'Same κ=1/8 action and two fixed boundaries at every degree. Degrees0,4,8 are insufficient for the10⁻¹² target;12 and16 pass. The exact geometric remainder bounds the whole tail; these are not empirical quadrature errors.')
    evidence=read('forward/c2/output/collection.json')
    primary=evidence['refinements'][-1]
    fixtures={r['id']:r['certificate'] for r in evidence['fixtures']}
    pairs=[('-1/8',fixtures['negative_tetrahedral'],fixtures['negative_commuting']),('0',fixtures['zero_tetrahedral'],fixtures['zero_commuting']),('1/16',fixtures['half_tetrahedral'],fixtures['half_commuting']),('1/8',primary['tetrahedral'],primary['commuting'])]
    source=HERE/'presentation/conditional-boundaries.csv';source.parent.mkdir(exist_ok=True)
    with source.open('w',newline='') as f:
        writer=csv.writer(f);writer.writerow(['kappa','tetra_lower','tetra_upper','commuting_lower','commuting_upper'])
        for k,t,c in pairs:
            if t['action_vector']!=c['action_vector'] or t['partition_interval']!=c['partition_interval']:raise ValueError('Unmatched plotted boundary pair')
            writer.writerow([k,*t['expectation_interval'],*c['expectation_interval']])
    plot_from_csv(plots,'conditional-boundaries','presentation/conditional-boundaries.csv','Equal action, distinct joint observables','Common Euclidean coefficient κ','Conditional expectation (enclosure lower endpoint)','kappa',[('Tetrahedral boundary','tetra_lower',None),('Commuting boundary','commuting_lower',None)],'Recorded degree16 fixtures with one common action and normalization at each κ. Both exact interval endpoints are in the CSV. Their widths are below display resolution. Lines guide the eye between fixtures; no coupling-interval coverage or bulk calculation is claimed.')
    (HERE/'presentation/derivation.json').write_text(json.dumps({'input':'forward/c2/output/collection.json','input_sha256':digest(HERE/'forward/c2/output/collection.json'),'output_sha256':digest(source),'method':'Extract exact degree16 interval endpoints for the four declared paired coupling fixtures.'},indent=2)+'\n')

if __name__=='__main__':main()
