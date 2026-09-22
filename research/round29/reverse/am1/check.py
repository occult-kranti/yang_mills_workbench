#!/usr/bin/env python3
"""AM1 reverse geometry/counting controls; no numerical stability radius."""
from pathlib import Path
from fractions import Fraction as F
import argparse,hashlib,json
BASE=Path(__file__).resolve().parent
def need(x,msg):
    if not x:raise AssertionError(msg)
def add(x,y):return tuple(a+b for a,b in zip(x,y))
E=[(1,0,0),(0,1,0),(0,0,1)];O=(0,0,0)
def block(x):return(x[0]//4,x[1]//2,x[2])
def face(v,i,j):return[(v,i),(add(v,E[i]),j),(add(v,E[j]),i),(v,j)]
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=BASE/'output');args=p.parse_args()
    need(json.loads((BASE/'inputs/research/round29/contracts/am1.json').read_text())['id']=='AM1','contract')
    loop=face(O,0,1);tails={v for v,d in loop};vertices={O,E[0],E[1],add(E[0],E[1])};coarse={block(v) for v,d in loop}
    need(len(loop)==4 and len(vertices)==4 and len(tails)==3 and len(coarse)==1,'cycle versus block counts')
    # Exact excitation-sector tensor algebra on four factors: |1000>.
    bitstate=8; number=sum((bitstate>>i)&1 for i in range(4));need(number==1 and number<4,'one coarse excitation')
    omitted=[]
    for x in range(4):
     for y in range(2):
      for i,j in [(0,1),(0,2),(1,2)]:
       if not ((i,j)==(0,1) and y==0 and x<3):omitted.append(face((x,y,0),i,j))
    need(len(omitted)==21,'complete omitted inventory')
    q=(1,1,1);anchors=[q]+[tuple(q[j]-e[j] for j in range(3)) for e in E]
    need(len(set(anchors))==4,'all star anchors')
    tau=F(1,1000);per_anchor=21*tau/3;per_site=4*per_anchor
    need(per_anchor==7*tau and per_site==28*tau,'incidence conversion')
    # Gauge-group normalization, with known fundamental Casimirs and trace ranges.
    su2_casimir=F(3,4);su3_casimir=F(4,3)
    su2_radius=(F(1)-F(-1))/2;su3_radius=(F(1)-F(-1,2))/2
    need(su2_casimir!=su3_casimir and su2_radius!=su3_radius,'SU3 transfer invalid')
    # Arbitrary finite self-adjoint K: retain scalar, mixing and diagonal.
    K=[[F(2),F(1),F(0)],[F(1),F(3),F(2)],[F(0),F(2),F(-1)]]
    c=K[0][0];B=[[F(0) for j in range(3)] for i in range(3)];Z=[[F(0) for j in range(3)] for i in range(3)]
    for i in range(3):
     for j in range(3):
      if (i==0) != (j==0):B[i][j]=K[i][j]
      if i>0 and j>0:Z[i][j]=K[i][j]-(c if i==j else 0)
    full=[[c*(i==j)+B[i][j]+Z[i][j] for j in range(3)] for i in range(3)]
    need(full==K,'exact decomposition')
    controls={'fine_vertices_not_coarse_factors':len(vertices)!=len(coarse),'incoming_stars_required':per_site!=per_anchor,'SU3_Casimir_not_SU2':su3_casimir!=su2_casimir,'SU3_trace_radius_not_SU2':su3_radius!=su2_radius,'drop_scalar_changes_operator':[[B[i][j]+Z[i][j] for j in range(3)] for i in range(3)]!=K,'drop_retained_diagonal_changes_operator':[[c*(i==j)+B[i][j] for j in range(3)] for i in range(3)]!=K}
    # No execution turns a source existence declaration into a numerical bound.
    source_constants={'c1':None,'c2':None,'fixed_point_radius':None,'commutator_constant':None,'resolvent_constant':None}
    numerical_admission=all(v is not None for v in source_constants.values());need(not numerical_admission,'unresolved source constants')
    need(all(controls.values()),'controls')
    result={'loop':'AM1','direction':'reverse','verdict':'insufficient numerical radius; specified source transfer unmatched','selected_loop':{'links':len(loop),'fine_vertices':len(vertices),'fine_outgoing_blocks':len(tails),'coarse_factors':len(coarse),'centered_excitation_number':number},'star_budget':{'faces':21,'anchors':4,'norm_per_anchor':'7|tau|','norm_per_site':'28|tau|'},'source_constants':source_constants,'numerical_admission':numerical_admission,'controls':controls,'scope':'One-factor count counterexample refutes >=4 excited coarse factors, not >=4-energy inequality or actual gap. Source itself counts active links, not >=4 blocks.'}
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    files=[BASE/'check.py',BASE/'report.md']+sorted(f for f in (BASE/'inputs').rglob('*') if f.is_file());h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
    (out/'manifest.json').write_text(json.dumps({'source_files':[{'path':str(f.relative_to(BASE)),'sha256':h(f)} for f in files],'results_sha256':h(out/'results.json')},indent=2)+'\n');print(json.dumps({'loop':'AM1','passed':True,'controls':len(controls),'radius':'insufficient'}))
if __name__=='__main__':main()
