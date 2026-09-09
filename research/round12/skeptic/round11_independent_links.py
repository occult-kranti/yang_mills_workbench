#!/usr/bin/env python3
"""Independent exact seven-link SU(2) and quotient checks; stdlib only.

This file deliberately does not import the production solver. Complex matrix
jets differentiate every original link occurrence before any tree reduction.
Run with Python or Python -O. Failure gates use explicit exceptions.
"""
from fractions import Fraction as F
from itertools import product
from math import factorial, comb
from pathlib import Path
import hashlib
import json


class Q:
    """Gaussian rational; separate from quaternion arithmetic."""
    def __init__(self, r=0, i=0):
        self.r, self.i = F(r), F(i)
    def __add__(self, other):
        b = other if isinstance(other, Q) else Q(other)
        return Q(self.r+b.r, self.i+b.i)
    __radd__ = __add__
    def __neg__(self): return Q(-self.r, -self.i)
    def __sub__(self, other): return self + (-other if isinstance(other,Q) else -Q(other))
    def __mul__(self, other):
        b = other if isinstance(other, Q) else Q(other)
        return Q(self.r*b.r-self.i*b.i, self.r*b.i+self.i*b.r)
    __rmul__ = __mul__
    def conj(self): return Q(self.r, -self.i)
    def __eq__(self, other):
        b = other if isinstance(other, Q) else Q(other)
        return self.r == b.r and self.i == b.i


I = ((Q(1), Q()), (Q(), Q(1)))
O = ((Q(), Q()), (Q(), Q()))
T = (
    ((Q(),Q(0,F(1,2))),(Q(0,F(1,2)),Q())),
    ((Q(),Q(F(1,2))),(Q(-F(1,2)),Q())),
    ((Q(0,F(1,2)),Q()),(Q(),Q(0,-F(1,2)))),
)
def madd(a,b): return tuple(tuple(a[i][j]+b[i][j] for j in range(2)) for i in range(2))
def mscale(a,s): return tuple(tuple(a[i][j]*s for j in range(2)) for i in range(2))
def mm(a,b): return tuple(tuple(sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)) for i in range(2))
def dagger(a): return tuple(tuple(a[j][i].conj() for j in range(2)) for i in range(2))
def realtrace(a):
    v = (a[0][0]+a[1][1])*F(1,2)
    if v.i: raise RuntimeError('Trace is not exactly real')
    return v.r
def su2(t):
    den = 1+sum(F(v)**2 for v in t)
    w = (2-den)/den
    x,y,z = [2*F(v)/den for v in t]
    return ((Q(w,z),Q(y,x)),(Q(-y,x),Q(w,-z)))
def jmul(a,b):
    return (mm(a[0],b[0]),
            madd(mm(a[1],b[0]),mm(a[0],b[1])),
            madd(madd(mm(a[2],b[0]),mscale(mm(a[1],b[1]),2)),mm(a[0],b[2])))

# A→B→C and D→E→F, with vertical links f:A→D,s:B→E,c:C→F.
# All letters below are actual independent link variables.
WORDS = (
    (('s',1),('e',-1),('f',-1),('a',1)),
    (('b',1),('c',1),('d',-1),('s',-1)),
    (('s',1),('e',-1),('f',-1),('a',1),('b',1),('c',1),('d',-1),('s',-1)),
)
ENDS = {'a':('A','B'),'b':('B','C'),'c':('C','F'),'d':('E','F'),
        'e':('D','E'),'f':('A','D'),'s':('B','E')}

def trace_jet(links,word,link=None,axis=0,omit_inverse=False):
    out = (I,O,O)
    for name,orientation in word:
        u = links[name]
        if orientation == -1 and not omit_inverse:
            u = dagger(u)
            jet = (u, mscale(mm(u,T[axis]),-1),mscale(u,-F(1,4))) if name == link else (u,O,O)
        else:
            jet = (u,mm(T[axis],u),mscale(u,-F(1,4))) if name == link else (u,O,O)
        out = jmul(out,jet)
    return tuple(realtrace(m) for m in out)


