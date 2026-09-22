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
def nearest(x,D):return F((2*x.numerator*D+x.denominator)//(2*x.denominator),D)
def fixed_decimal(x,digits=30):
    D=10**digits;require((x*D).denominator==1,'exact export grid');n=int(x*D);sign='-' if n<0 else '';n=abs(n);return sign+str(n//D)+'.'+str(n%D).zfill(digits)
def heat_polynomial(lam,center,time,basis,S,degree=80):
    n=len(basis);vec=[F(1)]+[F(0)]*(n-1);total=list(vec)
    if time==0:return total
    for j in range(1,degree+1):
        av=apply_L(lam,vec,basis,S);vec=[-time*(av[i]-center*vec[i])/j for i in range(n)];total=[total[i]+vec[i] for i in range(n)]
    return total
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);a=p.parse_args();out=Path(a.output).resolve();require(not out.exists(),'fresh output required')
    con=json.loads((ROOT/'research/round26/contracts/af1.json').read_text())
    for rel,h in con['bindings'].items():require(hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h,'binding '+rel)
    basis,S=construct();old=json.loads((ROOT/'research/round26/forward/ac1/output/results.json').read_text())
    for i,b in enumerate(basis):
        if b['label'].startswith('pair_') and old['basis'][i]['label'].startswith('disjoint_'):b['label']=b['label'].replace('pair_','disjoint_',1)
    require(basis==old['basis'],'actual basis');require([[i,j,str(v)] for (i,j),v in sorted(S.items())]==old['magnetic_sparse_entries'],'all sparse metric entries')
    weights=[F(b['norm2']) for b in basis];require(sum(weights)==417,'full export metric')
    require(all(weights[i]*v==weights[j]*S[j,i] for (i,j),v in S.items()),'metric self-adjointness')
    lam=F(1,100);rad=9+20*lam*lam;den=10**30;n=math.isqrt(rad.numerator*den*den//rad.denominator);lo=F(n,den);hi=F(n+1,den);require(lo*lo<=rad<=hi*hi,'integer radical certificate')
    mlo=20*lam-(hi-3)/2;mhi=20*lam-(lo-3)/2;d21=F(7,30000)**2/F(14,5);mu_lo=mlo-d21;mu_hi=mhi;center=nearest((mu_lo+mu_hi)/2,10**12);u=max(abs(center-mu_lo),abs(center-mu_hi))
    require(0<mu_lo<mu_hi<F(1,5) and mu_hi-mu_lo<F(2,10**8) and u<F(1,10**8),'actual minimum enclosure and center uncertainty')
    exact=heat_polynomial(lam,center,F(1),basis,S);export=[nearest(v,10**30) for v in exact]
    err2=sum(weights[i]*(exact[i]-export[i])**2 for i in range(293));export_bound=F(11,10**30);require(err2<export_bound**2,'full metric export error')
    polynomial_bound=2*F(9)**81/math.factorial(81);center_bound=u/(1-u)
    require(sum(F(3)**j/math.factorial(j) for j in range(20))>20,'exp3 rational bound')
    physical=F(1,10080000000)+F(130,9)*lam*lam*(4*lam/3)*F(41,60);true_den=F(7199,7200);total=physical+center_bound+polynomial_bound+export_bound;relative=total/true_den
    require(relative<F(14,10**6),'complete full-space point certificate')
    vacuum=[F(1)]+[F(0)]*292;require(heat_polynomial(lam,center,F(0),basis,S)==vacuum,'zero time exact')
    require(heat_polynomial(F(0),F(0),F(1),basis,S)==vacuum,'zero coupling exact')
    triplet=next(i for i,b in enumerate(basis) if b['norm2']=='3');require(weights[triplet]!=1,'wrong Euclidean norm rejected')
    paths=list(con['bindings'])+['research/round26/contracts/af1.json','research/round26/contracts/af1-freeze.json','research/round26/reverse/af1/report.md','research/round26/reverse/af1/check.py','.codex/skills/qeg-research-advisor/references/newton-tesla-project-method.md']
    data={'schema':'ym26-reverse-result-v1','loop':'af1','status':'accepted-certified-heat-point','checks_passed':True,'lambda':str(lam),'sigma':'1','input':'vacuum','retained_minimum_enclosure':[str(mu_lo),str(mu_hi)],'chosen_ground_center':str(center),'center_uncertainty':str(u),'coordinate_convention':'AC1 rational basis, triplet squared norm3; decimal strings are exact','coordinates':[{'label':b['label'],'norm2':b['norm2'],'value':fixed_decimal(export[i])} for i,b in enumerate(basis)],'certified_errors':{k:str(v) for k,v in {'physical_full_space':physical,'ground_center':center_bound,'degree80_remainder':polynomial_bound,'coordinate_export':export_bound,'absolute_total':total,'true_denominator_floor':true_den,'relative_total':relative}.items()},'display_only':{'vacuum_coefficient':float(export[0]),'first_face_coefficient':float(export[1]),'relative_bound':float(relative),'minimum_enclosure':[float(mu_lo),float(mu_hi)]},'source_inventory':{r:hashlib.sha256((ROOT/r).read_bytes()).hexdigest() for r in sorted(set(paths))}}
    out.mkdir(parents=True);(out/'results.json').write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
if __name__=='__main__':main()
