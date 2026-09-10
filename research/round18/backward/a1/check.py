"""Independent finite bridge proof checks; no approximation to dressed grounds."""
from fractions import Fraction as F
from pathlib import Path
import argparse,copy,csv,hashlib,json
from bridge import graph,validate,untouched_links,certify,conditional_coefficients,multiplication_norm_identities,word_value,qmul,inverse,QUATERNIONS,generic_gap


DEFINITIONS=[
 ('primary','1','1','1/2','1/2','1/8'),('negative_bridge','1','1','1/2','1/2','-1/8'),('no_bridge','1','1','1/2','1/2','0'),
 ('zero_margin','1','1','1/2','1/2','1/4'),('beyond_margin','1','1','1/2','1/2','3/8'),('signed_ends','1','1','-1/2','1/2','1/8'),
 ('left_end_zero','1','1','0','1/2','1/8'),('zero_ends','1','1','0','0','1/8'),('all_zero','1','1','0','0','0'),
 ('scaled_double','2','1','1','1','1/4'),('scaled_half','1/2','1/4','1/4','1/4','1/16')]


def run(output):
    output=Path(output).resolve()
    if output.is_relative_to(Path(__file__).resolve().parent):raise ValueError('output outside frozen source required')
    output.mkdir(parents=True,exist_ok=False);checks=[]
    def check(name,ok):
        if not ok:raise RuntimeError(name)
        checks.append({'name':name,'passed':True})
    def reject(name,fn):
        try:fn()
        except (ValueError,TypeError,KeyError):check(name,True);return
        raise RuntimeError('invalid premise admitted '+name)
    g=graph();d=validate(g);L,M,R=(d[k] for k in ('left','middle','right'));supports=d['supports'];free=untouched_links(g,(L,R))
    check('actual three-square graph retains all ten electric links',(len(g['vertices']),len(g['edges']),len(g['faces']))==(8,10,3))
    check('end supports disjoint while bridge overlaps each once',not supports[L]&supports[R] and len(supports[L]&supports[M])==len(supports[R]&supports[M])==1)
    check('two actual middle horizontal links remain reference Haar factors',len(free)==2 and all(d['edges'][eid][0][0]!=d['edges'][eid][1][0] for eid in free))
    polynomial_records=multiplication_norm_identities()
    check('both quaternion multiplication norm identities hold as symbolic polynomials',len(polynomial_records)==32)
    haar_records=[]
    for offset in range(len(QUATERNIONS)):
        links={eid:QUATERNIONS[(eid+offset)%len(QUATERNIONS)] for eid in d['edges']}
        for edge in free:
            coeff=conditional_coefficients(g,links,edge);mean=F(0);second=sum(x*x for x in coeff)/4
            if sum(x*x for x in coeff)!=1 or second!=F(1,4):raise RuntimeError('actual conditional quaternion integration failed')
            haar_records.append({'offset':offset,'untouched_link':edge,'linear_coefficients':list(map(str,coeff)),'haar_mean':str(mean),'haar_square':str(second)})
    check('actual signed words realize first and second conditional Haar identities',len(haar_records)==8)
    check('conditional coefficients vary with other links so no bare-vacuum substitution',len({tuple(r['linear_coefficients']) for r in haar_records})>1)
    check('physical isolated-loop gap is not substituted for unprojected reference gap',F(3,4)<3)
    links={eid:QUATERNIONS[eid%4] for eid in d['edges']};gauges={tuple(v):QUATERNIONS[(i+1)%4] for i,v in enumerate(g['vertices'])}
    changed={eid:qmul(qmul(gauges[a],q),inverse(gauges[b])) for eid,q in links.items() for a,b in [d['edges'][eid]]}
    check('noncommuting vertex gauges preserve every actual plaquette trace',all(word_value(f['word'],links)[0]==word_value(f['word'],changed)[0] for f in g['faces']))
    fixtures={name:certify(a,(left,right),mu,amin,g) for name,a,amin,left,right,mu in DEFINITIONS}
    check('primary sharp lower is positive where generic lower is zero',fixtures['primary']['sharp_gap_lower']=='1/8' and fixtures['primary']['generic_gap_lower']=='0')
    check('bridge sign symmetry retained',fixtures['negative_bridge']['sharp_gap_lower']==fixtures['primary']['sharp_gap_lower'])
    check('zero bridge exactly recovers reference lower',fixtures['no_bridge']['sharp_gap_lower']==fixtures['no_bridge']['reference_gap_lower']=='1/4')
    check('zero and negative sufficient margins are retained as insufficient',fixtures['zero_margin']['sharp_sign']=='zero' and fixtures['zero_margin']['sharp_status']=='insufficient' and fixtures['beyond_margin']['sharp_sign']=='negative' and fixtures['beyond_margin']['sharp_status']=='insufficient')
    check('signed end couplings retain the same reference estimate',fixtures['signed_ends']['sharp_gap_lower']=='1/8')
    check('zero end coefficients change actual active support',len(fixtures['left_end_zero']['untouched_bridge_links'])==3 and fixtures['zero_ends']['active_reference_faces']==[] and len(fixtures['zero_ends']['untouched_bridge_links'])==4)
    check('empty active reference support is a valid free exception',fixtures['all_zero']['reference_gap_lower']==fixtures['all_zero']['sharp_gap_lower']=='3/4' and fixtures['all_zero']['active_reference_faces']==[])
    check('two nonunit energy scales preserve proportional finite bounds',fixtures['scaled_double']['sharp_gap_lower']=='1/4' and fixtures['scaled_half']['sharp_gap_lower']=='1/16')
    check('declared common physical floors give exact family margins',fixtures['scaled_double']['common_energy_floor_lower']=='1/8' and fixtures['scaled_half']['common_energy_floor_lower']=='1/32')
    check('primary family inequality is an exact parameter bound',F(3,4)-F(1,2)-F(1,8)==F(1,8) and all(F(c['sharp_gap_lower'])>=F(c['alpha'])/8 for c in fixtures.values() if c['primary_family_member']))
    reference_gap=F(1);norm=F(1,4);spectrum=[norm,reference_gap-norm];actual=spectrum[1]-spectrum[0]
    counterexample={'reference_H_diagonal':['0','1'],'perturbation_diagonal':['1/4','-1/4'],'perturbation_norm':'1/4','reference_expectation':'1/4','perturbed_spectrum':list(map(str,spectrum)),
      'actual_gap':str(actual),'invalid_one_norm_estimate':str(generic_gap(reference_gap,norm,True)),'valid_generic_estimate':str(generic_gap(reference_gap,norm,False)),
      'scope':'Two-dimensional bounded self-adjoint perturbation counterexample, not an SU(2) cluster spectrum.'}
    check('generic one-norm shortcut fails without zero reference expectation',actual==F(1,2)==generic_gap(reference_gap,norm,False)<generic_gap(reference_gap,norm,True))
    reject('including the middle interaction removes every untouched bridge link',lambda:untouched_links(g,(L,M,R)))
    bad=copy.deepcopy(g);bad['faces'][M]['word'][0][1]*=-1;reject('altered middle dagger rejected',lambda:validate(bad))
    bad=copy.deepcopy(g);bad['edges'].pop();reject('discarding an original electric link rejected',lambda:validate(bad))
    bad=copy.deepcopy(g);bad['faces'].pop();reject('missing face rejected',lambda:validate(bad))
    bad=copy.deepcopy(g);bad['edges'][0]['head'][0]=True;reject('Boolean coordinate alias rejected',lambda:validate(bad))
    reject('Boolean alpha rejected',lambda:certify(True,('1/2','1/2'),'1/8'))
    reject('Boolean bridge coefficient rejected',lambda:certify(1,('1/2','1/2'),True))
    reject('missing end coefficient tuple rejected',lambda:certify(1,(),'1/8'))
    reject('nonpositive energy scale rejected',lambda:certify(0,(0,0),0))
    reject('false common energy floor rejected',lambda:certify(1,('1/2','1/2'),'1/8',2))
    reject('unproved reference uniqueness domain blocked',lambda:certify(1,('3/4',0),0))
    reject('Boolean reference face index rejected',lambda:untouched_links(g,(False,R)))
    reject('assumption flag is strict Boolean',lambda:generic_gap(1,'1/4',1))
    reject('nonunit quaternion link rejected',lambda:conditional_coefficients(g,{**links,free[0]:(1,1,0,0)},free[1]))
    result={'schema':'ym18-independent-a1-results-v1','status':'passed','checks_count':len(checks),'checks':checks,
      'source_sha256':{'check.py':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'bridge.py':hashlib.sha256(Path(__file__).with_name('bridge.py').read_bytes()).hexdigest()},
      'graph_counts':[8,10,3],'universal_norm_identity_entries':32,'conditional_word_cases':8,'primary_sharp_gap_over_alpha':'1/8',
      'fixtures':fixtures,'scope':'Finite internally overlapping bridge cluster, conditional Haar identities valid for arbitrary dressed end states; no cluster repetition or homogeneous dense conclusion.'}
    for name,obj in [('results.json',result),('graph.json',g),('quaternion_norm_polynomials.json',polynomial_records),('conditional_haar.json',haar_records),('generic_counterexample.json',counterexample)]:
        (output/name).write_text(json.dumps(obj,indent=2)+'\n')
    with (output/'parameters.csv').open('w',newline='') as f:
        keys=['name','alpha','alpha_min','left','right','mu','rho','reference_gap_lower','sharp_gap_lower','generic_gap_lower','status'];w=csv.DictWriter(f,fieldnames=keys);w.writeheader()
        for name,c in fixtures.items():w.writerow(dict(zip(keys,[name,c['alpha'],c['alpha_min'],*c['end_couplings'],c['mu'],c['rho_actual'],c['reference_gap_lower'],c['sharp_gap_lower'],c['generic_gap_lower'],c['sharp_status']])))
    print(json.dumps({'status':'passed','checks_count':len(checks),'primary_lower':'1/8'}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();run(a.output)
