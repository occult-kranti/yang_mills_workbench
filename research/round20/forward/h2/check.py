#!/usr/bin/env python3
from fractions import Fraction as F
from pathlib import Path
from itertools import combinations
import argparse,hashlib,json,importlib.util
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
D1=ROOT/'research/round20/forward/d1/check.py';H1=ROOT/'research/round20/forward/h1/check.py'
def module(path,name):
    sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
geo=module(D1,'geo_h2_forward');profile=module(H1,'profile_h2_forward')
def require(ok,m):
    if not ok:raise ValueError(m)
def rejected(fn):
    try:fn()
    except ValueError:return True
    return False
def witnesses(f):
    a,b,x,y,z=f
    if (a,b)==(0,2):return {(2,x,y,z),(2,x+1,y,z)}
    if (a,b)==(1,2):return {(2,x,y,z),(2,x,y+1,z)}
    if y%2:return {(1,x,y,z),(1,x+1,y,z)}
    return {(0,x,y,z),(0,x,y+1,z)}
def incident(link):
    a,*p=link;out=set()
    for b in range(3):
        if b==a:continue
        for shift in (0,1):
            base=list(p);base[b]-=shift
            if min(base)>=0:out.add((*sorted((a,b)),*base))
    return out
def neighbors(f):
    facs={geo.factor(e) for e in geo.face_links(f)}
    return {g for fac in facs for e in geo.factor_links(fac) for g in incident(e) if not geo.selected(g)}
def ray(q,eta=F(1,2),alpha=F(1)):
    require(alpha==1,'alpha/E_star fixed at1 in this evidence; varying alpha is another physical scaling')
    require(0<eta<1,'strict budget fraction required')
    B=profile.B(q);tau=eta/(8*B);floor=(1-eta)/8
    variance=tau*tau*profile.B(q*q)/96
    conservative=F(5,6)*tau*tau/(1-q*q)**3
    require(variance<=conservative,'exact variance exceeds general bound')
    return {'q':q,'eta':eta,'tau':tau,'B':B,'g_bar_over_alpha':floor,'variance_over_alpha_squared':variance,'conservative_variance_over_alpha_squared':conservative,'projector_error_squared':min(F(1),variance/floor**2),'energy_lower_over_alpha':-variance/floor,'operator_norm_over_alpha':tau*B,'variance_scaled_by_1minusq_cubed':variance/(1-q)**3,'tau_scaled_by_1minusq_cubed':tau/(1-q)**3}
def encode(o):
    if isinstance(o,F):return str(o)
    if isinstance(o,dict):return {k:encode(v) for k,v in o.items()}
    if isinstance(o,(list,tuple)):return [encode(v) for v in o]
    return o
