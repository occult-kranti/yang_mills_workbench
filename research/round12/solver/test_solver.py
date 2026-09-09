"""Exact action/certificate fixtures and independent finite-chain counterchecks."""
from fractions import Fraction as F
from pathlib import Path
import copy,json,hashlib,math
import numpy as np
from scipy.linalg import expm
import drive_bound as db

ROOT=Path(__file__).resolve().parent;RESULTS=[]
def check(name,condition,details=None):
    RESULTS.append({'name':name,'passed':bool(condition),'details':details})
    if not condition:raise RuntimeError(name)
def rejects(name,fn):
    try:fn()
    except (ValueError,TypeError,KeyError,RuntimeError,OverflowError,ZeroDivisionError):check(name,True);return
    check(name,False)
def ramp(T='2',a='1/10',b='3/20'):return {'kind':'cosine_ramp','duration':T,'lambda1_scale':a,'lambda2_scale':b}

def exact_tests():
    p=ramp();pl,pu=db.pi_interval();check('exact Machin enclosure has rational expected range',F(3)<pl<pu<F(22,7) and pu-pl<F(1,10**25))
    check('alternating action terms decrease',pu*pu<20)
    check('full-ramp endpoint exact action',db.action_interval(p)==(F(1,2),F(1,2)))
    # Independently use exact sin(pi/2)=1 and sin(pi/6)=1/2.
    for s,sinvalue in ((F(1,2),F(1)),(F(1,6),F(1,2))):
        lo,hi=db.action_interval(p,2*s);olo=F(1,2)*(s-sinvalue/pl);ohi=F(1,2)*(s-sinvalue/pu)
        check('exact-angle independent action enclosure '+str(s),lo<=olo<=ohi<=hi,{'interval':[str(lo),str(hi)]})
    check('zero time',db.action_interval(p,0)==(F(0),F(0)))
    check('zero-duration protocol',db.action_interval(ramp('0'))==(F(0),F(0)))
    check('zero drive',db.action_interval(ramp('2','0','0'),F(7,5))==(F(0),F(0)))
    check('sign-invariant accumulated action',db.action_interval(ramp('2','-1/10','3/20'),F(7,5))==db.action_interval(p,F(7,5)))
    check('D3 endpoint exact 1/384',db.factorial_bound(F(1,2),3)==F(1,384))
    check('D4 endpoint exact 1/3840',db.factorial_bound(F(1,2),4)==F(1,3840))
    check('D0 first-order bound',db.factorial_bound(F(1,2),0)==F(1,2))
    check('nonzero initial degree exponent',db.factorial_bound(F(1,2),4,2)==F(1,48))
    check('trivial normalized cap',db.factorial_bound(5,3)==2)
    piece={'kind':'piecewise_constant','segments':[{'duration':'1/2','lambda1':'2','lambda2':'-1'},{'duration':'1/2','lambda1':'-2','lambda2':'1'}]}
    check('discontinuous signed action exact',db.action_interval(piece)==(F(3),F(3)))
    check('partial second signed segment',db.action_interval(piece,F(3,4))==(F(9,4),F(9,4)))
    constant={'kind':'constant','duration':'3/2','lambda1_scale':'-2','lambda2_scale':'3'}
    check('constant signed action',db.action_interval(constant,F(1,3))==(F(5,3),F(5,3)))
    c=db.certificate(p,4);check('certificate replay',db.verify_certificate(c))
    for pp,d in ((ramp('0'),0),(ramp('2','0','0'),3),(piece,0),(constant,1)):
        cc=db.certificate(pp,d);check('edge certificate replay '+str((pp['kind'],d)),db.verify_certificate(cc))
    mutations={'scope':'four-dimensional-continuum','degree':True,'initial_degree':True,'factorial_order':6,'state_error_upper':'0','uncapped_error_upper':'0','action_interval':['0','0'],'bound_is_below_trivial_two':1,'target':'exact-versus-floating-code','time_step_error':'certified','coefficient_conditioning_error':'certified','status':'numerically-passed'}
    for k,v in mutations.items():
        bad=copy.deepcopy(c);bad[k]=v;rejects('certificate mutation '+k,lambda b=bad:db.verify_certificate(b))
    bad=copy.deepcopy(c);bad['source_hashes']={};rejects('empty provenance',lambda:db.verify_certificate(bad))
    bad=copy.deepcopy(c);del bad['scope'];rejects('missing scope',lambda:db.verify_certificate(bad))
    for a in (True,float('nan'),float('inf'),'NaN'):
        rejects('bad rational action '+str(a),lambda a=a:db.factorial_bound(a,3))
        rejects('bad protocol coefficient '+str(a),lambda a=a:db.certificate(ramp(a=a),3))
    for d,d0 in ((True,0),(-1,0),(2,True),(1,2)):
        rejects('bad degrees '+str((d,d0)),lambda d=d,d0=d0:db.factorial_bound(1,d,d0))
    for t in ('-1','3',True,float('nan')):rejects('time outside contract '+str(t),lambda t=t:db.action_interval(p,t))
    for a,r in ((0,1),(1,0),(-1,1),(1,-1),(True,1),(1,float('inf'))):rejects('bad fixed kinetic parameters '+str((a,r)),lambda a=a,r=r:db.certificate(p,3,alpha=a,rho=r))
    rejects('negative action',lambda:db.factorial_bound(-1,3))
    rejects('unknown protocol',lambda:db.certificate({'kind':'anything'},3))
    rejects('empty steps',lambda:db.certificate({'kind':'piecewise_constant','segments':[]},3))
    bad=copy.deepcopy(piece);bad['segments'][0]['duration']='0';rejects('zero step duration',lambda:db.certificate(bad,3))
    # Values throughout ramp are enclosed and rounded outward as exact rational numbers.
    for i in range(41):
        lo,hi=db.action_interval(p,F(i,20));check('action interval ordered '+str(i),0<=lo<=hi<=F(1,2))
    return c

