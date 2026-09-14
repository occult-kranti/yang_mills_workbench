#!/usr/bin/env python3
"""Exact R2 locality/tail algebra and actual free-character sector controls."""
import sys
sys.dont_write_bytecode=True
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json

ROOT=Path(__file__).absolute().parents[4]
BASE='research/round22/forward/r2/'
CONTRACT='research/round22/contracts/r2.json'
CONTRACT_SHA='e6bd37712b4a561e332e61339da3f2d60b8cf2037c909016c9eeaebb857e4f93'
HELPER='research/round22/forward/r1/check.py'
HELPER_SHA='a5f00d25b42d98a8dd602964c6ecaf495e58e0732eed890a9e34ac823ba10539'
INSTRUCTIONS=['research/round22/methods/team-protocol.md',
 'research/round22/methods/v4/AGENTS-at-selection.md',
 'research/round22/methods/v4/generated-support-and-iteration.md',
 'research/round22/methods/v4/haar-maps-and-induced-dynamics.md',
 'research/round22/methods/v4/paired-physics-research-at-selection.md',
 'research/round22/methods/v4/stationarity-support-and-admission.md']
EXTRA=[HELPER,'research/round22/forward/r1/report.md',
 'research/round22/forward/r1/source-notes.md','research/round22/forward/r1/submission.json',
 'research/round22/forward/r1/output/results.json',BASE+'report.md',BASE+'source-notes.md',BASE+'check.py']
Z=(0,0,0);E=((1,0,0),(0,1,0),(0,0,1));STAR=(Z,*E)


def need(ok,why):
    if type(ok) is not bool or not ok:raise ValueError(why)


def reject(name,wrong,details):
    did=False
    try:need(wrong,name)
    except ValueError:did=True
    need(did,'nondiscriminating control '+name)
    return {'id':name,'passed':True,'rejected':True,'details':details}


def sha(path):
    path=path.absolute()
    for p in [path,*path.parents]:need(not p.is_symlink(),'symlink component')
    need(path.is_file(),'missing input/output')
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path,data):path.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def star(b):return {add(b,e) for e in STAR}
def collar(Y,n):
    return {add(y,d) for y in Y for d in product(range(-n,n+1),repeat=3)
            if min(add(y,d))>=0}
def meeting(Y):
    return {tuple(y[j]-e[j] for j in range(3)) for y in Y for e in STAR
            if all(y[j]>=e[j] for j in range(3))}
def J(a,k):
    g=1-k
    return k**a*(F(a**3)/g+3*a*a*k/g**2+3*a*k*(1+k)/g**3+k*(1+4*k+k*k)/g**4)
def T(N,k):
    g=1-k;m=2*N+1
    return k**(N+1)*(F(m**3)/g+6*m*m*k/g**2+12*m*k*(1+k)/g**3+8*k*(1+4*k+k*k)/g**4)
def geom(N,k):return k**(N+1)/(1-k)
def mv(A,v):return [sum((a*b for a,b in zip(row,v)),F(0)) for row in A]
def mm(A,B):return [[sum((A[i][k]*B[k][j] for k in range(len(B))),F(0))
                     for j in range(len(B[0]))] for i in range(len(A))]
def plus(A,B):return [[a+b for a,b in zip(r,s)] for r,s in zip(A,B)]
def scale(c,A):return [[c*a for a in r] for r in A]
def addv(a,b):return [x+y for x,y in zip(a,b)]
def negv(a):return [-x for x in a]
def norm2(v):return sum((x*x for x in v),F(0))
def diag(values):return [[v if i==j else F(0) for j in range(len(values))] for i,v in enumerate(values)]
def inv(A):
    n=len(A);B=[list(row)+[F(i==j) for j in range(n)] for i,row in enumerate(A)]
    for j in range(n):
        p=next(i for i in range(j,n) if B[i][j]);B[j],B[p]=B[p],B[j]
        v=B[j][j];B[j]=[x/v for x in B[j]]
        for i in range(n):
            if i!=j:
                v=B[i][j];B[i]=[x-v*y for x,y in zip(B[i],B[j])]
    return [r[n:] for r in B]


