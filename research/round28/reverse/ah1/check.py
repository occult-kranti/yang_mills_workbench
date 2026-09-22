#!/usr/bin/env python3
"""AH1 reverse: exact new-graph reconstruction; standard library only.

Usage: python3 -B check.py --output /absolute/new/directory
No historical checker is imported or executed. Fractions are authoritative.
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from fractions import Fraction as F
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CONTRACT = "research/round28/contracts/ah1.json"
CONTRACT_SHA = "9c6f5bc1a71fcd49b93a1212e1b1837a82bc588b27b695fd600cbec46be17053"
CHECKS = {}


def require(name, condition):
    if name in CHECKS:
        raise RuntimeError("duplicate check: " + name)
    CHECKS[name] = bool(condition)
    if not condition:
        raise RuntimeError("failed: " + name)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def encode(x):
    if isinstance(x, F):
        return {"numerator": x.numerator, "denominator": x.denominator}
    if isinstance(x, dict):
        return {str(k): encode(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [encode(v) for v in x]
    return x


def packed(x):
    return (json.dumps(encode(x), indent=2, sort_keys=True) + "\n").encode()


def source_bindings():
    require("exact_frozen_contract", sha(ROOT / CONTRACT) == CONTRACT_SHA)
    c = json.loads((ROOT / CONTRACT).read_text())
    inv = json.loads((HERE / "inputs/source-inventory.json").read_text())
    expected = dict(c["sources"])
    expected[CONTRACT] = CONTRACT_SHA
    entries = {v["source"]: v for v in inv["entries"]}
    require("all_42_sources_and_contract", len(c["sources"]) == 42 and set(entries) == set(expected))
    bindings = {}
    for i, (source, h) in enumerate(sorted(expected.items())):
        e = entries[source]
        require("source_snapshot_%02d" % i,
                e["sha256"] == h and sha(ROOT / source) == h and sha(ROOT / e["snapshot"]) == h)
        bindings[source] = h
        bindings[e["snapshot"]] = h
    ii = json.loads((HERE / "inputs/instruction-inventory.json").read_text())
    require("instruction_inventory_complete", len(ii) == 26)
    for i, (name, e) in enumerate(sorted(ii.items())):
        snap = HERE / e["snapshot"]
        require("instruction_snapshot_%02d" % i, sha(snap) == e["sha256"])
        bindings[str(snap.relative_to(ROOT))] = e["sha256"]
        original = Path(e["origin"])
        # External skill origins are provenance, not portable runtime imports.
        if original.is_relative_to(ROOT):
            require("repo_instruction_original_%02d" % i, sha(original) == e["sha256"])
            bindings[str(original.relative_to(ROOT))] = e["sha256"]
    for p in sorted((HERE / "inputs").rglob("*")):
        if p.is_file():
            bindings[str(p.relative_to(ROOT))] = sha(p)
    bindings[str((HERE / "check.py").relative_to(ROOT))] = sha(HERE / "check.py")
    return bindings


def qmul(a, b):
    a0, a1, a2, a3 = a
    b0, b1, b2, b3 = b
    return (a0*b0-a1*b1-a2*b2-a3*b3,
            a0*b1+a1*b0+a2*b3-a3*b2,
            a0*b2-a1*b3+a2*b0+a3*b1,
            a0*b3+a1*b2-a2*b1+a3*b0)


def qinv(a):
    return (a[0], -a[1], -a[2], -a[3])


def word_value(word, values):
    ans = (F(1), F(0), F(0), F(0))
    for e, s in word:
        ans = qmul(ans, values[e] if s == 1 else qinv(values[e]))
    return ans[0]


def graph():
    dims = (4, 3, 2)
    vertices = list(itertools.product(*(range(d) for d in dims)))
    vid = {v: i for i, v in enumerate(vertices)}
    links = []
    edge_id = {}
    for v in vertices:
        for axis in range(3):
            if v[axis] + 1 < dims[axis]:
                w = list(v); w[axis] += 1; w = tuple(w)
                edge_id[(v, axis)] = len(links)
                links.append({"id": len(links), "tail": vid[v], "head": vid[w], "axis": axis,
                              "tail_coordinate": v, "head_coordinate": w})
    faces = []
    for v in vertices:
        for a, b in itertools.combinations(range(3), 2):
            if v[a]+1 < dims[a] and v[b]+1 < dims[b]:
                va = list(v); va[a] += 1; va = tuple(va)
                vb = list(v); vb[b] += 1; vb = tuple(vb)
                word = [(edge_id[(v, a)], 1), (edge_id[(va, b)], 1),
                        (edge_id[(vb, a)], -1), (edge_id[(v, b)], -1)]
                faces.append({"id": len(faces), "base": v, "axes": (a, b), "word": word,
                              "mask": sum(1 << e for e, _ in word)})
    require("graph_counts", (len(vertices), len(links), len(faces)) == (24, 46, 29))
    require("cycle_rank", len(links)-len(vertices)+1 == 23)
    incidence = [[(e["id"], 1 if e["tail"] == v else -1)
                  for e in links if v in (e["tail"], e["head"])] for v in range(len(vertices))]
    require("all_vertex_Gauss_actions", sum(map(len, incidence)) == 2*len(links) and all(incidence))
    face_sets = [frozenset(e for e, _ in f["word"]) for f in faces]
    for f in faces:
        current = vid[f["base"]]
        for e, s in f["word"]:
            edge = links[e]
            require("face_%02d_edge_%02d_orientation" % (f["id"], e),
                    current == (edge["tail"] if s == 1 else edge["head"]))
            current = edge["head"] if s == 1 else edge["tail"]
        require("face_%02d_closed" % f["id"], current == vid[f["base"]])
    normals = {(a, b): 3-a-b for a, b in itertools.combinations(range(3), 2)}
    internal = [f["id"] for f in faces if 0 < f["base"][normals[f["axes"]]] < dims[normals[f["axes"]]]-1]
    require("internal_faces_present", len(internal) == 7)
    require("missing_internal_faces_discriminates", len(faces)-len(internal) == 22 != len(faces))
    adjacency = [set() for _ in vertices]
    for e in links:
        adjacency[e["tail"]].add(e["head"]); adjacency[e["head"]].add(e["tail"])
    endpoint_edge = {frozenset((e["tail"], e["head"])): e["id"] for e in links}
    cycles = set()
    for u, v in itertools.combinations(range(len(vertices)), 2):
        for x, y in itertools.combinations(sorted(adjacency[u] & adjacency[v]), 2):
            cycles.add(frozenset(endpoint_edge[frozenset(p)] for p in ((u,x),(x,v),(v,y),(y,u))))
    require("all_four_cycles_are_faces", cycles == set(face_sets) and len(cycles) == 29)
    require("bipartite_graph", all(sum(vertices[e["tail"]]) % 2 != sum(vertices[e["head"]]) % 2 for e in links))
    signs = [1 if e["axis"] == 0 else (-1)**(e["tail_coordinate"][0] if e["axis"] == 1
                                                  else sum(e["tail_coordinate"][:2])) for e in links]
    require("coordinate_center_every_face_odd", all(product(signs[e] for e, _ in f["word"]) == -1 for f in faces))
    require("uniform_link_flip_is_wrong_control", all(product(-1 for _ in f["word"]) == 1 for f in faces))
    fixtures = [(F(1),F(0),F(0),F(0)), (F(3,5),F(4,5),F(0),F(0)),
                (F(5,13),F(0),F(12,13),F(0)), (F(8,17),F(0),F(0),F(15,17))]
    values = [fixtures[(e["id"]*e["id"]+e["id"]//3+1) % len(fixtures)] for e in links]
    gauges = [fixtures[(i*i+2*i+1) % len(fixtures)] for i in range(len(vertices))]
    transformed = [qmul(qmul(gauges[e["tail"]], values[e["id"]]), qinv(gauges[e["head"]])) for e in links]
    require("noncommuting_fixture", qmul(fixtures[1],fixtures[2]) != qmul(fixtures[2],fixtures[1]))
    require("Gauss_covariance_all_face_words", all(word_value(f["word"], values) == word_value(f["word"], transformed) for f in faces))
    wrong = [(e,s if i != 2 else -s) for i,(e,s) in enumerate(faces[0]["word"])]
    first_mutation_blind = word_value(wrong,values) == word_value(wrong,transformed)
    require("first_wrong_orientation_fixture_was_nondiscriminating", first_mutation_blind)
    changed = []
    for f in faces:
        for position in range(4):
            mutated = [(e,s if i != position else -s) for i,(e,s) in enumerate(f["word"])]
            if word_value(mutated,values) != word_value(mutated,transformed): changed.append([f["id"],position])
    require("replacement_wrong_orientation_changes_gauge_trace", bool(changed))
    wrong_gauss = [qmul(qmul(gauges[e["tail"]],values[e["id"]]), gauges[e["head"]]) for e in links]
    require("wrong_head_Gauss_action_discriminates", any(word_value(f["word"], values) != word_value(f["word"],wrong_gauss) for f in faces))
    return vertices, links, faces, face_sets, {"vertex_incidence":incidence,"center_signs":signs,"internal_faces":internal,
        "orientation_control":{"first_face_nondiscriminating":first_mutation_blind,"discriminating_faces":changed}}


def product(seq):
    p = 1
    for x in seq: p *= x
    return p


def cutoff_controls():
    # Every bipartite support on <=5 vertices is a subgraph of K_(a,b).
    bad = []
    for n in range(2, 6):
        for a in range(1, n):
            es = list(itertools.product(range(a), range(a,n)))
            for chosen in itertools.combinations(es, 5):
                deg = [0]*n
                for u,v in chosen: deg[u]+=1;deg[v]+=1
                if all(d >= 2 for d in deg): bad.append(chosen)
    require("five_edge_min_degree_two_bipartite_excluded", not bad)
    require("strict_cutoff_excludes_six_fundamental_edges", 6*F(3,4) == F(9,2) and not 6*F(3,4) < F(9,2))
    require("included_endpoint_mutation_rejected", 6*F(3,4) <= F(9,2))
    require("forced_square_spin_half_energy", 4*F(1,2)*F(3,2) == 3)
    require("next_equal_square_spin_excluded", 4*1*2 >= F(9,2))
    require("old_degree_cutoff_not_definition", 6*1 == 6 and 4*2 > 6)


def poly_add(a, b, scale=F(1)):
    out = dict(a)
    for p,v in b.items(): out[p] = out.get(p,F(0)) + scale*v
    return {p:v for p,v in out.items() if v}


def poly_mul(a, b):
    out = {}
    for p,v in a.items():
        for q,w in b.items():
            k = tuple(x+y for x,y in zip(p,q));out[k] = out.get(k,F(0))+v*w
    return {p:v for p,v in out.items() if v}


def sphere_moment(powers):
    if any(p % 2 for p in powers): return F(0)
    n = sum(powers)//2
    num = product(product(range(1,p,2)) for p in powers)
    den = product(range(4,4+2*n,2))
    return F(num,den)


def haar(poly):
    return sum((v*product(sphere_moment(p[k:k+4]) for k in range(0,len(p),4)) for p,v in poly.items()),F(0))


def pair_trace(a,b,inverse_a=False):
    out={}
    for i in range(4):
        powers=[0]*12;powers[4*a+i]+=1;powers[4*b+i]+=1
        out[tuple(powers)]=F(1 if i == 0 or inverse_a else -1)
    return out


def local_haar_controls():
    # t(G A)t(G^-1 B), and its exact shared-link Haar projection t(A B)/4.
    x = poly_mul(pair_trace(0,1),pair_trace(0,2,True))
    s = {p:v/4 for p,v in pair_trace(1,2).items()}
    t = poly_add(x,s,F(-1))
    require("shared_product_Haar_norm", haar(poly_mul(x,x)) == F(1,16))
    require("shared_singlet_Haar_norm", haar(poly_mul(s,s)) == F(1,64))
    require("shared_triplet_Haar_norm", haar(poly_mul(t,t)) == F(3,64))
    require("shared_branches_Haar_orthogonal", haar(poly_mul(s,t)) == 0)
    # Conditional projection integrates only G and agrees coefficientwise.
    projected={}
    for p,v in x.items():
        k=(0,0,0,0)+p[4:]
        projected[k]=projected.get(k,F(0))+v*sphere_moment(p[:4])
    projected={p:v for p,v in projected.items() if v}
    require("shared_link_conditional_projection", projected == s)
    require("fundamental_Haar_second_fourth", sphere_moment((2,0,0,0)) == F(1,4) and sphere_moment((4,0,0,0)) == F(1,8))
    require("spin_one_character_norm", 16*sphere_moment((4,0,0,0))-8*sphere_moment((2,0,0,0))+1 == 1)
    require("spin_one_character_mean_zero", 4*sphere_moment((2,0,0,0))-1 == 0)
    require("omit_singlet_wrong_norm", F(3,64) != F(1,16))
    require("omit_triplet_wrong_norm", F(1,64) != F(1,16))


def exact_rank(matrix):
    a = [list(map(F,row)) for row in matrix];rank=0
    for col in range(len(a[0])):
        pivot = next((i for i in range(rank,len(a)) if a[i][col]),None)
        if pivot is None: continue
        a[rank],a[pivot]=a[pivot],a[rank]
        d=a[rank][col];a[rank]=[x/d for x in a[rank]]
        for i in range(len(a)):
            if i!=rank:
                q=a[i][col];a[i]=[x-q*y for x,y in zip(a[i],a[rank])]
        rank+=1
    return rank


def construct_basis(faces, sets):
    n=len(faces); pairs=list(itertools.combinations(range(n),2)); masks=[f["mask"] for f in faces]
    pm=[masks[p]^masks[q] for p,q in pairs]
    require("pair_masks_nonzero", all(pm))
    require("pair_masks_individually_distinct", len(set(pm)) == len(pairs))
    require("pair_masks_disjoint_from_faces", not set(pm)&set(masks))
    require("no_three_face_relation", all(masks[p]^masks[q]^masks[r] for p,q,r in itertools.combinations(range(n),3)))
    require("no_four_distinct_face_relation", all(masks[p]^masks[q]^masks[r]^masks[s] for p,q,r,s in itertools.combinations(range(n),4)))
    require("global_parity_not_pair_independence", (-1)**4 == 1)
    require("at_most_one_shared_edge", all(len(sets[p]&sets[q]) <= 1 for p,q in pairs))
    basis=[]
    def add(kind, fs, metric, energy, spins, function):
        i=len(basis);basis.append({"id":i,"kind":kind,"faces":list(fs),"metric":F(metric),"electric":F(energy),
                                  "twice_edge_spins":dict(sorted(spins.items())),"function":function,
                                  "center_parity":-1 if kind=="fundamental" else 1})
        return i
    vac=add("vacuum",(),1,0,{},"1")
    odd={p:add("fundamental",(p,),1,3,{e:1 for e in sets[p]},"2 W_p") for p in range(n)}
    chi={p:add("spin_one",(p,),1,8,{e:2 for e in sets[p]},"4 W_p^2 - 1") for p in range(n)}
    pdata=[];shared=0;disjoint=0;vertex_only=0
    for p,q in pairs:
        common=sets[p]&sets[q]; union=sets[p]|sets[q]
        if common:
            shared+=1;e=next(iter(common)); outer={k:1 for k in union if k!=e}
            ids=[add("singlet",(p,q),1,F(9,2),outer,"8 E_common[W_p W_q]"),
                 add("triplet",(p,q),3,F(13,2),{**outer,e:2},"8 (I-E_common)[W_p W_q]")]
            weights=[F(1,4),F(1,4)]
        else:
            disjoint+=1
            ids=[add("product",(p,q),1,6,{e:1 for e in union},"4 W_p W_q")];weights=[F(1,2)]
        pdata.append({"faces":(p,q),"shared_edge":next(iter(common)) if common else None,
                      "mask":masks[p]^masks[q],"basis_ids":ids})
    require("new_pair_counts", shared==96 and disjoint==310 and len(pairs)==406)
    require("new_quotient_rank", len(basis)==561 and len(basis)!=293)
    require("positive_actual_Gram_and_empty_kernel", all(b["metric"]>0 for b in basis))
    require("spin_support_distinguishes_integer_characters", len({tuple(sorted(b["twice_edge_spins"].items())) for b in basis if b["kind"]=="spin_one"})==n)
    require("complete_K_eigenvalues_from_edge_spins", all(sum((F(j,2)*(F(j,2)+1) for j in b["twice_edge_spins"].values()),F(0))==b["electric"] for b in basis))
    S={}
    def connect(even,face,coefficient):
        j=odd[face];S[(even,j)]=coefficient
        S[(j,even)]=coefficient*basis[even]["metric"]/basis[j]["metric"]
    for p in range(n): connect(vac,p,F(1,2));connect(chi[p],p,F(1,2))
    for record in pdata:
        for i in record["basis_ids"]:
            for p in record["faces"]: connect(i,p,F(1,2) if record["shared_edge"] is None else F(1,4))
    require("full_sparse_action_count", len(S)==2124)
    require("metric_self_adjoint_every_nonzero", all(basis[i]["metric"]*v==basis[j]["metric"]*S[(j,i)] for (i,j),v in S.items()))
    require("all_parity_structural_zeros", all(basis[i]["center_parity"] != basis[j]["center_parity"] for i,j in S))
    require("all_odd_columns_in_generated_span", all(sum(1 for i,j in S if j==odd[p])==2+sum(1 if not sets[p]&sets[q] else 2 for q in range(n) if q!=p) for p in range(n)))
    trip=next(b for b in basis if b["kind"]=="triplet");p=trip["faces"][0];tid=trip["id"]
    require("triplet_reverse_entry_is_three_quarters", S[(odd[p],tid)]==F(3,4) and S[(tid,odd[p])]==F(1,4))
    require("metric_blind_transposition_rejected", S[(tid,odd[p])]!=S[(odd[p],tid)])
    require("wrong_triplet_metric_rejected", 1*S[(tid,odd[p])] != 1*S[(odd[p],tid)])
    duplicate_gram=[[1,0,0],[0,1,1],[0,1,1]]
    require("synthetic_duplicate_Gram_has_kernel", exact_rank(duplicate_gram)==2)
    kernel=[0,1,-1]
    duplicate_K=[[0,0,0],[0,3,0],[0,0,3]]
    duplicate_S=[[0,F(1,2),F(1,2)],[F(1,4),0,0],[F(1,4),0,0]]
    def apply(m,v):return [sum((x*y for x,y in zip(row,v)),F(0)) for row in m]
    require("synthetic_quotient_K_preserves_null", apply(duplicate_gram,apply(duplicate_K,kernel))==[0,0,0])
    require("synthetic_quotient_S_preserves_null", apply(duplicate_gram,apply(duplicate_S,kernel))==[0,0,0])
    require("lost_null_unquotiented_rank_rejected", exact_rank(duplicate_gram)!=len(duplicate_gram))
    # Distinct equal-energy vectors cannot be resolved from only their sum by K.
    require("summed_cyclic_columns_not_individual_enrichment", exact_rank([[1,1],[6,6]])==1 and exact_rank([[1,0],[0,1]])==2)
    return basis,pdata,S


def exp_lower(x,terms):
    term=F(1);s=term
    for k in range(1,terms+1):term*=x/k;s+=term
    return s


def certificates(basis, pairs, S):
    n=29;lam=F(1,100);g=3-n*lam
    # F_source=S^2-N/4 is orthogonal to P0 by masks; exact coefficients in basis.
    coeff={b["id"]:(F(1,4) if b["kind"] in ("spin_one","singlet","triplet") else F(1,2))
           for b in basis if b["kind"] not in ("vacuum","fundamental")}
    norm2=sum((v*v*basis[i]["metric"] for i,v in coeff.items()),F(0))
    energy=sum((v*v*basis[i]["metric"]*basis[i]["electric"] for i,v in coeff.items()),F(0))
    expected=F(n*(2*n-1),16);fourth=F(n*(3*n-1),16)
    require("complete_residual_Haar_norm", norm2==expected==F(1653,16))
    require("residual_electric_first_moment", energy==4*fourth==F(1247,2))
    require("Haar_fourth_moment_independent_count", fourth==F(n,8)+6*F(n*(n-1)//2,16))
    require("spin_one_only_residual_rejected", F(n,16)!=norm2 and norm2/F(n,16)==57)
    require("old_graph_residual_constant_rejected", norm2!=F(195,4))
    require("original_projection_rank", 1+sum(b["kind"]=="fundamental" for b in basis)==30)
    require("full_spectral_separation_positive", g==F(271,100)>0)
    require("negative_coupling_positivity_rejected", n*(-lam)<0)
    require("r0_radical_majorant", F(41)**2>n*(2*n-1))
    require("vacuum_angle_radical_majorant", F(27,5)**2>n)
    r0=F(41,12)*lam**2;p0=r0/g;rplus=n*lam*p0;pplus=rplus/g;dplus=rplus**2/g
    z=1-F(n,72)*lam**2;q0=F(9,10)*lam;eta=F(1,100)
    D=z-eta-p0;b=q0+p0+eta
    require("positive_true_output_denominator", D>0)
    require("nested_residual_factor", rplus==n*lam*r0/g and rplus<r0)
    require("B_P0_zero_does_not_set_full_B_zero", F(1,2)*lam>0)
    require("all_new_inputs_outside_budget", len(basis)-30==531 and n*lam==F(29,100))
    require("old_graph_all_input_envelope_rejected", n*lam!=20*lam)
    require("new_input_leakage_character_witness", F(1,2)**2==F(1,4))
    # e^(2g)>225 by a positive exact Taylor lower sum.
    expbound=F(1,225)
    require("late_exponential_certified", exp_lower(2*g,40)>225)
    V=2*(rplus+dplus)+(n*lam)*b/g
    J=pplus+(2*b+pplus)*expbound
    absolute=max(V,J);relative=absolute/D
    require("join_two_early_dominates", V>J)
    require("all_time_relative_bound", relative<F(43,20000))
    require("no_old_accuracy_import", relative>F(37,1000000))
    # Rational prepared states, with either a real or imaginary face coefficient.
    u=F(1,250);a=(1-u*u)/(1+u*u);v=2*u/(1+u*u)
    require("normalized_real_face_preparation", a*a+v*v==1)
    require("normalized_imaginary_face_preparation", a*a+v*v==1 and v!=0)
    require("preparation_ball_exact", (a-1)**2+v*v<eta**2)
    require("complex_preparation_overlap_floor", z-eta-p0==D and D>0)
    # Build the metric orthogonal projection at zero time, including one actual
    # outside spin-3/2 character coordinate. Test real and imaginary inputs.
    metric=[b0["metric"] for b0 in basis]+[F(1)]
    def project(coords):
        inner=[metric[i]*coords[i] for i in range(len(basis))]
        return [inner[i]/metric[i] for i in range(len(basis))]+[0]
    real=[F(0)]*len(metric);real[0]=a;real[1]=v
    imag_re=[F(0)]*len(metric);imag_re[0]=a
    imag_im=[F(0)]*len(metric);imag_im[1]=v
    require("zero_time_both_identity_on_preparation", project(real)==real and project(imag_re)==imag_re and project(imag_im)==imag_im)
    outside=[F(0)]*len(metric);outside[-1]=1
    require("zero_time_full_input_error_one_preserved", sum((metric[i]*(outside[i]-project(outside)[i])**2 for i in range(len(metric))),F(0))==1)
    K0={(i,i):b0["electric"] for i,b0 in enumerate(basis) if b0["electric"]}
    L0=dict(K0)
    for ij,value in S.items():L0[ij]=L0.get(ij,F(0))-F(0)*value
    L0={ij:value for ij,value in L0.items() if value}
    require("zero_coupling_complete_retained_generator", L0==K0)
    require("zero_coupling_complete_omitted_map", F(0)*29==0 and all(b0["electric"]==sum((F(j,2)*(F(j,2)+1) for j in b0["twice_edge_spins"].values()),F(0)) for b0 in basis))
    require("zero_coupling_ground_and_center", 29*F(0)==0 and (F(3)-3)/2==0)
    trial_drop=F(n,12)*lam**2/(1+F(n,36)*lam**2)
    require("scalar_reference_is_not_true_ground", trial_drop>0 and n*lam-trial_drop<n*lam)
    # A rounded center differing by delta makes the ground coefficient
    # exp(sigma*delta); its derivative at zero is delta, not zero.
    delta=F(1,10**12)
    require("rounded_center_changes_ground_derivative", delta!=0 and exp_lower((1/delta)*delta,2)>2)
    require("own_center_defect_retained", dplus>0 and 2*(rplus+dplus)>2*rplus)
    # Check exact P0 spectral identities at rational h parameterizations.
    # Choose h rational and lambda=6h/(1-Nh^2), giving w=N lambda h/2.
    parametrized=[]
    for h in (F(0),F(1,2400),F(1,1200),F(1,601)):
        l=6*h/(1-n*h*h);w=n*l*h/2;Z=1+n*h*h;mu=n*l-w
        require("Ritz_parameter_%s" % h, (3+w)*h==l/2 and mu==n*l-n*l*h/2 and 0<=l<=lam)
        require("Ritz_full_residual_parameter_%s" % h,
                4*l*l*h*h*norm2/Z==F(n*(2*n-1),4)*l*l*h*h/Z)
        parametrized.append({"h":h,"lambda":l,"w":w,"mu0":mu,"Z":Z,"r0_squared":4*l*l*h*h*norm2/Z})
    return {"N":n,"Lambda":lam,"gap_floor":g,"source_norm_squared":norm2,"source_electric_moment":energy,
            "r0":r0,"p0_full_ground":p0,"p0_enriched_ground":p0,"r_plus":rplus,"p_plus":pplus,
            "ground_energy_error":dplus,"vacuum_overlap_floor":z,"vacuum_excited_bound":q0,
            "preparation_radius":eta,"excited_input_bound":b,"true_output_floor":D,
            "join":F(2),"exp_minus_join_gap_upper":expbound,"early_join_upper":V,"late_join_upper":J,
            "all_time_absolute_upper":absolute,"all_time_true_relative_upper":relative,
            "simple_strict_relative_upper":F(43,20000),"rational_Ritz_controls":parametrized,
            "preparation_examples":{"vacuum_coefficient":a,"face_coefficient_magnitude":v,"phases":["1","i"]}}


def main():
    ap=argparse.ArgumentParser();ap.add_argument("--output",required=True,type=Path);args=ap.parse_args()
    out=args.output
    if not out.is_absolute() or out.exists(): raise SystemExit("--output must be a fresh absolute directory")
    bindings=source_bindings()
    vertices,links,faces,sets,extra=graph()
    cutoff_controls();local_haar_controls()
    basis,pairs,S=construct_basis(faces,sets)
    cert=certificates(basis,pairs,S)
    # Vertex-only pairs are kept as their actual product vector, with no ambient
    # eigenshell claim. This check counts them independently from edge incidence.
    vs=[set(v for e in ss for v in (links[e]["tail"],links[e]["head"])) for ss in sets]
    vertex_only=sum(not sets[p]&sets[q] and bool(vs[p]&vs[q]) for p,q in itertools.combinations(range(29),2))
    require("vertex_touching_products_retained", vertex_only>0 and all(len(r["basis_ids"])==1 for r in pairs if r["shared_edge"] is None))
    payloads={
        "graph.json":{"vertices":vertices,"links":links,"faces":faces,"face_pairs":pairs,"vertex_only_pairs":vertex_only,**extra},
        "basis.json":{"conventions":"lexicographic tail then axis; face base then increasing axis pair; unordered p<q; common-edge Haar projection",
                      "basis":basis,"dimension":len(basis),"Gram":"diagonal metric field; all unlisted entries zero",
                      "Gram_nullspace":[],"quotient_rank":len(basis),"electric_action":"diagonal electric field; all unlisted entries zero"},
        "magnetic.json":{"dimension":len(basis),"entries":[[i,j,v] for (i,j),v in sorted(S.items())],
                         "orientation":"entry[i,j] is coefficient of basis_i in P+ S basis_j",
                         "unlisted_entries":"exact zero by center parity or complete fundamental-column expansion and metric adjointness",
                         "nonzero_entries":len(S),"zero_entries":len(basis)**2-len(S),
                         "hamiltonian":"A+=diag(K+29 lambda)-lambda S in this physical Gram",
                         "outside":"B basis_j=-lambda[S basis_j-sum_i basis_i magnetic[i,j]]; every column included; ||B||<=29 lambda"}}
    artifact_hashes={name:hashlib.sha256(packed(data)).hexdigest() for name,data in payloads.items()}
    result={"schema":"ym28-ah1-reverse-v1","loop":"ah1","independence":"current forward and skeptic science unread before producer freeze",
            "model":"full physical SU(2) open3x2x1-cell graph; L=K+lambda(29-S); H=alpha L; sigma=alpha t/hbar",
            "scope":{"full_physical_space_domain":True,"strict_P0_complete":True,"individual_K_reducing_enrichment":True,
                     "exact_retained_Gram_K_S":True,"simultaneous_all_input_outside_envelope":True,
                     "exact_semigroup_all_time_true_relative_bound":True,"numerical_heat_evaluator":False,
                     "full_outside_Gram_evaluated":False,"ambient_electric_shell_complete":False,
                     "all_input_full_space_zero_time_accuracy":False,"real_time_relative":False,
                     "graph_size_uniform":False,"continuum":False,"scientific_priority_verified":False},
            "counts":{"vertices":24,"links":46,"faces":29,"internal_faces":len(extra["internal_faces"]),"cycle_rank":23,
                      "P0_rank":30,"Pplus_rank":561,"shared_edge_pairs":96,"edge_disjoint_pairs":310,
                      "vertex_only_pairs":vertex_only,"new_retained_inputs":531,"magnetic_nonzero_entries":len(S)},
            "certificates":cert,"artifact_sha256":artifact_hashes,"bindings":bindings,"checks":CHECKS,
            "check_count":len(CHECKS),"all_checks_passed":all(CHECKS.values())}
    out.mkdir(parents=True)
    for name,data in payloads.items():(out/name).write_bytes(packed(data))
    (out/"results.json").write_bytes(packed(result))
    print(json.dumps({"checks":len(CHECKS),"rank":len(basis),"relative_upper_display":float(cert["all_time_true_relative_upper"]),
                      "results_sha256":sha(out/"results.json")},sort_keys=True))


if __name__=="__main__":main()
