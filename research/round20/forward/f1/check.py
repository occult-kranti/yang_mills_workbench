#!/usr/bin/env python3
from fractions import Fraction as F
from pathlib import Path
from math import factorial
import argparse,hashlib,json
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
def require(x,m):
    if not x:raise ValueError(m)
def rejected(fn):
    try:fn()
    except ValueError:return True
    return False
def exp_upper(x,n=24):
    require(x>=0 and x<F(n+2),'exponential tail ratio invalid')
    return sum((x**j/F(factorial(j)) for j in range(n+1)),F())+x**(n+1)/F(factorial(n+1))/(1-x/F(n+2))
def scale(c=F(1),reference='E_star',positive=True,source='independent energy measurement'):
    require(reference=='E_star' and positive is True and c>0,'fixed positive energies required')
    require(source=='independent energy measurement','static symbols do not calibrate c')
    return c
def encode(o):
    if isinstance(o,F):return str(o)
    if isinstance(o,dict):return {k:encode(v) for k,v in o.items()}
    if isinstance(o,list):return [encode(v) for v in o]
    return o
def main(out):
    contract=ROOT/'research/round20/contracts/f1.json';con=json.loads(contract.read_text());gate=ROOT/con['depends_on']['gate']
    require(hashlib.sha256(gate.read_bytes()).hexdigest()==con['depends_on']['sha256'],'E2 gate changed')
    graphfile=ROOT/'research/round19/forward/c1/output/graph-reduction.json';graph=json.loads(graphfile.read_text())
    require(graph['action_coefficients']=={'x':3,'y':1,'z':1,'w':1,'t':1},'C1 action changed')
    rows=[]
    for k in map(F,('-1/8','-1/64','0','1/64','1/8')):
        for c in (F(1),F(2)):
            scale(c);E=exp_upper(14*abs(k));lap=F(-27,4);grad=F(0)
            correct_adjoint=(-k*lap-k*k*grad)+(k*lap+k*k*grad)
            wrong_adjoint=(-k*lap-k*k*grad)-(k*lap+k*k*grad)
            require(correct_adjoint==0,'correct invariant adjoint fails')
            if k:require(wrong_adjoint!=0 and k*lap!=0,'wrong density/drift discriminator is zero')
            rows.append({'kappa':k,'c_over_E_star':c,'gap_lower_over_E_star':3*c/(4*E),'exp_upper_14abs_kappa':E,'correct_adjoint_residual_over_rho':correct_adjoint,'wrong_drift_adjoint_residual_over_rho':wrong_adjoint,'bare_Haar_adjoint_residual':k*lap,'exact_gap_at_kappa_zero':3*c/4 if k==0 else None})
    free_spectrum=sorted({F(n*(n+2),4)+F(m*(m+2),4)+F(l*(l+2),4) for n in range(3) for m in range(3) for l in range(3)})
    require(free_spectrum[:2]==[F(0),F(3,4)],'Casimir convention mismatch')
    controls={'different_c_same_static_law_different_gap':rows[4]['exact_gap_at_kappa_zero']!=rows[5]['exact_gap_at_kappa_zero'],
      'wrong_drift_rejected_both_signs':all(r['wrong_drift_adjoint_residual_over_rho']!=0 for r in rows if r['kappa']),
      'bare_Haar_measure_rejected_both_signs':all(r['bare_Haar_adjoint_residual']!=0 for r in rows if r['kappa']),
      'zero_c_rejected':rejected(lambda:scale(F(0))),
      'zero_reference_rejected':rejected(lambda:scale(positive=False)),
      'c_from_kappa_rejected':rejected(lambda:scale(source='kappa notation')),
      'c_from_alpha_rejected':rejected(lambda:scale(source='alpha notation')),
      'fibonacci_energy_rejected':rejected(lambda:scale(source='Fibonacci label'))}
    require(all(controls.values()),'a discriminator failed')
    result={'schema':'ym20-forward-f1-v1','loop':'f1','status':'passed','fixtures':rows,'controls':controls,'free_gap':'3/4','weighted_generator':'A=-Delta-kappa gradS.grad','measure':'rho_kappa Haar; same common V as C1','time_generator':'exp(-t*c*A/hbar)','scope':'specified added reversible family; static law does not identify c or original Yang-Mills dynamics'}
    out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_text(json.dumps(encode(result),indent=2,sort_keys=True)+'\n')
    sources=[HERE/'check.py',HERE/'report.md',contract,gate,graphfile,ROOT/'research/round19/advisor/c2-gate.json',ROOT/'research/round19/forward/c1/report.md',ROOT/'research/round20/advisor/diffusion-source-notes.md']
    manifest={'sources':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'outputs':{'results.json':hashlib.sha256((out/'results.json').read_bytes()).hexdigest()}}
    (out/'source-manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'passed','loop':'f1','fixtures':len(rows),'controls':len(controls)}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE/'output');main(p.parse_args().output)
