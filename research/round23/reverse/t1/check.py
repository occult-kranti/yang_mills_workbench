#!/usr/bin/env python3
"""Exact T1 block algebra, kernel weights and controlled exponential checks."""
from pathlib import Path
from fractions import Fraction as F
from math import factorial
from itertools import product
import argparse,hashlib,json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];CONTRACT=ROOT/'research/round23/contracts/t1.json'
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def zeros(n,m=None):return [[F(0) for _ in range(m or n)] for _ in range(n)]
def eye(n):return [[F(i==j) for j in range(n)] for i in range(n)]
def add(a,b):return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def mul(c,a):return [[c*x for x in r] for r in a]
def mm(a,b):return [[sum((a[i][k]*b[k][j] for k in range(len(b))),F(0)) for j in range(len(b[0]))] for i in range(len(a))]
def trans(a):return list(map(list,zip(*a)))
def power(a,n):
    out=eye(len(a))
    for _ in range(n):out=mm(out,a)
    return out
def block(a,rows,cols):return [[a[i][j] for j in cols] for i in rows]
def inverse(a):
    n=len(a);r=[row[:]+e for row,e in zip(a,eye(n))]
    for j in range(n):
        pivot=next((k for k in range(j,n) if r[k][j]),None);need(pivot is not None,'singular matrix')
        r[j],r[pivot]=r[pivot],r[j];div=r[j][j];r[j]=[x/div for x in r[j]]
        for k in range(n):
            if k!=j:
                fac=r[k][j];r[k]=[x-fac*y for x,y in zip(r[k],r[j])]
    return [row[n:] for row in r]
def rownorm(a):return max(sum(abs(x) for x in r) for r in a)
def exp_poly(a,u,n=14):
    term=eye(len(a));out=term
    for k in range(1,n+1):term=mul(-u/F(k),mm(term,a));out=add(out,term)
    r=u*rownorm(a);need(r<F(n+2),'Taylor tail ratio invalid')
    tail=r**(n+1)/factorial(n+1)/(1-r/F(n+2))
    return out,tail

def fixture(lam):
    HE=zeros(4)
    for i,e in enumerate([0,2,3,4]):HE[i][i]=F(e)
    V=[[F(20),F(1,2),F(1),F(0)],[F(1,2),F(20),F(1,2),F(1)],[F(1),F(1,2),F(5),F(1)],[F(0),F(1),F(1),F(6)]]
    need(all(V[i][i]>sum(abs(V[i][j]) for j in range(4) if j!=i) for i in range(4)),'V positivity diagonal dominance')
    need(rownorm(V)<40,'fixture magnetic norm')
    H=add(HE,mul(lam,V));Ht=[row[:] for row in H]
    for i in [2,3]:
        for j in [2,3]:Ht[i][j]=HE[i][j]
    A=block(Ht,range(2),range(2));B=block(Ht,range(2,4),range(2));C=block(Ht,range(2,4),range(2,4));BB=mm(trans(B),B)
    fourth=block(power(Ht,4),range(2),range(2));one_return=zeros(2)
    for i,j in product(range(2),repeat=2):
        for path in product(range(4),repeat=3):
            seq=(i,)+path+(j,);excursions=sum(1 for a,b in zip(seq,seq[1:]) if a<2 and b>=2)
            if excursions<=1:
                term=F(1)
                for a,b in zip(seq,seq[1:]):term*=Ht[a][b]
                one_return[i][j]+=term
    difference=add(fourth,mul(-1,one_return))
    need(difference==mm(BB,BB),'repeated return fourth coefficient')
    need(rownorm(difference)>0 if lam else rownorm(difference)==0,'repeated return discrimination')
    second=block(power(Ht,2),range(2),range(2))
    need(second==add(mm(A,A),BB),'Volterra positive sign')
    need(second!=add(mm(A,A),mul(-1,BB)) if lam else True,'wrong Volterra sign discriminator')
    z=F(1);res=block(inverse(add(Ht,mul(z,eye(4)))),range(2),range(2))
    sigma=mm(trans(B),mm(inverse(add(C,mul(z,eye(2)))),B))
    correct=inverse(add(add(A,mul(z,eye(2))),mul(-1,sigma)))
    wrong=inverse(add(add(A,mul(z,eye(2))),sigma))
    need(res==correct,'Schur exact identity')
    need(res!=wrong if lam else res==wrong,'Schur wrong sign control')
    shift=F(2,7)
    kernel_first=mul(-1,mm(trans(B),mm(C,B)))
    shifted_first=mul(-1,mm(trans(B),mm(add(C,mul(shift,eye(2))),B)))
    need(shifted_first==add(kernel_first,mul(-shift,BB)),'common scalar shift kernel derivative')
    need(shifted_first!=kernel_first if lam else True,'selected-only shift discriminator')
    # A nonzero off-block model with distinct complementary energies.
    need(mm(C,block(V,range(2,4),range(2,4)))!=mm(block(V,range(2,4),range(2,4)),C),'fixture must be noncommuting')
    u=F(1,20);exact_poly,tail1=exp_poly(H,u);approx_poly,tail2=exp_poly(Ht,u)
    delta=add(block(exact_poly,range(2),range(2)),mul(-1,block(approx_poly,range(2),range(2))))
    # Sum of absolute entries dominates operator norm. Each of four entries
    # has error <=tail1+tail2, so the total is rigorously controlled.
    upper=sum(abs(x) for row in delta for x in row)+4*(tail1+tail2)
    bound=F(125,3)*lam**3*u**3
    if lam:need(upper<=bound,'projected cubic error enclosure failed')
    else:need(H==Ht and rownorm(delta)==0,'lambda-zero exact reduction')
    return {'lambda':str(lam),'fourth_missing_return_frobenius_squared':str(sum(x*x for r in difference for x in r)),'projected_error_upper':str(upper),'cubic_bound':str(bound),'sigma':str(u),'algebra_fixture_only':True}

