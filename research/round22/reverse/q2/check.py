#!/usr/bin/env python3
"""Q2 exact shared-path spectra, Haar weights, Schur and memory controls."""
from __future__ import annotations
import argparse
from collections import Counter,deque
from fractions import Fraction as F
import hashlib
import importlib.util
import itertools
import json
from math import factorial
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
CONTRACT=ROOT/'research/round22/contracts/q2.json'
CONTRACT_HASH='7b8e7a1dfc4d7d4bb05d7123d26396e0333f48e2bb68f34dfc82703707d0612f'
HELPER=ROOT/'research/round22/reverse/q1/check.py'
HELPER_HASH='40204a8962b84e5a71a7aceb0f6b999eb429d0fcfc9b58db82d645ff96a4fb17'
LEDGER='research/round19/forward/c1/output/graph-reduction.json'


def need(ok,message):
    if not ok: raise RuntimeError(message)


def sha(p):
    need(p.is_file(),'required source absent: '+str(p))
    for q in (p,*p.parents): need(not q.is_symlink(),'symlink input')
    return hashlib.sha256(p.read_bytes()).hexdigest()


def dump(p,data): p.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
def sh(v,a): return tuple(x+(i==a) for i,x in enumerate(v))
def reverse(word): return [(e,-s) for e,s in reversed(word)]


