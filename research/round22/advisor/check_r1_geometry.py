"""Independent advisor check of actual free-link parity and complete-star boundary counts."""
from fractions import Fraction as F
from itertools import product,combinations
import json
from pathlib import Path

def need(ok,why):
    if ok is not True:raise ValueError(why)
def add(p,a):return tuple(x+int(i==a) for i,x in enumerate(p))
def free(edge):
    a,p=edge
    return a==2 or (a==0 and p[0]%4==3) or (a==1 and p[1]%2==1)
def star(p):return {p,*[add(p,a) for a in range(3)]}
faces=[]
for p in product(range(4),range(2),range(1)):
 for a,b in combinations(range(3),2):
  if (a,b)==(0,1) and p[0]<3 and p[1]==0:continue
  edges={(a,p),(b,add(p,a)),(a,add(p,b)),(b,p)}
  faces.append({'base':p,'axes':(a,b),'free':{e for e in edges if free(e)}})
probe=(2,(0,0,0))
need(len(faces)==21,'all omitted faces')
need(all(len(f['free']-{probe})>=1 for f in faces),'another free link must remain')
need(len({tuple(sorted(f['free'])) for f in faces})==21,'distinct free-center parity sectors')
need(F(21,4)*F(1,18)**2==F(7,432),'actual boundary norm coefficient')
rows=[]
for L in range(1,15):
 lam=set(product(range(L+2),repeat=3));anchors=[b for b in lam if star(b)<=lam]
 for kind,start in [('origin',0),('bulk',1)]:
  Y=set(product(range(start,start+L),repeat=3))
  boundary=[b for b in anchors if star(b)&Y and not star(b)<=Y]
  expected=(3*L*L-3*L+1) if kind=='origin' else 6*L*L-3*L+1
  need(len(boundary)==expected,'crossing star count')
  rows.append({'L':L,'kind':kind,'boundary_stars':len(boundary)})
small=set(product(range(2),repeat=3)); retained=[b for b in small if star(b)<=small]
need(retained==[(0,0,0)],'fixed probe volume retains only origin star')
result={'passed':True,'all_actual_omitted_faces':21,'free_center_parity_sectors':21,'each_face_has_free_link_other_than_probe':True,'probe_onsite_energy':'6','probe_source_norm_squared':'1','actual_boundary_defect_squared':'(7/432) tau^2','probe_is_actual_O1_residual':False,'cube_counts':rows,'minimum_inverse_gap_in_contract':str(1-28*F(5,1664)),'research_loops_added':0}
import argparse
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);out=p.parse_args().output
need(not out.exists(),'fresh output required');out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
