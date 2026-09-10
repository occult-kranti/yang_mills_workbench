"""Independent exact admission of the complete forward C1 certificate."""
from pathlib import Path
from fractions import Fraction as F
import argparse,copy,hashlib,json
from geometry import graph,validate,boundary,strict,TETRA
from projector import haar_projector,pair_basis,matmul,integrate,joint_polynomial,adjoint_poly,tensor_contraction


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


def expected_certificate(source_sha):
    fg=named_graph();g=convert(fg);data=validate(g);links,paths,chosen=boundary(g);ename={i:e['id'] for i,e in enumerate(fg['edges'])};fname={i:f['id'] for i,f in enumerate(fg['faces'])}
    info={'central_edge':ename[data['central']],'central_face_indices':data['internal_faces'],
      'outer_face_ids':[fname[i] for i in data['outer_faces']],'outer_edge_ids':sorted(ename[e] for e in data['outer_edges']),
      'outer_vertices':sorted(','.join(map(str,v)) for v in data['outer_vertices']),'internal_face_ids':[fname[i] for i in data['internal_faces']]}
    words=[];choices=[]
    for path,H in zip(paths,TETRA):
        fi=path['face'];word=[{'edge':ename[e],'sign':sign} for e,sign in path['word']]
        originalsign=next(sign for e,sign in g['faces'][fi]['word'] if e==data['central'])
        words.append({'face_index':fi,'face_id':fname[fi],'whole_face_reversed':originalsign==-1,'word':word,'boundary_path':word[1:]})
        choices.append({'edge':ename[path['assigned_edge']],'path_sign':next(sign for e,sign in path['word'] if e==path['assigned_edge']),
          'target_H':list(map(str,H)),'face_id':fname[fi]})
    labels,P=haar_projector();B=pair_basis(labels);Bt=list(map(list,zip(*B)));G=matmul(Bt,B);Gi=[[F(2,15) if i==j else -F(1,30) for j in range(3)] for i in range(3)]
    wrong=matmul(matmul(B,[[Gi[i][j] if i==j else F(0) for j in range(3)] for i in range(3)]),Bt)
    one=[[B[i][0]*B[j][0]/9 for j in range(81)] for i in range(81)];encode=lambda M:[[str(x) for x in row] for row in M]
    return {'schema':'ym17-central-four-adjoint-v1','source_sha256':source_sha,'graph':fg,'geometry':info,'central_words':words,
      'boundary_assignments':{ename[e]:list(map(str,q)) for e,q in links.items()},'chosen_boundary_links':choices,'boundary_H':[list(map(str,H)) for H in TETRA],
      'tensor_index_order':list(map(list,labels)),'basis':encode(B),'gram':encode(G),'gram_inverse':encode(Gi),'projector':encode(P),
      'invariant_dimension':3,'pair_channels':[0,1,2],'adjoint_normalization_per_face':'3','conditional_joint':str(integrate(joint_polynomial(TETRA))/81),
      'wrong_diagonal_inverse_joint':str(tensor_contraction(wrong,labels,TETRA)/81),'wrong_one_channel_joint':str(tensor_contraction(one,labels,TETRA)/81),
      'individual_conditional_means':[str(integrate(adjoint_poly(H))/3) for H in TETRA],'central_action':'0','C2_nonzero_action':'not executed',
      'scope':'Complete central-link conditional Haar tensor and realizable fixed boundary; not twenty-face bulk integration or a spectral theorem'}


def main(source,evidence,output):
    source,evidence,output=map(Path,(source,evidence,output));output=output.resolve()
    if output.is_relative_to(Path(__file__).resolve().parent):raise ValueError('output outside source required')
    output.mkdir(parents=True,exist_ok=False);h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();r=json.loads((evidence/'evidence.json').read_text());expected=expected_certificate(h(source/'central.py'));checks=[]
    def check(name,ok):
        if not ok:raise RuntimeError(name)
        checks.append({'name':name,'passed':True})
    def verify(c):
        if not strict(c,expected):raise ValueError('complete independent central tensor replay differs')
        return True
    for name,keys in [('actual full graph and cell inventory',['graph','geometry']),('all fully oriented paths and link assignments',['central_words','boundary_assignments','chosen_boundary_links','boundary_H']),('all 6561 S3-integrated projector entries',['tensor_index_order','projector']),('complete signed invariant channels',['basis','gram','gram_inverse','invariant_dimension','pair_channels']),('joint and discriminating wrong-channel values',['conditional_joint','wrong_diagonal_inverse_joint','wrong_one_channel_joint','individual_conditional_means'])]:
        check(name,all(strict(r[k],expected[k]) for k in keys))
    check('complete schema physical normalization and scope replay',verify(r))
    bads=[]
    bad=copy.deepcopy(r);bad['projector'][0][0]='0';bads.append(('changed actual Haar tensor entry',bad))
    bad=copy.deepcopy(r);bad['gram_inverse'][0][1]='0';bads.append(('omitted offdiagonal invariant overlap',bad))
    bad=copy.deepcopy(r);bad['adjoint_normalization_per_face']='1';bads.append(('ordinary character substituted for normalized insertion',bad))
    bad=copy.deepcopy(r);bad['central_words'][0]['word'][0]['sign']=-1;bads.append(('one dagger changed without full face reversal',bad))
    bad=copy.deepcopy(r);bad['graph']['faces'][0]['incident_cells']=[];bads.append(('changed cell incidence metadata',bad))
    bad=copy.deepcopy(r);bad['pair_channels'][0]=False;bads.append(('Boolean intermediate-spin metadata',bad))
    bad=copy.deepcopy(r);bad['source_sha256']='0'*64;bads.append(('stale source binding',bad))
    bad=copy.deepcopy(r);bad['extra_assumption']='factorized physical space';bads.append(('hidden extra premise',bad))
    for name,bad in bads:
        try:verify(bad)
        except ValueError:check('reject '+name,True)
        else:raise RuntimeError('incorrect tensor admitted '+name)
    result={'schema':'ym17-independent-c1-comparison-v1','status':'passed','checks_count':len(checks),'checks':checks,
      'reviewed_input_sha256':{'producer/'+f:h(source/f) for f in ('central.py','check.py','report.md')},'producer_evidence_sha256':h(evidence/'evidence.json'),
      'discrepancies':[],'scope':'Whole producer graph/cell/word/boundary schema and full 81 by 81 tensor replayed with independent S3 polynomial moments; static conditional zero-action scope retained.'}
    (output/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'passed','checks_count':len(checks)}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--producer',required=True);p.add_argument('--evidence',required=True);p.add_argument('--output',required=True);a=p.parse_args();main(a.producer,a.evidence,a.output)
