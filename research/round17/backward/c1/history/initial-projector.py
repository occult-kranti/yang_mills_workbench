"""S³-polynomial Haar oracle for the full four-adjoint tensor."""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product


ZERO=(0,0,0,0)
def mono(i,j,coefficient=1):
    p=[0]*4;p[i]+=1;p[j]+=1
    return {tuple(p):coefficient}


def add(*polynomials):
    ans={}
    for p in polynomials:
        for e,c in p.items():ans[e]=ans.get(e,0)+c
    return {e:c for e,c in ans.items() if c}


def mul(a,b):
    ans={}
    for e,c in a.items():
        for f,d in b.items():
            k=tuple(x+y for x,y in zip(e,f));ans[k]=ans.get(k,0)+c*d
    return {e:c for e,c in ans.items() if c}


def scale(poly,k):return {e:c*k for e,c in poly.items() if c*k}


@lru_cache(None)
def sphere_moment(powers):
    if len(powers)!=4 or any(type(k) is not int or k<0 for k in powers):raise ValueError('four exact nonnegative exponents required')
    if any(k%2 for k in powers):return F(0)
    numerator=1
    for k in powers:
        for j in range(1,k,2):numerator*=j
    denominator=1
    for j in range(sum(powers)//2):denominator*=4+2*j
    return F(numerator,denominator)


def integrate(poly):return sum(c*sphere_moment(e) for e,c in poly.items())


def rotation_polynomials():
    return (
      add(mono(0,0),mono(1,1),mono(2,2,-1),mono(3,3,-1)),add(mono(1,2,2),mono(0,3,-2)),add(mono(1,3,2),mono(0,2,2)),
      add(mono(1,2,2),mono(0,3,2)),add(mono(0,0),mono(1,1,-1),mono(2,2),mono(3,3,-1)),add(mono(2,3,2),mono(0,1,-2)),
      add(mono(1,3,2),mono(0,2,-2)),add(mono(2,3,2),mono(0,1,2)),add(mono(0,0),mono(1,1,-1),mono(2,2,-1),mono(3,3)))


def evaluate(poly,q):
    return sum(c*q[0]**e[0]*q[1]**e[1]*q[2]**e[2]*q[3]**e[3] for e,c in poly.items())


def rotation(q):
    values=[evaluate(p,q) for p in rotation_polynomials()]
    return [values[3*i:3*i+3] for i in range(3)]


@lru_cache(None)
def entry_moment(indices):
    if len(indices)!=4:raise ValueError('four rotation factors required')
    poly={ZERO:1};R=rotation_polynomials()
    for i in indices:poly=mul(poly,R[i])
    return integrate(poly)


def haar_projector():
    labels=list(product(range(3),repeat=4))
    P=[[entry_moment(tuple(sorted(3*a[k]+b[k] for k in range(4)))) for b in labels] for a in labels]
    return labels,P


def matmul(a,b):
    out=[[F(0) for _ in b[0]] for _ in a]
    sparse=[[ (j,v) for j,v in enumerate(row) if v] for row in b]
    for i,row in enumerate(a):
        for k,v in enumerate(row):
            if v:
                for j,w in sparse[k]:out[i][j]+=v*w
    return out


def rank(matrix):
    a=[list(map(F,row)) for row in matrix];row=0
    for col in range(len(a[0])):
        pivot=next((j for j in range(row,len(a)) if a[j][col]),None)
        if pivot is None:continue
        a[row],a[pivot]=a[pivot],a[row];p=a[row][col];a[row]=[x/p for x in a[row]]
        for j in range(row+1,len(a)):
            if a[j][col]:
                f=a[j][col];a[j]=[x-f*y for x,y in zip(a[j],a[row])]
        row+=1
        if row==len(a):break
    return row


def pair_basis(labels):
    return [[F(a[0]==a[1] and a[2]==a[3]),F(a[0]==a[2] and a[1]==a[3]),F(a[0]==a[3] and a[1]==a[2])] for a in labels]


def generators(labels):
    index={a:i for i,a in enumerate(labels)};ans=[]
    for a,b in ((1,2),(2,0),(0,1)):
        J=[[F(0) for _ in labels] for _ in labels]
        for col,v in enumerate(labels):
            for k in range(4):
                w=list(v)
                if v[k]==b:w[k]=a;J[index[tuple(w)]][col]+=1
                if v[k]==a:w[k]=b;J[index[tuple(w)]][col]-=1
        ans.append(J)
    return ans


def adjoint_poly(H):
    x={tuple(int(j==i) for j in range(4)):H[i] if i==0 else -H[i] for i in range(4)}
    return add(scale(mul(x,x),4),{ZERO:-1})


def joint_polynomial(holonomies):
    ans={ZERO:1}
    for H in holonomies:ans=mul(ans,adjoint_poly(H))
    return ans


def tensor_contraction(P,labels,holonomies):
    rotations=[rotation(H) for H in holonomies];answer=F(0)
    for i,a in enumerate(labels):
        for j,b in enumerate(labels):
            if P[i][j]:
                term=P[i][j]
                for k in range(4):term*=rotations[k][b[k]][a[k]]
                answer+=term
    return answer
