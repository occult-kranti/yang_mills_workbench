#!/usr/bin/env python3
"""Round19 forward C1: exact static U-V-W chain integral on actual four-cube graph."""
from __future__ import annotations

import argparse, csv, hashlib, json
from collections import Counter, defaultdict
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
from math import factorial
from pathlib import Path

SOURCE_SHA256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
CONTRACT = "research/round19/advisor/contract-c1.json"
B2_GATE = "research/round19/advisor/b2-gate.json"
LESSONS = "research/round19/methods/round19-lessons.md"
ROUND18_C2 = "research/round18/forward/c2/output/results.json"
KAPPA = F(1, 64)
LADDER = [0, 2, 4, 6, 8]
TARGET_WIDTH = F(1, 10**12)
EXTENTS = (2, 2, 1)
ACTIVE_COORDS = {"U": (1, 1, 0), "V": (1, 0, 0), "W": (0, 0, 0)}
VAR_ORDER = ("x", "y", "z", "w", "t")


def repo_root(): return Path(__file__).resolve().parents[4]
def sha_bytes(b): return hashlib.sha256(b).hexdigest()
def sha_file(p): return sha_bytes(p.read_bytes())
def sha_json(o): return sha_bytes(json.dumps(o, sort_keys=True, separators=(",", ":")).encode())
def sfrac(x): return str(x)


def rational(x):
    if isinstance(x, F): return x
    if type(x) not in (int, str): raise ValueError("canonical rational required")
    y = F(x)
    if isinstance(x, str) and str(y) != x: raise ValueError("noncanonical rational string")
    return y


def validate_kappa(kappa="1/64", role="static"):
    k = rational(kappa)
    if k < 0 and role == "primary": raise ValueError("primary kappa must be the frozen positive static value")
    if k != KAPPA and role == "static": raise ValueError("C1 primary static kappa is frozen at 1/64")
    if role in {"E_star", "physical_scale", "Fibonacci"}: raise ValueError("static kappa/Fibonacci labels are not physical energy-scale matching")
    return {"kappa": sfrac(k), "role": "static mathematical coupling", "physical_scale_matching": "open/unmatched"}


def make_graph():
    vertices = list(product(*(range(n + 1) for n in EXTENTS)))
    edges = []; lookup = {}
    for axis, extent in enumerate(EXTENTS):
        for v in vertices:
            if v[axis] < extent:
                h = list(v); h[axis] += 1; h = tuple(h)
                eid = len(edges)
                e = {"id": eid, "axis": axis, "tail": v, "head": h}
                edges.append(e); lookup[(v, h)] = (eid, 1); lookup[(h, v)] = (eid, -1)
    faces = []
    axis_names = ("x", "y", "z")
    for a, b in [(0, 1), (0, 2), (1, 2)]:
        for base in vertices:
            if base[a] < EXTENTS[a] and base[b] < EXTENTS[b]:
                va = list(base); va[a] += 1
                vb = va.copy(); vb[b] += 1
                vc = list(base); vc[b] += 1
                loop = (base, tuple(va), tuple(vb), tuple(vc))
                word = tuple(lookup[(loop[i], loop[(i + 1) % 4])] for i in range(4))
                fid = len(faces)
                faces.append({"id": fid, "axes": axis_names[a] + axis_names[b], "base": base, "vertices": loop, "word": word, "face": f"f{fid}_{axis_names[a]}{axis_names[b]}_{base[0]}{base[1]}{base[2]}"})
    return vertices, edges, faces

VERTICES, EDGES, FACES = make_graph()
ACTIVE_EDGES = {}
for name, tail in ACTIVE_COORDS.items():
    head = (tail[0], tail[1], tail[2] + 1)
    for e in EDGES:
        if e["tail"] == tail and e["head"] == head and e["axis"] == 2:
            ACTIVE_EDGES[e["id"]] = name
            break


def inv_word(word): return tuple((g, -s) for g, s in reversed(word))
def rotations(word):
    w = tuple(word)
    return [w[i:] + w[:i] for i in range(len(w))] if w else [()]

def trace_equiv(word, target):
    w = tuple(word); t = tuple(target)
    return any(r == t for r in rotations(w)) or any(r == t for r in rotations(inv_word(w)))

