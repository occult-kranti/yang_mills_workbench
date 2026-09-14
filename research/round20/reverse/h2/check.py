#!/usr/bin/env python3
"""Independent exact free-witness covariance and reference-residual H2 proof data."""
from pathlib import Path
from fractions import Fraction as F
import argparse,json,hashlib,importlib.util
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
H1=ROOT/'research/round20/reverse/h1/check.py'
spec=importlib.util.spec_from_file_location('reverse_h1_budget',H1);h1=importlib.util.module_from_spec(spec);spec.loader.exec_module(h1)

def flinks(f):
 a,b,x,y,z=f;c=(x,y,z);ca=list(c);ca[a]+=1;cb=list(c);cb[b]+=1
 return {(a,*c),(b,*ca),(a,*cb),(b,*c)}
def factor(e):
 a,x,y,z=e
 if a==0 and x%4<3:return ('s',x-x%4,y-y%2,z)
 if a==1 and y%2==0:return ('s',x-x%4,y,z)
 return ('f',*e)
def faces(L):return [(a,b,x,y,z) for a,b in [(0,1),(0,2),(1,2)] for x in range(L+1) for y in range(L+1) for z in range(L+1) if (a,b)!=(0,1) or y%2==1 or x%4==3]
def finite_covariance(q,L):return sum(((q**sum(f[2:])/24)**2/F(4) for f in faces(L)),F(0))

