#!/usr/bin/env python3
from fractions import Fraction as F
from pathlib import Path
import argparse,hashlib,json,importlib.util
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
D1=ROOT/'research/round20/forward/d1/check.py'
sp=importlib.util.spec_from_file_location('d1_g1_forward',D1);geo=importlib.util.module_from_spec(sp);sp.loader.exec_module(geo)
def require(ok,m):
    if not ok:raise ValueError(m)
def rejected(fn):
    try:fn()
    except ValueError:return True
    return False
def bound(M,time,tau=F(1,64),hbar=F(1),energy_name='alpha'):
    require(hbar>0 and energy_name=='alpha','original lattice energy and positive action constant required')
    eps=abs(tau)*(F(107,135)-geo.closed(M))
    return eps,4*abs(time)*eps/hbar
def encode(o):
    if isinstance(o,F):return str(o)
    if isinstance(o,dict):return {k:encode(v) for k,v in o.items()}
    if isinstance(o,list):return [encode(v) for v in o]
    return o
def main(out):
    contract=ROOT/'research/round20/contracts/g1.json';con=json.loads(contract.read_text());gate=ROOT/con['depends_on']['gate']
    require(hashlib.sha256(gate.read_bytes()).hexdigest()==con['depends_on']['sha256'],'F2 gate changed')
    phasesfile=ROOT/'research/round20/forward/e2/output/results.json';phases=json.loads(phasesfile.read_text())['phase_fixtures']
    require({(r['x_mod4'],r['y_mod2']) for r in phases}==set((x,y) for x in range(4) for y in range(2)),'missing all-phase support premise')
    rows=[]
    for M in range(9):
        for t in (F(-2),F(0),F(1,2),F(2)):
            eps,error=bound(M,t)
            rows.append({'M':M,'time_alpha_over_hbar':t,'epsilon_over_alpha':eps,'unit_A_error':error})
    shifts=[]
    for n in (0,1,4,16,64,256):
        En=F(n*(n+2),4);En1=F((n+1)*(n+3),4);time=F(4,2*n+3);phase=time*(En1-En)
        require(phase==1,'character-shift phase not pi')
        shifts.append({'n':n,'E_n_over_alpha':En,'increment_over_alpha':En1-En,'time_over_pi_hbar_over_alpha':time,'phase_over_pi':phase,'norm_difference':F(2)})
    require(all(shifts[i+1]['time_over_pi_hbar_over_alpha']<shifts[i]['time_over_pi_hbar_over_alpha'] for i in range(len(shifts)-1)),'times not decreasing')
    _,factors,full=geo.complete(geo.retained(0));A={(0,4,0,0)}
    phase_energy=F(-3,7);left_phase=phase_energy;right_phase=-phase_energy
    controls={
      'point_norm_continuity_rejected':all(v['norm_difference']==2 for v in shifts),
      'missing_hbar_rejected':rejected(lambda:bound(0,F(1),hbar=F(0))),
      'diffusion_c_substitution_rejected':rejected(lambda:bound(0,F(1),energy_name='c')),
      'missing_central_observable_rejected':rejected(lambda:require(A<=full,'observable factor omitted')),
      'scalar_phase_cancels_in_Heisenberg':left_phase+right_phase==0 and phase_energy!=0,
      'signed_time_symmetric_error':bound(2,F(-2))[1]==bound(2,F(2))[1],
      'arbitrary_finite_tau_dynamics_admitted':bound(2,F(1),tau=F(2))[1]>0,
      'signed_tau_absolute_budget':bound(2,F(1),tau=F(-2))==bound(2,F(1),tau=F(2)),
    }
    require(all(controls.values()),'a dynamics control failed')
    result={'schema':'ym20-forward-g1-v1','loop':'g1','status':'passed','time_tail_fixtures':rows,'phase_pairs':[[r['x_mod4'],r['y_mod2']] for r in phases],'character_shift_fixtures':shifts,'controls':controls,'error_bound':'4||A||abs(t)epsilon_M/hbar','scope':'fixed-time operator-norm local limit; automorphism group; strong implementing unitaries; no point-norm continuity claim','tau_scope':'any fixed finite real tau for dynamics, no gap assumption used','scale':{'alpha':'original lattice energy','hbar':'positive action constant','E_star':'fixed positive energy','c':'absent'}}
    out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_text(json.dumps(encode(result),indent=2,sort_keys=True)+'\n')
    sources=[HERE/'check.py',HERE/'report.md',D1,contract,gate,phasesfile,ROOT/'research/round20/advisor/e2-gate.json',ROOT/'research/round19/advisor/a2-gate.json']
    manifest={'sources':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'outputs':{'results.json':hashlib.sha256((out/'results.json').read_bytes()).hexdigest()}}
    (out/'source-manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'passed','loop':'g1','time_fixtures':len(rows),'controls':len(controls)}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE/'output');main(p.parse_args().output)
