#!/usr/bin/env python3
"""Build recorded-data pages only from current reviewed research artifacts."""
from pathlib import Path
from fractions import Fraction as F
import csv
import hashlib
import json
import math
import shutil
from proof_routes import checked_inputs
from trace_archive import read_json,verify_archives

HERE=Path(__file__).resolve().parent
DIST=HERE.parents[1]/'dist'

def read(path):return read_json(HERE/path)
def digest(path):return hashlib.sha256((HERE/path).read_bytes()).hexdigest()
def rows(path):
    with (HERE/path).open() as f:return list(csv.DictReader(f))

def check_sources(record,prefix=''):
    if not isinstance(record,dict) or not record:raise ValueError('Missing source binding')
    for key,value in record.items():
        p=HERE/prefix/key
        if not p.resolve().is_relative_to(HERE) or p.is_symlink():raise ValueError('Unsafe source binding')
        if hashlib.sha256(p.read_bytes()).hexdigest()!=value:raise ValueError('Stale reviewed source '+str(p))

def build():
    verify_archives()
    manifest,_=checked_inputs();proof=read('proof_results.json')
    if proof['status']!='passed' or proof['manifest']!=manifest:raise ValueError('Stale proof replay')
    acceptance=read('skeptic/acceptance.json')
    required={'advisor/advisor.md','solver/drive_bound.py','solver/exact_stepper.py','solver/run_study.py',
              'solver/test_solver.py','volume/volume_checks.py','volume/volume-bridge.md',
              'closure/closure_audit.py','closure/closure-audit.md','proof_routes.py'}
    if acceptance.get('status')!='passed' or not required<=set(acceptance.get('reviewed_source_hashes',{})):
        raise ValueError('Required independent reviews incomplete')
    check_sources(acceptance['reviewed_source_hashes'])
    validation=read('solver/output/validation.json');edge=read('solver/output/edge_tests.json')
    optimized_edge=read('solver/output/edge_tests_optimized.json')
    for report in (validation,edge,optimized_edge):
        if report['status']!='passed':raise ValueError('Producer gate incomplete')
        check_sources(report['source_hashes'],'solver')
    exact=read('solver/output/exact_step_certificate.json');check_sources(exact['source_hashes'],'solver')
    if exact['computed_vector_was_renormalized'] is not False or F(exact['total_state_error_upper'])>=F(337501,10**9):
        raise ValueError('Exact fixture statement does not match certificate')
    closure=read('closure/output/results.json')
    if closure['status']!='passed' or closure['source_sha256']!=digest('closure/closure_audit.py'):raise ValueError('Stale closure output')
    volume=read('volume/output/checks.json')
    check_sources(read('volume/artifact_manifest.json')['files'],'volume')
    if volume.get('all_checks_passed') is not True or not all(x.get('passed') is True for x in volume['checks']):
        raise ValueError('Volume diagnostic incomplete')
    docs={key:(HERE/path).read_text() for key,path in {
        'advisor':'advisor/advisor.md','solver':'solver/README.md','skeptic':'skeptic/REVIEW.md',
        'volume':'volume/volume-bridge.md','closure':'closure/closure-audit.md','readme':'README.md'}.items()}
    docs['exact']=json.dumps(exact,indent=2)
    docs['certificates']=json.dumps(read('solver/output/analytic_certificates.json'),indent=2)
    docs['study']=json.dumps({'validation':validation,'comparison':read('solver/output/numerical_comparisons.json')},indent=2)
    docs['checks']=json.dumps({'independent':acceptance,'solver':edge,'study':validation,'volume':volume,'closure':closure},indent=2)
    compact={k:v for k,v in proof.items() if k!='routes'}
    compact['trace_storage']='Full unmodified search traces are in proof_results.json.gz; this dialog omits explored states/frontiers.'
    compact['routes']={name:{'library':route['library'],'result':{k:v for k,v in route['result'].items()
        if k not in ('search_trace','frontier')}} for name,route in proof['routes'].items()}
    docs['routes']=json.dumps(compact,indent=2)
    shutil.copyfile(HERE/'proof_results.json.gz',DIST/'research-round12-proof-trace.json.gz')
    docs['roadmap']=json.dumps({'current':read('current_roadmap.json'),'advisor_handoff':read('advisor/roadmap.json')},indent=2)
    summary=rows('solver/output/comparison_summary.csv');curves=rows('solver/output/bound_curves.csv')
    tensor=rows('volume/output/tensor_counterbenchmark.csv');boxes=rows('volume/output/volume_scaling.csv')
    moments=rows('closure/output/closure_moments.csv')
    for source,target in [('solver/output/comparison_summary.csv','bridge-drive-summary.csv'),
                          ('solver/output/bound_curves.csv','bridge-drive-bounds.csv'),
                          ('volume/output/tensor_counterbenchmark.csv','bridge-tensor.csv'),
                          ('volume/output/volume_scaling.csv','bridge-volume.csv'),
                          ('closure/output/closure_moments.csv','bridge-closure.csv')]:
        shutil.copyfile(HERE/source,DIST/target)
    def logpoints(data,x,y):
        return [[float(F(r[x])),math.log10(float(F(r[y])))] for r in data if float(F(r[y]))>0]
    plots={}
    plots['drive_bound']={'title':'Reduced cosine drive: representation bound and numerical comparison',
        'xLabel':'Time, α=1','yLabel':'log₁₀ Haar state distance','csv':'/bridge-drive-bounds.csv',
        'caption':'Exact rational bounds are converted to log10 for display. Numerical differences compare two computed Galerkin states and may be dominated by integration error at very early times. Zero entries are omitted, never assigned a fictitious logarithm.',
        'series':[{'name':label,'points':logpoints([r for r in curves if r['case']=='reduced' and int(r['degree'])==d],'time',field)}
                  for d in (3,4) for label,field in [(f'D{d} analytic representation bound','analytic_error_upper'),(f'D{d} numerical difference from D6','empirical_D6_difference')]]}
    equal=[r for r in summary if r['case'] in ('reduced','short','slow') and r['degree']=='4']
    plots['drive_action']={'title':'Same action A=1/2, different physical durations',
        'xLabel':'Drive duration T, α=1','yLabel':'log₁₀ final state distance','csv':'/bridge-drive-summary.csv',
        'caption':'D4: durations 0.2,2,4 change the electric phase while preserving the accumulated magnetic action. The common bound is exact; smaller numerical differences do not constitute a tighter certificate.',
        'series':[{'name':label,'points':sorted(logpoints(equal,'duration',field))} for label,field in [('Common analytic bound','analytic_state_error_upper'),('Numerical D4–D6 difference','empirical_final_D6_difference')]]}
    plots['volume_tensor']={'title':'Independent copies: fixed gap, deteriorating comparison',
        'xLabel':'Number of independent copies q','yLabel':'log₁₀ gap / α','csv':'/bridge-tensor.csv',
        'caption':'The one-square tensor gap equals its one-copy gap exactly. The constant 2.5 is an analytic lower bound; the 3.028986 curve is a numerical eigenvalue estimate. The vanishing global estimate does not imply a vanishing true gap.',
        'series':[{'name':name,'points':logpoints(tensor,'q_independent_copies',key)} for name,key in [('Analytic tensor gap lower bound','analytic_tensor_gap_lower_bound_over_alpha'),('One-copy numerical gap','numerical_one_square_gap_over_alpha')]]+
                 [{'name':'Global one-square comparison','points':[[float(r['q_independent_copies']),float(r['global_one_square_log10_comparison'])] for r in tensor]}]}
    selected=[r for r in boxes if r['spatial_dimension']=='3' and float(r['kappa_lambda_over_alpha'])==0.1]
    if not selected:
        available=sorted({float(r['kappa_lambda_over_alpha']) for r in boxes if r['spatial_dimension']=='3'})
        if not available:raise ValueError('No recorded volume family')
        chosen=available[-1];selected=[r for r in boxes if r['spatial_dimension']=='3' and float(r['kappa_lambda_over_alpha'])==chosen]
    plots['volume_box']={'title':'Open cubic boxes at fixed κ='+selected[0]['kappa_lambda_over_alpha'],
        'xLabel':'Cells per spatial side','yLabel':'log₁₀ finite-volume lower bound / α','csv':'/bridge-volume.csv',
        'caption':'Displayed log bounds remain finite when exponentiating them would underflow. This is the proved estimate, not a measured physical gap or a continuum extrapolation.',
        'series':[{'name':'Explicit global heat comparison','points':[[float(r['n_cells_per_side']),float(r['log10_bound_Delta_over_alpha'])] for r in selected]}]}
    plots['closure']={'title':'A missing fluctuation leaves a nonzero identity residual',
        'xLabel':'Tilted-measure coefficient κ','yLabel':'First-identity residual','csv':'/bridge-closure.csv',
        'caption':'Floating Haar quadrature checks the exact recurrence. The collapsed-moment residual is κ times the positive variance. At κ=0 the first identity is blind; the next detects the false closure.',
        'series':[{'name':label,'points':[[float(r['kappa']),float(r[field])] for r in moments]} for label,field in [('Exact hierarchy, numerical residual','true_residual'),('Replace m₂ by m₁²','collapsed_residual')]]}
    for p in plots.values():
        if not p['series'] or not all(s['points'] and all(math.isfinite(v) for point in s['points'] for v in point) for s in p['series']):
            raise ValueError('Empty or nonfinite plot')
    sources=read('root-sources.json')['sources']
    # The volume ledger records exact reading scopes; title metadata comes from
    # the same report's source inventory, not a guess based on arXiv identifiers.
    titles={
        'S1':('A stochastic analysis approach to lattice Yang–Mills at strong coupling','Volume-uniform strong-coupling Gibbs inequalities and separate Euclidean covariance decay; not a continuum Hamiltonian construction.'),
        'S1-journal':('Shen–Zhu–Zhu journal publication record','Publication metadata only; mathematical scope taken from the primary preprint.'),
        'S2':('Simulating Fully Gauge-Fixed SU(2) Hamiltonian Dynamics on Digital Quantum Computers','Finite Hamiltonian normalization and graph scope.'),
        'S3':('Quantum Yang–Mills Theory','Official construction, reconstruction and mass-gap requirements.')}
    for s in read('volume/sources.json')['sources']:
        if s['id'] not in titles:continue
        title,use=titles[s['id']]
        sources.append({'title':title,'url':s['url'],'use':use,'depth':s['reading_depth']})
    for s in read('advisor/sources.json')['primary_sources']:
        url=s.get('url')
        if url and not any(t['url']==url for t in sources):
            sources.append({'title':s['title'],'url':url,'use':' '.join(s['supports']),'depth':s['reading_depth']+' '+' '.join(s['limitations'])})
    inventory=read('advisor/theorem_inventory.json')
    if inventory['advisor_sha256']!=digest('advisor/advisor.md'):raise ValueError('Stale advisor inventory')
    nodes=[{'id':c['claim_id'],'kind':c['status'],'statement':c['statement'],'assumption_ids':c['dependencies']} for c in inventory['claims']]
    routes=[{'name':k,'summary':v['result']['status']+(f" · {v['result']['certified_cost']} reviewed rules" if v['result']['status']=='proved' else '')} for k,v in proof['routes'].items()]
    roadmap=read('current_roadmap.json')['items']
    reports=[{'name':r['name'],'status':str(r.get('count',''))+' independent checks · '+r['status'],'scope':r['scope']} for r in acceptance['reports']]
    reports.extend([{'name':'Solver tests','status':str(len(edge['checks']))+' checks passed','scope':'Same checks under normal and optimized Python; repeats not added.'},
                    {'name':'Four-drive study','status':str(len(validation['gates']))+' gates passed','scope':'Exact truncation arithmetic plus clearly separate numerical diagnostics.'},
                    {'name':'Four-dimensional Yang–Mills','status':'OPEN','scope':'No completed volume-uniform continuum construction or physical mass-gap theorem.'}])
    selected=next(r for r in summary if r['case']=='reduced' and r['degree']=='4')
    payload={'documents':docs,'plots':plots,'sources':sources,'nodes':nodes,'routes':routes,'roadmap':roadmap,'reports':reports,
        'driveSummary':f"Reduced cosine ramp: D4 exact representation bound 1/3840; computed D4–D6 endpoint difference {float(selected['empirical_final_D6_difference']):.4g}. The latter is a numerical diagnostic, not a total-error certificate.",
        'exactSummary':{'representation':exact['representation_error_upper'],'algorithm':exact['finite_step_algorithm_error_upper'],'total':exact['total_state_error_upper'],'dimension':exact['dimension']},
        'errorBudget':[{'component':'Smooth-drive representation cutoff','status':'Analytic factorial theorem with exact rational action enclosures.'},
                       {'component':'Smooth-drive time integration','status':'Tolerance and independent midpoint diagnostics; no rigorous total time-error enclosure.'},
                       {'component':'Smooth-drive coefficient conditioning','status':'Gram condition and metric-defect diagnostics; no floating-rounding certificate.'},
                       {'component':'New exact two-step drive','status':'Exact rational state plus analytic Taylor remainder and representation bound: complete endpoint error certificate for this fixture.'},
                       {'component':'Spatial volume and continuum','status':'Open; the graph and physical theory are not certified by changing the representation cutoff.'}]}
    (DIST/'research-bridges-data.js').write_text('window.OBSERVATORY_BRIDGES='+json.dumps(payload,ensure_ascii=False,separators=(',',':'),allow_nan=False)+';\n')
    print(json.dumps({'plots':len(plots),'nodes':len(nodes),'sources':len(sources),'routes':len(routes)}))

if __name__=='__main__':build()