def geometry():
    rows=[];controls=[]
    for label,Y in [('origin',{Z}),('two_sites',{Z,E[0]}),('bulk',{(2,2,2)})]:
        for n in range(4):
            F0=collar(Y,n);F1=collar(Y,n+1);anchors=meeting(F0)
            need(collar(F0,1)==F1,'successive collars')
            need(len(F0)<=len(Y)*(2*n+1)**3,'general cubic collar bound')
            need(len(anchors)<=4*len(F0),'all incident star budget')
            need(all(star(b)<=F1 and bool(star(b)&F0) for b in anchors),'every acting star inside next collar')
            expected=(n+1)**3 if label=='origin' else (n+2)*(n+1)**2 if label=='two_sites' else (2+n-max(0,2-n)+1)**3
            need(len(F0)==expected,'exact collar geometry')
            Lambda=collar(Y,4)
            need(all(star(b)<=Lambda for b in anchors),'containing collar retains all coefficient stars')
            rows.append({'source':label,'n':n,'collar_sites':len(F0),'meeting_anchors':len(anchors)})
    controls.append(reject('linear_instead_of_volume_collar',len(collar({Z},2))==3,{'actual':27,'wrong':3}))
    controls.append(reject('ignore_positive_octant_clipping',len(collar({(2,2,2)},3))==7**3,{'actual':216,'wrong':343}))
    controls.append(reject('drop_boundary_star_action',len([b for b in meeting({Z}) if star(b)<={Z}])==1,
                           {'actual_acting_stars':1,'interior_only':0}))
    need(meeting(star(Z))==star(Z),'exact four positive anchors meeting origin star')
    return rows,controls


def tails():
    rows=[];controls=[]
    for k in (F(0),F(7,2**20),F(35,416)):
        for N in (0,1,3):
            need(J(N+1,k)-J(N+2,k)==(N+1)**3*k**(N+1),'exact origin polynomial tail identity')
            need(T(N,k)-T(N+1,k)==(2*N+1)**3*k**(N+1),'exact general polynomial tail identity')
            need(geom(N,k)-geom(N+1,k)==k**(N+1),'exact geometric tail identity')
            need(J(N+1,k)==sum((n**3*k**n for n in range(N+1,N+8)),F(0))+J(N+8,k),'origin finite-plus-tail equality')
            need(T(N,k)==sum(((2*n-1)**3*k**n for n in range(N+1,N+8)),F(0))+T(N+7,k),'general finite-plus-tail equality')
            need(J(N+1,k)<=T(N,k),'origin tail improves general singleton bound')
            rows.append({'kappa':str(k),'N':N,'Hilbert_energy_tail_over_r':str(geom(N,k)),
              'origin_H0_tail_over_r':str(J(N+1,k)),'general_H0_tail_over_r_sizeY':str(T(N,k)),
              'origin_G_partial_residual_over_r':str((N+1)**3*k**(N+1)),
              'finite_volume_Hilbert_energy_over_r':str(2*geom(N,k)),
              'finite_volume_origin_H0_over_r':str(2*J(N+1,k)),
              'finite_volume_origin_G_over_r':str(J(N+1,k))})
    k=F(35,416)
    controls.append(reject('discard_polynomial_graph_factor',J(2,k)==geom(1,k),
                          {'correct':str(J(2,k)),'wrong':str(geom(1,k))}))
    need(all(geom(N,F(0))==0 and T(N,F(0))==0 for N in range(4)),'tau-zero exact tails')
    controls.append({'id':'tau_zero_and_zero_source_exceptions','passed':True,'rejected':False,
       'outcome':'kappa=0 gives u0 only; r=0 multiplies every response and tail by zero'})
    return rows,controls


def matrix_neumann():
    tau=F(5,1664);k=28*tau
    H=diag([F(1),F(4),F(9)]);Hi=inv(H);Hs=diag([F(1),F(1,2),F(1,3)])
    D=scale(tau,[[F(1),F(2),F(0)],[F(2),F(-1),F(1)],[F(0),F(1),F(2)]])
    K=mm(mm(Hs,D),Hs);G=plus(H,D);v=[F(1),F(0),F(0)];u=mv(inv(G),v)
    need(mm(H,D)!=mm(D,H),'noncommuting exact algebra fixture')
    need(max(sum(abs(x) for x in row) for row in K)<=k,'certified matrix K norm via symmetric row bound')
    terms=[];w=mv(Hs,v);rec=mv(Hi,v);p=[F(0)]*3;rows=[]
    for n in range(5):
        term=mv(Hs,w);need(term==rec,'both form inverse factors match recurrence')
        terms.append(term);p=addv(p,term)
        residual=addv(mv(G,p),negv(v));need(residual==mv(D,term),'exact telescoping inverse residual')
        need(norm2(addv(u,negv(p)))<=geom(n,k)**2,'noncommuting inverse tail bound')
        rows.append({'N':n,'residual_squared':str(norm2(residual)),'tail_squared':str(norm2(addv(u,negv(p))))})
        w=negv(mv(K,w));rec=negv(mv(Hi,mv(D,rec)))
    wrong=addv(terms[0],negv(terms[1]))
    controls=[reject('wrong_Neumann_sign_in_algebra',addv(mv(G,wrong),negv(v))==mv(D,negv(terms[1])),
                    {'wrong_residual_squared':str(norm2(addv(mv(G,wrong),negv(v))))}),
        reject('missing_right_inverse_factor',mv(mm(Hs,inv(plus(diag([F(1)]*3),K))),[F(0),F(1),F(0)])==mv(inv(G),[F(0),F(1),F(0)]),
               {'scope':'noncommuting algebra fixture, not an SU2 spectral truncation'})]
    return rows,controls


