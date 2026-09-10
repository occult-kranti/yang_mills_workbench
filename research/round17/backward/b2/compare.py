"""Independent replay of the complete forward B2 tables and trial certificates."""
from pathlib import Path
from fractions import Fraction as F
import argparse,copy,hashlib,json
from check import geometry,entries,shared_face,compute

def strict(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return set(a)==set(b) and all(strict(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(strict(x,y) for x,y in zip(a,b))
    return a==b


def convert(g):
    vertices=[list(map(int,v.split(','))) for v in g['vertices']];emap={e['id']:i for i,e in enumerate(g['edges'])}
    edges=[{'id':i,'tail':list(map(int,e['tail'].split(','))),'head':list(map(int,e['head'].split(',')))} for i,e in enumerate(g['edges'])];faces=[]
    for i,f in enumerate(g['faces']):
        vs=[list(map(int,v.split(','))) for v in f['vertices']];spans=[max(v[a] for v in vs)-min(v[a] for v in vs) for a in range(3)]
        faces.append({'id':i,'axes':[a for a in range(3) if spans[a]],'base':[min(v[a] for v in vs) for a in range(3)],'vertices':vs,'word':[[emap[t['edge']],t['sign']] for t in f['word']]})
    return {'schema':'ym17-independent-dense-two-cube-v1','vertices':vertices,'edges':edges,'faces':faces}


SCOPE='Finite dense two-cube untruncated physical operator; independent full E1 lower minus actual Rayleigh E0 upper; no dense volume-uniform theorem and no physical gap upper bound'


def main(source,evidence,output):
    source,evidence,output=map(Path,(source,evidence,output));output=output.resolve()
    if output.is_relative_to(Path(__file__).resolve().parent):raise ValueError('output outside source required')
    output.mkdir(parents=True,exist_ok=False);h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
    r=json.loads((evidence/'evidence.json').read_text());fg=json.loads((source/'graph.json').read_text());g=convert(fg);inc,girth=geometry(g);s=shared_face(g);G,M,T,count=entries(g);mat=(G,M,T,count);checks=[]
    def check(name,ok):
        if not ok:raise RuntimeError(name)
        checks.append({'name':name,'passed':True})
    check('complete evidence schema and actual graph-derived shared face',set(r)=={'schema','source_sha256','gram_entries','individual_insertions','fixtures','amplitude_rows','positive_amplitude_interval','selected_amplitude','physical_common_coupling_ratio','dense_uniform_goal','C1'} and r['schema']=='ym17-b2-evidence-v1' and r['source_sha256']==h(source/'adjoint.py') and fg['shared_face']==fg['faces'][s]['id'] and girth==4)
    check('all 169 producer Gram entries independently reconstructed',strict(r['gram_entries'],[[i,j,str(G[i][j])] for i in range(13) for j in range(13)]))
    check('all 1859 producer magnetic entries independently reconstructed',strict(r['individual_insertions'],[[i,j,f,str(M[f][i][j])] for i in range(13) for j in range(13) for f in range(11)]))
    definitions=[('negative','1','-3/3817'),('zero','1','0'),('quarter','1','3/7634'),('selected','1','3/3817'),('three_quarters','1','9/7634'),('endpoint','1','6/3817'),('beyond','1','9/3817'),('scaled_double','2','3/3817'),('scaled_half','1/2','3/3817')]
    check('complete nine-fixture fixed parameter inventory',strict([(f['id'],f['certificate']['alpha'],f['certificate']['eta']) for f in r['fixtures']],definitions))
    def verify(c):
        if type(c) is not dict or type(c.get('alpha')) is not str or type(c.get('eta')) is not str:raise ValueError('strict certificate parameters required')
        a,t=F(c['alpha']),F(c['eta'])
        if a<=0 or str(a)!=c['alpha'] or str(t)!=c['eta']:raise ValueError('positive scale and canonical amplitude required')
        ours=compute(a,t,g,mat);E=[[a*x for x in row] for row in T];V=[[-a*F(12,43)*sum(M[f][i][j] for f in range(11)) for j in range(13)] for i in range(13)];H=[[E[i][j]+V[i][j] for j in range(13)] for i in range(13)]
        encode=lambda x:[[str(v) for v in row] for row in x];lower=F(ours['full_gap_lower_bound']);status='positive' if lower>0 else 'zero-insufficient' if not lower else 'negative-insufficient'
        expected={'schema':'ym17-shared-adjoint-rayleigh-v1','source_sha256':h(source/'adjoint.py'),'haar_source_sha256':h(source/'haar_graph.py'),'graph_file_sha256':h(source/'graph.json'),
          'alpha':str(a),'eta':str(t),'common_lambda_over_alpha':'12/43','physical_coefficients':[str(a*F(12,43))]*11,'face_order':[f['id'] for f in fg['faces']],
          'shared_face_index':s,'shared_face_id':fg['faces'][s]['id'],'trial_vector':['1']+['1/22']*11+[str(t)],
          'gram':encode(G),'electric_matrix':encode(E),'potential_matrix':encode(V),'trial_H':encode(H),
          'trial_norm_squared':ours['norm_squared'],'energy_numerator':ours['energy_numerator'],'full_E0_upper':ours['full_ground_upper'],'full_E1_lower':ours['full_E1_lower'],
          'gap_numerator':str(lower*F(ours['norm_squared'])),'full_gap_lower':str(lower),'bound_status':status,'valid_trial':True,
          'positive_amplitude_interval':['0','6/3817'],'positive_interval_open':[True,True],
          'inside_positive_amplitude_interval':F(0)<t<F(6,3817),'scope':SCOPE}
        if not strict(c,expected):raise ValueError('certificate differs from independent full matrix replay')
        return True
    for fixture in r['fixtures']:check('exact full matrix and physical-bound replay '+fixture['id'],verify(fixture['certificate']))
    expected_rows=[]
    for name,a,t in definitions[:7]:
        ours=compute(a,t,g,mat);lower=F(ours['full_gap_lower_bound']);expected_rows.append({'id':name,'eta':t,'eta_fraction_of_endpoint':str(F(t)/F(6,3817)),
          'gap_lower_over_alpha':str(lower),'full_E1_lower':ours['full_E1_lower'],'rayleigh_E0_upper':ours['full_ground_upper'],
          'bound_status':'positive' if lower>0 else 'zero-insufficient' if not lower else 'negative-insufficient','valid_trial':'true'})
    check('all seven frozen amplitude rows match exact quotients',strict(r['amplitude_rows'],expected_rows))
    selected=r['fixtures'][3]['certificate'];endpoint=r['fixtures'][5]['certificate']
    controls=[]
    bad=copy.deepcopy(selected);bad['potential_matrix'][s+1][12]='0';controls.append(('missing adjoint mixed coupling',bad))
    bad=copy.deepcopy(selected);bad['electric_matrix'][12][12]='3';controls.append(('fundamental energy substituted for adjoint',bad))
    bad=copy.deepcopy(endpoint);bad['bound_status']='positive';controls.append(('zero endpoint relabeled positive',bad))
    bad=copy.deepcopy(selected);bad['valid_trial']=1;controls.append(('Boolean result replaced by integer',bad))
    bad=copy.deepcopy(selected);bad['graph_file_sha256']='0'*64;controls.append(('unbound graph source',bad))
    for name,bad in controls:
        try:verify(bad)
        except ValueError:check('reject '+name,True)
        else:raise RuntimeError('false certificate accepted '+name)
    check('finite interval and original dense uniform goal retained',r['positive_amplitude_interval']==['0','6/3817'] and r['selected_amplitude']=='3/3817' and r['physical_common_coupling_ratio']=='12/43' and r['dense_uniform_goal']=='open' and r['C1']=='not executed')
    result={'schema':'ym17-independent-b2-comparison-v1','status':'passed','checks_count':len(checks),'checks':checks,
      'reviewed_input_sha256':{'producer/'+f:h(source/f) for f in ('adjoint.py','haar_graph.py','graph.json','check.py','report.md')},'producer_evidence_sha256':h(evidence/'evidence.json'),
      'discrepancies':[],'scope':'Independent actual-link polynomial Haar replay of all 169 Gram entries, 1859 magnetic entries, nine full matrix certificates and the complete seven-point amplitude ledger.'}
    (output/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'passed','checks_count':len(checks)}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--producer',required=True);p.add_argument('--evidence',required=True);p.add_argument('--output',required=True);a=p.parse_args();main(a.producer,a.evidence,a.output)
