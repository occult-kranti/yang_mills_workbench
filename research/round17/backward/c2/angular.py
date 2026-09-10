"""Independent S² angular reduction followed by scalar semicircle integration."""
from fractions import Fraction as F
from functools import lru_cache
from math import comb,factorial
from geometry import TETRA,IDENTITY

COMMUTING=(IDENTITY,IDENTITY,(F(0),F(1),F(0),F(0)),(F(0),F(-1),F(0),F(0)))
ZERO=(0,0,0,0)


def exact(x):
    if type(x) not in (str,int,F):raise ValueError('exact rational, not Boolean or float')
    try:return F(x)
    except (ValueError,ZeroDivisionError) as e:raise ValueError('finite rational required') from e


def boundary_values(H):
    if type(H) is not tuple or len(H)!=4:raise ValueError('tuple of four boundary quaternions required')
    result=[]
    for q in H:
        if type(q) is not tuple or len(q)!=4:raise ValueError('tuple of four quaternion coordinates required')
        q=tuple(exact(x) for x in q)
        if sum(x*x for x in q)!=1:raise ValueError('unit boundary quaternion required')
        result.append(q)
    return tuple(result)


def multiply(a,b):
    result={}
    for p,c in a.items():
        for q,d in b.items():
            e=tuple(x+y for x,y in zip(p,q));result[e]=result.get(e,F(0))+c*d
    return {e:c for e,c in result.items() if c}


def adjoint(H):
    x={tuple(int(i==j) for j in range(4)):H[i] if i==0 else -H[i] for i in range(4)}
    result={e:4*c/3 for e,c in multiply(x,x).items()};result[ZERO]=result.get(ZERO,F(0))-F(1,3)
    return result


def angular_moment(powers):
    if type(powers) is not tuple or len(powers)!=3 or any(type(k) is not int or k<0 for k in powers):raise ValueError('strict tuple of three nonnegative integer angular exponents required')
    return _angular_moment(powers)


@lru_cache(None)
def _angular_moment(powers):
    if any(k%2 for k in powers):return F(0)
    numerator=1;denominator=1
    for p in powers:
        for j in range(1,p,2):numerator*=j
    for j in range(sum(powers)//2):denominator*=3+2*j
    return F(numerator,denominator)


def reduce_angular(poly):
    result={}
    for powers,coefficient in poly.items():
        angular=angular_moment(powers[1:])
        if not angular:continue
        K=sum(powers[1:])//2
        for j in range(K+1):
            power=powers[0]+2*j;term=coefficient*angular*comb(K,j)*(-1)**j
            result[power]=result.get(power,F(0))+term
    return {k:c for k,c in result.items() if c}


def semicircle(power):
    if type(power) is not int or power<0:raise ValueError('strict nonnegative integer semicircle exponent required')
    return _semicircle(power)


@lru_cache(None)
def _semicircle(power):
    if power%2:return F(0)
    m=power//2
    return F(comb(2*m,m)//(m+1),4**m)


def radial_data(boundaries):
    boundaries=boundary_values(boundaries);observable={ZERO:F(1)};individual=[]
    for H in boundaries:
        p=adjoint(H);observable=multiply(observable,p);individual.append(reduce_angular(p))
    return reduce_angular(observable),individual


def scalar_coefficients(radial,b0,degree):
    if type(degree) is not int or not 0<=degree<=16 or type(b0) is not F:raise ValueError('strict bounded integer degree and Fraction action coefficient required')
    return [b0**n/F(factorial(n))*sum(c*semicircle(p+n) for p,c in radial.items()) for n in range(degree+1)]


def quotient(numerator,denominator):
    a,b=numerator;c,d=denominator
    if a>b or c<=0 or c>d:raise ValueError('ordered numerator and positive denominator intervals required')
    values=[a/c,a/d,b/c,b/d]
    return min(values),max(values)


def data(boundaries,coefficients,degree,precision='1/1000000000000'):
    H=boundary_values(boundaries)
    if type(coefficients) is not tuple or len(coefficients)!=4:raise ValueError('tuple of four physical coefficients required')
    ks=tuple(map(exact,coefficients));tol=exact(precision)
    if type(degree) is not int or not 0<=degree<=16 or tol<=0:raise ValueError('integer degree zero through sixteen and positive precision required')
    directions=[(q[0],-q[1],-q[2],-q[3]) for q in H];b=tuple(sum(k*a[j] for k,a in zip(ks,directions)) for j in range(4))
    if any(b[1:]):raise ValueError('this exact numerical routine requires scalar-axis or zero action vector')
    M=abs(b[0])
    if M>=degree+2:raise ValueError('geometric exponential remainder requires M less than degree plus two')
    radial,individual=radial_data(H);A=scalar_coefficients(radial,b[0],degree);Z=scalar_coefficients({0:F(1)},b[0],degree)
    tail=M**(degree+1)/F(factorial(degree+1))/(1-M/F(degree+2))
    Aval=sum(A);Zval=sum(Z);Zi=(max(F(1),Zval-tail),Zval+tail);Ai=(Aval-tail,Aval+tail);interval=quotient(Ai,Zi)
    return {'boundary':H,'coefficients':ks,'degree':degree,'precision':tol,'directions':directions,'b':b,'branch':'zero-b Haar' if not M else 'scalar-axis action',
      'M':M,'radial':radial,'individual_radial':individual,'A_coefficients':A,'Z_coefficients':Z,'A_value':Aval,'Z_value':Zval,'tail':tail,'A_interval':Ai,'Z_interval':Zi,
      'expectation_interval':interval,'width':interval[1]-interval[0],
      'sign':'positive' if interval[0]>0 else 'negative' if interval[1]<0 else 'zero' if interval==(0,0) else 'inconclusive',
      'precision_status':'met' if interval[1]-interval[0]<=tol else 'insufficient'}


def comparison(kappa,degree,precision='1/1000000000000'):
    k=exact(kappa);left=data(TETRA,(k,)*4,degree,precision);right=data(COMMUTING,(k,)*4,degree,precision)
    if left['b']!=right['b'] or left['Z_interval']!=right['Z_interval']:raise ValueError('comparison requires same action and partition')
    diff=right['A_value']-left['A_value'];tail=right['tail']+left['tail'];Ai=(diff-tail,diff+tail);interval=quotient(Ai,left['Z_interval']);width=interval[1]-interval[0]
    return {'kappa':k,'degree':degree,'T':left,'C':right,'contrast_numerator_interval':Ai,'contrast_interval':interval,'contrast_width':width,
      'sign_status':'positive' if interval[0]>0 else 'insufficient','precision_status':'met' if width<=left['precision'] else 'insufficient',
      'status':'positive' if interval[0]>0 and width<=left['precision'] and left['precision_status']==right['precision_status']=='met' else 'insufficient'}


def encoded(value):
    if type(value) is F:return str(value)
    if type(value) is dict:return {str(k):encoded(v) for k,v in value.items()}
    if type(value) in (tuple,list):return [encoded(v) for v in value]
    return value
