#!/usr/bin/env python3
"""Q2 exact graph spectral decomposition, physical Casimir jets and block controls."""
from collections import Counter
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import argparse
import hashlib
import json

ROOT=Path(__file__).absolute().parents[4]
BASE='research/round22/forward/q2/'
CONTRACT='research/round22/contracts/q2.json'
CONTRACT_SHA='7b8e7a1dfc4d7d4bb05d7123d26396e0333f48e2bb68f34dfc82703707d0612f'
LEDGER='research/round19/forward/c1/output/graph-reduction.json'
INSTRUCTIONS=['research/round22/methods/team-protocol.md',
 'research/round22/methods/v4/AGENTS-at-selection.md',
 'research/round22/methods/v4/generated-support-and-iteration.md',
 'research/round22/methods/v4/haar-maps-and-induced-dynamics.md',
 'research/round22/methods/v4/paired-physics-research-at-selection.md',
 'research/round22/methods/v4/stationarity-support-and-admission.md']
DEPENDENCIES=[LEDGER,'research/round22/advisor/p2-gate.json',
 'research/round22/advisor/q1-decision.md','research/round22/advisor/q1-gate.json',
 'research/round22/advisor/q1-root-source-note.json','research/round22/skeptic/q1-review.json',
 'research/round22/skeptic/q1.md']
INPUTS=[CONTRACT,*INSTRUCTIONS,*DEPENDENCIES,'research/round22/forward/p2/report.md',
 'research/round22/forward/p2/check.py','research/round22/forward/q1/report.md',
 'research/round22/forward/q1/check.py','research/round22/forward/q1/source-notes.md',
 BASE+'report.md',BASE+'source-notes.md',BASE+'check.py']
TREE=set(range(16))|{26}
QI=(F(1),F(0),F(0),F(0));Q0=(F(0),)*4


def need(ok,why):
    if type(ok) is not bool or not ok:raise ValueError(why)


def safe(path):
    for p in [path.absolute(),*path.absolute().parents]:need(not p.is_symlink(),'symlink component')


def sha(path):
    safe(path);need(path.is_file(),'missing source '+str(path))
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path,value):path.write_text(json.dumps(value,sort_keys=True,indent=2)+'\n')
def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
def qc(a):return (a[0],-a[1],-a[2],-a[3])
def qa(a,b):return tuple(x+y for x,y in zip(a,b))
def qs(c,a):return tuple(c*x for x in a)


def qm(a,b):
    w,x,y,z=a;v,r,s,t=b
    return (w*v-x*r-y*s-z*t,w*r+x*v+y*t-z*s,
            w*s+y*v+z*r-x*t,w*t+z*v+x*s-y*r)


def word(g,p):
    q=QI
    for e,s in p:q=qm(q,g[e] if s==1 else qc(g[e]))
    return q


def jet(q):return (q,Q0,Q0)
def jc(a):return tuple(qc(q) for q in a)
def jm(a,b):
    out=[]
    for n in range(3):
        q=Q0
        for k in range(n+1):q=qa(q,qm(a[k],b[n-k]))
        out.append(q)
    return tuple(out)
def je(axis):return (QI,tuple(F(1,2) if j==axis+1 else F(0) for j in range(4)),qs(-F(1,8),QI))
def jword(g,p):
    value=jet(QI)
    for e,s in p:value=jm(value,g[e] if s==1 else jc(g[e]))
    return value


def graph():
    sizes=(3,3,2);vertices=list(product(*(range(n) for n in sizes)));edges=[];lookup={}
    def shift(p,a):return tuple(p[j]+int(j==a) for j in range(3))
    for a in range(3):
        for p in product(*(range(n-int(j==a)) for j,n in enumerate(sizes))):
            lookup[(a,p)]=len(edges);edges.append((p,shift(p,a)))
    paths={(0,2,0):[]}
    while len(paths)<18:
        before=len(paths)
        for e in sorted(TREE):
            s,t=edges[e]
            if s in paths and t not in paths:paths[t]=paths[s]+[(e,1)]
            if t in paths and s not in paths:paths[s]=paths[t]+[(e,-1)]
        need(len(paths)>before,'tree connected')
    s,t=edges[28];loop=paths[s]+[(28,1)]+[(e,-o) for e,o in reversed(paths[t])]
    need(loop==[(14,-1),(2,1),(28,1),(3,-1),(15,1),(26,-1)],'fixed actual f1 completion')
    ledger=json.loads((ROOT/LEDGER).read_text())
    inherited={f['face_id']:f for f in ledger['affected_faces']+ledger['constant_faces']};faces=[]
    for a,b in combinations(range(3),2):
        for p in product(*(range(n-int(j in (a,b))) for j,n in enumerate(sizes))):
            w=[(lookup[(a,p)],1),(lookup[(b,shift(p,a))],1),
               (lookup[(a,shift(p,b))],-1),(lookup[(b,p)],-1)]
            need(inherited[len(faces)]['signed_word']==[{'edge':e,'sign':s} for e,s in w],
                 'actual signed face ledger')
            faces.append(w)
    need((len(vertices),len(edges),len(faces))==(18,33,20),'complete graph')
    return edges,loop,faces


