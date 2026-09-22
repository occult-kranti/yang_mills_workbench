#!/usr/bin/env python3
"""Exact arithmetic and geometry controls; not an SU(2) spectral simulation."""
import argparse, hashlib, itertools, json
from fractions import Fraction as F
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parent
def require(ok,message):
    if not ok: raise ValueError(message)
def star(c):
    return {c,*[tuple(c[j]+int(j==i) for j in range(3)) for i in range(3)]}
def mm(a,b): return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def sub(a,b): return [[x-y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);out=Path(ap.parse_args().output)
    require(not out.exists(),'output must be fresh')
    y=star((0,0,0));geometry={}
    for side in (2,3,4):
        volume=set(itertools.product(range(side),repeat=3))
        anchors=[c for c in sorted(volume) if star(c)<=volume]
        crossing=[c for c in anchors if star(c)&y and not star(c)<=y]
        require(len(crossing)==(0 if side==2 else 3),'crossing enumeration')
        require(all(len(star(c)|y)==7 for c in crossing),'complete support size')
        geometry[str(side)]={'retained_stars':len(anchors),'crossing_anchors':crossing,'union_sizes':[len(star(c)|y) for c in crossing]}
    cap=F(5,1664);m=7*cap;ratio=6*m/(1-m)
    require(ratio==F(70,543),'cap ratio');require(ratio<F(129,1000),'cap numerical threshold')
    signs=[]
    for tau in (-cap,F(0),cap):
        sig2=F(7,12)*tau*tau
        r2_upper=F(16,9)*sig2**3
        e2_upper=(6*7*abs(tau)/(1-7*abs(tau)))**2*r2_upper
        require((r2_upper==0)==(tau==0),'zero exception')
        signs.append({'tau':str(tau),'source_norm_squared_upper':str(r2_upper),'diagonal_norm_squared_upper':str(e2_upper)})
    # Algebra-only fixture: diagonal G has a degenerate excited eigenspace.
    g=[[F(0),F(0),F(0)],[F(0),F(2),F(0)],[F(0),F(0),F(2)]]
    k=[[F(0),F(-1),F(0)],[F(1),F(0),F(0)],[F(0),F(0),F(0)]]
    a=[[F(0),F(2),F(0)],[F(2),F(0),F(1,10)],[F(0),F(1,10),F(0)]]
    comm=sub(mm(k,g),mm(g,k));e=[[comm[i][j]+a[i][j] for j in range(3)] for i in range(3)]
    energies=(0,2,2)
    require(all(a[i][j]==e[i][j] for i in range(3) for j in range(3) if energies[i]==energies[j]),'diagonal compression identity')
    require(a[1][2]!=0,'wrong zero-residual inference rejected')
    contract=json.loads((ROOT/'research/round26/contracts/ab1.json').read_text())
    paths=['research/round26/contracts/ab1.json',*contract['bindings'],'research/round23/forward/s1/report.md',str(HERE.relative_to(ROOT)/'report.md'),str(HERE.relative_to(ROOT)/'check.py')]
    bindings={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sorted(set(paths))}
    for p,digest in contract['bindings'].items():require(bindings[p]==digest,'frozen dependency mismatch '+p)
    result={'schema':'ym26-forward-ab1-v1','verdict':'limited_parent; proved_actual_diagonal_boundary_identity_and_upper_bound','geometry':geometry,'cap_diagonal_to_source_ratio':str(ratio),'sign_checks':signs,'controls':{'algebra_fixture_is_not_actual_spectrum':True,'defect_deletion_rejected':True,'strong_to_norm_promotion_not_admitted':True,'identity_exterior_required':True},'bindings':bindings}
    out.mkdir(parents=True);(out/'results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
