#!/usr/bin/env python3
"""Actual same-state AQ grid provenance and two exact inverse-energy readouts."""
from pathlib import Path
from fractions import Fraction as Q
import argparse,csv,hashlib,json
from arithmetic import exp_negative,sqrt_interval,pi_interval,log_positive,down,up,textq,interval,require,DEN
import historical_evaluator as inherited

BASE=Path(__file__).resolve().parent
CONTRACT_SHA='7ce892e9fb5bf7a5da03777206129db31f9d757d0d4c227cc6077c51fbe55daf'
TAU=Q(1,10**14);L=Q(10**9);T=Q(128);H=Q(1,32);N=4096;EPS=Q(1,10**6)
HEADER=['index','s','datum','reference_lower','reference_upper','arithmetic_radius','analytic_error','certified_actual_error','trapezoid_weight','tau']

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def serial(value):
 if isinstance(value,Q):return textq(value)
 if isinstance(value,dict):return {k:serial(v) for k,v in value.items()}
 if isinstance(value,(tuple,list)):return [serial(v) for v in value]
 return value

def constants(tau=TAU,cutoff=L):
 _,sq=sqrt_interval(Q(49,3)*abs(tau));D=2*sq;k=Q(49,4)*abs(tau)
 pil,piu=pi_interval();_,loghi=log_positive(1+(cutoff/T)**2)
 costs={'state':D,'centering':D*D,'real_time_comparison':k*T*loghi/pil,'Poisson_tail':(Q(1,2)+D/2)*2*T/(pil*cutoff)}
 uniform=sum(costs.values(),Q(0));zero=D/2+D*D
 return {'D':D,'k':k,'pi_lower':pil,'pi_upper':piu,'costs':costs,'uniform_positive_time_error':uniform,'zero_time_error':zero}

def provenance():
 return {'contract_sha256':CONTRACT_SHA,'model':'AQ centered full-Z3 zero-selected patterned family',
 'tau':textq(TAU),'selected':['0','0','0'],'L':textq(L),'T':textq(T),'h':textq(H),'N':N,
 'clock':'s=alpha*t_E/hbar','state':'same chosen AQ subsequential state at tau=+1e-14 throughout every node',
 'input_kind':'exact rational reference proxies with proved actual-AQ absolute error; not observations or simulations'}

def generate_rows(const):
 qlo,qhi=exp_negative(3*H);plo=phi=Q(1);rows=[]
 for j in range(N+1):
  flo,fhi=plo/4,phi/4;datum=(flo+fhi)/2;arithmetic=(fhi-flo)/2
  analytic=const['zero_time_error'] if j==0 else const['uniform_positive_time_error']
  rows.append({'index':j,'s':j*H,'datum':datum,'reference_lower':flo,'reference_upper':fhi,
  'arithmetic_radius':arithmetic,'analytic_error':analytic,'certified_actual_error':analytic+arithmetic,
  'trapezoid_weight':H/2 if j in (0,N) else H,'tau':TAU})
  if j<N:plo,phi=down(plo*qlo),up(phi*qhi)
 return rows

def readout(rows,proof):
 """Only this contract-bound, independently reconstructed proxy grid is accepted.

 This wrapper checks the declared model packet and every generated row against
 the proved reference recurrence/error rule. The proof is in report.md; hashing
 or a caller's Boolean alone never establishes a theorem or state provenance.
 """
 if proof!=provenance():raise ValueError('missing or mismatched actual-state provenance')
 if not isinstance(rows,list) or len(rows)!=N+1:raise ValueError('all 4097 nodes required')
 for row in rows:
  if not isinstance(row,dict) or set(row)!=set(HEADER):raise ValueError('complete node fields required')
  if type(row['index']) is not int or any(type(row[k]) is not Q for k in HEADER if k!='index'):
   raise ValueError('exact rational node fields and integer index required')
 expected=generate_rows(constants())
 if rows!=expected:raise ValueError('node, reference recurrence, actual error, clock or weight mismatch')
 if any(r['certified_actual_error']>EPS for r in rows):raise ValueError('actual node error exceeds inherited contract')
 exact_bins=[(r['datum'],r['datum']) for r in rows]
 old=inherited.evaluate(exact_bins)
 require(old['computed_AQ_samples'] is False and old['conditional_on_sample_contract'] is True,'historical evaluator flags changed')
 endpoint=max(Q(0),rows[-1]['datum']+rows[-1]['certified_actual_error'])
 endpoint_tail=16*endpoint
 tail=min(endpoint_tail,old['tail_upper'])
 secondary_lower=max(Q(0),old['trap_lower']-old['quadrature_allowance']-old['noise_allowance'])
 secondary_upper=old['trap_upper']+tail+old['noise_allowance']
 secondary={'lower':secondary_lower,'upper':secondary_upper,'width':secondary_upper-secondary_lower,
 'endpoint_actual_upper':endpoint,'endpoint_tail_upper':endpoint_tail,'mass_tail_upper':old['tail_upper'],
 'selected_tail_upper':tail,'target_width':Q(1,2500),'target_width_passed':secondary_upper-secondary_lower<=Q(1,2500),
 'free_inverse_included':secondary_lower<=Q(1,12)<=secondary_upper}
 return old,secondary

