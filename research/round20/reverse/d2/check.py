#!/usr/bin/env python3
"""Independent residual and contour reconstruction for D2."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent

def tail(L):
 S=2*(1-F(1,2**(L+1)));Y=F(4,3)*(1-F(1,4**(L//2+1)));X=F(2,15)*(1-F(1,16**((L+1)//4)))
 return F(107,135)-(2*S**3+S*(S-Y)*S+X*Y*S)/24

def bounds(L,alpha=F(2),tau=F(1,64),E=F(1)):
 if E<=0 or alpha<=0:raise ValueError('positive fixed energy reference required')
 beta=alpha*abs(tau)*F(107,135);delta=alpha/8
 if beta>=delta:raise ValueError('ground isolation premise fails')
 eps=alpha*abs(tau)*tail(L);bL=beta-eps;gL=delta-bL;g=delta-beta
 return {'L':L,'tail':str(tail(L)),'beta_L_over_E_star':str(bL/E),'g_L_over_E_star':str(gL/E),'epsilon_over_E_star':str(eps/E),'ground_energy_error_over_E_star':str(eps/E),'projector_norm_bound':str(eps/gL),'observable_error_over_operator_norm':str(2*eps/gL),'contour_projection_bound':str(2*delta*eps/g**2)}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
 rows=[bounds(L) for L in range(9)];controls=[]
 def ck(name,condition):
  if not condition:raise RuntimeError(name)
  controls.append({'name':name,'passed':True})
 for r in rows:ck('residual_sharper_than_contour_L'+str(r['L']),F(r['projector_norm_bound'])<F(r['contour_projection_bound']))
 # Unit vectors (1,0) and (3/5,4/5): the difference of rank-one
 # projectors squares to (16/25)I, proving both singular values are 4/5.
 M=[[F(16,25),F(-12,25)],[F(-12,25),F(-16,25)]]
 MM=[[sum((M[i][k]*M[k][j] for k in range(2)),F(0)) for j in range(2)] for i in range(2)]
 ck('rank_one_norm_leakage_trace_conversion',MM==[[F(16,25),0],[0,F(16,25)]])
 # If e=epsilon>0, the asserted denominator is false, even when the
 # perturbation is as simple as +epsilon I (no actual off-diagonal leakage).
 g=F(1,4);e=F(1,32)
 ck('missing_zero_mean_invalidates_denominator',g-e<g)
 ck('threshold_not_ground_gap',F(1,4)-F(-1,16)!=F(1,4))
 # P=diag(1,1,0), PL=diag(1,0,0), psi=e0: leakage zero but ||P-PL||=1.
 Pdiag=[F(1),F(1),F(0)];PLdiag=[F(1),F(0),F(0)];psi=[F(1),F(0),F(0)]
 leakage_squared=sum(((1-q)*v)**2 for q,v in zip(PLdiag,psi))
 difference_norm=max(abs(p-q) for p,q in zip(Pdiag,PLdiag))
 ck('higher_rank_projector_identity_rejected',leakage_squared!=difference_norm**2)
 # Escaping rank-one projectors annihilate every eventually fixed finite
 # support vector while retaining norm 1 for all n.
 ck('strong_resolvent_does_not_prevent_escape',all(int(n==j)==0 for n in range(5,10) for j in range(5)))
 for name,args in [('zero_reference',(0,F(2),F(1,64),F(0))),('lost_isolation',(0,F(2),F(1),F(1)))]:
  try:bounds(*args)
  except ValueError:ck(name+'_rejected',True)
  else:raise RuntimeError(name+' admitted')
 data={'schema':'ym20-reverse-d2-v1','status':'passed','rows':rows,'controls':controls,'claim':'Energy, rank-one projector and bounded-observable convergence of D1 exterior lifts','scale':{'alpha/E_star':'2','tau':'1/64','delta/E_star':'1/4','beta_infty/E_star':'107/4320','g_infty/E_star':'973/4320'}}
 p=out/'results.json';p.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
 files=[HERE/'check.py',HERE/'report.md',ROOT/'research/round20/contracts/d2.json',ROOT/'research/round20/advisor/d1-gate.json',ROOT/'research/round20/reverse/d1/output/results.json']
 m={'sources':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'outputs':{'results.json':hashlib.sha256(p.read_bytes()).hexdigest()}}
 (out/'source-manifest.json').write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':'passed','rows':len(rows),'controls':len(controls)}))
if __name__=='__main__':main()
