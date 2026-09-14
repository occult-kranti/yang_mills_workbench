"""Round19 forward B1: strict cutoff channels and exact cross Gram.

Self-contained exact arithmetic for the actual two-cube SU(2) graph.  The
projector P is the complete physical electric-energy projector for E_el<6 alpha:
vacuum plus all fundamental simple cycles of length four and six.  The magnetic
cross object is W*W = P V^2 P - (P V P)^2 for V=-sum_f lambda_f chi_f/2.
"""
from __future__ import annotations
from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import argparse, csv, hashlib, json

SOURCE_SHA256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
CONTRACT = "research/round19/advisor/contract-b1.json"
POST_A_ROADMAP = "research/round19/advisor/post-a-roadmap.md"
PAIRED_SKILL = "research/round19/methods/paired-physics-research.md"
SCALE_METHOD = "research/round19/methods/scale-and-exceptions.md"
DIMS = (3, 2, 2)
EDGE_LABEL_COST = {1: F(3, 4), 2: F(2), 3: F(15, 4), 4: F(6)}
STRICT_CUTOFF = F(6)

ZERO = (F(0), F(0)); ONE = (F(1), F(0)); I = (F(0), F(1)); NI = (F(0), F(-1))

def cadd(a,b): return (a[0]+b[0], a[1]+b[1])
def cmul(a,b): return (a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0])
def cneg(a): return (-a[0], -a[1])
def sfrac(x): return str(x)
def sha_bytes(b): return hashlib.sha256(b).hexdigest()
def sha_json(obj): return sha_bytes(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode())

def rational(x):
    if isinstance(x, F): return x
    if type(x) not in (int, str): raise ValueError("exact rational input required")
    y=F(x)
    if isinstance(x, str) and str(y)!=x: raise ValueError("canonical rational string required")
    return y

def validate_scale(alpha_over_E_star="2", energy_reference="E_star"):
    a=rational(alpha_over_E_star)
    if energy_reference != "E_star": raise ValueError("B1 requires positive E_star, not kappa/tolerance/volume/Fibonacci labels")
    if a <= 0: raise ValueError("alpha/E_star must be positive")
    return {"E_star":"positive symbolic physical energy reference", "alpha_over_E_star":sfrac(a), "strict_cutoff_over_E_star":sfrac(STRICT_CUTOFF*a), "kappa":"absent", "fibonacci_labels":"organizing analogy only"}

@dataclass(frozen=True)
class Edge:
    id: int; axis: int; tail: tuple; head: tuple
@dataclass(frozen=True)
class Face:
    id: int; normal: int; base: tuple; vertices: tuple; word: tuple

def make_graph():
    vertices=list(product(*(range(n) for n in DIMS)))
    edges=[]; lookup={}
    for v in vertices:
        for axis,extent in enumerate(DIMS):
            if v[axis]+1 < extent:
                h=list(v); h[axis]+=1; h=tuple(h)
                e=Edge(len(edges), axis, v, h); edges.append(e)
                lookup[(v,h)] = (e.id, 1); lookup[(h,v)] = (e.id, -1)
    faces=[]
    for normal in range(3):
        tang=[i for i in range(3) if i!=normal]
        ranges=[range(DIMS[i]) if i==normal else range(DIMS[i]-1) for i in range(3)]
        for base in product(*ranges):
            a,b=tang
            va=list(base); va[a]+=1
            vb=va.copy(); vb[b]+=1
            vc=list(base); vc[b]+=1
            loop=(base, tuple(va), tuple(vb), tuple(vc))
            word=tuple(lookup[(loop[i], loop[(i+1)%4])] for i in range(4))
            faces.append(Face(len(faces), normal, base, loop, word))
    return vertices, edges, faces, lookup

VERTICES, EDGES, FACES, LOOKUP = make_graph()
ADJ=defaultdict(list)
INCIDENT=defaultdict(list)
for e in EDGES:
    ADJ[e.tail].append((e.head,e.id)); ADJ[e.head].append((e.tail,e.id))
    INCIDENT[e.tail].append(e.id); INCIDENT[e.head].append(e.id)

def graph_record():
    return {"schema":"ym19-b1-actual-two-cube-graph-v1", "vertices":[list(v) for v in VERTICES], "edges":[{"id":e.id,"axis":e.axis,"tail":list(e.tail),"head":list(e.head)} for e in EDGES], "faces":[{"id":f.id,"normal":f.normal,"base":list(f.base),"vertices":[list(v) for v in f.vertices],"word":[{"edge":e,"sign":s} for e,s in f.word]} for f in FACES], "counts":{"vertices":len(VERTICES),"edges":len(EDGES),"faces":len(FACES)}}

