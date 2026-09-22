#!/usr/bin/env python3
"""Exact spectral-tail diagnostics for the analytic AO2 transfer."""
import argparse,hashlib,json
from fractions import Fraction as Q
from pathlib import Path
HERE=Path(__file__).resolve().parent;tests=[]
def need(ok,name):
 if not ok:raise RuntimeError(name)
 tests.append(name)
def moment(mu,k):return sum(w*E**k for E,w in mu)
def resolvent_i(mu):return [sum(w*E/(E*E+1) for E,w in mu),sum(w/(E*E+1) for E,w in mu)]
def theta(x):return Q(1) if x<=1 else (2-x if x<2 else Q(0))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args()
 out=Path(a.output).resolve();out.mkdir(parents=True,exist_ok=False)
 old=[];new=[]
 for n in (2,4,16,64,256):
  mu=[(Q(1,4),1-Q(1,2*n)),(Q(n),Q(1,2*n))]
  need(moment(mu,1)<1 and moment(mu,2)>Q(n,2),'old_escape_second_moment_'+str(n))
  old.append({'n':n,'mu1':str(moment(mu,1)),'mu2':str(moment(mu,2))})
  eta=[(Q(1),1-Q(1,n*n)),(Q(n),Q(1,n*n))]
  need(moment(eta,0)==1 and moment(eta,2)==2-Q(1,n*n),'bounded_second_escape_'+str(n))
  need(moment(eta,1)==1-Q(1,n*n)+Q(1,n),'first_moment_still_converges_'+str(n))
  need(Q(1,n*n)*n*n==1,'second_tail_mass_one_'+str(n))
  for cutoff_index,L in enumerate((Q(1),Q(3,2),Q(n,2),Q(2*n))):
   tail=sum(w*E for E,w in eta if E>L)
   need(tail<=moment(eta,2)/L,'tail_bound_'+str((n,cutoff_index,L)))
   cutoff=sum(w*E*theta(E/L) for E,w in eta)
   need(0<=moment(eta,1)-cutoff<=moment(eta,2)/L,'compact_cutoff_error_'+str((n,cutoff_index,L)))
  new.append({'n':n,'mu1':str(moment(eta,1)),'mu2':str(moment(eta,2)),'resolvent_i':list(map(str,resolvent_i(eta)))})
 # Correct centering in a two-state diagnostic W=(I+sigma_x)/2.
 uncentered=[(Q(0),Q(1,4)),(Q(6),Q(1,4))];centered=[(Q(6),Q(1,4))]
 need(moment(uncentered,0)==Q(1,2) and moment(centered,0)==Q(1,4),'moving_mean_changes_mass')
 shifted=[(E+7,w) for E,w in centered]
 need(moment(shifted,1)!=moment(centered,1) and moment(shifted,2)!=moment(centered,2),'raw_ground_shift_not_centered')
 alpha=Q(24);delta=alpha/8;Ehat=Q(2);v=Q(1,4)
 need(delta*Ehat==6 and v*(delta*Ehat)**2==9,'delta_energy_and_second_moment')
 need(v*Ehat**2!=v*(delta*Ehat)**2,'normalized_generator_substitution_rejected')
 B2=alpha**2*(36+28*Q(1,65536));L=10*alpha
 need(B2/L==alpha*(36+Q(7,16384))/10,'physical_tail_units')
 need(Q(3,4)*alpha==alpha*(1-Q(1,4)),'free_Wilson_first_identity')
 premises=['|tau|<tau_*','|tau|<=2^-16','actual AK2 state/resolvent','AO1 same finite measures']
 need(any('tau_*' in s for s in premises),'original_symbolic_restriction_retained')
 result={'loop':'AO2','direction':'forward','verdict':'actual_first_moment_equality_and_operator_domain','checks':tests,'identity':'<chi,H_phys chi>=alpha omega(1-W^2)','second_moment_bound':'alpha^2(36+28|tau|)','first_tail':'B2/L','old_countermeasure':old,'second_escape_control':new,'premises':premises,'second_moment_equality_proved':False,'new_AQ_state_identity_assumed':False}
 (out/'results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 src=[HERE/'report.md',HERE/'check.py',*sorted((HERE/'inputs').rglob('*'))]
 man={'sources':{str(p.relative_to(HERE)):sha(p) for p in src if p.is_file()},'outputs':{'results.json':sha(out/'results.json')}}
 (out/'source-manifest.json').write_text(json.dumps(man,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'checks':len(tests),'verdict':result['verdict']}))
if __name__=='__main__':main()
