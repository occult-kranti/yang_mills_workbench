#!/usr/bin/env python3
"""Independent exact matrix falsifier for Gibbs-state/physical-vacuum identification.

This is an advisor side audit; it does not construct a mass gap. The cube is
independently enumerated here, with a loop's full orientation irrelevant to its
SU(2) trace. Each individual signed link factor is differentiated directly.
"""
from pathlib import Path
from itertools import product,combinations
import hashlib,json
from fractions import Fraction as Q
from dataclasses import dataclass

@dataclass(frozen=True)
class Gaussian:
    re: Q=Q(0)
    im: Q=Q(0)
    @staticmethod
    def cast(x): return x if isinstance(x,Gaussian) else Gaussian(Q(x))
    def __add__(self,b):
        b=self.cast(b);return Gaussian(self.re+b.re,self.im+b.im)
    __radd__=__add__
    def __neg__(self):return Gaussian(-self.re,-self.im)
    def __sub__(self,b):return self+-self.cast(b)
    def __mul__(self,b):
        b=self.cast(b);return Gaussian(self.re*b.re-self.im*b.im,self.re*b.im+self.im*b.re)
    __rmul__=__mul__
    def __truediv__(self,b):return self*Q(1,b)
    def conjugate(self):return Gaussian(self.re,-self.im)

class Matrix:
    def __init__(self,rows):self.a=tuple(tuple(Gaussian.cast(x) for x in row) for row in rows)
    def __mul__(self,b):
        if isinstance(b,Matrix):return Matrix([[sum((self.a[i][k]*b.a[k][j] for k in range(2)),Gaussian()) for j in range(2)] for i in range(2)])
        return Matrix([[x*b for x in row] for row in self.a])
    __rmul__=__mul__
    def __truediv__(self,b):return self*Q(1,b)
    def __neg__(self):return self*-1
    def adjoint(self):return Matrix([[self.a[j][i].conjugate() for j in range(2)] for i in range(2)])
    def trace(self):return self.a[0][0]+self.a[1][1]

J=Gaussian(Q(0),Q(1))

HERE=Path(__file__).resolve().parent
I=Matrix([[1,0],[0,1]])
PAULI=(Matrix([[0,1],[1,0]]),Matrix([[0,-J],[J,0]]),Matrix([[1,0],[0,-1]]))
GENERATORS=tuple(p*J/2 for p in PAULI)
VERTICES=tuple(product((0,1),repeat=3))
EDGES=tuple((v,tuple(v[j]+(j==axis) for j in range(3))) for v in VERTICES for axis in range(3) if v[axis]==0)
def word(vertices):
    result=[]
    for v,w in zip(vertices,vertices[1:]+vertices[:1]):
        if (v,w) in EDGES:result.append((EDGES.index((v,w)),1))
        elif (w,v) in EDGES:result.append((EDGES.index((w,v)),-1))
        else:raise ValueError('Face contains a nonexistent cube edge')
    return tuple(result)
FACES=[]
for a,b in combinations(range(3),2):
    c=next(i for i in range(3) if i not in (a,b))
    for side in (0,1):
        vs=[]
        for u,v in ((0,0),(1,0),(1,1),(0,1)):
            x=[0,0,0];x[a]=u;x[b]=v;x[c]=side;vs.append(tuple(x))
        FACES.append(word(vs))
FACES=tuple(FACES)
def trace_product(values,face,derivative=None,order=0):
    matrix=I
    for edge,sign in face:
        U=values[edge]
        if derivative is not None and edge==derivative[0]:
            T=GENERATORS[derivative[1]]
            if order==1:factor=T*U if sign==1 else -U.adjoint()*T
            elif order==2:factor=-U/4 if sign==1 else -U.adjoint()/4
            else:raise ValueError('Invalid derivative order')
        else:factor=U if sign==1 else U.adjoint()
        matrix=matrix*factor
    return matrix.trace()/2
def run():
    checks=[]
    def gate(name,ok):
        if not ok:raise ValueError(name)
        checks.append({'name':name,'passed':True})
    gate('Independently enumerated cube counts',len(VERTICES)==8 and len(EDGES)==12 and len(FACES)==6)
    gate('All face words have four distinct links',all(len(set(e for e,_ in f))==4 for f in FACES))
    gate('Every link meets exactly two faces',all(sum(any(e==j for e,_ in f) for f in FACES)==2 for j in range(12)))
    fixtures=[]
    for name,U,expectedS,expectedG in [('identity',I,Q(6),Q(0)),('one_center_link',-I,Q(2),Q(0)),('one_noncentral_link',Matrix([[J,0],[0,-J]]),Q(4),Q(5,2))]:
        values=[I]*12;values[0]=U
        S=sum(trace_product(values,f) for f in FACES)
        grad=[];lap=Gaussian()
        for edge in range(12):
            for a in range(3):
                first=sum(trace_product(values,f,(edge,a),1) for f in FACES if any(j==edge for j,_ in f))
                second=sum(trace_product(values,f,(edge,a),2) for f in FACES if any(j==edge for j,_ in f))
                gate(name+' real Lie derivative '+str((edge,a)),first.im==0)
                grad.append(first);lap+=second
        G=sum((x*x for x in grad),Gaussian())
        gate(name+' exact action trace',S==Gaussian(expectedS))
        gate(name+' exact squared gradient',G==Gaussian(expectedG))
        gate(name+' total electric Casimir eigenvalue',-lap-3*S==Gaussian())
        fixtures.append({'fixture':name,'S':str(S.re),'gradient_squared':str(G.re),'electric_Casimir_S':str(-lap.re)})
    # Exact polynomial coefficients in (alpha*kappa, lambda, alpha*kappa^2).
    ratios=[(Q(3,2)*Q(f['S']),-Q(f['S']),-Q(f['gradient_squared'])/4) for f in fixtures]
    difference=tuple(a-b for a,b in zip(ratios[0],ratios[1]))
    gate('Central configurations force linear coefficient to vanish',difference==(Q(6),Q(-4),Q(0)))
    matched=[(a+Q(3,2)*b,c) for a,b,c in ratios]
    gate('Matching cancels every linear coefficient',all(a==0 for a,_ in matched))
    gate('Noncentral configuration rejects nonzero Gibbs exponent',matched[2][1]-matched[0][1]==Q(-5,8))
    result={'status':'passed','checks_count':len(checks),'checks':checks,'fixtures':fixtures,
      'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'identity':'H psi/psi=(3 alpha kappa/2-lambda) S-alpha kappa^2 |grad S|^2/4, psi proportional exp(kappa S/2)',
      'verdict':'For alpha>0, the cube Gibbs square root with kappa!=0 is not an eigenstate of this electric-plus-Wilson Hamiltonian for any lambda.',
      'scope':'Exact configuration-space test for the stated finite cube; no spectral lower bound or continuum claim.'}
    (HERE/'cube_state_check.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'passed','checks':len(checks),'fixtures':fixtures}));return result
if __name__=='__main__':run()
