"""Deterministic exact fixtures, unreduced link derivative oracle, and mutation gates."""
from fractions import Fraction as F
from pathlib import Path
import copy,json,hashlib,sys
import numpy as np
import two_plaquette as tp

RESULTS=[]
def check(name,condition,details=None):
    item={'name':name,'passed':bool(condition)}
    if details is not None:item['details']=details
    RESULTS.append(item)
    if not condition: raise RuntimeError(name)
def rejects(name,fn):
    try: fn()
    except (ValueError,TypeError,RuntimeError,KeyError,IndexError,ZeroDivisionError): check(name,True);return
    check(name,False)

def qmul(a,b): return np.r_[a[0]*b[0]-a[1:]@b[1:],a[0]*b[1:]+b[0]*a[1:]+np.cross(a[1:],b[1:])]
def qinv(a): return np.r_[a[0],-a[1:]]
def qmatrix(q):
    w,x,y,z=q
    # q representation wI - i (x sigma_x+y sigma_y+z sigma_z), matching positive vector cross.
    return np.array([[w-1j*z,-y-1j*x],[y-1j*x,w+1j*z]])
def qprod(*args):
    out=np.array([1.,0,0,0])
    for q in args:out=qmul(out,q)
    return out
def invariants(links):
    h1,h2,h3,h4,vL,vM,vR=links
    A=qprod(vM,qinv(h3),qinv(vL),h1)
    B=qprod(h2,vR,qinv(h4),qinv(vM))
    return A[0],B[0],qmul(A,B)[0]
def link_C(p,links,e,h):
    base=tp.evaluate(p,*invariants(links));out=0.
    for axis in range(3):
        step=np.zeros(4);step[0]=np.cos(h/2);step[axis+1]=np.sin(h/2)
        pp=links.copy();mm=links.copy();pp[e]=qmul(step,links[e]);mm[e]=qmul(qinv(step),links[e])
        out-=(tp.evaluate(p,*invariants(pp))-2*base+tp.evaluate(p,*invariants(mm)))/h**2
    return out

def exact_tests():
    check('Haar normalization',tp.moment((0,0,0))==1)
    anchors={(2,0,0):F(1,4),(0,2,0):F(1,4),(0,0,2):F(1,4),(1,1,1):F(1,16),(2,2,0):F(1,16),(0,0,4):F(1,8),(1,0,0):F(0)}
    for k,v in anchors.items():check('exact moment '+str(k),tp.moment(k)==v)
    check('K constant zero',tp.kinetic(tp.ONE)=={})
    for rho in (F(1,2),F(1),F(2),F(5)):
        check('Kx rho='+str(rho),tp.kinetic(tp.X,rho)=={(1,0,0):F(3,4)*(3+rho)})
        check('Kz rho='+str(rho),tp.kinetic(tp.Z,rho)=={(0,0,1):F(9,2)})
        p=tp.add(tp.mul(tp.X,tp.Y),tp.Z,F(-1,4));eig=F(9,2)+2*rho
        check('exact xy-z/4 eigenvector rho='+str(rho),tp.kinetic(p,rho)=={k:eig*v for k,v in p.items()})
        bs,G,K,_,_=tp.matrices(3,rho)
        check('exact Haar Gram positive rho='+str(rho),tp.inertia(G)==(0,0,len(G)))
        check('exact symmetric K rho='+str(rho),K==[list(row) for row in zip(*K)])
        for k in bs:
            out=tp.kinetic({k:F(1)},rho)
            check('triangular coefficient '+str((rho,k)),out.get(k,F(0))==tp.free_energy(k,rho) and all(sum(j)<sum(k) for j in out if j!=k))
        e=tp.ritz(3,1,0,0,rho);expected=sorted(float(tp.free_energy(k,rho)) for k in bs)
        check('free complete polynomial spectrum rho='+str(rho),np.max(np.abs(e-expected))<1e-10)
    for d in range(1,13):
        m=min(tp.free_energy(k) for k in tp.basis(d) if sum(k)==d)
        check('sharp shell minimum d='+str(d),m==tp.tail_lower(d-1))
    check('zero pivot 2x2 inertia',tp.inertia([[0,2],[2,0]])==(1,0,1))
    check('zero singular inertia',tp.inertia([[0,0],[0,0]])==(0,2,0))
    check('diagonal endpoint inertia',tp.inertia([[0,0,0],[0,-2,0],[0,0,3]])==(1,1,1))
    check('nontrivial 2x2 pivot elimination',tp.inertia([[0,1,2],[1,0,3],[2,3,0]])==(2,0,1))
    p=tp.add(tp.mul(tp.X,tp.Y),tp.Z,F(-1,4));check('xy-z/4 norm',tp.inner(p,p)==F(3,64))
    check('joint domain boundary',tp.domain(1,0,0) and not tp.domain(1,0,.1))
    for args in ((0,1,1,1),(1,-1,1,1),(1,1,1,0),(True,1,1,1),(float('nan'),1,1,1)):
        rejects('bad parameters '+str(args),lambda a=args:tp.parameters(*a))
    for d in (-1,True,1.5): rejects('bad degree '+str(d),lambda d=d:tp.basis(d))
    rejects('degree zero certificate',lambda:tp.certificate(0))
    rejects('insufficient tail',lambda:tp.certificate(1,1,20,20))

