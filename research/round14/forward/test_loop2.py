"""Exact producer replay, retained failures and diagnostic comparisons, loop 2."""
from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import sys
from fractions import Fraction as F
from pathlib import Path

import loop2_certificate as c

HERE=Path(__file__).resolve().parent


def run(out):
    out.mkdir(parents=True,exist_ok=True)
    checks=[]
    def gate(name,passed,**detail):
        passed=bool(passed)
        checks.append({"name":name,"status":"passed" if passed else "failed",**detail})
        if not passed:
            (out/"failure.json").write_text(json.dumps(checks,indent=2)+"\n")
            raise RuntimeError(name)
    def reject(name,call):
        try:
            call()
        except ValueError:
            gate(name,True)
        else:
            gate(name,False)
    for args,target in [((0,0,0),F(1)),((2,0,0),F(1,4)),((4,0,0),F(1,8)),
                        ((2,2,0),F(1,16)),((1,1,1),F(1,16)),((0,0,2),F(1,4)),
                        ((0,0,4),F(1,8)),((1,0,0),F(0)),((1,2,1),F(0))]:
        gate(f"exact angular Haar fixture {args}",c.haar_moment(*args)==target)
    for a,b,k in ((1,1,0),(0,0,0),(2,0,0)):
        c.haar_moment(a,b,k)
    for args in ((True,1,0),(1,True,0),(0,0,False)):
        reject(f"Boolean remains rejected after cache warmup {args}",lambda a=args:c.haar_moment(*a))
    for args in ((-1,0,0),(1.0,0,0),(0,0,51),(25,25,1)):
        reject(f"invalid Haar exponents {args}",lambda a=args:c.haar_moment(*a))
    for bad in (True,1.0,float("nan"),float("inf"),"NaN","1/0",None,9):
        reject(f"invalid exact parameter {type(bad).__name__} {bad}",lambda b=bad:c.certify(b,0,0,24))
    reject("parameter total exceeds domain",lambda:c.certify(8,8,0,24))
    for bad in (True,-1,49,4.0,"4",None):
        reject(f"invalid Taylor degree {bad}",lambda b=bad:c.certify(0,0,0,b))
    reject("strict tail boundary M=N+2",lambda:c.certify(1,1,0,0))
    reject("tail ratio above one",lambda:c.certify(2,1,0,0))
    reject("negative exponent bound",lambda:c.exponential_tail(-1,4))
    for denominator in ((0,1),(-1,1),(-2,-1),(2,1)):
        reject(f"invalid denominator {denominator}",lambda d=denominator:c.interval_div_positive((-1,1),d))
    reject("Boolean interval endpoint",lambda:c.interval_mul((False,1),(1,2)))
    reject("floating interval endpoint",lambda:c.interval_mul((0.0,1),(1,2)))
    reject("reversed numerator interval",lambda:c.interval_div_positive((2,1),(1,2)))
    gate("integer reciprocal remains rational",c.interval_div_positive((1,2),(2,3))==(F(1,3),F(1)) and
         all(type(v) is F for v in c.interval_div_positive((1,2),(2,3))))
    for a,b,target in [((-2,-1),(-3,-2),(F(2),F(6))),((-2,1),(-3,2),(F(-4),F(6))),
                       ((1,2),(-3,-2),(F(-6),F(-2))),((0,0),(-3,2),(F(0),F(0)))]:
        gate(f"signed interval multiplication {a,b}",c.interval_mul(a,b)==target)

    fixtures=[("zero_degree0",(0,0,0),0),
              ("factorized_positive",(1,2,0),24),("factorized_signed",(1,-2,0),24),
              ("factorized_double_negative",(-1,-2,0),24),
              ("special_positive",(0,0,1),24),("special_negative",(0,0,-1),24),
              ("special_five",(0,0,5),32),("special_minus_five",(0,0,-5),32)]
    fixtures.extend((f"central_N{n}",(1,1,"1/4"),n) for n in (4,8,12,16,24,32))
    fixtures.extend([("small_positive",(1,1,"1/1024"),24),("small_negative",(1,1,"-1/1024"),24),
                     ("negative_eta",(1,1,"-1/4"),24),("center_flip",(-1,1,"-1/4"),24),
                     ("double_center_flip",(-1,-1,"1/4"),24),("signed_mixed",(2,-1,"1/2"),24),
                     ("conditional_h_zero",(0,1,1),24),("max_single_parameter",(8,0,0),48),
                     ("max_total_parameter",(8,4,0),48)])
    certs=[];summary=[]
    for name,parameters,degree in fixtures:
        certificate=c.certify(*parameters,degree)
        gate(f"exact complete certificate replay {name}",c.verify(certificate))
        lo,hi=map(F,certificate["enclosures"]["covariance"])
        gate(f"ordered covariance and positive denominator {name}",lo<=hi and
             F(certificate["enclosures"]["denominator"][0])>=1)
        certs.append({"id":name,"certificate":certificate})
        summary.append({"id":name,"k1":str(parameters[0]),"k2":str(parameters[1]),"eta":str(parameters[2]),
                        "degree":degree,"status":certificate["status"],"lower":str(lo),"upper":str(hi),
                        "width":str(hi-lo),"lower_display":float(lo),"upper_display":float(hi),
                        "width_display":float(hi-lo),"interpretation":"exact endpoints; display fields are rounded"})
    byid={entry["id"]:entry["certificate"] for entry in certs}
    gate("central degree24 meets requested exact width",F(byid["central_N24"]["width"])<=F(1,10**12) and
         byid["central_N24"]["status"]=="certified-positive")
    gate("central degree32 strictly improves exact width",F(byid["central_N32"]["width"])<F(byid["central_N24"]["width"]))
    gate("inadequate degree4 is retained as inconclusive",byid["central_N4"]["status"]=="certified-enclosure-inconclusive")
    gate("zero action degree0 is exactly zero",byid["zero_degree0"]["enclosures"]["covariance"]==["0","0"] and
         byid["zero_degree0"]["status"]=="certified-zero")
    for name in ("factorized_positive","factorized_signed","factorized_double_negative","max_single_parameter","max_total_parameter"):
        lo,hi=map(F,byid[name]["enclosures"]["covariance"])
        gate(f"factorization zero is enclosed without analytic override {name}",lo<=0<=hi and
             byid[name]["status"]=="certified-enclosure-inconclusive")
    for plus,minus in (("special_positive","special_negative"),("special_five","special_minus_five"),("central_N24","center_flip")):
        a,b=byid[plus]["enclosures"]["covariance"],byid[minus]["enclosures"]["covariance"]
        gate(f"exact center-sign interval reflection {plus,minus}",tuple(map(F,a))==(-F(b[1]),-F(b[0])))
    gate("double center leaves covariance unchanged",byid["central_N24"]["enclosures"]["covariance"]==
         byid["double_center_flip"]["enclosures"]["covariance"])
    gate("small positive and negative signs resolved",byid["small_positive"]["status"]=="certified-positive" and
         byid["small_negative"]["status"]=="certified-negative")
    gate("wrong factorization zero rigorously excluded at central point",F(byid["central_N24"]["enclosures"]["covariance"][0])>0)

    mutations=[("empty object",lambda q:q.clear()),("unknown field",lambda q:q.update(extra=True)),
               ("wrong source",lambda q:q.update(source_sha256="0"*64)),
               ("wrong target scope",lambda q:q["scope"].update(observable="mass gap")),
               ("undeclared parameter",lambda q:q["parameters"].update(eta="0")),
               ("noncanonical parameter",lambda q:q["parameters"].update(k1="1/1")),
               ("float parameter",lambda q:q["parameters"].update(k1=1.0)),
               ("Boolean degree",lambda q:q.update(degree=True)),
               ("false tail",lambda q:q["tail"].update(remainder="0")),
               ("false ratio",lambda q:q["tail"].update(ratio_bound="0")),
               ("omitted normalization",lambda q:q["polynomial_integrals"].pop("Z")),
               ("wrong Haar integral",lambda q:q["polynomial_integrals"].update(Axy="0")),
               ("negative denominator",lambda q:q["enclosures"].update(denominator=["-1","-1"])),
               ("zero denominator",lambda q:q["enclosures"].update(denominator=["0","0"])),
               ("false zero covariance",lambda q:q["enclosures"].update(covariance=["0","0"])),
               ("reversed covariance",lambda q:q["enclosures"]["covariance"].reverse()),
               ("missing numerator",lambda q:q["enclosures"].pop("numerator")),
               ("wrong width",lambda q:q.update(width="0")),
               ("false status",lambda q:q.update(status="certified-zero")),
               ("tuple instead of JSON array",lambda q:q["enclosures"].update(covariance=tuple(q["enclosures"]["covariance"])))]
    for name,mutate in mutations:
        q=copy.deepcopy(byid["central_N24"]);mutate(q)
        reject(f"certificate mutation {name}",lambda v=q:c.verify(v))
    for value in (True,1.0):
        q=copy.deepcopy(byid["zero_degree0"]);q["tail"]["first_omitted_degree"]=value
        reject(f"nested integer type mutation {type(value).__name__}",lambda v=q:c.verify(v))
    q=copy.deepcopy(byid["central_N4"]);q["status"]="certified-positive"
    reject("inadequate degree cannot be promoted by status",lambda:c.verify(q))

    # Floating values are diagnostic distances only. A tiny exact interval can
    # legitimately fail to contain a rounded quadrature value.
    from forward_model import marginal_moments,direct_moments
    numerical=[]
    for name in ("central_N24","central_N32","negative_eta","signed_mixed","conditional_h_zero"):
        cert=byid[name];p=[float(F(cert["parameters"][k])) for k in ("k1","k2","eta")]
        lo,hi=map(F,cert["enclosures"]["covariance"])
        one=marginal_moments(*p,128)["cov_xy"];three=direct_moments(*p,96)["cov_xy"]
        nearest=F.from_float(one)
        row={"id":name,"covariance_1d":one,"covariance_3d":three,
             "difference_between_floating_methods":abs(one-three),
             "distance_of_1d_to_exact_midpoint":float(abs(nearest-(lo+hi)/2)),
             "float_1d_inside_exact_interval":lo<=nearest<=hi,
             "interpretation":"floating containment is recorded, never an exact proof gate"}
        numerical.append(row)
        gate(f"separate numerical comparison {name}",abs(one-three)<5e-12,
             floating_difference=abs(one-three))
    gate("producer bytes still match frozen run",hashlib.sha256(c.SOURCE_PATH.read_bytes()).hexdigest()==c.SOURCE_SHA256)
    report={"schema":"ym14-loop2-producer-results-v1","status":"passed","check_count":len(checks),"checks":checks,
            "source_sha256":c.SOURCE_SHA256,"test_source_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "certificate_count":len(certs),"central_degree24_width":byid["central_N24"]["width"],
            "central_degree32_width":byid["central_N32"]["width"],
            "not_claimed":["formal proof-assistant verification","Hamiltonian gap","four-dimensional continuum solution"],
            "numerical_diagnostics":numerical}
    collection={"schema":"ym14-two-loop-certificate-collection-v1","producer_source_sha256":c.SOURCE_SHA256,
                "certificates":certs,"status":"all-certificates-replayed"}
    (out/"certificates.json").write_text(json.dumps(collection,indent=2,allow_nan=False)+"\n")
    (out/"results.json").write_text(json.dumps(report,indent=2,allow_nan=False)+"\n")
    for filename,rows in (("certificate_summary.csv",summary),("floating_diagnostics.csv",numerical)):
        with (out/filename).open("w",newline="") as f:
            writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    print(json.dumps({k:report[k] for k in ("status","check_count","certificate_count","source_sha256")}))


if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--output",type=Path,default=HERE/"loop2_output")
    run(parser.parse_args().output)
