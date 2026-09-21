#!/usr/bin/env python3
"""Independent exact compact-filter moments; no physical spectral approximation."""
from pathlib import Path
from fractions import Fraction as F
from math import factorial
import hashlib,json

def require(condition,message):
    if not condition:raise ValueError(message)
def result():
    theta=F(1,16);M=F(35,1664)
    require(192*M*theta==F(105,416),'radius')
    rows=[]
    for n in range(1,9):
        residual_coeff=(-1)**n*theta**(2*n)/factorial(2*n+1)
        L_coeff=(-1)**(n+1)*theta**(2*n)/factorial(2*n+1)
        require(-L_coeff==residual_coeff,'filter sign')
        integral=theta**(2*n)/((2*n)*(2*n+1))
        require((-1)**(n-1)*integral/factorial(2*n-1)==L_coeff,'triangular moment')
        rows.append({'n':n,'residual_even_coefficient':str(residual_coeff),'generator_odd_coefficient':str(L_coeff)})
    return {'schema':'ym23-s2-skeptic-preparation-checks-v1','status':'passed','radius_max':'105/416','zero_frequency_residual':'1','zero_frequency_generator':'0','exact_taylor_moments':rows,'scope':'independent exact filter coefficient checks; no physical frequency sampling or new research loop'}

if __name__=='__main__':
    path=Path(__file__).with_name('s2-independent-preparation-checks.json')
    encoded=(json.dumps(result(),indent=2,sort_keys=True)+'\n').encode()
    require(path.read_bytes()==encoded,'frozen preparation output drift')
    print(json.dumps({'status':'passed','sha256':hashlib.sha256(encoded).hexdigest()}))