def actual_controls(helper):
    omitted=helper.faces();moments,inherited_controls=helper.haar(omitted)
    coefficient=F(moments['defect_norm_squared_tau2_coefficient'])
    need(coefficient==F(7,432) and moments['cross_sign_witnesses']==210,'actual all-face boundary moment')
    origin=(Z,2);exterior=((4,0,0),2)
    need(helper.free(origin) and helper.free(exterior) and helper.owner(exterior[0])==E[0],
         'actual exterior free-character link at prescribed coarse site')
    axes=helper.AXES
    mean=sum(2*q[0] for q in axes)/8;single=sum((2*q[0])**2 for q in axes)/8
    double=sum((2*q[0]*2*p[0])**2 for q,p in product(axes,repeat=2))/64
    need(mean==0 and single==1 and double==1,'actual two-character Haar orthonormality')
    # Exact restrictions to Omega, exterior character, source character, product character.
    local=[[F(0)]*4 for _ in range(4)];vac=[[F(0)]*4 for _ in range(4)]
    for a,b in ((0,2),(1,3)):local[a][b]=local[b][a]=F(1)
    vac[0][2]=vac[2][0]=F(1);eta=[F(0),F(1),F(0),F(0)]
    need(mv(vac,eta)==[F(0)]*4 and norm2(mv(local,eta))==1,'actual source-sector action')
    controls=list(inherited_controls)
    controls.append(reject('exterior_identity_replaced_by_vacuum_projection',mv(local,eta)==mv(vac,eta),
                          {'actual_difference_norm_squared':'1','valid_even_at_tau_zero':True}))
    rows=[]
    for tau in (F(-5,1664),F(0),F(5,1664)):
        k=28*abs(tau);d2=coefficient*tau*tau;sign_lower=(2-k)**2*d2
        need((d2>0)==(tau!=0),'actual bare response exception')
        need(1-k>=F(381,416),'frozen infinite initial form gap')
        if tau:
            controls.append(reject('bare_truncation_'+str(tau),d2==0,{'actual_residual_norm_squared':str(d2)}))
            controls.append(reject('actual_wrong_first_correction_sign_'+str(tau),sign_lower==0,
                                  {'actual_residual_norm_squared_lower':str(sign_lower)}))
        rows.append({'tau':str(tau),'kappa':str(k),'bare_residual_squared':str(d2),
          'wrong_first_correction_residual_squared_lower':str(sign_lower),'exterior_source_error_squared':'1'})
    return {'faces':len(omitted),'cross_moment_witnesses':moments['cross_sign_witnesses'],
            'free_probe_energy':'6','source_norm_squared':'1','exterior_norm_squared':str(single),
            'product_character_norm_squared':str(double),'coupling_fixtures':rows},controls


