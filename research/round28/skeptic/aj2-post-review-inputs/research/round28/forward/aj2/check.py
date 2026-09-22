#!/usr/bin/env python3
"""Independent AJ2 exact diagnostics; analytic statements are proved in report.md.

Use --output with a fresh absolute directory. No installed or historical
algorithm is opened or executed. Repository originals are provenance metadata;
all source-content reads use frozen owned snapshots.
"""
import argparse
from fractions import Fraction as F
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CONTRACT_SHA = "0f71cc35d4e6fef93188cee740f9cdf90596f034193f3c9aee9455fb0411c154"
PACK_SHA = "a8fbbe82d129b9108bf12b4920d0ead9e4cec3dc17761f4d271e9e4a457fcc5c"
CHECKS = 0


def check(truth, message):
    global CHECKS
    CHECKS += 1
    if not truth:
        raise ValueError(message)


def fraction(x):
    x = F(x)
    return {"numerator": x.numerator, "denominator": x.denominator}


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def source_bindings():
    pack_path = HERE / "inputs/input-pack-freeze.json"
    check(digest(pack_path) == PACK_SHA, "Input pack changed")
    pack = json.loads(pack_path.read_text())
    bindings = {}
    for name, expected in pack["bindings"].items():
        p = ROOT / name
        check(p.is_relative_to(HERE / "inputs"), "Input path outside owned snapshots")
        check(digest(p) == expected, "Frozen input mismatch: " + name)
        bindings[name] = expected
    bindings[str(pack_path.relative_to(ROOT))] = PACK_SHA
    manifest = HERE / "inputs/source-inventory.json"
    entries = json.loads(manifest.read_text())["entries"]
    for entry in entries:
        src, snap, expected = entry["source"], entry["snapshot"], entry["sha256"]
        check(not Path(src).is_absolute() and ".." not in Path(src).parts, "Nonportable original provenance")
        check(not Path(snap).is_absolute() and ".." not in Path(snap).parts, "Nonportable snapshot")
        check(bindings.get(snap) == expected, "Manifest snapshot not bound by input freeze")
        check(src not in bindings or bindings[src] == expected, "Conflicting original provenance")
        # Deliberately do not open src: preflight checked originals; runtime uses snapshots.
        bindings[src] = expected
    contract = HERE / "inputs/repo/research/round28/contracts/aj2.json"
    check(digest(contract) == CONTRACT_SHA, "Wrong contract")
    c = json.loads(contract.read_text())
    check(c["sequence"] == 8 and c["loop"] == "aj2" and len(c["sources"]) == 47, "Wrong investigation")
    for src, expected in c["sources"].items():
        check(bindings.get(src) == expected, "Missing contract original binding")
    bindings[str(Path(__file__).resolve().relative_to(ROOT))] = digest(Path(__file__).resolve())
    check(all(not Path(p).is_absolute() for p in bindings), "Bindings must be flat repository-relative paths")
    return dict(sorted(bindings.items()))


E = ((1,0,0), (0,1,0), (0,0,1))
O = (0,0,0)


def plus(a,b):
    return tuple(x+y for x,y in zip(a,b))


