#!/usr/bin/env python3
"""Independent T1 rational lower-block and compressed-power controls."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib

def need(c,m):
    if not c:raise ValueError(m)
def mm(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def sub(a,b):return [[x-y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def power(a,n):
    z=[[F(i==j) for j in range(len(a))] for i in range(len(a))]
    for _ in range(n):z=mm(z,a)
    return z
def pp(a):return [row[:2] for row in a[:2]]
rows=[]
for lam in [F(0),F(1,10000),F(1,100)]:
 m=18*lam;det=lam*(3-m)-F(25,4)*lam*lam
 need(det==lam*(3-F(97,4)*lam)>=0,'actual lower block positivity')
 need(3-m>0,'complement decay denominator')
 rows.append({'lambda':str(lam),'m':str(m),'determinant_lower':str(det)})
# Two selected coordinates, one complementary coordinate: an algebra fixture only.
b=[F(1,7),F(2,9)];d=F(1,5)
h0=[[F(1),F(0),b[0]],[F(0),F(2),b[1]],[b[0],b[1],F(3)]]
h=[row[:] for row in h0];h[2][2]+=d
need(pp(h)==pp(h0),'first compressed coefficient')
need(pp(power(h,2))==pp(power(h0,2)),'second compressed coefficient')
cubic=pp(sub(power(h,3),power(h0,3)));expected=[[d*x*y for y in b] for x in b]
need(cubic==expected,'third compressed return coefficient')
bb=[[x*y for y in b] for x in b];repeat=mm(bb,bb)
need(any(x for row in repeat for x in row),'omitted second return term')
result={'schema':'ym23-t1-skeptic-preparation-checks-v1','status':'passed','positive_lower_block':rows,'cubic_power_difference':[[str(x) for x in row] for row in cubic],'repeated_return_coefficient':[[str(x) for x in row] for row in repeat],'scope':'exact algebra controls; actual infinite-rank block proof is in preparation text'}
p=Path(__file__).with_name('t1-independent-preparation-checks.json');data=(json.dumps(result,indent=2,sort_keys=True)+'\n').encode()
if p.exists():need(p.read_bytes()==data,'frozen output changed')
else:p.write_bytes(data)
print(json.dumps({'status':'passed','sha256':hashlib.sha256(data).hexdigest()}))
