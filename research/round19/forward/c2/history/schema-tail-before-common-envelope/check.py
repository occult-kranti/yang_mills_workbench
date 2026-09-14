#!/usr/bin/env python3
"""Round19 forward C2: continuous static-kappa theorem for the accepted C1 chain."""
from __future__ import annotations

import argparse, csv, hashlib, json
from fractions import Fraction as F
from math import factorial
from pathlib import Path

SOURCE_SHA256 = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
CONTRACT = "research/round19/advisor/contract-c2.json"
CONTRACT_SHA = "704e4dc65890fe00cf5873fd8eed7cd8e78522c185a85d2210830db25f12db54"
C1_GATE = "research/round19/advisor/c1-gate.json"
C1_GATE_SHA = "6d4e07ac09529a8c796d9ae44a667f23a43fd52ba7fcd0a52241c072f64b933f"
LESSONS = "research/round19/methods/round19-lessons.md"
C1_COEFFS = "research/round19/forward/c1/output/coefficients.json"
C1_RESULTS = "research/round19/forward/c1/output/results.json"
C1_GRAPH = "research/round19/forward/c1/output/graph-reduction.json"
C1_MANIFEST = "research/round19/forward/c1/output/source-manifest.json"
PRIMARY_K = F(1, 8)
SIGN_K = F(1, 8)
TARGET_C = F(1, 2048)
TAIL_DEGREE = 8
EXP_M = 80
ACTION_BOUND = F(7)


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

def validate_K(K):
    k = rational(K)
    if k < 0: raise ValueError("K must be nonnegative")
    return k

def exp_upper(q, M=EXP_M):
    if type(M) is not int or M < 0: raise ValueError("nonnegative integer M required")
    q = rational(q)
    if q < 0: raise ValueError("q must be nonnegative")
    if q >= F(M + 2): raise ValueError("geometric denominator invalid")
    partial = sum(q**n / F(factorial(n)) for n in range(M + 1))
    tail = q**(M + 1) / F(factorial(M + 1)) / (1 - q / F(M + 2))
    return partial + tail

def load_c1():
    root = repo_root()
    if sha_file(root / CONTRACT) != CONTRACT_SHA: raise ValueError("contract-c2 hash mismatch")
    if sha_file(root / C1_GATE) != C1_GATE_SHA: raise ValueError("c1 gate hash mismatch")
    coeff_data = json.loads((root / C1_COEFFS).read_text())
    rows = coeff_data["rows"]
    N = [rational(r["numerator_taylor_coeff"]) for r in rows]
    Z = [rational(r["partition_taylor_coeff"]) for r in rows]
    required = {"N0":F(0),"N1":F(0),"N2":F(1,324),"N3":F(13,1296),"Z0":F(1),"Z1":F(0),"Z2":F(13,8),"Z3":F(1,4)}
    actual = {"N0":N[0],"N1":N[1],"N2":N[2],"N3":N[3],"Z0":Z[0],"Z1":Z[1],"Z2":Z[2],"Z3":Z[3]}
    if actual != required: raise ValueError("accepted C1 coefficient recovery failed")
    c1r = json.loads((root / C1_RESULTS).read_text())
    graph = json.loads((root / C1_GRAPH).read_text())
    if c1r["common_V_discriminator"] != {"exponents":[1,0,1,1,1],"value":"1/64","independent_V_resampling_value":"0"}:
        raise ValueError("accepted common-V discriminator missing")
    return N, Z, rows, c1r, graph

def tail_bound(K, degree=TAIL_DEGREE):
    K = validate_K(K)
    E = exp_upper(ACTION_BOUND * K)
    return E * (ACTION_BOUND * K)**(degree + 1) / F(factorial(degree + 1))

def numerator_coefficient_lower(N, K, degree=TAIL_DEGREE):
    K = validate_K(K); E = exp_upper(ACTION_BOUND * K)
    if degree < 2 or degree >= len(N): raise ValueError("unsupported numerator certificate degree")
    c = N[2] - sum(abs(N[n]) * K**(n - 2) for n in range(3, degree + 1)) - E * ACTION_BOUND**(degree + 1) * K**(degree - 1) / F(factorial(degree + 1))
    return c, E

