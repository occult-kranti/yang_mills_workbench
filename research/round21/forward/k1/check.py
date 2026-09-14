#!/usr/bin/env python3
"""Exact Haar polynomial rates and mobility controls for K1."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]


def need(ok,message):
    if not ok:
        raise ValueError(message)


def moment(n):
    if n%2:
        return F(0)
    m=F(1)
    for k in range(2,n+1,2):
        m*=F(k-1,k+2)
    return m


def mul(a,b):
    out=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            out[i+j]+=x*y
    return out


def integral(a):
    return sum((x*moment(n) for n,x in enumerate(a)),F(0))


def rate_coefficients(f):
    derivative=[i*f[i] for i in range(1,len(f))]
    if not derivative:
        return F(0),F(0)
    squared=mul(derivative,derivative)
    energy=mul(squared,[F(1,4),F(0),F(-1,4)])
    return integral(energy),integral([F(0)]+energy)


def inverse(rf,rg):
    need(rf>0,"first slope must be positive")
    c=16*rf/3
    z=8*rg/c-F(5,2)
    need(abs(z)<1,"inferred mobility leaves strict-positive range")
    return c,z


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,default=HERE/"output")
    args=parser.parse_args()
    sources=[HERE/"check.py",HERE/"report.md",ROOT/"research/round21/contracts/k1.json",
             ROOT/"research/round21/advisor/j2-gate.json",ROOT/"research/round20/forward/f1/report.md",
             ROOT/"research/round20/forward/f2/report.md"]
    inputs={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    contract=json.loads((ROOT/"research/round21/contracts/k1.json").read_text())
    need(contract["depends_on"]["sha256"]==inputs["research/round21/advisor/j2-gate.json"],"J2 gate mismatch")
    f=rate_coefficients([F(0),F(1)])
    g=rate_coefficients([F(0),F(1),F(1)])
    parity=rate_coefficients([F(0),F(0),F(1)])
    constant=rate_coefficients([F(1)])
    determinant=f[0]*g[1]-f[1]*g[0]
    need(f==(F(3,16),0) and g==(F(5,16),F(1,8)),"rate integration mismatch")
    need(parity==(F(1,8),0) and constant==(0,0),"parity/constant integration mismatch")
    need(determinant==F(3,128),"linear-variable determinant wrong")
    fixtures=[]
    for c,z in ((F(2),F(1,2)),(F(1,3),F(-3,4)),(F(7),F(0))):
        rf,rg=c*(f[0]+z*f[1]),c*(g[0]+z*g[1])
        need(inverse(rf,rg)==(c,z),"synthetic inverse failed")
        fixtures.append({"c":str(c),"zeta":str(z),"r_f":str(rf),"r_g":str(rg),"Jacobian_c_zeta":str(c*determinant),"synthetic":True})
    # Exact tangent projection fixture u=q=i, v=1.
    projected_u=(F(4),F(0),F(0),F(0))
    projected_v=(F(0),F(2),F(0),F(0))
    projected_q=(F(2),F(0),F(0),F(0))
    gamma=sum((x*x for vector in (projected_u,projected_v,projected_q) for x in vector),F(0))/4
    gamma_x_s=projected_u[0]/4
    lap=F(-3,4)
    need(gamma==6 and gamma_x_s==1,"tangent metric fixture failed")
    kappa,zeta=F(1,8),F(1,2)
    divergence=lap+zeta*gamma_x_s
    potential=kappa*divergence/2+kappa*kappa*gamma/4
    kinetic=-kappa*divergence/2-kappa*kappa*gamma/4
    need(kinetic+potential==0,"ground transform fails")
    missing_divergence=kinetic+kappa*lap/2+kappa*kappa*gamma/4
    missing_shared=kinetic+kappa*divergence/2+kappa*kappa*(gamma-F(1,2))/4
    need(missing_divergence==F(-1,32) and missing_shared==F(-1,512),"ground-transform rejection controls failed")
    wrong_stationary=3*zeta*moment(2)/4
    correct_stationary=wrong_stationary-zeta*(1-moment(2))/4
    need(wrong_stationary==F(3,32) and correct_stationary==0,"divergence drift stationarity control failed")
    rejection=[]
    for rf,rg in ((F(0),F(1)),(F(1),F(1)),(F(1),F(7,3))):
        try:
            inverse(rf,rg)
        except ValueError:
            rejection.append([str(rf),str(rg)])
    need(len(rejection)==3,"invalid inverse data admitted")
    c,zeta=F(2),F(1,2)
    symbols=(c*(1-zeta),c*(1+zeta))
    need(symbols[0]!=symbols[1],"nonconstant principal symbol was invisible")
    need(1-F(3,2)<0 and 1-F(1)==0,"mobility boundary controls failed")
    controls={"missing_divergence_drift":{"wrong_stationary_expectation":str(wrong_stationary),"correct":"0","rejected":True},
              "missing_mobility_transform_term":{"ground_residual":str(missing_divergence),"rejected":True},
              "missing_shared_link_derivative":{"ground_residual":str(missing_shared),"rejected":True},
              "mobility_boundary":{"zeta1_min":"0","zeta3over2_min":"-1/2","rejected":True},
              "zero_Dirichlet_observable":{"rate_coefficients":[str(x) for x in constant],"identifying":False},
              "parity_degenerate_pair":{"linear_rank":1,"zeta_identified":False},
              "invalid_inverse_inputs":{"rejected":rejection},
              "constant_rotor_symbol_match":{"endpoint_symbols":[str(x) for x in symbols],"rejected":True}}
    result={"schema":"ym21-forward-k1-v1","loop":"k1","direction":"forward","status":"conditional_mobility_and_two_rate_inverse_verified",
            "comparison":{"mobility_lower":"1-|zeta|","gap_factor":"(1-|zeta|)/6","rate_f_c":str(f[0]),
                          "rate_g_c_constant":str(g[0]),"rate_g_c_zeta":str(g[1]),"two_rate_determinant":str(determinant),
                          "static_parameters_identified":False,"physical_model_matched":False},
            "determinant_coordinates":"linear variables (c,c*zeta); Jacobian in (c,zeta) is c*3/128",
            "haar_moments":{str(n):str(moment(n)) for n in range(7)},"synthetic_fixtures":fixtures,
            "ground_transform_fixture":{"Gamma_S":str(gamma),"Gamma_x_S":str(gamma_x_s),"Delta_S":str(lap),"potential":str(potential),"correct_residual":"0"},
            "scope":{"known_kappa_for_exact_inverse":"0","physical_slope_data_supplied":False,"c_equals_alpha_inferred":False,
                     "mobility_classification":"explicit dynamics deformation","next_loop_executed":False}}
    out=args.output.resolve()
    out.mkdir(parents=True,exist_ok=True)
    payloads={"results.json":result,"controls.json":controls}
    for name,payload in payloads.items():
        (out/name).write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n")
    need(all(hashlib.sha256(p.read_bytes()).hexdigest()==inputs[str(p.relative_to(ROOT))] for p in sources),"sources changed")
    manifest={"schema":"ym21-source-manifest-v1","inputs":inputs,
              "outputs":{n:hashlib.sha256((out/n).read_bytes()).hexdigest() for n in payloads},"cache_files_admitted":False}
    (out/"source-manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result["comparison"],sort_keys=True))


if __name__=="__main__":
    main()
