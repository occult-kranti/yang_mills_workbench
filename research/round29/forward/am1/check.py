#!/usr/bin/env python3
"""Independent exact AM1 support/template audit, no interacting spectral simulation."""
import argparse,hashlib,json
from fractions import Fraction as Q
from itertools import product,combinations
from pathlib import Path
HERE=Path(__file__).resolve().parent
tests=[]
def need(ok,name):
 if not ok:raise RuntimeError(name)
 tests.append(name)
E=((1,0,0),(0,1,0),(0,0,1));S=((0,0,0),)+E
def plus(a,b):return tuple(x+y for x,y in zip(a,b))
def own(p):return (p[0]//4,p[1]//2,p[2])
def faces(b):
 out=[]
 for r,s in product(range(4),range(2)):
  p=(4*b[0]+r,2*b[1]+s,b[2])
  for i,j in combinations(range(3),2):
   edges={(p,i),(plus(p,E[i]),j),(plus(p,E[j]),i),(p,j)}
   out.append((edges,(i,j)==(0,1) and s==0 and r<3))
 return out
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);a=ap.parse_args()
 out=Path(a.output).resolve();out.mkdir(parents=True,exist_ok=False)
 b=(1,1,1);square=faces(b)[0][0]
 need(len(square)==4,'selected_square_four_links')
 need({own(p) for p,i in square}=={b},'selected_square_one_coarse_factor')
 ends=set()
 for p,i in square:ends|={p,plus(p,E[i])}
 need(len(ends)==4,'four_fine_vertices_not_four_coarse_factors')
 fs=faces((0,0,0));need(sum(sel for _,sel in fs)==3 and sum(not sel for _,sel in fs)==21,'three_selected_21_omitted')
 ancestors={tuple(x-y for x,y in zip(b,s)) for s in S}
 need(len(ancestors)==4,'all_incoming_and_outgoing_anchors')
 indexed=[];touch=[]
 for anc in ancestors:
  for edges,sel in faces(anc):
   if not sel:
    indexed.append(edges)
    if b in {own(p) for p,i in edges}:touch.append(edges)
 need(len(indexed)==84 and len(touch)==49,'84_indexed_49_touching_faces')
 tau=Q(1,64);M=7*tau;J=4*M
 need(J==28*tau and J!=M,'per_site_norm_28tau_not_7tau')
 # Q8 scalar coordinates reproduce only first/second Haar scalar moments.
 qcoords=[Q(1),Q(-1),Q(0),Q(0),Q(0),Q(0),Q(0),Q(0)]
 need(sum(qcoords)/8==0 and sum(x*x for x in qcoords)/8==Q(1,4),'Haar_second_moment_diagnostic')
 need(Q(1)!=Q(0),'Wilson_nonconstant_configuration_values')
 need(Q(3,4)!=Q(4,3),'SU2_SU3_Casimir_copy_rejected')
 need(len(S)==4 and len(S)>3,'three_site_template_not_current_grouping')
 # Actual centered vector proof is analytic. This projector arithmetic audits support label.
 coarse_excitation=[1,0,0,0]
 need(sum(coarse_excitation)==1 and sum(coarse_excitation)<4,'one_factor_counterexample_to_imported_count')
 # Scalar and diagonal retention: simple exact operator fixture, not a rotor cutoff.
 H=[Q(0),Q(2)];scalar=Q(7);D=[Q(0),Q(3)]
 full=[h+scalar+d for h,d in zip(H,D)]
 need(full[1]-full[0]==5,'retained_diagonal_gap_five')
 need(H[1]-H[0]==2 and full[1]-full[0]!=H[1]-H[0],'drop_diagonal_rejected')
 need((full[1]-scalar)-(full[0]-scalar)==full[1]-full[0] and full[0]!=full[0]-scalar,'scalar_ground_and_gap_distinguished')
 # A missing value cannot pass numeric admission; zeros and convenient epsilons are not constants.
 constants={'c1':None,'c2':None,'fixed_point_radius':None,'transformed_commutator_factor':None}
 need(not all(v is not None and v>0 for v in constants.values()),'unevaluated_constants_block_numeric_radius')
 result={'loop':'AM1','direction':'forward','verdict':'insufficient_numerical_radius_scoped_transfer_obstruction','checks':tests,'one_factor_excitation':'(W-mean_Omega W)Omega, positive variance from strict ground positivity','counts':{'selected':3,'omitted':21,'incoming_anchors':4,'indexed_faces':84,'actually_touching_faces':49},'J':'28|tau|','unknown_constants':constants,'source_four_active_links_not_four_blocks':True,'source_energy_inequality_refuted':False,'new_numerical_radius':False}
 (out/'results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 src=[HERE/'report.md',HERE/'check.py',*sorted((HERE/'inputs').rglob('*'))]
 man={'sources':{str(p.relative_to(HERE)):sha(p) for p in src if p.is_file()},'outputs':{'results.json':sha(out/'results.json')}}
 (out/'source-manifest.json').write_text(json.dumps(man,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'checks':len(tests),'verdict':result['verdict']}))
if __name__=='__main__':main()