def load_helper():
    need(sha(HELPER)==HELPER_HASH,'frozen own arithmetic helper changed')
    spec=importlib.util.spec_from_file_location('q2_own_q1_arithmetic',HELPER)
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def graph_control(M):
    vertices=list(itertools.product(range(3),range(3),range(2)))
    edges=[(a,v,sh(v,a)) for a in range(3) for v in vertices if sh(v,a) in vertices]
    index={(a,s):i for i,(a,s,t) in enumerate(edges)}
    tree=set(range(16))|{26}; root=(0,2,0); paths={root:[]}; queue=[root]
    for v in queue:
        for e in sorted(tree):
            a,s,t=edges[e]
            if v==s and t not in paths: paths[t]=paths[v]+[(e,1)]; queue.append(t)
            if v==t and s not in paths: paths[s]=paths[v]+[(e,-1)]; queue.append(s)
    need(len(paths)==18,'actual spanning tree')
    _,s,t=edges[28]; loop=paths[s]+[(28,1)]+reverse(paths[t]); loopset={e for e,s in loop}
    need(loop==[(14,-1),(2,1),(28,1),(3,-1),(15,1),(26,-1)],'frozen f1 physical completion')
    old=json.loads((ROOT/LEDGER).read_text()); inherited={f['id']:f for f in old['affected_faces']+old['constant_faces']}
    faces=[]
    for a,b in ((0,1),(0,2),(1,2)):
        for v in vertices:
            if sh(v,a) not in vertices or sh(v,b) not in vertices: continue
            w=[(index[a,v],1),(index[b,sh(v,a)],1),(index[a,sh(v,b)],-1),(index[b,v],-1)]
            need([{'edge':e,'sign':s} for e,s in w]==inherited[len(faces)]['signed_word'],'actual signed face ledger')
            faces.append(w)
    adjacency={v:[] for v in vertices}
    for e,(a,s,t) in enumerate(edges):
        need((sum(s)-sum(t))%2==1,'actual graph bipartition')
        adjacency[s].append((t,e)); adjacency[t].append((s,e))
    shortest=100
    for blocked,(a,start,end) in enumerate(edges):
        distance={start:0}; q=deque([start])
        while q:
            v=q.popleft()
            for w,e in adjacency[v]:
                if e!=blocked and w not in distance: distance[w]=distance[v]+1;q.append(w)
        if end in distance: shortest=min(shortest,distance[end]+1)
    need(shortest==4 and F(3,4)*shortest==3,'actual complementary electric gap geometry')
    # Reconstruct coherent three-path orientations for each overlapping face.
    classes={i:[] for i in range(4)}; decompositions=[]
    original={e:M.POOL[e%4] for e in range(33)}
    for p,w in enumerate(faces):
        if p==8: continue
        common=loopset&{e for e,s in w}; m=len(common); classes[m].append(p)
        if not m: continue
        starts=[i for i in range(6) if loop[i][0] in common and loop[(i-1)%6][0] not in common]
        need(len(starts)==1,'shared support must be one consecutive path')
        rotated=loop[starts[0]:]+loop[:starts[0]]
        pathP=rotated[:m];pathR=reverse(rotated[m:])
        need({e for e,s in pathP}==common,'shared path length and set')
        matches=[]
        for orientation in (w,reverse(w)):
            for j in range(4):
                face=orientation[j:]+orientation[:j]
                if face[:m]==pathP: matches.append(face)
        need(len(matches)==1,'coherent face/shared-path orientation')
        pathQ=reverse(matches[0][m:])
        need([len(pathP),len(pathR),len(pathQ)]==[m,6-m,4-m],'three exact path lengths')
        sets=[{e for e,s in w} for w in (pathP,pathR,pathQ)]
        need(sum(len(s) for s in sets)==len(set.union(*sets)),'path Haar independence requires edge disjointness')
        qp,qr,qq=[M.qword(path,original) for path in (pathP,pathR,pathQ)]
        dot=lambda u,v:sum((a*b for a,b in zip(u,v)),F(0))
        g=2*dot(qp,qr)*dot(qp,qq)
        need(g==2*M.qword(loop,original)[0]*M.qword(w,original)[0],'actual signed product versus path model')
        decompositions.append({'face':p,'m':m,'P':pathP,'R':pathR,'Q':pathQ})
    need(classes=={0:[4,5,6,7,11,13,14,18,19],1:[0,1,10,12,16,17],2:[2,3],3:[9,15]},'actual shared-path classes')
    face_sets=[{e for e,s in w} for w in faces]
    random=[p for p in range(20) if p!=8]
    parity_g={p:face_sets[p]^loopset for p in random}
    need(len({tuple(sorted(s)) for s in parity_g.values()})==19,'distinct spectral center sectors')
    crossing=[(p,q) for p in random for q in random if face_sets[p]==parity_g[q]]
    need(crossing==[(9,15),(15,9)],'actual off-diagonal parity selection')
    leaf_counts=Counter(v for v in edges[0][1:])
    need(sum(n==1 for n in leaf_counts.values())==2,'one-link nontrivial irrep is not Gauss-admissible')
    return classes,{'outcome':'wrong physical completion, independent shared-edge spins and scalar cross-channel omission rejected',
                    'passed':True,'full_graph_counts':[18,33,20],'tree':sorted(tree),'f1_loop':loop,
                    'girth':shortest,'complement_electric_lower_over_alpha':'3','sharp_complement_witness':'physical W0',
                    'face_classes_by_shared_path':classes,'three_path_decompositions':decompositions,
                    'mutually_distinct_B1f1_face_center_patterns':19,'cross_channel_allowed_pairs':crossing}


