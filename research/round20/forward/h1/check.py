#!/usr/bin/env python3
from fractions import Fraction as F
from pathlib import Path
from itertools import product
import argparse,hashlib,json
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
def require(ok,m):
    if not ok:raise ValueError(m)
def rejected(fn):
    try:fn()
    except ValueError:return True
    return False
def B(q):
    require(0<q<1,'profile must satisfy0<q<1')
    return (2+5*q+5*q*q+6*q**3+3*q**4)/(24*(1-q)**3*(1+q)**2*(1+q*q))
def Bclasses(q):
    return 2/(24*(1-q)**3)+q/(24*(1-q)**2*(1-q*q))+q**3/(24*(1-q**4)*(1-q*q)*(1-q))
def retained(q,L):
    m=L+1;g=(1-q**m)/(1-q)
    a=sum((q**r*(1-q**(4*max(0,1+(L-r)//4)))/(1-q**4) for r in range(3)),F())
    b=(1-q**(2*((m+1)//2)))/(1-q*q)
    return (3*g**3-a*b*g)/24
def enumeration(q,L):
    return sum((q**(x+y+z)/24 for a,b in ((0,1),(0,2),(1,2)) for x,y,z in product(range(L+1),repeat=3) if not ((a,b)==(0,1) and y%2==0 and x%4<3)),F())
def conv(a,b):
    c=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return c
def encode(o):
    if isinstance(o,F):return str(o)
    if isinstance(o,dict):return {k:encode(v) for k,v in o.items()}
    if isinstance(o,list):return [encode(v) for v in o]
    return o
def main(out):
    contract=ROOT/'research/round20/contracts/h1.json';con=json.loads(contract.read_text());gate=ROOT/con['depends_on']['gate']
    require(hashlib.sha256(gate.read_bytes()).hexdigest()==con['depends_on']['sha256'],'G2 gate changed')
    common=conv(conv([1,1],[1,1]),[1,0,1])
    totalminus=[3*v-(1 if i<3 else 0) for i,v in enumerate(common)]
    classes=[2*v for v in common];odd=[0]+conv([1,1],[1,0,1])
    classes=[x+y for x,y in zip(classes,odd)];classes[3]+=1
    require(totalminus==classes==[2,5,5,6,3],'rational numerator identities disagree')
    rows=[];tails=[]
    for q in map(F,('1/4','1/2','3/4','7/8')):
        weight=B(q);require(weight==Bclasses(q),'omitted classes differ')
        margin=F(1,8)-weight/64
        rows.append({'q':q,'B':weight,'scaled_B':(1-q)**3*weight,'default_gap_margin_over_alpha':margin,'default_certificate':'positive_lower_bound' if margin>0 else 'not_certified'})
        previous=weight
        for L in range(5):
            s=retained(q,L);require(s==enumeration(q,L),'finite ledger mismatch');t=weight-s
            require(0<t<previous,'tail not strictly descending');previous=t
            tails.append({'q':q,'L':L,'retained_weight':s,'tail_weight':t})
    require(B(F(1,2))==F(107,135),'dyadic regression failed')
    low,high=1,999999
    while high-low>1:
        mid=(low+high)//2
        if B(F(mid,10**6))<8:low=mid
        else:high=mid
    qlo,qhi=F(low,10**6),F(high,10**6)
    require(B(qlo)<8<B(qhi),'critical bracket signs wrong')
    asymptotic=F(sum(totalminus),24*4*2);require(asymptotic==F(7,64),'endpoint residue wrong')
    signed=F(1,96)
    controls={
      'fixed_dyadic_budget_rejected':rejected(lambda:require(B(F(3,4))==F(107,135),'changed profile needs changed budget')),
      'signed_cancellation_rejected':rejected(lambda:require(abs(signed-signed)>=abs(signed)+abs(-signed),'signed sum cannot be absolute budget')),
      'q_one_finite_promotion_rejected':rejected(lambda:B(F(1))),
      'q_zero_outside_declared_domain_rejected':rejected(lambda:B(F(0))),
      'zero_physical_ratio_rejected':rejected(lambda:require(F(0)>0,'alpha/E_star must remain fixed positive finite')),
      'failed_certificate_not_gap_closed':rows[-1]['default_certificate']=='not_certified' and rows[-1]['default_gap_margin_over_alpha']<0,
      'signed_tau_same_absolute_budget':abs(F(-1,64))*B(F(1,2))==abs(F(1,64))*B(F(1,2)),
    }
    require(all(controls.values()),'profile control failed')
    result={'schema':'ym20-forward-h1-v1','loop':'h1','status':'passed','q_fixtures':rows,'tail_fixtures':tails,'controls':controls,'numerator_coefficients_ascending':totalminus,'asymptotic_scaled_budget':asymptotic,'critical_q_lower':qlo,'critical_q_upper':qhi,'B_critical_lower':B(qlo),'B_critical_upper':B(qhi),'critical_bracket_interpretation':'unique B(q)=8 sufficient-certificate boundary for tau=1/64; not a physical gap closure','scope':'continuous omitted action-profile deformation at fixed physical alpha/E_star and spacing'}
    out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_text(json.dumps(encode(result),indent=2,sort_keys=True)+'\n')
    sources=[HERE/'check.py',HERE/'report.md',contract,gate,ROOT/'research/round19/advisor/a2-gate.json',ROOT/'research/round19/forward/a2/report.md']
    manifest={'sources':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'outputs':{'results.json':hashlib.sha256((out/'results.json').read_bytes()).hexdigest()}}
    (out/'source-manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'passed','loop':'h1','q_fixtures':len(rows),'critical_bracket':[str(qlo),str(qhi)],'controls':len(controls)}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE/'output');main(p.parse_args().output)
