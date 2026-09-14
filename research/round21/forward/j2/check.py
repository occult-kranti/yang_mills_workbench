#!/usr/bin/env python3
"""Exact finite symmetry and spectral controls for the scoped J2 proof."""
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


def rank(columns):
    if not columns:
        return 0
    a=[list(row) for row in zip(*columns)]
    r=0
    for j in range(len(a[0])):
        pivot=next((i for i in range(r,len(a)) if a[i][j]),None)
        if pivot is None:
            continue
        a[r],a[pivot]=a[pivot],a[r]
        v=a[r][j]
        a[r]=[x/v for x in a[r]]
        for i in range(len(a)):
            if i!=r:
                v=a[i][j]
                a[i]=[x-v*y for x,y in zip(a[i],a[r])]
        r+=1
        if r==len(a):
            break
    return r


def unit(i,j):
    a=[[F(0) for _ in range(3)] for _ in range(3)]
    a[i][j]=F(1)
    return a


def twirl(a):
    signs=(1,1,-1)
    return [[a[i][j]*F(1+signs[i]*signs[j],2) for j in range(3)] for i in range(3)]


def apply(a,v):
    return [sum((x*y for x,y in zip(row,v)),F(0)) for row in a]


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,default=HERE/"output")
    args=parser.parse_args()
    paths=[HERE/"check.py",HERE/"report.md",ROOT/"research/round21/contracts/j2.json",
           ROOT/"research/round21/advisor/j1-gate.json",ROOT/"research/round21/forward/j1/report.md",
           ROOT/"research/round20/forward/g2/report.md",ROOT/"research/round19/forward/a2/report.md"]
    inputs={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    contract=json.loads((ROOT/"research/round21/contracts/j2.json").read_text())
    need(contract["depends_on"]["sha256"]==inputs["research/round21/advisor/j1-gate.json"],"J1 gate mismatch")
    vacuum=[F(1),F(0),F(0)]
    matrix_units=[unit(i,j) for i in range(3) for j in range(3)]
    full_rank=rank([apply(a,vacuum) for a in matrix_units])
    physical_rank=rank([apply(twirl(a),vacuum) for a in matrix_units])
    need((full_rank,physical_rank)==(3,2),"GNS orbit dimensions are incorrect")
    approx=[[F(3,5),F(0),F(0)],[F(4,5),F(0),F(0)],[F(1,100),F(0),F(0)]]
    target=[F(3,5),F(4,5),F(0)]
    need(apply(twirl(approx),vacuum)==target,"finite twirl did not recover invariant target")
    noninvariant=[F(3,5),F(0),F(4,5)]
    transformed=[noninvariant[0],noninvariant[1],-noninvariant[2]]
    need(transformed!=noninvariant,"noninvariant vacuum control is degenerate")
    h=[F(-2),F(1),F(5)]
    energy=h[0]
    k=[x-energy for x in h]
    need(k==[0,3,7] and k[0]==0,"ground-energy subtraction failed")
    need(h[0]!=0,"unshifted-generator rejection is degenerate")
    physical_energies=k[:2]
    c=F(1,2)**int(physical_energies[1])
    faster=F(1,2)**6
    need(c==F(1,8) and 0<faster<c,"imaginary-time spectral controls failed")
    real_phase=(F(3,5),F(4,5))
    need(sum(x*x for x in real_phase)==1 and real_phase!=(1,0),"real-time phase control failed")
    controls={
        "physical_equals_full":{"rejected":True,"physical_dimension":physical_rank,"full_dimension":full_rank},
        "noninvariant_vacuum_premise_omitted":{"rejected":True,"vacuum":[str(x) for x in noninvariant],"gauge_transformed":[str(x) for x in transformed]},
        "ground_energy_not_subtracted":{"rejected":True,"raw_ground_energy":str(h[0]),"correct_ground_energy":"0"},
        "gap_implies_lower_imaginarytime_bound":{"rejected":True,"claimed_lower_at_log2":"1/8","actual_with_energy6":str(faster)},
        "gap_implies_real_time_decay":{"rejected":True,"nontrivial_phase":[str(x) for x in real_phase],"correlation_magnitude_squared":"1"},
    }
    results={"schema":"ym21-forward-j2-v1","loop":"j2","direction":"forward",
             "status":"physical_GNS_equals_invariant_subspace_with_restricted_gapped_generator",
             "comparison":{"physical_cyclic_equals_invariant":True,"physical_equals_full":False,
                           "gap_lower_alpha":"973/8640","generator_ground_energy_subtracted":True,
                           "real_time_exponential_decay_implied":False},
             "finite_fixture":{"symmetry_signs":[1,1,-1],"full_GNS_dimension":full_rank,
                               "physical_GNS_dimension":physical_rank,"physical_energy_spectrum":[str(x) for x in physical_energies],
                               "imaginary_time":"log(2)","hbar":"1","correlator":str(c)},
             "integral":"weak operator finite endpoint Haar average; strong vector integral on invariant vacuum",
             "domain":"D(H) intersect H_inv; abstract GNS domain transported by the proved unitary",
             "correlator":"0<C_W(t)<=Var_Psi(W)*exp(-973*alpha*t/(8640*hbar)), finite t>=0",
             "scope":{"model":"dyadic summable fixed spacing","homogeneous_identification":False,"continuum_identification":False,
                      "scientific_priority":"unverified"},"next_loop_executed":False}
    out=args.output.resolve()
    out.mkdir(parents=True,exist_ok=True)
    payloads={"results.json":results,"controls.json":controls}
    for name,payload in payloads.items():
        (out/name).write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n")
    need(all(hashlib.sha256(p.read_bytes()).hexdigest()==inputs[str(p.relative_to(ROOT))] for p in paths),"sources changed")
    manifest={"schema":"ym21-source-manifest-v1","inputs":inputs,
              "outputs":{n:hashlib.sha256((out/n).read_bytes()).hexdigest() for n in payloads},"cache_files_admitted":False}
    (out/"source-manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
    print(json.dumps(results["comparison"],sort_keys=True))


if __name__=="__main__":
    main()
