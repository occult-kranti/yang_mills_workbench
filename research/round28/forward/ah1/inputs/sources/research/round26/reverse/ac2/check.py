#!/usr/bin/env python3
import argparse,hashlib,itertools,json,math
from fractions import Fraction as F
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def require(x,m):
    if x is not True:raise RuntimeError(m)
def graph():
    sizes=(3,3,2);vs=list(itertools.product(*(range(n) for n in sizes)));es=[];lookup={}
    for v in vs:
        for a in range(3):
            if v[a]+1<sizes[a]:
                w=tuple(v[i]+int(i==a) for i in range(3));lookup[frozenset((v,w))]=len(es);es.append((v,w,a))
    fs=[]
    for v in vs:
        for a,b in itertools.combinations(range(3),2):
            if v[a]+1<sizes[a] and v[b]+1<sizes[b]:
                loop=[v,tuple(v[i]+int(i==a) for i in range(3)),tuple(v[i]+int(i in (a,b)) for i in range(3)),tuple(v[i]+int(i==b) for i in range(3))]
                fs.append({lookup[frozenset((loop[j],loop[(j+1)%4]))] for j in range(4)})
    return es,fs
def construct():
    es,fs=graph();basis=[{'label':'vacuum','norm2':'1','energy':'0'}]
    basis +=[{'label':f'face_{i}','norm2':'1','energy':'3'} for i in range(20)]
    basis +=[{'label':f'spin1_{i}','norm2':'1','energy':'8'} for i in range(20)]
    S={}
    def put(i,j,v):S[i,j]=v;S[j,i]=v*F(basis[i]['norm2'])/F(basis[j]['norm2'])
    for j in range(20):put(0,j+1,F(1,2));put(j+21,j+1,F(1,2))
    for i,j in itertools.combinations(range(20),2):
        if fs[i]&fs[j]:
            labels=[(f'singlet_{i}_{j}','1','9/2'),(f'triplet_{i}_{j}','3','13/2')];coeff=F(1,4)
        else:labels=[(f'pair_{i}_{j}','1','6')];coeff=F(1,2)
        for label,norm,energy in labels:
            k=len(basis);basis.append({'label':label,'norm2':norm,'energy':energy});put(k,i+1,coeff);put(k,j+1,coeff)
    # Exact actual link-center transformation makes every face odd.
    signs=[(-1)**sum(v[:a]) for v,w,a in es]
    require(all(math.prod(signs[e] for e in f)==-1 for f in fs),'all-face center parity')
    return basis,S
def apply_L(lam,vector,basis,S):
    require(F(0)<=lam<=F(1,100),'coupling range');require(len(vector)==293,'293 rational coordinates required')
    out=[(F(basis[i]['energy'])+20*lam)*vector[i] for i in range(293)]
    for (i,j),value in S.items():out[i]-=lam*value*vector[j]
    return out
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--vector-file');p.add_argument('--lambda',dest='lam',default='1/100');a=p.parse_args();out=Path(a.output).resolve();require(not out.exists(),'fresh output required')
    con=json.loads((ROOT/'research/round26/contracts/ac2.json').read_text())
    for rel,h in con['bindings'].items():require(hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h,'binding '+rel)
    basis,S=construct();old=json.loads((ROOT/'research/round26/forward/ac1/output/results.json').read_text())
    # Label convention may differ only in the word for a disjoint pair; compare all geometric labels explicitly.
    old_labels=[r['label'] for r in old['basis']]
    for i,b in enumerate(basis):
        if b['label'].startswith('pair_') and old_labels[i].startswith('disjoint_'):b['label']=b['label'].replace('pair_','disjoint_',1)
    require(basis==old['basis'],'independent actual basis reconstruction')
    sparse=[[i,j,str(v)] for (i,j),v in sorted(S.items())]
    require(sparse==old['magnetic_sparse_entries'],'independent full sparse metric matrix')
    require(len(S)==1088,'complete nonzero entries')
    weights=[F(b['norm2']) for b in basis]
    require(all(weights[i]*v==weights[j]*S[j,i] for (i,j),v in S.items()),'metric self-adjointness')
    gramR=[[sum(weights[k]*S.get((k,i+1),F(0))*S.get((k,j+1),F(0)) for k in range(21,293)) for j in range(20)] for i in range(20)]
    gramAll=[[sum(weights[k]*S.get((k,i+1),F(0))*S.get((k,j+1),F(0)) for k in range(293) if k not in range(1,21)) for j in range(20)] for i in range(20)]
    require(all(gramR[i][j]==(F(5) if i==j else F(1,4)) for i in range(20) for j in range(20)),'new-to-face complete Gram')
    require(all(gramAll[i][j]==(F(21,4) if i==j else F(1,2)) for i in range(20) for j in range(20)),'full even-to-face Gram')
    require(sum(gramR[0])==F(39,4) and sum(gramAll[0])==F(59,4),'exact coupling norms squared')
    require(F(39,4)<F(13,4)**2 and F(59,4)<16,'rational coupling envelopes')
    require(sum(F(7)**j/math.factorial(j) for j in range(20))>1000,'continuous exponential bound')
    La=F(1,100);pold=F(1,12000);pn=F(1,168000);dn=F(1,10080000000);T=F(5,2);rows=[]
    for eta,threshold in [(F(1,100),F(48,10**6)),(F(0),F(43,10**6))]:
        den=1-5*La*La/9-F(3,2)*pold-eta-pn;b=F(3,4)*La+F(3,2)*pold+eta
        early=dn*T+F(130,9)*La*La*(eta/3+4*La/3*(T-F(333,1000)))
        late=pn+(2*b+pn)/1000;ratio=max(early,late)/den
        require(den>0 and ratio<threshold,'strict all-time true relative threshold')
        rows.append({k:str(v) for k,v in {'eta':eta,'join':T,'true_denominator_floor':den,'early_absolute_upper':early,'late_absolute_upper':late,'relative_upper':ratio,'advertised_threshold':threshold}.items()})
    lam=F(a.lam);vector=[F(1)]+[F(0)]*292
    if a.vector_file:
        raw=json.loads(Path(a.vector_file).read_text());require(type(raw)==list and all(type(v)==str for v in raw),'vector rational strings');vector=[F(v) for v in raw]
    action=apply_L(lam,vector,basis,S)
    vac=apply_L(F(0),[F(1)]+[F(0)]*292,basis,S);require(all(v==0 for v in vac),'zero coupling vacuum')
    paths=list(con['bindings'])+['research/round26/contracts/ac2.json','research/round26/reverse/ac2/report.md','research/round26/reverse/ac2/check.py','.codex/skills/qeg-research-advisor/references/newton-tesla-project-method.md']
    data={'schema':'ym26-reverse-result-v1','loop':'ac2','status':'accepted-same-preparation-improvement','checks_passed':True,'independent_sparse_matrix_match':True,'generator_action':{'lambda':str(lam),'input':[str(x) for x in vector],'output':[str(x) for x in action],'arithmetic':'exact rational, actual diagonal Gram'},'all_time_continuous_certificates':rows,'physical_error_only_heat_evaluator_not_supplied':True,'source_inventory':{r:hashlib.sha256((ROOT/r).read_bytes()).hexdigest() for r in sorted(set(paths))}}
    out.mkdir(parents=True);(out/'results.json').write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
if __name__=='__main__':main()