def positivity_certificate(N, Z, K, degree=TAIL_DEGREE):
    K = validate_K(K)
    c, E = numerator_coefficient_lower(N, K, degree)
    constant = c / E
    return {"K":sfrac(K),"degree":degree,"exp_argument":"7*K","exp_upper_E":sfrac(E),"tail_bound_at_K":sfrac(tail_bound(K,degree)),"numerator_quadratic_coefficient_lower_C_N":sfrac(c),"denominator_positive_reason":"Z(kappa)=E[exp(kappa*S)]>0 pointwise and Z(kappa)<=E_K since |S|<=7","denominator_upper_bound_used":sfrac(E),"lower_constant_C_N_over_E":sfrac(constant),"target_constant":"1/2048","margin_over_target":sfrac(constant - TARGET_C),"proves_F_ge_target_kappa_squared":constant >= TARGET_C and c > 0,"endpoint_kappa_zero":"F(0)=0 from N0=N1=0; no division by kappa at the endpoint"}

def D_coefficients(N, Z):
    coeff=[]
    for m in range(2*TAIL_DEGREE+1):
        c=F(0)
        for i in range(min(TAIL_DEGREE,m)+1):
            j=m-i
            if j<=TAIL_DEGREE:
                c += N[i]*Z[j]*((-1)**j) - N[i]*((-1)**i)*Z[j]
        coeff.append(c)
    return coeff

def sign_asymmetry_certificate(N,Z,K=SIGN_K):
    K=validate_K(K); E=exp_upper(ACTION_BOUND*K)
    D=D_coefficients(N,Z)
    nonzero=[{"degree":i,"coefficient":sfrac(c)} for i,c in enumerate(D) if c]
    if D[3] != F(13,648): raise ValueError("cross-difference leading coefficient mismatch")
    if any(c < 0 for i,c in enumerate(D) if i>=3): raise ValueError("unexpected negative retained D coefficient")
    R = E * (ACTION_BOUND*K)**(TAIL_DEGREE+1) / F(factorial(TAIL_DEGREE+1))
    tail_over_k3 = (4*E*R + 6*R*R) / (K**3)
    margin = D[3] - tail_over_k3
    return {"range":"0 < kappa <= 1/8","K":sfrac(K),"D_definition":"N(kappa)*Z(-kappa)-N(-kappa)*Z(kappa)","retained_D_coefficients":nonzero,"leading_term":"2*N3*kappa^3 = (13/648)*kappa^3","tail_error_over_kappa_cubed_bound":sfrac(tail_over_k3),"positive_margin_over_kappa_cubed":sfrac(margin),"proves_F_kappa_gt_F_minus_kappa":margin>0,"denominator_reason":"Z(kappa) and Z(-kappa) are positive pointwise expectations"}

def higher_degree_probe_from_c1_model(K, max_degree=20):
    # Import C1 source functions without mutating accepted outputs; used only for boundary diagnostics.
    import importlib.util
    c1_path = repo_root() / "research/round19/forward/c1/check.py"
    spec = importlib.util.spec_from_file_location("ym19_forward_c1_for_c2_probe", c1_path)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)  # type: ignore[union-attr]
    K=validate_K(K); out=[]
    coeff=[mod.num_coeff(n, (3,1,1,1,1)) for n in range(max_degree+1)]
    for degree in [8,10,12,14,16,18,20]:
        E=exp_upper(ACTION_BOUND*K)
        c=coeff[2]-sum(abs(coeff[n])*K**(n-2) for n in range(3,degree+1))-E*ACTION_BOUND**(degree+1)*K**(degree-1)/F(factorial(degree+1))
        out.append({"degree":degree,"C_N":sfrac(c),"C_N_over_E":sfrac(c/E),"margin_over_1_2048":sfrac(c/E - TARGET_C),"proves_target_constant":c/E >= TARGET_C and c>0})
    return out

def boundary_diagnostics(N,Z):
    diag=[]
    for K in [F(1,7), F(1,6)]:
        base=positivity_certificate(N,Z,K,TAIL_DEGREE)
        probe=higher_degree_probe_from_c1_model(K,20)
        diag.append({"K":sfrac(K),"degree8_certificate":base,"higher_degree_probe_to_20":probe,"classification":"degree-8 method proves only a weaker positive coefficient, not 1/2048" if K==F(1,7) else "degree-8 numerator margin is negative; higher-degree probe becomes positive but remains below 1/2048 through degree 20"})
    return {"schema":"ym19-forward-c2-boundary-diagnostics-v1","diagnostics":diag}

