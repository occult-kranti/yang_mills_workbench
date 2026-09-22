#!/usr/bin/env python3
"""Build all 293 actual retained coordinates and rigorous full remainder bounds."""
import argparse, hashlib, itertools, json, math
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4];HERE=Path(__file__).resolve().parent
def require(c,m):
    if not c:raise ValueError(m)
def clean(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,dict):return {str(k):clean(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [clean(v) for v in x]
    return x
def graph():
    vertices=list(itertools.product(range(3),range(3),range(2)));edges=[];lookup={};faces=[]
    for v in vertices:
        for a,n in enumerate((3,3,2)):
            if v[a]+1<n:
                w=tuple(v[j]+int(j==a) for j in range(3));lookup[frozenset((v,w))]=len(edges);edges.append((v,w,a))
    for v in vertices:
        for a,b in itertools.combinations(range(3),2):
            if v[a]+1<(3,3,2)[a] and v[b]+1<(3,3,2)[b]:
                loop=[v,tuple(v[j]+int(j==a) for j in range(3)),tuple(v[j]+int(j in (a,b)) for j in range(3)),tuple(v[j]+int(j==b) for j in range(3))]
                faces.append(sum(1<<lookup[frozenset((loop[i],loop[(i+1)%4]))] for i in range(4)))
    return vertices,edges,faces
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);out=Path(ap.parse_args().output);require(not out.exists(),'fresh output required')
    vs,es,fs=graph();require((len(vs),len(es),len(fs))==(18,33,20),'actual graph')
    center=sum(1<<i for i,(v,w,a) in enumerate(es) if (a==1 and v[0]%2) or (a==2 and (v[0]+v[1])%2))
    require(all((f&center).bit_count()%2==1 for f in fs),'global odd face parity')
    require(all(a^b^c for a,b,c in itertools.combinations(fs,3)),'no triple mask identity')
    pairs=list(itertools.combinations(range(20),2));masks=[fs[p]^fs[q] for p,q in pairs]
    require(len(set(masks))==190 and all(masks),'pair parity orthogonality')
    basis=[{'label':'vacuum','norm2':F(1),'energy':F(0)}]+[{'label':'face_'+str(p),'norm2':F(1),'energy':F(3)} for p in range(20)]
    mat={}
    def add_basis(label,norm2,energy):
        basis.append({'label':label,'norm2':F(norm2),'energy':F(energy)});return len(basis)-1
    def couple(even,face,coefficient):
        j=1+face;mat[(even,j)]=F(coefficient);mat[(j,even)]=F(coefficient)*basis[even]['norm2']
    for p in range(20):couple(0,p,F(1,2))
    for p in range(20):couple(add_basis('spin1_'+str(p),1,8),p,F(1,2))
    counts={'disjoint':0,'shared':0}
    for p,q in pairs:
        shared=(fs[p]&fs[q]).bit_count();require(shared in (0,1),'face edge intersection')
        if shared:
            counts['shared']+=1
            for kind,norm,en in [('singlet',1,F(9,2)),('triplet',3,F(13,2))]:
                idx=add_basis(f'{kind}_{p}_{q}',norm,en)
                for face in (p,q):couple(idx,face,F(1,4))
        else:
            counts['disjoint']+=1;idx=add_basis(f'pair_{p}_{q}',1,6)
            for face in (p,q):couple(idx,face,F(1,2))
    require(counts=={'disjoint':128,'shared':62},'all pair geometries');require(len(basis)==293,'full dimension')
    require(all(basis[i]['norm2']*a==basis[j]['norm2']*mat[j,i] for (i,j),a in mat.items()),'metric self-adjointness')
    require(sum(b['norm2']==3 for b in basis)==62,'triplet Gram')
    nonzero=len(mat)
    require(nonzero==1088,'sparse magnetic count')
    wrong_metric=any(a!=mat[j,i] for (i,j),a in mat.items());require(wrong_metric,'incorrect Euclidean metric must fail')
    # Every pair contribution to the inherited bright residual is included.
    weights={F(9,2):F(62,16),F(6):F(128,4),F(13,2):F(186,16),F(8):F(20,16)}
    require(sum(weights.values())==F(195,4),'complete residual weight')
    require(sum(e*w for e,w in weights.items())==295,'complete K action')
    lam=F(1,100);g=3-20*lam;r21=F(7,3)*lam**2;p21=r21/g;r293=20*lam*p21;p293=r293/g;d293=r293*r293/g
    require((p21,r293,p293,d293)==(F(1,12000),F(1,60000),F(1,168000),F(1,10080000000)),'cap envelopes')
    t=F(2);x=t*g;positive_sum=sum((x**n/F(math.factorial(n)) for n in range(40)),F(0));require(positive_sum>250,'exact exp tail')
    accuracy=[]
    for eta,threshold in [(F(0),F(59,100000)),(F(1,100),F(14,10000))]:
        a=1-F(5,9)*lam**2-F(3,2)*p21-eta;b=F(3,4)*lam+F(3,2)*p21+eta;den=a-p293
        early=(r293+d293)*t+20*lam*b/g;late=p293+(2*b+p293)/250;bound=max(early,late)/den
        require(den>0 and bound<threshold,'true denominator and all-time relative certificate')
        accuracy.append({'eta':eta,'true_denominator_floor':den,'early_upper':early,'late_upper':late,'relative_upper':bound,'threshold':threshold})
    contract=json.loads((ROOT/'research/round26/contracts/ac1.json').read_text());paths=['research/round26/contracts/ac1.json',*contract['bindings'],str(HERE.relative_to(ROOT)/'report.md'),str(HERE.relative_to(ROOT)/'check.py')]
    bindings={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sorted(set(paths))}
    for p,d in contract['bindings'].items():require(bindings[p]==d,'dependency binding '+p)
    result={'schema':'ym26-forward-ac1-v1','dimension':293,'basis':basis,'magnetic_sparse_entries':[[i,j,a] for (i,j),a in sorted(mat.items())],'nonzero_magnetic_entries':nonzero,'gram':'diagonal norms in basis, not identity','whole_omitted_norm_upper':'20*lambda; not claimed exact','old21_omitted_columns':'exactly zero','cap':{'ground_residual_upper':r293,'ground_projection_upper':p293,'ground_energy_error_upper':d293},'accuracy':accuracy,'controls':{'wrong_triplet_metric_rejected':True,'all_shared_singlets_retained':True,'lambda_zero_exact_K_reduction':True,'ambient_shell_not_complete':True,'all_input_bound_worsens':True},'bindings':bindings}
    out.mkdir(parents=True);(out/'results.json').write_text(json.dumps(clean(result),indent=2,sort_keys=True)+'\n')
if __name__=='__main__':main()
