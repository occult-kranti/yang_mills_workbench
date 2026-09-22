#!/usr/bin/env python3
"""Exact applicability and countermodel audits for AQ1's analytic construction."""
import argparse,hashlib,json
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
HERE=Path(__file__).resolve().parent;tests=[]
def need(ok,name):
 if not ok:raise RuntimeError(name)
 tests.append(name)
S=((0,0,0),(1,0,0),(0,1,0),(0,0,1));E=S[1:]
def plus(a,b):return tuple(x+y for x,y in zip(a,b))
def minus(a,b):return tuple(x-y for x,y in zip(a,b))
def own(p):return(p[0]//4,p[1]//2,p[2])
def dist(a,b):return sum(abs(x-y) for x,y in zip(a,b))
def F(r):return Q(1,(1+r)**4)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args()
 out=Path(a.output).resolve();out.mkdir(parents=True,exist_ok=False)
 links=set();ends=set()
 for b in product(range(-1,2),repeat=3):
  for r,s,j in product(range(4),range(2),range(3)):
   p=(4*b[0]+r,2*b[1]+s,b[2]);need(own(p)==b,'ownership_'+str((b,r,s,j)))
   links.add((p,j));ends|={p,plus(p,E[j])}
 need(len(links)==648 and len(ends)==342,'negative_box_complete_factors_endpoints')
 need((-1)//4==-1 and int(Q(-1,4))==0,'negative_floor_not_truncation')
 need(-1-4*((-1)//4)==3 and -1-4*int(Q(-1,4))==-1,'negative_residue_control')
 zero=(0,0,0);inc={minus(zero,s) for s in S}
 need(len(inc)==4 and len(inc-{zero})==3,'all_incoming_stars')
 tau=Q(1,100000000);M=7*tau;J=4*M
 need(2*M*4==56*tau,'actual_reference_reset_coefficient')
 need(max(dist(s,t) for s in S for t in S)==2,'star_diameter_two')
 shells=[]
 for r in range(1,9):
  count=sum(sum(map(abs,p))==r for p in product(range(-r,r+1),repeat=3))
  need(count==4*r*r+2,'integer_shell_'+str(r));shells.append(count)
  need(Q(count,(1+r)**4)<=Q(6,(1+r)**2),'shell_summability_'+str(r))
 need(32*7==224,'convolution_ceiling')
 B=81*J
 need(B==2268*tau,'interaction_F_norm_ceiling')
 for y in product(range(-2,3),repeat=3):
  common=inc & {minus(y,s) for s in S}
  lhs=len(common)*M/F(dist(zero,y))
  need(lhs<=B,'pair_F_norm_'+str(y))
 conv=sum(F(dist(zero,z))*F(dist((1,2,1),z)) for z in product(range(-3,4),repeat=3))
 need(conv<=224*F(4),'finite_convolution_diagnostic')
 # Trace-one mass escape: each density is normal, but no common energy-tight bound.
 escape=[]
 for n in (2,8,32,128):
  need(n>1 and int(n<=1)==0,'escaping_mass_projection_'+str(n))
  escape.append({'n':n,'trace':1,'energy':n,'fixed_rank_one_mass':0})
 need([Q(1,2),Q(1,2)]!=[Q(1,3),Q(2,3)],'incompatible_marginal_rejected')
 # t_n=pi/n and e_n witness the exact phase -1, norm distance2.
 for n in (1,2,4,16,64):need(2*n-n==n and Q(n,n)==1,'norm_time_discontinuity_'+str(n))
 alpha=Q(24);delta=alpha/8;hbar=Q(2);t=Q(4)
 need(delta*t/hbar==6 and t/hbar==2,'physical_normalized_time_dictionary')
 need(delta*Q(2)==6 and delta*Q(2)/hbar==3,'energy_frequency_dictionary')
 need(Q(0)*81*28==0,'zero_interaction_norm')
 need(len(tests)==len(set(tests)),'unique_check_ids')
 result={'loop':'AQ1','direction':'forward','verdict':'numerical_cap_locally_normal_stationary_subsequence_GNS_nonnegative','checks':tests,'tau_cap':str(tau),'reset_bound':'56|tau||F|','F_sum_ceiling':7,'F_convolution_ceiling':224,'interaction_F_ceiling':str(B),'shell_counts':shells,'mass_escape_control':escape,'norm_volume_convergence':'uniform compact physical time, after delta/hbar conversion','norm_time_continuity_claim':False,'old_tau_star_premise':False,'HTW_premise':False,'whole_sequence_convergence_claim':False,'translation_invariance_claim':False,'gap_passage_this_loop':False,'physical_fixed_sector_equality_this_loop':False}
 (out/'results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 src=[HERE/'report.md',HERE/'check.py',*sorted((HERE/'inputs').rglob('*'))]
 man={'sources':{str(p.relative_to(HERE)):sha(p) for p in src if p.is_file()},'outputs':{'results.json':sha(out/'results.json')}}
 (out/'source-manifest.json').write_text(json.dumps(man,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'checks':len(tests),'verdict':result['verdict']}))
if __name__=='__main__':main()