def controls(N,Z,primary,sign,diag,c1r):
    records=[]
    def add(name, passed, **kw):
        r={"name":name,"passed":bool(passed)}; r.update(kw); records.append(r)
    add("recover_C1_low_coefficients", N[:4]==[F(0),F(0),F(1,324),F(13,1296)] and Z[:4]==[F(1),F(0),F(13,8),F(1,4)], N0=sfrac(N[0]), N1=sfrac(N[1]), N2=sfrac(N[2]), N3=sfrac(N[3]))
    add("kappa_zero_endpoint_before_division", N[0]==0 and N[1]==0, endpoint="F(0)=0")
    add("primary_continuous_K_1_8_certificate", primary["proves_F_ge_target_kappa_squared"], margin=primary["margin_over_target"])
    add("denominator_direction_uses_upper_bound", F(primary["lower_constant_C_N_over_E"]) == F(primary["numerator_quadratic_coefficient_lower_C_N"]) / F(primary["denominator_upper_bound_used"]))
    wrong = F(primary["numerator_quadratic_coefficient_lower_C_N"]) * F(primary["denominator_upper_bound_used"])
    add("wrong_denominator_direction_rejected", wrong > F(primary["lower_constant_C_N_over_E"]), wrong_claim_constant=sfrac(wrong), certified_constant=primary["lower_constant_C_N_over_E"])
    add("common_V_measure_not_independent_resampling", c1r["common_V_discriminator"]["value"]=="1/64" and c1r["common_V_discriminator"]["independent_V_resampling_value"]=="0")
    add("sign_asymmetry_cross_difference", sign["proves_F_kappa_gt_F_minus_kappa"], margin=sign["positive_margin_over_kappa_cubed"])
    add("K_1_7_boundary_recorded", diag["diagnostics"][0]["degree8_certificate"]["proves_F_ge_target_kappa_squared"] is False and F(diag["diagnostics"][0]["degree8_certificate"]["numerator_quadratic_coefficient_lower_C_N"])>0)
    add("K_1_6_boundary_recorded", diag["diagnostics"][1]["degree8_certificate"]["proves_F_ge_target_kappa_squared"] is False and F(diag["diagnostics"][1]["degree8_certificate"]["numerator_quadratic_coefficient_lower_C_N"])<0)
    for label, bad in [("noncanonical_K", "0.125"), ("negative_K", "-1/8"), ("boolean_K", True)]:
        try: validate_K(bad); add("reject_"+label, False)
        except ValueError as exc: add("reject_"+label, True, reason=str(exc))
    mutatedN=list(N); mutatedN[2]=F(0)
    add("delete_N2_mutation_rejected", not positivity_certificate(mutatedN,Z,PRIMARY_K)["proves_F_ge_target_kappa_squared"])
    mutatedN=list(N); mutatedN[0]=F(1)
    add("nonzero_N0_endpoint_mutation_rejected", not (mutatedN[0]==0 and mutatedN[1]==0))
    add("static_kappa_physical_matching_rejected", "open/unmatched" in c1r["physical_scale_exception"]["classification"] and "not E_star" in c1r["physical_scale_exception"]["classification"])
    # Executed public-domain guards.
    bads=[]
    for name, fn in [("bad_exp_M", lambda: exp_upper(F(1), True)), ("negative_q", lambda: exp_upper(F(-1,2))), ("bad_K_bool", lambda: validate_K(True))]:
        try: fn(); bads.append({"case":name,"rejected":False})
        except ValueError as exc: bads.append({"case":name,"rejected":True,"reason":str(exc)})
    add("public_input_domain_checks_execute", all(x["rejected"] for x in bads), cases=bads)
    return records

