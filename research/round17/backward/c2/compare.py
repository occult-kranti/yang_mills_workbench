"""Independent complete C2 producer collection replay by angular/radial integration."""
from pathlib import Path
from fractions import Fraction as F
import argparse,copy,hashlib,json
from geometry import graph,validate,boundary,strict,TETRA
from angular import COMMUTING,data,comparison,encoded,multiply,adjoint,radial_data

def named_graph():
    g=graph();data=validate(g);name=lambda v:','.join(map(str,v));enames={};edges=[]
    for e in g['edges']:
        axis=next(a for a in range(3) if e['tail'][a]!=e['head'][a]);eid='e'+str(axis)+':'+name(e['tail']);enames[e['id']]=eid
        edges.append({'id':eid,'tail':name(e['tail']),'head':name(e['head']),'axis':axis})
    def key(f):
        base=[min(v[a] for v in f['vertices']) for a in range(3)];normal=next(a for a in range(3) if all(v[a]==base[a] for v in f['vertices']))
        return normal,tuple(base)
    ordered=sorted(g['faces'],key=key);faces=[];fnames={};cellnames=['c:'+name([x,y,0]) for x in range(2) for y in range(2)]
    for f in ordered:
        normal,base=key(f);fid='f'+str(normal)+':'+name(base);fnames[f['id']]=fid
        faces.append({'id':fid,'normal':normal,'base':list(base),'vertices':[name(v) for v in f['vertices']],
          'word':[{'edge':enames[eid],'sign':sign} for eid,sign in f['word']],
          'incident_cells':[cellnames[i] for i,c in enumerate(data['cells']) if f['id'] in c]})
    cells=[]
    for i,(x,y) in enumerate(( (x,y) for x in range(2) for y in range(2))):
        cells.append({'id':cellnames[i],'base':[x,y,0],'faces':[f['id'] for f in faces if cellnames[i] in f['incident_cells']]})
    return {'schema':'ym17-four-cube-complex-v1','vertices':[name(v) for v in g['vertices']],'edges':edges,'faces':faces,'cells':cells,
      'group':'SU(2)','measure':'normalized Haar on the central link conditional on all other links',
      'scope':'Static conditional central-link tensor; not a bulk amplitude or a physical Hamiltonian gap'}


def convert(fg):
    coords=lambda v:list(map(int,v.split(',')));emap={e['id']:i for i,e in enumerate(fg['edges'])}
    return {'schema':'ym17-independent-four-cube-v1','vertices':[coords(v) for v in fg['vertices']],
      'edges':[{'id':i,'tail':coords(e['tail']),'head':coords(e['head'])} for i,e in enumerate(fg['edges'])],
      'faces':[{'id':i,'vertices':[coords(v) for v in f['vertices']],'word':[[emap[t['edge']],t['sign']] for t in f['word']]} for i,f in enumerate(fg['faces'])]}


SCOPE='Finite central-link conditional integral on the actual four-cube graph, axis-aligned action, normalized adjoint product; not a bulk result or a physical spectral gap'
COLLECTION_SCOPE='Same central action and partition with distinct boundary-dependent joint observables; no action-only observable closure or bulk/spectral conclusion'


def realization(H):
    fg=named_graph();g=convert(fg);links,paths,_=boundary(g,H);enames={i:e['id'] for i,e in enumerate(fg['edges'])};records=[]
    for path,h in zip(paths,H):
        records.append({'face_id':fg['faces'][path['face']]['id'],'edge':enames[path['assigned_edge']],
          'sign':next(sign for eid,sign in path['word'] if eid==path['assigned_edge']),'target_H':list(map(str,h))})
    return {'chosen_links':records,'all_link_assignments':{enames[eid]:list(map(str,q)) for eid,q in links.items()}}


