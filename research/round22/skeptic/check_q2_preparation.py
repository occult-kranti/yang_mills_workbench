#!/usr/bin/env python3
"""Independent Q2 graph overlaps, finite exact spectral weights and block signs."""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations,product
from pathlib import Path
import argparse,hashlib,json

def need(ok,why):
    if ok is not True:raise RuntimeError(why)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
def qm(a,b):
    w,x,y,z=a;v,r,s,t=b
    return (w*v-x*r-y*s-z*t,w*r+x*v+y*t-z*s,w*s+y*v+z*r-x*t,w*t+z*v+x*s-y*r)
def mm(a,b):return [[sum((x*y for x,y in zip(row,col)),F(0)) for col in zip(*b)] for row in a]
def add(a,b):return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def scale(a,c):return [[c*x for x in r] for r in a]
def sub(a,b):return add(a,scale(b,-1))
def eye(n):return [[F(i==j) for j in range(n)] for i in range(n)]
def power(a,n):
    ans=eye(len(a))
    for _ in range(n):ans=mm(ans,a)
    return ans
def inv(a):
    n=len(a);m=[r[:]+s for r,s in zip(a,eye(n))]
    for i in range(n):
        pivot=next(j for j in range(i,n) if m[j][i]);m[i],m[pivot]=m[pivot],m[i]
        d=m[i][i];m[i]=[x/d for x in m[i]]
        for j in range(n):
            if j!=i:
                d=m[j][i];m[j]=[x-d*y for x,y in zip(m[j],m[i])]
    return [r[n:] for r in m]
