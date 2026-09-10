"""Run A1 exact checks; write only to a separate output directory."""
import argparse,copy,csv,hashlib,json
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import projectors as p

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
    source=Path(__file__).resolve().parent;out=Path(args.output).resolve()
    if out==source or source in out.parents:raise ValueError('output must be outside frozen source directory')
    out.mkdir(parents=True,exist_ok=True);checks=[];controls=[]
    def check(name,ok):
        if not ok:raise RuntimeError(name)
        checks.append(name)
    def reject(name,fn):
        try:fn()
        except (ValueError,TypeError,KeyError):controls.append(name);return
        raise RuntimeError('invalid accepted: '+name)
    moments={str(n):str(p.trace_haar_moment(n)) for n in range(5)}
    check('Haar mean zero',moments['1']=='0')
    check('Haar norm squared1/4',moments['2']=='1/4')
    check('Haar cubic zero',moments['3']=='0')
    check('normalized fundamental character norm1',4*p.trace_haar_moment(2)==1)
    check('offdiagonal ranktwo square exactly1/4',F(1,2)**2==F(1,4))
    occupancy=[]
    for bits in product((0,1),repeat=4):
        q=1
        for x in bits:q*=1-x
        Q=1-q;total=sum(bits)
        if Q>total:raise RuntimeError('projector inequality false')
        occupancy.append({'link_excitation_flags':list(bits),'Qp':Q,'sum_qe':total})
    check('all16joint-projector sectors satisfy inequality',len(occupancy)==16)
    casimirs=[]
    for twicej in range(9):
        j=F(twicej,2);C=j*(j+1);q=int(j>0)
        check('electric-projector ratio spin'+str(j),q<=F(4,3)*C)
        casimirs.append({'j':str(j),'Casimir':str(C),'q':q})
    trials=[]
    for alpha,lam,t in [('1','1/2','0'),('1','0','0'),('1','0','1/8'),('1','1/2','1/4'),('1','1/2','-1/4'),('1','-1/2','1/4'),('2','-1/2','-1/8')]:
        c=p.trial(alpha,lam,t);check('trial replay '+str((alpha,lam,t)),p.verify_trial(c));trials.append(c)
    check('zero-free-energy ratio is unavailable',trials[0]['absolute_relative_ratio'] is None)
    check('nonzero vacuum image retained',trials[0]['vacuum_image_norm_squared']=='1/16')
    check('zero coupling removes obstruction',trials[2]['absolute_relative_ratio']=='0')
    check('signed t reverses magnetic expectation',F(trials[3]['magnetic_energy'])==-F(trials[4]['magnetic_energy']))
    check('signed lambda reverses magnetic expectation',F(trials[3]['magnetic_energy'])==-F(trials[5]['magnetic_energy']))
    relative=[]
    for bound in [1,8,64]:
        t=F(1,2)/(6*bound);c=p.trial('1','1/2',str(t));ratio=F(c['absolute_relative_ratio'])
        check('pure relative shortcut fails proposed'+str(bound),ratio==2*bound and ratio>bound)
        relative.append({'claimed_bound':str(bound),'trial_t':str(t),'actual_ratio':str(ratio),'status':'counterexample'})
    sequence=[]
    for k in [1,2,4,8,16,32]:
        c=p.trial('1','1/2',str(F(1,2**k)))
        sequence.append({'k':k,'t':c['t'],'free_energy':c['free_energy'],'magnetic_energy':c['magnetic_energy'],'ratio':c['absolute_relative_ratio']})
    check('exact small-t ratio doubles with inverse t',all(F(r['ratio'])==F(2**r['k'],6) for r in sequence))
    graphs=[]
    for n in [2,3,4]:
        a=p.graph_audit(n);graphs.append(a)
        check('openbox exact counts'+str(n),a['vertices']==n**3 and a['edges']==3*n*n*(n-1) and a['plaquettes']==3*n*(n-1)**2)
        check('incidence bound'+str(n),a['maximum_link_incidence']<=4)
        check('plaquette-overlap bound'+str(n),a['maximum_overlapping_plaquettes_including_self']<=13)
    check('bulk incidence constant attained',graphs[-1]['maximum_link_incidence']==4)
    check('bulk overlapping bound attained',graphs[-1]['maximum_overlapping_plaquettes_including_self']==13)
    g=p.box(3);relations=[p.overlap(g,'01:0,0,0','01:1,0,0'),p.overlap(g,'01:0,0,0','01:1,1,0')]
    check('shared-link and shared-vertex distinguished',[r['relation'] for r in relations]==['shared-link','shared-vertex-only'])
    constants=p.local_constants('2','-1/2')
    check('diagonal form energy and relativeunits',constants['diagonal_form_coefficient_against_sum_C']=='8/3' and constants['diagonal_relative_coefficient_against_H0']=='4/3')
    check('local and physical gaps distinguished',constants['full_link_free_gap']=='3/2' and constants['fundamental_loop_energy']=='6')
    for name,fn in [
      ('zero alpha',lambda:p.trial('0','1','1')),('negative alpha',lambda:p.trial('-1','1','1')),
      ('Boolean alpha',lambda:p.trial(True,'1','1')),('float lambda',lambda:p.trial('1',.5,'1')),
      ('Boolean t',lambda:p.trial('1','1',True)),('nonfinite t',lambda:p.trial('1','1','NaN')),
      ('noncanonical rational',lambda:p.trial('1','2/4','1')),('Boolean extent',lambda:p.box(True)),
      ('extent-one excluded contract',lambda:p.box(1)),('box implementation cap',lambda:p.box(13)),
      ('Boolean Haar degree',lambda:p.trace_haar_moment(True)),('invalid plaquette identifier',lambda:p.overlap(g,'missing','01:0,0,0'))]:reject(name,fn)
    for name,mut in [
      ('duplicate plaquette',lambda a:a['plaquettes'].append(copy.deepcopy(a['plaquettes'][0]))),
      ('missing link',lambda a:a['edges'].pop()),
      ('wrong single dagger',lambda a:a['plaquettes'][0]['word'][0].update(sign=-a['plaquettes'][0]['word'][0]['sign'])),
      ('Boolean sign',lambda a:a['plaquettes'][0]['word'][0].update(sign=True)),
      ('changed Gauss contract',lambda a:a.update(Gauss='boundary charges allowed'))]:
        a=copy.deepcopy(g);mut(a);reject(name,lambda a=a:p.validate_graph(a))
    for name,mut in [('wrongfactor',lambda a:a.update(magnetic_energy='-1')),('forgedvacuumratio',lambda a:a.update(absolute_relative_ratio='0')),('unphysicalscope',lambda a:a.update(scope='independent face spins'))]:
        a=copy.deepcopy(trials[0] if name=='forgedvacuumratio' else trials[3]);mut(a);reject(name,lambda a=a:p.verify_trial(a))
    data={'schema':'ym17-a1-evidence-v1','source_sha256':p.SOURCE_SHA,'moments':moments,'occupancy':occupancy,'casimir_checks':casimirs,
          'local_constants':constants,'trials':trials,'relative_counterexamples':relative,'small_t_sequence':sequence,'graphs':graphs,'support_relations':relations,
          'dense_uniform_gap_status':'open; diagonal form bound leaves vacuum offdiagonal component uncontrolled','next_loop_status':'not executed'}
    (out/'evidence.json').write_text(json.dumps(data,indent=2)+'\n')
    with (out/'small_t.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(sequence[0]));w.writeheader();w.writerows(sequence)
    with (out/'incidence.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(graphs[0]));w.writeheader();w.writerows(graphs)
    result={'schema':'ym17-a1-results-v1','status':'passed','checks_count':len(checks)+len(controls),'positive_checks_count':len(checks),'control_count':len(controls),'gate_count':len(checks)+len(controls),
            'checks':checks+['reject: '+name for name in controls],'rejected_controls':controls,'source_sha256':p.SOURCE_SHA,'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'evidence_sha256':hashlib.sha256((out/'evidence.json').read_bytes()).hexdigest(),'scientific_scope':'Exact local projector/overlap constants and physical relative-bound counterexample; no dense uniform gap theorem'}
    (out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    files=['evidence.json','small_t.csv','incidence.csv','results.json']
    (out/'manifest.json').write_text(json.dumps({'schema':'ym17-a1-output-manifest-v1','files':{x:hashlib.sha256((out/x).read_bytes()).hexdigest() for x in files}},indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('checks','rejected_controls')},indent=2))
if __name__=='__main__':main()
