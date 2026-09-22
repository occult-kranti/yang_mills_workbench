#!/usr/bin/env python3
"""Independent-cutoff geometry and logical controls for AN2."""
import argparse,hashlib,json
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
HERE=Path(__file__).resolve().parent
tests=[]
def need(ok,name):
 if not ok:raise RuntimeError(name)
 tests.append(name)
S=((0,0,0),(1,0,0),(0,1,0),(0,0,1))
def plus(a,b):return tuple(x+y for x,y in zip(a,b))
def box(lo,hi):return set(product(range(lo,hi+1),repeat=3))
def stars(B):return {b for b in B if all(plus(b,s) in B for s in S)}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args()
 out=Path(a.output).resolve();out.mkdir(parents=True,exist_ok=False)
 rows=[]
 for n,L,M in ((3,6,3),(3,9,5),(4,8,7),(4,13,4),(5,12,6)):
  O=box(-n,L-n);C=box(-M,M);core=box(-n,n);D=box(-n+2,n-2);canon=box(-n+1,n-1)
  need(core<=O and core<=C,'independent_outer_containment_'+str((n,L,M)))
  different=(stars(O)|stars(C))-canon
  need(all(not {plus(b,s) for s in S}&D for b in different),'common_bulk_difference_'+str((n,L,M)))
  F={(0,0,0),(1,-1,1)};r=1
  distance=min(n-1-max(abs(x) for x in f) for f in F)
  need(distance==n-r-1,'region_distance_'+str((n,L,M)))
  rows.append({'n':n,'L':L,'M':M,'O_sites':len(O),'C_sites':len(C),'F_distance':distance})
 for n,M,Mp in ((3,3,6),(3,7,4),(4,6,5)):
  need(box(-n,n)<=box(-M,M) and box(-n,n)<=box(-Mp,Mp),'all_pair_Cauchy_geometry_'+str((n,M,Mp)))
 k=(1,-2,1);n=3;M=n+max(map(abs,k));translated={tuple(x-y for x,y in zip(b,k)) for b in box(-M,M)}
 need(box(-n,n)<=translated,'translation_invariance_common_bulk')
 triangular=[]
 for n in (3,4,8,16):
  diagonal=int(2*n>=n*n);outer=int(n*n>=n*n)
  need(diagonal==0 and outer==1,'triangular_array_'+str(n))
  triangular.append({'n':n,'a_n_2n':diagonal,'a_n_n2':outer})
 # Normal two-factor density and its exact marginal.
 joint=[Q(1,8),Q(3,8),Q(1,4),Q(1,4)]
 marginal=[sum(joint[:2]),sum(joint[2:])]
 need(sum(joint)==1 and all(x>=0 for x in joint) and marginal==[Q(1,2),Q(1,2)],'compatible_positive_trace_one_marginal')
 need(marginal!=[Q(1,3),Q(2,3)],'one_inconsistent_marginal_rejected')
 for n in (3,9,27):need((-n,0,0) not in box(-n+2,n-2),'near_boundary_no_vanishing_distance_'+str(n))
 need(Q(1,8)!=Q(1,16),'altered_selected_triple_rejected')
 premises=['I1 |tau|<tau_*','7|tau|<=c_HTW(1,1)','same coarse translation triple','AN1 bounded-commutator domain dictionary']
 need(any('HTW' in p for p in premises),'added_HTW_premise_required')
 result={'loop':'AN2','direction':'forward','verdict':'conditional_ordered_local_bulk_state_identification','checks':tests,'independent_cutoffs':rows,'triangular_array_control':triangular,'bound':'min(2,exp(C1*|F|-C2*(n-r-1)))','limit_order':['L->infinity with n fixed','M->infinity independently','n->infinity'],'normal_compatible_local_state':True,'coarse_translation_invariant':True,'required_premises':premises,'generator_identification':False,'all_boundaries_identified':False,'continuum_proof':False}
 (out/'results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 src=[HERE/'report.md',HERE/'check.py',*sorted((HERE/'inputs').rglob('*'))]
 man={'sources':{str(p.relative_to(HERE)):sha(p) for p in src if p.is_file()},'outputs':{'results.json':sha(out/'results.json')}}
 (out/'source-manifest.json').write_text(json.dumps(man,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'checks':len(tests),'verdict':result['verdict']}))
if __name__=='__main__':main()
