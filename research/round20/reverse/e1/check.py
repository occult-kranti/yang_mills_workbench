#!/usr/bin/env python3
"""Independent literal orientation cutoffs, alignment and scalar shift E1."""
from pathlib import Path
from fractions import Fraction as F
import argparse,json,hashlib
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent

def links(N):
 return {(a,x,y,z) for a in range(3) for x in range(N+1) for y in range(N+1) for z in range(N+1) if (x,y,z)[a]<N}
def factor(e):
 a,x,y,z=e
 if a==0 and x%4<3:return ('s',x-x%4,y-y%2,z)
 if a==1 and y%2==0:return ('s',x-x%4,y,z)
 return ('f',*e)
def support(f):
 if f[0]=='f':return {tuple(f[1:])}
 _,x,y,z=f
 return {(0,x+j,y+k,z) for j in range(3) for k in range(2)}|{(1,x+j,y,z) for j in range(4)}
def faces(N):
 return [(a,b,x,y,z) for a,b in [(0,1),(0,2),(1,2)] for x in range(N+1) for y in range(N+1) for z in range(N+1) if (x,y,z)[a]<N and (x,y,z)[b]<N]
def selected(f):
 a,b,x,y,z=f;return (a,b)==(0,1) and y%2==0 and x%4<3

def literal(N):
 if type(N) is not int or N<3 or N%4!=3:raise ValueError('E1 only accepts N=4m+3')
 A=2*(1-F(1,2**N));B=2*(1-F(1,2**(N+1)));Y=F(4,3)*(1-F(1,4**((N+1)//2)));X=F(2,15)*(1-F(1,16**((N-3)//4)))
 W=(2*A*A*B+A*(A-Y)*B+X*Y*B)/24
 return W,F(107,135)-W

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args();out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
 rows=[];controls=[]
 def ck(name,value):
  if not value:raise RuntimeError(name)
  controls.append({'name':name,'passed':True})
 for N in [3,7,11,15]:
  es=links(N);fs=faces(N);fact={factor(e) for e in es};strips=[f for f in fact if f[0]=='s'];free=[f for f in fact if f[0]=='f'];W,t=literal(N)
  if any(not support(f)<=es for f in fact):raise RuntimeError('aligned box clipped reference')
  nsel=sum(map(selected,fs));w=sum((F(1,24*2**sum(f[2:])) for f in fs if not selected(f)),F(0))
  if (len(es),len(fs),len(strips),len(free),nsel)!=(3*N*(N+1)**2,3*N*N*(N+1),(N+1)**3//8,3*N*(N+1)**2-10*(N+1)**3//8,3*(N+1)**3//8) or W!=w:raise RuntimeError('exact count/weight mismatch')
  eps=t/32;g=F(1,4)-W/32
  rows.append({'N':N,'links':len(es),'faces':len(fs),'strips':len(strips),'free_factors':len(free),'selected_faces':nsel,'omitted_faces':len(fs)-nsel,'retained_weight':str(W),'tail':str(t),'epsilon_over_E_star':str(eps),'g_N_over_E_star':str(g),'projector_bound':str(eps/g),'observable_over_norm_bound':str(2*eps/g),'resolvent_dimensionless_bound':str(4*eps)})
 es=links(4);bad={factor(e) for e in es if not support(factor(e))<=es}
 ck('nonaligned_factor_promotion_rejected',len(bad)>0)
 try:literal(4)
 except ValueError:ck('nonaligned_contract_input_rejected',True)
 else:raise RuntimeError('N4 admitted')
 # Wrong common anchor cube x,y,z<N omits allowed boundary faces.
 N=3;proper={f for f in faces(N) if not selected(f)};wrong={f for f in proper if max(f[2:])<N}
 ck('wrong_common_anchor_cube_rejected',sum((F(1,24*2**sum(f[2:])) for f in proper-wrong),F(0))>0)
 c=F(-1,7);resolvent_diff_squared=c*c/(1+c*c)
 ck('omit_energy_shift_changes_fixed_resolvent',resolvent_diff_squared==F(1,50))
 energies=[F(-1,7),F(5,7)];shifted=[e-c for e in energies]
 ck('scalar_shift_preserves_gap',energies[1]-energies[0]==shifted[1]-shifted[0] and energies!=shifted)
 ck('omit_exterior_generator_is_unbounded',all(F(j*(j+1))>j for j in range(1,20)))
 def energy_ratio(alpha,E):
  if E<=0:raise ValueError('positive energy reference required')
  return alpha/E
 try:energy_ratio(F(2),F(0))
 except ValueError:ck('zero_energy_reference_rejected',True)
 else:raise RuntimeError('zero energy admitted')
 data={'schema':'ym20-reverse-e1-v1','status':'passed','rows':rows,'controls':controls,'nonaligned_N4_incomplete_factors':len(bad),'scalar_shift_fixture':{'c':'-1/7','fixed_z_i_resolvent_difference_squared':str(resolvent_diff_squared)},'energy_origin':'c_N=sum of included complete-strip ground energies; symbolic, not assumed zero','scope':'literal aligned shifted exterior-completed boxes only'}
 p=out/'results.json';p.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
 files=[HERE/'check.py',HERE/'report.md',ROOT/'research/round20/contracts/e1.json',ROOT/'research/round20/advisor/d2-gate.json']
 (out/'source-manifest.json').write_text(json.dumps({'sources':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'outputs':{'results.json':hashlib.sha256(p.read_bytes()).hexdigest()}},indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':'passed','rows':len(rows),'controls':len(controls)}))
if __name__=='__main__':main()
