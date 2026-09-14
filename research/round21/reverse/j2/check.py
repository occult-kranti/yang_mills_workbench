#!/usr/bin/env python3
"""Reverse J2 exact symmetry, GNS and reducing-subspace fixtures."""
from pathlib import Path
from fractions import Fraction as F
import argparse, hashlib, json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def mm(a,b):return [[sum((a[i][k]*b[k][j] for k in range(len(b))),F(0)) for j in range(len(b[0]))] for i in range(len(a))]
def sub(a,b):return [[a[i][j]-b[i][j] for j in range(len(a[0]))] for i in range(len(a))]
def rank(a):
    a=[list(r) for r in a];row=0
    for c in range(len(a[0])):
        pivot=next((r for r in range(row,len(a)) if a[r][c]),None)
        if pivot is None:continue
        a[row],a[pivot]=a[pivot],a[row];z=a[row][c];a[row]=[v/z for v in a[row]]
        for r in range(len(a)):
            if r!=row:
                z=a[r][c];a[r]=[a[r][j]-z*a[row][j] for j in range(len(a[0]))]
        row+=1
        if row==len(a):break
    return row
def stringify(a):return [[str(v) for v in row] for row in a]
def unit(i,j):return [[F(int((r,c)==(i,j))) for c in range(3)] for r in range(3)]
def run():
    symmetry=[[F(1),F(0),F(0)],[F(0),F(1),F(0)],[F(0),F(0),F(-1)]]
    a=[[F(1),F(2),F(3)],[F(4),F(5),F(6)],[F(7),F(8),F(9)]]
    conjugate=mm(mm(symmetry,a),symmetry)
    twirl=[[(a[i][j]+conjugate[i][j])/2 for j in range(3)] for i in range(3)]
    need(mm(symmetry,twirl)==mm(twirl,symmetry),'twirled operator invariant')
    need(sum(v*v for row in twirl for v in row)<=sum(v*v for row in a for v in row),'finite averaging norm sanity')
    basis=[unit(0,0),unit(0,1),unit(1,0),unit(1,1),unit(2,2)]
    vectors=[[m[r][0] for r in range(3)] for m in basis]
    gram=[[sum((x*y for x,y in zip(u,v)),F(0)) for v in vectors] for u in vectors]
    cyclic_rank=rank(gram)
    need(cyclic_rank==2 and cyclic_rank<3,'physical/full equality control')
    need(symmetry[2][2]==-1,'charged vector not invariant')
    ground=F(-2)
    h=[[ground,F(0),F(0)],[F(0),F(1),F(0)],[F(0),F(0),F(0)]]
    projector=[[F(1),F(0),F(0)],[F(0),F(1),F(0)],[F(0),F(0),F(0)]]
    need(mm(h,projector)==mm(projector,h),'physical subspace reducing')
    restricted=[[h[i][j]-ground*F(i==j) for j in range(2)] for i in range(2)]
    need(restricted==[[F(0),F(0)],[F(0),F(3)]],'canonical ground-energy shift')
    need(h[0][0]!=0,'wrong shift must fail to fix vacuum vector')
    mixed=[[F(1),F(0),F(0)],[F(0),F(1,2),F(1,2)],[F(0),F(1,2),F(1,2)]]
    defect=sub(mm(h,mixed),mm(mixed,h))
    need(any(v for row in defect for v in row),'nonreducing compression control')
    imaginary=[]
    for n in range(5):
        actual=F(1,4)*F(1,2)**(3*n)
        upper=F(1,4)*F(1,2)**(2*n)
        need(0<actual<=upper,'imaginary-time spectral bound')
        imaginary.append({'time_over_hbar':f'{n}*log(2)','actual_connected_correlator':str(actual),
                          'upper_bound_using_full_gap_2':str(upper)})
    return {'schema':'ym21-reverse-j2-v1','loop':'j2','direction':'reverse','passed':True,
      'target_verdict':'physical_cyclic_invariant_equality_and_restricted_generator_verified',
      'comparison':{'physical_cyclic_equals_invariant':True,'physical_equals_full':False,
        'gap_lower_alpha':'973/8640','generator_ground_energy_subtracted':True,
        'real_time_exponential_decay_implied':False},
      'symmetry_fixture':{'group':'Z2 finite illustration, not replacement for SU2 proof',
        'unitary':stringify(symmetry),'operator':stringify(a),'twirl':stringify(twirl),
        'invariant_dimension':2,'full_dimension':3,'physical_GNS_Gram':stringify(gram),
        'physical_GNS_rank':cyclic_rank,'physical_GNS_null_dimension':len(basis)-cyclic_rank},
      'generator_fixture':{'H':stringify(h),'ground_energy':str(ground),
        'physical_restricted_H_minus_e':stringify(restricted),
        'nonreducing_projector':stringify(mixed),'commutator_defect':stringify(defect)},
      'correlator_fixture':{'observable':'one-half times E01+E10','variance':'1/4',
        'physical_excitation_energy':'3','imaginary_time':imaginary,
        'real_time_return':'At t/hbar=2*pi/3, connected correlator is exactly 1/4, so positive-gap real-time decay is not implied.'},
      'infinite_statement':{'averaging':'finite endpoint SU(2) product Haar integral in weak/strong operator topology',
        'support':'same finite union of reference-factor link sets',
        'norm_contraction':True,'domain':'D(H) intersect K_phys',
        'physical_generator':'(H-e) restricted to K_phys=H_inv',
        'correlator':'0<C_W(t)<=Var_Psi(W) exp(-973 alpha t/(8640 hbar)) for each finite t>=0',
        'scope':'J1 dyadic summable representation only'},
      'controls':{'full_space_equality_rejected':True,'wrong_ground_shift_rejected':True,
        'nonreducing_compression_rejected':True,'real_time_decay_inference_rejected':True,
        'operator_norm_continuity_not_assumed':True}}
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    files=[HERE/'check.py',HERE/'report.md',ROOT/'research/round21/contracts/j2.json',
      ROOT/'research/round21/advisor/j1-gate.json',ROOT/'research/round21/reverse/j1/report.md',
      ROOT/'research/round20/reverse/g2/report.md',ROOT/'research/round19/forward/a2/report.md']
    need(all(p.is_file() for p in files),'bound source absent')
    before={str(p.relative_to(ROOT)):digest(p) for p in files}
    c=json.loads((ROOT/'research/round21/contracts/j2.json').read_text())
    need(c['loop']=='j2' and c['status']=='frozen','J2 contract not frozen')
    need(digest(ROOT/c['depends_on']['gate'])==c['depends_on']['sha256'],'J1 gate mismatch')
    result=run();need(before=={str(p.relative_to(ROOT)):digest(p) for p in files},'source changed')
    result['source_bindings']=before
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    (out/'results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    (out/'source-manifest.json').write_text(json.dumps({'schema':'ym21-source-bindings-v1','inputs':before,
      'outputs':{'results.json':digest(out/'results.json')}},indent=2,sort_keys=True)+'\n')
    print(json.dumps({'passed':result['passed'],'comparison':result['comparison'],'output':str(out)}))
if __name__=='__main__':main()
