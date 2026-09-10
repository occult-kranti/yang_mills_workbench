"""Floating tensor quadrature: an auxiliary comparison, never an exact certificate."""
from pathlib import Path
from fractions import Fraction as F
import argparse,csv,hashlib,itertools,json,math,sys
import numpy as np
HERE=Path(__file__).resolve().parent
NODES=(8,12,16);KAPPAS=(F(-1,64),F(0),F(1,64));COEFFICIENTS=(0,1,2)
TOL=5e-15

def grid(n):
    if type(n) is not int or n not in NODES:raise ValueError('Use a frozen quadrature refinement')
    theta=np.pi*np.arange(1,n+1)/(n+1)
    x=np.cos(theta);sx=np.sin(theta);wx=2*sx*sx/(n+1)
    z,wz=np.polynomial.legendre.leggauss(n);wz=wz/2
    X=x[:,None,None];Y=x[None,:,None]
    W=X*Y+sx[:,None,None]*sx[None,:,None]*z[None,None,:]
    WP=X*Y-sx[:,None,None]*sx[None,:,None]*z[None,None,:]
    weights=wx[:,None,None]*wx[None,:,None]*wz[None,None,:]
    return X,Y,W,WP,weights,x,wx

def integral(n,kappa,d):
    if type(kappa) is not F or kappa not in KAPPAS or type(d) is not int or d not in COEFFICIENTS:raise ValueError('Use a frozen signed coefficient fixture')
    X,Y,W,WP,weights,_,_=grid(n)
    def evaluate(w):
        observable=(4*X*X-1)**3*(4*w*w-1)/81
        weighted=weights*np.exp(float(kappa)*(3*X+d*Y+w))
        numerator=float(np.sum(weighted*observable));partition=float(np.sum(weighted))
        if not math.isfinite(numerator) or not math.isfinite(partition) or partition<=0:raise ValueError('Invalid floating numerator/partition')
        return numerator,partition,numerator/partition
    result=evaluate(W);conjugate=evaluate(WP)
    return {'numerator':result[0],'partition':result[1],'ratio':result[2],'consistent_plus_word_ratio':conjugate[2]}

def exact_intervals():
    source=HERE/'forward/c2/output/completecollection.json';data=json.loads(source.read_bytes())
    if data.get('schema')!='ym18-c2-collection-v1' or type(data.get('fixtures')) is not list:raise ValueError('Wrong exact collection schema')
    result={}
    for fixture in data['fixtures']:
        c=fixture['certificate'];k=F(c['kappa']);d=c['V_only_coefficient'];v=c['expectation_interval'];lo,hi=F(v['lower']),F(v['upper'])
        if type(d) is not int or c['degree']!=8 or c['target_width']!='1/1000000000000' or hi<lo or F(v['width'])!=hi-lo or hi-lo>F(1,10**12) or c['status']!='target-met':raise ValueError('Incomplete exact comparison fixture')
        if (k,d) in result:raise ValueError('Duplicate exact fixture')
        result[k,d]=(lo,hi)
    return result,source

def main(output):
    sys.path.insert(0,str(HERE/'advisor'));from freeze_gate import verify
    verify(HERE/'advisor/c2-gate.json')
    if NODES!=(8,12,16) or KAPPAS!=(F(-1,64),F(0),F(1,64)) or COEFFICIENTS!=(0,1,2) or type(TOL) is not float or TOL!=5e-15:raise ValueError('Changed auxiliary experiment contract')
    out=Path(output).resolve()
    if out.exists() or out==HERE or out in HERE.parents or any(HERE/role in out.parents for role in ('forward','backward')):raise ValueError('Use a new output directory')
    exact,source=exact_intervals();expected=set(itertools.product(KAPPAS,COEFFICIENTS))
    if set(exact)!=expected:raise ValueError('Missing exact signed/action fixtures')
    checks=[];rows=[]
    def check(name,condition):
        if not condition:raise ValueError(name)
        checks.append({'name':name,'passed':True})
    for n in NODES:
        X,Y,W,WP,weight,x,wx=grid(n)
        check(f'{n}: normalized induced angular measure',abs(float(np.sum(weight))-1)<=TOL)
        check(f'{n}: correlated first mixed moment',abs(float(np.sum(weight*X*Y*W))-1/16)<=TOL)
        check(f'{n}: repeated mixed moment',abs(float(np.sum(weight*X**2*Y**2*W**2))-1/48)<=TOL)
        check(f'{n}: separate frozen-V zero-action result',abs(float(np.sum(wx*(4*x*x-1)**4/81))-1/27)<=TOL)
        for k,d in itertools.product(KAPPAS,COEFFICIENTS):
            v=integral(n,k,d);lo,hi=exact[k,d]
            # Floats test arithmetic implementation at their own rounding scale.
            # This allowance neither widens nor proves the exact rational interval.
            distance=max(float(lo)-v['ratio'],v['ratio']-float(hi),0.0)
            convention=abs(v['ratio']-v['consistent_plus_word_ratio'])
            check(f'{n}: kappa={k}, V-only coefficient={d}',distance<=TOL and convention<=TOL and all(math.isfinite(q) for q in v.values()))
            rows.append({'nodes_per_variable':n,'kappa':str(k),'v_only_coefficient':d,**v,'exact_lower':str(lo),'exact_upper':str(hi),'distance_to_exact_interval':distance,'consistent_word_difference':convention})
    out.mkdir(parents=True)
    with (out/'quadrature.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    report={'status':'passed','checks_count':len(checks),'checks':checks,'rows':rows,'absolute_floating_tolerance':TOL,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'exact_collection_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'scope':'Independent floating Gauss-Chebyshev/Gauss-Legendre angular quadrature at8,12,16 nodes. It checks the implementation and a Haar substitution; it does not alter or prove the exact rational tail certificate.'}
    (out/'results.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n');print(json.dumps({'status':'passed','checks_count':len(checks),'quadrature_comparisons':len(rows)}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',required=True);main(p.parse_args().output)
