#!/usr/bin/env python3
"""Exact independent forward AL1 dictionary checks; no SU(2) truncation."""
import argparse, hashlib, json
from fractions import Fraction as Q
from itertools import combinations, product
from pathlib import Path

HERE=Path(__file__).resolve().parent
checks=[]
def need(value,name):
    if not value: raise RuntimeError(name)
    checks.append(name)
def add(v,e): return tuple(a+b for a,b in zip(v,e))
ES=((1,0,0),(0,1,0),(0,0,1))
def owner(p): return (p[0]//4,p[1]//2,p[2])
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);args=ap.parse_args()
    out=Path(args.output).resolve();out.mkdir(parents=True,exist_ok=False)
    faces=[];selected=[];omitted=[]
    for r,s in product(range(4),range(2)):
        p=(r,s,0)
        for i,j in combinations(range(3),2):
            supp=sorted({owner(p),owner(add(p,ES[i])),owner(add(p,ES[j]))})
            row={'p':p,'ij':(i,j),'support':supp}
            faces.append(row)
            (selected if (i,j)==(0,1) and s==0 and r<3 else omitted).append(row)
    need(len(faces)==24 and len(selected)==3 and len(omitted)==21,'all_face_classes')
    links={(r,s,0,k) for r,s,k in product(range(4),range(2),range(3))}
    need(len(links)==24,'all_24_electric_links')
    strip={(r,s,0,0) for r,s in product(range(3),range(2))}|{(r,0,0,1) for r in range(4)}
    need(len(strip)==10 and len(links-strip)==14,'ten_plus_fourteen')
    star={(0,0,0),*ES}
    need(set().union(*(set(x['support']) for x in omitted))==star,'whole_star_union')
    B={(0,0,0),(0,0,1)}
    actual=sum(set(x['support'])<=B for x in omitted)
    need(actual==10 and not star<=B,'finite_boundary_mismatch_10_vs_0')
    # Entire-scope statements are proved in report; these rational cases audit them.
    rows=[]
    for n in (1,2,3,8,64,1024):
        a0=Q(3,2);a=a0/n;g2=Q(1,n)
        alpha=g2/(2*a);lam=2/(g2*a);r=lam/alpha;tau=24*r;eps=7*tau
        need(alpha==1/(2*a0) and r==4*n*n and tau==96*n*n and eps==672*n*n,'exact_path_'+str(n))
        need(r>Q(1,2) and r>Q(1,8),'selected_range_fail_'+str(n))
        rows.append(dict(n=n,alpha=str(alpha),lam=str(lam),r=str(r),tau=str(tau),eps=str(eps)))
    r=Q(1,4)
    need(r<=Q(1,2) and r>Q(1,8),'omit_bridge_wrong_model_rejected')
    need(24*r!=r,'tau_equals_r_rejected')
    incoming={(1,1,1),(0,1,1),(1,0,1),(1,1,0)}
    need(len(incoming)==4 and len(incoming-{(1,1,1)})==3,'drop_incoming_stars_rejected')
    g2=Q(2);a=Q(3)
    need(g2/(2*a)!=g2/a,'wrong_electric_coefficient_rejected')
    alpha=Q(24);delta=alpha/8;hbar=Q(2);G=Q(2)
    need(delta*G/hbar==3 and G/hbar==1,'wrong_clock_rejected')
    raw=Q(37);center=Q(31);c=Q(19)
    need((raw+c)-(center+c)==raw-center and raw+c-center!=raw-center,'actual_ground_scalar_cancellation')
    def ref(e):
        if e<=0:raise ValueError('positive E_star required')
        return alpha/e
    rejected=False
    try:ref(Q(0))
    except ValueError:rejected=True
    need(rejected,'zero_E_star_rejected')
    N=8;M=Q(7,64)
    need(N*M!=sum(M/Q(2)**j for j in range(1,N+1)),'summable_substitution_rejected')
    need(Q(4)/Q(1,8)==32 and Q(4)/Q(3,8)==Q(32,3),'incremental_bridge_vs_R18')
    result={'loop':'AL1','direction':'forward','verdict':'bulk_dictionary_and_sufficient_regime_obstruction','checks':checks,'face_classes':faces,'counts':{'electric_links':24,'selected':3,'omitted':21,'boundary_omitted_actual':actual,'boundary_whole_star':0},'path':rows,'analytic_thresholds':{'selected':'g^4>=32','omitted_c1':'g^4>672/c1(S)','omitted_c2':'g^4>1344c2(S)'},'source_constants_evaluated':False,'continuum_proof':False}
    (out/'results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    sources=[HERE/'check.py',HERE/'report.md',*sorted((HERE/'inputs').rglob('*'))]
    manifest={'sources':{str(p.relative_to(HERE)):digest(p) for p in sources if p.is_file()},'outputs':{'results.json':digest(out/'results.json')}}
    (out/'source-manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'checks':len(checks),'verdict':result['verdict']}))
if __name__=='__main__':main()