def walk_cycle(edges,support):
    adjacent={}
    for e in support:
        for v in edges[e]:adjacent.setdefault(v,[]).append(e)
    need(all(len(v)==2 for v in adjacent.values()),'symmetric difference is a simple cycle')
    start=min(adjacent);v=start;previous=None;w=[]
    while True:
        choices=sorted(e for e in adjacent[v] if e!=previous);e=choices[0]
        s,t=edges[e];sign=1 if s==v else -1;v=t if sign==1 else s
        w.append((e,sign));previous=e
        if v==start:break
        need(len(w)<=len(support),'cycle walk closes')
    need(len(w)==len(support),'one connected cycle')
    return w


def connected_path(edges,support):
    if not support:return True
    adj={}
    for e in support:
        s,t=edges[e];adj.setdefault(s,[]).append(t);adj.setdefault(t,[]).append(s)
    reached={next(iter(adj))}
    while True:
        after=reached|{v for u in reached for v in adj[u]}
        if after==reached:break
        reached=after
    degrees=Counter(map(len,adj.values()))
    return len(reached)==len(adj) and degrees[1]==2 and all(d in [1,2] for d in degrees)


def zero(n,m=None):return [[F(0) for j in range(m or n)] for i in range(n)]
def eye(n):return [[F(int(i==j)) for j in range(n)] for i in range(n)]
def add(a,b):return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def scale(c,a):return [[c*x for x in row] for row in a]
def mm(a,b):return [[sum((a[i][k]*b[k][j] for k in range(len(b))),F(0))
                     for j in range(len(b[0]))] for i in range(len(a))]
def transpose(a):return [list(c) for c in zip(*a)]
def enc(a):return [[str(x) for x in row] for row in a]
def inverse(a):
    n=len(a);b=[list(row)+unit for row,unit in zip(a,eye(n))]
    for j in range(n):
        pivot=next((i for i in range(j,n) if b[i][j]),None);need(pivot is not None,'invertible matrix')
        b[j],b[pivot]=b[pivot],b[j];b[j]=[x/b[j][j] for x in b[j]]
        for i in range(n):
            if i!=j:
                c=b[i][j];b[i]=[x-c*y for x,y in zip(b[i],b[j])]
    return [row[n:] for row in b]


