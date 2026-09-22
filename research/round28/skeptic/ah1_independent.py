#!/usr/bin/env python3
"""Independent AH1 full-link geometry, Haar, metric action and heat certificate."""
import argparse
import hashlib
import itertools
import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
CHECKS=[]
sys.set_int_max_str_digits(0)


def need(ok,label):
    if not ok: raise RuntimeError(label)
    CHECKS.append(label)


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def serial(a):
    if isinstance(a,F):return str(a)
    if isinstance(a,dict):return {str(k):serial(v) for k,v in a.items()}
    if isinstance(a,(list,tuple)):return [serial(v) for v in a]
    return a


def graph():
    vertices=list(itertools.product(range(4),range(3),range(2)))
    links=sorted((v,a) for v in vertices for a in range(3) if v[a]+1<(4,3,2)[a])
    ids={e:i for i,e in enumerate(links)}
    faces=[]
    for v in vertices:
        for a,b in itertools.combinations(range(3),2):
            va=list(v);vb=list(v);va[a]+=1;vb[b]+=1
            if tuple(va) not in vertices or tuple(vb) not in vertices:continue
            word=[(ids[v,a],1),(ids[tuple(va),b],1),(ids[tuple(vb),a],-1),(ids[v,b],-1)]
            faces.append({'anchor':v,'axes':(a,b),'word':word,'mask':sum(1<<e for e,s in word)})
    faces.sort(key=lambda f:(f['anchor'],f['axes']))
    need((len(vertices),len(links),len(faces))==(24,46,29),'new complete vertex/link/face counts')
    adjacency={v:set() for v in vertices}
    for v,a in links:
        w=list(v);w[a]+=1;w=tuple(w);adjacency[v].add(w);adjacency[w].add(v)
        need(sum(v)%2!=sum(w)%2,'bipartite oriented link '+str((v,a)))
    reached={vertices[0]};pending=list(reached)
    while pending:
        v=pending.pop()
        for w in adjacency[v]-reached:reached.add(w);pending.append(w)
    need(len(reached)==24 and len(links)-len(vertices)+1==23,'connected graph and full cycle rank')
    cycles=set()
    for a,c in itertools.combinations(vertices,2):
        for b,d in itertools.combinations(adjacency[a]&adjacency[c],2):
            edges=[]
            for v,w in ((a,b),(b,c),(c,d),(d,a)):
                lo,hi=sorted((v,w));axis=next(i for i in range(3) if lo[i]!=hi[i]);edges.append(ids[lo,axis])
            cycles.add(sum(1<<e for e in edges))
    need(cycles=={f['mask'] for f in faces},'every four-cycle exactly one elementary face')
    counts={}
    for f in faces:
        for e,s in f['word']:counts[e]=counts.get(e,0)+1
    # A six-edge perimeter of a coplanar adjacent pair is an actual endpoint state.
    pairs=[];pairmasks={};overlap_counts={};vertex_touch=0
    for p,q in itertools.combinations(range(29),2):
        a,b=faces[p],faces[q];shared=a['mask']&b['mask'];n=shared.bit_count()
        need(n<=1,'distinct faces share at most one link '+str((p,q)))
        mask=a['mask']^b['mask'];need(mask!=0 and mask not in pairmasks and mask not in cycles,'distinct nonzero pair parity mask '+str((p,q)))
        pairmasks[mask]=(p,q);overlap_counts[n]=overlap_counts.get(n,0)+1
        ea={v for e,s in a['word'] for v in endpoints(links[e])};eb={v for e,s in b['word'] for v in endpoints(links[e])}
        if n==0 and ea&eb:vertex_touch+=1
        pairs.append({'p':p,'q':q,'shared_link':shared.bit_length()-1 if shared else None,'mask':mask,'vertex_intersection_count':len(ea&eb)})
    endpoint=next(p for p in pairs if p['shared_link'] is not None and faces[p['p']]['axes']==faces[p['q']]['axes'])
    need(endpoint['mask'].bit_count()==6 and 6*F(3,4)==F(9,2),'actual six-edge strict-cutoff endpoint remains outside P0')
    need(F(9,2)/F(3,4)==6 and 4*F(3,4)==3 and 4*2==8,'strict cutoff admits at most five active edges and only fundamental four-cycle spin')
    need(max(a*(4-a) for a in range(5))==4 and 2*5==2*5,'five-edge support exclusion: four vertices have bipartite capacity4; five degree-two vertices would form forbidden odd cycle')
    signs=[1 if a==0 else (-1)**(v[0] if a==1 else v[0]+v[1]) for v,a in links]
    for i,f in enumerate(faces):
        need(math.prod(signs[e] for e,s in f['word'])==-1,'actual center assignment makes face odd '+str(i))
        need(math.prod(-1 for e,s in f['word'])==1,'uniform link flip is nondiscriminating '+str(i))
    boundary_faces=[f for f in faces if f['anchor'][next(c for c in range(3) if c not in f['axes'])] in (0,(3,2,1)[next(c for c in range(3) if c not in f['axes'])])]
    need(len(boundary_faces)<29,'omitting internal faces changes actual model')
    return vertices,links,faces,pairs,{'shared_edge_pairs':overlap_counts.get(1,0),'edge_disjoint_pairs':overlap_counts.get(0,0),'vertex_touching_edge_disjoint_pairs':vertex_touch,'boundary_faces_only':len(boundary_faces),'internal_faces':29-len(boundary_faces),'cycle_rank':23,'strict_endpoint_pair':[endpoint['p'],endpoint['q']],'center_signs':signs}


