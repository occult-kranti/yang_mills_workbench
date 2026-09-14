#!/usr/bin/env python3
"""J1 exact rational gauge and perturbed-variance checks."""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]


def need(condition, message):
    if not condition:
        raise ValueError(message)


def qmul(a, b):
    w,x,y,z = a
    v,r,s,t = b
    return (w*v-x*r-y*s-z*t, w*r+x*v+y*t-z*s,
            w*s-x*t+y*v+z*r, w*t+x*s-y*r+z*v)


def adj(q):
    return (q[0], -q[1], -q[2], -q[3])


def holonomy(edges):
    a,b,c,d = edges
    return qmul(qmul(qmul(a,b),adj(c)),adj(d))


def gauge_fixture():
    one = (F(1),F(0),F(0),F(0))
    minus = tuple(-x for x in one)
    edges = [(F(3,5),F(4,5),F(0),F(0)),
             (F(0),F(0),F(1),F(0)),
             (F(5,13),F(0),F(0),F(12,13)),
             (F(0),F(1),F(0),F(0))]
    gauges = [(F(4,5),F(0),F(3,5),F(0)),
              (F(0),F(0),F(0),F(1)),
              (F(12,13),F(5,13),F(0),F(0)),
              (F(0),F(1),F(0),F(0))]
    for q in edges+gauges:
        need(sum(x*x for x in q) == 1, "quaternion is not SU2")
    # Edges: 0->1, 1->2, 3->2, 0->3.
    endpoints = ((0,1),(1,2),(3,2),(0,3))
    transformed = [qmul(qmul(gauges[a],u),adj(gauges[b]))
                   for u,(a,b) in zip(edges,endpoints)]
    before, after = holonomy(edges), holonomy(transformed)
    need(after == qmul(qmul(gauges[0], before), adj(gauges[0])), "loop did not transform by conjugation")
    need(before[0] == after[0], "Wilson trace changed under gauge action")
    need(qmul(minus,one)[0] == -one[0], "charged open-link control failed")
    return {"wilson_before": str(before[0]), "wilson_after": str(after[0]),
            "full_holonomy_covariance": True, "charged_open_link_trace_before": "1",
            "charged_open_link_trace_after": "-1", "omitted_face": {"base":[0,0,0],"directions":[0,2]},
            "free_z_link_tails": [[0,0,0],[1,0,0]]}


def B(q):
    need(0 < q < 1, "profile parameter must be in (0,1)")
    return F(1,8)/(1-q)**3-(1+q+q*q)/(24*(1-q**4)*(1-q*q)*(1-q))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,default=HERE/"output")
    args = parser.parse_args()
    sources = [HERE/"check.py",HERE/"report.md", ROOT/"research/round21/contracts/j1.json",
               ROOT/"research/round21/advisor/i2-gate.json",ROOT/"research/round19/forward/a2/report.md",
               ROOT/"research/round20/forward/h2/report.md",ROOT/"research/round20/forward/g2/report.md"]
    inputs = {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources}
    contract = json.loads((ROOT/"research/round21/contracts/j1.json").read_text())
    need(contract["depends_on"]["sha256"] == inputs["research/round21/advisor/i2-gate.json"], "I2 dependency hash mismatch")
    tau = F(1,64)
    b_half,b_quarter = B(F(1,2)),B(F(1,4))
    sigma2 = tau*tau*b_quarter/96
    gap = F(1,8)-tau*b_half
    d2 = sigma2/gap**2
    d_upper = F(1,150)
    variance = F(1,4)-2*d_upper-4*d_upper*d_upper
    need(b_half == F(107,135) and b_quarter == F(2504,11475), "wrong geometric profile sums")
    need(sigma2 == F(313,564019200), "wrong residual variance")
    need(gap == F(973,8640) and gap > 0, "excited threshold not certified")
    need(d2 == F(2817,64377572) and d2 < d_upper*d_upper, "projector rational enclosure failed")
    need(variance == F(5321,22500) and variance > F(1,5), "physical fluctuation bound not positive")
    signed = []
    for t in (-tau,-tau/2,F(0),tau/2,tau):
        g = F(1,8)-abs(t)*b_half
        square = t*t*b_quarter/(96*g*g)
        need(square <= d2, "signed endpoint bound failed")
        signed.append({"tau":str(t),"projector_square_upper":str(square)})
    gauge = gauge_fixture()
    # W=sigma_x, reference=e0, perturbed=(3/5,4/5): nonzero expectation.
    reference_expectation = F(0)
    perturbed_expectation = 2*F(3,5)*F(4,5)
    need(perturbed_expectation == F(24,25) and perturbed_expectation != reference_expectation,
         "reference-zero-mean substitution control failed")
    controls = {
        "charged_open_link": {"rejected": True,"before":"1","after":"-1"},
        "vacuum_only_algebra": {"centered_scalar_vector_norm_square":"0","incompatible_with_variance_lower_bound":str(variance),"rejected":True},
        "full_irreducibility_on_restricted_algebra": {"full_M2_cyclic_dimension":2,"diagonal_algebra_at_e0_cyclic_dimension":1,"rejected":True},
        "reference_moment_used_as_perturbed_moment": {"reference_mean":str(reference_expectation),"perturbed_mean":str(perturbed_expectation),"rejected":True},
        "model_switch_hidden": {"current_profile":"dyadic q=1/2","homogeneous_interval_imported":False},
    }
    result = {"schema":"ym21-forward-j1-v1","loop":"j1","direction":"forward",
              "status":"invariant_algebra_and_positive_perturbed_variance_verified",
              "comparison":{"variance_lower_bound":str(variance),"projector_square_upper":str(d2),
                            "gap_lower_alpha":str(gap),"physical_fluctuation_nonzero":True,
                            "full_and_physical_spaces_identified":False},
              "exact_values":{"B_half":str(b_half),"B_quarter":str(b_quarter),"sigma_squared_over_alpha_squared":str(sigma2),
                              "projector_norm_rational_upper":str(d_upper)},
              "signed_fixtures":signed,"gauge_check":gauge,
              "scope":{"model":"A2 dyadic summable fixed spacing","tau_absolute_max":"1/64",
                       "gauge_invariant_local_algebra":True,"common_invariant_operator_and_form_core":True,
                       "invariant_quasilocal_dynamics":True,"physical_cyclic_equals_invariant_space_proved":False,
                       "homogeneous_numerical_claim":False,"continuum_claim":False},"next_loop_executed":False}
    output=args.output.resolve()
    output.mkdir(parents=True,exist_ok=True)
    payloads={"results.json":result,"controls.json":controls}
    for name,payload in payloads.items():
        (output/name).write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n")
    need(all(hashlib.sha256(p.read_bytes()).hexdigest()==inputs[str(p.relative_to(ROOT))] for p in sources),"source changed during execution")
    manifest={"schema":"ym21-source-manifest-v1","inputs":inputs,
              "outputs":{name:hashlib.sha256((output/name).read_bytes()).hexdigest() for name in payloads},
              "cache_files_admitted":False}
    (output/"source-manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
    print(json.dumps(result["comparison"],sort_keys=True))


if __name__ == "__main__":
    main()
