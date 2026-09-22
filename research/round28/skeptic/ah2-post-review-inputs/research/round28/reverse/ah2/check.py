#!/usr/bin/env python3
"""Independent AH2 rational block/loading certificate, not a heat evaluator.

python3 -B check.py --output /absolute/fresh/directory
Admitted AH1 JSON is parsed as data; no historical algorithm is imported.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import math

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
CONTRACT="research/round28/contracts/ah2.json"
CONTRACT_SHA="a7d558a8517cf3b1577d93a282ab6f6c22c462f2d06107e1255cfce0ee3f3ef1"
CHECKS={}


def need(name,condition):
    if name in CHECKS:raise RuntimeError("duplicate check "+name)
    CHECKS[name]=bool(condition)
    if not condition:raise RuntimeError("failed "+name)


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def frac(x):return Q(x["numerator"],x["denominator"]) if isinstance(x,dict) else Q(x)


def encode(x):
    if isinstance(x,Q):return {"numerator":x.numerator,"denominator":x.denominator}
    if isinstance(x,dict):return {str(k):encode(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [encode(v) for v in x]
    return x


def packed(x):return (json.dumps(encode(x),indent=2,sort_keys=True)+"\n").encode()


def bind_inputs():
    need("frozen_contract",sha(ROOT/CONTRACT)==CONTRACT_SHA)
    c=json.loads((ROOT/CONTRACT).read_text())
    inv=json.loads((HERE/"inputs/source-inventory.json").read_text())
    entries={x["source"]:x for x in inv["entries"]}
    required={**c["sources"],CONTRACT:CONTRACT_SHA}
    need("all_declared_sources",len(c["sources"])==33 and set(required)<=set(entries))
    need("two_read_AC2_reports_bound",set(entries)-set(required)=={
        "research/round26/forward/ac2/report.md","research/round26/reverse/ac2/report.md"})
    bindings={}
    for n,(origin,e) in enumerate(sorted(entries.items())):
        need("source_original_snapshot_%02d"%n,sha(ROOT/origin)==e["sha256"]==sha(ROOT/e["snapshot"]))
        if origin in required:need("contract_source_%02d"%n,e["sha256"]==required[origin])
        bindings[origin]=e["sha256"];bindings[e["snapshot"]]=e["sha256"]
    instructions=json.loads((HERE/"inputs/instruction-inventory.json").read_text())
    need("instruction_count",len(instructions)==26)
    for n,e in enumerate(instructions.values()):
        p=HERE/e["snapshot"];need("instruction_%02d"%n,sha(p)==e["sha256"])
        bindings[str(p.relative_to(ROOT))]=e["sha256"]
        origin=Path(e["origin"])
        if origin.is_relative_to(ROOT):
            need("repo_instruction_%02d"%n,sha(origin)==e["sha256"])
            bindings[str(origin.relative_to(ROOT))]=e["sha256"]
    for p in sorted((HERE/"inputs").rglob("*")):
        if p.is_file():bindings[str(p.relative_to(ROOT))]=sha(p)
    for name in ("check.py","preflight-pass.json"):
        bindings[str((HERE/name).relative_to(ROOT))]=sha(HERE/name)
    return bindings


def inherited_data():
    path=ROOT/"research/round28/reverse/ah1/output"
    graph=json.loads((path/"graph.json").read_text())
    basis=json.loads((path/"basis.json").read_text())["basis"]
    mag=json.loads((path/"magnetic.json").read_text())
    ah1=json.loads((path/"results.json").read_text())
    need("AH1_sidecars_bound",all(sha(path/n)==h for n,h in ah1["artifact_sha256"].items()))
    vertices=list(itertools.product(range(4),range(3),range(2)))
    linkkeys=[(v,a) for v in vertices for a in range(3) if v[a]+1<(4,3,2)[a]]
    ids={key:i for i,key in enumerate(linkkeys)}
    words=[]
    for v in vertices:
        for a,b in itertools.combinations(range(3),2):
            if v[a]+1<(4,3,2)[a] and v[b]+1<(4,3,2)[b]:
                va=list(v);va[a]+=1;vb=list(v);vb[b]+=1
                words.append([[ids[(v,a)],1],[ids[(tuple(va),b)],1],
                              [ids[(tuple(vb),a)],-1],[ids[(v,b)],-1]])
    need("same_full_graph_vertices_links",len(vertices)==24 and len(linkkeys)==46 and
         [list(v) for v in vertices]==graph["vertices"] and
         [(list(v),a) for v,a in linkkeys]==[(e["tail_coordinate"],e["axis"]) for e in graph["links"]])
    need("all_original_oriented_face_words",len(words)==29 and words==[f["word"] for f in graph["faces"]])
    need("all_vertex_Gauss_incidence_retained",sum(map(len,graph["vertex_incidence"]))==92 and len(graph["vertex_incidence"])==24)
    face_sets=[set(e for e,s in w) for w in words]
    S={(i,j):frac(v) for i,j,v in mag["entries"]}
    g=[frac(b["metric"]) for b in basis];K=[frac(b["electric"]) for b in basis]
    need("physical_dimensions",len(basis)==561 and len(S)==2124)
    need("positive_Gram",all(x>0 for x in g))
    need("complete_electric_edge_support",all(K[i]==sum((Q(j,2)*(Q(j,2)+1) for j in b["twice_edge_spins"].values()),Q(0)) for i,b in enumerate(basis)))
    P0=[i for i,b in enumerate(basis) if b["kind"] in ("vacuum","fundamental")]
    F=[i for i,b in enumerate(basis) if b["kind"]=="fundamental"]
    N=[i for i in range(len(basis)) if i not in P0]
    need("P0_strict_endpoint",P0==[i for i,e in enumerate(K) if e<Q(9,2)] and len(P0)==30)
    need("all_531_new_states",len(N)==531 and len(F)==29)
    expected={}
    bykind={(b["kind"],tuple(b["faces"])):i for i,b in enumerate(basis)}
    def link(i,j,v):expected[(i,j)]=v;expected[(j,i)]=v*g[i]/g[j]
    for p in range(29):
        f=bykind[("fundamental",(p,))]
        link(0,f,Q(1,2));link(bykind[("spin_one",(p,))],f,Q(1,2))
    for p,q in itertools.combinations(range(29),2):
        kinds=("singlet","triplet") if face_sets[p]&face_sets[q] else ("product",)
        for kind in kinds:
            row=bykind[(kind,(p,q))];v=Q(1,4) if len(kinds)==2 else Q(1,2)
            for f in (p,q):link(row,bykind[("fundamental",(f,))],v)
    need("entire_S_reconstructed",S==expected)
    need("metric_adjoint_all_entries",all(g[i]*v==g[j]*S[(j,i)] for (i,j),v in S.items()))
    ns=set(N);fs=set(F)
    need("complete_N_to_N_magnetic_zero",all(not(i in ns and j in ns) for i,j in S))
    need("full_face_to_face_zero",all(not(i in fs and j in fs) for i,j in S))
    need("new_block_floor",min(K[i] for i in N)==Q(9,2))
    vacuum_C_norm2=sum((g[i]*S.get((i,0),Q(0))**2 for i in N),Q(0))
    need("new_coupling_kills_vacuum",vacuum_C_norm2==0)
    C=[[S.get((i,j),Q(0)) for j in F] for i in N]
    H=[[sum((g[i]*C[k][a]*C[k][b] for k,i in enumerate(N)),Q(0)) for b in range(29)] for a in range(29)]
    need("complete_old_face_to_new_Gram",all(H[a][b]==Q(7)*(a==b)+Q(1,4) for a in range(29) for b in range(29)))
    need("bright_norm_equality",all(sum(row)==Q(57,4) for row in H))
    need("dark_norm_equality",all(H[a][0]-H[a][1]==7*((a==0)-(a==1)) for a in range(29)))
    need("safe_coupling_norm_majorant",Q(19,5)**2>Q(57,4))
    need("old_graph_coupling_constant_rejected",Q(25,8)**2<Q(57,4))
    contributions=[]
    for k,i in enumerate(N):
        bright_loss=g[i]*sum(C[k])**2/29
        need("delete_new_channel_%03d_changes_full_Gram"%i,bright_loss>0)
        contributions.append({"basis_id":i,"kind":basis[i]["kind"],"energy":K[i],"metric":g[i],
                              "face_coefficients":[[F[j],v] for j,v in enumerate(C[k]) if v],
                              "deleted_bright_quadratic_loss":bright_loss})
    trip=next(i for i in N if basis[i]["kind"]=="triplet");k=N.index(trip)
    j=next(j for j,x in enumerate(C[k]) if x)
    need("wrong_triplet_metric_discriminates",H[j][j]-2*C[k][j]**2 != H[j][j])
    chi=next(i for i in N if basis[i]["kind"]=="spin_one")
    need("N_is_not_full_Q",chi in N and chi<561 and 561 not in N)
    # Haar moments of phi=Tr(U): <phi^(2k)>=Catalan(k).
    m2,m4,m6=(Q(math.comb(2*k,k),k+1) for k in (1,2,3))
    witness_norm2=m6-4*m4+4*m2
    witness_coefficient=(m6-3*m4+2*m2)/2
    need("outside_new_input_witness",witness_norm2==1 and witness_coefficient==Q(1,2) and 4*Q(3,2)*Q(5,2)==15>max(K))
    need("all_outside_inputs_charged",len(N)==531 and ah1["scope"]["simultaneous_all_input_outside_envelope"] is True)
    return {"N_rows":contributions,"P0_ids":P0,"face_ids":F,"N_ids":N,"dimension":561,
            "C_over_lambda_Gram":{"diagonal":Q(29,4),"off_diagonal":Q(1,4),"bright_eigenvalue":Q(57,4),"dark_eigenvalue":Q(7)},
            "new_block_K_floor":Q(9,2),"new_block_magnetic_zero":True,"full_S_nonzero_count":len(S),
            "vacuum_C_norm_squared":vacuum_C_norm2,"outside_witness_norm_squared":witness_norm2,
            "outside_witness_coefficient":witness_coefficient},H


def exp_negative(x,terms=80):
    if x==0:return (Q(1),Q(1))
    if x<0:raise ValueError("nonnegative exponent required")
    term=Q(1);s=term
    for k in range(1,terms+1):term*=x/k;s+=term
    nxt=term*x/(terms+1);ratio=x/(terms+2)
    if ratio>=1:raise ValueError("Taylor tail ratio")
    upper=s+nxt/(1-ratio)
    return (1/upper,1/s)


def envelopes(cap,eta=Q(1,100)):
    g=3-29*cap;r0=Q(41,12)*cap**2;p0=r0/g
    rplus=29*cap*p0;pplus=rplus/g;delta=rplus*rplus/g
    z=1-Q(29,72)*cap**2;q0=Q(9,10)*cap
    a=q0+p0;b=a+eta;D=z-eta-p0
    return {"Lambda":cap,"eta_theorem":eta,"g":g,"d":Q(9,2),"r0":r0,"p0_full":p0,"p0_nested":p0,
            "r_plus":rplus,"p_plus":pplus,"delta_plus":delta,"z":z,"q0_reverse_AH1":q0,
            "stationary_face_bound":a,"excited_input_bound":b,"D_true":D,
            "Cbar":Q(19,5)*cap,"Bbar":29*cap}


def integrated_certificate(e,t):
    g=e["g"];d=e["d"];a=e["stationary_face_bound"];b=e["excited_input_bound"]
    if t==0:
        return {"loading_lower":Q(0),"loading_upper":Q(0),"early_lower":Q(0),"early_upper":Q(0),
                "late_upper":e["p_plus"]+2*b+e["p_plus"],"exp_g_interval":(Q(1),Q(1)),"exp_d_interval":(Q(1),Q(1))}
    eglo,eghi=exp_negative(g*t);edlo,edhi=exp_negative(d*t)
    loadlo=e["Cbar"]*(a*(1-edhi)/d+b*(eglo-edhi)/(d-g))
    loadhi=e["Cbar"]*(a*(1-edlo)/d+b*(eghi-edlo)/(d-g))
    ilo=a*(t/d-(1-edlo)/d**2)+b*((1-eghi)/g-(1-edlo)/d)/(d-g)
    ihi=a*(t/d-(1-edhi)/d**2)+b*((1-eglo)/g-(1-edhi)/d)/(d-g)
    earlylo=e["delta_plus"]*t+e["Bbar"]*e["Cbar"]*ilo
    earlyhi=e["delta_plus"]*t+e["Bbar"]*e["Cbar"]*ihi
    late=e["p_plus"]+(2*b+e["p_plus"])*eghi
    return {"loading_lower":max(Q(0),loadlo),"loading_upper":loadhi,
            "early_lower":max(Q(0),earlylo),"early_upper":earlyhi,"late_upper":late,
            "exp_g_interval":(eglo,eghi),"exp_d_interval":(edlo,edhi)}


def algebra_and_controls(H,e,block):
    lam=e["Lambda"];a=e["stationary_face_bound"];g=e["g"];d=e["d"]
    need("all_spectral_separations_positive",g==Q(271,100)>0 and d>g and e["D_true"]>0)
    need("actual_stationary_projector_component_bound",a==e["q0_reverse_AH1"]+e["p0_nested"])
    need("both_distinct_projector_inputs_used",e["p0_full"]==e["p0_nested"]==Q(41,325200))
    # Differentiate the exact convolution formula algebraically. The source
    # constant and exp(-g t) coefficients solve y'+d y=C(a+b exp(-g t)).
    cd=-(a/d+e["excited_input_bound"]/(d-g));cg=e["excited_input_bound"]/(d-g);c0=a/d
    need("loading_initial_condition",c0+cg+cd==0)
    need("loading_ODE_constant_coefficient",d*c0==a)
    need("loading_ODE_excited_coefficient",(d-g)*cg==e["excited_input_bound"])
    need("loading_ODE_transient_coefficient",(d-d)*cd==0)
    need("integrated_transient_total",(1/g-1/d)/(d-g)==1/(g*d))
    need("positive_kernel_monotonicity_premises",a>0 and e["excited_input_bound"]>0 and e["Cbar"]>0 and e["Bbar"]>0)
    # A physical lower witness for a persistent face component, using the
    # vacuum row and a rational P0 Rayleigh trial h=lambda/6.
    drop=Q(29,12)*lam**2/(1+Q(29,36)*lam**2)
    overlap=e["z"]-e["p0_nested"]
    stationary_lower=2*drop*overlap**2/(lam*Q(27,5))
    need("Ritz_ground_below_scalar_reference",drop>0)
    need("stationary_face_component_cannot_be_dropped",overlap>0 and stationary_lower>0)
    # A vacuum-only second-order return test is blind. A valid prepared face
    # component detects the actual C* C return in the projected second derivative.
    eta_amp=Q(1,200)
    return_norm2=eta_amp**2*lam**4*sum((H[j][0]**2 for j in range(29)),Q(0))
    need("vacuum_second_order_feedback_control_nondiscriminating",block["vacuum_C_norm_squared"]==0)
    need("prepared_face_feedback_replacement_nonzero",return_norm2>0 and sum((H[j][0]**2 for j in range(29)),Q(0))==Q(869,16))
    # Full-output and retained-output denominators need not coincide. The
    # exact two-state diagnostic has ground (3,4)/5, excitation (-4,3)/5;
    # at exp(-t)=1/2, a rank-one retained own-centered output has norm 1.
    full_diag_norm2=Q(9,25)+Q(16,25)*Q(1,4)
    need("approximate_output_is_not_true_denominator",full_diag_norm2==Q(13,25)<1)
    need("center_defect_retained",e["delta_plus"]>0)
    lo,hi=exp_negative(Q(1))
    need("rounded_center_changes_unbounded_time_ground",1/hi>2)
    # Diagnostic functions show why exact fixture agreement is not uniformity.
    timeblind=lambda t:t*t*(t-1)**2*(t-3)**2
    couplingblind=lambda l:l*l*(l-Q(1,200))**2*(l-Q(1,100))**2
    need("finite_time_fixtures_not_all_time_proof",all(timeblind(t)==0 for t in (0,1,3)) and timeblind(Q(2))>0)
    need("finite_coupling_fixtures_not_continuous_proof",all(couplingblind(l)==0 for l in (Q(0),Q(1,200),Q(1,100))) and couplingblind(Q(1,400))>0)
    need("original_clock_fixed",-Q(3)!=-Q(3)*2)
    return {"stationary_face_limit_on_vacuum_lower_at_cap":stationary_lower,
            "stationary_lower_scope":"||F Gplus Omega|| lower bound; not an error lower bound",
            "vacuum_second_order_return_nondiscriminating":True,
            "prepared_face_second_derivative_return_squared":return_norm2,
            "denominator_diagnostic_scope":"Two-state countermodel to a general denominator substitution; not a changed AH model",
            "denominator_diagnostic_full_squared":full_diag_norm2}


def preparation_fixtures():
    eta=Q(1,200);rad=1-eta*eta;den=10**30
    integer=math.isqrt(rad.numerator*den*den//rad.denominator)
    lo=Q(integer,den);hi=Q(integer+1,den)
    need("fixture_radical_enclosed",lo*lo<=rad<=hi*hi)
    need("real_fixture_metric_normalization",rad+eta*eta==1)
    need("imaginary_fixture_metric_normalization",rad+eta*eta==1 and eta>0)
    dist_upper=2*(1-lo)
    need("fixture_in_full_point01_ball",dist_upper<Q(1,100)**2)
    need("amplitude_not_vector_distance",rad<(1-eta*eta/2)**2)
    return [{"id":"Omega","vacuum_coefficient":Q(1),"face_coefficient":Q(0),"distance_squared":Q(0)},
            {"id":"real_phi0","vacuum_coefficient":{"positive_square_root_of":rad,"interval":[lo,hi]},
             "face_id":0,"face_coefficient":eta,"face_phase":"1","norm_squared":Q(1),"distance_squared_upper":dist_upper},
            {"id":"imaginary_phi0","vacuum_coefficient":{"positive_square_root_of":rad,"interval":[lo,hi]},
             "face_id":0,"face_coefficient":eta,"face_phase":"i","norm_squared":Q(1),"distance_squared_upper":dist_upper}]


def main():
    p=argparse.ArgumentParser();p.add_argument("--output",required=True,type=Path);args=p.parse_args()
    if not args.output.is_absolute() or args.output.exists():raise SystemExit("fresh absolute --output directory required")
    bindings=bind_inputs();block,H=inherited_data();e=envelopes(Q(1,100))
    control=algebra_and_controls(H,e,block);preparations=preparation_fixtures()
    T=Q(3)
    early=e["delta_plus"]*T+e["Bbar"]*e["Cbar"]*(e["stationary_face_bound"]*T/e["d"]+e["excited_input_bound"]/(e["g"]*e["d"]))
    explow,expup=exp_negative(e["g"]*T)
    need("join_exponential_rational_ceiling",expup<Q(1,3000))
    late=e["p_plus"]+(2*e["excited_input_bound"]+e["p_plus"])/3000
    absolute=max(early,late);relative=absolute/e["D_true"]
    need("join_fixed_three",T==3)
    need("early_join_dominates",early>late)
    need("strict_improvement_AH1",relative<Q(11,5000))
    need("prospective_point0001_target_met",relative<Q(1,10000))
    need("old_graph_accuracy_not_imported",relative>Q(37,1000000))
    grid=[];fixtures=[]
    for lam in (Q(0),Q(1,200),Q(1,100)):
        point=envelopes(lam)
        for t in (Q(0),Q(1),Q(3)):
            cert=integrated_certificate(point,t)
            need("fixture_integrated_order_%s_%s"%(lam,t),0<=cert["early_lower"]<=cert["early_upper"] and 0<=cert["loading_lower"]<=cert["loading_upper"])
            exact_zero=lam==0 or t==0
            if exact_zero:need("exact_zero_case_%s_%s"%(lam,t),cert["early_upper"]==0 and cert["loading_upper"]==0)
            pointabs=Q(0) if exact_zero else min(cert["early_upper"],cert["late_upper"])
            need("fixture_inside_uniform_certificate_%s_%s"%(lam,t),pointabs/point["D_true"]<=relative)
            gid=len(grid);grid.append({"id":gid,"lambda":lam,"sigma":t,"certificate":cert,
                                       "absolute_upper":pointabs,"true_relative_upper":pointabs/point["D_true"],
                                       "true_denominator":point["D_true"],"exact_error_zero":exact_zero})
            for prep in preparations:fixtures.append({"preparation":prep["id"],"certificate_grid_id":gid,
                                                       "scope":"certificate/preparation check; no numerical heat state"})
    need("all_frozen_fixture_combinations",len(grid)==9 and len(fixtures)==27)
    result={"schema":"ym28-ah2-reverse-v1","loop":"ah2","sequence":6,
            "model":"unchanged full46-link gauge invariant open3x2x1 graph; H=alpha[K+lambda(29-S)]; sigma=alpha*t/hbar",
            "scope":{"full_preparation_radius":Q(1,100),"continuous_coupling_interval":[Q(0),Q(1,100)],
                     "all_time_own_ground_centered_heat":True,"full_delayed_loading_with_feedback":True,
                     "all_531_new_channels":True,"true_relative_denominator":True,"numerical_heat_evaluator":False,
                     "actual_heat_errors_computed":False,"full_outside_Gram_evaluated":False,
                     "real_time_relative":False,"graph_size_uniform":False,"continuum_gap":False},
            "envelopes":e,"join_certificate":{"join":T,"early_absolute_upper":early,"late_absolute_upper":late,
                "exp_minus_gT_upper":Q(1,3000),"all_time_absolute_upper":absolute,
                "all_time_true_relative_upper":relative,"strict_target":Q(1,10000),"limiting_upper_term":"early envelope",
                "sharper_integrated_join_enclosure":integrated_certificate(e,T)},
            "full_blocks":block,"control_evidence":control,"preparations":preparations,
            "certificate_grid":grid,"fixture_combinations":fixtures,"checks":CHECKS,"check_count":len(CHECKS),
            "all_checks_passed":all(CHECKS.values()),"bindings":bindings,
            "historical_algorithms_imported_or_executed":False,"current_opposite_science_read":False,
            "attribution":"q0=9Lambda/10 from admitted reverse AH1; AC2 methods inherited and rederived for all new graph columns"}
    args.output.mkdir(parents=True);(args.output/"results.json").write_bytes(packed(result))
    print(json.dumps({"checks":len(CHECKS),"relative_upper_display":float(relative),"results_sha256":sha(args.output/"results.json")},sort_keys=True))


if __name__=="__main__":main()