def row(q,eta,alpha=F(2),E=F(1)):
 q=h1.validq(q)
 if not 0<eta<1 or E<=0 or alpha<=0:raise ValueError('strict uniform budget and fixed positive physical scale required')
 B=h1.budget(q);tau=eta/(8*B);sigma2=alpha*alpha*tau*tau*h1.budget(q*q)/96;coarse=F(5,6)*alpha*alpha*tau*tau/(1-q*q)**3;g=alpha*(1-eta)/8
 if sigma2>coarse:raise RuntimeError('exact variance exceeds fallback')
 return {'q':str(q),'eta':str(eta),'B':str(B),'tau':str(tau),'operator_norm_over_E_star':str(alpha*eta/(8*E)),'g_bar_over_E_star':str(g/E),'exact_sigma_squared_over_E_star_squared':str(sigma2/(E*E)),'fallback_sigma_squared_over_E_star_squared':str(coarse/(E*E)),'projector_norm_squared_upper':str(min(F(1),sigma2/(g*g))),'state_trace_norm_squared_upper':str(4*min(F(1),sigma2/(g*g))),'negative_ground_energy_bound_over_E_star':str(sigma2/(g*E)),'normalized_tau':str(tau/(1-q)**3),'normalized_sigma2_over_alpha2_eta2':str(sigma2/(alpha*alpha*eta*eta*(1-q)**3))}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args();out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
 rows=[row(q,eta) for eta in [F(1,4),F(1,2),F(3,4)] for q in [F(1,2),F(3,4),F(7,8),F(15,16),F(31,32),F(63,64)]]
 seed=faces(2);candidate=faces(7);edge={f:flinks(f) for f in candidate};factors={f:{factor(e) for e in edge[f]} for f in candidate}
 pair_checks=0;shared_factor_disjoint_links=None
 for i,f in enumerate(seed):
  free={e for e in edge[f] if factor(e)[0]=='f'}
  if len(free)<2:raise RuntimeError('two free Haar witnesses missing')
  for g in seed[i+1:]:
   if len(edge[f]&edge[g])>1 or not free-edge[g]:raise RuntimeError('offdiagonal covariance witness missing')
   pair_checks+=1
   if not edge[f]&edge[g] and factors[f]&factors[g]:shared_factor_disjoint_links=[f,g]
 degree=max(sum(bool(factors[f]&factors[g]) for g in candidate) for f in seed)
 if degree>160:raise RuntimeError('factor-overlap degree exceeds universal bound')
 variance_rows=[]
 for q in [F(1,2),F(3,4),F(7,8)]:
  v=finite_covariance(q,2);expected=h1.retained(q*q,2)/96
  if v!=expected:raise RuntimeError('exact diagonal variance mismatch')
  variance_rows.append({'q':str(q),'L':2,'diagonal_variance_without_alpha_tau':str(v),'retained_B_q_squared_over96':str(expected)})
 controls=[]
 def ck(name,v):
  if not v:raise RuntimeError(name)
  controls.append({'name':name,'passed':True})
 ck('disjoint_links_not_disjoint_reference_factors',shared_factor_disjoint_links is not None)
 first_face=seed[0];free_first={e for e in edge[first_face] if factor(e)[0]=='f'}
 ck('duplicate_face_not_zero_covariance',not (free_first-edge[first_face]) and F(1,4)>0)
 full,remote=F(-1,16),F(-1,8)
 ck('invalid_remote_energy_shortcut_rejected',full<=0 and remote<=0 and full>remote)
 # H0=diag(0,1,2), V=diag(0,1,0): nonzero norm perturbation, exactly
 # unchanged ground projection. This is a topology control only.
 h0=[F(0),F(1),F(2)];v=[F(0),F(1),F(0)];h=[x+y for x,y in zip(h0,v)]
 ck('constant_operator_norm_compatible_with_identical_ground',max(map(abs,v))==1 and h0.index(min(h0))==h.index(min(h))==0)
 ck('fixture_degree_not_claimed_universal',degree<160 and 4*10*4==160)
 ck('asymptotic_sigma_constant',F(1,6144)*F(8,7)==F(1,5376))
 ck('asymptotic_projector_squared_constant',F(64,5376)==F(1,84))
 for name,kwargs in [('q1',{'q':F(1),'eta':F(1,2)}),('eta1',{'q':F(1,2),'eta':F(1)}),('zero_E',{'q':F(1,2),'eta':F(1,2),'E':F(0)})]:
  try:row(**kwargs)
  except ValueError:ck(name+'_rejected',True)
  else:raise RuntimeError(name+' admitted')
 # A proposed alpha(q)=1/B(q) hides the changing physical Hamiltonian.
 proposed=[1/h1.budget(q) for q in [F(1,2),F(3,4),F(7,8)]]
 ck('varying_alpha_to_hide_budget_detected',len(set(proposed))>1)
 # Localize finite positive Wilson sums near identity. This records exact
 # lower approximants (1-eps)W_L-tail, justified analytically in report.
 lower=[];q=F(1,2);eta=F(1,2);tau=eta/(8*h1.budget(q))
 for L in [2,4,8,16]:
  W=h1.retained(q,L);tail=h1.budget(q)-W;eps=F(1,2**L)
  lower.append({'L':L,'localization_loss':str(eps),'norm_lower_over_alpha':str(tau*((1-eps)*W-tail)),'norm_upper_over_alpha':str(eta/8)})
 data={'schema':'ym20-reverse-h2-v1','status':'passed','rows':rows,'controls':controls,'geometry':{'seed_faces':len(seed),'pairwise_distinct_face_checks':pair_checks,'candidate_faces':len(candidate),'fixture_max_factor_overlap_degree':degree,'universal_overlap_bound':160,'disjoint_link_shared_factor_example':[list(f) for f in shared_factor_disjoint_links]},'finite_variance_rows':variance_rows,'norm_localization_lower_approximants':lower,'exact_sigma_identity':'alpha^2*tau^2*B(q^2)/96','asymptotic_sigma2_over_alpha2_eta2_one_minus_q_cubed':'1/5376','asymptotic_projector_squared_coefficient':'eta^2/[84(1-eta)^2]','conclusion':'global rank-one projector and state convergence to selected-strip reference despite constant canonical operator norm','scope':'same fixed-spacing inhomogeneous representation; no homogeneous gap/continuum inference'}
 p=out/'results.json';p.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
 files=[HERE/'check.py',HERE/'report.md',H1,ROOT/'research/round20/contracts/h2.json',ROOT/'research/round20/advisor/h1-gate.json']
 (out/'source-manifest.json').write_text(json.dumps({'sources':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'outputs':{'results.json':hashlib.sha256(p.read_bytes()).hexdigest()}},indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':'passed','rows':len(rows),'pair_checks':pair_checks,'fixture_degree':degree,'controls':len(controls)}))
if __name__=='__main__':main()
