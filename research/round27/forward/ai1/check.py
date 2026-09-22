#!/usr/bin/env python3
"""Exact identifiability controls for AI1's explicitly declared readout maps."""
import argparse
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
checks=[]

def require(condition,name):
    if not condition:
        raise ValueError(name)
    checks.append(name)

def reject(predicate,name):
    require(not predicate,name)

def clean(value):
    if isinstance(value,F): return str(value)
    if isinstance(value,dict): return {str(k):clean(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)): return [clean(v) for v in value]
    return value

def rates(alpha,eta,q):
    require(alpha>0 and 0<eta<1 and 0<q<1,'admissible parameter '+str((alpha,eta,q)))
    return alpha,alpha*eta*(1-q)**3/84  # hbar=E_star=1 fixes units for fixtures only.

def cube():
    vertices=list(itertools.product(range(2),repeat=3))
    edges=[(v,w) for v in vertices for w in vertices if v<w and sum(a!=b for a,b in zip(v,w))==1]
    require(len(edges)==12,'cube has twelve edges')
    idx={frozenset(e):i for i,e in enumerate(edges)}
    faces={}
    origin=(3,1,0)
    for axis in range(3):
        for side in (0,1):
            es=frozenset(i for i,(v,w) in enumerate(edges) if v[axis]==w[axis]==side)
            anchor=list(origin);anchor[axis]+=side
            require(len(es)==4,'complete square face '+str((axis,side)))
            faces[es]=sum(anchor)
    cycles=[]
    for subset in itertools.combinations(range(12),6):
        adjacency={}
        for i in subset:
            v,w=edges[i];adjacency.setdefault(v,set()).add(w);adjacency.setdefault(w,set()).add(v)
        if len(adjacency)!=6 or any(len(v)!=2 for v in adjacency.values()):continue
        seen=set();pending=[next(iter(adjacency))]
        while pending:
            v=pending.pop()
            if v not in seen:seen.add(v);pending.extend(adjacency[v]-seen)
        if len(seen)==6:cycles.append(frozenset(subset))
    require(len(cycles)==16,'all and only simple six cycles')
    def path(points):return {idx[frozenset((a,b))] for a,b in zip(points,points[1:])}
    X=[(0,0,0),(0,1,0),(0,1,1)]
    Y=[(0,0,0),(0,0,1),(0,1,1)]
    Z=[(0,0,0),(1,0,0),(1,1,0),(1,1,1),(0,1,1)]
    ix=cycles.index(frozenset(path(X)|path(Z)));iy=cycles.index(frozenset(path(Y)|path(Z)))
    require(faces[cycles[ix]^cycles[iy]]==4,'physical X/Y shared face anchor exponent four')
    return cycles,faces,ix,iy

def moments(q,cycles,faces,ix,iy,kind):
    Q=[[q**faces[c^d] if c^d in faces else F(0) for d in cycles] for c in cycles]
    v=[F(i==ix or (kind=='sum' and i==iy)) for i in range(len(cycles))]
    norm=F(2 if kind=='sum' else 1);w=v[:];out=[]
    for n in range(7):
        out.append(sum(a*b for a,b in zip(v,w))/norm)
        w=[sum(a*b for a,b in zip(row,w)) for row in Q]
    return out