def validate_control_measure(atoms):
 """Only the abstract gap/mass/first-moment upper class; not AQ provenance."""
 if not atoms or any(w<=0 or x<Q(1,16) for w,x in atoms):
  raise ValueError('positive centered spectral support at least 1/16 required')
 if sum((w for w,x in atoms),Q(0))>Q(63,250) or sum((w*x for w,x in atoms),Q(0))>Q(94,125):
  raise ValueError('abstract spectral moment upper bound violated')
 return True

def compute():
 cp=BASE/'inputs/research/round31/contracts/at6.json'
 require(sha(cp)==CONTRACT_SHA,'contract changed')
 contract=json.loads(cp.read_text())
 for rel in contract['shared_premises']+[contract['contract_review']]:
  path=BASE/'inputs'/rel
  require(path.is_file() and not path.is_symlink(),'required premise snapshot missing: '+rel)
 require((BASE/'historical_evaluator.py').read_bytes()==(BASE/'inputs/research/round30/forward/at3/evaluator.py').read_bytes(),'historical evaluator modified')
 require((BASE/'arithmetic.py').read_bytes()==(BASE/'inputs/research/round31/forward/at5/calculator.py').read_bytes(),'inherited own arithmetic modified')
 const=constants();rows=generate_rows(const);proof=provenance();old,second=readout(rows,proof)
 checks=[]
 def check(name,condition,**detail):
  require(condition,'failed '+name);checks.append({'id':name,'passed':True,**serial(detail)})
 exp2lo,exp2hi=exp_negative(2)
 check('continuous_window_monotonicity',L/T>3 and exp2lo>Q(1,10),proof='derivative s log(1+(L/s)^2) >= log(10)-2 >0 since L/s>=L/T>3')
 check('zero_time_centered_variance',rows[0]['datum']==Q(1,4) and rows[0]['arithmetic_radius']==0 and const['zero_time_error']==const['D']/2+const['D']**2>const['D']/2)
 max_arithmetic=max(r['arithmetic_radius'] for r in rows);max_error=max(r['certified_actual_error'] for r in rows)
 check('entire_continuous_analytic_window',const['zero_time_error']<=const['uniform_positive_time_error']<EPS and const['uniform_positive_time_error']+max_arithmetic<=EPS,uniform_error=const['uniform_positive_time_error'],max_export_arithmetic=max_arithmetic)
 check('all_nodes_same_model_clock',len(rows)==4097 and all(r['index']==j and r['s']==j*H and r['tau']==TAU for j,r in enumerate(rows)) and rows[-1]['s']==T)
 weighted=sum((r['trapezoid_weight']*r['datum'] for r in rows),Q(0))
 weights=sum((r['trapezoid_weight'] for r in rows),Q(0))
 check('every_trapezoid_weight_used',weights==T and weighted==old['trap_lower']==old['trap_upper'] and rows[0]['trapezoid_weight']==rows[-1]['trapezoid_weight']==H/2)
 wrong_endpoint_sum=weighted+H*(rows[0]['datum']+rows[-1]['datum'])/2
 check('endpoint_halfweights_necessary',wrong_endpoint_sum>weighted)
 check('arithmetic_and_actual_error_distinct',old['arithmetic_trap_width']==0 and max_arithmetic>0 and all(r['certified_actual_error']==r['analytic_error']+r['arithmetic_radius'] for r in rows),description='exact rational datum is passed to evaluator, so node midpoint arithmetic is already charged to actual error, with zero additional evaluator bins')
 rejects=[]
 bad_proof=dict(proof);bad_proof['tau']='1/100000000'
 bad_rows=list(rows);bad_rows[1]=dict(rows[1]);bad_rows[1]['datum']+=Q(1,100)
 bad_error=list(rows);bad_error[-1]=dict(rows[-1]);bad_error[-1]['certified_actual_error']=Q(0)
 bad_index=list(rows);bad_index[2]=dict(rows[2]);bad_index[2]['index']=1
 bad_float=list(rows);bad_float[0]=dict(rows[0]);bad_float[0]['datum']=0.25
 bad_weight=list(rows);bad_weight[-1]=dict(rows[-1]);bad_weight[-1]['trapezoid_weight']=H
 for label,r,p in [('no_provenance',rows,None),('wrong_coupling',rows,bad_proof),('missing_node',rows[:-1],proof),('changed_datum',bad_rows,proof),('deleted_actual_error',bad_error,proof),('duplicate_index',bad_index,proof),('floating_datum',bad_float,proof),('full_endpoint_weight',bad_weight,proof)]:
  try:readout(r,p)
  except ValueError:rejects.append(label)
  else:raise RuntimeError('invalid grid/provenance admitted '+label)
 check('provenance_and_all_rows_required',len(rejects)==8,rejected=rejects)
 check('historical_source_and_flags_unchanged',old['computed_AQ_samples'] is False and old['conditional_on_sample_contract'] is True)
 check('primary_actual_inverse_width',old['target_width_passed'] is True and old['width']<=Q(1,500))
 check('secondary_endpoint_tail_width',second['target_width_passed'] is True and second['width']<=Q(1,2500) and second['endpoint_tail_upper']<old['tail_upper'])
 check('free_inverse_retained',old['lower']<=Q(1,12)<=old['upper'] and second['free_inverse_included'])
 plus=inherited.evaluate([r['datum']+EPS for r in rows]);minus=inherited.evaluate([r['datum']-EPS for r in rows])
 check('rootN_rejected_for_correlated_errors',plus['trap_lower']-weighted==T*EPS and weighted-minus['trap_upper']==T*EPS and T*EPS/64<T*EPS)
 # Valid slow measure eta=(1/4)delta_(1/16), for the gap/moment upper class.
 slow_mass=Q(1,4);gap=Q(1,16);e8lo,e8hi=exp_negative(8)
 validate_control_measure([(slow_mass,gap)])
 slow_tail_lower=slow_mass/gap*e8lo
 slow_quadrature=H*H*(slow_mass*gap)/8
 check('deleting_infinite_tail_is_damaging',slow_tail_lower>slow_quadrature+T*EPS,scope='abstract positive measure with support at the gap; not an AQ realization',tail_lower=slow_tail_lower)
 # eta_delta=(1/4-delta)delta_3+delta delta_a differs from free C
 # by delta(exp(-as)-exp(-3s)) in [0,delta], hence is compatible
 # with the uniform epsilon data error but has a slow endpoint component.
 delta=EPS/2;reference_end_upper=rows[-1]['reference_upper']
 validate_control_measure([(Q(1,4)-delta,Q(3)),(delta,gap)])
 check('actual_endpoint_upper_not_free_endpoint',delta/gap*e8lo>16*reference_end_upper and delta<=EPS and second['endpoint_actual_upper']>reference_end_upper,scope='abstract gap/moment-upper control consistent with uniform proxy errors, not an AQ realization')
 # Wrong quadrature sign can reject even the exact free inverse despite noise.
 check('wrong_quadrature_sign_rejected',weighted+old['quadrature_allowance']-old['noise_allowance']>Q(1,12))
 vacuum_residue=Q(1,100)
 rejected_zero=False
 try:validate_control_measure([(Q(1,4)-vacuum_residue,Q(3)),(vacuum_residue,Q(0))])
 except ValueError:rejected_zero=True
 check('zero_energy_contamination_rejected',rejected_zero,description='a zero-energy atom gives constant C, divergent inverse integral and violates centered positive-gap premise')
 cap=constants(tau=Q(1,10**8));old_cutoff=constants(cutoff=Q(10000))
 check('original_cap_and_old_cutoff_insufficient',cap['uniform_positive_time_error']>EPS and old_cutoff['uniform_positive_time_error']>EPS)
 alpha_fixture=Q(5);hbar_fixture=Q(7)
 check('physical_inverse_and_clock',T*hbar_fixture/alpha_fixture==Q(896,5) and (old['lower']/alpha_fixture)*alpha_fixture==old['lower'] and (old['lower']*hbar_fixture/alpha_fixture)/hbar_fixture==old['lower']/alpha_fixture)
 return {'loop':'AT6','direction':'forward','human_author':'Hruday N M (BUNZEEY)',
 'contribution_alias':'HNM-AT6-F actual AQ finite-grid and inverse-energy enclosure',
 'actual_aq_enclosure':True,'actual_aq_certified_proxy_grid':True,'actual_aq_inverse_enclosure':True,
 'measured_interacting_samples':False,'simulated_interacting_samples':False,'exact_interacting_trajectory':False,
 'actual_input_provenance_discharged':True,'historical_evaluator_flags_preserved':True,
 'uniform_wilson_claim':False,'continuum_claim':False,'state_uniqueness_claim':False,'resolved_interaction_shift':False,
 'scientific_priority_verified':False,'target_met':old['target_width_passed'],'secondary_target_met':second['target_width_passed'],
 'parameters':proof,'window_certificate':const,'node_count':len(rows),'max_node_error':max_error,'max_reference_arithmetic_radius':max_arithmetic,
 'historical_evaluator_output':old,'primary_actual_inverse_interval':{'lower':old['lower'],'upper':old['upper'],'width':old['width'],'target_width':Q(1,500),'free_inverse_included':old['lower']<=Q(1,12)<=old['upper']},
 'endpoint_informed_actual_inverse_interval':second,
 'physical_R_intervals':{'definition':'R=I/alpha, alpha>0; inverse-energy units; not susceptibility','primary_lower':f"({textq(old['lower'])})/alpha",'primary_upper':f"({textq(old['upper'])})/alpha",'secondary_lower':f"({textq(second['lower'])})/alpha",'secondary_upper':f"({textq(second['upper'])})/alpha"},
 'checks':checks,'stop':'third and final authorized investigation; no further scientific loop'},rows,proof

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
 out=Path(args.output);require(out.is_absolute() and not out.exists(),'fresh absolute output directory required')
 result,rows,proof=compute();out.mkdir(parents=True)
 with (out/'aq-certified-grid.csv').open('w',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=HEADER,lineterminator='\n');writer.writeheader()
  for row in rows:writer.writerow({k:(row[k] if k=='index' else textq(row[k])) for k in HEADER})
 (out/'input-provenance.json').write_text(json.dumps(proof,indent=2,sort_keys=True)+'\n')
 result['grid_sha256']=sha(out/'aq-certified-grid.csv')
 (out/'results.json').write_text(json.dumps(serial(result),indent=2,sort_keys=True)+'\n')
 sources={p.relative_to(BASE).as_posix():sha(p) for p in sorted(BASE.rglob('*')) if p.is_file() and (p.relative_to(BASE).parts[0]=='inputs' or p.name in ('check.py','arithmetic.py','historical_evaluator.py','report.md'))}
 outputs={p.name:sha(p) for p in sorted(out.iterdir()) if p.is_file()}
 (out/'source-manifest.json').write_text(json.dumps({'loop':'AT6','direction':'forward','sources':sources,'outputs':outputs,'contract_sha256':CONTRACT_SHA},indent=2,sort_keys=True)+'\n')
 print(json.dumps({'loop':'AT6','direction':'forward','checks_passed':len(result['checks']),'nodes':len(rows),'target_met':result['target_met'],'secondary_target_met':result['secondary_target_met'],'resolved_interaction_shift':False},sort_keys=True))
if __name__=='__main__':main()
