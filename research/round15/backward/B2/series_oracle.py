"""Independent tensor-power multiplicities and total-degree cube Taylor sums."""
from fractions import Fraction as Q
from functools import lru_cache
from math import comb,factorial


def integer(value,maximum):
    if type(value) is not int or not 0<=value<=maximum:
        raise ValueError('bounded nonnegative strict integer required')
    return value


def character_multiplicity(power,label):
    integer(power,32);integer(label,32)
    if label>power or (power-label)%2:return 0
    j=(power-label)//2
    return comb(power,j)-(comb(power,j-1) if j else 0)


def multiply_series(a,b,n):
    out=[Q(0)]*(n+1)
    for i,x in enumerate(a):
        if not x:continue
        for j,y in enumerate(b[:n-i+1]):
            if y:out[i+j]+=x*y
    return out


@lru_cache(maxsize=256)
def _six_series(label,n,insert):
    face=[Q(character_multiplicity(i+insert,label),2**(i+insert)*factorial(i)) for i in range(n+1)]
    out=[Q(1)]+[Q(0)]*n
    for _ in range(6):out=multiply_series(out,face,n)
    return tuple(out)


def action_coefficients(n,insert):
    integer(n,30)
    if type(insert) is not bool:raise ValueError('strict Boolean insertion selector required')
    shift=int(insert);result=[Q(0)]*(n+1)
    for label in range(n//6+shift+1):
        series=_six_series(label,n,shift)
        for i,coefficient in enumerate(series):result[i]+=coefficient/Q((label+1)**4)
    return result


def evaluate(coefficients,k):return sum((coefficient*k**i for i,coefficient in enumerate(coefficients)),Q(0))


def quotient(numerator,denominator):
    if not 0<denominator[0]<=denominator[1]:raise ValueError('positive normalization interval required')
    corners=[x/y for x in numerator for y in denominator]
    return min(corners),max(corners)


def calculate(k,n):
    if type(k) is not Q or abs(k)>1:raise ValueError('rational coupling in[-1,1] required')
    integer(n,30);m=6*abs(k)
    if m>=n+2:raise ValueError('strict geometric remainder ratio required')
    tail=m**(n+1)/factorial(n+1)/(1-m/Q(n+2))
    partition=evaluate(action_coefficients(n,False),k)
    numerator=evaluate(action_coefficients(n,True),k)
    independent=evaluate(_six_series(0,n,0),k)
    z=(max(Q(1),partition-tail),partition+tail)
    zi=(max(Q(1),independent-tail),independent+tail)
    if z[0]>z[1] or zi[0]>zi[1]:raise ValueError('empty Jensen interval')
    a=(numerator-tail,numerator+tail)
    observable=quotient(a,z)
    excess=(z[0]-zi[1],z[1]-zi[0])
    return {'M':m,'tail':tail,'Z_poly':partition,'A_poly':numerator,'Z_ind_poly':independent,
       'Z':z,'A':a,'Z_ind':zi,'observable':observable,'excess':excess,
       'observable_width':observable[1]-observable[0],'excess_width':excess[1]-excess[0]}