def main(out):
    contract=ROOT/'research/round20/contracts/h2.json';con=json.loads(contract.read_text());gate=ROOT/con['depends_on']['gate']
    require(hashlib.sha256(gate.read_bytes()).hexdigest()==con['depends_on']['sha256'],'H1 gate changed')
    faces=geo.retained(3);max_degree=0;degrees=[]
    for f in faces:
        W=witnesses(f);links=geo.face_links(f)
        require(len(W)==2 and W<=links and all(geo.factor(e)[0]=='free' for e in W),'two actual free witnesses failed')
        facs={geo.factor(e) for e in links};require(len(facs)<=4 and all(len(geo.factor_links(i))<=10 for i in facs),'general factor cardinality failed')
        for i in facs:
            for e in geo.factor_links(i):require(len(incident(e))<=4,'elementary link incidence exceeds4')
        deg=len(neighbors(f));require(deg<=160 and f in neighbors(f),'full factor overlap row bound failed');degrees.append(deg);max_degree=max(max_degree,deg)
    pair_count=0;max_shared=0
    for f,g in combinations(faces,2):
        shared=len(geo.face_links(f)&geo.face_links(g));max_shared=max(max_shared,shared)
        require(shared<=1 and witnesses(f)-geo.face_links(g),'off-diagonal Haar cancellation lacks witness');pair_count+=1
    # Conditional Haar E[(u dot a)^2]=|a|^2/4 for arbitrary fixed unit coefficient a.
    haar_fixtures=[]
    for a in [(F(1),F(0),F(0),F(0)),(F(3,5),F(4,5),F(0),F(0)),(F(1,3),F(2,3),F(2,3),F(0))]:
        second=sum(v*v for v in a)/4;require(second==F(1,4),'conditional Haar second moment differs');haar_fixtures.append({'coefficient':a,'first_moment':F(0),'second_moment':second})
    rows=[ray(q,eta) for eta in (F(1,4),F(1,2)) for q in map(F,('1/4','1/2','3/4','7/8','15/16','31/32','63/64'))]
    for row in rows:
        q,tau=row['q'],row['tau'];finite=sum((tau*tau*q**(2*sum(f[2:]))/2304 for f in faces),F())
        require(finite<row['variance_over_alpha_squared'],'infinite exact variance missing positive tail')
        require(row['operator_norm_over_alpha']==row['eta']/8,'canonical norm budget changed')
    # Real graph distinction: disjoint links can touch the same full strip.
    f=(0,2,0,0,0);g=(1,2,2,0,0)
    f_links,g_links=geo.face_links(f),geo.face_links(g)
    f_factors={geo.factor(e) for e in f_links};g_factors={geo.factor(e) for e in g_links}
    require(not(f_links&g_links) and f_factors&g_factors,'shared-factor counterexample invalid')
    # Two disjoint-link observables in a Bell state: zero means, covariance one.
    bell_prob=[F(1,2),F(0),F(0),F(1,2)];Z1=[1,1,-1,-1];Z2=[1,-1,1,-1]
    bell_cov=sum(p*a*b for p,a,b in zip(bell_prob,Z1,Z2))-sum(p*a for p,a in zip(bell_prob,Z1))*sum(p*b for p,b in zip(bell_prob,Z2))
    # Reference-zero-mean V=[0,-60;-60,0], H_ref=diag(0,119); perturbed ground (12,5)/13 has e=-25.
    remote=[F(12,13),F(5,13)];remote_mean=-120*remote[0]*remote[1]
    require(-60*remote[1]==-25*remote[0] and -60*remote[0]+119*remote[1]==-25*remote[1],'remote ground fixture not an eigenvector')
    def universal_degree_claim(degree,proof_kind):
        require(proof_kind=='all_faces_product_incidence' and degree>=4*10*4,'finite observed maximum has no universal proof')
    asymptotic=[]
    for eta in (F(1,4),F(1,2)):
        residue=F(7,64);tau_lead=eta/(8*residue)
        sigma_lead=tau_lead*tau_lead*(residue/8)/96
        projection_lead=sigma_lead/((1-eta)/8)**2
        require(sigma_lead==eta*eta/5376 and projection_lead==eta*eta/(84*(1-eta)**2),'asymptotic constant mismatch')
        asymptotic.append({'eta':eta,'tau_leading_coefficient':tau_lead,'variance_leading_coefficient':sigma_lead,'projector_squared_leading_coefficient':projection_lead})
    controls={
      'disjoint_links_not_factor_independence':bool(f_factors&g_factors) and bell_cov==1,
      'actual_omitted_pair_orthogonality_witness':bool(witnesses(f)-g_links),
      'remote_ground_zero_mean_rejected':rejected(lambda:require(remote_mean==0,'reference mean does not transfer to perturbed ground')),
      'constant_operator_norm_not_state_obstruction':min([0,2])==min([0,3])==0 and max(abs(a-b) for a,b in zip([0,2],[0,3]))==1,
      'fixture_max_not_universal_degree':rejected(lambda:universal_degree_claim(max_degree,'finite_observation')),
      'varying_alpha_rejected':rejected(lambda:ray(F(3,4),alpha=F(64))),
      'eta_one_rejected':rejected(lambda:ray(F(1,2),eta=F(1))),
      'q_one_rejected':rejected(lambda:ray(F(1))),
    }
    require(all(controls.values()),'H2 wrong-model control failed')
    result={'schema':'ym20-forward-h2-v1','loop':'h2','status':'passed','ray_fixtures':rows,'asymptotic_fixtures':asymptotic,'controls':controls,'faces_checked':len(faces),'distinct_face_pairs_checked':pair_count,'max_shared_links':max_shared,'observed_max_factor_overlap_degree':max_degree,'proved_universal_factor_overlap_degree':160,'conditional_Haar_fixtures':haar_fixtures,'exact_variance_formula':'alpha^2*tau(q)^2*B(q^2)/96','canonical_tau_asymptotic':'(8eta/7)(1-q)^3','canonical_variance_scaled_limit':'eta^2/5376','canonical_projector_squared_scaled_limit':'eta^2/[84(1-eta)^2]','projector_error_order':'(1-q)^(3/2)','energy_error_order':'(1-q)^3','operator_norm_on_ray':'alpha eta/8','scope':'global ground projector returns to the selected-strip reference at fixed energy and spacing; no nonzero homogeneous omitted-coupling limit inside this certificate'}
    out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_text(json.dumps(encode(result),indent=2,sort_keys=True)+'\n')
    sources=[HERE/'check.py',HERE/'report.md',D1,H1,contract,gate,ROOT/'research/round19/advisor/a2-gate.json',ROOT/'research/round20/advisor/g2-gate.json']
    manifest={'sources':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'outputs':{'results.json':hashlib.sha256((out/'results.json').read_bytes()).hexdigest()}}
    (out/'source-manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n');print(json.dumps({'status':'passed','loop':'h2','faces':len(faces),'pairs':pair_count,'max_factor_degree':max_degree,'controls':len(controls)}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE/'output');main(p.parse_args().output)
