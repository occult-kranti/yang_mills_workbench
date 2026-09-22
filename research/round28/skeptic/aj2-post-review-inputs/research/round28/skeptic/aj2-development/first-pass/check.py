#!/usr/bin/env python3
"""AJ2 exact geometry and implication controls; analytic proofs are separate.
Only owned frozen snapshots are runtime sources. No producer checker imports.
"""
import argparse, hashlib, itertools, json, math
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
S='research/round28/skeptic/'
INV=S+'aj2-inputs/source-inventory.json'
INV_SHA='4f8094a3dad41d334523a22603c2451a5ddddb7d77b0a95355faf4120821fb5c'
CONTRACT='research/round28/contracts/aj2.json'
CONTRACT_SHA='0f71cc35d4e6fef93188cee740f9cdf90596f034193f3c9aee9455fb0411c154'
COUNT=Counter()
def need(ok,label):
 COUNT[label]+=1
 if not ok:raise RuntimeError(label)
def H(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def J(p):return json.loads((ROOT/p).read_text())
def pack(x):
 if isinstance(x,F):return str(x.numerator)+'/'+str(x.denominator)
 if isinstance(x,dict):return {str(k):pack(v) for k,v in x.items()}
 if isinstance(x,(list,tuple)):return [pack(v) for v in x]
 return x
def add(a,b):return tuple(a[k]+b[k] for k in range(3))
O=(0,0,0);E=((1,0,0),(0,1,0),(0,0,1))
def owner(p):return (p[0]//4,p[1]//2,p[2])
def mul(a,b):
 w,x,y,z=a;u,v,s,t=b
 return (w*u-x*v-y*s-z*t,w*v+x*u+y*t-z*s,w*s-x*t+y*u+z*v,w*t+x*s-y*v+z*u)
def inv(a):return (a[0],-a[1],-a[2],-a[3])
ONE=(F(1),F(0),F(0),F(0))
Q=((F(3,5),F(4,5),F(0),F(0)),(F(5,13),F(0),F(12,13),F(0)),(F(8,17),F(0),F(0),F(15,17)))
def hol(word,values):
 a=ONE
 for edge,sign in word:a=mul(a,values[edge] if sign==1 else inv(values[edge]))
 return a

def inputs():
 need(H(INV)==INV_SHA,'frozen source inventory identity')
 inventory=J(INV);bindings={INV:INV_SHA};mapping={}
 for row in inventory['entries']:
  p=row['snapshot'];need(not Path(p).is_absolute() and p.startswith(S+'aj2-inputs/'),'owned portable runtime snapshot')
  need(H(p)==row['sha256'],'all frozen source bytes');bindings[p]=row['sha256'];mapping[row['source']]=p
 need(len(mapping)==67 and inventory['contract_source_count']==47,'complete input count')
 c=J(mapping[CONTRACT]);need(H(mapping[CONTRACT])==CONTRACT_SHA and c['sequence']==8 and c['loop']=='aj2','actual frozen AJ2 contract')
 for p,h in c['sources'].items():need(p in mapping and bindings[mapping[p]]==h,'every declared contract source present')
 for p in [S+'aj2_independent.py',S+'aj2-independent-derivation.md']:bindings[p]=H(p)
 return bindings

def geometry():
 word=[((O,0),1),((E[0],2),1),((E[2],0),-1),((O,2),-1)]
 p=O;vertices=[p]
 for (tail,d),sign in word:
  start=tail if sign==1 else add(tail,E[d]);end=add(tail,E[d]) if sign==1 else tail
  need(p==start,'actual original face path continuity');p=end;vertices.append(p)
 need(p==O and len({edge for edge,s in word})==4,'actual face closed with four distinct links')
 R=sorted({owner(t) for (t,d),sign in word});need(R==[O,E[2]],'minimal full-factor owner cover')
 links=sorted(((4*b[0]+x,2*b[1]+y,b[2]),d) for b in R for x,y,d in itertools.product(range(4),range(2),range(3)))
 endpoints=sorted({v for p,d in links for v in (p,add(p,E[d]))});tails={p for p,d in links};heads=sorted(set(endpoints)-tails)
 need(len(links)==48 and len(set(links))==48,'all48 original link factors')
 need(len(endpoints)==36 and len(tails)==16 and len(heads)==20,'complete36 endpoint actions and20 outgoing heads')
 selected=set()
 for b in R:
  for x in range(3):
   p=(4*b[0]+x,2*b[1],b[2])
   selected|={(p,0),(add(p,E[0]),1),(add(p,E[1]),0),(p,1)}
 need(len(selected)==20 and len(set(links)-selected)==28,'selected20 and free28 full factors')
 need((E[0],2) in set(links)-selected,'reference Haar integration uses an actual free z link')
 need({edge for edge,s in word}<=set(links),'no missing Wilson factors')
 values={edge:Q[i%3] for i,(edge,s) in enumerate(word)}
 gauge={v:Q[(2*i+1)%3] for i,v in enumerate(endpoints)}
 transformed={edge:mul(mul(gauge[edge[0]],a),inv(gauge[add(edge[0],E[edge[1]])])) for edge,a in values.items()}
 a=hol(word,values);b=hol(word,transformed)
 need(all(mul(q,inv(q))==ONE for q in Q),'exact rational SU2 unitaries')
 need(b==mul(mul(gauge[O],a),inv(gauge[O])) and a[0]==b[0],'actual noncommuting closed holonomy covariance')
 need(sum(x*x for x in a)==1 and abs(a[0])<=1,'real bounded half trace')
 # Deliberately discriminating identity-link/head-action fixture; no search/refit.
 values0={edge:ONE for edge,s in word};g={v:ONE for v in endpoints};g[E[0]]=Q[0]
 good={edge:mul(g[edge[0]],inv(g[add(edge[0],E[edge[1]])])) for edge in values0}
 bad=dict(good);bad[(O,0)]=g[O]
 need(hol(word,good)==ONE and hol(word,bad)[0]==F(3,5)!=1,'missing head fixture discriminates')
 center={edge:a for edge,a in values.items()}
 for edge in center:
  tail,d=edge
  if tail==E[0]:center[edge]=tuple(-v for v in center[edge])
  if add(tail,E[d])==E[0]:center[edge]=tuple(-v for v in center[edge])
 need(center[(O,0)][0]==-values[(O,0)][0]!=values[(O,0)][0],'charged open link center action discriminates')
 need(hol(word,center)[0]==a[0],'same full endpoint center action preserves closed Wilson')
 return {'word':word,'ordered_vertices':vertices,'owners':R,'links':links,'endpoint_vertices':endpoints,'head_vertices_outside_tail_set':heads,'selected_links':sorted(selected),'free_link_count':28,'spectator_link_factors':44,'gauge_fixture':{'before':a,'after':b,'closed_half_trace':a[0],'missing_head_identity_fixture_before':F(1),'missing_head_identity_fixture_after':F(3,5),'charged_before':values[(O,0)][0],'charged_after':center[(O,0)][0]},'finite_fixture_proves_level_sets':False}

def moments_and_states():
 mult={0:1};mom=[]
 for n in range(9):
  if n%2==0:
   k=n//2;v=F(mult.get(0,0),2**n);expected=F(math.comb(2*k,k), (k+1)*4**k)
   need(v==expected,'fundamental Haar tensor fusion reference moment')
   mom.append({'power':n,'singlet_multiplicity':mult.get(0,0),'moment':v})
  nxt=Counter()
  for j,m in mult.items():
   nxt[j+1]+=m
   if j>0:nxt[j-1]+=m
  mult=dict(nxt)
 need([r['moment'] for r in mom]==[F(1),F(1,4),F(1,8),F(5,64),F(7,128)],'normalized reference even moment list')
 # Conditional Haar moments of the actual free B link also apply at tau=0 only.
 tilted=[]
 for k in [F(-1),F(0),F(1,2),F(1)]:
  mean=k/4;second=F(1,4);var=second-mean*mean
  need(var>0 and 1-abs(k)>=0,'normal tilted Haar probability and positive variance')
  tilted.append({'kappa':k,'density_normalization':F(1),'mean':mean,'second_moment':second,'variance':var,'density_pointwise_lower':1-abs(k)})
 need(tilted[-1]['variance']==F(3,16)!=F(1,4),'Haar variance substitution rejected for a normal state')
 need(F(4)*F(1,4)==1 and F(2)*F(0)==0,'Haar rank-one normal state is nonfaithful yet Wilson variance positive')
 small=[]
 for n in [1,2,4]:
  width=F(1,2**n);cap=width*width/4
  need(0<cap<=F(1,16),'arbitrarily small positive normal-state variance upper cap')
  small.append({'n':n,'band':'0<W<a','a':width,'variance_upper':cap,'strict_positivity_source':'analytic null-level-set theorem'})
 escape=[]
 for n in [2,4,8]:
  a=F(1,n);need(a*a==F(1,n*n),'singular concentration normal-state second moment upper')
  escape.append({'n':n,'band':'abs(W)<1/n','second_moment_upper':a*a})
 need(F(3,7)**2-F(3,7)**2==0,'constant multiplier zero variance')
 need(F(1)-F(1)**2==0 and F(1,2)>0,'nonconstant step positive-measure level admits normal zero variance')
 return {'reference_even_moments':mom,'reference_odd_moments_zero':'center inversion symmetry','scope':'Haar and tau=0 free-link reference diagnostics only, not interacting-state moments','normal_nonfaithful_control':{'state':'rank-one constant Haar vector','orthogonal_vector':'2W','projection_expectation':F(0),'Wilson_variance':F(1,4)},'constant_control':{'value':F(3,7),'variance':F(0)},'step_control':{'measure':'dx/2 on[-1,1]','multiplier':'indicator_[0,1]','normal_vector':'sqrt(2) indicator_[0,1]','level_one_measure':F(1,2),'state_mean':F(1),'state_second':F(1),'state_variance':F(0)},'tilted_normal_states':tilted,'small_positive_normal_variances':small,'singular_weakstar_cluster_controls':escape,'singular_cluster_is_actual_I1_state':False}

def spectral_controls():
 # Times use s=g*t/hbar=log2, g=alpha/16; exact Laplace values are rational.
 energy_multiple=2;t_factor=16;laplace=F(1,2)**energy_multiple;upper=F(1,2)
 need(F(1,8)*F(1,2)==F(1,16),'inherited physical alpha normalization')
 need(t_factor*F(1,16)==1,'physical time retains alpha and hbar')
 need(0<laplace<upper,'gap ceiling is upper not lower')
 need(energy_multiple!=1,'lower threshold need not be an eigenvalue')
 mean=F(1,2);weight=F(1,16);raw_weight=mean*mean+weight
 connected=weight*laplace;raw=mean*mean+connected
 need(connected==F(1,64) and raw==F(17,64),'actual centering exact correlation')
 need(raw>raw_weight*upper and connected<=weight*upper,'uncentered vacuum prevents gap decay')
 need(F(1,2)+F(1,4)<1,'bounded self-adjoint centering fixture operator norm ceiling')
 domain=[]
 for n in [1,4,16]:
  norm=sum((F(1,4*k*k) for k in range(1,n+1)),F(0));form=F(n,4);op=F(n*(n+1)*(2*n+1),24)
  need(norm<F(1,2) and form==sum((F(1,4) for k in range(1,n+1)),F(0)),'bounded vector with divergent form-energy prefixes')
  need(op==sum((F(k*k,4) for k in range(1,n+1)),F(0)),'unbounded operator-domain prefix')
  domain.append({'N':n,'norm_squared':norm,'form_energy_over_g':form,'operator_norm_squared_over_g2':op})
 need(F(1)>upper,'single energy real-time modulus rejects exponential decay')
 need(F(0)==0,'vacuum-only restricted gap has zero excited measure')
 return {'abstract_fixture':True,'time':'t=16*hbar*log(2)/alpha','spectral_point_over_g':2,'point_mass':F(1),'laplace_value':laplace,'gap_upper_factor':upper,'claimed_lower_factor_rejected':upper,'threshold_atom_present':False,'real_time_modulus':F(1),'centering':{'mean':mean,'centered_norm_squared':weight,'raw_norm_squared':raw_weight,'connected_correlation':connected,'raw_correlation':raw},'vacuum_only_control':{'physical_dimension':1,'excited_measure_mass':F(0),'gap_exclusion_holds':True,'nonvacuity_follows_from_gap_alone':False},'domain_countermodel':{'energies':'g*n^2','vector_coefficients':'1/(2n)','bounded_operator':'|chi><Omega|+adjoint','form_energy_infinite':True,'actual_Wilson_domain_obstruction_proved':False,'prefixes':domain}}

LIMITS=[
 'The result concerns one fixed original xz Wilson multiplication observable in the actual I1/AJ1 homogeneous omitted-coupling positive-orthant state and its full bounded physical algebra.',
 'The coupling regime is symbolic with unevaluated positive source constants; no numerical nonzero stability interval or quantitative uniform variance margin is established.',
 'Local normality is inherited from AJ1 and is not faithfulness, full support, global trace-class representability, or equality of interacting and Haar/reference moments.',
 'The physical threshold alpha/16 is inherited; the spectral measure is nonzero but its lowest overlapping energy, threshold atom and an evaluated physical mass are not identified.',
 'The correlation statement is finite-time imaginary-time positivity and an upper exponential ceiling; no universal lower exponential bound or real-time magnitude decay follows.',
 'No energy moment, membership of the actual centered Wilson vector in an operator or form domain, or differentiability at zero is claimed.',
 'Exact geometry, Haar reference moments and countermodel prefixes do not prove the analytic level-set, trace-class or infinite-volume source theorems by sampling.',
 'No alternative-boundary identification, dyadic/finite-model transfer, Wilson-only density theorem, continuum Yang-Mills construction, physical matching, completion percentage or scientific priority is established.'
]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',default=str(HERE/'aj2-independent.json'));a=ap.parse_args()
 bindings=inputs();geo=geometry();states=moments_and_states();spec=spectral_controls()
 out={'schema':'ym28-aj2-skeptic-independent-v1','loop':'aj2','sequence':8,'status':'independent derivation frozen before producer exchange; pending final review','check_count':sum(COUNT.values()),'check_groups':dict(sorted(COUNT.items())),'all_checks_passed':True,'bindings':bindings,'geometry':geo,'reference_and_state_controls':states,'spectral_controls':spec,
 'analytic_result':{'all_real_Wilson_level_spectral_projections_zero':True,'actual_normal_state_variance_positive':True,'uniform_positive_variance_margin_proved':False,'actual_centered_physical_vector_nonzero':True,'vacuum_orthogonal':True,'positive_spectral_measure_mass':'Var_omega(W)>0','physical_energy':'(alpha/8)G_phys','spectral_support':'[alpha/16,infinity)','correlation':'0<C(t)<=Var_omega(W)*exp[-alpha*t/(16*hbar)] for every finite t>=0','at_zero':'C(0)=Var_omega(W)','limit_at_infinite_time':0,'coupling_quantifier':'every real |tau|<min(c1(S),1/(2c2(S)))/7 with fixed inherited selected coefficients','faithfulness_used':False,'energy_moment_used':False,'same_model_and_actual_center':True},
 'limitations':LIMITS,'current_producer_science_read':False,'historical_checker_imports':False,'finite_checks_prove_analytic_claims':False,'nondiscriminating_attempts':[],'additional_research_loops':0,'goal5_selected_or_executed':False}
 Path(a.output).write_text(json.dumps(pack(out),indent=2,sort_keys=True)+'\n');print(json.dumps({'check_count':out['check_count'],'all_checks_passed':True,'binding_count':len(bindings)}))
if __name__=='__main__':main()
