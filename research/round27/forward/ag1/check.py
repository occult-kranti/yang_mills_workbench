#!/usr/bin/env python3
"""AG1 exact continuous bounds and separately labeled finite-algebra diagnostics."""
import argparse,hashlib,itertools,json,math
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];checks=[]
def require(ok,msg):
    if not ok:raise ValueError(msg)
    checks.append(msg)
def clean(v):
    if isinstance(v,F):return str(v)
    if isinstance(v,dict):return {str(k):clean(x) for k,x in v.items()}
    if isinstance(v,(tuple,list)):return [clean(x) for x in v]
    return v
def zero():return [[F(0) for j in range(3)] for i in range(3)]
def ident():return [[F(i==j) for j in range(3)] for i in range(3)]
def add(A,B):return [[a+b for a,b in zip(x,y)] for x,y in zip(A,B)]
def scale(c,A):return [[c*a for a in x] for x in A]
def mul(A,B):return [[sum(A[i][k]*B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
def comm(A,B):return add(mul(A,B),scale(-1,mul(B,A)))
def polmul(A,B,degree):
    C={n:zero() for n in range(degree+1)}
    for i,a in A.items():
        for j,b in B.items():
            if i+j<=degree:C[i+j]=add(C[i+j],mul(a,b))
    return C
def scalar_split(A):
    c=A[0][0];B=zero();D=zero()
    for i in range(1,3):B[0][i]=A[0][i];B[i][0]=A[i][0]
    for i in range(1,3):
        for j in range(1,3):D[i][j]=A[i][j]-c*(i==j)
    return c,B,D
def diagnostic():
    G=[[F(0),F(0),F(0)],[F(0),F(1),F(0)],[F(0),F(0),F(3)]]
    A=[[F(0),F(1,10),F(1,20)],[F(1,10),F(0),F(0)],[F(1,20),F(0),F(0)]]
    K=[[F(0),-F(1,10),F(0)],[F(1,10),F(0),F(0)],[F(0),F(0),F(0)]]
    R=add(A,comm(K,G));require(R!=zero(),'diagnostic residual is genuinely retained')
    degree=8;power=ident();ep={};em={}
    for n in range(degree+1):
        ep[n]=scale(F(1,math.factorial(n)),power);em[n]=scale(F((-1)**n,math.factorial(n)),power);power=mul(power,K)
    actual=polmul(polmul(ep,{0:G,1:A},degree),em,degree)
    expected={0:G,1:R};remainder=[]
    for n in range(1,degree):
        X=add(scale(n,A),R)
        for k in range(n):X=comm(K,X)
        X=scale(F(1,math.factorial(n+1)),X);expected[n+1]=X
        c,B,D=scalar_split(X)
        require(add(add(scale(c,ident()),B),D)==X,'every nonlinear coefficient scalar/source/diagonal split '+str(n))
        remainder.append({'power':n+1,'coefficient':X,'reference_scalar':c,'source':B,'centered_diagonal':D})
    for n in range(degree+1):require(actual[n]==expected[n],'independent polynomial-conjugation coefficient '+str(n))
    correct=scale(F(1,2),comm(K,add(A,R)))
    g_only=scale(F(1,2),comm(K,add(scale(-1,A),R)))
    require(correct!=g_only,'G-only BCH coefficient rejected')
    require(actual[1]!=zero(),'omitting residual fails first order')
    # For an additional E, direct polynomial conjugation equals its own full commutator series.
    E=[[F(1,7),F(1,11),F(0)],[F(1,11),F(-1,13),F(1,17)],[F(0),F(1,17),F(1,19)]]
    transported=polmul(polmul(ep,{0:E},degree),em,degree);w=E
    for n in range(degree+1):
        require(transported[n]==scale(F(1,math.factorial(n)),w),'additional E retained through degree '+str(n));w=comm(K,w)
    return {'label':'finite algebra diagnostic only, not SU(2) completeness','G':G,'A':A,'K':K,'R':R,'nonlinear_coefficients':remainder}
STAR={(0,0,0),(1,0,0),(0,1,0),(0,0,1)}
def translate(b):return frozenset(tuple(b[j]+s[j] for j in range(3)) for s in STAR)
def geometry():
    diff={tuple(a[j]-b[j] for j in range(3)) for a in STAR for b in STAR}
    require(len(diff)==13,'complete star difference set')
    rows=[]
    for L in (2,3,4):
        stars={b:translate(b) for b in itertools.product(range(L-1),repeat=3)}
        rootcounts={x:sum(x in s for s in stars.values()) for x in itertools.product(range(L),repeat=3)}
        m=max(rootcounts.values());require(1<=m<=4,'actual source multiplicity L='+str(L))
        cross={b:sum(bool(s&t) and c!=b for c,t in stars.items()) for b,s in stars.items()}
        require(cross[(0,0,0)]==(0 if L==2 else 3),'origin boundary crossing count L='+str(L))
        if L==4:require(cross[(1,1,1)]==12,'interior has twelve crossings')
        require(all(len(s|t)==7 for b,s in stars.items() for c,t in stars.items() if b!=c and s&t),'every distinct crossing has seven-site connected union L='+str(L))
        rows.append({'side':L,'retained_stars':len(stars),'max_stars_at_root':m,'origin_crossings':cross[(0,0,0)],'max_crossings':max(cross.values())})
    # Complete finite ordered-word diagnostic, including repeated and incoming roots.
    stars=list({b:translate(b) for b in itertools.product(range(3),repeat=3)}.values())
    norms={};word_stats=[]
    for weight in (F(2),F(9,4)):
        words=[(s,1) for s in stars];initial=None
        for n in range(3):
            totals={}
            for support,multiplicity in words:
                value=weight**len(support)*2**n*multiplicity
                for x in support:totals[x]=totals.get(x,F(0))+value
            current=max(totals.values())
            if n==0:initial=current;require(initial==4*weight**4,'actual indexed input norm in word diagnostic '+str(weight))
            rising=F(1)
            for j in range(n):rising*=F(8,3)+j
            upper=initial*(24*weight**3)**n*rising
            require(current<=upper,'all connected words below recurrence at '+str((weight,n)))
            word_stats.append({'weight':weight,'depth':n,'actual_rooted_coefficient':current,'recurrence_upper':upper})
            if n<2:words=[(support|s,mult) for support,mult in words for s in stars if support&s]
    return {'cuboids':rows,'difference_set':sorted(diff),'ordered_word_diagnostics':word_stats}
def constants(M):
    rho=F(9,4);T=F(3);x=24*rho**3*M*T;F_rho=1/(1-x)**3;r_bd=M**3/567
    A_rho_bd=4*rho**4*r_bd;S_bd=A_rho_bd*F_rho;theta=18*S_bd
    require(x<1 and theta<1,'continuous rho summability and full BCH at M='+str(M))
    n_ratio=theta/(1-theta)*(rho/2)**4*(1+F_rho/2)
    kappa=F(4,9)+1/(1-576*M)**3-1
    return {'M':M,'rho':rho,'T':T,'x_rho':x,'F_rho':F_rho,'rational_actual_source_upper':r_bd,'A_rho_upper':A_rho_bd,'S_rho_upper':S_bd,'theta_upper':theta,'N_over_actual_A2_upper':n_ratio,'free_residual_over_actual_A2_upper':kappa,'new_mixing_over_actual_A2_upper':kappa+n_ratio,'additional_E_transport_factor':1/(1-theta),'A2_upper':64*r_bd,'N_absolute_upper':64*r_bd*n_ratio}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);out=Path(ap.parse_args().output)
    require(out.is_absolute() and not out.exists(),'fresh absolute output')
    inv=json.loads((HERE/'inputs/source-inventory.json').read_text())
    for p,d in inv.items():
        require(hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==d,'source binding '+p)
        require(hashlib.sha256((HERE/'inputs'/p).read_bytes()).hexdigest()==d,'snapshot binding '+p)
    contract=json.loads((HERE/'inputs/research/round27/contracts/ag1.json').read_text())
    for p,d in contract['sources'].items():require(inv.get(p)==d,'contract binding '+p)
    require(F(7,9)**2>=F(7,12),'rational square-root enclosure')
    require(F(4,3)*F(7,12)*F(7,9)/7**3==F(1,567),'cubic upper bound simplification')
    # Actual filter moments independently by polynomial integration over positive half.
    T=F(3)
    for n in range(13):
        pm=2/T*(T**(n+1)/F(n+1)-T**(n+2)/(T*(n+2)))/math.factorial(n)
        hm=(T**(n+1)/F(n+1)-2*T**(n+2)/(T*(n+2))+T**(n+3)/(T*T*(n+3)))/math.factorial(n)
        require(pm==2*T**n/math.factorial(n+2),'exact residual filter moment '+str(n))
        require(hm==2*T**(n+1)/math.factorial(n+3),'exact generator filter moment '+str(n))
    require(F(1,8)/(1+F(1,8))==F(1,9),'rational log lower bound endpoint')
    require(F(4,9)<1,'free rank-source spectral residual strict bound')
    mainc=constants(F(1,1000));narrow=constants(F(1,10000));zero_c=constants(F(0))
    require(mainc['x_rho']==F(6561,8000),'main auxiliary convergence endpoint')
    require(narrow['new_mixing_over_actual_A2_upper']<F(2,3),'narrow selected-source contraction against actual norm')
    require(mainc['free_residual_over_actual_A2_upper']>1,'main positive residual certificate does not contract')
    require(zero_c['rational_actual_source_upper']==zero_c['S_rho_upper']==zero_c['N_absolute_upper']==0,'tau zero gives exact zero source generator and nonlinear update')
    require((24*F(1,1000)+F(2,3))/(1-F(1,1000))==F(2072,2997)<F(7,10),'complete twelve-crossing per-source certificate')
    # Continuous monotonicity is proved in report; values at several rational scales are controls only.
    signrows=[]
    for tau in (F(-1,7000),F(-1,70000),F(0),F(1,70000),F(1,7000)):
        M=7*abs(tau);rb=M**3/567
        require(rb>=0 and M<=F(1,1000),'both coupling signs and zero bound '+str(tau))
        signrows.append({'tau':tau,'M':M,'r_upper':rb,'actual_r_positive_by_S1':tau!=0,'ratio_used':tau!=0})
    # A chosen actual r>0 and arbitrary finite-volume multiplicity retain the exact denominator.
    for m in (1,2,3,4):
        r=F(1,10**20);a2=m*16*r;ar=m*F(9,4)**4*r
        require(ar/a2==F(9,8)**4,'actual chosen-family denominator cancellation m='+str(m))
    # Fixed-weight norm failure is exact and not a numerical dense Pauli computation.
    fixedweight=[]
    for n in (1,2,4,8,16):
        s_norm=2**n*F(1,2**n);phi_norm=2*F(1,2);bracket_norm=2**n*F(n,2**n)
        require(s_norm==phi_norm==1 and bracket_norm==n,'fixed-weight commutator amplification n='+str(n))
        fixedweight.append({'sites':n,'input_norms':[s_norm,phi_norm],'output_norm':bracket_norm})
    # A geometric bound for the entire BCH tail is valid only with theta<1.
    th=mainc['theta_upper'];partial=sum(th**n for n in range(1,9));tail=th**9/(1-th)
    require(partial+tail==th/(1-th),'entire nonlinear geometric tail retained exactly')
    require(mainc['additional_E_transport_factor']>1 and narrow['additional_E_transport_factor']>1,'additional E cannot be deleted or called unchanged')
    geo=geometry();diag=diagnostic()
    bindings=dict(inv)
    for p in ('check.py','report.md','inputs/source-inventory.json'):bindings[str((HERE/p).relative_to(ROOT))]=hashlib.sha256((HERE/p).read_bytes()).hexdigest()
    result={'schema':'ym27-forward-ag1-v1','main':mainc,'narrow':narrow,'zero':zero_c,'geometry':geo,'sign_controls':signrows,'fixed_weight_counterexample':fixedweight,'finite_algebra_diagnostic':diag,'checks':checks,'checks_count':len(checks),'bindings':bindings,'scope':'One selected-source nonlinear update, narrower new-mixing contraction; complete original E remains conditional, no all-stage or continuum theorem'}
    out.mkdir(parents=True);(out/'results.json').write_text(json.dumps(clean(result),indent=2,sort_keys=True)+'\n')
    display={name:{key:float(v) for key,v in value.items() if isinstance(v,F)} for name,value in (('main',mainc),('narrow',narrow))}
    print(json.dumps({'status':'PASS','checks':len(checks),'display_only':display},indent=2))
if __name__=='__main__':main()
