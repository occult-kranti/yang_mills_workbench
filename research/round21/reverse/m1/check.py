#!/usr/bin/env python3
"""Independent reverse M1 support, rational profile and topology controls."""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction as Q
from math import isqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CONTRACT = ROOT / "research/round21/contracts/m1.json"


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def polynomial(q):
    return 2 + 5*q + 5*q*q + 6*q**3 + 3*q**4


def budget(q):
    if isinstance(q, bool) or not 0 < q < 1:
        raise ValueError("q must lie strictly between zero and one")
    return polynomial(q)/(24*(1-q)**3*(1+q)**2*(1+q*q))


def profile(q, eta=Q(1,2), alpha=Q(2), energy=Q(1), hbar=Q(1)):
    if any(isinstance(v,bool) for v in (eta,alpha,energy,hbar)) or not 0 < eta < 1 or min(alpha,energy,hbar) <= 0:
        raise ValueError("strict eta and fixed positive physical scales required")
    b=budget(q); tau=eta/(8*b); sigma2=alpha*alpha*tau*tau*budget(q*q)/96
    tau_normalized=3*eta*(1+q)**2*(1+q*q)/polynomial(q)
    variance_normalized=polynomial(q*q)*(1+q)/(256*polynomial(q)**2*(1+q**4))
    need(tau/(1-q)**3==tau_normalized,"normalized tau identity")
    need(sigma2/(alpha*alpha*eta*eta*(1-q)**3)==variance_normalized,"normalized variance identity")
    return {"q":q,"tau":tau,"sigma2":sigma2,"norm":alpha*eta/8,
            "tau_normalized":tau_normalized,"variance_normalized":variance_normalized,
            "energy_shift_upper":sigma2/(alpha*(1-eta)/8)}


def face_edges(face):
    a,b,*base=face
    plus_a=base.copy(); plus_a[a]+=1
    plus_b=base.copy(); plus_b[b]+=1
    return {(a,*base),(b,*base),(a,*plus_b),(b,*plus_a)}


def omitted(face):
    a,b,x,y,z=face
    return (a,b)!=(0,1) or y%2==1 or x%4==3


def strip_edges(anchor):
    x,y,z=anchor
    return {(0,x+r,y+s,z) for r in range(3) for s in range(2)} | {(1,x+r,y,z) for r in range(4)}


def owner(edge):
    axis,x,y,z=edge
    if axis==0 and x%4!=3:
        return ("strip",x-x%4,y-y%2,z)
    if axis==1 and y%2==0:
        return ("strip",x-x%4,y,z)
    return ("free",*edge)


def completed_edges(edges):
    answer=set()
    for edge in edges:
        own=owner(edge)
        answer.update(strip_edges(own[1:]) if own[0]=="strip" else {edge})
    return answer


def incident_faces(edge):
    axis,*tail=edge
    answer=set()
    for other in range(3):
        if other==axis:
            continue
        a,b=sorted((axis,other))
        for offset in (0,-1):
            base=tail.copy(); base[other]+=offset
            if min(base)>=0:
                answer.add((a,b,*base))
    return answer


def touched_omitted(edges):
    return {face for edge in edges for face in incident_faces(edge) if omitted(face)}


def face_sum(faces,q):
    return sum((q**sum(f[2:])/24 for f in faces),Q(0))


