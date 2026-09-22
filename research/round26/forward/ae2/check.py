#!/usr/bin/env python3
"""Exact triangular-kernel, complete-crossing and cardinality-budget checks."""
import argparse,hashlib,itertools,json,math
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
def require(c,m):
    if not c:raise ValueError(m)
def star(c):return {c,*[tuple(c[j]+(j==a) for j in range(3)) for a in range(3)]}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);out=Path(ap.parse_args().output);require(not out.exists(),'fresh output')
    geometry=[]
    for b,expected in [((0,0,0),3),((2,2,2),12)]:
        y=star(b);cross=[c for c in itertools.product(range(5),repeat=3) if c!=b and star(c)&y];require(len(cross)==expected,'complete translated crossing count');require(all(len(y|star(c))==7 for c in cross),'complete seven-site support');geometry.append({'source':b,'crossings':cross})
    T=F(3);M=F(1,1000);ratio=(24*M+2/T)/(1-M);require(ratio==F(2072,2997)<F(7,10),'family full operator contraction')
    radius=192*M*T;require(radius==F(72,125)<1,'positive cardinality radius');weighted=64*F(125,53)**3
    require(weighted>64,'weighted upper bound is not contraction')
    moments=[]
    for n in range(12):
        p_integral=2/T*(T**(n+1)/F(n+1)-T**(n+2)/(T*(n+2)))/math.factorial(n)
        h_integral=(T**(n+1)/F(n+1)-2*T**(n+2)/(T*(n+2))+T**(n+3)/(T*T*(n+3)))/math.factorial(n)
        require(p_integral==2*T**n/math.factorial(n+2),'normalized residual kernel moment');require(h_integral==2*T**(n+1)/math.factorial(n+3),'inverse kernel moment');moments.append({'n':n,'residual':str(p_integral),'inverse':str(h_integral)})
    original=F(35,1664);lower=2/(1-25*original);upper=1/(192*original)
    require(lower==F(3328,789) and upper==F(26,105) and lower>upper,'original cap incompatible certificate')
    require(409*M<1 and 409*original>1,'continuous feasibility criterion')
    # Off-diagonal multiplier sign with arbitrary q in [0,1]; q=1 at omega0.
    for omega in (F(-2),F(0),F(2)):
        q=F(1) if not omega else F(1,4);ell=F(0) if not omega else (1-q)/omega;require(-omega*ell==-1+q,'homological sign and zero-frequency residual')
    contract=json.loads((ROOT/'research/round26/contracts/ae2.json').read_text());paths=['research/round26/contracts/ae2.json',*contract['bindings'],'research/round23/forward/s2/report.md',str(HERE.relative_to(ROOT)/'report.md'),str(HERE.relative_to(ROOT)/'check.py')]
    bindings={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sorted(set(paths))}
    for p,digest in contract['bindings'].items():require(bindings[p]==digest,'dependency binding '+p)
    result={'schema':'ym26-forward-ae2-v1','geometry':geometry,'restricted':{'M_cap':str(M),'tau_absolute_cap':'1/7000','T':str(T),'per_source_full_norm_ratio':str(ratio),'cardinality_radius':str(radius),'both_weighted_norm_upper_per_r_star':str(weighted)},'kernel_moments':moments,'original_cap':{'M':str(original),'contraction_duration_lower':str(lower),'residual_cardinality_duration_upper':str(upper),'feasible':False},'controls':{'origin_count_not_used_for_family':True,'all_order_rooted_recurrence_retained':True,'zero_frequency_residual_retained':True,'finite_weighted_norm_not_weighted_contraction':True,'zero_coupling_sources_zero':True,'failed_upper_certificate_not_dynamics_divergence':True,'inverse_endpoint_may_converge_residual_does_not':True},'bindings':bindings}
    out.mkdir(parents=True);(out/'results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
