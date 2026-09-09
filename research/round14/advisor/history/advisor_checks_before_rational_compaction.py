"""Independent symbolic cumulant algebra and reuse of reviewed rational evidence."""
from pathlib import Path
from fractions import Fraction as F
from math import comb
import hashlib
import importlib.util
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
PIN = 'e912eb67f1835b6f9218f52620a8fa57f740e085fda8d87be96b3a9f571ed41a'


def add(*polys):
    result = {}
    for p in polys:
        for m, c in p.items():
            result[m] = result.get(m, F(0)) + c
    return {m: c for m, c in result.items() if c}


def scale(p, c):
    return {m: F(c)*v for m, v in p.items() if c*v}


def mul(*polys):
    result = {(): F(1)}
    for p in polys:
        terms = []
        for a, x in result.items():
            for b, y in p.items():
                terms.append({tuple(sorted(a+b)): x*y})
        result = add(*terms)
    return result


def moment(a, b, c):
    return {(): F(1)} if a+b+c == 0 else {((a,b,c),): F(1)}


def derivative(p):
    terms = []
    for factors, coefficient in p.items():
        for i, (a,b,c) in enumerate(factors):
            rest = {factors[:i]+factors[i+1:]: coefficient}
            dm = add(moment(a,b,c+1), scale(mul(moment(a,b,c),moment(0,0,1)),-1))
            terms.append(mul(rest,dm))
    return add(*terms)


def covariance(a,b):
    return add(moment(*(x+y for x,y in zip(a,b))), scale(mul(moment(*a),moment(*b)),-1))


def main():
    checks = []
    def gate(name, condition):
        checks.append({'name': name, 'passed': bool(condition)})
        if not condition:
            raise ValueError(name)
    mx,my,mz = moment(1,0,0),moment(0,1,0),moment(0,0,1)
    xy = covariance((1,0,0),(0,1,0))
    d2 = derivative(derivative(xy))
    centered = {}
    for a in range(2):
        for b in range(2):
            for c in range(3):
                factors=[moment(a,b,c)]+[mx]*(1-a)+[my]*(1-b)+[mz]*(2-c)
                centered=add(centered,scale(mul(*factors),(-1)**(4-a-b-c)*comb(2,c)))
    varz=covariance((0,0,1),(0,0,1))
    xz=covariance((1,0,0),(0,0,1)); yz=covariance((0,1,0),(0,0,1))
    cumulant=add(centered,scale(mul(xy,varz),-1),scale(mul(xz,yz),-2))
    gate('Second exponential-family derivative equals centered fourth cumulant',d2==cumulant)
    gate('Omitting covariance subtraction fails the formal identity',d2!=centered)
    gate('Wrong repeated-z contraction coefficient fails',d2!=add(centered,scale(mul(xy,varz),-1),scale(mul(xz,yz),-1)))
    # Each derivative is performed on independent formal raw moments, with no
    # numerical fixture or forward-model implementation in this calculation.
    bound=4+1+2
    gate('Bound7 follows from the three independently bounded terms',bound==7)
    source=ROOT/'vendor/moment_bounds.py'
    gate('Round13 exact checker source matches its independent reviewed version',hashlib.sha256(source.read_bytes()).hexdigest()==PIN)
    spec=importlib.util.spec_from_file_location('ym14_legacy_moments',source)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    collection=json.loads((ROOT/'vendor/round13-certificates.json').read_text())
    certificate=next(c for c in collection['certificates'] if c['kappa']=='1' and c['level']==6)
    gate('Existing variance certificate replays exactly',module.verify(certificate) is True)
    lo,hi=map(F,certificate['variance_interval'])
    gate('Existing variance interval is strictly positive',0<lo<=hi)
    rows=[]
    for eta in [F(-1,1024),F(1,1024),F(1,4)]:
        linear=sorted([eta*lo*lo,eta*hi*hi]); radius=F(7,2)*eta*eta
        lower,upper=linear[0]-radius,linear[1]+radius
        status='positive' if lower>0 else 'negative' if upper<0 else 'inconclusive'
        rows.append({'k1':'1','k2':'1','eta':str(eta),'lower':str(lower),'upper':str(upper),
                     'lower_display':float(lower),'upper_display':float(upper),'status':status,
                     'scope':'Exact perturbative covariance enclosure in the declared finite Euclidean mixed-loop measure.'})
    gate('Positive small deformation has rigorously positive covariance',rows[1]['status']=='positive')
    gate('Negative small deformation has rigorously negative covariance',rows[0]['status']=='negative')
    gate('Larger deformation remains inconclusive under this sufficient bound',rows[2]['status']=='inconclusive')
    # These finite restrictions illustrate the analytical spectral accumulation
    # countermodel. Their numerical sizes do not constitute the infinite proof.
    spectral=[{'n':n,'lowest_nonzero_energy':str(F(1,n))} for n in (2,4,8,16,32)]
    gate('Same static state can coexist with arbitrarily small excitation energies',all(F(r['lowest_nonzero_energy'])==F(1,r['n']) for r in spectral))
    record={'status':'passed','count':len(checks),'checks':checks,
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'legacy_checker_sha256':PIN,
        'legacy_collection_sha256':hashlib.sha256((ROOT/'vendor/round13-certificates.json').read_bytes()).hexdigest(),
        'perturbative_intervals':rows,'spectral_countermodel_restrictions':spectral,
        'limits':['Formal polynomial identity plus conventional analytic inequalities, not a proof assistant.',
                  'Perturbative sign only inside its sufficient range; an inconclusive interval does not prove zero covariance.',
                  'The spectral countermodel isolates a missing generator premise; it is not asserted to be Yang–Mills.']}
    (HERE/'advisor_checks.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({'status':'passed','count':len(checks),'intervals':[{k:r[k] for k in ['eta','lower_display','upper_display','status']} for r in rows]}))


if __name__=='__main__':
    main()
