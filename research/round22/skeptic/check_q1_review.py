#!/usr/bin/env python3
"""Independent Q1 moment and noncommuting Duhamel-order controls."""
import argparse
from fractions import Fraction as F
import hashlib
from itertools import product
import json
from math import factorial
from pathlib import Path
import subprocess
import sys
import tempfile

def need(ok,why):
    if ok is not True: raise RuntimeError(why)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def mm(a,b):return [[sum((x*y for x,y in zip(r,c)),F(0)) for c in zip(*b)] for r in a]
def add(a,b):return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def scale(a,s):return [[s*x for x in r] for r in a]
def sub(a,b):return add(a,scale(b,-1))
def eye(n):return [[F(i==j) for j in range(n)] for i in range(n)]
def power(a,n):
    ans=eye(len(a))
    for _ in range(n):ans=mm(ans,a)
    return ans
def pp(a):return [r[:2] for r in a[:2]]
def qq(a):return [r[2:] for r in a[2:]]
def serial(a):return [[str(x) for x in r] for r in a]

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    out=parser.parse_args().output
    need(not out.exists(),'fresh output required')
    root=Path(__file__).resolve().parents[3]
    prep=root/'research/round22/skeptic/check_q1_preparation.py'
    frozen=root/'research/round22/skeptic/q1-preparation-checks.json'
    with tempfile.TemporaryDirectory(prefix='ym22-q1-independent-') as folder:
        target=Path(folder)/'preparation.json'
        flags=['-B']+(['-O'] if sys.flags.optimize else [])
        run=subprocess.run([sys.executable,*flags,str(prep),'--output',str(target)],capture_output=True,text=True)
        need(run.returncode==0,'frozen independent preparation failed: '+run.stderr)
        need(target.read_bytes()==frozen.read_bytes(),'frozen independent graph/moment replay drift')
    axes=[tuple(F(sign) if i==j else F(0) for i in range(4)) for j in range(4) for sign in [-1,1]]
    values=[];covariances=[]
    for u,w in product(axes,repeat=2):
        r=sum((x*y for x,y in zip(u,w)),F(0));x=u[0];z=w[0]
        values.append(F(19,4)+(r+x+z)/2)
        covariances.append((r,x,z))
    mean=sum(values,F(0))/64;second=sum((v*v for v in values),F(0))/64
    cov=[[sum((row[i]*row[j] for row in covariances),F(0))/64 for j in range(3)] for i in range(3)]
    need(cov==scale(eye(3),F(1,4)),'three trace channels not pairwise Haar orthogonal')
    need(mean==F(19,4) and second==F(91,4) and second-mean*mean==F(3,16),'reference squared multiplier moment')
    need(second/4==F(91,16),'reference vector quadratic norm coefficient')
    # Positive, strictly diagonally dominant physical-algebra surrogate only.
    H=[[F(x) for x in row] for row in [[4,1,1,1],[1,6,0,2],[1,0,6,1],[1,2,1,7]]]
    need(all(H[i][i]>sum(abs(H[i][j]) for j in range(4) if i!=j) for i in range(4)),'positive block witness')
    A=pp(H);C=qq(H);B=[r[:2] for r in H[2:]];Bt=list(map(list,zip(*B)))
    D=[[H[i][j] if (i<2)==(j<2) else F(0) for j in range(4)] for i in range(4)]
    B2=mm(Bt,B)
    need(mm(A,B2)!=mm(B2,A),'noncommuting witness required')
    coefficients=[];wrong_four=None
    for n in range(2,7):
        exact=scale(sub(pp(power(H,n)),power(A,n)),F((-1)**n,factorial(n)))
        actual=scale(eye(2),0);wrong=scale(eye(2),0)
        for a in range(n-1):
            for b in range(n-1-a):
                c=n-2-a-b
                piece=mm(mm(mm(mm(power(A,a),Bt),qq(power(H,b))),B),power(A,c))
                bad=mm(mm(mm(mm(power(A,a),Bt),power(C,b)),B),power(A,c))
                weight=F((-1)**(n-2),factorial(n))
                actual=add(actual,scale(piece,weight));wrong=add(wrong,scale(bad,weight))
        need(actual==exact,'symmetric double-Duhamel ordering/factor at degree '+str(n))
        if n==4:
            need(wrong!=exact,'discarding interior returns must be discriminating')
            wrong_four={'correct':serial(exact),'incorrect_complement_only':serial(wrong),'margin':serial(sub(exact,wrong))}
        coefficients.append({'degree':n,'verified_exact_coefficient':serial(exact)})
    for shift in [F(-7,3),F(5)]:
        shifted=add(H,scale(eye(4),shift));sa=pp(shifted)
        need(sub(pp(power(shifted,2)),power(sa,2))==B2,'common scalar alters leakage')
        need(sub(sa,A)==scale(eye(2),shift),'unequal scalar does not alter first derivative')
    need(sub(pp(power(D,2)),power(A,2))==scale(eye(2),0),'zero off-diagonal recovery')
    result={'schema':'ym22-skeptic-independent-check-v1','loop':'q1','passed':True,
      'checker_sha256':sha(Path(__file__)),'producer_imports':False,'research_loops_added':0,
      'frozen_preparation_driver_sha256':sha(prep),'frozen_preparation_output_sha256':sha(frozen),
      'frozen_preparation_byte_exact':True,
      'independent_Haar_covariance':serial(cov),'K_Haar_mean':str(mean),'K_squared_Haar_mean':str(second),
      'K_Haar_variance':str(second-mean*mean),'reference_vector_defect_norm_coefficient_squared':'91/16',
      'symmetric_Duhamel_coefficients':coefficients,'wrong_middle_semigroup_control_degree_four':wrong_four,
      'fixture_development':'Initial second diagonal entry5 made A commute with B*B and failed the explicit noncommutation guard; changing it to6 supplies the required noncommuting control before review freeze',
      'common_and_unequal_scalar_controls':True,'zero_off_diagonal_recovery':True,
      'block_fixture_scope':'Formal noncommuting algebra only; actual infinite-dimensional topology is proved in the mathematical review',
      'topology_review':'Strong quotient and scalar norm asymptotic do not imply norm convergence of the quotient'}
    out.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'loop':'q1','passed':True,'degrees_checked':[2,3,4,5,6]}))
if __name__=='__main__':main()
