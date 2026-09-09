#!/usr/bin/env python3
"""Independent monomial Gram algebra and backward Horner exact state replay."""
from pathlib import Path
from fractions import Fraction as F
from math import factorial
import argparse,copy,hashlib,json,sys
from round11_independent_algebra import load,my_matrices,gauss_jordan_inverse,matmul
from independent_banded import sqrt_interval

def horner(A,state,h,order):
    base=state;v=state
    for k in range(order,0,-1):
        real=[sum((a*w[0] for a,w in zip(row,v)),F(0)) for row in A]
        imag=[sum((a*w[1] for a,w in zip(row,v)),F(0)) for row in A]
        v=[(b[0]+h*y/k,b[1]-h*x/k) for b,x,y in zip(base,real,imag)]
    return v
def gram_norm(G,c):return sum((G[i][j]*(c[i][0]*c[j][0]+c[i][1]*c[j][1]) for i in range(len(G)) for j in range(len(G))),F(0))
def main():
    ap=argparse.ArgumentParser();ap.add_argument('source',type=Path);ap.add_argument('--label',default='exact_step_audit');args=ap.parse_args();source=args.source.resolve();sys.path.insert(0,str(source.parent))
    before=hashlib.sha256(source.read_bytes()).hexdigest();m=load(source,'reviewed_exact_stepper');records=[];defects=[]
    def check(ok,name,detail=None):
        if not ok:raise RuntimeError(name)
        records.append({'test':name,'passed':True,'detail':detail})
    def rejects(fn,name):
        try:fn()
        except (ValueError,TypeError,RuntimeError,KeyError):records.append({'test':name,'passed':True});return
        raise RuntimeError('Unexpected acceptance: '+name)
    c=m.build_certificate();check(m.verify_certificate(c),'production_exact_step_replay')
    basis,G,K,X,Y=my_matrices(3,F(1));Gi=gauss_jordan_inverse(G);n=len(G)
    state=[(F(1),F(0))]+[(F(0),F(0))]*(n-1);wrong=state
    for j,segment in enumerate(c['protocol']['segments']):
        h,l1,l2=map(F,(segment['duration'],segment['lambda1'],segment['lambda2']))
        H=[[K[i][j]+(l1+l2)*G[i][j]-l1*X[i][j]-l2*Y[i][j] for j in range(n)] for i in range(n)];A=matmul(Gi,H)
        _,pG,sparse,kmax,bound=m.operator(3,F(1),l1,l2,F(1));dense=[[F(0)]*n for _ in range(n)]
        for i,row in enumerate(sparse):
            for k,v in row:dense[i][k]+=v
        check(G==pG and A==dense,f'independent_form_to_coordinate_operator.{j}')
        check(kmax==F(45,2) and bound==F(114,5),f'physical_operator_norm_bound.{j}')
        state=horner(A,state,h,100);wrong=horner(H,wrong,h,100)
    delivered=[(F(row['real']),F(row['imag'])) for row in c['final_coefficients']]
    check(delivered==state,'independent_backward_Horner_coefficients')
    actual_norm=gram_norm(G,state);check(actual_norm==F(c['final_norm_squared']),'independent_Haar_norm_squared')
    check(c['computed_vector_was_renormalized'] is False and actual_norm!=1,'no_hidden_state_renormalization')
    eps=F(114,5)**101/factorial(101);step=2*eps+eps*eps;representation=F(27,80000)
    check(F(c['accumulated_action'])==F(3,10) and F(c['representation_error_upper'])==representation,'independent_action_and_representation_error')
    check(F(c['finite_step_algorithm_error_upper'])==step and F(c['total_state_error_upper'])==representation+step,'independent_total_error_budget')
    check(abs(actual_norm-1)<=2*step+step*step,'exact_norm_defect_consistent_with_operator_error')
    diff=[(a[0]-b[0],a[1]-b[1]) for a,b in zip(state,wrong)];wrong_error=sqrt_interval(gram_norm(G,diff))
    check(wrong_error[0]>representation+2*step,'Euclidean_form_matrix_substitution_falsified',{'wrong_state_distance_lower':str(wrong_error[0]),'correct_total_error_upper':str(representation+step)})
    mutations={
       'vector':lambda d:d['final_coefficients'][0].__setitem__('real','0'),
       'norm':lambda d:d.__setitem__('final_norm_squared','1'),
       'renormalized':lambda d:d.__setitem__('computed_vector_was_renormalized',True),
       'int_boolean':lambda d:d.__setitem__('computed_vector_was_renormalized',0),
       'bool_index':lambda d:d['steps'][0].__setitem__('index',False),
       'bool_basis':lambda d:d['basis_exponents'][0].__setitem__(0,False),
       'wrong_error':lambda d:d.__setitem__('finite_step_algorithm_error_upper','0'),
       'wrong_total':lambda d:d.__setitem__('total_state_error_upper','0'),
       'wrong_protocol':lambda d:d['protocol']['segments'][0].__setitem__('lambda1','1/5'),
       'wrong_target':lambda d:d.__setitem__('target','cosine_ramp_total_error'),
       'empty_sources':lambda d:d.__setitem__('source_hashes',{}),
    }
    for name,mutate in mutations.items():
        changed=copy.deepcopy(c);mutate(changed);rejects(lambda:m.verify_certificate(changed),'exact_step_mutation.'+name)
    for errors in ([],[-1],[True]):rejects(lambda:m.product_error_bound(errors),'invalid_product_error.'+str(errors))
    direct=m.norm_squared([[F(1)]],[(0.1,0)])
    if not isinstance(direct,F):defects.append({'defect':'public norm_squared accepts float state and returns float','certificate_constructor_affected':False,'input':'G=[[1]], state=[(0.1,0)]','returned_type':type(direct).__name__})
    else:check(direct==F(1,100),'public_exact_norm_input_normalization')
    check(hashlib.sha256(source.read_bytes()).hexdigest()==before,'exact_step_source_unchanged')
    result={'status':'passed-with-public-API-defect' if defects else 'passed','optimized_python':not __debug__,'gate_count':len(records),'records':records,'defects':defects,
      'source_sha256':before,'source_hashes':c['source_hashes'],'audit_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'independent_method':'Spherical Haar moments; divergence-form kinetic polynomials; Gauss-Jordan Gram inverse; backwards rational Horner polynomial application',
      'scope':'Fixed nonnegative two-segment swap protocol, degree3, order100, exact stored unrenormalized vector; does not certify earlier cosine trajectories.'}
    Path(__file__).with_name(args.label+'_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'gate_count':len(records),'source_sha256':before,'defects':defects}))
if __name__=='__main__':main()