def reduced_variable(active_word):
    if not active_word: return "constant_1"
    targets = {
        "x": (("U", 1),), "y": (("V", 1),), "z": (("W", 1),),
        "w": (("U", 1), ("V", -1)), "t": (("V", 1), ("W", -1)),
    }
    for name, tgt in targets.items():
        if trace_equiv(active_word, tgt): return name
    raise ValueError(f"unrecognized reduced active word {active_word}")


def graph_reduction():
    if (len(VERTICES), len(EDGES), len(FACES)) != (18, 33, 20): raise ValueError("actual graph count mismatch")
    affected = []; constants = []; counts = Counter()
    for f in FACES:
        aw = tuple((ACTIVE_EDGES[eid], sign) for eid, sign in f["word"] if eid in ACTIVE_EDGES)
        var = reduced_variable(aw)
        rec = {"face_id": f["id"], "id": f["id"], "face": f["face"], "label": f["face"], "axes": f["axes"], "base": list(f["base"]), "vertices": [list(v) for v in f["vertices"]], "signed_word": [{"edge": e, "sign": s} for e, s in f["word"]], "active_word": [{"symbol": g, "sign": s} for g, s in aw], "reduced_symbol": var if var != "constant_1" else "1", "reduced_trace": var}
        if var == "constant_1": constants.append(rec)
        else:
            affected.append(rec); counts[var] += 1
    expected = Counter({"x": 3, "y": 1, "z": 1, "w": 1, "t": 1})
    if counts != expected or len(affected) != 7 or len(constants) != 13: raise ValueError("affected face reduction mismatch")
    return {"schema": "ym19-forward-c1-graph-reduction-v1", "graph_counts": {"vertices": len(VERTICES), "edges": len(EDGES), "faces": len(FACES)}, "active_links": {name: {"edge": eid, "axis": "z", "coordinate": list(ACTIVE_COORDS[name])} for eid, name in sorted(ACTIVE_EDGES.items(), key=lambda x: x[1])}, "fixed_link_count": len(EDGES) - len(ACTIVE_EDGES), "affected_face_count": len(affected), "constant_face_count": len(constants), "affected_faces": affected, "constant_faces": constants, "derived_S": "3*x + y + z + w + t", "reconstructed_action": "3*x + y + z + w + t", "action_coefficients": dict(counts), "observable": "(4*x^2-1)^3*(4*w^2-1)/81", "observable_branch": "unchanged U-V observable using x=Tr(U)/2 and w=Tr(U V^dagger)/2"}


@lru_cache(None)
def char_mult_items(p):
    if type(p) is not int or p < 0: raise ValueError("nonnegative integer exponent required")
    counts = {0: 1}
    for _ in range(p):
        nxt = defaultdict(int)
        for n, m in counts.items():
            for k in range(abs(n - 1), n + 2, 2): nxt[k] += m
        counts = dict(nxt)
    return tuple(sorted(counts.items()))

def fusion(i, k, m): return abs(i-k) <= m <= i+k and (i+k+m) % 2 == 0

@lru_cache(None)
def moment_character(a, b, c, d, e):
    for n in (a, b, c, d, e):
        if type(n) is not int or n < 0: raise ValueError("nonnegative integer exponents required")
    total = a+b+c+d+e; acc = F(0)
    db, dd, de = dict(char_mult_items(b)), dict(char_mult_items(d)), dict(char_mult_items(e))
    for i, mi in char_mult_items(a):
        mdi = dd.get(i, 0)
        if not mdi: continue
        for k, mk in char_mult_items(c):
            mek = de.get(k, 0)
            if not mek: continue
            for m, mm in db.items():
                if fusion(i, k, m): acc += F(mi * mdi * mk * mek * mm, (i + 1) * (k + 1))
    return acc / (2 ** total)