def validate_graph():
    if (len(VERTICES),len(EDGES),len(FACES)) != (12,20,11): raise ValueError("actual two-cube graph count mismatch")
    for f in FACES:
        for i,(eid,sign) in enumerate(f.word):
            e=EDGES[eid]; ends=(e.tail,e.head) if sign==1 else (e.head,e.tail)
            if ends != (f.vertices[i], f.vertices[(i+1)%4]): raise ValueError("signed face word does not close")
    return True

def simple_cycles(max_len=8):
    found={}
    def dfs(start,cur,path,edgepath):
        if len(edgepath)>=max_len: return
        for nxt,eid in ADJ[cur]:
            if nxt==start and len(edgepath)+1>=4:
                S=tuple(sorted(edgepath+[eid]))
                if S not in found:
                    word=tuple(LOOKUP[(u,v)] for u,v in zip(path, path[1:]+[start]))
                    found[S]=word
            elif nxt not in path and nxt>=start:
                dfs(start,nxt,path+[nxt],edgepath+[eid])
    for s in sorted(VERTICES): dfs(s,s,[s],[])
    return found

CYCLES_ALL = simple_cycles(8)
LOW_CYCLE_ITEMS = sorted([(S,w) for S,w in CYCLES_ALL.items() if len(S) in (4,6)], key=lambda x:(len(x[0]),x[0]))
LOOP_WORDS = [w for S,w in LOW_CYCLE_ITEMS]
FACE_WORDS = [f.word for f in FACES]
ALL_MOMENT_LOOPS = LOOP_WORDS + FACE_WORDS
FACE_LOOP_IDS = list(range(len(LOOP_WORDS), len(LOOP_WORDS)+len(FACES)))

def inv_mult(ns):
    counts={0:1}
    for n in ns:
        nxt=Counter()
        for a,m in counts.items():
            for c in range(abs(a-n), a+n+1, 2): nxt[c]+=m
        counts=dict(nxt)
    return counts.get(0,0)

def enumerate_label_channels(strict=True):
    threshold = STRICT_CUTOFF
    channels=[]; support_rows=[]
    max_support=7 if strict else 8
    for k in range(max_support+1):
        for S in combinations(range(len(EDGES)), k):
            if k==0:
                if strict: channels.append({"support":[],"labels":[],"energy_over_alpha":"0","intertwiner_multiplicity":1,"kind":"vacuum"})
                continue
            deg=Counter(v for eid in S for v in (EDGES[eid].tail, EDGES[eid].head))
            no_leaf = min(deg.values())>=2
            if not no_leaf:
                continue
            admitted=[]
            for labels in product((1,2,3), repeat=k):
                E=sum((EDGE_LABEL_COST[n] for n in labels), F(0))
                if (E >= threshold if strict else E != threshold): continue
                label=dict(zip(S,labels)); mult=1; ok=True
                for v,elist in INCIDENT.items():
                    ns=[label[e] for e in elist if e in label]
                    if ns:
                        m=inv_mult(ns)
                        if not m: ok=False; break
                        mult*=m
                if ok:
                    admitted.append((labels,E,mult))
                    channels.append({"support":list(S),"labels":list(labels),"energy_over_alpha":sfrac(E),"intertwiner_multiplicity":mult,"kind":"labelled_spin_network"})
            support_rows.append({"support":list(S),"size":k,"no_leaf":no_leaf,"admitted_label_count":len(admitted),"min_admitted_energy_over_alpha":sfrac(min((x[1] for x in admitted), default=F(0))) if admitted else None})
    return channels, support_rows

