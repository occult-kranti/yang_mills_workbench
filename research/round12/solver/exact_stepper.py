"""One end-to-end exact rational driven-state certificate on the seven-link graph.

Fixed bounded fixture: D=3, two duration-one nonnegative constant segments, Taylor
order 100. Stored complex coefficients are Fraction pairs; no float arithmetic
or normalization enters construction or replay.
"""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
from functools import lru_cache
import hashlib,json
import drive_bound as db
from vendor import two_plaquette as tp

ROOT=Path(__file__).resolve().parent
PROTOCOL={'kind':'piecewise_constant','segments':[{'duration':'1','lambda1':'1/20','lambda2':'1/10'},{'duration':'1','lambda1':'1/10','lambda2':'1/20'}]}
DEGREE=3;ORDER=100

def hashes():
    return {**db.source_hashes(),'exact_stepper.py':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}

@lru_cache(None)
def _operator_cached(degree,alpha,lambda1,lambda2,rho):
    D=db.nonnegative_int(degree,'degree');a,l1,l2,r=map(db.rat,(alpha,lambda1,lambda2,rho))
    if a<=0 or r<=0:raise ValueError('positive alpha and rho required')
    basis,G,K,X,Y=tp.matrices(D,r);Hform=tp.combine(G,K,X,Y,a,l1,l2);Hcoord=tp.solve_exact(G,Hform)
    if Hform!=[list(row) for row in zip(*Hform)]:raise RuntimeError('exact physical selfadjointness failed')
    # K spectrum on P_D is known exactly from the independent round-11 degree algebra.
    free_max=a*max(tp.free_energy(k,r) for k in basis)
    norm_upper=free_max+2*(abs(l1)+abs(l2))
    sparse=[[(j,value) for j,value in enumerate(row) if value] for row in Hcoord]
    return basis,G,sparse,free_max,norm_upper

def operator(degree,alpha,lambda1,lambda2,rho):
    # Validate before the cache so Python's True==1 cannot bypass the input contract.
    D=db.nonnegative_int(degree,'degree');a,l1,l2,r=map(db.rat,(alpha,lambda1,lambda2,rho))
    if a<=0 or r<=0:raise ValueError('positive alpha and rho required')
    return _operator_cached(D,a,l1,l2,r)

def rational_taylor(sparse,state,duration,order):
    h=db.rat(duration);p=db.nonnegative_int(order,'Taylor order')
    if h<0:raise ValueError('nonnegative step duration required')
    if not sparse or len(state)!=len(sparse):raise ValueError('nonempty compatible operator and state required')
    psi=[]
    for value in state:
        if not isinstance(value,(tuple,list)) or len(value)!=2:raise ValueError('complex rational pairs required')
        psi.append((db.rat(value[0]),db.rat(value[1])))
    if any(type(j) is not int or j<0 or j>=len(state) for row in sparse for j,_ in row):raise ValueError('invalid sparse index')
    A=[[(j,db.rat(value)) for j,value in row] for row in sparse]
    term=list(psi);result=list(psi)
    for k in range(1,p+1):
        factor=h/k;next_term=[]
        for row in A:
            real=sum((v*term[j][0] for j,v in row),F(0));imag=sum((v*term[j][1] for j,v in row),F(0))
            next_term.append((factor*imag,-factor*real))
        term=next_term;result=[(u[0]+v[0],u[1]+v[1]) for u,v in zip(result,term)]
    return result

def norm_squared(G,state):
    if not state or len(state)!=len(G) or any(len(row)!=len(state) for row in G):raise ValueError('compatible nonempty Gram norm required')
    if any(not isinstance(v,(tuple,list)) or len(v)!=2 for v in state):raise ValueError('complex rational pairs required')
    metric=[[db.rat(value) for value in row] for row in G]
    values=[(db.rat(v[0]),db.rat(v[1])) for v in state]
    result=sum((metric[i][j]*(values[i][0]*values[j][0]+values[i][1]*values[j][1]) for i in range(len(values)) for j in range(len(values))),F(0))
    if result<0:raise ValueError('negative physical norm squared')
    return result

