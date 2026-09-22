#!/usr/bin/env python3
"""Geometry and exact constants for the all-time Gaussian locality proof."""
import argparse,hashlib,itertools,json,math
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
def require(c,m):
    if not c:raise ValueError(m)
def star(c):return {c,*[tuple(c[j]+(j==a) for j in range(3)) for a in range(3)]}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);out=Path(ap.parse_args().output);require(not out.exists(),'fresh output')
    Y=star((0,0,0));geometry=[]
    for R in range(5):
        C={v for v in itertools.product(range(2*R+2),repeat=3) if sum(v)<=2*R+1};require(len(C)==math.comb(2*R+4,3),'exact collar volume')
        require(Y<=C,'source retained');diam=max(sum(abs(x-y) for x,y in zip(a,b)) for a in C for b in C);require(diam==4*R+2,'collar diameter')
        geometry.append({'R':R,'sites':len(C),'diameter':diam})
    S=star((3,3,3));anchors=[c for c in itertools.product(range(2,5),repeat=3) if star(c)&S];require(len(anchors)==13<=16,'complete interior star adjacency')
    # Every successive intersecting star can add at most two units of l1 radius.
    require(all(max(sum(abs(x-y) for x,y in zip(a,b)) for a in star(c) for b in star(c))==2 for c in anchors),'actual star diameter')
    m=F(35,1664);s=F(4);expo=(64*m*s)**2/2;require(expo==F(2450,169)<F(44,3),'Gaussian cap exponent')
    x=F(2,3);n=30;partial=sum((x**k/F(math.factorial(k)) for k in range(n+1)),F(0));first=x**(n+1)/math.factorial(n+1);upper=partial+first/(1-x/(n+2));require(upper<2,'rigorous exp(2/3)<2')
    R=64;error=F(1,2**(R-22));require(error==F(1,2**42) and math.comb(2*R+4,3)==374660,'regional size/error')
    # Witness that cardinality exponential exponents eventually beat any fixed
    # linear radius decay; exact polynomial growth, not an actual divergence claim.
    require(math.comb(2*20+4,3)>20**3,'cubic support growth')
    contract=json.loads((ROOT/'research/round26/contracts/ae1.json').read_text());paths=['research/round26/contracts/ae1.json',*contract['bindings'],str(HERE.relative_to(ROOT)/'report.md'),str(HERE.relative_to(ROOT)/'check.py')]
    bindings={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sorted(set(paths))}
    for p,digest in contract['bindings'].items():require(bindings[p]==digest,'dependency binding '+p)
    result={'schema':'ym26-forward-ae1-v1','geometry':geometry,'star_overlap_bound':16,'all_time_error':'r*sum_{m>=R+1}(32M|t|)^m/m!','gaussian_error':'r*2^(-R)*exp((64Ms)^2/2)','example':{'M':str(m),'s':str(s),'R':R,'sites':374660,'relative_error_upper':str(error)},'controls':{'onsite_generator_not_bounded':True,'full_Gaussian_time_support':True,'diameter_weight_summable':'nu<log(2)/4','cardinality_weight_not_proved':True,'failed_majorant_not_actual_divergence':True,'zero_coupling_actual_source_zero':True},'external_sources':[{'url':'https://arxiv.org/pdf/1410.8174','read':'Theorem3.1 proof Eq71-73 and Theorem4.1 proof','use':'unbounded-onsite interaction-picture commutator framework; constants derived here'}],'bindings':bindings}
    out.mkdir(parents=True);(out/'results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
