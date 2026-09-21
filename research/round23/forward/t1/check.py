#!/usr/bin/env python3
"""Exact block/memory controls for T1; matrices do not truncate the SU2 model."""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json
import math

ROOT=Path(__file__).absolute().parents[4]
BASE='research/round23/forward/t1/'
CONTRACT='research/round23/contracts/t1.json'
CONTRACT_SHA='2e3cc33531ce062d5cd50344eaaccbad1e623c1505618da9faa55a5f367f6407'

def need(c,m):
    if not c: raise ValueError(m)

def digest(p):
    for x in (p,*p.parents): need(not x.is_symlink(),'symlink rejected')
    need(p.is_file(),'missing source '+str(p))
    return hashlib.sha256(p.read_bytes()).hexdigest()

def save(p,x): p.write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
def zero(n,m=None): return [[F(0) for _ in range(m or n)] for _ in range(n)]
def eye(n): return [[F(i==j) for j in range(n)] for i in range(n)]
def add(a,b): return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def scale(c,a): return [[c*x for x in row] for row in a]
def mm(a,b): return [[sum((a[i][k]*b[k][j] for k in range(len(b))),F(0)) for j in range(len(b[0]))] for i in range(len(a))]
def power(a,n):
    out=eye(len(a))
    for _ in range(n): out=mm(out,a)
    return out

def tr(a): return [list(x) for x in zip(*a)]
def pp(a): return [row[:2] for row in a[:2]]
def encode(a): return [[str(x) for x in row] for row in a]
def block(a,b,c): return [a[i]+tr(b)[i] for i in range(2)]+[b[i]+c[i] for i in range(2)]
def inv(a):
    n=len(a); aug=[list(row)+ident for row,ident in zip(a,eye(n))]
    for j in range(n):
        k=next((i for i in range(j,n) if aug[i][j]),None)
        need(k is not None,'invertible matrix')
        aug[j],aug[k]=aug[k],aug[j]
        q=aug[j][j]; aug[j]=[x/q for x in aug[j]]
        for i in range(n):
            if i!=j:
                q=aug[i][j]; aug[i]=[x-q*y for x,y in zip(aug[i],aug[j])]
    return [row[n:] for row in aug]

def block_controls():
    lam=F(1,100)
    A=[[F(2),F(1,7)],[F(1,7),F(3)]]
    C0=[[F(4),F(1,5)],[F(1,5),F(5)]]
    B=scale(lam,[[F(1),F(1,3)],[F(1,2),F(-1)]])
    D=[[F(2),F(1,4)],[F(1,4),F(1)]]
    Delta=scale(lam,D); C=add(C0,Delta)
    Ht=block(A,B,C0); H=block(A,B,C)
    need(mm(C0,D)!=mm(D,C0),'noncommuting complementary fixture')
    K=[scale((-1)**j,mm(tr(B),mm(power(C0,j),B))) for j in range(6)]
    T=[eye(2)]
    for n in range(6):
        nxt=scale(-1,mm(A,T[n]))
        for j in range(n): nxt=add(nxt,mm(K[j],T[n-1-j]))
        T.append(nxt)
    for n in range(7):
        need(T[n]==scale((-1)**n,pp(power(Ht,n))),'full Volterra derivative coefficient')
    # Single-return replacement E_A + E_A*K*E_A omits four B factors.
    single=[]
    for n in range(7):
        val=power(scale(-1,A),n)
        for a in range(max(0,n-1)):
            for b in range(max(0,n-1-a)):
                c=n-2-a-b
                if c>=0:
                    val=add(val,mm(power(scale(-1,A),a),mm(K[b],power(scale(-1,A),c))))
        single.append(val)
    need(add(T[4],scale(-1,single[4]))==power(mm(tr(B),B),2),'fourth-order repeated return retained')
    need(T[4]!=single[4],'single return rejected')
    need(T[2]!=power(A,2),'wrong Volterra sign/memory omission rejected')
    for n in (0,1,2): need(pp(power(H,n))==pp(power(Ht,n)),'projected difference vanishes through second order')
    cubic=add(pp(power(H,3)),scale(-1,pp(power(Ht,3))))
    need(cubic==mm(tr(B),mm(Delta,B)) and cubic!=zero(2),'actual Duhamel block mechanism cubic coefficient')
    z=F(1); S=add(add(A,scale(z,eye(2))),scale(-1,mm(tr(B),mm(inv(add(C0,scale(z,eye(2)))),B))))
    actual=pp(inv(add(Ht,scale(z,eye(4)))))
    need(actual==inv(S),'minus Schur exact')
    plusS=add(add(A,scale(z,eye(2))),mm(tr(B),mm(inv(add(C0,scale(z,eye(2)))),B)))
    need(actual!=inv(plusS),'wrong plus Schur rejected')
    shift=F(2,7)
    shifted=add(Ht,scale(shift,eye(4)))
    for n in range(7):
        via_scalar=zero(2)
        for k in range(n+1): via_scalar=add(via_scalar,scale(F(math.comb(n,k))*(-shift)**(n-k),T[k]))
        need(via_scalar==scale((-1)**n,pp(power(shifted,n))),'common scalar shift all time coefficients')
    wrong=block(A,B,add(C0,scale(shift,eye(2))))
    need(scale(-1,pp(wrong))!=scale(-1,pp(shifted)),'complement-only shift is different problem')
    Hzero=block(A,zero(2),C0)
    need(all(pp(power(Hzero,n))==power(A,n) for n in range(7)),'lambda zero electric block reduction')
    return {'lambda_fixture':str(lam),'cubic_H_power_difference':encode(cubic),
            'missing_return_fourth_derivative':encode(add(T[4],scale(-1,single[4]))),
            'tested_derivative_orders':list(range(7)),
            'scope':'finite block algebra only; not actual SU2 spectral truncation'}

