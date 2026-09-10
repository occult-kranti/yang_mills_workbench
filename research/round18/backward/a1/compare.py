"""Independent complete comparison of the signed strip and bridge certificates."""
from pathlib import Path
from fractions import Fraction as F
import argparse,copy,hashlib,json
from bridge import graph,validate,certify,untouched_links
from check import DEFINITIONS


def strict(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return set(a)==set(b) and all(strict(a[k],b[k]) for k in a)
    if type(a) in (tuple,list):return len(a)==len(b) and all(strict(x,y) for x,y in zip(a,b))
    return a==b


def named_graph():
    g=graph();name=lambda v:','.join(map(str,v));edges=[];emap={}
    for e in g['edges']:
        axis=next(i for i in (0,1) if e['head'][i]!=e['tail'][i]);eid=('ex:' if axis==0 else 'ey:')+name(e['tail']);emap[e['id']]=eid
        edges.append({'id':eid,'tail':name(e['tail']),'head':name(e['head']),'axis':axis})
    faces=[]
    for f,label in zip(g['faces'],('left','middle','right')):
        faces.append({'id':label,'anchor':[min(v[0] for v in f['vertices']),0,0],'vertices':[name(v) for v in f['vertices']],
          'word':[{'edge':emap[eid],'sign':sign} for eid,sign in f['word']]})
    return {'schema':'ym18-three-square-strip-v1','vertices':[name(v) for v in g['vertices']],'edges':edges,'faces':faces,
      'reference_end_faces':['left','right'],'bridge_face':'middle','group':'SU(2)','measure':'independent normalized Haar on all ten links',
      'Hilbert':'full untruncated link Hilbert space first, then all-eight-vertex Gauss restriction',
      'electric_terms':'alpha times the Casimir on every one of the ten links','external_charges':False}


def expected_certificate(parameters,source_sha):
    if type(parameters) is not dict or set(parameters)!={'alpha','alpha_min','lambda_left','lambda_right','mu'} or any(type(v) is not str or str(F(v))!=v for v in parameters.values()):raise ValueError('complete canonical parameter dictionary required')
    a,amin,left,right,mu=(parameters[n] for n in ('alpha','alpha_min','lambda_left','lambda_right','mu'))
    c=certify(a,(left,right),mu,amin);g=graph();d=validate(g);fg=named_graph();emap={i:e['id'] for i,e in enumerate(fg['edges'])};fnames={0:'left',1:'middle',2:'right'}
    active=[fnames[i] for i in c['active_reference_faces']];used=set().union(*(d['supports'][i] for i in c['active_reference_faces'])) if active else set()
    gate={'active_reference_faces':active,'reference_support_overlap':False,'untouched_bridge_links':sorted(emap[i] for i in c['untouched_bridge_links']),
      'status':'proved-conditional-Haar-moments','conditional_first_moment':'0','conditional_second_moment':'1/4','norm_x_times_reference_ground':'1/2',
      'reason':'Haar invariance on an unused link; chi1 squared equals chi0 plus chi2'}
    bound=F(c['sharp_gap_lower']);primary=c['primary_family_member']
    return {'schema':'ym18-dressed-bridge-bound-v1','source_sha256':source_sha,
      'graph_sha256':hashlib.sha256(json.dumps(fg,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'parameters':{k:parameters[k] for k in sorted(parameters)},
      'actual_end_ratio':c['rho_actual'],'bridge_ratio':str(abs(F(mu))/F(a)),
      'active_reference_faces':active,'reference_free_edges':sorted(emap[i] for i in d['edges'] if i not in used),'haar_gate':gate,
      'reference_ground':'unique dressed product ground; wavefunction and absolute energy E_s not computed','reference_gap_lower':c['reference_gap_lower'],
      'bridge_offdiagonal_norm':c['bridge_offdiagonal_norm'],'bridge_offdiagonal_norm_squared':str(F(mu)**2/4),
      'full_E1_minus_Es_lower':str(bound),'full_E0_minus_Es_upper':'0','full_gap_lower':str(bound),'generic_two_norm_gap_lower':c['generic_gap_lower'],
      'bound_status':'positive' if bound>0 else 'zero-insufficient' if not bound else 'negative-insufficient',
      'ground_uniqueness_certified':bound>0,'physical_Gauss_inclusion_certified':bound>0,'primary_family_member':primary,
      'primary_family_bound_at_alpha':c['primary_parameter_family_lower'],'primary_family_common_bound':c['common_energy_floor_lower'],
      'scope':'Finite internally overlapping strip; full untruncated link bound followed by Gauss restriction; lower estimate not an actual computed spectrum; cluster repetition and dense uniform extensions unexecuted'}


def expected_collection(source_sha):
    fixtures=[]
    for name,a,amin,l,r,mu in DEFINITIONS:
        if name=='signed_ends':r='1/4'  # Author's additional unequal signed fixture, explicitly bound.
        p=dict(zip(('alpha','alpha_min','lambda_left','lambda_right','mu'),(a,amin,l,r,mu)))
        fixtures.append({'id':name,'certificate':expected_certificate(p,source_sha)})
    rows=[]
    for mu in ('-3/8','-1/4','-1/8','-1/16','0','1/16','1/8','1/4','3/8'):
        c=expected_certificate({'alpha':'1','alpha_min':'1','lambda_left':'1/2','lambda_right':'1/2','mu':mu},source_sha)
        rows.append({'mu_over_alpha':mu,'reference_lower':c['reference_gap_lower'],'generic_lower':c['generic_two_norm_gap_lower'],
                     'improved_lower':c['full_gap_lower'],'status':c['bound_status'],'primary_family_member':c['primary_family_member']})
    return {'schema':'ym18-a1-evidence-v1','source_sha256':source_sha,'graph':named_graph(),'fixtures':fixtures,'mu_rows':rows,
      'missing_untouched_link_gate':{'active_reference_faces':['middle'],'reference_support_overlap':False,'untouched_bridge_links':[],
        'status':'blocked-reference-factorization-or-free-link','conditional_first_moment':None,'conditional_second_moment':None,
        'norm_x_times_reference_ground':None,'reason':'the sharpened inference lacks its product-reference and untouched-link premises'},
      'generic_one_norm_counterexample':{'reference_H':[['0','0'],['0','1']],'perturbation':[['1/4','0'],['0','-1/4']],
        'perturbation_norm':'1/4','reference_expectation':'1/4','actual_gap':'1/2','generic_valid_lower':'1/2','invalid_one_norm_claim':'3/4',
        'invalid_claim_exceeds_actual_gap':True,'scope':'Finite counterexample to the generic one-norm shortcut when zero reference mean is absent'},
      'primary_family':{'end_ratio_max':'1/2','bridge_ratio_max':'1/8','gap_lower_over_alpha':'1/8','common_scale_required':'alpha >= alpha_min > 0'},
      'dressed_ground_wavefunctions_computed':False,'scope':'Finite bridge bound; A2 repetition and remaining-interaction extensions not executed'}


def verify_evidence(value,source_sha):
    if not strict(value,expected_collection(source_sha)):raise ValueError('independent complete evidence replay mismatch')
    return True


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--producer',type=Path,required=True);ap.add_argument('--evidence',type=Path,required=True);ap.add_argument('--output',type=Path,required=True)
    ns=ap.parse_args();out=ns.output.resolve();own=Path(__file__).resolve().parent
    if out==own or own in out.parents:raise ValueError('output must be outside frozen source directory')
    source=ns.producer.resolve();evidence=ns.evidence.resolve();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    source_sha=sha(source/'bridge.py');value=json.loads((evidence/'evidence.json').read_text());expected=expected_collection(source_sha);checks=[]
    def gate(name,condition):
        if type(condition) is not bool or not condition:raise ValueError(name)
        checks.append({'name':name,'passed':True})
    manifest=json.loads((source/'source-manifest.json').read_text())
    gate('frozen author source inventory is complete and hash correct',strict(manifest['files'],{name:sha(source/name) for name in ('bridge.py','check.py','report.md')}))
    gate('independently rebuilt entire signed graph agrees',strict(value['graph'],named_graph()))
    gate('required ordered fixture inventory is complete',strict([r['id'] for r in value['fixtures']],[r['id'] for r in expected['fixtures']]))
    for a,b in zip(value['fixtures'],expected['fixtures']):gate('independent full certificate: '+b['id'],strict(a,b))
    gate('all signed bridge scan rows agree',strict(value['mu_rows'],expected['mu_rows']))
    gate('missing actual unused link produces blocked null diagnostics',strict(value['missing_untouched_link_gate'],expected['missing_untouched_link_gate']))
    gate('generic invalid shortcut retains actual counterexample',strict(value['generic_one_norm_counterexample'],expected['generic_one_norm_counterexample']))
    gate('complete schema parameters premises sources and scope replay',verify_evidence(value,source_sha))
    mutations=[]
    def mutate(name,fn):
        bad=copy.deepcopy(value);fn(bad);mutations.append((name,bad))
    mutate('omitted scale fixture rejected',lambda v:v['fixtures'].pop())
    mutate('invented source digest rejected',lambda v:v.update(source_sha256='0'*64))
    mutate('hidden ground computation claim rejected',lambda v:v.update(dressed_ground_wavefunctions_computed=True))
    mutate('missing moment replaced by zero rejected',lambda v:v['missing_untouched_link_gate'].update(conditional_first_moment='0'))
    mutate('unproved endpoint physical inclusion rejected',lambda v:v['fixtures'][3]['certificate'].update(physical_Gauss_inclusion_certified=True))
    mutate('common physical floor changed rejected',lambda v:v['fixtures'][-1]['certificate'].update(primary_family_common_bound='1/16'))
    mutate('Boolean word sign alias rejected',lambda v:v['graph']['faces'][1]['word'][0].update(sign=True))
    mutate('reversed signed fixture label rejected',lambda v:v['fixtures'][1]['certificate']['parameters'].update(mu='1/8'))
    mutate('forged caller pass metadata rejected',lambda v:v.update(status='passed'))
    for name,bad in mutations:
        rejected=False
        try:verify_evidence(bad,source_sha)
        except ValueError:rejected=True
        gate(name,rejected)
    hashes={**{'producer/'+n:sha(source/n) for n in ('bridge.py','check.py','report.md','source-manifest.json')},'evidence/evidence.json':sha(evidence/'evidence.json'),
            **{'independent/'+n:sha(own/n) for n in ('bridge.py','check.py','compare.py')}}
    result={'schema':'ym18-independent-a1-comparison-v1','status':'passed','checks_count':len(checks),'checks':checks,'input_sha256':hashes,
      'oracle':'Own signed geometry, universal quaternion multiplication norm identities, conditional S3 moments and exact rational spectral inequalities; no author module imported.',
      'scope':'Complete finite strip fixture collection; zero and negative sufficient margins retained; arbitrary dressed reference supported by analytic conditional integral.'}
    out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'passed','checks_count':len(checks)}))


if __name__=='__main__':main()