def pp(a):return [r[:2] for r in a[:2]]
def qq(a):return [r[2:] for r in a[2:]]
def serial(a):return [[str(x) for x in r] for r in a]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    out=parser.parse_args().output;need(not out.exists(),'fresh output required')
    root=Path(__file__).resolve().parents[3]
    contract=root/'research/round22/contracts/q2.json'
    need(sha(contract)=='7b8e7a1dfc4d7d4bb05d7123d26396e0333f48e2bb68f34dfc82703707d0612f','contract changed')
    ledger=root/'research/round19/forward/c1/output/graph-reduction.json'
    old=json.loads(ledger.read_text());old={r['face_id']:r for r in old['affected_faces']+old['constant_faces']}
    vertices=list(product(range(3),range(3),range(2)))
    def move(v,a):return tuple(x+int(i==a) for i,x in enumerate(v))
    edges=[(v,move(v,a)) for a in range(3) for v in vertices if v[a]<(2,2,1)[a]]
    ids={(s,t):e for e,(s,t) in enumerate(edges)}
    faces=[]
    for a,b in combinations(range(3),2):
        for v in vertices:
            if v[a]<(2,2,1)[a] and v[b]<(2,2,1)[b]:
                w=[(ids[v,move(v,a)],1),(ids[move(v,a),move(move(v,a),b)],1),
                   (ids[move(v,b),move(move(v,b),a)],-1),(ids[v,move(v,b)],-1)]
                need([{'edge':e,'sign':s} for e,s in w]==old[len(faces)]['signed_word'],'actual signed face')
                faces.append(w)
    tree=set(range(16))|{26};paths={(0,2,0):[]}
    while len(paths)<18:
        before=len(paths)
        for e in sorted(tree):
            s,t=edges[e]
            if s in paths and t not in paths:paths[t]=paths[s]+[(e,1)]
            if t in paths and s not in paths:paths[s]=paths[t]+[(e,-1)]
        need(len(paths)>before,'tree disconnected')
    s,t=edges[28];uw=paths[s]+[(28,1)]+[(e,-sign) for e,sign in reversed(paths[t])]
    need(uw==[(14,-1),(2,1),(28,1),(3,-1),(15,1),(26,-1)],'actual fixed f1 completion')
    us={e for e,sign in uw};sets=[{e for e,sign in w} for w in faces]
    def connected(edge_set):
        if not edge_set:return False
        vs={v for e in edge_set for v in edges[e]};seen={next(iter(vs))}
        while True:
            before=len(seen)
            for e in edge_set:
                s,t=edges[e]
                if s in seen or t in seen:seen.update((s,t))
            if len(seen)==before:return seen==vs
    groups={k:[] for k in range(4)}
    for p,fs in enumerate(sets):
        if p==8:continue
        common=us&fs;k=len(common);groups[k].append(p)
        if k:
            degrees=Counter(v for e in common for v in edges[e])
            need(connected(common) and sorted(degrees.values()).count(1)==2 and max(degrees.values())<=2,'shared edges must form one path')
            remainder=us^fs;degrees=Counter(v for e in remainder for v in edges[e])
            need(connected(remainder) and all(d==2 for d in degrees.values()),'remaining symmetric difference must be a simple cycle')
    need(groups=={0:[4,5,6,7,11,13,14,18,19],1:[0,1,10,12,16,17],2:[2,3],3:[9,15]},'shared-path census')
    parity_cross=[(p,q) for p in range(20) if p!=8 for q in range(20) if q!=8 and sets[p]==us^sets[q]]
    need(parity_cross==[(9,15),(15,9)],'actual off-diagonal parity pairs')
    adjacency={v:set() for v in vertices}
    for s,t in edges:adjacency[s].add(t);adjacency[t].add(s)
    need(all(v not in adjacency[v] for v in vertices),'no self-loops')
    need(all(not(adjacency[s]&adjacency[t]) for s,t in edges),'no triangles')
    need(all(len(fs)==4 for fs in sets),'four-cycle gap witnesses')
    # 24 equally weighted S3 points integrate quartics exactly: 8 axes+16 half-sign vectors.
    axes=[tuple(F(sign) if i==j else F(0) for i in range(4)) for j in range(4) for sign in [-1,1]]
    sphere=axes+[tuple(F(sign,2) for sign in signs) for signs in product([-1,1],repeat=4)]
    need(all(dot(q,q)==1 for q in sphere),'unit cubature nodes')
    for i in range(4):
        need(sum((q[i]**4 for q in sphere),F(0))/24==F(1,8),'quartic diagonal Haar moment')
        for j in range(i):need(sum((q[i]**2*q[j]**2 for q in sphere),F(0))/24==F(1,24),'quartic mixed Haar moment')
    total=F(0);singlet=F(0);triplet=F(0);orthog=F(0)
    for a,b,g in product(axes,axes,sphere):
        v=2*qm(g,a)[0]*qm(g,b)[0];v0=dot(a,b)/2;v1=v-v0
        total+=v*v;singlet+=v0*v0;triplet+=v1*v1;orthog+=v0*v1
    denom=F(8*8*24);norms=[x/denom for x in [total,singlet,triplet,orthog]]
    need(norms==[F(1,4),F(1,16),F(3,16),F(0)],'shared-path singlet/triplet exact weights')
    weights={F(3):[[F(19,4),F(1,4)],[F(1,4),F(0)]]}
    def add11(e,w):
        if e not in weights:weights[e]=scale(eye(2),0)
        weights[e][1][1]+=w
    add11(F(15,2),F(len(groups[0]),4))
    for k in [1,2,3]:
        e0=F(3,4)*(10-2*k);e1=e0+2*k
        add11(e0,F(len(groups[k]),16));add11(e1,F(3*len(groups[k]),16))
    totalmat=scale(eye(2),0)
    for e,w in weights.items():
        totalmat=add(totalmat,w)
        need(w[0][0]>=0 and w[1][1]>=0 and w[0][0]*w[1][1]>=w[0][1]**2,'positive spectral matrix')
    need(totalmat==[[F(19,4),F(1,4)],[F(1,4),F(19,4)]],'instantaneous Q1 moment matrix')
    need(len(weights)==7 and weights[F(3)][1][1]==F(1,8),'actual nonconstant spectral support')
    H=[[F(x) for x in r] for r in [[4,1,1,1],[1,6,0,2],[1,0,6,1],[1,2,1,7]]]
    A=pp(H);C=qq(H);B=[r[:2] for r in H[2:]];Bt=list(map(list,zip(*B)));z=F(2)
    Sigma=mm(mm(Bt,inv(add(C,scale(eye(2),z)))),B)
    correct=inv(sub(add(A,scale(eye(2),z)),Sigma));full=pp(inv(add(H,scale(eye(4),z))))
    wrong=inv(add(add(A,scale(eye(2),z)),Sigma))
    need(correct==full and wrong!=full,'Schur minus sign')
    c=F(1,3);shifted=add(H,scale(eye(4),c))
    need(pp(inv(add(shifted,scale(eye(4),z))))==pp(inv(add(H,scale(eye(4),z+c)))),'common scalar shifts resolvent energy')
    need(inv(add(A,scale(eye(2),z)))!=full,'omitted memory return control')
    # Volterra double integral has C in the middle and full compressed T on its right.
    degrees=[]
    for n in range(2,6):
        rhs=scale(eye(2),0)
        for a in range(n-1):
            for b in range(n-1-a):
                c=n-2-a-b
                rhs=add(rhs,mm(mm(mm(mm(power(A,a),Bt),power(C,b)),B),pp(power(H,c))))
        need(rhs==sub(pp(power(H,n)),power(A,n)),'Volterra coefficient/order at '+str(n))
        degrees.append(n)
    result={'schema':'ym22-skeptic-preparation-check-v1','loop':'q2','passed':True,
      'current_producers_read':False,'producer_imports':False,'research_loops_added':0,
      'driver_sha256':sha(Path(__file__)),'contract_sha256':sha(contract),'ledger_sha256':sha(ledger),
      'fixed_f1_physical_word':uw,'overlap_groups':groups,'off_diagonal_parity_pairs':parity_cross,
      'shared_path_norms':{'total':'1/4','singlet':'1/16','triplet':'3/16','inner_product':'0'},
      'actual_complement_gap_over_alpha':'3, analytic gauge-support argument plus W0 witness',
      'spectral_weights':[{'energy_over_alpha':str(e),'matrix':serial(w)} for e,w in sorted(weights.items())],
      'instantaneous_matrix':serial(totalmat),'Schur_sign_control':{'correct':serial(correct),'wrong_plus':serial(wrong)},
      'scalar_energy_shift_checked':True,'memory_omission_rejected':True,'Volterra_degrees_checked':degrees,
      'kernel_remainder':'250 alpha^3 lambda^3 (s/hbar) exp(-3alpha s/hbar)',
      'self_energy_remainder':'250 alpha^3 lambda^3/(3alpha+z)^2',
      'topology_scope':'Finite exact checks accompany analytic domains/gap and full-Hilbert norm bounds; no cutoff or channel closure claim'}
    out.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'loop':'q2','prepared':True,'spectral_energies':len(weights)}))
if __name__=='__main__':main()