def independent_chains():
    W=np.diag(np.full(7,.5),1)+np.diag(np.full(7,.5),-1);H0=np.diag(np.arange(8,dtype=float)**2);initial=np.eye(8)[:,0].astype(complex)
    # Independent finite matrix reference with degree-one bandwidth and ||W||<=1.
    for t in (0.,.1,.5,1.,3.):
        full=expm(-1j*t*(H0+W))@initial
        for D in range(5):
            short=expm(-1j*t*(H0[:D+1,:D+1]+W[:D+1,:D+1]))@initial[:D+1];embedded=np.zeros(8,complex);embedded[:D+1]=short
            error=float(np.linalg.norm(full-embedded));bound=float(db.factorial_bound(F(str(t)),D));check('independent chain bound '+str((t,D)),error<=bound+2e-14,{'error':error,'bound':bound})
    sigma=np.array([[0.,1.],[1.,0.]]);e0=np.array([1.,0.],complex);t=.1
    actual=np.linalg.norm(expm(-1j*t*sigma)@e0-e0)
    check('missing first hop factorial mutation distinguished',actual>t*t/2 and actual<t)
    # Two noncommuting signed pulses with zero signed integral still cause a state change.
    drift=np.diag([0.,1.]);t=.25;state=expm(-1j*t*(drift-sigma))@expm(-1j*t*(drift+sigma))@e0
    check('absolute value must be inside action integral',np.linalg.norm(state-e0)>1e-3,{'zero_signed_action':0,'true_action':2*t,'state_error':float(np.linalg.norm(state-e0))})
    terminal=expm(-1j*np.pi*sigma)@e0
    check('terminal leakage is not an evolution error bound',abs(terminal[1])<1e-14 and np.linalg.norm(terminal-e0)>1.99)