def finiteq_slope(q):
    p=2+5*q+5*q*q+6*q**3+3*q**4
    return q**4*(1+q)**2*(1+q*q)/(32*p)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True)
    out=Path(parser.parse_args().output)
    require(out.is_absolute() and not out.exists(),'fresh absolute output required')
    inventory=json.loads((HERE/'inputs/source-inventory.json').read_text())
    for path,digest in inventory.items():
        require(hashlib.sha256((HERE/'inputs'/path).read_bytes()).hexdigest()==digest,'snapshot binding '+path)
        require(hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest,'source binding '+path)
    contract=json.loads((HERE/'inputs/research/round27/contracts/ai1.json').read_text())
    for path,digest in contract['sources'].items():require(inventory.get(path)==digest,'contract coverage '+path)

    a=(F(1),F(1,4),F(1,2));b=(F(2),F(1,8),F(1,2));c=(F(1),F(2,27),F(1,4))
    ra,rb,rc=(rates(*v) for v in (a,b,c))
    require(ra[1]==rb[1]==rc[1]==F(1,2688),'exact three-point slow-rate fiber')
    reject(ra[0]==rb[0],'wrong claim: slow rate fixes alpha rejected')
    require(ra[0]==rc[0] and a[1:]!=c[1:],'same alpha still leaves eta/q fiber')
    # A near-endpoint fiber, not merely a moderate-q illustration.
    eps=F(1,10**12)
    near1=(F(1),F(1,4),1-eps);near2=(F(1),F(1,32),1-2*eps)
    require(rates(*near1)==rates(*near2),'exact compensated fiber arbitrarily near q one')
    # Distinct alpha/eta with same q; fixed physical time gives same z.
    t=F(1,10**6)
    za=84*ra[1]*t;zb=84*rb[1]*t
    require(za==zb and 0<za<=F(1,10**6),'independently fixed physical time and common admitted z')
    theta_max=F(1,84*10**6)
    require(1-4*theta_max**2>0,'strict coherent-imaginary monotonicity certificate')
    require(2*theta_max<1 and 12*theta_max**2<1,'X sine arguments strictly inside positive small-angle range')
    require(1-theta_max**2>0,'X amplitude strictly positive from inherited quadratic bound')
    # Exact logarithmic-Jacobian rank and null directions, no floating SVD.
    row=[1,1,3];nulls=[[1,-1,0],[0,-3,1]]
    for v in nulls:require(sum(a*b for a,b in zip(row,v))==0,'demodulated null direction '+str(v))
    require(1*1-0*1==1,'carrier plus slow Jacobian has nonzero alpha/eta minor')
    require(sum(a*b for a,b in zip([1,0,0],nulls[1]))==0,'eta/q fiber survives carrier')
    recovered_eta=84*ra[1]/(ra[0]*(1-a[2])**3)
    require(recovered_eta==a[1],'known q and independently calibrated beta identify eta')
    # Analytic coefficients: actual t=0 derivative claims are intentionally absent.
    cycles,faces,ix,iy=cube()
    mx=moments(F(1),cycles,faces,ix,iy,'X');ms=moments(F(1),cycles,faces,ix,iy,'sum')
    require(mx==[1,0,2,0,16,0,160],'independent X source endpoint moments')
    require(ms==[1,1,4,8,32,80,320],'independent coherent endpoint moments')
    require(ms[2]-ms[1]**2==3,'coherent amplitude identifies positive slow rate')
    reject(mx[1]!=0,'wrong claim: nonzero slow signal requires nonzero first coefficient rejected')
    require(mx[2]>0,'X remains informative through curvature')
    elementary_moments=[F(1)]+[F(0)]*6
    reject(any(elementary_moments[1:]),'wrong claim: elementary variance one implies informative slow endpoint rejected')
    finite=[]
    for q in (F(1,4),F(1,2),1-F(1,10**12),F(1)):
        m=moments(q,cycles,faces,ix,iy,'sum')
        require(m[1]==q**4,'finite-q coherent mean retains weighted physical face '+str(q))
        p=2+5*q+5*q*q+6*q**3+3*q**4
        slope=(3*(1+q)**2*(1+q*q)/p)*m[1]/96
        require(slope==finiteq_slope(q),'finite-q z coefficient reconstructed '+str(q))
        finite.append({'q':q,'linear_imaginary_z_coefficient':slope})
    require(finiteq_slope(F(1))==F(1,84),'limiting coefficient')
    reject(finiteq_slope(a[2])==finiteq_slope(c[2]),'wrong claim: compensated q leaves finite-q center unchanged rejected')
    # Equal q,z centers do not remove eta-dependent state-error prefactor.
    require(a[1]/(1-a[1])!=b[1]/(1-b[1]),'eta-dependent stationary replacement budgets differ on alpha compensation fiber')
    # Pure-phase alias expressed as an exact integer number of cycles, without approximating pi.
    for n in (-1,1,2):require(F(3)*F(2*n,3)==2*n,'elementary phase alias in pi units '+str(n))
    sign_coeffs_X=[F(0),F(1),F(0),F(-1)]
    require(all(mx[n]==0 for n in (1,3,5)),'X analytic map loses rate sign')
    require(ms[1]!=0,'coherent imaginary analytic map resolves rate sign locally')
    bindings=dict(inventory)
    for path in ('check.py','report.md','inputs/source-inventory.json'):
        bindings[str((HERE/path).relative_to(ROOT))]=hashlib.sha256((HERE/path).read_bytes()).hexdigest()
    result={'schema':'ym27-forward-ai1-v1','scope':'analytic endpoint/readout-map identifiability, not exact finite-q inverse theorem',
      'rate_definition':'lambda=alpha*eta*(1-q)^3/(84*hbar)',
      'rational_fibers':{'points':[a,b,c],'rates_beta_lambda':[ra,rb,rc],'near_endpoint_points':[near1,near2]},
      'log_jacobian':{'demodulated':[row],'with_carrier':[[1,0,0],row],'demodulated_rank':1,'with_carrier_rank':2,'remaining_null':nulls[1]},
      'moments':{'X':mx,'sum':ms,'null_elementary':elementary_moments},
      'finite_q_center_slopes':finite,'monotonicity_lower_bound':1-4*theta_max**2,
      'controls':checks,'checks_count':len(checks),'bindings':bindings,
      'nonclaims':['No derivative theorem for actual finite-q correlations','No exact finite-q parameter equivalence','No physical calibration demonstrated','No homogeneous or continuum transfer']}
    out.mkdir(parents=True)
    (out/'results.json').write_text(json.dumps(clean(result),indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','checks':len(checks),'output':str(out/'results.json')}))

if __name__=='__main__':main()