def expected_certificate(H,ks,n,source_sha,geometry_sha):
    d=data(H,tuple(ks),n);poly={(0,0,0,0):F(1)}
    for h in H:poly=multiply(poly,adjoint(h))
    dirs=d['directions'];lo,hi=d['expectation_interval']
    return {'schema':'ym17-axis-conditional-v1','source_sha256':source_sha,'geometry_source_sha256':geometry_sha,
      'boundary_H':encoded(d['boundary']),'kappas':encoded(d['coefficients']),'degree':n,'trace_directions':encoded(dirs),
      'direction_gram':[[str(sum(x*y for x,y in zip(p,q))) for q in dirs] for p in dirs],
      'action_vector':encoded(d['b']),'action_magnitude':str(d['M']),'action_branch':'zero-vector Haar' if not d['M'] else 'scalar-axis',
      'observable_polynomial':[[list(p),str(c)] for p,c in sorted(poly.items())],
      'numerator_coefficients':encoded(d['A_coefficients']),'partition_coefficients':encoded(d['Z_coefficients']),
      'numerator_partial':str(d['A_value']),'partition_partial':str(d['Z_value']),'tail':str(d['tail']),
      'numerator_interval':encoded(d['A_interval']),'partition_interval':encoded(d['Z_interval']),
      'expectation_interval':encoded(d['expectation_interval']),'width':str(d['width']),'precision':'1/1000000000000',
      'precision_status':'target-met' if d['precision_status']=='met' else 'insufficient-width',
      'sign_status':'positive' if lo>0 else 'negative' if hi<0 else 'sign-inconclusive',
      'actual_boundary_realization':realization(H),'scope':SCOPE}


def expected_collection(source_sha,geometry_sha):
    refinements=[]
    for n in (0,4,8,12,16):
        t=expected_certificate(TETRA,('1/8',)*4,n,source_sha,geometry_sha);c=expected_certificate(COMMUTING,('1/8',)*4,n,source_sha,geometry_sha);d=comparison('1/8',n)
        contrast={'degree':n,'definition':'commuting expectation minus tetrahedral expectation','common_action_vector':t['action_vector'],
          'common_partition_interval':t['partition_interval'],'numerator_difference_partial':str(d['C']['A_value']-d['T']['A_value']),
          'numerator_difference_tail':str(d['T']['tail']+d['C']['tail']),'interval':encoded(d['contrast_interval']),'width':str(d['contrast_width']),
          'sign_status':'positive' if d['contrast_interval'][0]>0 else 'negative' if d['contrast_interval'][1]<0 else 'sign-inconclusive',
          'precision_status':'target-met' if d['precision_status']=='met' else 'insufficient-width'}
        accepted=t['precision_status']==c['precision_status']==contrast['precision_status']=='target-met' and t['sign_status']=='negative' and c['sign_status']==contrast['sign_status']=='positive'
        refinements.append({'degree':n,'tetrahedral':t,'commuting':c,'contrast':contrast,'status':'accepted' if accepted else 'insufficient'})
    fixtures=[]
    for name,H,ks in [('zero_tetrahedral',TETRA,('0',)*4),('zero_commuting',COMMUTING,('0',)*4),('negative_tetrahedral',TETRA,('-1/8',)*4),('negative_commuting',COMMUTING,('-1/8',)*4),('half_tetrahedral',TETRA,('1/16',)*4),('half_commuting',COMMUTING,('1/16',)*4),('zero_b_nonzero_coefficients',COMMUTING,('1/8','-1/8','1/8','1/8'))]:
        fixtures.append({'id':name,'certificate':expected_certificate(H,ks,16,source_sha,geometry_sha)})
    _,individual=radial_data(TETRA)
    final=refinements[-1];cached=final['tetrahedral']['expectation_interval'];actual=final['commuting']['expectation_interval']
    shortcut={'definition':'cache the joint observable using only b and reuse the tetrahedral value for the commuting boundary',
      'same_action':final['tetrahedral']['action_vector']==final['commuting']['action_vector'],
      'same_partition':final['tetrahedral']['partition_interval']==final['commuting']['partition_interval'],
      'predicted_commuting_interval':cached,'actual_commuting_interval':actual,
      'intervals_disjoint':F(cached[1])<F(actual[0]) or F(actual[1])<F(cached[0]),
      'status':'rejected' if F(cached[1])<F(actual[0]) else 'not-resolved'}
    return {'schema':'ym17-c2-collection-v1','source_sha256':source_sha,'degree_sequence':[0,4,8,12,16],'precision':'1/1000000000000',
      'refinements':refinements,'fixtures':fixtures,'tetrahedral_individual_angular_polynomials':[[str(p.get(0,F(0))),str(p.get(2,F(0)))] for p in individual],
      'action_only_cache_control':shortcut,
      'status':refinements[-1]['status'],'scope':COLLECTION_SCOPE}


