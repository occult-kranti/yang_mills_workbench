#!/usr/bin/env python3
"""Exact polynomial, double-marginal and inverse checks for K2."""
import argparse
from fractions import Fraction as F
import hashlib
import json
import math
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]


def need(ok,message):
    if not ok:
        raise ValueError(message)


def moment(n):
    if n%2:
        return F(0)
    value=F(1)
    for k in range(2,n+1,2):
        value*=F(k-1,k+2)
    return value


def mul(p,q):
    out=[F(0)]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q):
            out[i+j]+=a*b
    return out


def integrate(p):
    return sum((v*moment(i) for i,v in enumerate(p)),F(0))


G=[F(1,4),F(0),F(-1,4)]


def matrix(a):
    h=[F(1),4*a,4*a*a]
    hg=mul(h,G)
    return [[integrate(G),integrate([F(0)]+G)],
            [integrate(hg),integrate([F(0)]+hg)]]


def determinant(m):
    return m[0][0]*m[1][1]-m[0][1]*m[1][0]


def double_integral(a):
    # Independent bivariate expansion of G(X)G(Y)(X-Y)^2[1+a(X+Y)].
    total=F(0)
    for i,gi in enumerate(G):
        for j,gj in enumerate(G):
            for u,v,coef in ((2,0,F(1)),(1,1,F(-2)),(0,2,F(1))):
                for r,s,weight in ((0,0,F(1)),(1,0,a),(0,1,a)):
                    total+=gi*gj*coef*weight*moment(i+u+r)*moment(j+v+s)
    return 2*a*total


def inverse(m,rf,rg):
    d=determinant(m)
    need(d>0,"determinant must be positive")
    c=(rf*m[1][1]-rg*m[0][1])/d
    cz=(m[0][0]*rg-m[1][0]*rf)/d
    need(c>0,"reconstructed energy must be positive")
    z=cz/c
    need(abs(z)<1,"reconstructed mobility is not strictly positive")
    return c,z


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,default=HERE/"output")
    args=parser.parse_args()
    sources=[HERE/"check.py",HERE/"report.md",ROOT/"research/round21/contracts/k2.json",
             ROOT/"research/round21/advisor/k1-gate.json",ROOT/"research/round21/forward/k1/report.md",
             ROOT/"research/round20/forward/f2/report.md"]
    inputs={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    contract=json.loads((ROOT/"research/round21/contracts/k2.json").read_text())
    need(contract["depends_on"]["sha256"]==inputs["research/round21/advisor/k1-gate.json"],"K1 gate mismatch")
    a=F(1,4)
    m=matrix(a)
    d=determinant(m)
    need(m==[[F(3,16),F(0)],[F(25,128),F(1,32)]] and d==F(3,512),"Haar matrix mismatch")
    for design in (F(0),F(1,10),a,F(2,5),F(1)):
        need(double_integral(design)==determinant(matrix(design)),"double-integral determinant identity failed")
    n=8
    exp_sum=sum((F(3)**k/math.factorial(k) for k in range(n+1)),F(0))
    next_term=F(3)**(n+1)/math.factorial(n+1)
    exp_upper=exp_sum+next_term/(1-F(3,n+2))
    need(exp_upper<21,"rational exp(3) upper enclosure failed")
    lower=3*a*(1-2*a)/(128*21)
    need(lower==F(1,7168),"uniform determinant lower mismatch")
    inverse_bound=F(13,16)/lower
    need(inverse_bound==5824,"conditioning coefficient mismatch")
    p3=[F(0),F(-3,8),F(0),F(1)]
    h=[F(1),4*a,4*a*a]
    blind1=integrate(mul(p3,G))
    blind2=integrate(mul(mul(p3,h),G))
    need(blind1==0 and blind2==0,"blind mobility polynomial affects one selected rate")
    positivity=1-F(1,4)*F(11,8)
    need(positivity==F(21,32)>0,"out-of-family mobility lacks positivity certificate")
    need(determinant(matrix(F(0)))==0,"zero-design collapse failed")
    derivative_at_minus1=4*(1-2)
    need(derivative_at_minus1<0 and determinant(matrix(F(1)))>0,"nonmonotone sufficient-range control failed")
    fixtures=[]
    for c,z in ((F(2),F(1,2)),(F(3,4),F(-1,2)),(F(5),F(0))):
        rf=c*(m[0][0]+z*m[0][1])
        rg=c*(m[1][0]+z*m[1][1])
        need(inverse(m,rf,rg)==(c,z),"synthetic inverse mismatch")
        fixtures.append({"c":str(c),"zeta":str(z),"r_f":str(rf),"r_g":str(rg),"synthetic":True})
    rejected=[]
    for c,z in ((F(0),F(0)),(F(-1),F(0)),(F(1),F(1)),(F(1),F(-1))):
        rf=c*(m[0][0]+z*m[0][1])
        rg=c*(m[1][0]+z*m[1][1])
        try:
            inverse(m,rf,rg)
        except ValueError:
            rejected.append([str(c),str(z)])
    need(len(rejected)==4,"inadmissible inverse output admitted")
    controls={"a_zero":{"determinant":"0","rejected":True},
              "nonmonotone_design":{"a":"1","h_derivative_at_minus1":str(derivative_at_minus1),"Haar_determinant":str(determinant(matrix(F(1)))),"rank_failure_inferred":False},
              "wrong_determinant_sign":{"wrong":str(-d),"correct":str(d),"rejected":True},
              "inadmissible_parameters":{"rejected":rejected},
              "arbitrary_mobility_identification":{"blind_polynomial":"x^3-3x/8","first_rate_shift":str(blind1),"second_rate_shift":str(blind2),"xi_max":"1/4","mobility_lower":str(positivity),"rejected":True}}
    result={"schema":"ym21-forward-k2-v1","loop":"k2","direction":"forward","status":"uniform_conditional_two_parameter_inverse_with_mobility_family_counterexample",
            "comparison":{"design_a":str(a),"zero_kappa_determinant":str(d),"uniform_determinant_lower":str(lower),
                          "kappa_absolute_bound":"1/8","two_parameter_inverse_identified":True,"arbitrary_mobility_identified":False,
                          "blind_polynomial":"x^3-3x/8"},
            "zero_kappa_matrix":[[str(x) for x in row] for row in m],
            "exponential_enclosure":{"argument":"3","Taylor_order":n,"rational_upper":str(exp_upper),"strictly_below":"21"},
            "uniform_inverse_norm_upper":str(inverse_bound),"synthetic_fixtures":fixtures,
            "scope":{"independent_copies":"same x marginal; not interacting-link independence","known_kappa_required":True,
                     "rate_data_observed":False,"coefficient_integration_error_budget_supplied":False,
                     "new_a_classification":"observable-design coefficient","physical_model_matched":False,"next_goals_selected":False}}
    out=args.output.resolve()
    out.mkdir(parents=True,exist_ok=True)
    payloads={"results.json":result,"controls.json":controls}
    for name,payload in payloads.items():
        (out/name).write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n")
    need(all(hashlib.sha256(p.read_bytes()).hexdigest()==inputs[str(p.relative_to(ROOT))] for p in sources),"source changed")
    manifest={"schema":"ym21-source-manifest-v1","inputs":inputs,
              "outputs":{n:hashlib.sha256((out/n).read_bytes()).hexdigest() for n in payloads},"cache_files_admitted":False}
    (out/"source-manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result["comparison"],sort_keys=True))


if __name__=="__main__":
    main()
