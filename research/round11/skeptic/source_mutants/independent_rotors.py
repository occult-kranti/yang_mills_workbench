"""Exact invariant algebra for two adjacent SU(2) plaquettes (seven links).

Only final numpy/scipy generalized eigensolves use floating arithmetic.
Fraction matrix entries, moment fixtures and certificate inertia are exact.
"""
from __future__ import annotations
from fractions import Fraction as F
from functools import lru_cache
from math import comb, isfinite
import hashlib
import json
from pathlib import Path
import numpy as np
from scipy.linalg import eigh

CONTRACT = "ym11-seven-link-v1"
SCOPE = "two-adjacent-open-plaquettes-seven-links-gauge-invariant-infinite-representation-space"
ZERO=(0,0,0)

def rational(v):
    if isinstance(v, bool): raise ValueError("Boolean is not a parameter")
    try: return F(str(v)) if isinstance(v,float) else F(v)
    except (ValueError,TypeError,OverflowError,ZeroDivisionError) as e: raise ValueError("finite rational required") from e

def parameters(alpha=1,lambda1=0,lambda2=0,rho=1):
    a,l1,l2,r=map(rational,(alpha,lambda1,lambda2,rho))
    if a<=0 or r<=0 or l1<0 or l2<0: raise ValueError("alpha,rho>0 and lambda1,lambda2>=0 required")
    return a,l1,l2,r

def degree_checked(d):
    if type(d) is not int or d<0: raise ValueError("degree must be nonnegative integer")
    return d

def basis(d):
    degree_checked(d)
    return [(a,b,n-a-b) for n in range(d+1) for a in range(n+1) for b in range(n-a+1)]

def add(p,q,scale=F(1)):
    out=dict(p)
    for k,v in q.items(): out[k]=out.get(k,F(0))+scale*v
    return {k:v for k,v in out.items() if v}

def mul(p,q):
    out={}
    for a,u in p.items():
        for b,v in q.items():
            k=tuple(a[i]+b[i] for i in range(3)); out[k]=out.get(k,F(0))+u*v
    return {k:v for k,v in out.items() if v}

def deriv(p,i):
    out={}
    for k,v in p.items():
        if k[i]:
            j=list(k); j[i]-=1; out[tuple(j)]=v*k[i]
    return out

ONE={ZERO:F(1)}
X={(1,0,0):F(1)};Y={(0,1,0):F(1)};Z={(0,0,1):F(1)}

def kinetic(p,rho=1):
    """K_rho = 3 C_A + 3 C_B + rho C_shared, C spin j -> j(j+1)."""
    r=rational(rho)
    out={}
    for i,coord in enumerate((X,Y,Z)):
        out=add(out,mul(coord,deriv(p,i)),(3*(3+r)/4 if i<2 else F(6)))
        out=add(out,mul(add(ONE,mul(coord,coord),-1),deriv(deriv(p,i),i)),(-(3+r)/4 if i<2 else F(-2)))
    out=add(out,mul(add(Z,mul(X,Y),-1),deriv(deriv(p,0),1)),F(0))
    out=add(out,mul(add(Y,mul(X,Z),-1),deriv(deriv(p,0),2)),F(-2))
    out=add(out,mul(add(X,mul(Y,Z),-1),deriv(deriv(p,1),2)),F(-2))
    return out

@lru_cache(None)
def haar_x_power(n):
    """E[x^n] for a scalar coordinate of normalized Haar S^3."""
    if n<0: raise ValueError("negative moment")
    if n%2: return F(0)
    m=n//2
    return F(comb(2*m,m),4**m*(m+1))

@lru_cache(None)
def radial_moment(n,k):
    """E[x^n (1-x²)^k]."""
    return sum(((-1)**j*comb(k,j)*haar_x_power(n+2*j) for j in range(k+1)),F(0))