def main(source,evidence,output):
    source,evidence,output=map(Path,(source,evidence,output));output=output.resolve()
    if output.is_relative_to(Path(__file__).resolve().parent):raise ValueError('output outside source required')
    output.mkdir(parents=True,exist_ok=False);h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();r=json.loads((evidence/'collection.json').read_text())
    expected=expected_collection(h(source/'conditional.py'),h(source/'geometry.py'));checks=[]
    def check(name,ok):
        if not ok:raise RuntimeError(name)
        checks.append({'name':name,'passed':True})
    def verify(c):
        if not strict(c,expected):raise ValueError('independent angular/radial complete replay differs')
        return True
    check('exact complete collection shape and fixed parameters',set(r)==set(expected) and r['degree_sequence']==[0,4,8,12,16] and r['precision']=='1/1000000000000' and [f['id'] for f in r['fixtures']]==[f['id'] for f in expected['fixtures']])
    for level,wanted in zip(r['refinements'],expected['refinements']):check('both full conditional certificates and common-denominator contrast degree '+str(wanted['degree']),strict(level,wanted))
    for fixture,wanted in zip(r['fixtures'],expected['fixtures']):check('complete source-bound fixture '+wanted['id'],strict(fixture,wanted))
    check('all angular zeros derived and complete scope admitted',verify(r))
    mutations=[]
    bad=copy.deepcopy(r);bad['refinements'][-1]['commuting']['numerator_coefficients']=bad['refinements'][-1]['tetrahedral']['numerator_coefficients'];mutations.append(('same action used as wrong observable cache key',bad))
    bad=copy.deepcopy(r);bad['refinements'][2]['status']='accepted';mutations.append(('degree-eight precision failure relabeled passed',bad))
    bad=copy.deepcopy(r);bad['refinements'][-1]['contrast']['numerator_difference_tail']='0';mutations.append(('complete contrast remainder omitted',bad))
    bad=copy.deepcopy(r);bad['fixtures'][-1]['certificate']['action_branch']='scalar-axis';mutations.append(('zero-b nonzero-coefficient branch removed',bad))
    bad=copy.deepcopy(r);bad['refinements'][-1]['tetrahedral']['observable_polynomial'][0][1]='1';mutations.append(('normalized observable changed',bad))
    bad=copy.deepcopy(r);bad['refinements'][0]['degree']=False;mutations.append(('Boolean degree alias',bad))
    bad=copy.deepcopy(r);bad['source_sha256']='0'*64;mutations.append(('stale producer source binding',bad))
    bad=copy.deepcopy(r);bad['fixtures'].pop();mutations.append(('required zero-b fixture omitted',bad))
    for name,bad in mutations:
        try:verify(bad)
        except ValueError:check('reject '+name,True)
        else:raise RuntimeError('false conditional evidence admitted '+name)
    result={'schema':'ym17-independent-c2-comparison-v1','status':'passed','checks_count':len(checks),'checks':checks,
      'reviewed_input_sha256':{'producer/'+f:h(source/f) for f in ('conditional.py','geometry.py','check.py','report.md')},'producer_evidence_sha256':h(evidence/'collection.json'),
      'discrepancies':[],'scope':'Five complete refinement records and seven required parameter fixtures reconstructed through S2 angular reduction and semicircle moments, with full source/geometry/boundary/observable/interval bindings.'}
    (output/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'passed','checks_count':len(checks)}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--producer',required=True);p.add_argument('--evidence',required=True);p.add_argument('--output',required=True);a=p.parse_args();main(a.producer,a.evidence,a.output)
