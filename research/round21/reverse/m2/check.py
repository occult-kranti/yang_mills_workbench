#!/usr/bin/env python3
"""Reverse M2: exact profile, complex covariance, support and scope controls."""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from dataclasses import dataclass
from fractions import Fraction as Q
from math import isqrt
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CONTRACT = ROOT / "research/round21/contracts/m2.json"


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sqrt_upper(x, scale=10**18):
    need(x >= 0, "negative squared magnitude")
    y = x * scale * scale
    n = isqrt(y.numerator // y.denominator)
    if Q(n*n) < y:
        n += 1
    answer = Q(n, scale)
    need(answer*answer >= x, "invalid rational root enclosure")
    return answer


@dataclass(frozen=True)
class G:
    """Gaussian rational; no floating arithmetic in complex controls."""
    r: Q = Q(0)
    i: Q = Q(0)

    def __post_init__(self):
        object.__setattr__(self, "r", Q(self.r))
        object.__setattr__(self, "i", Q(self.i))

    def __add__(self, b):
        b = b if isinstance(b, G) else G(b)
        return G(self.r+b.r, self.i+b.i)

    __radd__ = __add__

    def __neg__(self):
        return G(-self.r, -self.i)

    def __sub__(self, b):
        return self + (-b if isinstance(b, G) else G(-b))

    def __mul__(self, b):
        b = b if isinstance(b, G) else G(b)
        return G(self.r*b.r-self.i*b.i, self.r*b.i+self.i*b.r)

    __rmul__ = __mul__

    def conj(self):
        return G(self.r, -self.i)

    def square_abs(self):
        return self.r*self.r+self.i*self.i

    def data(self):
        return {"real": str(self.r), "imaginary": str(self.i)}


def mat(rows):
    return [[x if isinstance(x, G) else G(x) for x in row] for row in rows]


def adj(a):
    return [[a[j][i].conj() for j in range(len(a))] for i in range(len(a[0]))]


def mm(a, b):
    return [[sum((x*y for x, y in zip(row, col)), G()) for col in zip(*b)] for row in a]


def mv(a, v):
    return [sum((x*y for x, y in zip(row, v)), G()) for row in a]


def dot(v, w):
    return sum((x.conj()*y for x, y in zip(v, w)), G())


def minus(a, b):
    return [[x-y for x, y in zip(ar, br)] for ar, br in zip(a, b)]


def scale(a, c):
    return [[x*c for x in row] for row in a]


def eye(n):
    return mat([[int(i == j) for j in range(n)] for i in range(n)])


def frob2(a):
    return sum((x.square_abs() for row in a for x in row), Q(0))


def kron(a, b):
    return [[x*y for x in ar for y in br] for ar in a for br in b]


def mean(v, a):
    return dot(v, mv(a, v))


def covariance(v, a, b, u):
    return dot(mv(a, v), mv(u, mv(b, v))) - mean(v, adj(a))*mean(v, b)


def p(q):
    return 2+5*q+5*q*q+6*q**3+3*q**4


def budget(q):
    if isinstance(q, bool) or not isinstance(q, Q) or not 0 < q < 1:
        raise ValueError("q must be an exact rational strictly between zero and one")
    return p(q)/(24*(1-q)**3*(1+q)**2*(1+q*q))


def profile(q, eta=Q(1,2), alpha=Q(2), hbar=Q(1), e_star=Q(1)):
    if any(isinstance(x, bool) or not isinstance(x, Q) for x in (eta, alpha, hbar, e_star)):
        raise ValueError("exact rational model parameters required; Boolean excluded")
    if not 0 < eta < 1 or min(alpha, hbar, e_star) <= 0:
        raise ValueError("strict budget and positive physical units required")
    b = budget(q)
    eps = 1-q
    tau = eta/(8*b)
    sigma2 = alpha*alpha*tau*tau*budget(q*q)/96
    gap = alpha*(1-eta)/8
    d2 = sigma2/(gap*gap)
    normalized = p(q*q)*(1+q)/(256*p(q)**2*(1+q**4))
    need(sigma2/(alpha*alpha*eta*eta*eps**3) == normalized, "profile variance identity")
    need(tau/eps**3 == 3*eta*(1+q)**2*(1+q*q)/p(q), "profile coupling identity")
    need(d2 == eta*eta*eps**3*p(q*q)*(1+q)/(4*(1-eta)**2*p(q)**2*(1+q**4)), "distance identity")
    coarse = eta*eta*eps**3/(4*(1-eta)**2)
    need(d2 <= coarse, "uniform coarse variance condition")
    sufficient = eps**3 <= (1-eta)**2/(64*eta*eta)
    if sufficient:
        need(d2 <= Q(1,256), "sufficient profile condition fails")
    return {"q": q, "eta": eta, "alpha_over_E_star": alpha/e_star,
            "tau": tau, "sigma2": sigma2, "gap": gap, "projector_bound_squared": d2,
            "energy_shift_upper": sigma2/gap, "normalized_variance": normalized,
            "coarse_projector_bound_squared": coarse, "simple_variance_condition": sufficient}


def complex_controls():
    ref = [G(1), G(0)]
    state = [G(Q(3,5)), G(Q(4,5))]
    rotation = mat([[Q(3,5), Q(-4,5)], [Q(4,5), Q(3,5)]])
    a = scale(mat([[G(1,1), G(2,-1)], [G(3,2), G(-1,1)]]), Q(1,10))
    b = scale(mat([[G(2,-1), G(-1,3)], [G(1,-2), G(4,1)]]), Q(1,10))
    d = Q(4,5)
    proj = [[x*y.conj() for y in state] for x in state]
    diff = minus(proj, mat([[1,0],[0,0]]))
    need(diff[0][0]+diff[1][1] == G(), "projection difference trace")
    need(diff[0][0]*diff[1][1]-diff[0][1]*diff[1][0] == G(-d*d), "projection eigenvalue magnitude")
    na, nb = sqrt_upper(frob2(a)), sqrt_upper(frob2(b))
    rows = []
    phases = [G(1), G(0,1), G(-1), G(0,-1)]
    for phase in phases:
        u0 = [[G(1),G()],[G(),phase]]
        uq = mm(mm(rotation, u0), adj(rotation))
        need(mm(adj(uq), uq) == eye(2), "exact unitary control")
        need(mv(uq, state) == state, "canonical vacuum is not fixed")
        cq, c0 = covariance(state,a,b,uq), covariance(ref,a,b,u0)
        x = mm(mm(adj(a),uq),b)
        state_cost = mean(state,x)-mean(ref,x)
        mean_cost = mean(state,adj(a))*mean(state,b)-mean(ref,adj(a))*mean(ref,b)
        dynamic_vec = mv(minus(uq,u0),mv(b,ref))
        dynamic_cost = dot(mv(a,ref),dynamic_vec)
        need(cq-c0 == state_cost+dynamic_cost-mean_cost, "connected decomposition")
        need(state_cost.square_abs() <= (2*d*na*nb)**2, "pure-state operator expectation bound")
        need(mean_cost.square_abs() <= (4*d*na*nb)**2, "both means bound")
        dyn = sqrt_upper(dot(dynamic_vec,dynamic_vec).r)
        need((cq-c0).square_abs() <= (6*d*na*nb+na*dyn)**2, "coefficient-six bound")
        rows.append({"phase":phase.data(), "connected_q":cq.data(), "connected_reference":c0.data(),
                     "error_squared":str((cq-c0).square_abs())})
    raw0 = dot(mv(a,state),mv(b,state))
    centered0 = covariance(state,a,b,eye(2))
    wrong_star = mean(state,mm(a,b))-mean(state,a)*mean(state,b)
    need(raw0 != centered0, "uncentered control did not discriminate")
    need(wrong_star != centered0, "missing conjugation control did not discriminate")
    mean_change_a = mean(state,adj(a))-mean(ref,adj(a))
    mean_change_b = mean(state,b)-mean(ref,b)
    need(mean_change_a != G() and mean_change_b != G(), "one mean held fixed accidentally")
    return {"rows":rows, "uncentered_zero_time":raw0.data(), "correct_zero_time":centered0.data(),
            "wrong_no_adjoint_zero_time":wrong_star.data(), "projector_distance":str(d),
            "projector_trace_distance":str(2*d)}


def phase_and_sector_controls():
    vac = [G(1),G()]
    shifted = mat([[1,0],[0,G(0,1)]])
    unshifted = mat([[-1,0],[0,G(0,-1)]])
    x = mat([[0,1],[1,0]])
    need(covariance(vac,eye(2),eye(2),shifted) == G(), "centered identity must vanish")
    wrong_identity = covariance(vac,eye(2),eye(2),unshifted)
    need(wrong_identity == G(-2), "omitted-energy-shift control")
    need(covariance(vac,x,x,shifted) == G(0,1), "correct excitation phase")
    need(covariance(vac,x,x,unshifted) == G(0,-1), "wrong excitation phase")
    g = mat([[1,0,0],[0,1,0],[0,0,-1]])
    h = mat([[0,0,0],[0,Q(1,32),0],[0,0,Q(1,16)]])
    physical = mat([[1,0,0],[0,1,0],[0,0,0]])
    need(mm(h,g) == mm(g,h) and mm(h,physical) == mm(physical,h), "physical reduction")
    arbitrary = mat([[1,2,3],[4,5,6],[7,8,9]])
    averaged = scale([[a+b for a,b in zip(ar,br)] for ar,br in zip(arbitrary,mm(mm(g,arbitrary),g))],Q(1,2))
    need(averaged == mat([[1,2,0],[4,5,0],[0,0,9]]), "gauge averaging deletes charged entries")
    own_gap, dyadic = Q(1,32), Q(973,8640)
    need(own_gap < dyadic, "profile gap distinction control")
    return {"identity_with_omitted_shift":wrong_identity.data(), "units":"hbar=1; t=pi/2; H=diag(-2,1)",
            "physical_dimension":"2", "full_dimension":"3", "canonical_eta":"3/4",
            "own_gap_over_alpha":str(own_gap), "inadmissible_dyadic_floor_over_alpha":str(dyadic),
            "scope":"Finite controls expose wrong inferences; they do not compute the lattice spectrum."}


def face_edges(a,b,base):
    va, vb = list(base), list(base)
    va[a] += 1
    vb[b] += 1
    return {(a,*base),(b,*va),(a,*vb),(b,*base)}


def support_controls():
    displayed = face_edges(0,2,(0,0,0))
    # Construct actual tiles and locate membership, rather than importing M1's owner formula.
    tiles = []
    for x,y,z in itertools.product((0,4),(0,2),(0,1,2)):
        tiles.append({(0,x+r,y+s,z) for r in range(3) for s in range(2)} |
                     {(1,x+r,y,z) for r in range(4)})
    complete = set()
    for edge in displayed:
        hits = [tile for tile in tiles if edge in tile]
        need(len(hits) <= 1, "multiple complete-factor owners")
        complete.update(hits[0] if hits else {edge})

    def incident(edges):
        maxima = [max(e[k+1] for e in edges) for k in range(3)]
        answer = set()
        for base in itertools.product(*(range(m+1) for m in maxima)):
            x,y,z = base
            for a,b in ((0,1),(0,2),(1,2)):
                if (a,b)==(0,1) and y%2==0 and x%4 != 3:
                    continue
                if face_edges(a,b,base) & edges:
                    answer.add((a,b,*base))
        return answer

    narrow, broad = incident(displayed), incident(complete)
    need(len(displayed)==4 and len(complete)==22, "origin-xz complete cover")
    need(len(narrow)==5 and len(broad)==28 and narrow < broad, "incident omitted faces")
    q=Q(1,2)
    dn=sum((q**sum(f[2:])/24 for f in narrow),Q())
    df=sum((q**sum(f[2:])/24 for f in broad),Q())
    need(dn < df <= Q(len(complete),6), "support budget control")
    x,z = mat([[0,1],[1,0]]),mat([[1,0],[0,-1]])
    swap = mat([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])
    b = kron(x,eye(2))
    evolved = mm(mm(swap,b),adj(swap))
    need(evolved == kron(eye(2),x), "within-factor support migration")
    interaction = kron(eye(2),z)
    need(frob2(minus(mm(b,interaction),mm(interaction,b))) == 0, "initial displayed-link commutator")
    migrated = frob2(minus(mm(evolved,interaction),mm(interaction,evolved)))
    need(migrated > 0, "displayed support incorrectly preserved by factor dynamics")
    return {"displayed_links":"4", "complete_links":"22", "displayed_incident_faces":"5",
            "complete_incident_faces":"28", "D_displayed_at_half":str(dn), "D_complete_at_half":str(df),
            "missed_example":list(sorted(broad-narrow)[0]), "migrated_commutator_frobenius_squared":str(migrated)}


def exponent_controls():
    rows=[]
    for gamma in (Q(0),Q(1),Q(3,2),Q(2)):
        state, residual, energy_local = Q(3,2),Q(3,2)-gamma,Q(3)-gamma
        sufficient = min(state,residual,energy_local) > 0
        need(sufficient == (gamma < Q(3,2)), "time-window eligibility")
        rows.append({"gamma":str(gamma), "state_exponent":str(state), "residual_exponent":str(residual),
                     "energy_and_local_exponent":str(energy_local), "sufficient_vanishing_bound":sufficient})
    need(p(Q(1))*2/(256*p(Q(1))**2*2) == Q(1,5376), "endpoint residual coefficient")
    # Same declared upper order, two possible scalar phase errors at T=epsilon^-3/2.
    # epsilon=1/n^2. A phase frequency n^-6 vanishes uniformly there; n^-3 can persist.
    phase_rows=[]
    for n in (2,4,8,16):
        fast = Q(1,n**6)*n**3
        slow = Q(1,n**3)*n**3
        need(fast <= slow == 1, "upper-order endpoint ambiguity")
        phase_rows.append({"n":str(n), "vanishing_family_phase_upper":str(fast), "persistent_family_phase":"1"})
    return {"exponents":rows, "eta_half_C_one_endpoint_bound_squared":str(Q(1,21504)),
            "endpoint_included":False, "actual_endpoint_nonconvergence_claimed":False,
            "phase_order_controls":phase_rows,
            "scope":"Abstract phase-order controls illustrate insufficiency; no endpoint result for the actual profile."}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",required=True)
    args=parser.parse_args()
    out=Path(args.output)
    out.mkdir(parents=True,exist_ok=True)
    contract=json.loads(CONTRACT.read_text())
    dep=ROOT/contract["depends_on"]["gate"]
    need(sha(dep)==contract["depends_on"]["sha256"],"M1 gate changed after selection")
    need(json.loads(dep.read_text())["status"] == "accepted", "M1 was not admitted")
    selection=ROOT/contract["selection_record"]
    need(selection.is_file(),"missing M2 selection decision")
    profile_rows=[]
    for eta in (Q(1,4),Q(1,2),Q(3,4)):
        for n in (2,4,8,16,32,64):
            row=profile(1-Q(1,n*n),eta)
            sigma=sqrt_upper(row["sigma2"])
            # gamma=1, C=1, hbar=1, alpha=2, complete origin-xz cover.
            time=Q(n*n,2)
            bound=6*sigma/row["gap"]+time*(row["energy_shift_upper"]+sigma+2*row["tau"]*Q(22,3))
            row["gamma_one_window"] = time
            row["gamma_one_correlation_bound_for_unit_norms"] = bound
            profile_rows.append({k:v if type(v) is bool else str(v) for k,v in row.items()})
    exact=profile(Q(3,4),Q(1,2))
    need(exact["simple_variance_condition"] and exact["projector_bound_squared"] <= Q(1,256), "concrete Wilson condition")
    variance=Q(1,4)-2*Q(1,16)-4*Q(1,16)**2
    need(variance==Q(7,64)>0,"variance floor arithmetic")
    need(budget(Q(1,2))==Q(107,135),"inherited exact profile baseline")
    rejected=[]
    invalid=[("q_zero",{"q":Q(0)}),("q_one",{"q":Q(1)}),("q_boolean",{"q":True}),
             ("eta_zero",{"q":Q(1,2),"eta":Q(0)}),("eta_one",{"q":Q(1,2),"eta":Q(1)}),
             ("eta_boolean",{"q":Q(1,2),"eta":True}),("alpha_zero",{"q":Q(1,2),"alpha":Q(0)}),
             ("hbar_zero",{"q":Q(1,2),"hbar":Q(0)}),("E_star_zero",{"q":Q(1,2),"e_star":Q(0)})]
    for name,kwargs in invalid:
        try:
            profile(**kwargs)
        except ValueError:
            rejected.append(name)
        else:
            raise RuntimeError("invalid profile admitted: "+name)
    controls={"schema":"ym21-reverse-m2-controls-v1", "complex_centering":complex_controls(),
              "energy_shift_and_physical_sector":phase_and_sector_controls(), "complete_support":support_controls(),
              "time_scope":exponent_controls(), "invalid_inputs_rejected":rejected}
    result={"schema":"ym21-reverse-m2-v1", "loop":"m2", "direction":"reverse", "passed":True,
            "comparison":{"connected_error_projector_coefficient":"6", "time_window_exponent_upper":"3/2",
                          "time_window_endpoint_included":False, "fixed_time_error_exponent":"3/2",
                          "physical_sector_rechecked":True, "variance_floor_fixture":"7/64", "homogeneous_limit_obtained":False},
            "profile_rows":profile_rows,
            "wilson_condition":{"eta":"1/2", "q_lower":"3/4", "q_upper_excluded":"1", "variance_floor":"7/64",
                                "projector_bound_squared_at_lower":str(exact["projector_bound_squared"])},
            "scope":"Fixed canonical selected-strip full-link profile; fixed bounded local gauge-invariant A,B and energy/time units.",
            "proof_boundary":"Exact controls accompany the written infinite-space proof; no measured data, optimal window or continuum claim."}
    outputs={"results.json":result,"controls.json":controls}
    for name,payload in outputs.items():
        (out/name).write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n")
    inputs=[HERE/"check.py", HERE/"report.md", HERE/"instruction-snapshot.md", HERE/"isolation-note.json", CONTRACT, dep, selection,
            ROOT/"research/round21/reverse/m1/report.md", ROOT/"research/round21/reverse/m1/check.py",
            ROOT/"research/round21/reverse/m1/output/results.json", ROOT/"research/round21/reverse/m1/output/source-manifest.json",
            ROOT/"research/round20/advisor/h2-gate.json", ROOT/"research/round20/reverse/h2/report.md",
            ROOT/"research/round20/reverse/h2/check.py", ROOT/"research/round20/advisor/g2-gate.json",
            ROOT/"research/round20/reverse/g2/report.md", ROOT/"research/round19/advisor/a2-gate.json",
            ROOT/"research/round19/backward/a2/report.md", ROOT/"research/round21/advisor/j2-gate.json",
            ROOT/"research/round21/reverse/j1/report.md", ROOT/"research/round21/reverse/j2/report.md"]
    manifest={"schema":"ym21-source-manifest-v1",
              "inputs":{str(path.relative_to(ROOT)):sha(path) for path in sorted(set(inputs))},
              "outputs":{name:sha(out/name) for name in sorted(outputs)}}
    (out/"source-manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
    print(json.dumps({"loop":"m2","direction":"reverse","passed":True,"profile_rows":str(len(profile_rows)),
                      "rejected_inputs":str(len(rejected)),"scientific_outputs":str(len(outputs))}))


if __name__ == "__main__":
    main()