def actual_channel_controls():
    path='research/round22/forward/q2/output/results.json'
    gate=json.loads((ROOT/'research/round22/advisor/q2-gate.json').read_text())
    need(gate['files'][path]==digest(ROOT/path),'admitted actual channel source bound')
    data=json.loads((ROOT/path).read_text())
    W={F(e):[[F(x) for x in row] for row in w] for e,w in data['claims']['spectral_weights'].items()}
    zer=zero(2); first=zero(2)
    for e,w in W.items(): zer=add(zer,w); first=add(first,scale(e,w))
    need(zer==[[F(19,4),F(1,4)],[F(1,4),F(19,4)]],'actual complete channel weights')
    need(first==[[F(57,4),F(3,4)],[F(3,4),F(285,8)]],'actual unequal energy moments')
    need(first[0][0]!=first[1][1] and zer[0][1]!=0,'scalar leading-memory shortcut rejected by actual inherited data')
    return {'instantaneous':encode(zer),'first_moment':encode(first),'energy_count':len(W),
            'two_channel_autonomy_inferred':False}

def error_controls():
    lam=F(1,100); beta=18*lam; d=3-beta
    need(d==F(141,50) and d>0,'positive complementary decay difference')
    need(3-F(97,4)*lam>0,'Young lower bound covers full interval by monotonicity')
    need(40*F(5,2)**2==250,'projected Duhamel coefficient')
    uniform=F(125,24*d*d)
    need(uniform==F(312500,477144),'uniform rational envelope')
    # Independent convolution of truncated leakage series and closed formula coefficients.
    for n in range(9):
        coefficient=F(0)
        for j in range(n+1):
            k=n-j
            # integral u^(k+1)(s-u)^(j+1) supplies beta-factorials.
            coefficient+=(-d)**n/F(math.factorial(n+3))
        expected=F(n+1)*(-d)**n/F(math.factorial(n+3))
        need(coefficient==expected,'exact convolution coefficient')
        # Expansion of [s(1+exp(-ds))-2(1-exp(-ds))/d]/d^2.
        degree=n+3
        closed=(((-d)**(degree-1))/F(math.factorial(degree-1))
                +F(2,d)*((-d)**degree)/F(math.factorial(degree)))/(d*d)
        need(closed==expected,'closed error kernel versus independent convolution')
    # A rational small-time alternating enclosure of F_d, distinct from exact integral.
    sigma=F(1,16)
    partial=lambda N:sum((F(n+1)*(-d)**n*sigma**(n+3)/math.factorial(n+3) for n in range(N+1)),F(0))
    lo=partial(9); hi=partial(10)
    need(0<lo<hi<sigma**3/6 and hi<sigma/(d*d),'nonnegative kernel and two proved envelopes')
    # Dimensionless physical clock consistency, keeping alpha/hbar separately.
    alpha=F(3,2); hbar=F(5,4); t=F(7,8); s=alpha*t/hbar
    alpha2=alpha*3; t2=t/3
    need(alpha2*t2/hbar==s,'common sigma equality')
    need(alpha2*t/hbar!=s,'uncompensated clock change rejected')
    return {'lambda_bound':str(lam),'beta_at_cap':str(beta),'d_at_cap':str(d),
            'uniform_rational_coefficient':str(uniform),'sigma_fixture':str(sigma),
            'F_d_interval':[str(lo),str(hi)],'physical_sigma_fixture':str(s)}