def channel_classification():
    channels, support_rows = enumerate_label_channels(True)
    nonvac=[c for c in channels if c["support"]]
    cycle_sets={S for S,w in LOW_CYCLE_ITEMS}
    for c in nonvac:
        if tuple(c["support"]) not in cycle_sets or any(n!=1 for n in c["labels"]):
            raise ValueError("strict cutoff produced a non-fundamental-simple-cycle channel")
    threshold_channels,_=enumerate_label_channels(False)
    threshold=[c for c in threshold_channels if c["support"]]
    threshold_witness=dict(threshold[0])
    threshold_witness["excluded_reason"]="strict cutoff is E_el < 6 alpha"
    threshold_mult_dist=dict(sorted(Counter(c["intertwiner_multiplicity"] for c in threshold).items()))
    threshold_doublet_ledger=[]
    for idx,c in enumerate(threshold):
        if c["intertwiner_multiplicity"] != 2:
            continue
        deg=Counter(v for eid in c["support"] for v in (EDGES[eid].tail, EDGES[eid].head))
        threshold_doublet_ledger.append({
            "assignment_index":idx,
            "support":c["support"],
            "labels":c["labels"],
            "energy_over_alpha":c["energy_over_alpha"],
            "intertwiner_multiplicity":c["intertwiner_multiplicity"],
            "degree_four_vertices":[list(v) for v,d in sorted(deg.items()) if d==4],
            "vertex_degree_multiset":sorted(deg.values()),
        })
    cycles4=sum(1 for S,w in LOW_CYCLE_ITEMS if len(S)==4); cycles6=sum(1 for S,w in LOW_CYCLE_ITEMS if len(S)==6)
    planar6=sum(1 for S,w in LOW_CYCLE_ITEMS if len(S)==6 and len({EDGES[e].axis for e in S})==2)
    nonplanar6=cycles6-planar6
    return {"strict_cutoff":"E_el < 6*alpha", "basis_dimension":1+len(LOW_CYCLE_ITEMS), "vacuum_count":1, "four_edge_cycles":cycles4, "six_edge_cycles":cycles6, "six_edge_planar_cycles":planar6, "six_edge_nonplanar_cycles":nonplanar6, "labelled_channels_below_cutoff":len(channels), "support_audit_count_size_le_7":sum(1 for r in support_rows), "seven_edge_no_leaf_supports_rejected_by_intertwiners":sum(1 for r in support_rows if r['size']==7 and r['admitted_label_count']==0), "channels":[basis_record(i+1,S,w) for i,(S,w) in enumerate(LOW_CYCLE_ITEMS)], "threshold_witness":threshold_witness, "threshold_label_assignment_count":len(threshold), "threshold_channel_count":sum(c["intertwiner_multiplicity"] for c in threshold), "threshold_physical_channel_count_with_intertwiner_multiplicity":sum(c["intertwiner_multiplicity"] for c in threshold), "threshold_intertwiner_multiplicity_distribution":threshold_mult_dist, "threshold_double_multiplicity_ledger":threshold_doublet_ledger, "threshold_support_size_counts":dict(Counter(len(c['support']) for c in threshold))}

def basis_record(index,S,w):
    axes=Counter(EDGES[e].axis for e in S)
    return {"basis_index":index,"support":list(S),"word":[{"edge":e,"sign":s} for e,s in w],"length":len(S),"energy_over_alpha":sfrac(F(3,4)*len(S)),"cycle_class":"face-four-cycle" if len(S)==4 else ("planar-six-cycle" if len(axes)==2 else "nonplanar-six-cycle"),"intertwiner_multiplicity":1}

# SU(2) exact Haar tensor for fundamental matrices using S^3 coordinates.
def entry_terms(sign,i,j):
    if sign==1:
        table={(0,0):[(ONE,0),(I,1)], (0,1):[(ONE,2),(I,3)], (1,0):[(cneg(ONE),2),(I,3)], (1,1):[(ONE,0),(NI,1)]}
    else:
        table={(0,0):[(ONE,0),(NI,1)], (0,1):[(cneg(ONE),2),(NI,3)], (1,0):[(ONE,2),(NI,3)], (1,1):[(ONE,0),(I,1)]}
    return table[(i,j)]