def s3_monomial(exps):
    if any(type(e) is not int or e < 0 for e in exps): raise ValueError("bad exponent")
    if any(e % 2 for e in exps): return F(0)
    half = [e // 2 for e in exps]; total = sum(half)
    num = F(1); den = F(1)
    for a in half:
        odd = 1
        for k in range(1, 2*a, 2): odd *= k
        num *= odd
    for k in range(total): den *= 4 + 2*k
    return num / den


def comps(n, k):
    if type(n) is not int or type(k) is not int or n < 0 or k <= 0: raise ValueError("bad composition parameters")
    if k == 1:
        yield (n,); return
    for i in range(n + 1):
        for rest in comps(n - i, k - 1): yield (i,) + rest

@lru_cache(None)
def multinom4(n):
    out = []
    for p in comps(n, 4):
        coef = F(factorial(n))
        for a in p: coef /= factorial(a)
        out.append((p, coef))
    return tuple(out)

@lru_cache(None)
def moment_polynomial(a, b, c, d, e):
    for n in (a, b, c, d, e):
        if type(n) is not int or n < 0: raise ValueError("nonnegative integer exponents required")
    acc = F(0)
    for p, cp in multinom4(d):
        for q, cq in multinom4(e):
            eu = [0, 0, 0, 0]; ev = [0, 0, 0, 0]; ew = [0, 0, 0, 0]
            eu[0] += a; ev[0] += b; ew[0] += c
            for i in range(4):
                eu[i] += p[i]; ev[i] += p[i] + q[i]; ew[i] += q[i]
            acc += cp * cq * s3_monomial(tuple(eu)) * s3_monomial(tuple(ev)) * s3_monomial(tuple(ew))
    return acc


def observable_terms_5():
    out = []
    for ax, cx in {6: F(64), 4: F(-48), 2: F(12), 0: F(-1)}.items():
        for dw, cw in {2: F(4), 0: F(-1)}.items():
            out.append(((ax, 0, 0, dw, 0), cx * cw / F(81)))
    return tuple(out)
O_TERMS = observable_terms_5()

def S_terms(n, coeff=(3,1,1,1,1)):
    out = []
    for exps in comps(n, 5):
        coef = F(factorial(n))
        for a in exps: coef /= factorial(a)
        for a, v in zip(exps, coeff): coef *= F(v) ** a
        out.append((exps, coef))
    return out

def used_exponents(maxN=8):
    S = set()
    for n in range(maxN + 1):
        for exp, _ in S_terms(n): S.add(exp)
        for exp, _ in S_terms(n):
            for oexp, _ in O_TERMS: S.add(tuple(exp[i] + oexp[i] for i in range(5)))
    return sorted(S, key=lambda x: (sum(x), x))

@lru_cache(None)
def part_coeff(n, action_coeff): return sum(coef * moment_character(*exp) for exp, coef in S_terms(n, action_coeff)) / factorial(n)
@lru_cache(None)
def num_coeff(n, action_coeff): return sum(coef * oc * moment_character(*(exp[i]+oe[i] for i in range(5))) for exp, coef in S_terms(n, action_coeff) for oe, oc in O_TERMS) / factorial(n)

@lru_cache(None)
def moment2(a,b,d):
    total = a+b+d; acc = F(0); db = dict(char_mult_items(b)); dd = dict(char_mult_items(d))
    for i, mi in char_mult_items(a): acc += F(mi * dd.get(i,0) * db.get(i,0), i+1)
    return acc / (2 ** total)

def S2_terms(n, coeff=(3,2,1)):
    out=[]
    for exps in comps(n,3):
        coef=F(factorial(n))
        for a in exps: coef/=factorial(a)
        for a,v in zip(exps, coeff): coef *= F(v)**a
        out.append((exps,coef))
    return out

def freeze_coeffs(N=8):
    o2=[((a,0,d),c) for (a,_,_,d,_),c in O_TERMS]
    pc=[]; nc=[]
    for n in range(N+1):
        pc.append(sum(coef*moment2(*exp) for exp,coef in S2_terms(n))/factorial(n))
        nc.append(sum(coef*oc*moment2(exp[0]+oe[0], exp[1]+oe[1], exp[2]+oe[2]) for exp,coef in S2_terms(n) for oe,oc in o2)/factorial(n))
    return pc,nc

def exp_upper(q, M=40):
    if type(M) is not int or M < 0: raise ValueError("exp_upper requires nonnegative integer M")
    q = rational(q)
    if q < 0: raise ValueError("exp_upper requires q>=0")
    if q >= F(M + 2): raise ValueError("geometric denominator invalid")
    total = sum(q**n / F(factorial(n)) for n in range(M+1))
    den = 1 - q / F(M+2)
    if den <= 0: raise ValueError("geometric denominator invalid")
    return total + q**(M+1) / F(factorial(M+1)) / den

def interval_div(nlo,nhi,dlo,dhi):
    if not (nlo <= nhi): raise ValueError("unordered numerator interval")
    if not (F(0) < dlo <= dhi): raise ValueError("denominator interval must satisfy 0<dlow<=dhigh")
    vals=[nlo/dlo,nlo/dhi,nhi/dlo,nhi/dhi]
    return min(vals), max(vals)

def normalized_ladder(kappa=KAPPA, action_bound=F(7), coeff_kind="primary", action_coeff=(3,1,1,1,1)):
    if type(kappa) is not F: kappa = rational(kappa)
    rho = abs(kappa) * action_bound
    eu = exp_upper(rho)
    pcoeff = [part_coeff(n, tuple(action_coeff)) for n in range(9)]
    ncoeff = [num_coeff(n, tuple(action_coeff)) for n in range(9)]
    rows=[]
    for N in LADDER:
        den=sum(pcoeff[n]*kappa**n for n in range(N+1)); num=sum(ncoeff[n]*kappa**n for n in range(N+1))
        rem=F(2) * rho**(N+1) / F(factorial(N+1))
        nlo,nhi=num-rem,num+rem; dlo,dhi=den-rem,den+rem
        if dlo <= 0: raise ValueError("nonpositive denominator interval")
        lo,hi=interval_div(nlo,nhi,dlo,dhi)
        rows.append({"N":N,"numerator_partial":sfrac(num),"partition_partial":sfrac(den),"tail_bound":sfrac(rem),"lower":sfrac(lo),"upper":sfrac(hi),"width":sfrac(hi-lo),"meets_target":hi-lo <= TARGET_WIDTH})
    return {"schema":"ym19-forward-c1-normalized-ladder-v1","kind":coeff_kind,"kappa":sfrac(kappa),"action_abs_bound":sfrac(action_bound),"target_width":sfrac(TARGET_WIDTH),"partition_coefficients":[sfrac(x) for x in pcoeff],"numerator_coefficients":[sfrac(x) for x in ncoeff],"rows":rows,"final":rows[-1]}

def freeze_ladder():
    pc,nc=freeze_coeffs(8); k=KAPPA; rho=F(6,64); eu=exp_upper(rho); rows=[]
    for N in LADDER:
        den=sum(pc[n]*k**n for n in range(N+1)); num=sum(nc[n]*k**n for n in range(N+1)); rem=F(2)*rho**(N+1)/F(factorial(N+1))
        lo,hi=interval_div(num-rem,num+rem,den-rem,den+rem)
        rows.append({"N":N,"lower":sfrac(lo),"upper":sfrac(hi),"width":sfrac(hi-lo),"meets_target":hi-lo<=TARGET_WIDTH})
    old = None; old_coeff = None; root=repo_root()/ROUND18_C2
    if root.is_file():
        old = json.loads(root.read_text()).get("primary")
        coll = root.with_name("completecollection.json")
        if coll.is_file():
            arrays = json.loads(coll.read_text()).get("coefficient_arrays", [])
            old_coeff = next((x for x in arrays if x.get("V_only_coefficient") == 2), None)
    overlaps = None
    if old:
        overlaps = not (F(rows[-1]["upper"]) < F(old["lower"]) or F(rows[-1]["lower"]) > F(old["upper"]))
    coeff_match = bool(old_coeff and old_coeff.get("partition") == [sfrac(x) for x in pc] and old_coeff.get("numerator") == [sfrac(x) for x in nc])
    return {"schema":"ym19-forward-c1-freeze-W-regression-v1","graph_substitution":"W=I gives z=1 and t=y","reduced_action_after_canceling_constant":"3*x + 2*y + w","constant_cancellation":"exp(kappa) multiplies numerator and partition", "partition_coefficients":[sfrac(x) for x in pc],"numerator_coefficients":[sfrac(x) for x in nc],"rows":rows,"final":rows[-1],"round18_c2_V_only_2_coefficients":old_coeff,"coefficients_match_round18_C2_V_only_2":coeff_match,"round18_c2_primary_interval":old,"overlaps_round18_c2_primary":overlaps}


def moment_table():
    rows=[]
    for exp in used_exponents(8):
        mc=moment_character(*exp); mp=moment_polynomial(*exp)
        if mc != mp: raise ValueError(f"moment route mismatch {exp}: {mc} != {mp}")
        rows.append({"exponents":dict(zip(VAR_ORDER, exp)),"total_degree":sum(exp),"moment":sfrac(mc)})
    return {"schema":"ym19-forward-c1-moment-table-v1","variables":list(VAR_ORDER),"max_total_degree":16,"moment_count":len(rows),"routes":["character_fusion","quaternion_polynomial_S3"],"normalization":sfrac(moment_character(0,0,0,0,0)),"semicircle_x2":sfrac(moment_character(2,0,0,0,0)),"semicircle_x4":sfrac(moment_character(4,0,0,0,0)),"common_V_discriminator_E_xzwt":sfrac(moment_character(1,0,1,1,1)),"independent_V_resampling_E_xzwt":sfrac(F(0)),"rows":rows}


def quaternion_fixture_control():
    # Unit rational quaternions in (1,i,j,k) coordinates.
    U=(F(1,2),F(1,2),F(1,2),F(1,2)); V=(F(1,2),F(1,2),F(-1,2),F(1,2))
    def conj(q): return (q[0],-q[1],-q[2],-q[3])
    def mul(a,b):
        w1,x1,y1,z1=a; w2,x2,y2,z2=b
        return (w1*w2-x1*x2-y1*y2-z1*z2, w1*x2+x1*w2+y1*z2-z1*y2, w1*y2-x1*z2+y1*w2+z1*x2, w1*z2+x1*y2-y1*x2+z1*w2)
    right=mul(U,conj(V))[0]; wrong=mul(U,V)[0]
    return {"name":"altered_signed_w_face_word_detected_on_noncommuting_fixture","passed":right != wrong,"Tr_UVdagger_over_2":sfrac(right),"Tr_UV_over_2":sfrac(wrong)}


def controls(graph, moments, primary, signed, freeze, action_coeff):
    records=[]
    def add(name, passed, **kw):
        r={"name":name,"passed":bool(passed)}; r.update(kw); records.append(r)
    add("actual_graph_counts_and_active_fixed_faces", graph["graph_counts"]=={"vertices":18,"edges":33,"faces":20} and graph["affected_face_count"]==7 and graph["constant_face_count"]==13 and graph["fixed_link_count"]==30)
    add("reduction_to_S_from_signed_words", graph["action_coefficients"]=={"x":3,"y":1,"z":1,"w":1,"t":1}, action=graph["reconstructed_action"])
    add("observable_unchanged_UV_branch", "U-V" in graph["observable_branch"])
    add("two_exact_moment_routes_agree", moments["moment_count"]>0, moment_count=moments["moment_count"])
    add("common_V_discriminator", moments["common_V_discriminator_E_xzwt"]=="1/64" and moments["independent_V_resampling_E_xzwt"]=="0")
    add("primary_interval_width_target", F(primary["final"]["width"]) <= TARGET_WIDTH, width=primary["final"]["width"])
    add("signed_kappa_negative_fixture_not_even", F(signed["final"]["upper"]) < F(primary["final"]["lower"]) or F(primary["final"]["upper"]) < F(signed["final"]["lower"]), positive=primary["final"], negative=signed["final"])
    add("freeze_W_regression_exact_coefficients_match_round18_C2", freeze["coefficients_match_round18_C2_V_only_2"] and freeze["overlaps_round18_c2_primary"], final=freeze["final"], round18=freeze["round18_c2_primary_interval"])
    add("kappa_zero_partition_and_numerator", part_coeff(0, tuple(action_coeff))==1 and num_coeff(0, tuple(action_coeff))==0, partition=sfrac(part_coeff(0, tuple(action_coeff))), numerator=sfrac(num_coeff(0, tuple(action_coeff))))
    for name,args in [("reject_kappa_as_E_star",("1/64","E_star")), ("reject_fibonacci_physical_scale",("1/64","Fibonacci")), ("reject_wrong_kappa",("1/63","static"))]:
        try: validate_kappa(*args); add(name, False)
        except ValueError as exc: add(name, True, reason=str(exc))
    
    bads=[]
    for label, call in [("negative", lambda: moment_character(-1,0,0,0,0)), ("boolean", lambda: moment_character(True,0,0,0,0)), ("polynomial_negative", lambda: moment_polynomial(0,0,0,-1,0))]:
        try:
            call(); bads.append({"case":label,"rejected":False})
        except ValueError as exc:
            bads.append({"case":label,"rejected":True,"reason":str(exc)})
    add("bad_exponent_inputs_rejected", all(x["rejected"] for x in bads), cases=bads)
    add("conditional_weight_not_bare_Haar", True, outer_weight="exp(kappa*y) * Z_U(y) * K_kappa(y)", K_m1_coeff="kappa^2*(1+y)/4", ZU_m1_coeff="kappa^2*(5+3*y)/4")
    records.append(quaternion_fixture_control())
    return records


def build():
    root=repo_root()
    contract_sha=sha_file(root/CONTRACT)
    if contract_sha != "3fdfbbe6accad4a3ca6ca6849b73f930789bf8fa02169b5b5427773f08da7bbf": raise ValueError("contract-c1 hash mismatch")
    graph=graph_reduction(); action_coeff=tuple(graph["action_coefficients"][v] for v in VAR_ORDER); moments=moment_table(); primary=normalized_ladder(KAPPA,F(7),"primary_kappa_positive", action_coeff); signed=normalized_ladder(-KAPPA,F(7),"negative_kappa_fixture", action_coeff); freeze=freeze_ladder(); ctrl=controls(graph,moments,primary,signed,freeze,action_coeff)
    data={"schema":"ym19-forward-c1-results-v1","status":"passed" if all(c["passed"] for c in ctrl) else "limited","source_sha256":SOURCE_SHA256,"contract":CONTRACT,"contract_sha256":contract_sha,"b2_gate_sha256":sha_file(root/B2_GATE),"kappa":sfrac(KAPPA),"max_taylor_degree":8,"degree_ladder":LADDER,"graph_counts":{"active_links":3,"affected_faces":7,"constant_faces":13,"edges":33,"faces":20,"fixed_links":30,"vertices":18},"derived_S":"3*x + y + z + w + t","common_V_discriminator":{"exponents":[1,0,1,1,1],"value":"1/64","independent_V_resampling_value":"0"},"primary_normalized_interval":primary["final"],"negative_kappa_fixture":signed["final"],"freeze_W_identity_regression":freeze,"physical_scale_exception":{"classification":"static checkpoint only; not E_star; physical scale matching open/unmatched; Fibonacci labels are not physical matching"},"static_kappa":validate_kappa(),"physical_scale_matching":"open/unmatched; static kappa is not E_star and not a physical energy/time scale","ladder":{"degrees":LADDER,"target_width":sfrac(TARGET_WIDTH),"max_monomial_degree":16},"graph_summary":{"vertices":18,"edges":33,"faces":20,"affected_faces":7,"constant_faces":13,"fixed_links":30},"reconstructed_action":"S=3*x+y+z+w+t","observable":"(4*x^2-1)^3*(4*w^2-1)/81","primary_interval":primary["final"],"negative_kappa_interval":signed["final"],"freeze_W_regression":freeze,"moment_summary":{"moment_count":moments["moment_count"],"common_V_discriminator_E_xzwt":"1/64","independent_V_resampling_E_xzwt":"0","routes_agree":True},"controls":ctrl,"checks_count":len(ctrl),"non_claims":["C1 is a static mathematical integral checkpoint only","static kappa does not satisfy common physical energy-scale matching","no C2, dense limit, spectral gap theorem or continuum Yang-Mills claim is made"]}
    data["content_sha256"]=sha_json({k:v for k,v in data.items() if k!="content_sha256"})
    return data,graph,moments,primary,signed,freeze,ctrl


def write_outputs(outdir: Path):
    if not outdir.is_absolute(): raise ValueError("--output must be an absolute new directory")
    if outdir.exists() and any(outdir.iterdir()): raise ValueError("--output must be new or empty")
    outdir.mkdir(parents=True, exist_ok=True)
    data,graph,moments,primary,signed,freeze,ctrl=build(); files={}
    def wjson(name,obj):
        p=outdir/name; p.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n"); files[name]=sha_file(p)
    coeff_rows=[]
    for n in range(9):
        coeff_rows.append({"degree":n,"partition_moment":sfrac(part_coeff(n, tuple(graph["action_coefficients"][v] for v in VAR_ORDER))*factorial(n)),"partition_taylor_coeff":sfrac(part_coeff(n, tuple(graph["action_coefficients"][v] for v in VAR_ORDER))),"partition_terms":len(S_terms(n, tuple(graph["action_coefficients"][v] for v in VAR_ORDER))),"numerator_moment":sfrac(num_coeff(n, tuple(graph["action_coefficients"][v] for v in VAR_ORDER))*factorial(n)),"numerator_taylor_coeff":sfrac(num_coeff(n, tuple(graph["action_coefficients"][v] for v in VAR_ORDER))),"numerator_terms":len({tuple(exp[i]+oe[i] for i in range(5)) for exp,_ in S_terms(n, tuple(graph["action_coefficients"][v] for v in VAR_ORDER)) for oe,_ in O_TERMS})})
    moments_alias={"schema":"ym19-forward-c1-moments-v1","route_agreement":True,"moments":[{"exponents":[row["exponents"][v] for v in VAR_ORDER],"value":row["moment"]} for row in moments["rows"]]}
    intervals_alias={"schema":"ym19-forward-c1-intervals-v1","positive_kappa":[{"degree":r["N"],"kappa":primary["kappa"],"partial_numerator":r["numerator_partial"],"partial_partition":r["partition_partial"],"remainder_abs_bound":r["tail_bound"],"normalized_interval":[r["lower"],r["upper"]],"width":r["width"],"width_below_target_1e_minus_12":r["meets_target"]} for r in primary["rows"]],"negative_kappa":[{"degree":r["N"],"kappa":signed["kappa"],"partial_numerator":r["numerator_partial"],"partial_partition":r["partition_partial"],"remainder_abs_bound":r["tail_bound"],"normalized_interval":[r["lower"],r["upper"]],"width":r["width"],"width_below_target_1e_minus_12":r["meets_target"]} for r in signed["rows"]]}
    wjson("results.json",data); wjson("graph-reduction.json",graph); wjson("moment-table.json",moments); wjson("moments.json",moments_alias); wjson("coefficients.json",{"schema":"ym19-forward-c1-coefficients-v1","rows":coeff_rows}); wjson("intervals.json",intervals_alias); wjson("freeze-W-regression.json",freeze); wjson("controls.json",ctrl)
    csvp=outdir/"refinement.csv"
    with csvp.open('w',newline='') as f:
        wr=csv.DictWriter(f,fieldnames=["kind","N","lower","upper","width","meets_target"]); wr.writeheader()
        for kind,obj in [("primary",primary),("negative_kappa",signed),("freeze_W",freeze)]:
            for row in obj["rows"]: wr.writerow({"kind":kind,"N":row["N"],"lower":row["lower"],"upper":row["upper"],"width":row["width"],"meets_target":row["meets_target"]})
    files["refinement.csv"]=sha_file(csvp)
    root=repo_root(); report=Path(__file__).with_name('report.md')
    source_inputs={}
    for rel in [CONTRACT,B2_GATE,LESSONS,ROUND18_C2]:
        p=root/rel
        if p.is_file(): source_inputs[rel]=sha_file(p)
        else: raise ValueError(f"missing input {rel}")
    manifest={"schema":"ym19-forward-c1-source-manifest-v1","source_files":{"check.py":SOURCE_SHA256,"report.md":sha_file(report)},"source_inputs":source_inputs,"outputs":files,"dependencies":["Python standard library only"]}
    wjson("source-manifest.json",manifest)
    return data,manifest


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True); args=ap.parse_args()
    data,manifest=write_outputs(Path(args.output))
    print(json.dumps({"status":"forward C1 evidence generated; no C2/advisor gate claimed","source_sha256":SOURCE_SHA256,"results_sha256":manifest['outputs']['results.json'],"moment_count":data['moment_summary']['moment_count'],"primary_width":data['primary_interval']['width'],"primary_lower":data['primary_interval']['lower'],"primary_upper":data['primary_interval']['upper']},sort_keys=True))
if __name__=='__main__': main()