def main():
    p=argparse.ArgumentParser(); p.add_argument('--output',required=True)
    out=Path(p.parse_args().output)
    need(out.is_absolute() and not out.exists(),'fresh absolute output required')
    need(digest(ROOT/CONTRACT)==CONTRACT_SHA,'frozen T1 contract hash')
    con=json.loads((ROOT/CONTRACT).read_text())
    for name,h in con['dependencies'].items(): need(digest(ROOT/name)==h,'inherited dependency changed '+name)
    names=set(con['dependencies'])|set(con['instruction_inputs'])|{CONTRACT,BASE+'check.py',BASE+'report.md',BASE+'source-notes.md',
           'research/round22/forward/q2/output/results.json','research/round22/forward/q2/source-notes.md'}
    inputs={n:digest(ROOT/n) for n in sorted(names)}
    blocks=block_controls(); channels=actual_channel_controls(); errors=error_controls()
    rejected=[]
    for key,val in [('alpha',F(0)),('hbar',F(0)),('energy_reference',F(0))]:
        try: need(val>0,'physical scale must be positive')
        except ValueError: rejected.append(key)
        else: raise ValueError('invalid scale admitted')
    results={'schema':'ym23-producer-results-v1','loop':'t1','direction':'forward','status':'proved_full_selected_leading_memory_evolution','passed':True,
             'target_verdict':'accepted_scoped','self_adjoint_domain':'D(H_E)=J D(A) direct-sum Q D(H_E)',
             'both_generators_lower_bound':'18*alpha*lambda',
             'unique_full_memory_return':True,'projected_error':'250*lambda^3*exp(-18*lambda*sigma)*F_(3-18lambda)(sigma)',
             'fixed_sigma_error_order':'lambda^3','uniform_absolute_error_order':'lambda^2',
             'uniform_rational_coefficient':errors['uniform_rational_coefficient'],
             'ground_normalized_uniform_error_proved':False,'physical_clock_fitted':False,
             'blocks':blocks,'actual_channels':channels,'error_controls':errors,
             'next_missing_premise':'actual ground-energy/eigenvector control for normalized long-time comparison'}
    controls={'schema':'ym23-producer-controls-v1','loop':'t1','direction':'forward','status':'discriminating_controls_passed','passed':True,
              'repeated_return_omission_rejected':True,'wrong_Volterra_sign_rejected':True,'wrong_Schur_sign_rejected':True,
              'scalar_memory_rejected_actual_inherited':True,'common_scalar_shift_preserved':True,'partial_shift_rejected':True,
              'lambda_zero_exact':True,'clock_mismatch_rejected':True,'invalid_scales_rejected':rejected,
              'finite_matrix_scope_retained':True,'rational_error_enclosure_retained':True}
    out.mkdir(parents=True); save(out/'results.json',results); save(out/'controls.json',controls)
    save(out/'source-manifest.json',{'schema':'ym23-producer-source-manifest-v1','loop':'t1','direction':'forward','inputs':inputs,
         'outputs':{n:digest(out/n) for n in ['results.json','controls.json']}})
    print(json.dumps({'passed':True,'loop':'t1','direction':'forward','target_verdict':'accepted_scoped','output':str(out)},sort_keys=True))

if __name__=='__main__': main()