def weight():
    rows=[]
    for k in (F(7,2**20),F(35,416)):
        terms=[F(2**((n+1)**3))*k**n for n in range(4)]
        ratios=[terms[n+1]/terms[n] for n in range(3)]
        need(all(ratios[n]==k*2**(3*n*n+9*n+7) for n in range(3)),'exact cubic volume ratio')
        if k==F(7,2**20):need(ratios[0]<1 and ratios[1]>1,'initial shrinking prefix is not a certificate')
        rows.append({'mu':'log(2)','kappa':str(k),'upper_terms_over_r':[str(x) for x in terms],
                     'successive_ratios':[str(x) for x in ratios]})
    k=F(35,416)
    control=reject('replace_collar_volume_by_linear_radius',k*2**7==2*k,
                   {'actual_first_ratio':str(k*2**7),'wrong_ratio':str(2*k),
                    'wrong_linear_weight_sum':str(F(2)/(1-2*k)),
                    'actual_certificate':'diverges by cubic exponent; actual coefficient divergence unproved'})
    return rows,[control]


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True,type=Path);out=parser.parse_args().output.absolute()
    need(not out.exists(),'output must be fresh')
    for p in [out,*out.parents]:need(not p.is_symlink(),'symlink output component')
    need(sha(ROOT/CONTRACT)==CONTRACT_SHA,'immutable R2 contract')
    contract=json.loads((ROOT/CONTRACT).read_text())
    need(contract['loop']=='r2' and contract['instruction_inputs']==INSTRUCTIONS,'complete frozen method closure')
    for path,value in contract['dependencies'].items():need(sha(ROOT/path)==value,'dependency mismatch '+path)
    need(sha(ROOT/HELPER)==HELPER_SHA,'frozen own helper byte mismatch')
    spec=importlib.util.spec_from_file_location('forward_r1_frozen_helper',ROOT/HELPER)
    helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
    inputs=sorted(set([CONTRACT,*INSTRUCTIONS,*contract['dependencies'],*EXTRA]))
    bindings={p:sha(ROOT/p) for p in inputs}
    g,gc=geometry();t,tc=tails();m,mc=matrix_neumann();a,ac=actual_controls(helper);w,wc=weight()
    controls=gc+tc+mc+ac+wc+[reject('disabled_assertion_guard',False,{'mechanism':'explicit runtime ValueError'})]
    need(all(type(c['passed']) is bool and c['passed'] for c in controls),'strict control success')
    results={'schema':'ym22-forward-r2-v1','loop':'r2','direction':'forward','passed':True,
      'status':'proved_initial_response_tails_sector_and_weight_limits','claims':{
       'infinite_initial_form_relative_bound':'kappa=28*abs(tau)<=35/416',
       'infinite_initial_G_gap_lower':'g=1-kappa>=381/416','infinite_form_domain':'D(G^1/2)=D(H0^1/2)',
       'global_operator_domain_equality_asserted':False,'K_norm_upper':'kappa',
       'response_inverse':'G_Q^-1 v=H0^-1/2 (I+K)^-1 H0^-1/2 v',
       'coefficient':'u_n=H0^-1/2 (-K)^n H0^-1/2 v','coefficient_support':'Y^(n)',
       'coefficient_Hilbert_energy_majorant':'r*kappa^n','response_in_H0_and_G_operator_domains':True,
       'Hilbert_energy_tail':'r*kappa^(N+1)/g','H0_tail_general':'r*|Y|*T_N(kappa)',
       'H0_tail_origin':'r*J(N+1,kappa)','G_partial_residual':'G p_N-v=D u_N; norm<=r*|Y^(N)|*kappa^(N+1)',
       'finite_volume_if_collar_contained':'Hilbert/energy<=2*r*kappa^(N+1)/g; H0<=2*r*c_N; G<=r*c_N',
       'vacuum_homological_identity':'[S_vac,G]=-A_vac; A_vac=A_Y tensor P_ext',
       'remaining_local_source':'A_Y tensor (I-P_ext), norm=r for nontrivial exterior',
       'actual_exterior_character_error_norm':'1, both signs and tau=0',
       'actual_bare_response_residual_squared':'7*tau^2/432',
       'actual_wrong_first_sign_residual_lower_squared':'(2-kappa)^2*7*tau^2/432',
       'origin_collar_volume':'(n+1)^3','positive_volume_weight_upper_certificate':'diverges for mu>0,r>0,tau!=0',
       'actual_weighted_coefficient_divergence_proved':False,'local_operator_norm_locality_proved':False,
       'initial_response_source_is_O1_generated':False,'all_stage_closure_proved':False,
       'numerical_gap_H0_D_R_proved':False,'Q2_gap_or_magnetic_positivity_imported':False,
       'representation_or_continuum_transfer':False,'additional_research_loop_executed':False},
      'collar_checks':g,'tail_checks':t,'algebra_fixture':{'scope':'independent noncommuting matrix bookkeeping only','rows':m},
      'actual_SU2_controls':a,'volume_weight_checks':w}
    out.mkdir(parents=True)
    save(out/'results.json',results)
    save(out/'controls.json',{'schema':'ym22-controls-v1','loop':'r2','direction':'forward','passed':True,'controls':controls})
    save(out/'source-manifest.json',{'schema':'ym22-source-manifest-v1','loop':'r2','direction':'forward',
        'inputs':bindings,'outputs':{p:sha(out/p) for p in ['results.json','controls.json']}})
    print(json.dumps({'loop':'r2','direction':'forward','status':results['status'],'passed':True,
         'controls':len(controls),'outputs':{p:sha(out/p) for p in ['results.json','controls.json','source-manifest.json']}},sort_keys=True))


if __name__=='__main__':main()