def link_oracles():
    rng=np.random.default_rng(20260909);links=rng.normal(size=(7,4));links/=np.linalg.norm(links,axis=1)[:,None]
    check('quaternion complex-matrix multiplication',np.max(abs(qmatrix(qmul(links[0],links[1]))-qmatrix(links[0])@qmatrix(links[1])))<1e-14)
    x,y,z=invariants(links);check('joint quotient domain from seven links',tp.domain(x,y,z,1e-14))
    # Independent full product of 2x2 matrices, with literal oriented link words.
    h1,h2,h3,h4,vL,vM,vR=[qmatrix(q) for q in links]
    A=vM@h3.conj().T@vL.conj().T@h1;B=h2@vR@h4.conj().T@vM.conj().T
    check('loop quotient complex matrix oracle',np.max(abs(np.array([x,y,z])-np.real([np.trace(A)/2,np.trace(B)/2,np.trace(A@B)/2])))<1e-14)
    # Six independent vertex gauge transformations, exact endpoint assignments.
    gg=rng.normal(size=(6,4));gg/=np.linalg.norm(gg,axis=1)[:,None]
    endpoints=[(0,1),(1,2),(3,4),(4,5),(0,3),(1,4),(2,5)]
    transformed=np.array([qprod(gg[s],q,qinv(gg[t])) for q,(s,t) in zip(links,endpoints)])
    check('six-vertex local gauge invariance',np.max(abs(np.array(invariants(transformed))-np.array([x,y,z])))<1e-14)
    rows=[]
    ps=[tp.X,tp.Z,tp.mul(tp.X,tp.Y),{(2,1,1):F(1)}]
    for rho in (.5,1,2):
        for p in ps:
            target=tp.evaluate(tp.kinetic(p,F(str(rho))),x,y,z)
            errs=[]
            for h in (.04,.02,.01):
                value=sum((rho if e==5 else 1)*link_C(p,links,e,h) for e in range(7));errs.append(abs(value-target))
            order=np.log2(errs[0]/errs[1]) if errs[1]>1e-13 else None
            check('seven-link derivative '+str((rho,p)),errs[-1]<3e-4 and (order is None or 1.8<order<2.2),{'errors':errs,'order':order})
            rows.append({'rho':rho,'polynomial':str(p),'errors':errs,'order':order})
    # Shared link cancellation must hold in z; replacing inverse by direct is resolved.
    check('shared link has zero Casimir on outer trace',abs(link_C(tp.Z,links,5,.01))<1e-9)
    wrongZ=qprod(qprod(links[5],qinv(links[2]),qinv(links[4]),links[0]),qprod(links[1],links[6],qinv(links[3]),links[5]))[0]
    check('missing dagger mutation detected',abs(wrongZ-z)>1e-3)
    check('separable four-plus-four kinetic mutation detected',tp.evaluate(tp.kinetic(tp.Z),x,y,z)!=tp.evaluate({(0,0,1):F(6)},x,y,z))
    return rows