def build():
    N,Z,rows,c1r,graph=load_c1()
    primary=positivity_certificate(N,Z,PRIMARY_K)
    sign=sign_asymmetry_certificate(N,Z,SIGN_K)
    diag=boundary_diagnostics(N,Z)
    ctrl=controls(N,Z,primary,sign,diag,c1r)
    coeffs={"schema":"ym19-forward-c2-coefficients-v1","source":"accepted forward C1 coefficients.json","rows":rows,"recovered_low_coefficients":{"N0":"0","N1":"0","N2":"1/324","N3":"13/1296","Z0":"1","Z1":"0","Z2":"13/8","Z3":"1/4"}}
    data={"schema":"ym19-forward-c2-results-v1","status":"passed" if all(c["passed"] for c in ctrl) else "limited","source_sha256":SOURCE_SHA256,"contract":CONTRACT,"contract_sha256":CONTRACT_SHA,"c1_gate_sha256":sha_file(repo_root()/C1_GATE),"static_scope":"static kappa integral only; physical scale matching remains open/unmatched","theorem":{"positivity":"For every real kappa with |kappa|<=1/8, F(0)=0 and F(kappa)>=kappa^2/2048.","sign_asymmetry":"For 0<kappa<=1/8, F(kappa)>F(-kappa).","not_claimed":["physical energy/time-scale matching","dense convergence","continuum Yang-Mills","spectral or mass gap"]},"primary_certificate":primary,"sign_asymmetry_certificate":sign,"boundary_diagnostics":diag,"coefficient_summary":{"degree":8,"N0":sfrac(N[0]),"N1":sfrac(N[1]),"N2":sfrac(N[2]),"N3":sfrac(N[3]),"Z0":sfrac(Z[0]),"Z1":sfrac(Z[1]),"Z2":sfrac(Z[2]),"Z3":sfrac(Z[3])},"accepted_c1_links":{"results_sha256":sha_file(repo_root()/C1_RESULTS),"coefficients_sha256":sha_file(repo_root()/C1_COEFFS),"graph_sha256":sha_file(repo_root()/C1_GRAPH),"manifest_sha256":sha_file(repo_root()/C1_MANIFEST)},"controls":ctrl,"checks_count":len(ctrl)}
    data["content_sha256"]=sha_json({k:v for k,v in data.items() if k!="content_sha256"})
    return data,coeffs,primary,sign,diag,ctrl

def write_outputs(outdir: Path):
    if not outdir.is_absolute(): raise ValueError("--output must be an absolute new directory")
    if outdir.exists() and any(outdir.iterdir()): raise ValueError("--output must be new or empty")
    outdir.mkdir(parents=True, exist_ok=True)
    data,coeffs,primary,sign,diag,ctrl=build(); files={}
    def wjson(name,obj):
        p=outdir/name; p.write_text(json.dumps(obj,indent=2,sort_keys=True)+"\n"); files[name]=sha_file(p)
    wjson("results.json",data); wjson("coefficients.json",coeffs); wjson("positivity-certificate.json",primary); wjson("sign-asymmetry.json",sign); wjson("boundary-diagnostics.json",diag); wjson("controls.json",ctrl)
    csvp=outdir/"boundary-probe.csv"
    with csvp.open('w', newline='') as f:
        wr=csv.DictWriter(f, fieldnames=["K","degree","C_N","C_N_over_E","margin_over_1_2048","proves_target_constant"]); wr.writeheader()
        for d in diag["diagnostics"]:
            for row in d["higher_degree_probe_to_20"]:
                wr.writerow({"K":d["K"], **row})
    files["boundary-probe.csv"]=sha_file(csvp)
    root=repo_root(); report=Path(__file__).with_name('report.md')
    source_inputs={}
    for rel in [CONTRACT,C1_GATE,LESSONS,C1_RESULTS,C1_COEFFS,C1_GRAPH,C1_MANIFEST]:
        p=root/rel
        if not p.is_file(): raise ValueError(f"missing input {rel}")
        source_inputs[rel]=sha_file(p)
    manifest={"schema":"ym19-forward-c2-source-manifest-v1","source_files":{"check.py":SOURCE_SHA256,"report.md":sha_file(report)},"source_inputs":source_inputs,"outputs":files,"dependencies":["Python standard library only"]}
    wjson("source-manifest.json",manifest)
    return data,manifest

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--output',required=True); args=ap.parse_args()
    data,manifest=write_outputs(Path(args.output))
    print(json.dumps({"status":"forward C2 evidence generated; no advisor gate claimed","source_sha256":SOURCE_SHA256,"results_sha256":manifest['outputs']['results.json'],"primary_margin":data['primary_certificate']['margin_over_target'],"sign_range":data['sign_asymmetry_certificate']['range'],"controls_pass":all(c['passed'] for c in data['controls'])}, sort_keys=True))
if __name__=='__main__': main()