def casimir(M,p,group):
    answer={}
    for monomial,c in p.items():
        n=sum(v//4==group for v in monomial)
        if n: answer[monomial]=answer.get(monomial,F(0))+c*F(n*(n+2),4)
        count=Counter(monomial)
        for a in range(4):
            i=4*group+a
            if count[i]>=2:
                remainder=list(monomial);remainder.remove(i);remainder.remove(i);term=tuple(remainder)
                answer[term]=answer.get(term,F(0))-c*F(count[i]*(count[i]-1),4)
    return {m:c for m,c in answer.items() if c}


def spectral_control(M,classes):
    dot=lambda i,j:M.pa(*(M.pm(M.pv(4*i+a),M.pv(4*j+a)) for a in range(4)))
    pr,pq,rq=dot(0,1),dot(0,2),dot(1,2)
    g=M.ps(M.pm(pr,pq),2); low=M.expect(g,frozenset({0})); high=M.pa(g,M.ps(low,-1))
    need(low==M.ps(rq,F(1,2)),'shared-path spin zero projection')
    average=lambda p:M.expect(p,frozenset({0,1,2})).get((),F(0))
    need(average(M.pm(low,low))==F(1,16) and average(M.pm(high,high))==F(3,16),'exact Haar recoupling weights')
    need(average(M.pm(low,high))==0 and average(M.pm(g,g))==F(1,4),'orthogonal full path decomposition')
    need(not casimir(M,low,0) and casimir(M,high,0)==M.ps(high,2),'exact shared-path Casimir eigenvalues')
    for component in (low,high):
        for group in (1,2): need(casimir(M,component,group)==M.ps(component,F(3,4)),'unshared path fundamental Casimir')
    weights={}
    for m,faces in classes.items():
        count=len(faces)
        if m==0: weights[F(15,2)]=weights.get(F(15,2),F(0))+F(count,4);continue
        lo=F(3*(10-2*m),4);hi=lo+2*m
        for component,energy in ((low,lo),(high,hi)):
            action=M.pa(M.ps(casimir(M,component,0),m),M.ps(casimir(M,component,1),6-m),M.ps(casimir(M,component,2),4-m))
            need(action==M.ps(component,energy),'actual shared-path electric eigenfunction')
        weights[lo]=weights.get(lo,F(0))+F(count,16)
        weights[hi]=weights.get(hi,F(0))+F(3*count,16)
    expected={F(3):F(1,8),F(9,2):F(1,8),F(6):F(3,8),F(15,2):F(9,4),F(8):F(9,8),F(17,2):F(3,8),F(9):F(3,8)}
    need(weights==expected,'seven actual nonconstant channel spectral weights')
    triple=average(M.ps(M.pm(M.pm(pq,pr),rq),2))
    need(triple==F(1,8),'off-diagonal actual triple Haar integral')
    matrices={energy:[[F(19,4) if energy==3 else F(0),2*triple if energy==3 else F(0)],
                      [2*triple if energy==3 else F(0),weight]] for energy,weight in sorted(weights.items())}
    summed=[[sum((w[i][j] for w in matrices.values()),F(0)) for j in range(2)] for i in range(2)]
    need(summed==[[F(19,4),F(1,4)],[F(1,4),F(19,4)]],'Q1 multiplier matrix consistency')
    # Independent direct selected Haar check with the frozen normalized channel pair.
    d=M.pa(M.pc(F(19,4)),M.ps(M.pa(dot(28,24),M.pv(4*28),M.pv(4*24)),F(1,2)))
    basis=[M.pc(1),M.ps(M.pv(4*28),2)]; selected=frozenset({24,27,28})
    for i in range(2):
        for j in range(2):
            gram=M.expect(M.pm(basis[i],basis[j]),selected).get((),F(0))
            need(gram==int(i==j),'frozen channel orthonormality')
            value=M.expect(M.pm(d,M.pm(basis[i],basis[j])),selected).get((),F(0))
            need(value==summed[i][j],'spectral weight sum versus exact conditional multiplier')
    energy11=sum((e*w for e,w in weights.items()),F(0));energy00=F(19,4)*3
    need(energy11==F(285,8)!=energy00==F(57,4),'nonconstant delay dependence rejects scalar reference')
    for energy,w in matrices.items():
        need(w[0][0]>=0 and w[1][1]>=0 and w[0][0]*w[1][1]-w[0][1]**2>=0,'positive matrix spectral weight')
    at_one=[[sum((w[i][j]/(e+1) for e,w in matrices.items()),F(0)) for j in range(2)] for i in range(2)]
    need(at_one[0][1]==F(1,16) and at_one[0][0]==F(19,16) and at_one[1][1]!=at_one[0][0],'nonconstant self-energy fixture at z/alpha=1')
    records=[{'energy_over_alpha':str(e),'matrix':[[str(x) for x in row] for row in w]} for e,w in matrices.items()]
    return records,{'outcome':'scalar memory, missing off-diagonal and spurious intermediate shared-path energies rejected',
                    'passed':True,'shared_path_spin0_norm_squared':'1/16','shared_path_spin1_norm_squared':'3/16',
                    'cross_pair_triple_integral':'1/8','offdiagonal_energy3_weight':'1/4',
                    'spectral_weights':records,'kernel_zero_delay_matrix':[[str(x) for x in row] for row in summed],
                    'reference_energy_moment':'57/4','nonconstant_energy_moment':'285/8',
                    'self_energy_divided_by_alpha_lambda_squared_at_z_over_alpha_1':[[str(x) for x in row] for row in at_one],
                    'finite_spectral_sector_is_exact':True,'numerical_cutoff_used':False}


def mm(a,b): return [[sum((x*y for x,y in zip(row,col)),F(0)) for col in zip(*b)] for row in a]
def add(a,b): return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def scale(a,c): return [[c*x for x in row] for row in a]
def subtract(a,b): return add(a,scale(b,-1))
def mat(rows): return [[F(x) for x in row] for row in rows]
def eye(n): return [[F(i==j) for j in range(n)] for i in range(n)]
def corner(a): return [row[:2] for row in a[:2]]


def power(a,n):
    r=eye(len(a))
    for i in range(n): r=mm(r,a)
    return r


def inverse(a):
    n=len(a); aug=[list(row)+unit for row,unit in zip(a,eye(n))]
    for i in range(n):
        pivot=next((j for j in range(i,n) if aug[j][i]),None)
        need(pivot is not None,'singular rational inverse')
        aug[i],aug[pivot]=aug[pivot],aug[i];factor=aug[i][i];aug[i]=[x/factor for x in aug[i]]
        for j in range(n):
            if i!=j:
                factor=aug[j][i];aug[j]=[x-factor*y for x,y in zip(aug[j],aug[i])]
    return [row[n:] for row in aug]


def block_control():
    h0=mat([[0,0,0],[0,2,0],[0,0,3]]);v=mat([[2,1,1],[1,2,-1],[1,-1,2]])
    need(v==subtract(scale(eye(3),3),mat([[1,-1,-1],[-1,1,1],[-1,1,1]])),'positive rank-complement perturbation')
    lam=F(1,5);h=add(h0,scale(v,lam));a=corner(h);c=h[2][2]
    b=[[h[2][0],h[2][1]]];bt=[[x] for x in b[0]];d=mm(bt,b)
    need(mm(a,d)!=mm(d,a),'noncommuting block fixture')
    z=F(1);sigma=scale(d,1/(c+z))
    schur=subtract(add(a,scale(eye(2),z)),sigma)
    correct=corner(inverse(add(h,scale(eye(3),z))))
    need(inverse(schur)==correct,'exact Schur compressed resolvent')
    need(inverse(add(add(a,scale(eye(2),z)),sigma))!=correct,'wrong self-energy sign must reject')
    shift=F(1,3);new_z=F(2,3)
    need(corner(inverse(add(add(h,scale(eye(3),shift)),scale(eye(3),new_z))))==correct,'consistent scalar/spectral shift')
    correct_shift=subtract(add(add(a,scale(eye(2),shift)),scale(eye(2),new_z)),scale(d,1/(c+shift+new_z)))
    wrong_shift=subtract(add(add(a,scale(eye(2),shift)),scale(eye(2),new_z)),scale(d,1/(c+new_z)))
    need(inverse(correct_shift)==correct and inverse(wrong_shift)!=correct,'complement energy shift cannot be omitted')
    # Power-series coefficient recurrence from the exact differential Volterra equation.
    nmax=6; exact=[scale(corner(power(h,n)),F((-1)**n,factorial(n))) for n in range(nmax+1)]
    free=[scale(power(a,n),F((-1)**n,factorial(n))) for n in range(nmax+1)]
    kernel=[scale(d,(-c)**n/factorial(n)) for n in range(nmax+1)]
    def recurrence(drop_returns):
        ts=[eye(2)]
        for n in range(nmax):
            rhs=scale(mm(a,ts[n]),-1)
            for k in range(n):
                ell=n-1-k
                rhs=add(rhs,scale(mm(kernel[k],free[ell] if drop_returns else ts[ell]),F(factorial(k)*factorial(ell),factorial(n))))
            ts.append(scale(rhs,F(1,n+1)))
        return ts
    good=recurrence(False);bad=recurrence(True)
    need(good==exact,'exact Volterra returns/order through degree6')
    mismatches=[n for n in range(nmax+1) if bad[n]!=exact[n]]
    need(mismatches and mismatches[0]==4,'omitted memory return must fail at degree4')
    need(subtract(exact[4],bad[4])==scale(mm(d,d),F(1,24)),'exact omitted-return leading defect')
    need(corner(inverse(add(h0,eye(3))))==inverse(add(corner(h0),eye(2))),'lambda0 resolvent recovery')
    return {'outcome':'wrong Schur sign, omitted complementary scalar shift and omitted memory return rejected','passed':True,
            'scope':'positive finite noncommuting block algebra only; not the physical spectral calculation',
            'lambda':'1/5','z':'1','compressed_resolvent':[[str(x) for x in row] for row in correct],
            'Volterra_coefficients_exact_through_degree':6,'omitted_return_first_mismatch_degree':4,
            'omitted_return_degree4_defect':[[str(x) for x in row] for row in subtract(exact[4],bad[4])],
            'zero_coupling_recovered':True}


def remainder_control():
    bnorm2=F(25,4);vnorm=F(40);gap=F(3);end=F(1,100)
    coefficient=bnorm2*vnorm
    need(coefficient==250,'full-Hilbert remainder coefficient')
    need(coefficient*end**3/gap**2==F(1,36000),'uniform small-z endpoint error')
    need(coefficient*end**3/gap==F(1,12000),'uniform-delay endpoint error coefficient before 1/e')
    need(vnorm*end/gap==F(2,15)<1,'declared weak interval included')
    need(coefficient*F(0)**3==0,'zero-coupling remainder')
    need(1-gap*F(1,3)==0,'absolute delay envelope stationary point')
    return {'outcome':'cubic full-Hilbert bounds and zero coupling checked; no singular complement small-z shortcut',
            'passed':True,'valid_coupling_range':'all lambda>=0','required_weak_interval':'0<=lambda<=1/100',
            'complement_gap_over_alpha':'3','B1_norm_squared':'25/4','QVmagQ_norm_upper':'40',
            'kernel_remainder':'250*alpha^3*lambda^3*(s/hbar)*exp(-3*alpha*s/hbar)',
            'self_energy_remainder':'250*alpha^3*lambda^3/(3*alpha+z)^2',
            'uniform_delay_remainder':'250*alpha^2*lambda^3/(3*e)',
            'uniform_small_z_remainder':'250*alpha*lambda^3/9',
            'at_lambda_1_over_100_uniform_delay':'alpha^2/(12000*e)',
            'at_lambda_1_over_100_uniform_small_z':'alpha/36000',
            'uniform_relative_late_delay_claimed':False,'uniform_full_resolvent_as_z_down_to_zero_claimed':False}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True)
    args=parser.parse_args();out=Path(args.output).absolute()
    for p in (out,*out.parents): need(not p.is_symlink(),'symlink output')
    need(not out.exists(),'fresh output required')
    need(sha(CONTRACT)==CONTRACT_HASH,'frozen Q2 contract changed')
    contract=json.loads(CONTRACT.read_text())
    for rel,digest in contract['dependencies'].items(): need(sha(ROOT/rel)==digest,'inherited dependency changed: '+rel)
    M=load_helper();classes,graph=graph_control(M);weights,spectral=spectral_control(M,classes)
    controls={'schema':'ym22-reverse-q2-controls-v1','loop':'q2','direction':'reverse','status':'passed','passed':True,
              'actual_graph_and_complement':graph,'exact_channel_spectra':spectral,
              'Schur_and_memory_controls':block_control(),'operator_remainders':remainder_control()}
    results={'schema':'ym22-reverse-q2-results-v1','loop':'q2','direction':'reverse',
             'status':'proved_actual_projected_memory_spectra_and_controlled_remainders','passed':True,
             'claims':{'complement_electric_lower_over_alpha':'3','complement_electric_lower_sharp':True,
                       'complement_operator_domain':'QD(H_E)','complement_form_domain':'QD(H_E^(1/2))',
                       'C_lambda_lower':'3*alpha for lambda>=0','exact_Volterra_right_factor':'T_lambda(r)',
                       'exact_Volterra_kernel':'B_lambda* exp(-s*C_lambda/hbar) B_lambda',
                       'exact_compressed_resolvent':'(A_lambda+z-Sigma_lambda(z))^-1',
                       'Schur_operator_domain':'D(A_lambda)','Schur_lower':'z for z>0',
                       'channels':['1','2x with actual P2 U28 completion'],'leading_spectral_weights':weights,
                       'leading_kernel_formula':'(alpha*lambda)^2 sum_epsilon W_epsilon exp(-epsilon*alpha*s/hbar)',
                       'leading_self_energy_formula':'(alpha*lambda)^2 sum_epsilon W_epsilon/(epsilon*alpha+z)',
                       'offdiagonal_energy3_weight':'1/4','nonconstant_channel_spectral_energy_count':7,
                       'kernel_full_Hilbert_remainder':'250*alpha^3*lambda^3*(s/hbar)*exp(-3*alpha*s/hbar)',
                       'self_energy_full_Hilbert_remainder':'250*alpha^3*lambda^3/(3*alpha+z)^2',
                       'bounds_hold_for_all_lambda_ge_zero':True,'required_weak_interval_included':True,
                       'absolute_kernel_error_uniform_in_delay':True,'self_energy_error_uniform_as_z_down_to_zero':True,
                       'uniform_relative_late_delay_accuracy_claimed':False,'operator_norm_time_Taylor_claimed':False,
                       'finite_spectral_cutoff_used':False,'finite_autonomous_closure_proved':False,
                       'interacting_ground_identified':False,'homogeneous_or_continuum_transfer':False},
             'target_verdict':'Exact graph-specific two-channel spectral memory and self-energy accompany the full projected identities and cubic operator remainders.',
             'next_loop_selected':False}
    rels=list(contract['dependencies'])+contract['instruction_inputs']+[
        'research/round22/reverse/q1/report.md','research/round22/reverse/q1/source-review.json',
        'research/round22/reverse/p2/report.md','research/round22/reverse/p2/source-review.json',
        'research/round22/reverse/n1/inputs/advisor-finite-observations.md',
        'research/round22/reverse/n1/inputs/paired-admission-matching.md']
    inputs=[CONTRACT,HELPER,HERE/'report.md',HERE/'check.py',HERE/'independence.json',HERE/'source-review.json']+[ROOT/r for r in rels]
    hashes={str(p.relative_to(ROOT)):sha(p) for p in sorted(set(inputs))}
    need(all(r in hashes for r in contract['instruction_inputs']),'complete immutable instruction closure')
    out.mkdir(parents=True)
    for name,payload in [('results.json',results),('controls.json',controls)]: dump(out/name,payload)
    dump(out/'source-manifest.json',{'schema':'ym22-source-manifest-v1','inputs':hashes,
                                   'outputs':{n:sha(out/n) for n in ('results.json','controls.json')}})
    print(json.dumps({'loop':'q2','direction':'reverse','status':results['status'],'passed':True}))


if __name__=='__main__': main()