def metric(coords,rho=F(1)):
    x,y,z = coords
    return [[(3+rho)*(1-x*x)/4, rho*(z-x*y)/4, 3*(y-x*z)/4],
            [rho*(z-x*y)/4,(3+rho)*(1-y*y)/4,3*(x-y*z)/4],
            [3*(y-x*z)/4,3*(x-y*z)/4,3*(1-z*z)/2]]
def drift(coords,rho=F(1)):
    x,y,z=coords
    return [(9+3*rho)*x/4,(9+3*rho)*y/4,9*z/2]
def domain(q):
    x,y,z=q
    return 1-x*x-y*y-z*z+2*x*y*z
def demand(test,label):
    if not test: raise RuntimeError(label)


def compositions(n):
    for i in range(n+1):
        for j in range(n-i+1):
            for k in range(n-i-j+1): yield (i,j,k,n-i-j-k)
def sphere_moment(exponents):
    if any(e%2 for e in exponents): return F(0)
    total = sum(exponents)//2
    out = F(1)
    for exponent in exponents:
        for j in range(exponent//2): out *= F(2*j+1,2)
    for j in range(total): out /= 2+j
    return out
def matrix_haar_moment(a,b,c):
    """Expand z = Σ signature_i U_i V_i under two independent S³ Haar laws."""
    out = F(0)
    for ks in compositions(c):
        k0,k1,k2,k3=ks
        mult=F(factorial(c),1)
        for k in ks: mult /= factorial(k)
        out += (-1)**(c-k0)*mult*sphere_moment((a+k0,k1,k2,k3))*sphere_moment((b+k0,k1,k2,k3))
    return out
def semicircle_moment(n):
    return F(comb(n,n//2), (n//2+1)*4**(n//2)) if n%2 == 0 else F(0)
def reduced_haar_moment(a,b,c):
    """Independent orientation t uniform on [-1,1], x,y semicircular."""
    out=F(0)
    for k in range(0,c+1,2):
        r=k//2
        mx=sum((-1)**j*comb(r,j)*semicircle_moment(a+c-k+2*j) for j in range(r+1))
        my=sum((-1)**j*comb(r,j)*semicircle_moment(b+c-k+2*j) for j in range(r+1))
        out += F(comb(c,k),k+1)*mx*my
    return out


def main():
    records=[]
    def check(ok,label,detail=None):
        demand(ok,label)
        records.append({'test':label,'passed':True,'detail':detail})
    samples=[
        {n:su2((F(i+1,i+3),F(2-i,i+4),F(i%3-1,i+2))) for i,n in enumerate(ENDS)},
        {n:su2((F(i%2,i+2),F(i+2,i+5),F(1-i,i+6))) for i,n in enumerate(ENDS)},
        {n:I for n in ENDS},
    ]
    g={n:su2((F(i+1,i+2),F(2,i+3),F(-1,i+4))) for i,n in enumerate('ABCDEF')}
    mutations=[]
    for case,links in enumerate(samples):
        for n,u in links.items(): check(mm(u,dagger(u)) == I,f'unitarity.case{case}.{n}')
        q=tuple(trace_jet(links,w)[0] for w in WORDS)
        check(domain(q)>=0,f'quotient_domain.case{case}')
        changed={n:mm(mm(g[source],u),dagger(g[target])) for n,u in links.items() for source,target in [ENDS[n]]}
        check(tuple(trace_jet(changed,w)[0] for w in WORDS)==q,f'six_vertex_gauge.case{case}')
        derivatives={}
        for n in ENDS:
            for axis in range(3):
                derivatives[n,axis]=[trace_jet(links,w,n,axis) for w in WORDS]
        check(all(derivatives['s',axis][2][1:]==(0,0) for axis in range(3)),f'shared_cancellation_z.case{case}')
        for rho in (F(0),F(1,3),F(1),F(4)):
            actual_d=[F(0)]*3
            actual_a=[[F(0)]*3 for _ in range(3)]
            for (n,axis),jets in derivatives.items():
                weight=rho if n=='s' else F(1)
                for i in range(3):
                    actual_d[i]-=weight*jets[i][2]
                    for j in range(3): actual_a[i][j]+=weight*jets[i][1]*jets[j][1]
            target_a,target_d=metric(q,rho),drift(q,rho)
            check(actual_a==target_a,f'exact_link_metric.case{case}.rho{rho}')
            check(actual_d==target_d,f'exact_link_drift.case{case}.rho{rho}')
            x,y,z=q
            kxy=actual_d[0]*y+actual_d[1]*x-2*actual_a[0][1]
            check(kxy==(9+4*rho)*x*y/2-rho*z/2,f'k_xy.case{case}.rho{rho}')
            if case==0 and rho==1:
                controls={
                    'independent_rotors_xy':6*x*y,
                    'shared_cross_sign_xy':F(11,2)*x*y+z/2,
                    'extra_factor_four_xy':4*kxy,
                    'omitted_shared_link_xy':F(9,2)*x*y,
                }
                for name,wrong in controls.items():
                    check(wrong!=kxy,f'mutation_rejected.{name}')
                    mutations.append({'mutation':name,'wrong':str(wrong),'correct':str(kxy),'defect':str(wrong-kxy)})
        if case==0:
            badq=tuple(trace_jet(links,w,omit_inverse=True)[0] for w in WORDS)
            badg=tuple(trace_jet(changed,w,omit_inverse=True)[0] for w in WORDS)
            check(badq!=badg,'mutation_rejected.omitted_daggers_gauge')
            mutations.append({'mutation':'omitted_daggers','gauge_invariance_failure':True})
    for degree in range(9):
        for a in range(degree+1):
            for b in range(degree-a+1):
                c=degree-a-b
                m1,m2=matrix_haar_moment(a,b,c),reduced_haar_moment(a,b,c)
                check(m1==m2,f'haar_moment.{a}.{b}.{c}',str(m1))
    check(matrix_haar_moment(0,0,0)==1,'haar_normalized')
    check(matrix_haar_moment(1,1,1)==F(1,16),'haar_xyz_1_over_16')
    check(matrix_haar_moment(0,0,2)==F(1,4),'haar_z2_1_over_4')
    check(matrix_haar_moment(2,2,0)-matrix_haar_moment(1,1,1)/2+matrix_haar_moment(0,0,2)/16==F(3,64),'coupled_eigenfunction_norm_3_over_64')
    # A quotient boundary is singular, but Haar-pulled-back regular states need
    # no artificial Dirichlet condition there. Exact normals vanish in A.
    for x,y,z in [(F(1),F(2,3),F(2,3)),(F(0),F(0),F(1)),(F(3,5),F(3,5),F(-7,25)),(F(1),F(1),F(1))]:
        check(domain((x,y,z))==0,f'boundary_domain.{x}.{y}.{z}')
        normal=[-2*x+2*y*z,-2*y+2*x*z,-2*z+2*x*y]
        a=metric((x,y,z))
        check(all(sum(a[i][j]*normal[j] for j in range(3))==0 for i in range(3)),f'boundary_no_normal_diffusion.{x}.{y}.{z}')
    here=Path(__file__).resolve()
    result={'status':'passed','scope':'finite seven-link six-vertex SU(2); exact link jets and Haar moments; no continuum or truncation certificate',
            'source_sha256':hashlib.sha256(here.read_bytes()).hexdigest(),
            'gate_count':len(records),'records':records,'retained_mutation_failures':mutations}
    output=here.with_name('independent_results.json')
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'gate_count':len(records),'source_sha256':result['source_sha256'],'output':str(output)}))
if __name__=='__main__': main()
