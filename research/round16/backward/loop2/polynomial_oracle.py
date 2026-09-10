"""Exact Taylor coefficients from character polynomials and semicircle moments.

No producer coefficient, disk routine, fusion routine or special function imported.
"""
from fractions import Fraction as Q
from functools import lru_cache
from math import comb,factorial
from shared_projector import character_polynomial,graph_data


def exact(value):
    if type(value) not in (str,int,Q):raise ValueError('exact rational input required')
    try:return Q(value)
    except (ValueError,ZeroDivisionError) as e:raise ValueError('finite rational required') from e


def degree(value):
    if type(value) is not int or not 0<=value<=24:raise ValueError('strict integer degree0..24')
    return value


@lru_cache(maxsize=None)
def trace_moment(power):
    if power%2:return Q(0)
    r=power//2;return Q(comb(2*r,r),r+1)


@lru_cache(maxsize=None)
def project(power,label):
    # Integral x^power chi_label(U), with x=(Tr U)/2.
    poly=character_polynomial(label)
    return sum((c*trace_moment(power+j) for j,c in enumerate(poly)),Q(0))/2**power


@lru_cache(maxsize=None)
def boundary_moment(n,m,power):
    # Multiply ordinary characters as polynomials before Haar integration.
    a,b=character_polynomial(n),character_polynomial(m)
    return sum((ca*cb*trace_moment(power+i+j) for i,ca in enumerate(a) for j,cb in enumerate(b)),Q(0))/2**power


def convolution(a,b,N):
    result=[Q(0)]*(N+1)
    for i,x in enumerate(a):
        if not x:continue
        for j,y in enumerate(b[:N+1-i]):
            if y:result[i+j]+=x*y
    return result


def coefficients(graph,couplings,N,insertion):
    """Coefficient of epsilon^r in integral O exp(epsilon sum k_f x_f)."""
    N=degree(N)
    if type(insertion) is not int or insertion not in (0,1):raise ValueError('uniform insertion0 or1 required')
    if type(couplings) is not list or len(couplings)!=11:raise ValueError('eleven individual coefficients required')
    k=list(map(exact,couplings));data=graph_data(graph);faces=list(data['words'])
    shared=faces.index(data['shared'])
    def disk(ids):
        result={}
        for n in range(N//5+insertion+1):
            series=[Q(1)]+[Q(0)]*N
            for f in ids:
                index=faces.index(f)
                face_series=[k[index]**r*project(r+insertion,n)/factorial(r) for r in range(N+1)]
                series=convolution(series,face_series,N)
            if any(series):result[n]=[v/Q(n+1)**4 for v in series]
        return result
    left,right=disk(sorted(data['left'])),disk(sorted(data['right']))
    answer=[Q(0)]*(N+1)
    for n,a in left.items():
        for m,b in right.items():
            disk_product=convolution(a,b,N)
            shared_series=[k[shared]**r*boundary_moment(n,m,r+insertion)/factorial(r) for r in range(N+1)]
            term=convolution(disk_product,shared_series,N)
            answer=[x+y for x,y in zip(answer,term)]
    return answer


def tail(couplings,N):
    N=degree(N);M=sum(map(abs,map(exact,couplings)),Q(0))
    if M>=N+2:raise ValueError('tail geometric ratio not below one')
    return M**(N+1)/factorial(N+1)/(1-M/Q(N+2))


def quotient(numerator,denominator):
    a,b=map(exact,numerator);c,d=map(exact,denominator)
    if a>b or c>d or c<=0:raise ValueError('ordered numerator and positive denominator intervals required')
    candidates=(a/c,a/d,b/c,b/d)
    return min(candidates),max(candidates)


def enclose(graph,couplings,N):
    Z=coefficients(graph,couplings,N,0);A=coefficients(graph,couplings,N,1)
    R=tail(couplings,N);z=sum(Z);a=sum(A)
    denominator=(max(Q(1),z-R),z+R);numerator=(a-R,a+R)
    return {'Z':Z,'A':A,'tail':R,'Z_interval':denominator,'A_interval':numerator,'expectation':quotient(numerator,denominator)}