@lru_cache(None)
def moment(p):
    """Haar E[x^a y^b z^c], z=xy-sqrt(1-x²)sqrt(1-y²)u, u~U[-1,1]."""
    a,b,c=p
    if min(p)<0: raise ValueError("negative exponent")
    return sum((F(comb(c,2*k),2*k+1)*radial_moment(a+c-2*k,k)*radial_moment(b+c-2*k,k) for k in range(c//2+1)),F(0))

def inner(p,q): return sum((v*moment(k) for k,v in mul(p,q).items()),F(0))
def evaluate(p,x,y,z): return sum(float(v)*x**k[0]*y**k[1]*z**k[2] for k,v in p.items())
def domain(x,y,z,tol=0): return abs(x)<=1+tol and abs(y)<=1+tol and (z-x*y)**2 <= (1-x*x)*(1-y*y)+tol

def free_energy(k,rho=1):
    a,b,c=k;r=rational(rho)
    j=F(a+c,2);s=F(b+c,2);ell=F(a+b,2)
    return 3*j*(j+1)+3*s*(s+1)+r*ell*(ell+1)

def free_gap(rho=1):
    r=rational(rho)
    if r<=0: raise ValueError("rho must be positive")
    return min(F(3,4)*(3+r),F(9,2))

def tail_lower(degree,alpha=1,rho=1):
    """Exact minimum in first omitted layer; scaling proves later layers larger."""
    d=degree_checked(degree)+1;a,_,_,r=parameters(alpha,0,0,rho)
    # Lowering any nonzero exponent decreases every spin label or leaves it fixed.
    # Hence every later shell has minimum at least this first omitted shell.
    if r==1: return a*(F(5,8)*d*d+2*d+F(3,8)*(d%2))
    return a*min(free_energy((i,j,d-i-j),r) for i in range(d+1) for j in range(d-i+1))

@lru_cache(None)
def matrices(degree,rho=F(1)):
    bs=basis(degree);polys=[{p:F(1)} for p in bs]
    kp=[kinetic(p,rho) for p in polys]
    G=[[inner(p,q) for q in polys] for p in polys]
    K=[[inner(p,q) for q in kp] for p in polys]
    MX=[[inner(p,mul(X,q)) for q in polys] for p in polys]
    MY=[[inner(p,mul(Y,q)) for q in polys] for p in polys]
    if K!=[list(r) for r in zip(*K)]: raise RuntimeError("exact K symmetry failed")
    return bs,G,K,MX,MY

def combine(G,K,MX,MY,alpha,lambda1,lambda2):
    return [[alpha*K[i][j]+(lambda1+lambda2)*G[i][j]-lambda1*MX[i][j]-lambda2*MY[i][j] for j in range(len(G))] for i in range(len(G))]

def floating(M): return np.array([[float(v) for v in row] for row in M],dtype=float)

def ritz(degree,alpha=1,lambda1=0,lambda2=0,rho=1,vectors=False):
    a,l1,l2,r=parameters(alpha,lambda1,lambda2,rho)
    bs,G,K,MX,MY=matrices(degree,r)
    H=combine(G,K,MX,MY,a,l1,l2)
    vals,vec=eigh(floating(H),floating(G),check_finite=True)
    if not np.all(np.isfinite(vals)): raise RuntimeError("nonfinite Ritz spectrum")
    return (vals,vec,(bs,G,K,MX,MY,H)) if vectors else vals

def inertia(M):
    """Exact symmetric congruence inertia; nonzero diagonal pivot or 2x2 zero-diagonal pivot."""
    A=[list(map(F,row)) for row in M]
    if any(len(row)!=len(A) for row in A) or A!=[list(r) for r in zip(*A)]: raise ValueError("symmetric square matrix required")
    neg=zero=pos=0
    while A:
        n=len(A);pivot=next((i for i in range(n) if A[i][i]),None)
        if pivot is not None:
            if pivot:
                A[0],A[pivot]=A[pivot],A[0]
                for row in A: row[0],row[pivot]=row[pivot],row[0]
            p=A[0][0];neg+=p<0;pos+=p>0
            A=[[A[i][j]-A[i][0]*A[0][j]/p for j in range(1,n)] for i in range(1,n)]
        else:
            pair=next(((i,j) for i in range(n) for j in range(i+1,n) if A[i][j]),None)
            if pair is None: zero+=n;break
            i,j=pair;order=[i,j]+[k for k in range(n) if k not in pair]
            A=[[A[u][v] for v in order] for u in order];p=A[0][1]
            neg+=1;pos+=1
            A=[[A[u][v]-(A[u][0]*A[1][v]+A[u][1]*A[0][v])/p for v in range(2,n)] for u in range(2,n)]
    return int(neg),int(zero),int(pos)

def shifted(M,G,t): return [[M[i][j]-t*G[i][j] for j in range(len(G))] for i in range(len(G))]

def exact_bracket(M,G,index,guess,width=F(1,10**7)):
    """A float proposes endpoints; exact inertia locates and refines to absolute width."""
    if index<0 or index>=len(G): raise ValueError("invalid eigenindex")
    width=rational(width)
    if width<=0: raise ValueError("positive width required")
    if not isfinite(float(guess)): raise ValueError("finite numerical proposal required")
    center=F(str(float(guess)));radius=width/2
    for _ in range(200):
        lo=center-radius;hi=center+radius
        ni=inertia(shifted(M,G,lo));nj=inertia(shifted(M,G,hi))
        if ni[1]==0 and nj[1]==0 and ni[0]<=index<nj[0]: break
        radius*=2
    else: raise RuntimeError("could not locate rational eigenvalue bracket")
    for _ in range(1000):
        if hi-lo<=width:
            return {"index":index,"lower":str(lo),"upper":str(hi),"lower_inertia":list(ni),"upper_inertia":list(nj)}
        mid=(lo+hi)/2;nm=inertia(shifted(M,G,mid))
        if nm[1]:
            if nm[0]<=index<nm[0]+nm[1]:
                radius=min(width/3,(hi-lo)/3)
                for _ in range(200):
                    lower=mid-radius;upper=mid+radius
                    left=inertia(shifted(M,G,lower));right=inertia(shifted(M,G,upper))
                    if left[1]==0 and right[1]==0 and left[0]<=index<right[0]:
                        lo,hi,ni,nj=lower,upper,left,right;break
                    radius/=2
                else:raise RuntimeError("could not isolate exact-root endpoint")
                continue
            # Avoid non-target exact roots as endpoints; finitely many forbidden choices.
            for divisor in range(3,len(G)+4):
                mid=lo+(hi-lo)/divisor;nm=inertia(shifted(M,G,mid))
                if not nm[1]:break
            else:raise RuntimeError("could not choose non-eigenvalue interior point")
        if nm[0]<=index:lo,ni=mid,nm
        else:hi,nj=mid,nm
    raise RuntimeError("exact refinement exceeded bounded iteration budget")

def solve_exact(A,B):
    """Fraction Gaussian elimination, multiple right-hand sides."""
    n=len(A);m=len(B[0]);U=[list(A[i])+list(B[i]) for i in range(n)]
    for k in range(n):
        p=next((i for i in range(k,n) if U[i][k]),None)
        if p is None: raise ValueError("singular matrix")
        U[k],U[p]=U[p],U[k]
        for i in range(k+1,n):
            if U[i][k]:
                s=U[i][k]/U[k][k]
                for j in range(k,n+m): U[i][j]-=s*U[k][j]
    Xo=[[F(0)]*m for _ in range(n)]
    for i in range(n-1,-1,-1):
        for j in range(m): Xo[i][j]=(U[i][n+j]-sum((U[i][k]*Xo[k][j] for k in range(i+1,n)),F(0)))/U[i][i]
    return Xo

@lru_cache(None)
def coupling_square(degree,lambda1,lambda2,rho=F(1)):
    _,lambda1,lambda2,rho=parameters(1,lambda1,lambda2,rho)
    bs,G,_,MX,MY=matrices(degree,rho);n=len(bs)
    # W=-lambda1*x-lambda2*y. Constants have no P-Q coupling.
    W=add({k:v*lambda1 for k,v in X.items()},Y,lambda2)
    WP=[mul(W,{p:F(1)}) for p in bs]
    W2=[[inner(p,q) for q in WP] for p in WP]
    M=[[lambda1*MX[i][j]+lambda2*MY[i][j] for j in range(n)] for i in range(n)]
    solved=solve_exact(G,M)
    return [[W2[i][j]-sum((M[i][k]*solved[k][j] for k in range(n)),F(0)) for j in range(n)] for i in range(n)]

def source_digest(): return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()

def certificate(degree,alpha=1,lambda1=0,lambda2=0,rho=1,width=F(1,10**7)):
    if degree_checked(degree)<1: raise ValueError("degree >=1 required for first gap")
    a,l1,l2,r=parameters(alpha,lambda1,lambda2,rho);width=rational(width)
    vals,_,(_,G,K,MX,MY,H)=ritz(degree,a,l1,l2,r,True)
    abr=[exact_bracket(H,G,k,vals[k],width) for k in (0,1)]
    tau=tail_lower(degree,a,r)
    U=F(abr[1]['upper'])+max(F(1,10),width)
    if U>=tau: raise ValueError("certified first excitation upper bound does not fit below tail")
    C=coupling_square(degree,l1,l2,r)
    B=[[H[i][j]-C[i][j]/(tau-U) for j in range(len(G))] for i in range(len(G))]
    bvals=eigh(floating(B),floating(G),eigvals_only=True)
    bbr=[exact_bracket(B,G,k,bvals[k],width) for k in (0,1)]
    lo=F(bbr[1]['lower'])-F(abr[0]['upper']);hi=F(abr[1]['upper'])-F(bbr[0]['lower'])
    return {"contract":CONTRACT,"scope":SCOPE,"arithmetic":"exact-Fraction-congruence","degree":degree,"dimension":len(G),"alpha":str(a),"lambda1":str(l1),"lambda2":str(l2),"rho":str(r),"width_requested":str(width),"tail_lower":str(tau),"comparison_threshold":str(U),"A_brackets":abr,"B_brackets":bbr,"energy0":[bbr[0]['lower'],abr[0]['upper']],"energy1":[bbr[1]['lower'],abr[1]['upper']],"gap":[str(lo),str(hi)],"positive":lo>0,"status":"certified-positive" if lo>0 else "certified-enclosure-inconclusive-positivity","source_sha256":source_digest()}

def verify_certificate(c,bind_source=True):
    """Replay contract, matrices, exact endpoints, tail and every decisive semantic field."""
    required={"contract","scope","arithmetic","degree","dimension","alpha","lambda1","lambda2","rho","width_requested","tail_lower","comparison_threshold","A_brackets","B_brackets","energy0","energy1","gap","positive","status","source_sha256"}
    if set(c)!=required: raise ValueError("certificate field set mismatch")
    if c['contract']!=CONTRACT or c['scope']!=SCOPE or c['arithmetic']!="exact-Fraction-congruence": raise ValueError("contract/scope/arithmetic mismatch")
    if bind_source and c['source_sha256']!=source_digest(): raise ValueError("source hash mismatch")
    if not isinstance(c['source_sha256'],str) or len(c['source_sha256'])!=64 or any(x not in '0123456789abcdef' for x in c['source_sha256']): raise ValueError("invalid source digest")
    d=degree_checked(c['degree'])
    if d<1: raise ValueError("degree >=1 required")
    a,l1,l2,r=parameters(c['alpha'],c['lambda1'],c['lambda2'],c['rho'])
    bs,G,K,MX,MY=matrices(d,r);H=combine(G,K,MX,MY,a,l1,l2)
    if type(c['dimension']) is not int or c['dimension']!=len(G): raise ValueError("dimension mismatch")
    width=rational(c['width_requested']);tau=tail_lower(d,a,r);U=rational(c['comparison_threshold'])
    if width<=0 or rational(c['tail_lower'])!=tau or U>=tau: raise ValueError("invalid precision or tail premise")
    C=coupling_square(d,l1,l2,r);B=[[H[i][j]-C[i][j]/(tau-U) for j in range(len(G))] for i in range(len(G))]
    for records,M in ((c['A_brackets'],H),(c['B_brackets'],B)):
        if not isinstance(records,list) or len(records)!=2: raise ValueError("two ordered eigenvalue brackets required")
        for k,br in enumerate(records):
            if set(br)!={"index","lower","upper","lower_inertia","upper_inertia"} or type(br['index']) is not int or br['index']!=k: raise ValueError("bracket index mismatch")
            lo,hi=rational(br['lower']),rational(br['upper'])
            if lo>=hi or hi-lo>width: raise ValueError("invalid bracket width")
            if any(not isinstance(br[key],list) or len(br[key])!=3 or any(type(v) is not int or v<0 for v in br[key]) for key in ('lower_inertia','upper_inertia')): raise ValueError('integer inertia metadata required')
            nl=inertia(shifted(M,G,lo));nh=inertia(shifted(M,G,hi))
            if list(nl)!=br['lower_inertia'] or list(nh)!=br['upper_inertia'] or nl[1] or nh[1] or not(nl[0]<=k<nh[0]): raise ValueError("endpoint inertia mismatch")
    if F(c['A_brackets'][1]['upper'])>=U or F(c['B_brackets'][1]['upper'])>=U: raise ValueError("first two comparison levels must lie below U")
    e0=[c['B_brackets'][0]['lower'],c['A_brackets'][0]['upper']];e1=[c['B_brackets'][1]['lower'],c['A_brackets'][1]['upper']]
    gap=[F(e1[0])-F(e0[1]),F(e1[1])-F(e0[0])];positive=gap[0]>0
    if c['energy0']!=e0 or c['energy1']!=e1 or list(map(F,c['gap']))!=gap or type(c['positive']) is not bool or c['positive']!=positive or c['status']!=("certified-positive" if positive else "certified-enclosure-inconclusive-positivity"): raise ValueError("energy/gap/status mismatch")
    return True

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--degree',type=int,default=3);p.add_argument('--alpha',default='1');p.add_argument('--lambda1',default='1');p.add_argument('--lambda2',default='1');p.add_argument('--rho',default='1');p.add_argument('--certificate',action='store_true');args=p.parse_args()
    if args.certificate:
        c=certificate(args.degree,args.alpha,args.lambda1,args.lambda2,args.rho);verify_certificate(c);print(json.dumps(c,indent=2))
    else:
        e=ritz(args.degree,args.alpha,args.lambda1,args.lambda2,args.rho);print(json.dumps({"status":"numerical-Ritz-estimates-not-gap-certificate","energies":e[:6].tolist(),"gap_estimate":float(e[1]-e[0]) if len(e)>1 else None},indent=2))

# Continuous rectangle certificates are deliberately fixed to an explicit small cover.
def rectangle_certificate(points):
    expected=[(F(i),F(j)) for i in range(3) for j in range(3)]
    keyed={}
    for c in points:
        verify_certificate(c)
        key=(F(c['lambda1']),F(c['lambda2']))
        if key in keyed: raise ValueError('duplicate center')
        if F(c['alpha'])!=1 or F(c['rho'])!=1: raise ValueError('rectangle requires alpha=rho=1')
        keyed[key]=c
    if set(keyed)!=set(expected): raise ValueError('rectangle requires complete 3 by 3 center set')
    cells=[]
    for x,y in expected:
        c=keyed[x,y];margin=F(c['gap'][0])-2
        cells.append({'center':[str(x),str(y)],'x_interval':[str(max(F(0),x-F(1,2))),str(min(F(2),x+F(1,2)))],'y_interval':[str(max(F(0),y-F(1,2))),str(min(F(2),y+F(1,2)))],'radius_l1':'1','margin':str(margin),'point_certificate':c})
    lower=min(F(cell['margin']) for cell in cells)
    return {'contract':CONTRACT,'scope':SCOPE,'kind':'continuous-two-coupling-rectangle','alpha':'1','rho':'1','domain':[['0','2'],['0','2']],'gap_lipschitz_l1':'2','cells':cells,'gap_lower':str(lower),'positive':lower>0,'status':'certified-positive' if lower>0 else 'inconclusive','source_sha256':source_digest()}

def verify_rectangle(c):
    required={'contract','scope','kind','alpha','rho','domain','gap_lipschitz_l1','cells','gap_lower','positive','status','source_sha256'}
    if set(c)!=required or type(c['positive']) is not bool: raise ValueError('rectangle field/type mismatch')
    if not isinstance(c['cells'],list) or len(c['cells'])!=9: raise ValueError('missing cover cells')
    # Canonical construction validates point parameters and derives exact cells, coverage and margin.
    expected=rectangle_certificate([cell['point_certificate'] for cell in c['cells']])
    if c!=expected: raise ValueError('rectangle coverage/semantic mismatch')
    return True

# Descriptive aliases for external exact-replay consumers.
verify_continuous_rectangle = verify_rectangle
continuous_rectangle_certificate = rectangle_certificate