def numerical_edges():
    import run_study as study
    zero=study.evolve(ramp('0'),0,points=3);check('zero-time D0 numerical state unchanged',study.numerical_gate(zero) and np.linalg.norm(zero['states'][:,0]-zero['states'][:,-1])==0)
    drive=study.evolve(ramp('1/10','0','0'),0,points=3);check('zero-drive numerical work/norm',study.numerical_gate(drive))
    bad=copy.deepcopy(drive);bad['rows'][1]['work_defect']=float('nan');rejects('transient nonfinite history',lambda:study.numerical_gate(bad))
    bad=copy.deepcopy(drive);bad['rows']=[];rejects('empty history',lambda:study.numerical_gate(bad))
    rejects('Boolean midpoint step count',lambda:study.midpoint(ramp(),0,True))
    rejects('cached numerical Boolean degree',lambda:study.evolve(ramp(),False))
    rejects('Boolean numerical sample count',lambda:study.evolve(ramp(),0,points=True))
    other=copy.deepcopy(drive);other['rows'][1]['t']+=.001;rejects('mismatched comparison times',lambda:study.state_difference(drive,other))
    other=copy.deepcopy(drive);other['state_phase_convention']='physical-full-Hamiltonian';rejects('mixed scalar phase conventions',lambda:study.state_difference(drive,other))

def exact_stepper_tests():
    import exact_stepper as es
    c=es.build_certificate();check('end-to-end rational certificate replay',es.verify_certificate(c))
    check('exact nonnegative quench accumulated action',c['accumulated_action']=='3/10')
    check('exact representation contribution',c['representation_error_upper']=='27/80000')
    check('small exact finite-step remainder',F(c['finite_step_algorithm_error_upper'])<F(1,10**20))
    check('end-to-end total below declared decimal',F(c['total_state_error_upper'])<F(337501,10**9))
    check('stored vector not normalized by force',c['computed_vector_was_renormalized'] is False and F(c['final_norm_squared'])!=1)
    check('simple Gaussian rational Taylor',es.rational_taylor([[(0,F(1))]],[(F(1),F(0))],1,1)==[(F(1),F(-1))])
    check('Taylor zero duration exact identity',es.rational_taylor([[(0,F(5))]],[(F(2),F(3))],0,3)==[(F(2),F(3))])
    check('Taylor zero order exact identity',es.rational_taylor([[(0,F(5))]],[(F(2),F(3))],1,0)==[(F(2),F(3))])
    check('product algorithm error exact',es.product_error_bound([F(1,10),F(1,5)])==F(8,25))
    for value in (True,float('nan'),-1):rejects('invalid Taylor duration '+str(value),lambda v=value:es.rational_taylor([[(0,F(1))]],[(F(1),F(0))],v,2))
    rejects('Boolean Taylor order',lambda:es.step_error_bound(1,1,True))
    rejects('cached operator Boolean coefficient',lambda:es.operator(3,True,F(1,20),F(1,10),1))
    rejects('cached operator Boolean degree',lambda:es.operator(True,1,0,0,1))
    rejects('empty product error sequence',lambda:es.product_error_bound([]))
    for name in ('degree','protocol','norm','coefficient','status','source','normalization','error'):
        bad=copy.deepcopy(c)
        if name=='degree':bad['degree']=4
        elif name=='protocol':bad['protocol']['segments'][1]['lambda1']='-1/20'
        elif name=='norm':bad['final_norm_squared']='1'
        elif name=='coefficient':bad['final_coefficients'][0]['real']='0'
        elif name=='status':bad['target']='continuum-Yang-Mills-state'
        elif name=='source':bad['source_hashes']={}
        elif name=='normalization':bad['computed_vector_was_renormalized']=True
        else:bad['total_state_error_upper']='0'
        rejects('exact-step certificate mutation '+name,lambda b=bad:es.verify_certificate(b))
    return c

def main():
    c=exact_tests();independent_chains();numerical_edges();step=exact_stepper_tests();OUT=ROOT/'output';OUT.mkdir(exist_ok=True)
    name='edge_tests_optimized.json' if not __debug__ else 'edge_tests.json'
    result={'status':'passed','optimized_python':not __debug__,'source_hashes':{**step['source_hashes'],'test_solver.py':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()},'checks':RESULTS,'exact_fixture_certificate':c,'exact_step_total_error_upper':step['total_state_error_upper']}
    (OUT/name).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'passed','checks':len(RESULTS),'output':name}))
if __name__=='__main__':main()
