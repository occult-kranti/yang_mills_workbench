"""Exact compact SU(2) two-loop covariance enclosures by finite Taylor sums.

This is a fixed finite Euclidean action. No floating arithmetic enters a
certificate. Haar monomial integrals use a quaternion/angular Beta expansion.
"""
from __future__ import annotations

import hashlib
import math
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

SOURCE_PATH = Path(__file__).resolve()
SOURCE_BYTES = SOURCE_PATH.read_bytes()
SOURCE_SHA256 = hashlib.sha256(SOURCE_BYTES).hexdigest()
SCHEMA = "ym14-two-loop-taylor-certificate-v1"
SCOPE = {
    "group": "SU(2)",
    "space": "two holonomies U,V with normalized product Haar measure",
    "exponent": "k1*x+k2*y+eta*z",
    "coordinates": "x=Tr(U)/2; y=Tr(V)/2; z=Tr(UV)/2",
    "observable": "Cov(x,y) in the normalized finite Euclidean measure",
    "limit": "fixed finite action; no Hamiltonian or continuum claim",
}
INTEGRAL_NAMES = ("Z", "Ax", "Ay", "Axy")
MAX_DEGREE = 48


def _source_unchanged():
    if SOURCE_PATH.read_bytes() != SOURCE_BYTES:
        raise ValueError("producer source changed after module load")


def _integer(value, name, maximum):
    if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= maximum:
        raise ValueError(f"{name} must be an integer from 0 to {maximum}, not a Boolean")
    return value


def _rational(value, name="rational", canonical=False):
    if isinstance(value, bool) or not isinstance(value, (int, str, F)):
        raise ValueError(f"{name} must be an exact rational, not a float or Boolean")
    if isinstance(value, str) and len(value) > 20000:
        raise ValueError(f"{name} exceeds the serialized rational size limit")
    try:
        result = F(value)
    except (ValueError, ZeroDivisionError, OverflowError) as exc:
        raise ValueError(f"invalid {name}") from exc
    if canonical and (not isinstance(value, str) or str(result) != value):
        raise ValueError(f"{name} must be a canonical rational string")
    return result


def _parameters(k1, k2, eta):
    p = tuple(_rational(v,n) for v,n in zip((k1,k2,eta),("k1","k2","eta")))
    if any(abs(v) > 8 for v in p) or sum(map(abs,p)) > 12:
        raise ValueError("certificate implementation requires |each coupling|<=8 and sum<=12")
    return p


@lru_cache(maxsize=None)
def _q(n, s):
    """Exact Haar E[x^n (1-x²)^s], via its positive Beta-factorial value."""
    if n % 2:
        return F(0)
    r = n // 2
    return F(2 * math.factorial(2*r) * math.factorial(2*s+2),
             4**(r+s+1) * math.factorial(r) * math.factorial(s+1) * math.factorial(r+s+1))


def haar_moment(a, b, c):
    """E_Haar[x^a y^b z^c] with z=xy−sqrt(1−x²)sqrt(1−y²)cos(gamma)."""
    a,b,c = (_integer(v,n,MAX_DEGREE+2) for v,n in zip((a,b,c),("a","b","c")))
    if a+b+c > MAX_DEGREE+2:
        raise ValueError("total Haar monomial degree exceeds the implementation limit")
    return _haar_moment(a,b,c)


