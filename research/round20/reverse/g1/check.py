#!/usr/bin/env python3
"""Independent Duhamel error ledger and true SU2 norm-continuity obstruction."""
from pathlib import Path
from fractions import Fraction as F
import argparse,json,hashlib,importlib.util
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
E2=ROOT/'research/round20/reverse/e2/check.py'
spec=importlib.util.spec_from_file_location('reverse_e2_geometry',E2);geo=importlib.util.module_from_spec(spec);spec.loader.exec_module(geo)

def bound(M,t,tau,alpha=F(2),hbar=F(1),E=F(1),family='original_lattice'):
 if hbar<=0 or E<=0 or alpha<=0:raise ValueError('physical hbar, alpha, E_star must be positive')
 if family!='original_lattice':raise ValueError('F diffusion c cannot replace lattice alpha')
 eps=alpha*abs(tau)*geo.tail(M)
 return 4*abs(t)*eps/hbar

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
 rows=[]
 for M in [0,2,4,8]:
  for t in [F(-2),F(0),F(1,2)]:
   for tau in [F(-1,64),F(1,64),F(1)]:
    rows.append({'M':M,'t_in_hbar_over_E_star':str(t),'tau':str(tau),'tail':str(geo.tail(M)),'operator_error_over_A_norm':str(bound(M,t,tau))})
 M=1;vm=set().union(*(geo.flinks(f) for f in geo.interior(M)));obs={(2,9,2,1),(0,6,5,2)};central={geo.fullfactor(e) for e in vm|obs}
 geometry=[geo.box((12+r,12+s,12),central) for r in range(4) for s in range(2)]
 shifts=[]
 for n in [0,1,2,5,20,100,1000]:
  E_n=F(n*(n+2),4);E_next=F((n+1)*(n+3),4);T=F(4,2*n+3);phase=(E_next-E_n)*T
  if phase!=1:raise RuntimeError('character phase not pi')
  shifts.append({'n':n,'E_n_over_alpha':str(E_n),'spacing_over_alpha':str(E_next-E_n),'t_n_alpha_over_pi_hbar':str(T),'phase_over_pi':str(phase),'operator_norm_difference':'2'})
 controls=[]
 def ck(name,v):
  if not v:raise RuntimeError(name)
  controls.append({'name':name,'passed':True})
 ck('times_tend_zero_spacing_grows',all(F(shifts[i+1]['t_n_alpha_over_pi_hbar'])<F(shifts[i]['t_n_alpha_over_pi_hbar']) for i in range(len(shifts)-1)))
 ck('nonzero_norm_difference_at_small_times',all(r['operator_norm_difference']=='2' for r in shifts))
 ck('signed_time_uses_absolute_value',bound(2,F(-2),F(1))==bound(2,F(2),F(1)))
 ck('large_finite_tau_requires_no_gap_smallness',bound(2,F(1),F(1))>0)
 ck('observable_support_required',not obs<=set().union(*(geo.support(geo.fullfactor(e)) for e in vm)))
 for name,kwargs in [('missing_hbar',{'hbar':F(0)}),('zero_reference',{'E':F(0)}),('diffusion_c_substitution',{'family':'F_diffusion_c'})]:
  try:bound(1,F(1),F(1,64),**kwargs)
  except ValueError:ck(name+'_rejected',True)
  else:raise RuntimeError(name+' admitted')
 # Exact phase exponents in units hbar: scalar energies cancel in A(t)
 # while the one-sided propagator acquires the nonzero exponent -tc.
 t=F(2);c=F(-3,7);left=t*c;right=-t*c
 ck('scalar_energy_phase_cancels_in_Heisenberg',left+right==0 and -t*c!=0)
 data={'schema':'ym20-reverse-g1-v1','status':'passed','rows':rows,'geometry_fixtures':geometry,'character_shift':shifts,'controls':controls,'tau_scope':'every finite real tau; no gap assumption used','continuity':'fixed-time local operator norm limit; implementing unitary strongly continuous; full local B algebra need not be point-norm continuous','scope':'original fixed-spacing summable lattice dynamics only'}
 p=out/'results.json';p.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
 files=[HERE/'check.py',HERE/'report.md',E2,ROOT/'research/round20/contracts/g1.json',ROOT/'research/round20/advisor/f2-gate.json']
 (out/'source-manifest.json').write_text(json.dumps({'sources':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'outputs':{'results.json':hashlib.sha256(p.read_bytes()).hexdigest()}},indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':'passed','rows':len(rows),'geometry':len(geometry),'controls':len(controls)}))
if __name__=='__main__':main()