def certificate_tests():
    c=tp.certificate(2,1,1,1);check('exact coupled certificate',tp.verify_certificate(c))
    mutations={'scope':'continuum-four-dimensional','dimension':99,'positive':False,'status':'numerical','tail_lower':'9999','comparison_threshold':'9999','width_requested':'1/100000000000','source_sha256':'0'*64,'alpha':'2','rho':'2','lambda2':'2','degree':True}
    for key,value in mutations.items():
        altered=copy.deepcopy(c);altered[key]=value;rejects('certificate mutation '+key,lambda a=altered:tp.verify_certificate(a))
    altered=copy.deepcopy(c);del altered['scope'];rejects('missing field rejected',lambda:tp.verify_certificate(altered))
    altered=copy.deepcopy(c);altered['A_brackets']=[];rejects('empty eigen collection rejected',lambda:tp.verify_certificate(altered))
    altered=copy.deepcopy(c);altered['A_brackets'][0]['lower']='999';rejects('wrong exact endpoint rejected',lambda:tp.verify_certificate(altered))
    altered=copy.deepcopy(c);altered['gap'][0]='1';rejects('false gap subtraction rejected',lambda:tp.verify_certificate(altered))
    zero=tp.certificate(1,1,0,0);check('zero magnetic exact certificate',tp.verify_certificate(zero) and F(zero['gap'][0])<3<F(zero['gap'][1]))
    check('zero coupling P-Q norm exact zero',all(v==0 for row in tp.coupling_square(2,F(0),F(0)) for v in row))
    for scale in (F(1,3),F(3)):
        e=tp.ritz(3,scale,scale,2*scale);ref=tp.ritz(3,1,1,2);check('rational physical scale '+str(scale),np.max(abs(e-float(scale)*ref))<1e-10)
    e=tp.ritz(3,1,1,2);swap=tp.ritz(3,1,2,1);check('plaquette exchange symmetry',np.max(abs(e-swap))<1e-10)
    check('integer public coupling exactness',tp.coupling_square(1,22,15)==tp.coupling_square(1,F(22),F(15)))
    huge=tp.certificate(1,10**20+1,0,0)
    check('large absolute scale precision',tp.verify_certificate(huge) and all(F(b['upper'])-F(b['lower'])<=F(huge['width_requested']) for k in ('A_brackets','B_brackets') for b in huge[k]))
    altered=copy.deepcopy(c);altered['A_brackets'][0]['lower_inertia'][0]=False
    rejects('Boolean inertia metadata',lambda:tp.verify_certificate(altered))
    pts=[tp.certificate(2,1,i,j) for i in range(3) for j in range(3)]
    box=tp.rectangle_certificate(pts);check('rectangle exact replay',tp.verify_rectangle(box))
    for kind in ('missing_cell','wrong_center','wrong_radius','wrong_alpha','coverage_hole','wrong_margin','false_positive'):
        bad=copy.deepcopy(box)
        if kind=='missing_cell':bad['cells'].pop()
        elif kind=='wrong_center':bad['cells'][0]['center']=['1','1']
        elif kind=='wrong_radius':bad['cells'][0]['radius_l1']='0'
        elif kind=='wrong_alpha':bad['cells'][0]['point_certificate']['alpha']='2'
        elif kind=='coverage_hole':bad['cells'][0]['x_interval']=['0','1/4']
        elif kind=='wrong_margin':bad['gap_lower']='3'
        else:bad['positive']=1
        rejects('rectangle mutation '+kind,lambda b=bad:tp.verify_rectangle(b))
    rejects('rectangle empty point collection',lambda:tp.rectangle_certificate([]))
    import run_study as study
    valid={'norm_max':0.,'work_max':0.,'final_energy':1.,'final_work':1.}
    rejects('unknown dynamics method',lambda:study.dynamic_acceptance(valid,'unknown'))
    bad=dict(valid,work_max=float('nan'));rejects('nonfinite work gate',lambda:study.dynamic_acceptance(bad,'DOP853'))
    history=[{'energy':1.,'integrated_work':1.,'norm_defect':0.,'work_defect':0.}]
    good=dict(valid,rows=history);check('complete raw work gate',study.dynamic_acceptance(good,'DOP853'))
    bad=copy.deepcopy(good);bad['rows'][0]['work_defect']=float('nan');rejects('transient nonfinite history',lambda:study.dynamic_acceptance(bad,'DOP853'))
    bad=dict(valid,rows=[]);rejects('empty diagnostic history',lambda:study.dynamic_acceptance(bad,'midpoint'))
    return c

def main():
    exact_tests();rows=link_oracles();c=certificate_tests()
    out=Path(__file__).parent/'output';out.mkdir(exist_ok=True)
    fixtures={'contract':tp.CONTRACT,'scope':tp.SCOPE,'source_sha256':tp.source_digest(),'measure_density':'2/pi^2','joint_domain':'|x|<=1,|y|<=1,(z-xy)^2<=(1-x^2)(1-y^2)','moments':{'1':'1','x^2':'1/4','y^2':'1/4','z^2':'1/4','xyz':'1/16','x^2*y^2':'1/16','z^4':'1/8'},'kinetic_rho1':{'K1':'0','Kx':'3x','Ky':'3y','Kz':'9z/2','Kxy':'13xy/2-z/2'},'free_gap_rho1':'3','orthogonal_fixture':'xy-z/4','orthogonal_fixture_norm_squared':'3/64','orthogonal_fixture_energy_rho1':'13/2'}
    (out/'exact_fixtures.json').write_text(json.dumps(fixtures,indent=2)+'\n')
    record={'status':'passed','optimized_python':not __debug__,'source_sha256':tp.source_digest(),'test_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'checks':RESULTS,'link_derivative_rows':rows,'fixture_certificate':c}
    dest=out/('edge_tests_optimized.json' if not __debug__ else 'edge_tests.json');dest.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({'status':'passed','checks':len(RESULTS),'output':str(dest)}))
if __name__=='__main__':main()