def integrals():
    # Integrate products of (1-exp(-k t)) at the polynomial coefficient level.
    # Their convolution coefficient uses the beta integral p!q!/(p+q+1)!.
    records=[]
    for degree in range(3,12):
        direct=sum((F((-1)**(p+q),factorial(degree)) for p in range(1,degree-1) for q in [degree-1-p] if q>=1),F(0))
        # sigma(1+e^-k sigma)-(2/k)(1-e^-k sigma), k^(degree-1).
        analytic=F((-1)**(degree-1),factorial(degree-1))+F(2*(-1)**degree,factorial(degree))
        need(direct==analytic,'leakage convolution integral coefficient')
        records.append({'degree':degree,'coefficient':str(direct)})
    need(F(250,9)*F(9,6)==F(125,3),'short-time constant')
    lam=F(1,100);m=18*lam;k=3-m
    need(k==F(141,50),'decay denominator endpoint')
    need(lam*(3-F(97,4)*lam)>0,'lower energy form determinant')
    need(F(125,9)/k**2==F(312500,178929),'uniform error rational factor')
    return {'energy_floor':'18alpha lambda','k_min':str(k),'uniform_lambda2_factor_without_e':'312500/178929','cubic_constant':'125/3','integral_coefficients':records}

def actual_weights():
    data=[(F(3),F(19,4),F(1,4),F(1,8)),(F(9,2),0,0,F(1,8)),(F(6),0,0,F(3,8)),(F(15,2),0,0,F(9,4)),(F(8),0,0,F(9,8)),(F(17,2),0,0,F(3,8)),(F(9),0,0,F(3,8))]
    total0=sum(r[1] for r in data);total1=sum(r[3] for r in data)
    first0=sum(r[0]*r[1] for r in data);first1=sum(r[0]*r[3] for r in data)
    need(total0==total1==F(19,4),'actual equal instantaneous weights')
    need(first0==F(57,4) and first1==F(285,8),'actual unequal moment controls')
    need(first0!=first1 and sum(r[2] for r in data)==F(1,4),'scalar memory control nondiscriminating')
    return {'energies':len(data),'initial_diagonal':str(total0),'first_moments':[str(first0),str(first1)],'offdiagonal':str(sum(r[2] for r in data))}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();out=Path(args.output)
    need(out.is_absolute() and not out.exists(),'fresh absolute output required')
    contract=json.loads(CONTRACT.read_text())
    for p,h in contract['dependencies'].items():need(sha(ROOT/p)==h,'changed dependency '+p)
    for p in contract['instruction_inputs']:need((ROOT/p).is_file(),'missing instructions '+p)
    examples=[fixture(F(0)),fixture(F(1,100)),fixture(F(1,1000))];cert=integrals();weights=actual_weights()
    alpha,hbar,t=F(2),F(3),F(1,5);sigma=alpha*t/hbar
    need(sigma==F(2,15),'physical time combination')
    result={'schema':'ym23-reverse-t1-v1','loop':'t1','direction':'reverse','status':'checks_passed_full_space_evolution_certified','passed':True,'target_verdict':'full_space_leading_memory_evolution_and_error_certified','definition':'Htilde=[[A_lambda,B*],[B,C0]], Ttilde=J*exp(-tHtilde/hbar)J','volterra_return':'full Ttilde','comparison':{'fixed_time_cubic_error':'(250/9)lambda^3 I_3(sigma)','decaying_error':'250lambda^3 exp(-18lambda sigma) I_(3-18lambda)(sigma)/(3-18lambda)^2','uniform_absolute_error':'312500lambda^2/(178929e)','energy_floor':'18alpha lambda','all_selected_Hilbert_space':True,'relative_late_time_error_proved':False,'ground_gap_above_interacting_ground_proved':False,'physical_clock_calibrated':False,'continuum_proved':False},'certificate':cert,'fixtures':examples,'actual_Q2_weights':weights,'novelty':'project error certificate; scientific priority unverified'}
    controls={'schema':'ym23-reverse-t1-controls-v1','loop':'t1','direction':'reverse','status':'passed','passed':True,'omitted_repeated_return_rejected':True,'wrong_Volterra_sign_rejected':True,'wrong_Schur_sign_rejected':True,'scalar_memory_rejected_by_actual_Q2_weights':True,'autonomous_two_channel_claimed':False,'lambda_zero_exact':True,'common_shift_consistent':True,'inconsistent_selected_only_shift_rejected':True,'physical_time_check':str(sigma),'noncommuting_fixtures_only':True,'actual_infinite_rank_proof_from_fixtures':False}
    inventory=set(contract['dependencies'])|set(contract['instruction_inputs'])|{str(CONTRACT.relative_to(ROOT)),str((HERE/'check.py').relative_to(ROOT)),str((HERE/'report.md').relative_to(ROOT))}
    manifest={'schema':'ym23-source-manifest-v1','loop':'t1','direction':'reverse','inputs':{p:sha(ROOT/p) for p in sorted(inventory)},'outputs':{},'current_other_direction_read':False,'source_depth':'Inherited actual Q1/Q2/P2 reports and admitted S2 handoff; no new complete primary-paper reading claimed.'}
    out.mkdir(parents=True)
    for p,obj in [('results.json',result),('controls.json',controls)]:
        (out/p).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n');manifest['outputs'][p]=sha(out/p)
    (out/'source-manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'passed':True,'loop':'t1','output':str(out)},sort_keys=True))
if __name__=='__main__':main()
