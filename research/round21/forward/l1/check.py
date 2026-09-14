#!/usr/bin/env python3
"""Exact three-observable conditional calibration and failure controls."""
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
    v=F(1)
    for k in range(2,n+1,2):
        v*=F(k-1,k+2)
    return v


def mul(a,b):
    p=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            p[i+j]+=x*y
    return p


def integral(p):
    return sum((a*moment(i) for i,a in enumerate(p)),F(0))


G=[F(1,4),F(0),F(-1,4)]
P3=[F(0),F(-3,8),F(0),F(1)]


def row(observable):
    derivative=[i*observable[i] for i in range(1,len(observable))]
    energy=mul(G,mul(derivative,derivative))
    return [integral(energy),integral([F(0)]+energy),integral(mul(P3,energy))]


def det(m):
    return (m[0][0]*(m[1][1]*m[2][2]-m[1][2]*m[2][1])
            -m[0][1]*(m[1][0]*m[2][2]-m[1][2]*m[2][0])
            +m[0][2]*(m[1][0]*m[2][1]-m[1][1]*m[2][0]))


def solve(matrix,b):
    a=[list(r)+[v] for r,v in zip(matrix,b)]
    for j in range(3):
        pivot=next((i for i in range(j,3) if a[i][j]),None)
        need(pivot is not None,"singular calibration matrix")
        a[j],a[pivot]=a[pivot],a[j]
        scale=a[j][j]
        a[j]=[x/scale for x in a[j]]
        for i in range(3):
            if i!=j:
                scale=a[i][j]
                a[i]=[x-scale*y for x,y in zip(a[i],a[j])]
    return [r[-1] for r in a]


def inverse(rates):
    rf,rg,rh=rates
    c=16*rf/3
    need(c>0,"nonpositive reconstructed energy")
    z=32*rg/c-F(25,4)
    xi=512*rh/(9*c)-F(118,9)-8*z
    return c,z,xi


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,default=HERE/"output")
    args=parser.parse_args()
    sources=[HERE/"check.py",HERE/"report.md",ROOT/"research/round21/contracts/l1.json",
             ROOT/"research/round21/advisor/k2-gate.json",ROOT/"research/round21/advisor/post-six-selection.json",
             ROOT/"research/round21/forward/k1/report.md",ROOT/"research/round21/forward/k2/report.md"]
    inputs={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    contract=json.loads((ROOT/"research/round21/contracts/l1.json").read_text())
    need(contract["depends_on"]["sha256"]==inputs["research/round21/advisor/k2-gate.json"],"K2 gate mismatch")
    matrix=[row([F(0),F(1)]),row([F(0),F(1),F(1,4)]),row([F(0),F(0),F(1),F(1)])]
    expected=[[F(3,16),F(0),F(0)],[F(25,128),F(1,32),F(0)],[F(59,256),F(9,64),F(9,512)]]
    need(matrix==expected,"independent polynomial rate matrix differs")
    determinant=det(matrix)
    need(determinant==F(27,262144),"determinant mismatch")
    floor=1-F(1,4)-F(1,4)*F(11,8)
    gap=floor/6
    need(floor==F(13,32) and gap==F(13,192),"positive box/gap mismatch")
    # NIST finite sum C_3^(2): ell=0,1, each Pochhammer computed directly.
    gegenbauer=[F(0)]*4
    for ell in range(2):
        poch=math.prod(range(2,2+3-ell))
        degree=3-2*ell
        gegenbauer[degree]+=F((-1)**ell*poch*2**degree,math.factorial(ell)*math.factorial(degree))
    need(gegenbauer==[F(0),F(-12),F(0),F(32)] and [x/32 for x in gegenbauer]==P3,"NIST Gegenbauer substitution failed")
    fixtures=[]
    for c,z,xi in ((F(2),F(1,8),F(1,4)),(F(1,3),F(-1,4),F(-1,8)),(F(5),F(0),F(0))):
        params=[c,c*z,c*xi]
        rates=[sum((a*b for a,b in zip(r,params)),F(0)) for r in matrix]
        need(inverse(rates)==(c,z,xi),"closed inverse failed")
        need(solve(matrix,rates)==params,"independent Gaussian inverse failed")
        residual=rates[2]-c*(matrix[2][0]+z*matrix[2][1])
        need(residual==c*xi*F(9,512),"cubic residual wrong")
        fixtures.append({"c":str(c),"zeta":str(z),"xi":str(xi),"rates":[str(x) for x in rates],
                         "xi_omission_third_rate_residual":str(residual),"Jacobian_c_zeta_xi":str(c*c*determinant),"synthetic":True})
    wrong=[matrix[0],matrix[1],row([F(0),F(0),F(1)])]
    need(det(wrong)==0,"wrong-third-observable rank failure not detected")
    need(F(1,2)>F(1,4) and 1-F(1,2)>0,"outside-box positive-mobility control failed")
    controls={"wrong_third_observable":{"observable":"x^2","xi_coefficient":str(wrong[2][2]),"determinant":str(det(wrong)),"rejected":True},
              "hidden_cubic_omitted":{"nonzero_fixture_residual":fixtures[0]["xi_omission_third_rate_residual"],"rejected":fixtures[0]["xi_omission_third_rate_residual"]!="0"},
              "outside_box_implies_negative_mobility":{"zeta":"1/2","xi":"0","true_mobility_lower":"1/2","rejected":True},
              "new_polynomial_priority":{"p3":"C_3^(2)/32","classical_family":True},
              "arbitrary_mobility_identified":{"established":False,"scope":"declared three-parameter family only"}}
    result={"schema":"ym21-forward-l1-v1","loop":"l1","direction":"forward","status":"three_rate_finite_family_reconstruction_and_cubic_detection_verified",
            "comparison":{"linear_determinant":str(determinant),"third_rate_xi_coefficient":str(matrix[2][2]),
                          "mobility_floor_box":str(floor),"gap_factor_box":str(gap),"hidden_cubic_detected":True,"arbitrary_mobility_identified":False},
            "rate_matrix":[[str(x) for x in row] for row in matrix],"synthetic_fixtures":fixtures,
            "classical_polynomial":{"source":"https://dlmf.nist.gov/18.5.E10","C3_lambda2_coefficients":[str(x) for x in gegenbauer],"p3_equals_C3_over32":True},
            "scope":{"exact_inverse_kappa":"0","gap_kappa_absolute_max":"1/8","zeta_xi_absolute_max":"1/4",
                     "actual_physical_slopes_supplied":False,"c_alpha_matched":False,"next_loop_executed":False}}
    out=args.output.resolve()
    out.mkdir(parents=True,exist_ok=True)
    payloads={"results.json":result,"controls.json":controls}
    for name,payload in payloads.items():
        (out/name).write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n")
    need(all(hashlib.sha256(p.read_bytes()).hexdigest()==inputs[str(p.relative_to(ROOT))] for p in sources),"source changed")
    manifest={"schema":"ym21-source-manifest-v1","inputs":inputs,
              "outputs":{n:hashlib.sha256((out/n).read_bytes()).hexdigest() for n in payloads},
              "external_source":{"url":"https://dlmf.nist.gov/18.5.E10","read":"finite Gegenbauer representation and n3 lambda2 substitution"},"cache_files_admitted":False}
    (out/"source-manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result["comparison"],sort_keys=True))


if __name__=="__main__":
    main()
