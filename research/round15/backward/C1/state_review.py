"""Independent rational quaternion test of the advisor's Gibbs-state falsifier."""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import importlib.util
import json
import sys

HERE=Path(__file__).resolve().parent
ALGEBRA_PATH=HERE.parent/'B1/exact_algebra.py'
ALGEBRA_PIN='88ed912040d5cc988513c5d081465cdb08a6a29f11066c9ff05405f4b55a3dcf'
if hashlib.sha256(ALGEBRA_PATH.read_bytes()).hexdigest()!=ALGEBRA_PIN:raise ValueError('accepted quaternion source changed')
spec=importlib.util.spec_from_file_location('ym15_exact_quaternion',ALGEBRA_PATH)
alg=importlib.util.module_from_spec(spec);spec.loader.exec_module(alg)
ONE=(Q(1),Q(0),Q(0),Q(0))


def value(word,links,derivative=None):
    if derivative is not None and not any(edge==derivative[0] for edge,_ in word):return Q(0)
    out=ONE
    for edge,sign in word:
        factor=links[edge] if sign==1 else alg.inverse(links[edge])
        if derivative is not None and edge==derivative[0]:
            _,axis,order=derivative
            generator=(Q(0),*(Q(-1,2) if i==axis else Q(0) for i in range(3)))
            if order==1:
                factor=alg.multiply(generator,factor) if sign==1 else tuple(-x for x in alg.multiply(factor,generator))
            elif order==2:factor=tuple(-x/4 for x in factor)
            else:raise ValueError('first or second derivative only')
        out=alg.multiply(out,factor)
    return out[0]


def run(graph_path,advisor_dir,output_dir):
    graph_bytes=Path(graph_path).read_bytes()
    if hashlib.sha256(graph_bytes).hexdigest()!='4e85817855a880ce5f48e6b3995adca6852557d55103623bb0d686295f334f65':raise ValueError('accepted B1 graph changed')
    graph=json.loads(graph_bytes);advisor=Path(advisor_dir)
    source_bytes=(advisor/'cube_state_check.py').read_bytes();note_bytes=(advisor/'cube_state_check.md').read_bytes()
    saved=json.loads((advisor/'cube_state_check.json').read_bytes())
    if saved.get('source_sha256')!=hashlib.sha256(source_bytes).hexdigest():raise ValueError('advisor report does not bind actual source')
    edges=[e['id'] for e in graph['edges']]
    words=[[(x['edge'],x['sign']) for x in f['word']] for f in graph['faces']]
    checks=[];rows=[]
    def gate(name,test):
        if not test:raise ValueError(name)
        checks.append({'name':name,'passed':True})
    for name,first in [('identity',ONE),('one_center_link',tuple(-x for x in ONE)),('one_noncentral_link',(Q(0),Q(0),Q(0),Q(-1)))]:
        links={edge:ONE for edge in edges};links[edges[0]]=first
        action=sum(value(word,links) for word in words)
        gradient=[];laplacian=Q(0)
        for edge in edges:
            for axis in range(3):
                gradient.append(sum(value(word,links,(edge,axis,1)) for word in words))
                laplacian+=sum(value(word,links,(edge,axis,2)) for word in words)
        norm=sum(x*x for x in gradient)
        row={'fixture':name,'S':str(action),'gradient_squared':str(norm),'electric_Casimir_S':str(-laplacian)}
        rows.append(row);gate(name+' actual quaternion Casimir',-laplacian==3*action)
        matching=[r for r in saved['fixtures'] if r.get('fixture')==name]
        gate(name+' independent representation matches advisor fixture',len(matching)==1 and matching[0]==row)
    gate('full independently calculated fixture set',[(Q(r['S']),Q(r['gradient_squared'])) for r in rows]==[(Q(6),Q(0)),(Q(2),Q(0)),(Q(4),Q(5,2))])
    # q=a*kappa and l=lambda: the first two ratios differ by6q-4l.
    gate('center fixtures force lambda=3alpha*kappa/2',Q(rows[0]['S'])-Q(rows[1]['S'])==4)
    gate('matched noncentral gradient defect remains -5alpha*kappa^2/8',-(Q(rows[2]['gradient_squared'])-Q(rows[0]['gradient_squared']))/4==Q(-5,8))
    gate('kappa0 lambda nonzero is rejected by nonconstant S',Q(rows[0]['S'])!=Q(rows[1]['S']))
    gate('noncentral gradient is essential; central fixtures alone are inconclusive',all(Q(r['gradient_squared'])==0 for r in rows[:2]) and Q(rows[2]['gradient_squared'])>0)
    gate('smooth full-support premise stated in advisor proof',b'full support' in note_bytes and b'almost everywhere' in note_bytes and b'continuous' in note_bytes)
    gate('advisor source unchanged during independent review',(advisor/'cube_state_check.py').read_bytes()==source_bytes)
    result={'schema':'ym15-C1-independent-state-review-v1','status':'passed','checks_count':len(checks),'checks':checks,'fixtures':rows,
      'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'advisor_source_sha256':hashlib.sha256(source_bytes).hexdigest(),'advisor_proof_sha256':hashlib.sha256(note_bytes).hexdigest(),
      'quaternion_source_sha256':ALGEBRA_PIN,
      'verdict':'For alpha>0, no lambda makes exp(kappa S/2) an eigenfunction when kappa!=0; the constant is an eigenstate only at lambda=0.',
      'proof_review':'The smooth wavefunction is strictly positive, the Hamiltonian ratio is continuous, and Haar has full support; thus an a.e. eigenidentity would hold at the exact test configurations.',
      'limits':['This rejects a specific state identification, not use of that function as a variational trial.',
                'The eigenstate conclusion uses the analytic chain rule and full-support argument as well as the exact configuration calculations.']}
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=True);(out/'independent_state_review.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'passed','checks':len(checks),'fixtures':rows}));return result


if __name__=='__main__':
    if len(sys.argv)!=4:raise SystemExit('usage: state_review.py GRAPH ADVISOR_DIR OUTPUT_DIR')
    run(*sys.argv[1:])