def step_error_bound(duration,norm_upper,order):
    h,M=db.rat(duration),db.rat(norm_upper);p=db.nonnegative_int(order,'Taylor order')
    if h<0 or M<0:raise ValueError('nonnegative duration and operator bound required')
    return (h*M)**(p+1)/factorial(p+1)

def product_error_bound(errors):
    if not isinstance(errors,(tuple,list)) or not errors:raise ValueError('nonempty error sequence required')
    product=F(1)
    for error in errors:
        e=db.rat(error)
        if e<0:raise ValueError('nonnegative step error required')
        product*=1+e
    return product-1

def build_certificate():
    basis,G,_,_,_=operator(DEGREE,F(1),F(0),F(0),F(1));state=[(F(1),F(0))]+[(F(0),F(0))]*(len(basis)-1)
    initial_norm=norm_squared(G,state)
    if initial_norm!=1:raise RuntimeError('constant Haar state must be exactly normalized')
    steps=[];errors=[]
    for index,seg in enumerate(PROTOCOL['segments']):
        h,l1,l2=map(F,(seg['duration'],seg['lambda1'],seg['lambda2']))
        _,_,A,kmax,M=operator(DEGREE,F(1),l1,l2,F(1));state=rational_taylor(A,state,h,ORDER)
        eps=step_error_bound(h,M,ORDER);errors.append(eps)
        steps.append({'index':index,'duration':str(h),'lambda1':str(l1),'lambda2':str(l2),'free_kinetic_max':str(kmax),'Hamiltonian_norm_upper':str(M),'Taylor_order':ORDER,'operator_error_upper':str(eps)})
    action=db.action_interval(PROTOCOL)[1];rep=db.factorial_bound(action,DEGREE);numerical=product_error_bound(errors);total=rep+numerical
    return {'contract':'ym12-exact-rational-piecewise-state-v1','scope':db.SCOPE,'target':'exact-infinite-representation-state-versus-stored-rational-polynomial-state','norm':'normalized-product-Haar-L2','initial_state':'exact-constant-one-electric-vacuum','initial_norm_squared':str(initial_norm),'protocol':db.canonical_protocol(PROTOCOL),'alpha':'1','rho':'1','degree':DEGREE,'dimension':len(basis),'Taylor_order':ORDER,'basis_exponents':[list(k) for k in basis],'steps':steps,'final_coefficients':[{'real':str(v[0]),'imag':str(v[1])} for v in state],'final_norm_squared':str(norm_squared(G,state)),'computed_vector_was_renormalized':False,'accumulated_action':str(action),'representation_error_upper':str(rep),'finite_step_algorithm_error_upper':str(numerical),'arithmetic_roundoff_error':'0','total_state_error_upper':str(total),'status':'certified-total-Hilbert-state-error-for-fixed-finite-graph','source_hashes':hashes()}

def verify_certificate(c):
    if not isinstance(c,dict):raise ValueError('certificate object required')
    expected=build_certificate()
    if set(c)!=set(expected):raise ValueError('complete exact-step certificate fields required')
    for key in ('degree','dimension','Taylor_order'):
        if type(c[key]) is not int:raise ValueError('integer exact-step metadata required')
    if type(c['computed_vector_was_renormalized']) is not bool:raise ValueError('Boolean normalization metadata required')
    if not isinstance(c['basis_exponents'],list) or any(not isinstance(v,list) or len(v)!=3 or any(type(k) is not int for k in v) for v in c['basis_exponents']):raise ValueError('integer basis labels required')
    if not isinstance(c['steps'],list) or any(type(step.get('index')) is not int or type(step.get('Taylor_order')) is not int for step in c['steps']):raise ValueError('integer step metadata required')
    if c!=expected:raise ValueError('exact step protocol/vector/norm/error/provenance mismatch')
    return True

if __name__=='__main__':
    c=build_certificate();verify_certificate(c);out=ROOT/'output';out.mkdir(exist_ok=True);path=out/'exact_step_certificate.json';path.write_text(json.dumps(c,indent=2)+'\n')
    print(json.dumps({'status':c['status'],'degree':DEGREE,'dimension':c['dimension'],'action':c['accumulated_action'],'representation_error_upper':c['representation_error_upper'],'finite_step_error_upper':c['finite_step_algorithm_error_upper'],'total_error_upper':c['total_state_error_upper'],'output':str(path)},indent=2))