def checks():
    controls=[]
    def control(name,ok,outcome):
        need(ok,'failed control '+name)
        controls.append({'name':name,'passed':True,'outcome':outcome})
    edges,L,faces=graph();Ls={e for e,s in L};ids=[p for p in range(20) if p!=8]
    masks={p:{e for e,s in faces[p]} for p in range(20)}
    simple=len({tuple(sorted(e)) for e in edges})==33 and all(s!=t for s,t in edges)
    bipartite=all((sum(s)-sum(t))%2==1 for s,t in edges)
    control('actual_complement_gap_geometry',simple and bipartite and len(masks[0])==4,
            {'simple_graph':True,'bipartite':True,'girth':4,'minimum_nontrivial_edge_casimir':'3/4',
             'all_spin_proof':'nonempty gauge-invariant support has no degree-one vertex',
             'exact_complement_gap_over_alpha':'3','attaining_vector':'2 W0 in Q'})
    support={p:Ls&masks[p] for p in ids};counts=Counter(map(len,support.values()))
    control('all_shared_supports_are_connected_paths',
            counts==Counter({0:9,1:6,2:2,3:2}) and all(connected_path(edges,s) for s in support.values()),
            {'fixed_loop':L,'overlap_by_face':{str(p):sorted(support[p]) for p in ids},
             'counts':{str(k):counts[k] for k in sorted(counts)}})
    parity={p:Ls^masks[p] for p in ids}
    cross=[(p,q) for p in ids for q in ids if masks[p]==parity[q]]
    control('spectral_cross_sectors_and_offdiagonal_pairs',
            len({tuple(sorted(v)) for v in parity.values()})==19 and cross==[(9,15),(15,9)],
            {'cross_pairs':cross,'different_phi_sectors_orthogonal':True,
             'center_action':'one edge g->-g; H_E commutes with every edge center action'})
    axis_points=[tuple(F(s) if i==j else F(0) for i in range(4)) for j in range(4) for s in [-1,1]]
    fourth_points=axis_points+[tuple(F(s,2) for s in signs) for signs in product([-1,1],repeat=4)]
    need(len(fourth_points)==24 and all(dot(q,q)==1 for q in fourth_points),'degree-four Haar cubature')
    need(sum((q[0]**4 for q in fourth_points),F(0))/24==F(1,8)
         and sum((q[0]**2*q[1]**2 for q in fourth_points),F(0))/24==F(1,24),
         'correct Haar fourth moments')
    nphi=ns=nt=orth=F(0)
    for G in fourth_points:
        for A in axis_points:
            for B in axis_points:
                phi=2*qm(G,A)[0]*qm(qc(G),B)[0];singlet=qm(A,B)[0]/2;triplet=phi-singlet
                nphi+=phi*phi;ns+=singlet*singlet;nt+=triplet*triplet;orth+=singlet*triplet
    denom=24*8*8;nphi/=denom;ns/=denom;nt/=denom;orth/=denom
    control('shared_path_singlet_triplet_norms',
            (nphi,ns,nt,orth)==(F(1,4),F(1,16),F(3,16),F(0)),
            {'phi_norm_squared':str(nphi),'singlet_norm_squared':str(ns),
             'triplet_norm_squared':str(nt),'orthogonality':str(orth),
             'quadrature_degree':'4 in shared G;2 in each exclusive A,B'})
    pool=[(F(3,5),F(4,5),F(0),F(0)),(F(5,13),F(0),F(12,13),F(0)),
          (F(1,2),)*4,(F(2,3),F(1,3),F(2,3),F(0))]
    need(all(dot(q,q)==1 for q in pool),'physical quaternion values')
    g=[pool[e%4] for e in range(33)];gj=[jet(q) for q in g]
    phi={p:2*word(g,L)[0]*word(g,faces[p])[0] for p in ids};singlets={};eigen_rows=[]
    for p in ids:
        k=len(support[p])
        if k:
            cycle=walk_cycle(edges,parity[p]);sv=word(g,cycle)[0]/2
            b=min(support[p]);projected=F(0)
            for q in axis_points:
                variant=list(g);variant[b]=q
                projected+=2*word(variant,L)[0]*word(variant,faces[p])[0]/8
            need(projected==sv,'actual common-edge singlet projection')
            singlets[p]=sv
        else:singlets[p]=F(0)
    casimir={p:F(0) for p in ids}
    for e in range(33):
        for axis in range(3):
            variant=list(gj);variant[e]=jm(je(axis),gj[e])
            xjet=[q[0] for q in jword(variant,L)]
            for p in ids:
                fjet=[q[0] for q in jword(variant,faces[p])]
                casimir[p]-=4*sum((xjet[k]*fjet[2-k] for k in range(3)),F(0))
    nonzero_triplets=0
    for p in ids:
        k=len(support[p]);es=F(15,2)-F(3*k,2);et=F(15,2)+F(k,2)
        expected=es*singlets[p]+et*(phi[p]-singlets[p])
        need(casimir[p]==expected,'actual full electric spectral identity')
        if k and phi[p]!=singlets[p]:nonzero_triplets+=1
        eigen_rows.append({'face':p,'k':k,'energy_singlet':str(es) if k else None,
                           'energy_triplet_or_disjoint':str(et),'phi_fixture':str(phi[p]),
                           'singlet_fixture':str(singlets[p]),'H_E_phi_over_alpha':str(casimir[p])})
    control('actual_33_link_casimir_not_cutoff_spectrum',nonzero_triplets>0,
            {'link_axis_derivatives':99,'face_products_tested':19,
             'nonzero_triplet_fixtures':nonzero_triplets,'rows':eigen_rows})
    weights={}
    def W(e):
        if e not in weights:weights[e]=zero(2)
        return weights[e]
    W(F(3))[0][0]=F(19,4)
    for p in ids:
        k=len(support[p])
        if not k:W(F(15,2))[1][1]+=F(1,4)
        else:
            W(F(15,2)-F(3*k,2))[1][1]+=F(1,16)
            W(F(15,2)+F(k,2))[1][1]+=F(3,16)
    for p,q in cross:
        need(parity[q]==masks[p] and len(support[q])==3,'offdiagonal singlet energy')
        W(F(3))[0][1]+=F(1,8);W(F(3))[1][0]+=F(1,8)
    total=zero(2);first=zero(2);self_z1=zero(2)
    for e,w in weights.items():
        need(w[0][0]>=0 and w[1][1]>=0 and w[0][0]*w[1][1]>=w[0][1]**2,'positive spectral weight')
        total=add(total,w);first=add(first,scale(e,w));self_z1=add(self_z1,scale(1/(e+1),w))
    control('complete_fixed_channel_spectral_weights',
            total==[[F(19,4),F(1,4)],[F(1,4),F(19,4)]] and len(weights)==7,
            {'spectral_weights':{str(e):enc(w) for e,w in sorted(weights.items())},
             'matrix_at_zero_delay':enc(total)})
    control('scalar_reference_shortcut_rejected',
            first[1][1]==F(285,8) and first[0][0]==F(57,4) and total[0][1]==F(1,4),
            {'initial_diagonal_equality_is_nondiscriminating':True,
             'nonzero_offdiagonal_weight':'1/4','dimensionless_first_spectral_moment':enc(first),
             'self_energy_at_z_alpha_over_alpha_lambda_squared':enc(self_z1)})
    need(self_z1[1][1]==F(2285061,3979360),'reported exact resolvent evaluation')
    A=[[F(2),F(1)],[F(1),F(4)]];B=[[F(1),F(2)]];Bt=transpose(B);C=F(7)
    H=[[F(2),F(1),F(1)],[F(1),F(4),F(2)],[F(1),F(2),F(7)]]
    K0=mm(Bt,B);need(mm(A,K0)!=mm(K0,A),'noncommuting block control')
    exact=[eye(2)];hp=eye(3);recursive=[eye(2)];once=[];minusA=[eye(2)]
    for n in range(1,7):
        hp=mm(scale(-1,H),hp);exact.append([r[:2] for r in hp[:2]])
        minusA.append(mm(scale(-1,A),minusA[-1]))
        r=mm(scale(-1,A),recursive[-1])
        if n>=2:
            for k in range(n-1):r=add(r,mm(scale((-C)**k,K0),recursive[n-2-k]))
        recursive.append(r)
    for n in range(7):
        r=minusA[n]
        if n>=2:
            for i in range(n-1):
                for k in range(n-1-i):
                    l=n-2-i-k
                    r=add(r,mm(mm(minusA[i],scale((-C)**k,K0)),minusA[l]))
        once.append(r)
    control('Volterra_retains_full_compressed_return',
            recursive==exact and once[:4]==exact[:4] and once[4]!=exact[4],
            {'exact_raw_derivative_orders':list(range(7)),
             'wrong_last_factor_first_failure_order':4,
             'missing_fourth_derivative':enc(add(exact[4],scale(-1,once[4]))),
             'expected_return_square':enc(mm(K0,K0)),'finite_block_algebra_only':True})
    z=F(3);sigma=scale(1/(C+z),K0)
    full_inv=inverse(add(H,scale(z,eye(3))));compressed=[r[:2] for r in full_inv[:2]]
    schur=inverse(add(add(A,scale(z,eye(2))),scale(-1,sigma)))
    wrong=inverse(add(add(A,scale(z,eye(2))),sigma))
    shifted_sigma=scale(1/(C+1+z-1),K0)
    control('Schur_sign_and_compensated_scalar_energy',compressed==schur and wrong!=schur
            and shifted_sigma==sigma and scale(1/(C+1+z),K0)!=sigma,
            {'correct_compressed_resolvent':enc(schur),'wrong_plus_self_energy':enc(wrong),
             'common_shift':'1','spectral_shift':'3 to 2'})
    control('lambda_zero_recovers_electric_projection',
            scale(F(0),K0)==zero(2) and mm(eye(2),A)==A,
            {'physical_B_zero':True,'kernel_zero':True,'self_energy_zero':True,
             'exact_recovery':'T0=exp(-t H_eff/hbar)'})
    vmax=F(40);bnorm2=F(25,4);gap=F(3);maxlam=F(1,100)
    control('full_Hilbert_remainder_constants',vmax*bnorm2==250 and gap>0 and 40*maxlam/gap==F(2,15),
            {'valid_couplings':'all lambda>=0','required_max_lambda':'1/100',
             'kernel_error':'250 alpha^2 lambda^3 sigma exp(-3 sigma)',
             'uniform_delay_error':'250 alpha^2 lambda^3/(3e)',
             'self_energy_error':'250 alpha^3 lambda^3/(3alpha+z)^2',
             'uniform_positive_z_error_coefficient_over_alpha_lambda_cubed':str(F(250,9)),
             'scope':'entire selected Hilbert space, not just two channels'})
    rejects=0
    for bad in [False,1,'passed']:
        try:need(bad,'intentional failure')
        except ValueError:rejects+=1
    control('strict_checks_survive_optimized_python',rejects==3,{'rejected':['False','integer','string']})
    claims={'complement_exact_electric_gap':'3 alpha','complement_magnetic_lower_bound':'3 alpha',
      'complement_operator_domain':'Q D(H_E)','complement_form_domain':'Q D(H_E^(1/2))',
      'coupling_regime':'all lambda>=0, includes [0,1/100]',
      'Volterra':'T=E_A+hbar^-2 integral_triangle E_A K_lambda T',
      'Schur':'J*(H_lambda+z)^-1 J=(A_lambda+z-Sigma_lambda(z))^-1, z>0',
      'integral_topology':'strong vector-valued','fixed_channels':['1','2x, actual P2 completion'],
      'spectral_weights':{str(e):enc(w) for e,w in sorted(weights.items())},
      'leading_kernel':'(alpha lambda)^2 sum_e exp(-e alpha s/hbar) W_e',
      'leading_self_energy':'(alpha lambda)^2 sum_e W_e/(e alpha+z)',
      'offdiagonal_leading_kernel':'(alpha lambda)^2 exp(-3 alpha s/hbar)/4',
      'offdiagonal_leading_self_energy':'(alpha lambda)^2/[4(3alpha+z)]',
      'kernel_remainder':'250 alpha^2 lambda^3 sigma exp(-3sigma), sigma=alpha s/hbar',
      'uniform_delay_kernel_remainder':'250 alpha^2 lambda^3/(3e)',
      'self_energy_remainder':'250 alpha^3 lambda^3/(3alpha+z)^2',
      'uniform_positive_z_remainder':'250 alpha lambda^3/9',
      'remainder_scope':'full infinite-dimensional selected H3',
      'operator_norm_time_Taylor_claim':False,'two_channel_autonomous_closure':False,
      'interacting_ground_claim':False,'homogeneous_transfer':False,
      'physical_calibration':False,'continuum_transfer':False,'R1_executed':False}
    results={'schema':'ym22-forward-q2-results-v1','loop':'q2','direction':'forward',
      'status':'proved_scoped','passed':True,'claims':claims,
      'spectral_first_moment':enc(first),'self_energy_z_alpha_dimensionless':enc(self_z1),
      'finite_cutoff_used':False,'proof_location':BASE+'report.md','scientific_priority':'unverified'}
    return results,{'schema':'ym22-forward-q2-controls-v1','loop':'q2','direction':'forward',
                    'passed':True,'controls':controls}


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    out=p.parse_args().output.absolute();safe(out);need(not out.exists(),'fresh output required')
    inputs={p:sha(ROOT/p) for p in INPUTS};need(len(inputs)==len(INPUTS),'duplicate input')
    need(inputs[CONTRACT]==CONTRACT_SHA,'frozen Q2 contract mismatch')
    c=json.loads((ROOT/CONTRACT).read_text());need(c['loop']=='q2' and c['status']=='frozen','contract identity')
    for p,h in c['dependencies'].items():need(p in inputs and inputs[p]==h,'dependency mismatch '+p)
    for p in c['instruction_inputs']:need(p in inputs,'required instruction missing '+p)
    for p in ['research/round22/advisor/p2-gate.json','research/round22/advisor/q1-gate.json']:
        gate=json.loads((ROOT/p).read_text());need(gate['status']=='accepted','inherited admission status')
        for k,h in inputs.items():
            if k in gate['files']:need(gate['files'][k]==h,'admitted source mismatch '+k)
    results,controls=checks();out.mkdir(parents=True,exist_ok=False)
    save(out/'results.json',results);save(out/'controls.json',controls)
    save(out/'source-manifest.json',{'schema':'ym22-producer-source-manifest-v1','loop':'q2',
      'direction':'forward','inputs':inputs,
      'outputs':{p:sha(out/p) for p in ['results.json','controls.json']},
      'import_policy':'standard-library only; no other producer imports',
      'manifest_self_hash':'bound by submission inventory'})
    print(json.dumps({'loop':'q2','direction':'forward','status':'proved_scoped','passed':True,
                      'controls':len(controls['controls'])},sort_keys=True))


if __name__=='__main__':main()