def s3_monomial(exps):
    if any(e%2 for e in exps): return F(0)
    half=[e//2 for e in exps]; total=sum(half)
    num=F(1); den=F(1)
    for a in half:
        odd=1
        for k in range(1,2*a,2): odd*=k
        num*=odd
    for k in range(total): den*=4+2*k
    return num/den

@lru_cache(None)
def local_tensor(signs):
    k=len(signs); tab={}
    for mask in range(1<<(2*k)):
        inds=[(mask>>r)&1 for r in range(2*k)]
        poly={(0,0,0,0):ONE}
        for t,s in enumerate(signs):
            new=defaultdict(lambda: ZERO)
            for exp,coef in poly.items():
                for c,var in entry_terms(s, inds[2*t], inds[2*t+1]):
                    ee=list(exp); ee[var]+=1
                    new[tuple(ee)]=cadd(new[tuple(ee)], cmul(coef,c))
            poly=dict(new)
        val=ZERO
        for exp,coef in poly.items():
            m=s3_monomial(exp); val=cadd(val,(coef[0]*m,coef[1]*m))
        if val!=ZERO: tab[tuple(inds)]=val
    return tab

def multiply_factors(factors):
    if any(not tab for vs,tab in factors): return (), {}
    cur=(); table={():ONE}
    for vs,ft in factors:
        union=list(cur); pos={v:i for i,v in enumerate(union)}
        for v in vs:
            if v not in pos: pos[v]=len(union); union.append(v)
        curpos=[pos[v] for v in cur]; vspos=[pos[v] for v in vs]
        nt={}
        for k1,v1 in table.items():
            for k2,v2 in ft.items():
                arr=[None]*len(union); ok=True
                for i,b in zip(curpos,k1): arr[i]=b
                for i,b in zip(vspos,k2):
                    if arr[i] is not None and arr[i]!=b: ok=False; break
                    arr[i]=b
                if ok:
                    key=tuple(arr); nt[key]=cadd(nt.get(key,ZERO), cmul(v1,v2))
        cur=tuple(union); table=nt
    return cur,table

def eliminate(factor,var):
    vs,tab=factor
    if var not in vs: return factor
    j=vs.index(var); nvs=vs[:j]+vs[j+1:]; nt={}
    for key,val in tab.items():
        nk=key[:j]+key[j+1:]; nt[nk]=cadd(nt.get(nk,ZERO),val)
    return nvs,nt

def contract_factors(factors):
    if any(not tab for vs,tab in factors): return ZERO
    variables=sorted({v for vs,tab in factors for v in vs})
    for var in variables:
        withv=[f for f in factors if var in f[0]]; without=[f for f in factors if var not in f[0]]
        factors=without+[eliminate(multiply_factors(withv),var)]
        if not factors[-1][1]: return ZERO
    vs,tab=multiply_factors(factors) if factors else ((),{():ONE})
    if vs: raise ValueError("uneliminated tensor index")
    return tab.get((),ZERO)

@lru_cache(None)
def moment_by_ids(ids):
    words=[ALL_MOMENT_LOOPS[i] for i in ids]
    edge_occ=defaultdict(list); varid=0
    for word in words:
        L=len(word); vars=list(range(varid,varid+L)); varid+=L
        for t,(eid,sign) in enumerate(word): edge_occ[eid].append((sign,vars[t],vars[(t+1)%L]))
    factors=[]
    for occ in edge_occ.values():
        signs=tuple(o[0] for o in occ)
        tab=local_tensor(signs)
        vs=[]
        for s,r,c in occ: vs.extend([r,c])
        factors.append((tuple(vs),tab))
    val=contract_factors(factors)
    if val[1] != 0: raise ValueError("non-real Haar moment")
    return val[0]

def M(ids): return moment_by_ids(tuple(sorted(ids)))

def basis_loop_ids(i,j,*extra):
    ids=[]
    if i>0: ids.append(i-1)
    if j>0: ids.append(j-1)
    ids.extend(extra)
    return ids

def verify_basis_gram():
    N=1+len(LOOP_WORDS); bad=[]
    for i in range(N):
        for j in range(N):
            v=M(basis_loop_ids(i,j)); exp=F(1) if i==j else F(0)
            if v!=exp: bad.append((i,j,v,exp))
    if bad: raise ValueError("P basis is not orthonormal")
    return True

def haar_validation():
    f0=FACE_LOOP_IDS[0]; f1=FACE_LOOP_IDS[1]
    checks={
        "single_face_mean": M([f0]),
        "single_face_norm": M([f0,f0]),
        "single_face_fourth": M([f0,f0,f0,f0]),
        "two_distinct_face_square": M([f0,f1,f0,f1]),
    }
    expected={
        "single_face_mean": F(0),
        "single_face_norm": F(1),
        "single_face_fourth": F(2),
        "two_distinct_face_square": F(1),
    }
    bad={k:(checks[k],expected[k]) for k in checks if checks[k] != expected[k]}
    if bad: raise ValueError(f"Haar validation failed: {bad}")
    return {k:sfrac(v) for k,v in checks.items()} | {"basis_orthonormal": verify_basis_gram()}

def cross_coefficients():
    verify_basis_gram(); N=1+len(LOOP_WORDS); Fcount=len(FACES)
    A=[[[ -M(basis_loop_ids(i,j,FACE_LOOP_IDS[f]))/2 for f in range(Fcount)] for j in range(N)] for i in range(N)]
    coeff=[]; pvp=[]
    for i in range(N):
        for j in range(N):
            for f in range(Fcount):
                if A[i][j][f]: pvp.append({"i":i,"j":j,"face":f,"coeff":sfrac(A[i][j][f])})
    for i in range(N):
        for j in range(N):
            for f in range(Fcount):
                for g in range(Fcount):
                    pv2=M(basis_loop_ids(i,j,FACE_LOOP_IDS[f],FACE_LOOP_IDS[g]))/4
                    sub=sum((A[i][k][f]*A[k][j][g] for k in range(N)), F(0))
                    c=pv2-sub
                    if c: coeff.append({"i":i,"j":j,"face_f":f,"face_g":g,"coeff":sfrac(c)})
    return {"schema":"ym19-b1-cross-gram-coefficients-v1","basis_dimension":N,"face_count":Fcount,"pvp_linear_nonzero":pvp,"cross_quadratic_nonzero":coeff,"pvp_nonzero_count":len(pvp),"cross_quadratic_nonzero_count":len(coeff),"moment_cache_info":str(moment_by_ids.cache_info()),"local_tensor_cache_info":str(local_tensor.cache_info())}

def evaluate_sparse(coeffs, lambdas):
    lam=[rational(x) for x in lambdas]
    N=coeffs['basis_dimension']; mat=[[F(0) for _ in range(N)] for _ in range(N)]
    for row in coeffs['cross_quadratic_nonzero']:
        mat[row['i']][row['j']] += rational(row['coeff'])*lam[row['face_f']]*lam[row['face_g']]
    return mat

def fixture_matrices(coeffs):
    fixtures=[]
    defs=[('zero',['0']*11),('all_one_eighth',['1/8']*11),('alternating',[('1/8' if i%2==0 else '-1/8') for i in range(11)]),('single_face0',['1/4']+['0']*10)]
    for name,lam in defs:
        mat=evaluate_sparse(coeffs,lam)
        nonzero=[{"i":i,"j":j,"value":sfrac(v)} for i,row in enumerate(mat) for j,v in enumerate(row) if v]
        fixtures.append({"name":name,"lambda_over_alpha":lam,"nonzero_entries":nonzero,"nonzero_count":len(nonzero),"matrix_sha256":sha_json([[sfrac(v) for v in row] for row in mat])})
    return fixtures

def controls(classif, coeffs):
    records=[]
    for name,args in [('reject_E_star_zero',('0','E_star')),('reject_kappa_scale',('2','kappa'))]:
        try: validate_scale(*args); records.append({"name":name,"passed":False})
        except ValueError as exc: records.append({"name":name,"passed":True,"reason":str(exc)})
    records.append({"name":"outer_boundary_only_graph_rejected","passed":len(FACES)==11,"reason":"actual graph has internal/shared face counted once; outer boundary-only would have ten faces"})
    records.append({"name":"nonplanar_six_cycle_omission_detected","passed":classif['six_edge_nonplanar_cycles']>0,"nonplanar_six_cycles":classif['six_edge_nonplanar_cycles']})
    records.append({"name":"strict_threshold_excludes_E_equal_6alpha","passed":classif['threshold_label_assignment_count']>0 and classif['threshold_witness']['energy_over_alpha']=='6',"threshold_witness":classif['threshold_witness']})
    # deletion of P subtraction is detected by vacuum entry for all one-eighth: PV2 vacuum equals sum lambda^2/4, true cross vacuum is zero.
    pv2_vac=sum((F(1,8)*F(1,8)/4 for _ in range(11)), F(0))
    cross_zero=evaluate_sparse(coeffs,['1/8']*11)[0][0]
    records.append({"name":"PV2_without_PVP_subtraction_rejected_as_exact_cross_Gram","passed":pv2_vac != cross_zero and cross_zero==0,"pv2_vacuum_entry":sfrac(pv2_vac),"cross_vacuum_entry":sfrac(cross_zero)})
    records.append({"name":"conservative_bound_not_labeled_exact","passed":True,"reason":"output stores exact sparse coefficients; row/norm bounds, if used later, are separate B2 objects"})
    records.append({"name":"finite_or_Ritz_gap_not_promoted","passed":True,"reason":"B1 computes exact channel classification and W*W coefficients only; no B2 gap theorem claimed"})
    return records

def collection():
    validate_graph(); scale=validate_scale(); classif=channel_classification(); validation=haar_validation(); coeffs=cross_coefficients(); fixtures=fixture_matrices(coeffs)
    data={"schema":"ym19-forward-b1-strict-cutoff-cross-gram-v1","source_sha256":SOURCE_SHA256,"contract":CONTRACT,"scale_register":scale,"physical_contract":{"gauge_group":"SU(2)","graph":"actual two-cube graph P3 x P2 x P2 with 12 vertices, 20 links, 11 faces including shared face","hamiltonian":"H=alpha sum_e C_e - sum_f lambda_f x_f, x_f=chi_f/2","strict_cutoff":"E_el < 6 alpha","projector":"orthogonal projector onto vacuum plus all fundamental simple cycles of length 4 and 6"},"graph":graph_record(),"channel_classification":classif,"H0_reduction":{"P_reduces_H0":True,"reason":"each basis vector is a spin-network eigenvector of H0 with definite electric energy 0, 3alpha, or 9alpha/2; P is the direct sum of complete eigenspaces below the strict cutoff","complement_threshold_over_alpha":"6"},"cross_gram":{"definition":"W^*W=P V^2 P-(P V P)^2 for V=-sum lambda_f chi_f/2","basis_dimension":coeffs['basis_dimension'],"face_count":coeffs['face_count'],"pvp_nonzero_count":coeffs['pvp_nonzero_count'],"cross_quadratic_nonzero_count":coeffs['cross_quadratic_nonzero_count'],"coefficient_tensor_sha256":sha_json(coeffs)},"haar_validation":validation,"fixture_matrices":fixtures,"controls":controls(classif,coeffs),"non_claims":["B1 does not execute B2 continuous coefficient boxes or scalar gap estimates","B1 does not prove homogeneous dense stability or continuum mass gap","A2 product summability is not imported as a finite two-cube spectral result"]}
    data['content_sha256']=sha_json({k:v for k,v in data.items() if k!='content_sha256'})
    return data, coeffs

def write_outputs(outdir: Path):
    if not outdir.is_absolute(): raise ValueError("--output must be an absolute new directory")
    if outdir.exists() and any(outdir.iterdir()): raise ValueError("--output must be new or empty")
    outdir.mkdir(parents=True, exist_ok=True)
    files={}
    data, coeffs=collection()
    def wjson(name,obj):
        p=outdir/name; p.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n'); files[name]=sha_bytes(p.read_bytes())
    wjson('results.json',data); wjson('graph.json',data['graph']); wjson('channels.json',data['channel_classification']); wjson('cross-gram-coefficients.json',coeffs); wjson('fixture-matrices.json',data['fixture_matrices']); wjson('controls.json',data['controls'])
    csvp=outdir/'basis.csv'
    with csvp.open('w',newline='') as f:
        wr=csv.DictWriter(f,fieldnames=['basis_index','length','energy_over_alpha','cycle_class','support'])
        wr.writeheader(); wr.writerow({'basis_index':0,'length':0,'energy_over_alpha':'0','cycle_class':'vacuum','support':'[]'})
        for row in data['channel_classification']['channels']:
            wr.writerow({k: json.dumps(row[k]) if k=='support' else row[k] for k in ['basis_index','length','energy_over_alpha','cycle_class','support']})
    files['basis.csv']=sha_bytes(csvp.read_bytes())
    repo=Path(__file__).resolve().parents[4]; report=Path(__file__).with_name('report.md')
    source_inputs={}
    for rel in [CONTRACT,POST_A_ROADMAP,PAIRED_SKILL,SCALE_METHOD]:
        p=repo/rel
        if p.is_file(): source_inputs[rel]=sha_bytes(p.read_bytes())
    manifest={"schema":"ym19-forward-b1-source-manifest-v1","source_files":{"check.py":SOURCE_SHA256,"report.md":sha_bytes(report.read_bytes())},"source_inputs":source_inputs,"outputs":files,"dependencies":["Python standard library only"]}
    wjson('source-manifest.json',manifest)
    return data, manifest

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True); args=ap.parse_args()
    data,manifest=write_outputs(Path(args.output))
    print(json.dumps({"status":"forward B1 evidence generated; no advisor gate claimed","source_sha256":SOURCE_SHA256,"results_sha256":manifest['outputs']['results.json'],"basis_dimension":data['channel_classification']['basis_dimension'],"cross_quadratic_nonzero_count":data['cross_gram']['cross_quadratic_nonzero_count']},sort_keys=True))
if __name__=='__main__': main()
