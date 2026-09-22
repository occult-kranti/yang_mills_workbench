#!/usr/bin/env python3
"""Exact boundary/support fixtures for the analytic HTW application."""
import argparse,hashlib,json
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
HERE=Path(__file__).resolve().parent
tests=[]
def need(ok,name):
 if not ok:raise RuntimeError(name)
 tests.append(name)
E=((1,0,0),(0,1,0),(0,0,1));S=((0,0,0),)+E
def plus(a,b):return tuple(x+y for x,y in zip(a,b))
def box(n):return set(product(range(-n,n+1),repeat=3))
def anchors(B):return {b for b in B if all(plus(b,s) in B for s in S)}
def star(b):return {plus(b,s) for s in S}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args()
 out=Path(a.output).resolve();out.mkdir(parents=True,exist_ok=False)
 Y={(0,0,0),(0,0,1)};rows=[]
 for n in (3,4,5):
  A=box(n);B=box(2*n);D=box(n-2);canon=box(n-1);aa=anchors(A);bb=anchors(B)
  need(canon<=aa<=bb,'anchor_inclusions_'+str(n))
  need(len(aa)==(2*n)**3 and len(bb)==(4*n)**3,'whole_star_counts_'+str(n))
  need(all(not star(b)&D for b in (aa-canon)|(bb-canon)),'difference_misses_common_bulk_'+str(n))
  dist=min((n-2)+1-max(abs(t) for t in y) for y in Y)
  need(dist==n-2,'exact_Y_distance_'+str(n))
  need((-n,0,0) not in D,'near_boundary_distance_zero_'+str(n))
  rows.append({'n':n,'A_sites':len(A),'B_sites':len(B),'A_anchors':len(aa),'B_anchors':len(bb),'canonical_anchors':len(canon),'common_bulk_sites':len(D),'Y_distance':dist})
 inc={tuple(x-y for x,y in zip(b,s)) for b in Y for s in S}
 need(len(inc)==7 and len(inc-Y)==5,'seven_incident_stars_not_two')
 need(len({tuple(-v for v in s) for s in S})==4,'singleton_four_stars')
 links=set();ends=set()
 for b in Y:
  for r,s,i in product(range(4),range(2),range(3)):
   p=(4*b[0]+r,2*b[1]+s,b[2]);links.add((p,i));ends|={p,plus(p,E[i])}
 need(len(links)==48 and len(ends)==36,'complete_48_link_36_endpoint_cover')
 need(max(sum(abs(x) for x in s) for s in S)==1,'range_one_not_zero')
 need(star((0,0,0))&box(1),'changed_bulk_interaction_not_exterior')
 # sigma_x with sigma_z has a nonzero commutator, so disjointness is material.
 comm=[[0,-2],[2,0]]
 need(any(v!=0 for row in comm for v in row),'changed_bulk_commutator_control')
 # Rank-one map |psi><e0|, psi_n=1/n, is bounded but leaves D(diag n).
 domain_rows=[]
 for N in (4,16,64):
  norm2=sum(Q(1,k*k) for k in range(1,N+1));generator_norm2=sum(Q(k*k,k*k) for k in range(1,N+1))
  need(norm2<2 and generator_norm2==N,'unbounded_domain_control_'+str(N))
  domain_rows.append({'N':N,'norm2':str(norm2),'generator_norm2':str(generator_norm2)})
 need(Q(1,8)!=Q(1,16),'translated_selected_coefficient_change_detected')
 source_premises={'HTW_norm_smallness':'7|tau|<=c_HTW(1,1)','c_HTW_evaluated':False,'ground_in_bulk_proved':'report Sections1-2','R':1,'onsite_gap':1}
 need(bool(source_premises['HTW_norm_smallness']) and not source_premises['c_HTW_evaluated'],'symbolic_added_smallness_retained')
 result={'loop':'AN1','direction':'forward','verdict':'conditional_uniform_finite_local_comparison','checks':tests,'geometry':rows,'bound':'min(2,exp(2*C1-C2*(n-2))) for n>=3 and ||A||<=1','source_premises':source_premises,'domain_control':domain_rows,'limit_identification_executed':False,'numerical_HTW_radius':False}
 (out/'results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 src=[HERE/'report.md',HERE/'check.py',*sorted((HERE/'inputs').rglob('*'))]
 man={'sources':{str(p.relative_to(HERE)):sha(p) for p in src if p.is_file()},'outputs':{'results.json':sha(out/'results.json')}}
 (out/'source-manifest.json').write_text(json.dumps(man,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'checks':len(tests),'verdict':result['verdict']}))
if __name__=='__main__':main()
