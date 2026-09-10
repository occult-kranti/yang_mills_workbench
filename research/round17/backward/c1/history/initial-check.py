"""Independent full central-link Haar projector and conditional graph fixture."""
from fractions import Fraction as F
from pathlib import Path
from itertools import combinations
import argparse,copy,hashlib,json
from geometry import graph,validate,boundary,word_holonomy,qmul,inverse,IDENTITY,TETRA
from projector import haar_projector,matmul,rank,pair_basis,generators,rotation,integrate,joint_polynomial,adjoint_poly,sphere_moment


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
        raise RuntimeError('invalid input accepted '+name)
    g=graph();data=validate(g);labels,P=haar_projector();B=pair_basis(labels);Bt=list(map(list,zip(*B)));G=matmul(Bt,B)
    inverse_gram=[[F(2,15) if i==j else -F(1,30) for j in range(3)] for i in range(3)]
    gram_projector=matmul(matmul(B,inverse_gram),Bt)
    check('full graph has 18 vertices 33 links 20 faces and four cells',(len(g['vertices']),len(g['edges']),len(g['faces']),len(data['cells']))==(18,33,20,4))
    check('outer-only graph loses the actual central link',(len(data['outer_vertices']),len(data['outer_edges']),len(data['outer_faces']))==(18,32,16) and data['central'] not in data['outer_edges'])
    check('four internal faces meet the unique central link',len(data['internal_faces'])==4 and data['incidence'][data['central']]==data['internal_faces'])
    check('degree eight sphere moments fix normalized measure',sphere_moment((0,0,0,0))==1 and sphere_moment((2,0,0,0))==F(1,4) and sphere_moment((2,2,2,2))==F(1,1920))
    check('all 6561 quaternion-integrated entries equal full Gram projector',P==gram_projector)
    check('actual invariant Gram and inverse have signed overlaps',G==[[F(9) if i==j else F(3) for j in range(3)] for i in range(3)] and matmul(G,inverse_gram)==[[F(i==j) for j in range(3)] for i in range(3)])
    check('Haar tensor is exactly self-adjoint',P==list(map(list,zip(*P))))
    check('Haar tensor is exactly idempotent',matmul(P,P)==P)
    check('full tensor rank and trace are three',rank(P)==3 and sum(P[i][i] for i in range(81))==3)
    check('three pair-spin channels exhaust invariant dimension',integrate(joint_polynomial([IDENTITY]*4))==3 and rank(B)==3)
    zero=[[F(0)]*81 for _ in range(81)]
    check('all three infinitesimal group generators annihilate Haar range',all(matmul(J,P)==zero and matmul(P,J)==zero for J in generators(labels)))
    bad_diagonal=matmul(matmul(B,[[F(2,15) if i==j else F(0) for j in range(3)] for i in range(3)]),Bt)
    bad_one=[[B[i][0]*B[j][0]/9 for j in range(81)] for i in range(81)]
    check('dropping offdiagonal Gram coefficients destroys projection',matmul(bad_diagonal,bad_diagonal)!=bad_diagonal and sum(bad_diagonal[i][i] for i in range(81))!=3)
    check('one valid channel projector is incomplete',matmul(bad_one,bad_one)==bad_one and rank(bad_one)==1 and bad_one!=P)
    check('tetrahedral quaternions are orthonormal and noncommuting',all(sum(a*b for a,b in zip(TETRA[i],TETRA[j]))==int(i==j) for i in range(4) for j in range(4)) and all(qmul(TETRA[i],TETRA[j])!=qmul(TETRA[j],TETRA[i]) for i,j in combinations(range(4),2)))
    links,paths,chosen=boundary(g);check('actual three-edge paths independently realize all boundary holonomies',len(set(chosen))==4 and all(word_holonomy(path['word'][1:],links)==H for path,H in zip(paths,TETRA)))
    Q=(F(3,5),F(4,5),F(0),F(0));links[data['central']]=Q
    check('whole-face reorientations produce actual U H products',all(word_holonomy(path['word'],links)==qmul(Q,H) for path,H in zip(paths,TETRA)))
    check('real adjoint rotations respect quaternion products',all(matmul(rotation(Q),rotation(H))==rotation(qmul(Q,H)) for H in TETRA))
    gauges={tuple(v):TETRA[i%4] for i,v in enumerate(g['vertices'])};transformed={eid:qmul(qmul(gauges[a],q),inverse(gauges[b])) for eid,q in links.items() for a,b in [data['edges'][eid]]}
    check('actual conditional fixture has gauge-invariant face characters',all(word_holonomy(path['word'],links)[0]==word_holonomy(path['word'],transformed)[0] for path in paths))
    badword=copy.deepcopy(paths[0]['word']);badword[0][1]*=-1
    check('one isolated dagger change alters the conditional observable',word_holonomy(badword,links)[0]**2!=word_holonomy(paths[0]['word'],links)[0]**2)
    raw=integrate(joint_polynomial(TETRA));joint=raw/81;individual=[integrate(adjoint_poly(H))/3 for H in TETRA]
    check('independent sphere polynomial gives negative normalized joint',raw==-F(1,5) and joint==-F(1,405))
    from projector import tensor_contraction
    check('whole Haar tensor contraction matches joint polynomial',tensor_contraction(P,labels,TETRA)==raw)
    bad_diagonal_value=tensor_contraction(bad_diagonal,labels,TETRA)/81;bad_one_value=tensor_contraction(bad_one,labels,TETRA)/81
    check('zero marginal product does not equal nonzero joint',individual==[F(0)]*4 and joint!=0)
    check('positive scalar and dropped-channel shortcuts fail fixture',joint<0 and bad_diagonal_value!=joint and bad_one_value!=joint)
    bad=copy.deepcopy(g);bad['faces'][data['internal_faces'][0]]['word'][0][1]*=-1;reject('wrong graph dagger rejected',lambda:validate(bad))
    bad=copy.deepcopy(g);bad['faces'].pop();reject('omitted face rejected',lambda:validate(bad))
    bad=copy.deepcopy(g);bad['edges'][data['central']]['head'][0]=True;reject('Boolean central-link coordinate rejected',lambda:validate(bad))
    reject('nonunit boundary quaternion rejected',lambda:boundary(g,[(1,1,1,1)]+list(TETRA[1:])))
    reject('Boolean sphere exponent rejected',lambda:sphere_moment((True,0,0,0)))
    encode=lambda M:[[str(x) for x in row] for row in M]
    result={'schema':'ym17-independent-c1-results-v1','status':'passed','checks_count':len(checks),'checks':checks,
      'source_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in Path(__file__).parent.glob('*.py') if p.name!='compare.py'},
      'full_counts':[18,33,20],'outer_counts':[18,32,16],'rank':3,'trace':'3','gram':encode(G),'inverse_gram':encode(inverse_gram),
      'quaternion_projector_entries':6561,'central_link':data['central'],'internal_faces':data['internal_faces'],
      'raw_joint':str(raw),'normalized_joint':str(joint),'normalized_individuals':list(map(str,individual)),
      'wrong_diagonal_only_joint':str(bad_diagonal_value),'wrong_single_channel_joint':str(bad_one_value),
      'scope':'Full central-link four-adjoint Haar tensor and realizable fixed-boundary zero-action conditional observable; no fully integrated twenty-face bulk amplitude or Hamiltonian gap result.'}
    fixture={'unit_quaternions':[list(map(str,H)) for H in TETRA],'central_Q':list(map(str,Q)),'paths':paths,
      'assigned_boundary_links':chosen,'link_quaternions':{str(eid):list(map(str,q)) for eid,q in links.items()},
      'raw_joint':str(raw),'normalized_joint':str(joint)}
    for name,obj in [('results.json',result),('graph.json',g),('projector.json',{'labels':list(map(list,labels)),'projector':encode(P)}),('boundary_fixture.json',fixture)]:
        (output/name).write_text(json.dumps(obj,indent=2)+'\n')
    print(json.dumps({'status':'passed','checks_count':len(checks),'normalized_joint':str(joint),'wrong_diagonal_only':str(bad_diagonal_value),'wrong_single_channel':str(bad_one_value)}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();run(a.output)
