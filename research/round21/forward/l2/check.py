#!/usr/bin/env python3
"""Exact finite-slope nullspace and positive hidden-mobility fixture."""
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


def uniform_moment(n):
    return F(0) if n%2 else F(1,n+1)


def mul(a,b):
    out=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            out[i+j]+=x*y
    return out


def integral(p,law=moment):
    return sum((x*law(i) for i,x in enumerate(p)),F(0))


def weight(p):
    derivative=[i*p[i] for i in range(1,len(p))]
    return mul([F(1,4),F(0),F(-1,4)],mul(derivative,derivative))


def null_vector(matrix):
    a=[list(row) for row in matrix]
    columns=len(a[0])
    pivots=[]
    r=0
    for col in range(columns):
        pivot=next((i for i in range(r,len(a)) if a[i][col]),None)
        if pivot is None:
            continue
        a[r],a[pivot]=a[pivot],a[r]
        value=a[r][col]
        a[r]=[x/value for x in a[r]]
        for i in range(len(a)):
            if i!=r:
                value=a[i][col]
                a[i]=[x-value*y for x,y in zip(a[i],a[r])]
        pivots.append(col)
        r+=1
        if r==len(a):
            break
    free=next((i for i in range(columns) if i not in pivots),None)
    need(free is not None,"no finite-dimensional nullspace")
    v=[F(0)]*columns
    v[free]=F(1)
    for i,p in enumerate(pivots):
        v[p]=-a[i][free]
    need(any(v),"zero null vector")
    need(all(sum((x*y for x,y in zip(row,v)),F(0))==0 for row in matrix),"nullspace residual nonzero")
    norm_bound=sum(abs(x) for x in v)
    need(norm_bound>0,"zero normalization")
    return [x/norm_bound for x in v],len(pivots)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,default=HERE/"output")
    args=parser.parse_args()
    sources=[HERE/"check.py",HERE/"report.md",ROOT/"research/round21/contracts/l2.json",
             ROOT/"research/round21/advisor/l1-gate.json",ROOT/"research/round21/forward/l1/report.md",
             ROOT/"research/round21/forward/k1/report.md",ROOT/"research/round21/forward/k2/report.md"]
    inputs={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    contract=json.loads((ROOT/"research/round21/contracts/l2.json").read_text())
    need(contract["depends_on"]["sha256"]==inputs["research/round21/advisor/l1-gate.json"],"L1 gate mismatch")
    observables=[[F(0),F(1)],[F(0),F(1),F(1,4)],[F(0),F(0),F(1),F(1)]]
    weights=[weight(p) for p in observables]
    matrix=[[integral([F(0)]*k+w) for k in range(4)] for w in weights]
    null,rank=null_vector(matrix)
    need(sum(abs(x) for x in null)==1,"coefficient normalization failed")
    need(all(integral(mul(null,w))==0 for w in weights),"normalized null direction is not blind")
    p5=[F(0),F(1,8),F(0),F(-5,6),F(0),F(1)]
    zeros=[integral(mul(p5,w)) for w in weights]
    need(zeros==[0,0,0],"p5 changes an L1 initial slope")
    norm_bound=sum(abs(x) for x in p5)
    floor=1-F(1,4)*norm_bound
    need(norm_bound==F(47,24) and floor==F(49,96)>0,"p5 positive mobility fixture failed")
    epsilon=F(1,4)
    operator_residual=-epsilon*p5[1]/4
    need(operator_residual==F(-1,128) and operator_residual!=0,"generator-change witness vanished")
    derivative=[i*p5[i] for i in range(1,len(p5))]
    kinetic_piece=mul([F(0),F(3,4)],p5)
    drift_piece=mul([F(1,4),F(0),F(-1,4)],derivative)
    t_polynomial=[a-b for a,b in zip(kinetic_piece,drift_piece)]
    need(t_polynomial==[F(-1,32),F(0),F(3,4),F(0),F(-5,2),F(0),F(2)],"full generator-difference polynomial wrong")
    cross=integral([F(0)]+t_polynomial)
    curvature_coefficient=integral(mul(t_polynomial,t_polynomial))
    need(cross==0 and curvature_coefficient==F(1,1024),"second-curvature scope control failed")
    classical=[F(0)]*6
    for ell in range(3):
        poch=math.prod(range(2,2+5-ell))
        degree=5-2*ell
        classical[degree]+=F((-1)**ell*poch*2**degree,math.factorial(ell)*math.factorial(degree))
    need([x/192 for x in classical]==p5,"NIST classical polynomial identity failed")
    wrong=list(p5)
    wrong[1]=F(1,9)
    wrong_residuals=[integral(mul(wrong,w)) for w in weights]
    need(any(wrong_residuals),"wrong-polynomial control failed to discriminate")
    wrong_measure=[integral(mul(p5,w),uniform_moment) for w in weights]
    need(any(wrong_measure),"wrong marginal integration control failed to discriminate")
    controls={"wrong_polynomial_coefficient":{"replacement_x_coefficient":"1/9","rate_residuals":[str(x) for x in wrong_residuals],"rejected":True},
              "uniform_interval_instead_of_Haar":{"rate_residuals":[str(x) for x in wrong_measure],"rejected":True},
              "same_slopes_same_generator":{"epsilon":str(epsilon),"operator_difference_on_x_at_zero":str(operator_residual),"rejected":True},
              "complete_time_curves_underdetermined":{"claimed":False,"reason":"the theorem concerns finitely many initial slopes only; explicit x curvature changes",
                                                        "curvature_change_in_c_squared_epsilon_squared_over_hbar_squared":str(curvature_coefficient)},
              "new_Gegenbauer_family":{"claimed":False,"classical_scale":"192"}}
    result={"schema":"ym21-forward-l2-v1","loop":"l2","direction":"forward","status":"constructive_finite_initial_slope_mobility_obstruction_verified",
            "comparison":{"blind_polynomial":"x^5-5x^3/6+x/8","three_rate_null_vector":True,"mobility_floor_fixture":str(floor),
                          "finite_slope_general_obstruction":True,"complete_time_curve_obstruction_claimed":False,"classical_gegenbauer_scale":"192"},
            "finite_nullspace_instance":{"matrix":[[str(x) for x in row] for row in matrix],"rank":rank,
                                         "normalized_polynomial_coefficients":[str(x) for x in null],"coefficient_absolute_sum":"1",
                                         "three_exact_rate_residuals":["0","0","0"]},
            "p5_fixture":{"coefficients":[str(x) for x in p5],"three_rate_residuals":[str(x) for x in zeros],
                          "sup_norm_upper":str(norm_bound),"epsilon_absolute_max":"1/4","operator_residual_at_epsilon_quarter":str(operator_residual)},
            "full_time_curve_scope_control":{"T_coefficients":[str(x) for x in t_polynomial],"E_x_T":str(cross),"E_T_squared":str(curvature_coefficient),
                                             "C_x_second_derivative_in_c_squared_over_hbar_squared":"9/64+epsilon^2/1024","complete_x_curve_preserved":False},
            "classical_source":{"url":"https://dlmf.nist.gov/18.5.E10","C5_lambda2_coefficients":[str(x) for x in classical]},
            "scope":{"general_density":"fixed smooth strictly positive conditional density","c_fixed":True,
                     "observations":"finite initial imaginary-time slopes only","exact_moment_matrix_required":True,
                     "general_normalized_positivity_interval":"|epsilon|<=m_star/2 gives m_epsilon>=m_star/2",
                     "physical_model_matched":False,"future_goal_executed":False}}
    out=args.output.resolve()
    out.mkdir(parents=True,exist_ok=True)
    payloads={"results.json":result,"controls.json":controls}
    for name,payload in payloads.items():
        (out/name).write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n")
    need(all(hashlib.sha256(p.read_bytes()).hexdigest()==inputs[str(p.relative_to(ROOT))] for p in sources),"sources changed")
    manifest={"schema":"ym21-source-manifest-v1","inputs":inputs,
              "outputs":{n:hashlib.sha256((out/n).read_bytes()).hexdigest() for n in payloads},
              "external_source":{"url":"https://dlmf.nist.gov/18.5.E10","read":"finite sum, exact n5 lambda2 substitution"},"cache_files_admitted":False}
    (out/"source-manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result["comparison"],sort_keys=True))


if __name__=="__main__":
    main()