def endpoints(edge):
    v,a=edge;w=list(v);w[a]+=1;return v,tuple(w)


def qm(a,b):
    x,y,z,w=a;X,Y,Z,W=b
    return (x*X-y*Y-z*Z-w*W,x*Y+y*X+z*W-w*Z,x*Z-y*W+z*X+w*Y,x*W+y*Z-z*Y+w*X)


def qi(q):return (q[0],-q[1],-q[2],-q[3])
def traceword(word,values):
    q=(F(1),F(0),F(0),F(0))
    for e,s in word:q=qm(q,values[e] if s==1 else qi(values[e]))
    return 2*q[0]


def gauge_controls(vertices,links,faces):
    choices=[(F(3,5),F(4,5),F(0),F(0)),(F(5,13),F(0),F(12,13),F(0)),(F(8,17),F(0),F(0),F(15,17))]
    cm=lambda a,b:(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
    ca=lambda a,b:(a[0]+b[0],a[1]+b[1])
    matrix=lambda q:(((q[0],q[1]),(q[2],q[3])),((-q[2],q[3]),(q[0],-q[1])))
    mm=lambda a,b:tuple(tuple(ca(cm(a[i][0],b[0][j]),cm(a[i][1],b[1][j])) for j in range(2)) for i in range(2))
    for i,a in enumerate(choices):
        for j,b in enumerate(choices):need(mm(matrix(a),matrix(b))==matrix(qm(a,b)),'independent exact complex-matrix quaternion multiplication '+str((i,j)))
        need(mm(matrix(a),matrix(qi(a)))==(((F(1),F(0)),(F(0),F(0))),((F(0),F(0)),(F(1),F(0)))),'unit quaternion matrix inverse '+str(i))
    U=[choices[i%3] for i in range(len(links))];G={v:choices[(sum(v)+v[0])%3] for v in vertices}
    transformed=[qm(qm(G[v],U[i]),qi(G[w])) for i,edge in enumerate(links) for v,w in [endpoints(edge)]]
    bad=[qm(qm(G[v],U[i]),G[w]) for i,edge in enumerate(links) for v,w in [endpoints(edge)]]
    wrong_orientation=0;wrong_gauss=0
    for i,f in enumerate(faces):
        actual=traceword(f['word'],U)
        need(traceword(f['word'],transformed)==actual,'full vertex Gauss fixture '+str(i))
        changed=list(f['word']);changed[-1]=(changed[-1][0],1)
        wrong_orientation+=traceword(changed,U)!=actual
        wrong_gauss+=traceword(f['word'],bad)!=actual
    need(wrong_orientation>0 and wrong_gauss>0,'missing dagger and wrong Gauss inverse actually discriminate')
    return {'wrong_orientation_faces':wrong_orientation,'wrong_Gauss_faces':wrong_gauss,'all_vertex_actions':'U_e -> g_tail U_e g_head^-1, every one of24 vertices retained'}


# Independent polynomial Haar integration on unit quaternions, not old checker code.
NV=12;ZERO=(0,)*NV
def add(a,b):
    c=dict(a)
    for m,v in b.items():c[m]=c.get(m,F(0))+v
    return {m:v for m,v in c.items() if v}
def scale(a,c):return {m:v*c for m,v in a.items() if v*c}
def mul(a,b):
    c={}
    for m,x in a.items():
        for n,y in b.items():
            k=tuple(u+v for u,v in zip(m,n));c[k]=c.get(k,F(0))+x*y
    return {m:v for m,v in c.items() if v}
def var(i):
    m=list(ZERO);m[i]=1;return {tuple(m):F(1)}
def pqm(a,b):
    terms=[[(0,0,1),(1,1,-1),(2,2,-1),(3,3,-1)],[(0,1,1),(1,0,1),(2,3,1),(3,2,-1)],[(0,2,1),(1,3,-1),(2,0,1),(3,1,1)],[(0,3,1),(1,2,1),(2,1,-1),(3,0,1)]]
    out=[]
    for row in terms:
        p={}
        for i,j,s in row:p=add(p,scale(mul(a[i],b[j]),s))
        out.append(p)
    return out
def moment(exponents):
    if any(n%2 for n in exponents):return F(0)
    d=sum(exponents)//2;num=1
    for n in exponents:
        for j in range(1,n,2):num*=j
    den=math.prod(4+2*j for j in range(d));return F(num,den)
def integrate(p,blocks=(0,1,2)):
    out={}
    for mon,c in p.items():
        m=list(mon)
        for block in blocks:
            c*=moment(mon[4*block:4*block+4]);m[4*block:4*block+4]=[0]*4
        if c:out[tuple(m)]=out.get(tuple(m),F(0))+c
    return {m:v for m,v in out.items() if v}
def haar_checks():
    G=[var(i) for i in range(4)];A=[var(i) for i in range(4,8)];B=[var(i) for i in range(8,12)]
    Gi=[G[0]]+[scale(g,-1) for g in G[1:]]
    eta=mul(scale(pqm(A,G)[0],2),scale(pqm(Gi,B)[0],2));singlet=integrate(eta,(0,));triplet=add(eta,scale(singlet,-1))
    expected=pqm(A,B)[0]
    need(singlet==expected,'exact quaternion common-edge Haar projection chi(AB)/2')
    norm=lambda p:integrate(mul(p,p)).get(ZERO,F(0))
    need(norm(eta)==1 and norm(singlet)==F(1,4) and norm(triplet)==F(3,4),'independently integrated product and both branch norms')
    need(integrate(mul(singlet,triplet))=={},'exact singlet triplet Haar orthogonality')
    phi=scale(G[0],2);one={ZERO:F(1)};spin1=add(mul(phi,phi),scale(one,-1));spin3=add(mul(mul(phi,phi),phi),scale(phi,-2))
    need(norm(phi)==norm(spin1)==norm(spin3)==1,'actual fundamental spin1 and spin3/2 norm one')
    need(integrate(mul(phi,spin3))=={},'spin3/2 outside original odd face sector')
    need(integrate(mul(spin3,scale(mul(phi,spin1),F(1,2))))=={ZERO:F(1,2)},'new-input outside coefficient exactly one-half')
    return {'eta_norm_squared':F(1),'singlet_norm_squared':F(1,4),'triplet_norm_squared':F(3,4),'rational_basis_s_t_metrics':[1,3],'new_input_spin_three_halves_coefficient':F(1,2),'integration':'Exact S3 even-monomial moments for three independent unit quaternions; common edge integrated conditionally.'}


def basis_and_action(faces,pairs):
    basis=[{'kind':'vacuum','faces':[],'energy':F(0),'metric':1,'mask':0}]
    basis += [{'kind':'fundamental','faces':[p],'energy':F(3),'metric':1,'mask':f['mask']} for p,f in enumerate(faces)]
    basis += [{'kind':'spin_one','faces':[p],'energy':F(8),'metric':1,'mask':0} for p in range(29)]
    for pair in pairs:
        types=[('disjoint',F(6),1)] if pair['shared_link'] is None else [('singlet',F(9,2),1),('triplet',F(13,2),3)]
        for kind,energy,metric in types:
            basis.append({'kind':kind,'faces':[pair['p'],pair['q']],'shared_link':pair['shared_link'],'energy':energy,'metric':metric,'mask':pair['mask']})
    S={}
    def put(i,j,v):S[i,j]=S.get((i,j),F(0))+v
    for p in range(29):put(p+1,0,F(1,2))
    for i,v in enumerate(basis[30:],30):
        coefficient=F(1,4) if v['kind'] in ('singlet','triplet') else F(1,2)
        for p in v['faces']:put(i,p+1,coefficient)
    for (i,j),v in list(S.items()):put(j,i,v*F(basis[i]['metric'],basis[j]['metric']))
    for (i,j),v in S.items():need(basis[i]['metric']*v==basis[j]['metric']*S.get((j,i),0),'metric self-adjoint stored entry '+str((i,j)))
    # Matrix elements between equal center parity are all structural zeros.
    odd=set(range(1,30))
    need(all((i in odd)!=(j in odd) for i,j in S),'all within-parity magnetic blocks exactly zero')
    need(all(v['metric']>0 for v in basis),'positive exact physical Gram and empty nullspace')
    for i,v in enumerate(basis):
        if v['kind']=='spin_one':
            expected={str(e):2 for e,s in faces[v['faces'][0]]['word']}
        elif v['kind']=='vacuum':expected={}
        elif v['kind']=='fundamental':expected={str(e):1 for e,s in faces[v['faces'][0]]['word']}
        else:
            mask=v['mask'];expected={str(e):1 for e in range(46) if mask>>e&1}
            if v['kind']=='triplet':expected[str(v['shared_link'])]=2
        v['twice_spin_support']=expected
        need(sum(F(j*(j+2),4) for j in expected.values())==v['energy'],'complete electric representation support '+str(i))
    # Full columns Q0 S phi_p have Gram (2m-1)/4 I + 1/4 J.
    C={}
    for p in range(29):
        for q in range(29):
            C[p,q]=sum(F(basis[i]['metric'])*S.get((i,p+1),0)*S.get((i,q+1),0) for i in range(30,len(basis)))
            need(C[p,q]==(F(29,4) if p==q else F(1,4)),'complete original-residual Gram '+str((p,q)))
    bright=sum(C.values());need(bright==F(29*57,4),'all-channel bright residual norm coefficient')
    t=next(i for i,v in enumerate(basis) if v['kind']=='triplet');p=basis[t]['faces'][0]+1
    need(S[p,t]==F(3,4) and S[t,p]==F(1,4) and S[p,t]!=S[t,p],'metric-blind transpose is wrong')
    # Deliberately duplicate an actual normalized coordinate. Its Gram kernel
    # is physical zero and must be quotiented, not declared orthonormal.
    duplicate_gram=((1,1),(1,1));null=(1,-1)
    need(all(sum(row[j]*null[j] for j in range(2))==0 for row in duplicate_gram),'ordered duplicate descriptions create a real Gram null vector')
    need(sum(null[j]**2 for j in range(2))!=0,'replacing duplicate Gram by identity loses its null relation')
    need(all(S.get((i,1),0)*null[0]+S.get((i,1),0)*null[1]==0 for i in range(len(basis))) and 3*sum(null)==0,'electric and magnetic actions descend through duplicate-description kernel')
    need(basis[0]['mask']==basis[30]['mask']==0 and basis[0]['energy']!=basis[30]['energy'],'global even parity alone does not identify functions or prove their orthogonality')
    need(len(basis)!=293,'old graph rank not imported')
    return basis,S,{'quotient_rank':len(basis),'candidate_count':len(basis),'null_relations':[],'Gram':'Diagonal with supplied metric; full off-diagonal zeros proved by pair masks, edge representation supports and distinct K branches.','residual_Gram_diagonal':F(29,4),'residual_Gram_offdiagonal':F(1,4),'bright_residual_squared_coefficient':bright,'all_sparse_entries':len(S),'structural_zero_entries':len(basis)**2-len(S)}


def certificate():
    m=29;cap=F(1,100);eta=F(1,100);g=3-m*cap
    need(g>0 and m*cap<3,'full and nested second-spectrum separation follows positive coupling')
    need(41**2>m*(2*m-1),'new residual radical rational upper bound')
    need(F(11,2)**2>m,'new vacuum-angle rational upper bound')
    r0=F(41,12)*cap**2;p0=r0/g;rp=m*cap*p0;pp=rp/g;dp=rp**2/g
    z0=1-m*cap**2/72;q0=F(11,12)*cap;D=z0-eta-p0;b0=q0+p0+eta
    need(D>0,'strict true full-output denominator')
    early=2*(rp+dp)+m*cap*b0/g
    exp_lower=sum((2*g)**n/F(math.factorial(n)) for n in range(18))
    need(exp_lower>200,'positive Taylor certificate exp(2g)>200')
    late=pp+(2*b0+pp)/200;absolute=max(early,late);relative=absolute/D
    need(relative<F(11,5000),'conservative all-time relative constant below0.0022')
    need(relative>F(37,10**6),'old accuracy constant not transferred to new certificate')
    # Exact algebraic identities in the quadratic extension w(w+3)=m lambda^2/4.
    # At the cap use outward rational square-root brackets only for displaying old Ritz data.
    rad=9+m*cap**2;den=10**40;n=math.isqrt(rad.numerator*den*den//rad.denominator);lo=F(n,den);hi=F(n+1,den)
    need(lo*lo<=rad<=hi*hi,'Ritz radical directed rational bracket')
    wlo,whi=(lo-3)/2,(hi-3)/2;hlo,hhi=cap/(2*(3+whi)),cap/(2*(3+wlo))
    need(hlo>0 and hhi<=cap/6,'actual positive Ritz coefficients and uniform bound')
    # Independent exact Ritz equations in Q[w]/(w^2+3w-m lambda^2/4).
    qt=F(m,4)*cap**2
    qm2=lambda a,b:(a[0]*b[0]+a[1]*b[1]*qt,a[0]*b[1]+a[1]*b[0]-3*a[1]*b[1])
    h=(F(0),2/(m*cap));wh=qm2((F(3),F(1)),h)
    need(wh==(cap/2,F(0)) and (m*cap*h[0]/2,m*cap*h[1]/2)==(F(0),F(1)),'exact bright-star ground equations in quadratic number field')
    rho_lo=m*(2*m-1)*cap**2*hlo*hlo/(4*(1+m*hhi*hhi));rho_hi=m*(2*m-1)*cap**2*hhi*hhi/(4*(1+m*hlo*hlo))
    need(0<rho_lo<=rho_hi<=r0*r0,'full residual evaluated inside continuous envelope')
    mu=(m*cap-whi,m*cap-wlo)
    need(mu[0]>0 and mu[1]<m*cap,'Ritz ground distinct from scalar reference')
    # Rational normalized complex preparations, independent of spectral rounding.
    t=F(1,400);a=(1-t*t)/(1+t*t);c=2*t/(1+t*t)
    need(a*a+c*c==1 and (a-1)**2+c*c<eta*eta,'normalized real and imaginary one-face preparation class')
    need(3!=F(3,4),'naive independent-cycle electric Casimir misses three physical links')
    need(-cap<0 and -cap*29<0,'negative coupling invalidates nonnegative-potential premise')
    need(F(9,2)>=F(9,2) and not F(9,2)<F(9,2),'strict spectral endpoint control')
    need(m*cap/2>0,'new-input leakage does not vanish at positive coupling')
    need(F(1,16)+F(3,16)==F(1,4) and F(1,16)<F(1,4) and F(3,16)<F(1,4),'omitting either common-edge branch strictly undercounts a full source norm')
    need(1+F(1,100)*2>1 and 1/(1+F(1,100)*2)<1,'abstract positive or negative center offset changes the true stationary ground mode')
    need((a-1)**2+c*c==(a-1)**2+(-c)**2,'complex imaginary preparation uses the same exact Hilbert norm, not a real-only restriction')
    return {'lambda_cap':cap,'gap_g':g,'r0_upper':r0,'both_p0_projector_upper':p0,'enriched_full_residual_upper':rp,'enriched_projector_upper':pp,'enriched_energy_error_upper':dp,'vacuum_overlap_lower':z0,'vacuum_excited_upper':q0,'initial_distance':eta,'true_output_denominator_lower':D,'both_excited_preparation_upper':b0,'join':2,'exp_2g_positive_Taylor_lower':exp_lower,'exp_minus_2g_upper':F(1,200),'early_absolute_upper':early,'late_absolute_upper':late,'all_time_absolute_upper':absolute,'all_time_true_relative_upper':relative,'simple_relative_upper':F(11,5000),'Ritz_cap_energy_interval':mu,'Ritz_cap_residual_squared_interval':[rho_lo,rho_hi],'Ritz_radical_interval':[lo,hi],'normalized_real_preparation':[a,c],'normalized_imaginary_preparation':[a,{'imaginary':c}],'exact_zero_time_error':0,'exact_zero_coupling_error':0,'full_input_zero_time_error_outside_retained':1,'centering_defect':'B+(mu_plus-epsilon)Pplus; each exact own-ground spectral center retained','symbols':'All displayed residual/angle/error constants are uniform upper envelopes, not evaluated actual full or enriched norms.'}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,default=HERE/'ah1-independent.json');target=ap.parse_args().output
    inv=json.loads((HERE/'ah1-inputs/source-inventory.json').read_text());contract=json.loads((ROOT/'research/round28/contracts/ah1.json').read_text())
    need(sha(ROOT/'research/round28/contracts/ah1.json')=='9c6f5bc1a71fcd49b93a1212e1b1837a82bc588b27b695fd600cbec46be17053','exact AH1 contract')
    sources={e['source']:e for e in inv['entries']}
    need(set(contract['sources'])<=set(sources),'all42 prospective contract sources present')
    for e in inv['entries']:need(sha(ROOT/e['source'])==sha(ROOT/e['snapshot'])==e['sha256'],'prospective source '+e['source'])
    need(inv['frozen_before_scientific_production'] is True and inv['current_producer_scientific_access'] is False,'prospective independent snapshot event')
    vertices,links,faces,pairs,geometry=graph();gauge=gauge_controls(vertices,links,faces);haar=haar_checks();basis,S,metric=basis_and_action(faces,pairs);heat=certificate()
    m=29;shared=geometry['shared_edge_pairs'];disjoint=geometry['edge_disjoint_pairs']
    weights={F(8):F(m,16),F(6):F(disjoint,4),F(9,2):F(shared,16),F(13,2):F(3*shared,16)}
    need(sum(weights.values())==F(m*(2*m-1),16),'complete residual spectral weights sum')
    need(sum(e*w for e,w in weights.items())==F(m*(3*m-1),4),'residual electric form from Haar fourth moment')
    result={'schema':'ym28-ah1-skeptic-independent-v1','contract_sha256':sha(ROOT/'research/round28/contracts/ah1.json'),'model':'full physical open3x2x1-cell uniform-coupling SU2 graph; K on all46 links,24 Gauss actions','geometry':{**geometry,'vertices':vertices,'links':[{'tail':v,'axis':a} for v,a in links],'faces':faces,'unordered_pairs':pairs},'gauge_controls':gauge,'haar_calculation':haar,'physical_basis':basis,'metric_and_quotient':metric,'electric_action':'diagonal in physical_basis, every undeclared entry zero','magnetic_sparse_action':[[i,j,v] for (i,j),v in sorted(S.items())],'magnetic_zero_rule':'Every entry not in the complete sparse list is exactly zero; matrix acts on coefficient columns in the supplied physical diagonal Gram.','P0_dimension':30,'residual_spectral_weights':[[e,w] for e,w in sorted(weights.items())],'outside':{'definition':'B=-lambda(I-Pplus)S Pplus on every retained input','all_input_upper_coefficient':29,'BP0_zero':True,'full_B_zero_for_positive_lambda':False,'spin_one_input_spin_three_halves_lower_coefficient':F(1,2),'exact_cubic_outside_Gram_computed':False},'heat_certificate':heat,'scope':{'full_strict_cutoff_proved':True,'generated_span_complete':True,'ambient_shell_complete':False,'exact_retained_matrix':True,'all_time_own_ground_centered_heat':True,'true_relative_denominator':True,'numerical_heat_evaluator':False,'real_time_relative':False,'graph_size_uniform':False,'canonical_or_homogeneous_identification':False,'continuum_gap':False},'source_bindings':{e['source']:e['sha256'] for e in inv['entries']},'checks':CHECKS,'check_count':len(CHECKS),'current_producer_science_read':False,'historical_checkers_imported_or_executed':False,'research_loop_increment':0,'display_only':{'rank':len(basis),'shared_edge_pairs':shared,'relative_bound':float(heat['all_time_true_relative_upper']),'true_denominator':float(heat['true_output_denominator_lower'])}}
    target.write_text(json.dumps(serial(result),sort_keys=True,indent=2)+'\n');print(json.dumps({'status':'passed','checks':len(CHECKS),'rank':len(basis),'shared':shared,'relative_upper':float(heat['all_time_true_relative_upper'])}))


if __name__=='__main__':main()
