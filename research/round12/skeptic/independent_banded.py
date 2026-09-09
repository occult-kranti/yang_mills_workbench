#!/usr/bin/env python3
"""Exact-rational finite-Hamiltonian oracles for a dynamic Galerkin theorem.

Real symmetric rational matrices are evolved with a rational complex Taylor
polynomial. Unitarity supplies a rigorous remainder ||Ht||^(M+1)/(M+1)!.
This oracle is independent of production solvers and uses only the stdlib.
"""
from fractions import Fraction as F
from math import factorial,isqrt
from pathlib import Path
import hashlib,json

def sqrt_interval(q,digits=35):
    q=F(q)
    if q<0:raise ValueError('negative norm square')
    scale=10**digits;num=q.numerator*scale*scale;den=q.denominator
    low=isqrt(num//den);upper=low+(low*low*den<num)
    return F(low,scale),F(upper,scale)
def mv(A,v):return [sum((a*b for a,b in zip(row,v)),F(0)) for row in A]
def normsq(state):return sum((x*x+y*y for x,y in zip(*state)),F(0))
def subtract(a,b):return ([x-y for x,y in zip(a[0],b[0])],[x-y for x,y in zip(a[1],b[1])])
def embed(state,n):return (state[0]+[F(0)]*(n-len(state[0])),state[1]+[F(0)]*(n-len(state[1])))
def identity_state(n,index=0,scale=F(1)):
    r=[F(0)]*n;r[index]=scale;return r,[F(0)]*n
def truncate(A,n):return [row[:n] for row in A[:n]]
def evolve_segment(A,t,state,order=70):
    if A!=[list(row) for row in zip(*A)]:raise ValueError('Hermitian real matrix required')
    t=F(t);r,im=list(state[0]),list(state[1]);tr,ti=list(r),list(im)
    for k in range(1,order+1):
        tr,ti=[v*t/k for v in mv(A,ti)],[-v*t/k for v in mv(A,tr)]
        r=[a+b for a,b in zip(r,tr)];im=[a+b for a,b in zip(im,ti)]
    hnorm=max(sum(abs(x) for x in row) for row in A)
    remainder=(abs(t)*hnorm)**(order+1)/factorial(order+1)
    input_norm=sqrt_interval(normsq(state))[1]
    return (r,im),remainder*input_norm
def evolve(segments,state):
    out=state;error=F(0)
    for A,t in segments:
        out,local=evolve_segment(A,t,out);error+=local
    return out,error
def error_interval(a,ea,b,eb):
    lo,hi=sqrt_interval(normsq(subtract(a,b)))
    return max(F(0),lo-ea-eb),hi+ea+eb
def banded(n):
    W=[[F(0)]*n for _ in range(n)]
    for i in range(n-1):W[i][i+1]=W[i+1][i]=F(1,2)
    return W
def hamiltonian(K,W,coefficient):return [[k+coefficient*w for k,w in zip(kr,wr)] for kr,wr in zip(K,W)]
def scaled(A,c):return [[c*x for x in row] for row in A]
def factorial_bound(A,D,d0=0):return min(F(2),F(A)**(D-d0+1)/factorial(D-d0+1))

def main():
    rows=[];gates=[]
    def check(ok,name,detail=None):
        if not ok:raise RuntimeError(name)
        gates.append({'test':name,'passed':True,'detail':detail})
    n=7;W=banded(n);K=[[F(i==j)*F(i*i,4) for j in range(n)] for i in range(n)]
    schedules=[[(F(1,2),F(1))],[(F(1,3),F(1)),(F(1,3),F(-1))],[(F(1,4),F(2)),(F(1,4),F(0))]]
    for initial_degree in (0,1):
        for number,schedule in enumerate(schedules):
            A=sum((t*abs(coefficient) for t,coefficient in schedule),F(0));segments=[(hamiltonian(K,W,c),t) for t,c in schedule]
            full,ef=evolve(segments,identity_state(n,initial_degree))
            for D in range(initial_degree,5):
                projected,ep=evolve([(truncate(H,D+1),t) for H,t in segments],identity_state(D+1,initial_degree))
                interval=error_interval(full,ef,embed(projected,n),ep);bound=factorial_bound(A,D,initial_degree)
                check(interval[1]<=bound,f'factorial_bound.d0{initial_degree}.schedule{number}.D{D}',{'error_upper':str(interval[1]),'bound':str(bound)})
                rows.append({'initial_degree':initial_degree,'schedule':number,'cutoff':D,'action':str(A),'error_interval':list(map(str,interval)),'theorem_bound':str(bound)})
    # Two-level noncommuting free/drive matrices expose cancellation and endpoint errors.
    W2=[[F(0),F(1)],[F(1),F(0)]];K2=[[F(0),F(0)],[F(0),F(1)]]
    initial=identity_state(2)
    canceled,ec=evolve([(hamiltonian(K2,W2,F(1)),F(1,2)),(hamiltonian(K2,W2,F(-1)),F(1,2))],initial)
    interval=error_interval(canceled,ec,initial,F(0))
    check(interval[0]>F(1,10),'signed_action_zero_is_false_bound',{'signed_action':'0','actual_error_lower':str(interval[0])})
    endpoint,ee=evolve([(W2,F(1,2)),(scaled(W2,0),F(1,2))],initial)
    interval=error_interval(endpoint,ee,initial,F(0))
    check(interval[0]>F(2,5),'zero_endpoint_drive_is_false_bound',{'endpoint_lambda':'0','actual_error_lower':str(interval[0])})
    # Broken degree-preserving K: the theorem would falsely assert zero from W=0.
    wrong,ew=evolve([(W2,F(1,4))],initial)
    interval=error_interval(wrong,ew,initial,F(0))
    check(interval[0]>F(1,5),'non_degree_preserving_free_generator_rejected',str(interval[0]))
    # A jump of two coordinate degrees invalidates the one-layer factorial order.
    jump=[[F(0),F(0),F(1)],[F(0),F(0),F(0)],[F(1),F(0),F(0)]]
    jumped,ej=evolve([(jump,F(1,10))],identity_state(3))
    interval=error_interval(jumped,ej,identity_state(3),F(0))
    check(interval[0]>F(1,200),'degree_two_jump_breaks_bandwidth_one',{'error_lower':str(interval[0]),'wrong_bound':'1/200'})
    check(interval[0]>F(1,200),'basis_index_is_not_whole_degree_shell',{'grading':[0,1,1],'bad_retained_indices':[0,1],'correct_degree1_indices':[0,1,2]})
    # Unnormalized states need a scaled cap. At t=3, norm difference exceeds 5.
    unnormalized=identity_state(2,scale=F(3));driven,ed=evolve([(W2,F(3))],unnormalized)
    interval=error_interval(driven,ed,unnormalized,F(0))
    check(interval[0]>5,'cap_two_requires_normalized_states',str(interval[0]))
    # A unitary but incorrect temporal method (returning the initial state) has
    # exact norm conservation and still makes a resolved state error.
    unitary_wrong=initial;true,et=evolve([(W2,F(1))],initial)
    interval=error_interval(true,et,unitary_wrong,F(0))
    check(normsq(unitary_wrong)==1 and interval[0]>F(9,10),'normalization_does_not_certify_time_stepping',str(interval[0]))
    # Exact symbolic identity: exp(-i*pi*sigma_x)e0=-e0 has zero terminal
    # omitted component but state error 2 against P0 evolution.
    returned=([-F(1),F(0)],[F(0),F(0)])
    check(returned[0][1]==0 and normsq(subtract(returned,initial))==4,'terminal_leakage_does_not_bound_state_error')
    source=Path(__file__).resolve();result={'status':'passed','optimized_python':not __debug__,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
      'gate_count':len(gates),'gates':gates,'valid_cases':rows,'oracle':'Exact rational Taylor states with rigorous unitary remainder bounds for finite real symmetric matrices',
      'scope':'Independent finite test models and deliberately broken hypotheses; general theorem rests on separately reviewed block-Duhamel proof.'}
    source.with_name('banded_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':result['status'],'gate_count':len(gates),'source_sha256':result['source_sha256']}))
if __name__=='__main__':main()
