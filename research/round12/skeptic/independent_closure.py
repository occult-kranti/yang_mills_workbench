#!/usr/bin/env python3
"""Independent exact diagonal SU(2) link jets and tilted-Haar moment bounds."""
from fractions import Fraction as F
from math import comb,factorial,ceil
from pathlib import Path
import hashlib,json

def q(r=0,i=0):return F(r),F(i)
def qa(a,b):return a[0]+b[0],a[1]+b[1]
def qs(a,s):return a[0]*s,a[1]*s
def qm(a,b):return a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def qc(a):return a[0],-a[1]
def dm(a,b):return tuple(qm(x,y) for x,y in zip(a,b))
def da(a,b):return tuple(qa(x,y) for x,y in zip(a,b))
def ds(a,s):return tuple(qs(x,s) for x in a)
def dc(a):return tuple(qc(x) for x in a)
def trace(a):return qa(*a)
I=(q(1),q(1));ZERO=(q(),q());T=(q(F(1,2)),q(-F(1,2)));iT=(q(0,F(1,2)),q(0,-F(1,2)))
def jetmul(a,b):return dm(a[0],b[0]),da(dm(a[1],b[0]),dm(a[0],b[1]))
def haar(n):return F(comb(n,n//2),(n//2+1)*4**(n//2)) if n%2==0 else F(0)
def ivadd(a,b):return a[0]+b[0],a[1]+b[1]
def ivscale(a,b):return tuple(sorted((a[0]*b,a[1]*b)))
def tilted_moment(kappa,n,M=55):
    k=F(kappa);error=F(3)**ceil(abs(k))*abs(k)**(M+1)/factorial(M+1)
    raw=sum((k**j*haar(n+j)/factorial(j) for j in range(M+1)),F(0))
    z=sum((k**j*haar(j)/factorial(j) for j in range(M+1)),F(0))
    if z-error<=0:raise RuntimeError('normalization lower bound is not positive')
    candidates=[a/b for a in (raw-error,raw+error) for b in (z-error,z+error)]
    return min(candidates),max(candidates)

def main():
    gates=[];matrix_rows=[]
    def check(ok,name,detail=None):
        if not ok:raise RuntimeError(name)
        gates.append({'test':name,'passed':True,'detail':detail})
    for x,s in [(F(3,5),F(4,5)),(F(0),F(1)),(F(-3,5),F(4,5))]:
        U=(q(x,s),q(x,-s));dU=dm(iT,U);dag=dc(U);ddag=dc(dU)
        check(dm(U,dag)==I,'unitary_diagonal_fixture.'+str(x))
        directed=qs(qa(trace(U),trace(dag)),-F(1,2));later=qs(qa(trace(U),trace(dag)),-F(1,4))
        check(directed==qs(later,2) and (directed!=later if x else directed==q()),'equation8_directed_count.'+str(x))
        dS=qs(qa(trace(dU),trace(ddag)),-F(1,4))
        printed=qm(q(0,-F(1,16)),trace(da(dm(T,U),ds(dm(T,dag),-1))))
        check(printed==qs(dS,F(1,4)) and printed!=dS,'equation14_exact_matrix_derivative.'+str(x))
        matrix_rows.append({'x':str(x),'sin_theta':str(s),'first_action':list(map(str,directed)),'later_action':list(map(str,later)),
                            'direct_derivative':list(map(str,dS)),'printed_derivative':list(map(str,printed))})
    # Periodic extent3 protects this factor test from open-boundary staple conventions.
    N=3;U=(q(0,1),q(0,-1));links={(a,b,mu):((U,dm(iT,U)) if (a,b,mu)==(0,0,0) else (I,ZERO)) for a in range(N) for b in range(N) for mu in range(2)}
    total=q();dtotal=q()
    def shifted(v,mu):return tuple((v[j]+int(j==mu))%N for j in range(2))
    for a in range(N):
        for b in range(N):
            for mu,nu in ((0,1),(1,0)):
                v=(a,b);vm=shifted(v,mu);vn=shifted(v,nu)
                word=[links[(*v,mu)],links[(*vm,nu)],tuple(dc(x) for x in links[(*vn,mu)]),tuple(dc(x) for x in links[(*v,nu)])]
                out=(I,ZERO)
                for j in word:out=jetmul(out,j)
                total=qa(total,trace(out[0]));dtotal=qa(dtotal,trace(out[1]))
    periodic_derivative=qs(qa(dtotal,qc(dtotal)),-F(1,8))
    Sigma=ds(I,2);printed=qm(q(0,-F(1,16)),trace(da(dm(dm(T,U),dc(Sigma)),ds(dm(dm(Sigma,T),dc(U)),-1))))
    check(periodic_derivative==q(1) and printed==q(F(1,4)),'periodic_extent3_equation14_quarter_factor')
    source=trace(dm(T,dm(iT,I)));printed_source=qs(trace(I),F(1,4))
    check(source==q(0,F(1,2)) and printed_source==q(F(1,2)) and source!=printed_source,'equation18_source_phase')
    for n in range(18):check(n*haar(n-1)-(n+3)*haar(n+1)==0 if n else haar(1)==0,'exact_haar_recurrence.'+str(n))
    for kappa in (F(-2),F(-1,2),F(0),F(1,2),F(2)):
        moments=[tilted_moment(kappa,n) for n in range(9)]
        for n in range(7):
            out=ivscale(moments[n-1],n) if n else (F(0),F(0))
            out=ivadd(out,ivscale(moments[n+1],-(n+3)));out=ivadd(out,ivscale(moments[n],kappa));out=ivadd(out,ivscale(moments[n+2],-kappa))
            check(out[0]<=0<=out[1],f'tilted_interval_recurrence.{kappa}.{n}')
        m1=moments[1];square_max=max(m1[0]**2,m1[1]**2);variance_lower=moments[2][0]-square_max
        analytic_weaker=F(1,4*3**ceil(2*abs(kappa)))
        check(variance_lower>=analytic_weaker,f'positive_variance.{kappa}')
        if kappa:check(abs(kappa)*variance_lower>0,f'point_closure_has_resolved_residual.{kappa}')
    check(haar(1)==0 and 1-4*haar(2)==0 and haar(2)!=haar(1)**2,'zero_coupling_first_identity_blind_next_identity_not')
    check(3**2-1>4,'SU3_D4_rank_obstruction')
    check(2**2-1<=4,'SU2_D4_rank_test_only_is_inconclusive')
    here=Path(__file__).resolve();result={'status':'passed','optimized_python':not __debug__,'source_sha256':hashlib.sha256(here.read_bytes()).hexdigest(),
      'gate_count':len(gates),'gates':gates,'matrix_fixtures':matrix_rows,
      'reviewed_source':'https://arxiv.org/html/2608.05415v1','reviewed_display_equations':[5,8,14,18,19,29],
      'scope':'Displayed formula checks and a separately defined point-concentration closure; not a refutation of all scalar ansatze.',
      'rank_argument':'For eta a D by (N²−1) matrix, rank(eta^T g eta)≤rank(eta)≤D over either R or C; identity requires N²−1≤D.'}
    here.with_name('closure_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'gate_count':len(gates)}))
if __name__=='__main__':main()
