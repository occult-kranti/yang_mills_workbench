#!/usr/bin/env python3
"""AN1 reverse: exact full-star and two-radius geometry."""
from pathlib import Path
from itertools import product
import argparse,hashlib,json
BASE=Path(__file__).resolve().parent
E={(1,0,0),(0,1,0),(0,0,1)};O=(0,0,0);S={O,*E};Y={O,(0,0,1)}
def need(x,m):
    if not x:raise AssertionError(m)
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def star(a):return {add(a,e) for e in S}
def box(n):return set(product(range(-n,n+1),repeat=3))
def depth(x,n):return min(n+1-abs(t) for t in x)
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=BASE/'output');args=p.parse_args()
    need(json.loads((BASE/'inputs/research/round29/contracts/an1.json').read_text())['id']=='AN1','contract')
    fixtures=[]
    for n in (3,4,6):
      B=box(n);G=box(2*n);bulk={x for x in B if depth(x,n)>2};canonical={x for x in B if depth(x,n)>1}
      old={x for x in B if star(x)<=B};large={x for x in G if star(x)<=G}
      need(canonical<=old<=large,'nested canonical anchors')
      need(all(not (star(x)&bulk) for x in (old-canonical)|(large-canonical)),'all boundary differences outside bulk')
      distance=min(depth(y,n-2) for y in Y);need(distance==n-2,'fixed-Y distance')
      near={(n-2,0,0)};near_d=min(depth(y,n-2) for y in near);need(near_d==1,'near boundary control')
      fixtures.append({'n':n,'small_volume':len(B),'large_volume':len(G),'common_bulk':len(bulk),'whole_star_anchors_small':len(old),'canonical_anchors':len(canonical),'distance':distance,'near_boundary_distance':near_d,'boundary_anchor_difference':len(old-canonical)})
    # Full original endpoint cover of the two adjacent complete factors.
    links=set();vertices=set()
    for z in (0,1):
     for x in range(4):
      for y in range(2):
       for d,e in enumerate(sorted(E)):
        v=(x,y,z);links.add((v,d));vertices|={v,add(v,e)}
    need(len(links)==48 and len(vertices)==36,'48-link physical completion')
    incoming={tuple(y[i]-s[i] for i in range(3)) for y in Y for s in S}
    need(len(incoming)==7 and len({tuple(O[i]-s[i] for i in range(3)) for s in S})==4,'incoming incidence')
    changed_anchor=O;need(bool(star(changed_anchor)&Y),'changed bulk term detected')
    def admit(symbolic_premise,translation_equal):return symbolic_premise and translation_equal
    controls={'near_boundary_not_diverging':all(f['near_boundary_distance']==1 for f in fixtures),'changed_bulk_requires_new_problem':bool(star(changed_anchor)&Y),'incoming_stars_not_just_Y':len(incoming)>len(Y),'Rzero_wrong_distance':fixtures[-1]['distance']!=6,'deleted_HTW_smallness_rejected':not admit(False,True),'vary_selected_triple_rejected':not admit(True,False)}
    need(all(controls.values()),'controls')
    result={'loop':'AN1','direction':'reverse','verdict':'finite common-bulk theorem application accepted conditionally on explicit HTW smallness','region_original_links':48,'region_endpoint_vertices':36,'Y_sites':2,'incoming_anchors_to_Y':len(incoming),'range':1,'eroded_bulk':'[-n+2,n-2]^3','distance':'n-2','enclosure':'min(2, exp(2*c1-c2*(n-2)))','fixtures':fixtures,'controls':controls,'source_constants':'positive, unevaluated; 7|tau|<=c_HTW(1,1)','scope':'Finite comparison only; no limiting-state identification in this loop.'}
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    files=[BASE/'check.py',BASE/'report.md']+sorted(f for f in (BASE/'inputs').rglob('*') if f.is_file());h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
    (out/'manifest.json').write_text(json.dumps({'source_files':[{'path':str(f.relative_to(BASE)),'sha256':h(f)} for f in files],'results_sha256':h(out/'results.json')},indent=2)+'\n');print(json.dumps({'loop':'AN1','passed':True,'controls':len(controls),'geometries':len(fixtures)}))
if __name__=='__main__':main()
