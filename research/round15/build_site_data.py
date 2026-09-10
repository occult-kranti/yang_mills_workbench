#!/usr/bin/env python3
"""Publish recorded scientific evidence only after all six source-bound gates."""
from pathlib import Path
from fractions import Fraction as Q
import csv,hashlib,json,math,shutil
HERE=Path(__file__).resolve().parent
DIST=HERE.parents[1]/'dist'
PHASES=('A1','A2','B1','B2','C1','C2')
def read(path):return json.loads((HERE/path).read_bytes())
def raw(path):return (HERE/path).read_text()
def decimal(q,digits=25,up=False):
    q=Q(q);scale=10**digits;n=q.numerator*scale//q.denominator
    if up and Q(n,scale)<q:n+=1
    sign='-' if n<0 else '';n=abs(n)
    return f'{sign}{n//scale}.{n%scale:0{digits}d}'
def write_csv(name,rows):
    with (DIST/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def verify_gates():
    gates={}
    for phase in PHASES:
        gate=read('advisor/loop-gates/'+phase+'.json')
        if not gate['status'].startswith('accepted'):raise ValueError('Missing gate '+phase)
        expected={str(p.relative_to(HERE)) for role in ('forward','backward') for p in (HERE/role/phase).rglob('*') if p.is_file() and '__pycache__' not in p.parts}
        if set(gate['source_sha256'])!=expected:raise ValueError('Incomplete phase inventory '+phase)
        for path,digest in gate['source_sha256'].items():
            p=HERE/path
            if p.is_symlink() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest:raise ValueError('Stale gate '+path)
        gates[phase]=gate
    return gates

def main():
    gates=verify_gates()
    a=read('forward/A2/output/final_cover.json')
    b=read('forward/B2/output/certificates.json');bc=b['certificates'][-1]
    c=read('spectral-summary.json')
    if c['original_uniform_goal']!='open':raise ValueError('Uniform goal must retain supported status')
    review=read('backward/integration/output/independent_adapter_review.json')
    if review['status']!='passed':raise ValueError('Independent integration review absent')
    for field,path in [('adapter_sha256','proof_routes.py'),('replay_sha256','replay_evidence.py'),('inventory_sha256','proof_inputs.json'),('proof_results_sha256','proof_results.json')]:
        if review[field]!=hashlib.sha256((HERE/path).read_bytes()).hexdigest():raise ValueError('Stale independent integration '+path)
    proof=read('proof_results.json')
    if proof['status']!='passed':raise ValueError('Proof routes unavailable')
    goals=[
      {'id':'A','original':'Prove positivity throughout eta in[1/8,1/4] at k1=k2=1.','status':'Completed in the declared finite deformed measure.','next':'Extend a complete cover only after deriving a new interval contract.'},
      {'id':'B','original':'Use a larger Wilson graph and verify its actual coupled integral.','status':'Completed on the closed cube boundary; finite graph only.','next':'Derive higher-incidence Haar contractions before extending to two cubes.'},
      {'id':'C','original':'Extract an explicit volume-uniform physical stability threshold.','status':'Original goal open; finite-graph bounds and a variational improvement accepted as side results.','next':'Control local constants independently of plaquette count; retain the source-specific proof gap.'}]
    loops=[
      {'id':'A1','owner':'All three roles','forward':'Derivative transport and eight exact midpoint certificates.','backward':'Independent centered-derivative identity, points, endpoints and cell union.','outcome':'All eight point values positive; all eight cell bounds insufficient.'},
      {'id':'A2','owner':'All three roles','forward':'Bisect only the failed cells with degree24 fixed.','backward':'Replay each exact transition and all final endpoints; reject cap/coverage mutations.','outcome':'8→16→21 cells; every final lower margin positive.'},
      {'id':'B1','owner':'All three roles','forward':'Actual cube words, character gluing and matrix/gauge tests.','backward':'Independent exact edge-index contraction and repeated Haar moments.','outcome':'Six-face product1/1024; proper subsets vanish; one wrong dagger discriminated.'},
      {'id':'B2','owner':'All three roles','forward':'Exact factorial-series coefficients and complete Taylor/normalization bounds.','backward':'Tensor-power oracle reconstructs all seven certificates.','outcome':'Degree24 width below1e-12; independent-face partition rejected.'},
      {'id':'C1','owner':'All three roles','forward':'Finite graph girth/free gap, min-max bound and original source-constant audit.','backward':'Physical-domain proof, graph/domain cases and state-identification challenge.','outcome':c['loop1_outcome']},
      {'id':'C2','owner':'All three roles','forward':'Use reviewed Haar trial vectors to improve the boundary-case estimate.','backward':'Independently verify norms, full-operator inequality and exact radical endpoints.','outcome':c['loop2_outcome']}]
    feedback=[
      {'transition':'Planning → all goals','finding':'Point coverage, planar factorization and unspecified source constants were distinct gaps.','action':'Keep original targets; use interval transport, the closed cube and a separately labelled finite spectral side result.'},
      {'transition':'A1 → A2','finding':'Cell radius dominated point error; every coarse cell was insufficient.','action':'Bisect failed cells only; retain exact interval, action, Lipschitz2 and degree24.'},
      {'transition':'B1 → B2','finding':'Five face class observables factorize but all six do not.','action':'Use the cube dimension factor and six separate insertions; compare against a fully bounded factorized baseline.'},
      {'transition':'C1 → C2','finding':c['feedback_finding'],'action':c['feedback_action']}]
    planning=[{'goal':'A','objection':'Positive sampled points leave unchecked values between them.','decision':'Prove derivative transport and certify a complete exact cover.'},
      {'goal':'B','objection':'More open planar squares still factorize; whole-face reversal is a true SU(2) invariance.','decision':'Use an actual closed cube and a wrong single-link dagger.'},
      {'goal':'C','objection':'A theorem with existential constants has no supplied numerical uniform threshold.','decision':'Keep the original goal open; test a clearly distinguished finite-graph inequality.'}]
    documents={'planning':raw('advisor/revised-plan.md'),'gates':json.dumps(gates,indent=2),
       'sourceaudit':raw('advisor/source-audit.md'),'roadmap':raw('next-roadmap.md'),'readme':raw('README.md')}
    for phase in PHASES:
        documents[phase]='\n\n'.join(raw(str(p.relative_to(HERE))) for role in ('forward','backward') for p in sorted((HERE/role/phase).glob('*.md')))
        if not documents[phase]:raise ValueError('Missing derivation '+phase)
    compact={**proof,'routes':{n:{**r,'result':{k:v for k,v in r['result'].items() if k not in ('search_trace','frontier')}} for n,r in proof['routes'].items()},'trace_note':'Expansion traces omitted in dialog; full proof_results.json is in the archive.'}
    documents['proof']=json.dumps(compact,indent=2)
    documents['admissionreview']=raw('backward/integration/review.md') if (HERE/'backward/integration/review.md').exists() else raw('backward/integration/output/independent_adapter_review.json')
    documents['statecheck']=raw('advisor/cube_state_check.md')+'\n\nSubsequent independent acceptance:\n'+raw('backward/C1/output/independent_state_review.json')
    plots={}
    for phase,key,name in [('A1','A_coarse','cycles-a-coarse.csv'),('A2','A_refined','cycles-a-refined.csv')]:
        cover=read('forward/'+phase+'/output/'+('cover.json' if phase=='A1' else 'final_cover.json'))
        rows=[{'center':r['center'],'left':r['left'],'right':r['right'],'point_lower':r['certificate']['enclosures']['covariance'][0],'transported_lower':r['transported_lower'],'status':r['status']} for r in cover['cells']]
        write_csv(name,rows)
        plots[key]={'title':'Coarse cells: positive points, insufficient coverage' if phase=='A1' else 'Final 21 cells: every exact transported margin is positive',
          'xLabel':'eta cell midpoint','yLabel':'Covariance lower bound','csv':'/'+name,
          'caption':'Exact rational lower endpoints, rounded for plotting. Each transported lower bound applies throughout its listed closed cell; CSV includes both endpoints. Connecting segments are visual guides.',
          'series':[{'name':label,'points':[[float(Q(r['center'])),float(Q(r[field]))] for r in rows]} for field,label in [('point_lower','Exact point lower'),('transported_lower','Whole-cell lower')]]+ [{'name':'Zero','points':[[float(Q(rows[0]['center'])),0],[float(Q(rows[-1]['center'])),0]]}]}
    rows=[{'degree':r['degree'],'width_exact':r['expectation_width'],'log10_width':math.log10(Q(r['expectation_width']).numerator)-math.log10(Q(r['expectation_width']).denominator),'status':r['expectation_status'],'excess_lower':r['enclosures']['partition_excess'][0]} for r in b['certificates']]
    write_csv('cycles-b-refinement.csv',rows)
    plots['B_refinement']={'title':'Cube observable: exact total error narrows with degree','xLabel':'Total Taylor degree N','yLabel':'log10 enclosure width','csv':'/cycles-b-refinement.csv','caption':'All numerator and normalization errors included. Degrees0,6,12 miss the declared width;18 and24 pass. Widths are exact rational differences, not floating residuals.','series':[{'name':'Exact width','points':[[r['degree'],r['log10_width']] for r in rows]},{'name':'Width target1e-12','points':[[r['degree'],-12] for r in rows]}]}
    for key in ('C_coupling','C_volume'):
        plots[key]=c['plots'][key]
        shutil.copyfile(HERE/c['plot_files'][key],DIST/plots[key]['csv'].lstrip('/'))
    reviews=[]
    for phase,g in gates.items():
        reviews += [{'name':phase+' producer','status':str(g['author_checks'])+' producer gates passed','scope':'Author checks, normal and optimized counted once; see exact phase evidence.'},
                    {'name':phase+' independent reviewer','status':str(g['independent_checks'])+' independent gates passed','scope':'Separate reconstruction and semantic/domain controls; shared declared model assumptions.'}]
    reviews+=c.get('additional_reviews',[])
    reviews.append({'name':'Independent proof admission review','status':str(review['checks_count'])+' independent gates passed','scope':'Actual open-premise injection, all declaration mutations, exact evidence, two-front meetings and separate saturation/replay; normal and optimized counted once.'})
    reviews.append({'name':'Bidirectional planner','status':'Actual routes and withdrawal controls passed','scope':'Independent arithmetic admission and ordered rule replay; conventional analysis, not a formal theorem kernel.'})
    failures=[{'finding':'Changing allowed initial hypotheses could admit an unproved generator premise despite fresh arithmetic.','action':'Freeze and revalidate hypotheses, gates, open premises, statements and rules together; independent mutation replay now rejects the original failure.','limit':'A conventional proof planner still relies on reviewed mathematical premises and is not a formal proof assistant.'},{'finding':'A1 exact midpoints were positive, all eight coarse cells insufficient.','action':'Refined failed radii; final21 cells cover every endpoint.','limit':'No sign claim beyond the declared finite interval.'},
      {'finding':'A capped refinement may finish without a positive cover.','action':'Iteration and cell caps report insufficient; forged success is rejected.','limit':'A code cap is not a mathematical nonexistence theorem.'},
      {'finding':'Whole-face reversal does not create a wrong SU(2) trace.','action':'Verify reversal invariance and use one wrong dagger as a discriminating control.','limit':'The exact graph/action must stay matched.'},
      {'finding':'Six independent face factors omit the cube surface constraint.','action':'Keep d^-4 character gluing and certify both baseline tails.','limit':'This formula is not an arbitrary-volume lattice oracle.'},
      {'finding':'A sixth common-coupling derivative is not the six distinct-face insertion.','action':'Differentiate the six coefficients separately before setting them equal.','limit':'The two observables differ already at Haar.'}]+c['failures']
    network={'nodes':[{'id':'plan','label':'Advisor–skeptic planning gate','status':'three revised contracts','x':430,'y':40,'route':'cycle-map'}]+[
       {'id':phase,'label':phase+' · '+label,'status':status,'x':x,'y':y,'route':route} for phase,label,status,x,y,route in [
        ('A1','coarse cover','insufficient margins retained',145,155,'range-cover'),('B1','closed cube','graph and Haar identities accepted',430,155,'cube-graph'),('C1','physical gap','finite bound; uniform goal open',715,155,'spectral-audit'),
        ('A2','adaptive cover','entire original interval accepted',145,285,'range-cover'),('B2','exact integral','nonfactorization certified',430,285,'cube-certificate'),('C2','trial improvement','finite side result accepted',715,285,'spectral-audit')]]+
       [{'id':'next','label':'Advisor: next bounded roadmap','status':'original uniform and continuum gaps retained','x':430,'y':435,'route':'cycle-roadmap'}],
       'edges':[{'from':a,'to':b} for a,b in [('plan','A1'),('plan','B1'),('plan','C1'),('A1','A2'),('B1','B2'),('C1','C2'),('B1','C2'),('A2','next'),('B2','next'),('C2','next')]]}
    nextgoals=[{'id':'1 · Local constants','forward':'Track source-specific local norm and combinatorial constants.','backward':'Demand a threshold independent of plaquette count.','gate':'A global sum|lambda| bound does not complete the original uniform goal.'},
      {'id':'2 · Two cubes','forward':'Derive explicit higher-incidence link integrals on the adjacent-cube graph.','backward':'Reject unproved transfer of the one-sphere character formula.','gate':'One independently verified new coefficient before a nonzero-coupling certificate.'},
      {'id':'3 · Physical spectral refinement','forward':'Derive exact larger trial matrices and complementary-subspace estimates.','backward':'Separate the ground upper bound from the full excited lower bound.','gate':'A Galerkin gap or guessed Gibbs vacuum cannot certify the full physical gap.'}]
    data={'round':15,'team_size':3,'planning_loops':1,'research_loops':6,'loops_per_goal':2,'metrics':{
       'A_summary':f"All eta in [1/8,1/4] are covered at k1=k2=1. Failed-cell refinement8→16→21 yields minimum exact lower margin about {float(Q(a['minimum_lower'])):.9g}, with degree24 fixed.",
       'B_summary':f"At common k=1/4, the six-face trace expectation is about {float(sum(map(Q,bc['enclosures']['expectation']))/2):.16g}, with exact enclosure width {float(Q(bc['expectation_width'])):.6g}. Partition excess over independent faces has certified lower bound about {float(Q(bc['enclosures']['partition_excess'][0])):.9g}.",
       'B_graph_summary':'All64 distinct-face subsets,36 Gram entries and216 repeated triple moments were checked; any five face class observables factorize under Haar, while the six-face product does not.',
       'B_equation':decimal(bc['enclosures']['expectation'][0])+' <= E[product of six x_f] <= '+decimal(bc['enclosures']['expectation'][1],up=True)+'\nCommon k=1/4; total Taylor degree24',
       'C_summary':c['summary'],'C_equation':c['equation']},
       'documents':documents,'planning':planning,'loops':loops,'feedback':feedback,'goals':goals,'routes':[{'name':n,'status':r['result']['status'],'steps':r['result'].get('certified_cost')} for n,r in proof['routes'].items()],
       'next':nextgoals,'reviews':reviews,'failures':failures,'sources':read('advisor/sources.json')['sources'],'plots':plots,'network':network}
    (HERE/'current_roadmap.json').write_text(json.dumps({'team_size':3,'planning_loops':1,'completed_research_loops':6,'loops_per_goal':2,'goals':goals,'next':nextgoals},indent=2)+'\n')
    (HERE/'site-data.json').write_text(json.dumps(data,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
    (DIST/'research-cycles-data.js').write_text('window.OBSERVATORY_CYCLES = '+json.dumps(data,ensure_ascii=False,allow_nan=False)+';\n')
    shutil.copyfile(HERE/'forward/A2/output/final_cover.json',DIST/'research-round15-cover.json')
    shutil.copyfile(HERE/'forward/B2/output/certificates.json',DIST/'research-round15-cube.json')
    print(json.dumps({'status':'built','loops':6,'pages':8,'plots':len(plots),'goals':3}))
if __name__=='__main__':main()