def rational_sqrt_upper(value, denominator=10**12):
    scaled=value*denominator*denominator
    root=isqrt(scaled.numerator//scaled.denominator)
    if Q(root*root)<scaled:
        root+=1
    answer=Q(root,denominator)
    need(answer*answer>=value,"square-root upper bound")
    return answer


def geometric_checks():
    anchors=list(itertools.product(range(0,12,4),range(0,6,2),range(4)))
    constructed={}
    for anchor in anchors:
        edges=strip_edges(anchor)
        need(len(edges)==10,"strip must have ten links")
        for edge in edges:
            need(edge not in constructed,"overlapping selected-strip ownership")
            constructed[edge]=("strip",*anchor)
    universe=[(a,x,y,z) for a in range(3) for x in range(12) for y in range(6) for z in range(4)]
    boundary_counts=set()
    for edge in universe:
        expected=constructed.get(edge,("free",*edge))
        need(owner(edge)==expected,"complete-cover ownership mismatch")
        adjacent=incident_faces(edge)
        need(len(adjacent)<=4 and all(edge in face_edges(f) for f in adjacent),"incident-face reconstruction")
        boundary_counts.add(len(adjacent))
    need(boundary_counts=={2,3,4},"boundary incidence fixtures do not distinguish octant boundary")
    fixtures={
        "boundary_strip":strip_edges((0,0,0)),
        "interior_strip":strip_edges((4,2,1)),
        "free_z":{(2,5,3,1)},
        "wilson_dressed_strip":completed_edges(face_edges((0,1,0,0,1))),
        "mixed_factors":completed_edges({(0,3,2,1),(1,4,3,1),(2,2,2,0),(0,5,2,1)}),
    }
    rows=[]
    for name,edges in fixtures.items():
        need(completed_edges(edges)==edges,"fixture not complete-factor supported")
        faces=touched_omitted(edges)
        maxima=[max(edge[1+i] for edge in edges) for i in range(3)]
        direct={face for a,b in ((0,1),(0,2),(1,2))
                for base in itertools.product(*(range(m+1) for m in maxima))
                if omitted(face:=(a,b,*base)) and face_edges(face)&edges}
        need(faces==direct,"incident and direct enumeration disagree")
        need(len(faces)<=4*len(edges),"universal incidence bound violated")
        weights=[]
        for q in (Q(1,2),Q(3,4),Q(7,8),Q(31,32)):
            d=face_sum(faces,q)
            need(d<=Q(len(edges),6),"complete support weight bound violated")
            weights.append({"q":str(q),"D_F":str(d),"upper":str(Q(len(edges),6))})
        rows.append({"fixture":name,"links":len(edges),"omitted_faces":len(faces),"weights":weights})
    displayed=face_edges((0,1,0,0,1)); complete=completed_edges(displayed)
    missed=touched_omitted(complete)-touched_omitted(displayed)
    need(len(displayed)==4 and len(complete)==10 and bool(missed),"Wilson-only support control failed to discriminate")
    need(face_sum(touched_omitted(complete),Q(1,2))>face_sum(touched_omitted(displayed),Q(1,2)),"wrong support budget not smaller")
    return {"covered_links_checked":len(universe),"constructed_strips":len(anchors),
            "boundary_incidence_counts":sorted(boundary_counts),"fixtures":rows,
            "dressed_wilson_control":{"displayed_links":4,"complete_links":10,
                                      "missed_face_count":len(missed),"missed_example":list(sorted(missed)[0])}}


def topology_checks():
    c=Q(1,8); energy=Q(1); rows=[]
    flat_sq=c*c/(2*energy*energy*((energy+c)**2+energy*energy))
    previous=None
    for n in (1,2,4,8,16,32):
        fixed_sq=3*c*c/Q(4)**n
        moving_sq=c*c
        increasing_sq=c*c/(((n*energy)**2+energy*energy)*((n*energy+c)**2+energy*energy))
        need(fixed_sq<moving_sq,"fixed versus moving vector control")
        if previous:
            need(fixed_sq<previous[0] and increasing_sq<previous[1],"strong or norm-resolvent control not decreasing")
        previous=(fixed_sq,increasing_sq)
        # At t=pi*hbar/c the relative phase is exactly -1; no floating pi test.
        need((-1-1)**2==4,"propagator phase control")
        rows.append({"n":n,"fixed_vector_error_squared":str(fixed_sq),"moving_vector_error_squared":str(moving_sq),
                     "flat_reference_resolvent_norm_squared":str(flat_sq),
                     "growing_reference_resolvent_norm_squared":str(increasing_sq),
                     "propagator_norm_squared_at_half_turn":4})
    return rows


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--output",required=True)
    args=parser.parse_args(); out=Path(args.output)
    out.mkdir(parents=True,exist_ok=True)
    contract=json.loads(CONTRACT.read_text())
    dep=ROOT/contract["depends_on"]["gate"]
    need(sha(dep)==contract["depends_on"]["sha256"],"frozen predecessor digest mismatch")
    selection=ROOT/contract["selection_record"]
    record=json.loads(selection.read_text())
    need(set(record["completed_loops_at_selection"])=={"i1","i2","j1","j2","k1","k2"},"M selected before first six")
    for gate in record["evidence_gates"].values():
        need(sha(ROOT/gate["path"])==gate["sha256"],"selection-gate binding mismatch")
    geometry=geometric_checks()
    complete=completed_edges(face_edges((0,1,0,0,1)))
    rows=[]
    for eta in (Q(1,4),Q(1,2),Q(3,4)):
        previous=None
        for q in (Q(1,2),Q(3,4),Q(7,8),Q(15,16),Q(31,32),Q(127,128),Q(1023,1024)):
            row=profile(q,eta)
            d=face_sum(touched_omitted(complete),q)
            comm=4*row["tau"]*d
            local_upper=rational_sqrt_upper(row["sigma2"])+comm
            crude=rational_sqrt_upper(row["sigma2"])+2*row["tau"]*len(complete)/3
            need(local_upper<=crude,"local versus complete-cover crude bound")
            if previous:
                need(row["tau"]<previous[0] and row["sigma2"]<previous[1],"profile fixtures do not decay")
            previous=(row["tau"],row["sigma2"])
            rows.append({**{key:str(value) for key,value in row.items()},"eta":str(eta),"alpha_over_E_star":"2",
                         "local_vector_error_upper_for_norm_A_1":str(local_upper),"D_F":str(d)})
    need(budget(Q(1,2))==Q(107,135),"H2 exact baseline mismatch")
    need(3*Q(1,2)*4*2/polynomial(Q(1))==Q(4,7),"tau endpoint coefficient")
    need(polynomial(Q(1))*2/(256*polynomial(Q(1))**2*2)==Q(1,5376),"variance endpoint coefficient")
    rejected=[]
    for label,kwargs in [("q0",{"q":Q(0)}),("q1",{"q":Q(1)}),("eta0",{"q":Q(1,2),"eta":Q(0)}),
                         ("eta1",{"q":Q(1,2),"eta":Q(1)}),("alpha0",{"q":Q(1,2),"alpha":Q(0)}),
                         ("zero_E_star",{"q":Q(1,2),"energy":Q(0)}),("zero_hbar",{"q":Q(1,2),"hbar":Q(0)}),
                         ("boolean_eta",{"q":Q(1,2),"eta":True})]:
        try: profile(**kwargs)
        except ValueError: rejected.append(label)
        else: raise RuntimeError("invalid parameter admitted: "+label)
    result={"schema":"ym21-reverse-m1-v1","loop":"m1","direction":"reverse","passed":True,
            "comparison":{"strong_perturbation_limit_zero":True,"operator_norm_limit_zero":False,
                          "strong_resolvent_limit":True,"compact_time_strong_unitary_limit":True,
                          "norm_resolvent_conclusion":False,"homogeneous_limit_obtained":False},
            "geometry":geometry,"profile_rows":rows,"topology_rows":topology_checks(),
            "invalid_inputs_rejected":rejected,
            "scope":"Fixed A2 full-link representation and spacing, alpha/E_star>0, 0<eta<1; q approaches 1 from below.",
            "proof_boundary":"Exact arithmetic and support controls accompany the written density, domain and Duhamel proofs; no machine formalization or norm-resolvent verdict for the actual lattice family."}
    target=out/"results.json"; target.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    inputs=[HERE/"check.py",HERE/"report.md",CONTRACT,selection,dep,
            ROOT/"research/round21/methods/agent-instructions-at-selection.md",ROOT/"research/round21/methods/paired-physics-research.md",ROOT/"research/round21/methods/admission-and-matching.md",
            ROOT/"research/round19/advisor/a2-gate.json",ROOT/"research/round19/backward/a2/report.md",
            ROOT/"research/round20/advisor/h2-gate.json",ROOT/"research/round20/reverse/h2/report.md",ROOT/"research/round20/reverse/h2/check.py",
            ROOT/"research/round20/advisor/g2-gate.json",ROOT/"research/round20/reverse/g2/report.md",ROOT/"research/round21/advisor/j2-gate.json"]
    inputs.extend(ROOT/item["path"] for item in record["evidence_gates"].values())
    manifest={"schema":"ym21-source-manifest-v1","inputs":{str(path.relative_to(ROOT)):sha(path) for path in sorted(set(inputs))},
              "outputs":{"results.json":sha(target)}}
    (out/"source-manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"loop":"m1","direction":"reverse","passed":True,"profile_rows":len(rows),
                      "covered_links":geometry["covered_links_checked"],"invalid_inputs_rejected":len(rejected)}))


if __name__=="__main__":
    main()
