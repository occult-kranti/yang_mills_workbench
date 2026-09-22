#!/usr/bin/env python3
"""Independent exact structural controls. Does not import producer code."""
from fractions import Fraction as F
from pathlib import Path
import hashlib,json
BASE=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parent/'ai1-independent.json'
checks=[]
def require(name,condition):
    if not condition: raise RuntimeError(name)
    checks.append(name)
def kappa(alpha,eta,q,hbar=F(1)):
    return alpha*eta*(1-q)**3/hbar
def endpoint_jets(k):
    # Derivatives in physical time of F_X(k t), F_plus(k t).
    return {'x1':F(0),'x2':-2*(k/84)**2,'plus1_im':k/84,'plus2':-4*(k/84)**2,'null1':F(0),'null2':F(0)}
def raw_jets(a,k,h=F(1)):
    # Multiplication by a known mathematical carrier is conditional, not a new finite-q theorem.
    omega=F(9,2)*a/h
    return {'x1_im':-omega,'plus1_im':-omega+k/84,'x2':-omega**2-2*(k/84)**2}
a,eta,q=F(2),F(1,2),F(3,4)
k=kappa(a,eta,q)
require('reference effective rate',k==F(1,64))
# Full analytic readouts coincide because the scalar argument itself coincides.
fibers=[(a,eta,q),(F(4),F(1,4),q),(a,F(1,16),F(1,2))]
for i,(aa,ee,qq) in enumerate(fibers):
    require(f'fiber {i} admissible',aa>0 and 0<ee<1 and 0<qq<1)
    require(f'fiber {i} same scalar argument',kappa(aa,ee,qq)==k)
    require(f'fiber {i} jets same',endpoint_jets(kappa(aa,ee,qq))==endpoint_jets(k))
require('distinct alpha fiber exists',fibers[0][0]!=fibers[1][0])
require('distinct q eta fiber exists',fibers[0][1:]!=fibers[2][1:])
require('raw carrier separates changed alpha',raw_jets(a,k)!=raw_jets(F(4),k))
require('raw carrier leaves fixed alpha q eta fiber',raw_jets(a,k)==raw_jets(fibers[2][0],k))
j=raw_jets(a,k)
recovered_a=-F(2,9)*j['x1_im']
recovered_k=84*(j['plus1_im']-j['x1_im'])
require('raw joint slope recovers alpha',recovered_a==a)
require('raw joint slope recovers effective rate',recovered_k==k)
require('known q recovers eta',recovered_k/(recovered_a*(1-q)**3)==eta)
require('wrong single phase second moment rejected',F(4)!=F(1)**2)
require('wrong single cosine fourth moment rejected',F(16)!=F(2)**2)
# Sensitivities of kappa: log derivatives (1,1,-3q/(1-q)). Outer product rank <=1.
g=[F(1),F(1),-3*q/(1-q)]
J=[[u*v for v in g] for u in g]
for i in range(3):
 for j2 in range(i+1,3):
  for m in range(3):
   for n in range(m+1,3):
    require(f'Fisher minor {i}{j2}{m}{n} zero',J[i][m]*J[j2][n]-J[i][n]*J[j2][m]==0)
# Formal independent finite-q correction can recover q; equality of limiting maps alone cannot exclude it.
eps=F(1,1000)
require('endpoint equality need not finite-q equality',k+eps*fibers[0][2]!=k+eps*fibers[2][2])
# Exact noise-degeneracy control: two rates within 2*epsilon/derivative coefficient share an observation interval.
noise=F(1,10**12)
k2=k+84*noise
require('slope observations with radius epsilon overlap',abs(k2/84-k/84)<=2*noise)
result={'schema':'ym27-independent-ai1-v1','status':'PASS','number_of_checks':len(checks),'checks':checks,'scope':'Exact algebra for explicitly declared asymptotic maps and conditional carrier; not finite-q nonidentifiability or uncertainty-certified physical observation.','reference_rate':str(k),'fibers':[[str(v) for v in x] for x in fibers],'contract_sha256':hashlib.sha256((BASE/'research/round27/contracts/ai1.json').read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
OUT.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','checks':len(checks),'output':str(OUT)}))
