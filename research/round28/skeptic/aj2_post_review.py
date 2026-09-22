#!/usr/bin/env python3
"""Focused AJ2 post-exchange audit; no producer algorithm is imported."""
import argparse,hashlib,itertools,json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];P='research/round28/';S=P+'skeptic/'
INV=S+'aj2-post-review-inputs/source-inventory.json';ISH='40cb2b2fbecdabfe206d596612d1d5ec204b18b6cce84c0b005eca8e38f8be11'
C=Counter()
def need(v,s):
 C[s]+=1
 if not v:raise RuntimeError(s)
def H(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def J(p):return json.loads((ROOT/p).read_text())
def q(x):
 if isinstance(x,dict):
  need(set(x)=={'numerator','denominator'} and type(x['numerator']) is int and type(x['denominator']) is int and x['denominator']>0,'exact rational object type')
  return Q(x['numerator'],x['denominator'])
 need(type(x) in (str,int),'exact rational scalar type');return Q(x)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def native(x):return json.loads(json.dumps(x))
Z=(0,0,0);E=((1,0,0),(0,1,0),(0,0,1))
def owner(t):return (t[0]//4,t[1]//2,t[2])
def mul(a,b):
 w,x,y,z=a;u,v,s,t=b
 return (w*u-x*v-y*s-z*t,w*v+x*u+y*t-z*s,w*s-x*t+y*u+z*v,w*t+x*s-y*v+z*u)
def inv(a):return (a[0],-a[1],-a[2],-a[3])
ONE=(Q(1),Q(0),Q(0),Q(0));WORD=[((Z,0),1),((E[0],2),1),((E[2],0),-1),((Z,2),-1)]
def hol(values):
 out=ONE
 for edge,s in WORD:out=mul(out,values[edge] if s==1 else inv(values[edge]))
 return out

def source_audit():
 need(H(INV)==ISH,'frozen postreview inventory');d=J(INV);bindings={INV:ISH}
 for r in d['entries']:
  need(H(r['source'])==r['sha256']==H(r['snapshot']),'all postreview source and snapshot bytes')
  bindings[r['source']]=r['sha256'];bindings[r['snapshot']]=r['sha256']
 contract=J(P+'contracts/aj2.json');need(len(contract['sources'])==47,'all47 contract sources declared')
 results={};closure_counts={}
 receipt=J(S+'aj2-producer-replays.json')
 for side,key in [('forward','sha256'),('reverse','files')]:
  prefix=P+side+'/aj2/';fr=J(prefix+'freeze.json');mapping=fr[key] if side=='forward' else {prefix+k:v for k,v in fr[key].items()}
  actual={str(p.relative_to(ROOT)) for p in (ROOT/prefix).rglob('*') if p.is_file() and p!=ROOT/(prefix+'freeze.json')}
  need(set(mapping)==actual,'complete owned producer closure '+side)
  for p,h in mapping.items():need(H(p)==h,'frozen producer source '+side)
  r=J(prefix+'output/results.json');results[side]=r;closure_counts[side]=len(mapping)
  for p,h in r['bindings'].items():need(not Path(p).is_absolute() and H(p)==h,'portable flat runtime/provenance source '+side)
  for p,h in contract['sources'].items():
   snap=prefix+'inputs/'+('repo/' if side=='forward' else '')+p
   need(r['bindings'].get(p)==h==r['bindings'].get(snap)==H(snap),'exact contract snapshot closure '+side)
  need(H(prefix+'freeze.json')==receipt['side'][side]['freeze_sha256'],'fresh replay matches current freeze '+side)
  need({p.name for p in (ROOT/(prefix+'output')).iterdir()}=={'results.json'},'complete single producer output '+side)
  for mode in ['normal','optimized']:
   need((HERE/'aj2-producer-fresh-replays'/(side+'-'+mode)/'results.json').read_bytes()==(ROOT/(prefix+'output/results.json')).read_bytes(),'fresh normal optimized frozen byte equality '+side)
 for p,h in J(S+'aj2-independent-freeze.json')['bindings'].items():need(H(p)==h,'independent preexchange freeze unchanged')
 old=J(S+'aj2-development/first-pass/results.json');current=J(S+'aj2-independent.json')
 need(old['check_count']==236 and current['check_count']==249,'successful independent development preserved')
 for key in ['geometry','reference_and_state_controls','spectral_controls','analytic_result','limitations']:need(old[key]==current[key],'unchanged science after complex-matrix controls '+key)
 return results['forward'],results['reverse'],current,bindings,closure_counts

def geometry(f,r,i):
 links=sorted(((x,y,z),a) for x,y,z,a in itertools.product(range(4),range(2),range(2),range(3)))
 endpoints=sorted({v for t,a in links for v in (t,add(t,E[a]))})
 records=[{'tail':t,'axis':a,'head':add(t,E[a]),'owner':owner(t)} for t,a in links]
 need(f['geometry']['owned_links']==r['geometry']['links']==native(records),'all48 original link labels owners and heads agree')
 need(i['geometry']['links']==native(links),'independent complete link labels agree')
 need(f['geometry']['complete_endpoint_vertices']==r['geometry']['endpoints']==i['geometry']['endpoint_vertices']==native(endpoints),'all36 endpoint groups agree')
 need(len(links)==48 and len(endpoints)==36,'complete physical counts')
 for row,(edge,s) in zip(f['geometry']['ordered_word'],WORD):need(row==native({'tail':edge[0],'axis':edge[1],'orientation':s,'owner':owner(edge[0])}),'forward full original oriented word')
 for row,(edge,s) in zip(r['geometry']['face'],WORD):need(row==native({'tail':edge[0],'axis':edge[1],'sign':s,'owner':owner(edge[0])}),'reverse full original oriented word')
 need(f['geometry']['minimal_complete_coarse_region']==r['geometry']['region']==i['geometry']['owners']==[[0,0,0],[0,0,1]],'minimal complete two-factor region')
 need(len(f['geometry']['additional_complete_factor_endpoints'])==32 and r['geometry']['outside_heads']==20,'loop endpoints versus tail endpoints distinguished')
 g=f['quaternion_and_haar_diagnostics'];a={(tuple(x['tail']),x['axis']):tuple(q(v) for v in x['quaternion']) for x in g['exact_rational_assignments']}
 need(hol(a)[0]==Q(12,17)==q(g['missing_head_attempts'][0]['original']),'forward full rational word recalculated')
 need(len(g['missing_head_attempts'])==1 and g['blind_attempt_count']==0 and g['missing_head_attempts'][0]['discriminates'] is True,'forward first control genuinely discriminates')
 need(q(g['missing_head_attempts'][0]['complete'])==Q(12,17)!=q(g['missing_head_attempts'][0]['missing_heads'])==Q(10272,18785),'forward wrong head value retained')
 coeff=[]
 for k in range(4):
  v=dict(a);v[(Z,2)]=tuple(Q(int(j==k)) for j in range(4));coeff.append(hol(v)[0])
 need(tuple(map(q,g['conditional_coefficients']))==tuple(coeff) and sum(x*x for x in coeff)==1,'actual conditional link coefficients independently recalculated')
 gr=r['geometry']['quaternion_fixture'];v={(tuple(x['tail']),x['axis']):tuple(map(q,x['q'])) for x in gr['link_assignments']};gauges={tuple(x['vertex']):tuple(map(q,x['q'])) for x in gr['endpoint_assignments']}
 need(len(v)==48 and len(gauges)==36,'reverse actual full assignments')
 changed={edge:mul(mul(gauges[edge[0]],x),inv(gauges[add(edge[0],E[edge[1]])])) for edge,x in v.items()}
 need(hol(v)==tuple(map(q,gr['holonomy'])) and hol(changed)==tuple(map(q,gr['transformed'])),'reverse noncommuting full word and gauge transform recalculated')
 wrong=dict(changed);wrong[(Z,0)]=mul(gauges[Z],v[(Z,0)])
 need(hol(wrong)[0]==q(gr['missing_head_wilson'])==Q(38412,359125)!=hol(v)[0],'reverse missing head genuinely discriminates')
 need(hol(v)[0]==q(gr['wilson'])==Q(-648,5525),'reverse distinct valid Wilson fixture')
 need(q(gr['charged_trace'])==Q(3,13)!=q(gr['charged_transformed_trace'])==Q(2988,5525),'reverse charged open word discriminates')
 need(r['geometry']['development_fixture_history']['replacement_used'] is False,'reverse no concealed replacement')
 return {'links':48,'endpoints':36,'tail_vertices':16,'outside_heads':20,'spectator_links_outside_face':44}

def controls(f,r,i):
 fs=f['controls'];rs=r['state_and_reference_controls'];sp=r['spectral_and_domain_controls']
 need(q(rs['haar_second_moment'])==Q(1,4) and q(rs['haar_fourth_moment'])==Q(1,8),'reference Haar moments')
 need(q(rs['normal_nonfaithful_2W_variance'])==Q(1,2)!=q(rs['normal_nonfaithful_haar_variance']),'reverse2W normal-state variance contrast')
 need(q(fs['haar_variance_substitution']['normal_band_ceiling'])==Q(1,16)<q(fs['haar_variance_substitution']['reference']),'forward concentration variance contrast')
 tilted=i['reference_and_state_controls']['tilted_normal_states']
 need(q(tilted[-1]['variance'])==Q(3,16)!=Q(1,4),'independent tilted1+kW normal-state contrast')
 for row in fs['normal_concentration_bands']:need(q(row['normal_band_state_variance_upper'])==q(row['epsilon'])**2,'forward normal concentration upper radius')
 for row in rs['epsilon_diagnostic_ceilings']:need(q(row['variance_ceiling'])==q(row['epsilon'])**2,'reverse normal concentration upper radius')
 need(q(fs['constant_multiplier']['variance'])==q(rs['constant_multiplier_variance'])==0,'constant rejection')
 need(q(fs['nonconstant_step_multiplier']['variance'])==q(rs['step_multiplier_band_state_variance'])==0,'nonconstant step with normal zero variance')
 need(rs['faithfulness_required'] is False and fs['normal_nonfaithful_state']['faithful_on_full_local_B_H'] is False,'normality faithfulness distinction')
 for row in fs['spectral_point_measure_controls']:
  k=row['energy_in_units_Delta'];need(q(row['heat_at_s_log2'])==Q(1,2**k)<q(row['gap_upper_at_s_log2'])==Q(1,2),'upper versus lower decay exact point measure')
 need(q(sp['energy_2g_correlation'])==Q(1,16)<q(sp['gap_rate_upper'])==Q(1,8),'reverse distinct point measure mass')
 need(q(fs['centering']['centered_heat'])==Q(1,16) and q(fs['centering']['uncentered_heat'])==Q(5,16),'forward centering fixture')
 need(q(sp['centered_correlation'])==Q(1,8) and q(sp['uncentered_correlation'])==Q(3,8),'reverse distinct centering time energy fixture')
 for row in fs['unproved_domain_membership']['prefixes']:
  n=row['N'];need(q(row['squared_vector_norm'])==sum((Q(1,k*k) for k in range(1,n+1)),Q(0))<2,'forward bounded vector partial norm')
  need(q(row['normalized_form_prefix'])==sum((Q(1,k) for k in range(1,n+1)),Q(0)) and q(row['normalized_operator_norm_squared_prefix'])==n,'forward distinct harmonic domain obstruction')
 for row in sp['domain_countermodel_partials']:
  n=row['terms'];need(q(row['norm_squared'])==(1-Q(1,4**n))/3 and q(row['first_energy_moment_in_g'])==n,'reverse geometric domain obstruction')
 need(q(fs['real_time_no_gap_decay']['modulus_squared'])==1 and sum(q(x)**2 for x in sp['real_time_amplitude_at_phase_pi_over_2'])==q(sp['diagnostic_variance'])**2,'real-time atom has constant modulus')
 need(fs['vacuum_only_gap']['positive_excited_measure'] is False and q(sp['vacuum_only_positive_measure_mass'])==0,'gap alone lacks nonzero measure')
 need(q(f['exact_scales']['delta_over_alpha'])==Q(1,8) and q(f['exact_scales']['inherited_gap_over_alpha'])==Q(1,16),'actual physical normalization retained')
 for key in ['normality_implies_faithfulness','interacting_variance_equals_Haar','uniform_positive_variance_margin','numerical_nonzero_tau','threshold_eigenvalue_identified','lower_decay_bound_claimed','real_time_decay_claimed','actual_vector_form_or_operator_domain_claimed','new_energy_moment_goal','continuum_yang_mills','fifth_goal_executed']:need(f['scope'][key] is False,'forward exact scope limitation')
 for key in ['numerical_variance_margin','evaluated_stability_interval','threshold_eigenvalue','real_time_decay','energy_moment_or_t0_domain_result','boundary_identification','continuum_mass_gap_solution']:need(r['scope'][key] is False,'reverse exact scope limitation')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',default=str(HERE/'aj2-post-review.json'));args=ap.parse_args()
 f,r,i,bindings,closures=source_audit();geo=geometry(f,r,i);controls(f,r,i)
 out={'schema':'ym28-aj2-skeptic-postreview-v1','loop':'aj2','check_count':sum(C.values()),'check_groups':dict(sorted(C.items())),'blocking_issues':[],
 'supported':'For the fixed original xz Wilson observable in the actual I1/AJ1 homogeneous orthant state, every real local multiplication level projection vanishes; inherited local normality implies Var_omega(W)>0 throughout the inherited symbolic regime. Its nonzero centered physical vector has positive finite-time imaginary-time correlation 0<C(t)<=Var_omega(W) exp[-alpha t/(16 hbar)] for every finite t>=0, using the actual centered reducing energy generator.',
 'geometry':geo,'producer_closure_file_counts':closures,'producer_check_counts':{'forward':f['check_count'],'reverse':r['semantic_check_count']},'independent_check_count':249,'all_fresh_producer_normal_optimized_outputs_equal':True,
 'attributed_reference_state_controls':{'forward':'symmetric Haar band concentration, variance<=1/16 versus Haar1/4','reverse':'normal vector2W, variance1/2 versus Haar1/4','skeptic':'normal density1+kW, k=1 variance3/16 versus Haar1/4','actual_interacting_variance_evaluated':False},
 'proof_review':'Full reports/checkers/results read. Conditional actual-link Haar integration, all endpoint levels and full spectators, trace-class positivity without faithfulness, GNS null quotient and bounded spectral calculus are analytically valid. Different diagnostic states and energies are not forced to agree.',
 'limitations':i['limitations'],'new_research_loops':0,'goal5_selected_or_executed':False,'bindings':dict(sorted(bindings.items()))}
 Path(args.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print(json.dumps({'checks':out['check_count'],'blocking_issues':[]}))
if __name__=='__main__':main()