def owner(a):
    return (a[0]//4, a[1]//2, a[2])


def block_links(b):
    return {((4*b[0]+i,2*b[1]+j,b[2]),d)
            for i,j,d in product(range(4),range(2),range(3))}


def geometry():
    # Walk the specified closed oriented boundary and canonicalize each edge.
    walk = (O,E[0],plus(E[0],E[2]),E[2],O)
    word = []
    for a,b in zip(walk,walk[1:]):
        delta = tuple(b[k]-a[k] for k in range(3))
        axes = [k for k,v in enumerate(delta) if v]
        check(len(axes)==1 and abs(delta[axes[0]])==1, "Not an elementary original link")
        d = axes[0]
        sign = delta[d]
        tail = a if sign==1 else b
        word.append(((tail,d),sign))
    check(word == [((O,0),1),((E[0],2),1),((E[2],0),-1),((O,2),-1)], "Ordered original xz word")
    check(len({link for link,_ in word})==4 and walk[-1]==walk[0], "Four distinct closed-loop links")
    region = {owner(link[0]) for link,_ in word}
    check(region == {O,E[2]}, "Minimal complete-factor region")
    links = set().union(*(block_links(b) for b in region))
    vertices = {v for a,d in links for v in (a,plus(a,E[d]))}
    check(len(links)==48 and len(vertices)==36, "Full factor and endpoint counts")
    check(all(link in links for link,_ in word), "Original loop missing from complete factor support")
    for b in region:
        check(len(block_links(b))==24 and all(owner(a)==b for a,d in block_links(b)), "Tail ownership")
    loop_vertices = set(walk)
    extra_vertices = vertices-loop_vertices
    check(len(loop_vertices)==4 and len(extra_vertices)==32, "Loop-only endpoints are incomplete for the full factor")
    check(owner(E[2]) != owner(O), "Onsite-only support control must discriminate")
    return word, {
        "oriented_vertices": walk, "ordered_word": [{"tail":a,"axis":d,"orientation":s,"owner":owner(a)} for (a,d),s in word],
        "minimal_complete_coarse_region": sorted(region), "owned_link_count":len(links),
        "owned_links":[{"tail":a,"axis":d,"head":plus(a,E[d]),"owner":owner(a)} for a,d in sorted(links)],
        "complete_endpoint_count":len(vertices),"complete_endpoint_vertices":sorted(vertices),
        "loop_endpoint_count":4,"additional_complete_factor_endpoints":sorted(extra_vertices),
        "omitted_xz_face":True,"full_group_boundary":"I1 retains an anchor interaction only when its entire four-site star is present; this observable itself needs the two factors listed above."}


IDENTITY = (F(1),F(0),F(0),F(0))
UNITS = ((F(4,5),F(0),F(3,5),F(0)),
         (F(12,13),F(5,13),F(0),F(0)),
         (F(15,17),F(0),F(0),F(8,17)))


def multiply(a,b):
    s,x,y,z=a;t,u,v,w=b
    return (s*t-x*u-y*v-z*w,s*u+x*t+y*w-z*v,
            s*v-x*w+y*t+z*u,s*w+x*v-y*u+z*t)


def inverse(a):
    return (a[0],-a[1],-a[2],-a[3])


def word_value(word, assignment):
    value=IDENTITY
    for link,sign in word:
        q=assignment[link]
        value=multiply(value,q if sign==1 else inverse(q))
    return value


def gauged(assignment, action, missing_heads=False):
    return {(a,d):multiply(multiply(action.get(a,IDENTITY),q),
                          IDENTITY if missing_heads else inverse(action.get(plus(a,E[d]),IDENTITY)))
            for (a,d),q in assignment.items()}


def quaternion_diagnostics(word, geo):
    for q in UNITS:
        check(multiply(q,inverse(q))==IDENTITY,"Rational SU(2) unit norm")
    assignments={link:UNITS[(2*k+1)%3] for k,(link,_) in enumerate(word)}
    original=word_value(word,assignments)
    attempts=[]
    for offset in range(3):
        action={tuple(v):UNITS[(k+offset)%3] for k,v in enumerate(geo["complete_endpoint_vertices"])}
        full=word_value(word,gauged(assignments,action))
        wrong=word_value(word,gauged(assignments,action,True))
        check(full[0]==original[0],"Closed Wilson trace changed under complete gauge action")
        check(full==multiply(multiply(action[O],original),inverse(action[O])),"Holonomy basepoint conjugation")
        attempts.append({"offset":offset,"original":fraction(original[0]),"complete":fraction(full[0]),
                         "missing_heads":fraction(wrong[0]),"discriminates":wrong[0]!=original[0]})
        if wrong[0]!=original[0]:
            break
    check(attempts[-1]["discriminates"],"No discriminating missing-head control")
    charged=dict(assignments); first=word[0][0]
    transformed=gauged(charged,{first[0]:tuple(-x for x in IDENTITY)})
    check(transformed[first]==tuple(-x for x in charged[first]),"Open fundamental link must be charged")
    closed_center=word_value(word,transformed)
    check(closed_center[0]==original[0],"Closed loop survives endpoint center flip")
    # Conditional linear coefficient in the *actual* U_z(0), not a plaquette variable.
    variable=(O,2)
    coefficients=[]
    for k in range(4):
        current=dict(assignments)
        current[variable]=tuple(F(int(j==k)) for j in range(4))
        coefficients.append(word_value(word,current)[0])
    check(sum(x*x for x in coefficients)==1,"Actual conditional quaternion coefficient has unit norm")
    haar_second=sum(x*x/F(4) for x in coefficients)
    check(haar_second==F(1,4),"Fundamental Haar second moment")
    return {"exact_rational_assignments":[{"tail":a,"axis":d,"quaternion":[fraction(x) for x in q]} for (a,d),q in sorted(assignments.items())],
            "missing_head_attempts":attempts,"blind_attempt_count":sum(not x["discriminates"] for x in attempts),
            "closed_center_invariant":True,"open_link_center_charge":-1,
            "conditional_actual_link":{"tail":O,"axis":2},"conditional_coefficients":[fraction(x) for x in coefficients],
            "reference_haar_mean":fraction(0),"reference_haar_second_moment":fraction(haar_second),
            "reference_fundamental_character_second_moment":fraction(4*haar_second),
            "scope":"Conditional coefficients and exact Haar identities are reference diagnostics; no interacting-state moment, sampling proof or finite-group quadrature is asserted."}


def controls():
    epsilons=[F(1,2**k) for k in (1,2,3,4)]
    concentration=[]
    for epsilon in epsilons:
        check(0<epsilon<1 and 0<epsilon*epsilon<1,"Concentration band")
        concentration.append({"epsilon":fraction(epsilon),"normal_band_state_variance_upper":fraction(epsilon**2),
                              "variance_strictly_positive":"analytic non-atomic argument", "actual_ground_state":False})
    check(epsilons[1]**2<F(1,4),"Band-state control rejects universal Haar variance substitution")
    constant=F(1,3)
    check(constant*constant-constant**2==0,"Constant variance")
    step_values=(F(0),F(1)); step_density=(F(1),F(0))
    step_mean=sum(p*x for p,x in zip(step_density,step_values))
    step_variance=sum(p*x*x for p,x in zip(step_density,step_values))-step_mean**2
    check(step_values[0]!=step_values[1] and step_variance==0,"Nonconstant step control")
    check(sum(step_density)==1 and step_density[1]==0,"Normal nonfaithful finite diagnostic")
    # Abstract spectral measures, with s=Delta*t/hbar=log(2), Delta=alpha/16.
    measures=[]
    for k in (2,3,8):
        heat=F(1,2**k); upper=F(1,2)
        check(0<heat<upper,"Gap gives upper rather than threshold lower decay")
        measures.append({"energy_in_units_Delta":k,"total_measure":fraction(1),"mass_at_Delta":fraction(0),
                         "heat_at_s_log2":fraction(heat),"gap_upper_at_s_log2":fraction(upper)})
    real_phase=(F(0),F(-1))
    check(sum(x*x for x in real_phase)==1,"Real-time atom modulus does not decay")
    # W=(1/2)[[1,1],[1,1]], Omega=e0, H=diag(0,2Delta).
    mean=F(1,2);var=F(1,4);centered=var/F(4);uncentered=mean**2+centered
    check(centered==F(1,16) and uncentered==F(5,16),"Connected versus uncentered spectral correlation")
    check(uncentered>(mean**2+var)/2,"Uncentered vector invalidates a naive gap-decay ceiling")
    prefix=[]
    for k in range(5):
        N=2**k
        mass=sum((F(1,n*n) for n in range(1,N+1)),F(0))
        form=sum((F(1,n) for n in range(1,N+1)),F(0))
        op=F(N)
        check(mass<2 and form>=F(k+1,2) and op==N,"Bounded-vector/domain countermodel prefixes")
        prefix.append({"N":N,"squared_vector_norm":fraction(mass),"normalized_form_prefix":fraction(form),
                       "normalized_operator_norm_squared_prefix":fraction(op)})
    return {"constant_multiplier":{"value":fraction(constant),"variance":fraction(0)},
            "nonconstant_step_multiplier":{"finite_diagnostic_values":[fraction(x) for x in step_values],
                "density":[fraction(x) for x in step_density],"variance":fraction(step_variance),
                "analytic_model":"Multiplication by 1_[1/2,1] on L2([0,1]); normalized indicator of [0,1/2) is a normal vector state with variance0."},
            "normal_nonfaithful_state":{"rank_one_haar_vector":True,"reference_W_variance":fraction(F(1,4)),
                "faithful_on_full_local_B_H":False,"actual_interacting_state_identified":False},
            "normal_concentration_bands":concentration,
            "singular_concentration":{"analytic_construction":"Weak-star cluster of normal band vector states as epsilon goes to0 has W and W^2 expectation0 but I expectation1; it cannot be normal because ker W is zero.",
                "zero_original_point_spectral_projection_does_not_pass_Borel_calculus_through_singular_GNS":True},
            "haar_variance_substitution":{"reference":fraction(F(1,4)),"normal_band_ceiling":fraction(F(1,16)),"equal":False},
            "vacuum_only_gap":{"physical_dimension":1,"centered_excited_vector_norm_squared":fraction(0),"positive_excited_measure":False,"gap_exclusion_still_holds":True},
            "spectral_point_measure_controls":measures,
            "non_atomic_energy_measure":{"analytic_model":"Uniform probability on [Delta,2Delta] has lower support endpoint Delta and zero mass at that endpoint; no eigenatom follows."},
            "real_time_no_gap_decay":{"phase_at_energy2Delta_and_s_pi_over4":[fraction(x) for x in real_phase],"modulus_squared":fraction(1)},
            "centering":{"mean":fraction(mean),"variance":fraction(var),"centered_heat":fraction(centered),"uncentered_heat":fraction(uncentered)},
            "unproved_domain_membership":{"analytic_model":"H e_n=n Delta e_n, chi=sum n^-1 e_n perpendicular to an added zero vacuum. Its mass is finite but its form/operator moments diverge. A bounded self-adjoint rank-two observable can create it.","prefixes":prefix,"actual_W_energy_moment_computed":False}}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",required=True)
    out=Path(parser.parse_args().output)
    check(out.is_absolute() and not out.exists(),"Output must be fresh and absolute")
    bindings=source_bindings()
    word,geo=geometry()
    gauge=quaternion_diagnostics(word,geo)
    diagnostics=controls()
    result={"schema":"research-results-v1","loop":"aj2","sequence":8,"direction":"forward",
            "status":"exact diagnostics pass; independent analytic proof is in report.md, pending review",
            "bindings":bindings,"contract_sha256":CONTRACT_SHA,"input_pack_sha256":PACK_SHA,
            "scope":{"actual_I1_AJ1_homogeneous_orthant":True,"complete_local_factor_support":True,
                     "all_real_W_point_spectral_projections_zero":"analytic proof on original local Haar space",
                     "actual_centered_Wilson_vector_nonzero":"analytic proof using inherited local normality",
                     "finite_imaginary_time_positive":"analytic bounded-semigroup proof",
                     "gap_upper_decay":"actual variance times exp(-alpha*t/(16*hbar))",
                     "regime":"all real |tau|<unevaluated tau_* with inherited fixed selected coefficients",
                     "normality_implies_faithfulness":False,"interacting_variance_equals_Haar":False,
                     "uniform_positive_variance_margin":False,"numerical_nonzero_tau":False,
                     "threshold_eigenvalue_identified":False,"lower_decay_bound_claimed":False,
                     "real_time_decay_claimed":False,"actual_vector_form_or_operator_domain_claimed":False,
                     "new_energy_moment_goal":False,"continuum_yang_mills":False,"fifth_goal_executed":False},
            "exact_scales":{"delta_over_alpha":fraction(F(1,8)),"inherited_gap_over_alpha":fraction(F(1,16)),"frequency":"physical energy/hbar"},
            "geometry":geo,"quaternion_and_haar_diagnostics":gauge,"controls":diagnostics,
            "analytic_claims":{"conditional_W_law_under_product_Haar":"density (2/pi)*sqrt(1-x^2) on [-1,1], integral1",
                "normal_state_variance":"v=omega(W^2)-omega(W)^2>0; value not evaluated",
                "physical_vector":"chi=(pi(W)-omega(W))Omega in H_cyc intersect Omega-perp",
                "positive_measure":"nu_chi(B)=<chi,E_Hphys(B)chi>; mass v, support contained in [alpha/16,infinity)",
                "heat":"C(t)=integral exp(-t*E/hbar) dnu_chi(E); 0<C(t)<=v*exp(-alpha*t/(16*hbar)) for every finite t>=0"},
            "check_count":CHECKS,"blind_diagnostic_attempt_count":gauge["blind_attempt_count"],
            "limits":"Exact rational diagnostics do not prove Haar-null levels, local normality, the infinite-volume spectral theorem or interacting moments. Analytic proofs and inherited sources supply those premises."}
    out.mkdir(parents=True,exist_ok=False)
    (out/"results.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print("AJ2 exact diagnostics passed:",CHECKS,"checks; wrote deterministic results.json")


if __name__=="__main__":
    main()