@lru_cache(maxsize=None)
def _haar_moment(a,b,c):
    return sum((F(math.comb(c,j),j+1) * _q(a+c-j,j//2) * _q(b+c-j,j//2)
                for j in range(0,c+1,2)),F(0))


def interval_add(a, b):
    return a[0]+b[0], a[1]+b[1]


def interval_sub(a, b):
    return a[0]-b[1], a[1]-b[0]


def interval_mul(a, b):
    products = (a[0]*b[0],a[0]*b[1],a[1]*b[0],a[1]*b[1])
    return min(products),max(products)


def interval_div_positive(a,b):
    if not (b[0] > 0 and b[1] >= b[0]):
        raise ValueError("denominator interval must be strictly positive and ordered")
    return interval_mul(a,(1/b[1],1/b[0]))


def exponential_tail(m, degree):
    m = _rational(m,"absolute exponent bound")
    degree = _integer(degree,"degree",MAX_DEGREE)
    if m < 0:
        raise ValueError("absolute exponent bound is negative")
    ratio = m/F(degree+2)
    if ratio >= 1:
        raise ValueError("tail requires degree+2 > absolute exponent bound")
    remainder = m**(degree+1)/math.factorial(degree+1)/(1-ratio)
    return ratio,remainder


@lru_cache(maxsize=128)
def _polynomial_integrals(k1,k2,eta,degree):
    coefficients=[]
    for parameter in (k1,k2,eta):
        coefficients.append(tuple(parameter**j/math.factorial(j) for j in range(degree+1)))
    result=[F(0) for _ in INTEGRAL_NAMES]
    for i in range(degree+1):
        for j in range(degree-i+1):
            for k in range(degree-i-j+1):
                coefficient=coefficients[0][i]*coefficients[1][j]*coefficients[2][k]
                if not coefficient:
                    continue
                for index,(a,b) in enumerate(((0,0),(1,0),(0,1),(1,1))):
                    result[index] += coefficient*haar_moment(i+a,j+b,k)
    return tuple(result)


def certify(k1,k2,eta,degree=24):
    _source_unchanged()
    k1,k2,eta = _parameters(k1,k2,eta)
    degree = _integer(degree,"degree",MAX_DEGREE)
    m=abs(k1)+abs(k2)+abs(eta)
    ratio,remainder=exponential_tail(m,degree)
    polynomial=dict(zip(INTEGRAL_NAMES,_polynomial_integrals(k1,k2,eta,degree)))
    enclosed={name:(value-remainder,value+remainder) for name,value in polynomial.items()}
    # Jensen uses E_Haar[S]=0, so the exact positive normalizer is >=1.
    enclosed["Z"]=(max(F(1),enclosed["Z"][0]),enclosed["Z"][1])
    if enclosed["Z"][1] < enclosed["Z"][0]:
        raise ValueError("Taylor and Jensen normalization enclosures do not intersect")
    numerator=interval_sub(interval_mul(enclosed["Z"],enclosed["Axy"]),
                           interval_mul(enclosed["Ax"],enclosed["Ay"]))
    denominator=(enclosed["Z"][0]**2,enclosed["Z"][1]**2)
    covariance=interval_div_positive(numerator,denominator)
    enclosed.update(numerator=numerator,denominator=denominator,covariance=covariance)
    lo,hi=covariance
    if lo>0:
        status="certified-positive"
    elif hi<0:
        status="certified-negative"
    elif lo==hi==0:
        status="certified-zero"
    else:
        status="certified-enclosure-inconclusive"
    return {
        "schema":SCHEMA,"scope":dict(SCOPE),"source_sha256":SOURCE_SHA256,
        "parameters":dict(zip(("k1","k2","eta"),map(str,(k1,k2,eta)))),
        "degree":degree,"absolute_exponent_bound":str(m),
        "tail":{"first_omitted_degree":degree+1,"ratio_bound":str(ratio),"remainder":str(remainder)},
        "polynomial_integrals":{k:str(v) for k,v in polynomial.items()},
        "enclosures":{k:list(map(str,v)) for k,v in enclosed.items()},
        "width":str(hi-lo),"status":status,
    }


def verify(certificate):
    """Strict canonical replay. Returns True or raises ValueError.

    Recomputes every field from declared parameters; a hash alone is not
    mathematical verification. No externally supplied status is trusted.
    """
    _source_unchanged()
    if type(certificate) is not dict:
        raise ValueError("certificate must be an object")
    expected_keys={"schema","scope","source_sha256","parameters","degree","absolute_exponent_bound",
                   "tail","polynomial_integrals","enclosures","width","status"}
    if set(certificate) != expected_keys or certificate["schema"] != SCHEMA:
        raise ValueError("wrong certificate schema")
    if certificate["scope"] != SCOPE or certificate["source_sha256"] != SOURCE_SHA256:
        raise ValueError("wrong scope or producer source")
    params=certificate["parameters"]
    if type(params) is not dict or set(params) != {"k1","k2","eta"}:
        raise ValueError("wrong parameter fields")
    p=[_rational(params[name],name,canonical=True) for name in ("k1","k2","eta")]
    degree=_integer(certificate["degree"],"degree",MAX_DEGREE)
    expected=certify(*p,degree)
    if certificate != expected:
        raise ValueError("certificate arithmetic, intervals, semantics or metadata do not replay")
    return True
