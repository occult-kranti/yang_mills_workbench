#!/usr/bin/env python3
"""Independent invariant-vector-field and projected-gradient F2 reconstruction."""
from fractions import Fraction as F
from pathlib import Path
import argparse,json,hashlib,math
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent

def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
def qmul(a,b):
 a0,a1,a2,a3=a;b0,b1,b2,b3=b
 return (a0*b0-a1*b1-a2*b2-a3*b3,a0*b1+a1*b0+a2*b3-a3*b2,a0*b2-a1*b3+a2*b0+a3*b1,a0*b3+a1*b2-a2*b1+a3*b0)
def action(U,V,W):return 3*U[0]+V[0]+W[0]+dot(U,V)+dot(V,W)
def values(U,V,W):
 x,y,z=U[0],V[0],W[0];w,t,r=dot(U,V),dot(V,W),dot(U,W)
 gamma=(15+8*y+2*x+2*z+2*r-(3*x+w)**2-(y+w+t)**2-(z+t)**2)/4
 lap=-F(3,4)*(3*x+y+z+2*w+2*t)
 return x,y,z,w,t,r,gamma,lap

def directional(U,V,W):
 g=F(0);lap=F(0)
 for j in range(3):
  unit=tuple(F(int(k==j+1)) for k in range(4))
  for index,Q in enumerate([U,V,W]):
   d=tuple(v/2 for v in qmul(unit,Q));dd=tuple(-v/4 for v in Q)
   if index==0:first=3*d[0]+dot(d,V);second=3*dd[0]+dot(dd,V)
   elif index==1:first=d[0]+dot(U,d)+dot(d,W);second=dd[0]+dot(U,dd)+dot(dd,W)
   else:first=d[0]+dot(V,d);second=dd[0]+dot(V,dd)
   g+=first**2;lap+=second
 return g,lap

def exp_upper(x,degree=24):
 x=F(x)
 if x<0 or x>=degree+2:raise ValueError('invalid geometric tail ratio')
 return sum((x**j/math.factorial(j) for j in range(degree+1)),F(0))+x**(degree+1)/math.factorial(degree+1)/(1-x/F(degree+2))

def calibrate(slope,q,hbar,E,provenance='independent_dynamic_data'):
 if q<=0 or hbar<=0 or E<=0 or slope>=0:raise ValueError('positive form/units and negative physical dynamic slope required')
 if provenance!='independent_dynamic_data':raise ValueError('static notation is not dynamic calibration')
 return -hbar*slope/q

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
 I=(F(1),F(0),F(0),F(0));minus=tuple(-x for x in I);i=(F(0),F(1),F(0),F(0))
 P=(F(3,5),F(4,5),F(0),F(0));Q=(F(5,13),F(0),F(12,13),F(0));R=(F(8,17),F(0),F(0),F(15,17))
 fixtures=[(I,I,I),(minus,I,minus),(I,i,I),(P,Q,R),(R,P,Q),(Q,R,P)]
 rows=[]
 for idx,(U,V,W) in enumerate(fixtures):
  if any(dot(p,p)!=1 for p in [U,V,W]):raise RuntimeError('not unit quaternion')
  x,y,z,w,t,r,g,l=values(U,V,W);dg,dl=directional(U,V,W)
  if g!=dg or l!=dl or g<0:raise RuntimeError('derivative routes disagree')
  for k in [F(-1,8),F(0),F(1,8)]:
   potential=k*l/2+k*k*g/4;ground_laplacian_ratio=k*dl/2+k*k*dg/4
   rows.append({'fixture':idx,'kappa':str(k),'S':str(action(U,V,W)),'r':str(r),'GammaS':str(g),'DeltaS':str(l),'ground_residual_over_c_psi':str(potential-ground_laplacian_ratio),'drop_r_residual':str(-k*k*r/8),'independent_middle_cross_residual':str(-k*k*(r-w*t)/8),'flip_DeltaS_sign_residual':str(-k*l)})
 E=exp_upper(F(3,2));lower=F(3,4)/E
 if not E<F(9,2) or not lower>F(1,6):raise RuntimeError('conditional gap certificate fails')
 controls=[]
 def ck(name,v):
  if not v:raise RuntimeError(name)
  controls.append({'name':name,'passed':True})
 ck('sharp_action_extrema_attained',action(I,I,I)==7 and action(minus,I,minus)==-5)
 # Polynomial coefficients of (13+3y)^2/16-(10+6y)
 # and (3+y)^2/4-(2+2y) equal positive multiples of (1-y)^2.
 square1=[F(169,16)-10,F(78,16)-6,F(9,16)];square2=[F(9,4)-2,F(6,4)-2,F(1,4)]
 ck('global_range_sum_of_squares',square1==[F(9,16),F(-18,16),F(9,16)] and square2==[F(1,4),F(-1,2),F(1,4)])
 ck('drop_r_changes_ground_residual',any(F(r['drop_r_residual'])!=0 for r in rows))
 ck('independent_V_copies_change_residual',any(F(r['independent_middle_cross_residual'])!=0 for r in rows))
 ck('wrong_potential_sign_rejected',any(F(r['flip_DeltaS_sign_residual'])!=0 for r in rows))
 ck('missing_metric_factor_rejected',directional(I,i,I)[0]!=4*directional(I,i,I)[0])
 # An alleged E=4 is below the positive Taylor partial sum and is invalid.
 partial=sum((F(3,2)**n/math.factorial(n) for n in range(8)),F(0))
 ck('inward_exponential_envelope_rejected',F(4)<partial<E)
 synthetic=calibrate(F(-3,8),F(3,16),F(1),F(1));ck('synthetic_dynamic_coefficient_recovered',synthetic==2)
 for name,args in [('zero_form',(F(-1),F(0),F(1),F(1))),('zero_c',(F(0),F(1),F(1),F(1))),('zero_E',(F(-1),F(1),F(1),F(0))),('notation_matching',(F(-1),F(1),F(1),F(1),'from_alpha_or_kappa'))]:
  try:calibrate(*args)
  except ValueError:ck(name+'_rejected',True)
  else:raise RuntimeError(name+' admitted')
 data={'schema':'ym20-reverse-f2-v1','status':'passed','rows':rows,'controls':controls,'exact_range':['-5','7'],'oscillation':'12','exponential_upper_3over2':str(E),'gap_coefficient_lower':str(lower),'admitted_gap':'c/6 for |kappa|<=1/8 and c>0','synthetic_calibration':{'classification':'algebra test only, no measurement','recovered_c':'2'},'new_r':'derived observable Tr(UWdagger)/2 required by gradient closure, not a new action coefficient','scope':'chosen finite reversible diffusion family only; physical c unmatched'}
 p=out/'results.json';p.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
 files=[HERE/'check.py',HERE/'report.md',ROOT/'research/round20/contracts/f2.json',ROOT/'research/round20/advisor/f1-gate.json']
 (out/'source-manifest.json').write_text(json.dumps({'sources':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'outputs':{'results.json':hashlib.sha256(p.read_bytes()).hexdigest()}},indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':'passed','fixture_kappa_rows':len(rows),'controls':len(controls)}))
if __name__=='__main__':main()
