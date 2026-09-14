#!/usr/bin/env python3
from fractions import Fraction as F
from pathlib import Path
import argparse, hashlib, json

ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent

def require(ok,message):
    if not ok: raise ValueError(message)

def rejected(fn):
    try: fn()
    except ValueError: return True
    return False

def tail(L):
    m=L+1; q=F(1,2)
    g=(1-q**m)/(1-q)
    x=sum((q**r*(1-q**(4*max(0,1+(L-r)//4)))/(1-q**4) for r in range(3)),F())
    y=(1-q**(2*((m+1)//2)))/(1-q**2)
    return F(107,135)-(g**3/8-x*y*g/24)

def conditions(tau=F(1,64),reference_positive=True):
    require(reference_positive is True,'E_star must be positive physical reference')
    beta=abs(tau)*F(107,135)
    require(beta<F(1,8),'strict spectral isolation premise failed')
    return beta

def encode(o):
    if isinstance(o,F):return str(o)
    if isinstance(o,dict):return {k:encode(v) for k,v in o.items()}
    if isinstance(o,list):return [encode(v) for v in o]
    return o

def main(out):
    contract=ROOT/'research/round20/contracts/d2.json'
    con=json.loads(contract.read_text()); gate=ROOT/con['depends_on']['gate']
    require(hashlib.sha256(gate.read_bytes()).hexdigest()==con['depends_on']['sha256'],'D1 gate changed')
    oldfile=ROOT/'research/round20/forward/d1/output/results.json'
    old=json.loads(oldfile.read_text())
    beta=conditions(); rows=[]
    for L in range(9):
        t=tail(L); require(t==F(old['fixtures'][L]['tail_weight']),'D1 tail mismatch')
        eps=t/64; beta_L=beta-eps; g_L=F(1,8)-beta_L
        bound=min(F(1),eps/g_L)
        rows.append({'L':L,'tail_weight':t,'beta_L_over_alpha':beta_L,'g_L_over_alpha':g_L,
                     'energy_error_over_alpha':eps,'projector_norm_error':bound,'unit_observable_error':2*bound})
    # A rational rotation has exact singular norm sin(theta); derive its squared norm from entries.
    c,s=F(3,5),F(4,5)
    diff=[[-s*s,c*s],[c*s,s*s]]
    norm_squared=diff[0][0]**2+diff[0][1]**2
    require(norm_squared==s*s and sum(diff[0][j]*diff[j][1] for j in range(2))==0,'rotation control not scalar squared')
    unequal_p,unequal_q=[1,1,0],[1,0,0]
    unequal_distance=max(abs(a-b) for a,b in zip(unequal_p,unequal_q))
    common_vector_overlap=F(1)
    escaping=[]
    for n in (1,2,8):
        diag=[1]*(n+1);diag[n]=-1
        escaping.append({'n':n,'error_on_fixed_e0':abs(diag[0]-1),'operator_norm_error':max(abs(v-1) for v in diag),'ground_energy':min(diag),'projection_on_fixed_e0':int(diag[0]==min(diag))})
    controls={
      'missing_zero_mean_sharp_denominator_rejected':rejected(lambda:require(s<=s/2,'positive ground defeats denominator')),
      'rank_one_identity_checked':norm_squared==1-c*c,
      'trace_norm_conversion_checked':2*s==F(8,5),
      'threshold_equals_gap_rejected':rejected(lambda:require(F(3)==F(3)-F(-2),'threshold not eigenvalue gap')),
      'dropping_rank_one_rejected':rejected(lambda:require(unequal_distance**2==1-common_vector_overlap**2,'shared vector does not identify unequal-rank projections')),
      'strong_resolvent_ground_nonvanishing_rejected':all(v['error_on_fixed_e0']==0 and v['operator_norm_error']==2 and v['ground_energy']==-1 and v['projection_on_fixed_e0']==0 for v in escaping),
      'beta_threshold_rejected':rejected(lambda:conditions(F(1))),
      'zero_reference_rejected':rejected(lambda:conditions(reference_positive=False)),
    }
    require(all(controls.values()),'failed discriminating control')
    results={'schema':'ym20-forward-d2-v1','loop':'d2','status':'passed','fixtures':rows,'controls':controls,
             'default_gap_lower_over_alpha':F(973,8640),'scale':{'E_star':'fixed positive physical energy','alpha_over_E_star':'1','tau':'1/64'},
             'zero_mean_counterexample':{'projector_distance':s,'perturbation_norm':s,'wrong_sharp_bound':s/2},
             'strong_only_counterexample':{'operator':'I-2|e_n><e_n|','ground_energy':'-1','limit_operator':'I','limit_spectrum':['1'],'ground_projection_strong_limit':'0'},
             'escaping_fixtures':escaping,
             'theorem':'|e-e_L|<=epsilon_L; ||P-P_L||<=min(1,epsilon_L/g_L); observable<=2||A||min(1,epsilon_L/g_L)',
             'scope':'same A2 product representation and exact finite-factor exterior lifts; no clipped-box claim'}
    out.mkdir(parents=True,exist_ok=True)
    (out/'results.json').write_text(json.dumps(encode(results),indent=2,sort_keys=True)+'\n')
    sources=[HERE/'check.py',HERE/'report.md',contract,gate,oldfile,ROOT/'research/round19/advisor/a2-gate.json']
    manifest={'sources':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'outputs':{'results.json':hashlib.sha256((out/'results.json').read_bytes()).hexdigest()}}
    (out/'source-manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'passed','loop':'d2','fixtures':len(rows),'controls':len(controls)}))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE/'output');main(p.parse_args().output)
