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
def sqrt_upper(x,digits=40):
    require(x>=0,'nonnegative square root');D=10**digits;n=math.isqrt(x.numerator*D*D//x.denominator);r=F(n,D);return r if r*r==x else F(n+1,D)
def matvec(entries,v):
    out=[0]*293
    for i,j,c in entries:out[i]+=c*v[j]
    return out
def export_vector(v):return [nearest(x,10**30) for x in v]
def polynomial_action(time,inp,center,basis,S,degree=240):
    if time==0:return list(inp)
    qin=math.lcm(*(x.denominator for x in inp));xnum=[int(x*qin) for x in inp]
    D=10**24;require((center*D).denominator==1,'integer ground center');center_n=int(center*D)
    entries=[]
    for i,b in enumerate(basis):
        value=F(b['energy'])+F(1,5);require((value*D).denominator==1,'integer A diagonal');entries.append((i,i,time.numerator*(center_n-int(value*D))))
    for (i,j),value in S.items():
        c=value*D/100;require(c.denominator==1,'integer offdiagonal');entries.append((i,j,time.numerator*int(c)))
    DD=D*time.denominator;num=xnum[:];den=1
    for k in range(degree,0,-1):
        prod=matvec(entries,num);den*=DD*k;num=[xnum[i]*den+prod[i] for i in range(293)]
    grid=10**30;totalden=qin*den
    # Round exact rational Horner outputs without constructing 293 huge Fractions.
    return [F((2*n*grid+totalden)//(2*totalden),grid) for n in num]
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);p.add_argument('--sigma');p.add_argument('--input-vector');a=p.parse_args();out=Path(a.output).resolve();require(not out.exists(),'fresh output required')
    con=json.loads((ROOT/'research/round26/contracts/af2.json').read_text())
    for rel,h in con['bindings'].items():require(hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==h,'binding '+rel)
    basis,S=construct();old=json.loads((ROOT/'research/round26/forward/ac1/output/results.json').read_text())
    for i,b in enumerate(basis):
        if b['label'].startswith('pair_') and old['basis'][i]['label'].startswith('disjoint_'):b['label']=b['label'].replace('pair_','disjoint_',1)
    require(basis==old['basis'] and [[i,j,str(v)] for (i,j),v in sorted(S.items())]==old['magnetic_sparse_entries'],'independent complete retained matrix')
    weights=[int(F(b['norm2'])) for b in basis];require(sum(weights)==417,'actual metric weight')
    require(all(weights[i]*v==weights[j]*S[j,i] for (i,j),v in S.items()),'metric self-adjointness')
    # Integer power filtering with matrix 3600*(I-A/9).
    power_entries=[];A_entries=[]
    for i,b in enumerate(basis):
        av=F(b['energy'])+F(1,5);power_entries.append((i,i,int(3600*(1-av/9))));A_entries.append((i,i,int(400*av)))
    for (i,j),v in S.items():power_entries.append((i,j,int(4*v)));A_entries.append((i,j,int(-4*v)))
    n=[1]+[0]*292
    for _ in range(64):n=matvec(power_entries,n)
    norm=sum(weights[i]*n[i]*n[i] for i in range(293));an=matvec(A_entries,n);av=F(sum(weights[i]*n[i]*an[i] for i in range(293)),400*norm)
    r2=F(sum(weights[i]*an[i]*an[i] for i in range(293)),400**2*norm)-av*av
    require(r2>=0 and 0<av<F(1,5),'isolated ground Rayleigh')
    mu_lo=av-r2/(3-av);mu_hi=av;proj=sqrt_upper(r2/(3-av)**2);center=nearest((mu_lo+mu_hi)/2,10**24);u=max(abs(center-mu_lo),abs(center-mu_hi))
    require(0<mu_lo<=mu_hi<F(1,5) and u<F(1,10**20),'certified minimum and fine center')
    require(2*F(15,22)**64<F(1,10**10) and proj<F(1,10**10),'actual ground projection bound')
    rounderr=F(11,10**30);poly=16*F(72)**241/math.factorial(241);early=poly+8*u/(1-8*u)+rounderr
    require(sum(F(112,5)**j/math.factorial(j) for j in range(100))>10**9,'whole late time tail')
    late=proj+F(1,10**9)+rounderr;numerical=max(early,late);require(numerical<F(1,10**8),'uniform all-time numerical allowance')
    physical=F(457097,12600000000);denom=F(7127,7200);relative=(physical+numerical)/denom;require(relative<F(37,10**6),'full actual all-time relative certificate')
    vacuum=[F(1)]+[F(0)]*292;prepared=[F(159999,160001),F(800,160001)]+[F(0)]*291
    require(sum(weights[i]*prepared[i]**2 for i in range(293))==1,'nonvacuum exactly normalized')
    dist2=sum(weights[i]*(prepared[i]-vacuum[i])**2 for i in range(293));require(dist2==F(4,160001) and dist2<F(1,10000),'same original preparation ball')
    def projector_action(x):
        coeff=sum(F(weights[i]*n[i])*x[i] for i in range(293))/norm
        return export_vector([coeff*v for v in n])
    records=[];joins={}
    for name,x in [('vacuum',vacuum),('prepared_face',prepared)]:
        for t in [F(0),F(1),F(13,5),F(8),F(9),F(10**6)]:
            branch='early' if t<=8 else 'late';v=polynomial_action(t,x,center,basis,S) if branch=='early' else projector_action(x)
            if t==0:require(v==x,'zero-time return exact')
            if t==8:
                w=projector_action(x);difference2=sum(weights[i]*(v[i]-w[i])**2 for i in range(293));require(difference2<=(early+late)**2,'certified branch boundary agreement');joins[name]=str(difference2)
            records.append({'input':name,'sigma':str(t),'branch':branch,'coordinates':[str(y) for y in v],'display_only_vacuum_coordinate':float(v[0])})
    if a.sigma is not None:
        t=F(a.sigma);require(t>=0,'requested time must be nonnegative');x=vacuum
        if a.input_vector:
            raw=json.loads(Path(a.input_vector).read_text());require(type(raw)==list and len(raw)==293 and all(type(v)==str for v in raw),'293 exact rational coordinate strings required');x=[F(v) for v in raw]
        require(all(v==0 for v in x[21:]),'original P21 input required')
        require(sum(weights[i]*x[i]**2 for i in range(293))==1,'exactly normalized rational input required')
        require(sum(weights[i]*(x[i]-vacuum[i])**2 for i in range(293))<=F(1,10000),'original radius .01 preparation required')
        branch='early' if t<=8 else 'late';v=polynomial_action(t,x,center,basis,S) if branch=='early' else projector_action(x)
        records.append({'input':'requested_exact_rational','sigma':str(t),'branch':branch,'coordinates':[str(y) for y in v],'display_only_vacuum_coordinate':float(v[0])})
    else:require(a.input_vector is None,'input-vector requires sigma')
    require(apply_L(F(0),vacuum,basis,S)==[F(0)]*293,'zero coupling vacuum eigenvector control')
    triplet=next(i for i,w in enumerate(weights) if w==3);require(weights[triplet]!=1,'wrong Euclidean norm rejected')
    paths=list(con['bindings'])+['research/round26/contracts/af2.json','research/round26/contracts/af2-freeze.json','research/round26/reverse/af2/report.md','research/round26/reverse/af2/check.py','.codex/skills/qeg-research-advisor/references/newton-tesla-project-method.md']
    data={'schema':'ym26-reverse-result-v1','loop':'af2','status':'accepted-all-time-piecewise-evaluator','checks_passed':True,'lambda':'1/100','early_join':'8','early_degree':240,'basis_labels':[b['label'] for b in basis],'gram_weights':weights,'ground_projector':{'integer_vector':[str(v) for v in n],'metric_norm_squared':str(norm),'rayleigh':str(av),'residual_squared':str(r2),'minimum_interval':[str(mu_lo),str(mu_hi)],'projector_error_bound':str(proj),'chosen_center':str(center),'center_uncertainty':str(u)},'uniform_budgets':{k:str(v) for k,v in {'polynomial_remainder':poly,'early_center':8*u/(1-8*u),'export_metric_error':rounderr,'early_total':early,'late_projector':proj,'late_excited_tail':F(1,10**9),'late_total':late,'numerical_maximum':numerical,'physical_absolute':physical,'true_denominator_floor':denom,'full_relative':relative}.items()},'prepared_input':{'coordinates':[str(v) for v in prepared],'squared_distance_from_vacuum':str(dist2)},'branch_join_squared_differences':joins,'evaluations':records,'source_inventory':{r:hashlib.sha256((ROOT/r).read_bytes()).hexdigest() for r in sorted(set(paths))}}
    out.mkdir(parents=True);(out/'results.json').write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
if __name__=='__main__':main()
