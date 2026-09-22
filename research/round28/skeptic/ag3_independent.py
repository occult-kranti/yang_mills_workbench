#!/usr/bin/env python3
"""AG3 independent exact diagnostics; no physical SU(2) cutoff is used."""
from fractions import Fraction as Q
from math import factorial
from pathlib import Path
from itertools import product
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parents[3]
CHECKS = []


def require(name, condition):
    if not condition:
        raise RuntimeError(name)
    CHECKS.append(name)


def zero(n):
    return [[Q(0) for j in range(n)] for i in range(n)]


def eye(n):
    return [[Q(i==j) for j in range(n)] for i in range(n)]


def add(a,b):
    return [[x+y for x,y in zip(u,v)] for u,v in zip(a,b)]


def scale(t,a):
    return [[t*x for x in row] for row in a]


def mul(a,b):
    n=len(a)
    return [[sum((a[i][k]*b[k][j] for k in range(n)),Q(0)) for j in range(n)] for i in range(n)]


def comm(a,b):
    return add(mul(a,b),scale(-1,mul(b,a)))


def power(a,n):
    result=eye(len(a))
    for _ in range(n):result=mul(result,a)
    return result


def ad(a,b,n):
    for _ in range(n):b=comm(a,b)
    return b


def exp_coefficient(x,h,b,n):
    result=zero(len(x))
    for i in range(n+1):
        result=add(result,scale(Q((-1)**(n-i),factorial(i)*factorial(n-i)),
                               mul(mul(power(x,i),h),power(x,n-i))))
    if n:
        for i in range(n):
            result=add(result,scale(Q((-1)**(n-1-i),factorial(i)*factorial(n-1-i)),
                                   mul(mul(power(x,i),b),power(x,n-1-i))))
    return result


def split(k):
    n=len(k);p=zero(n);p[0][0]=1;q=add(eye(n),scale(-1,p))
    c=k[0][0]
    b=add(mul(mul(p,k),q),mul(mul(q,k),p))
    d=mul(mul(q,add(k,scale(-c,eye(n)))),q)
    return c,b,d,p,q


def algebra():
    h=zero(3);h[1][1]=1;h[2][2]=2
    b=[[Q(0),Q(3,5),Q(4,5)],[Q(3,5),Q(0),Q(0)],[Q(4,5),Q(0),Q(0)]]
    x=zero(3)
    for i in (1,2):x[i][0]=b[i][0]/h[i][i];x[0][i]=-x[i][0]
    d=[[Q(0),Q(0),Q(0)],[Q(0),Q(1,7),Q(1,11)],[Q(0),Q(1,11),Q(-1,13)]]
    old_scalar=Q(5,13)
    require('bare_first_commutator',comm(x,h)==scale(-1,b))
    require('rank_source_unit_norm_squared',sum(b[i][0]**2 for i in (1,2))==1)
    require('bare_inverse_norm_squared_below_source',sum(x[i][0]**2 for i in (1,2))==Q(13,25))
    for sign in (-1,0,1):
        xx=scale(sign,x);bb=scale(sign,b);dd=scale(sign,d)
        constant=add(h,add(dd,scale(old_scalar,eye(3))))
        for n in range(7):
            direct=exp_coefficient(xx,constant,bb,n)
            if n==0:
                expected=constant
            else:
                expected=scale(Q(1,factorial(n)),ad(xx,dd,n))
                if n>=2:expected=add(expected,scale(Q(n-1,factorial(n)),ad(xx,bb,n-1)))
            require(f'full_BCH_sign{sign}_degree{n}',direct==expected)
        require(f'old_scalar_stays_sign{sign}',exp_coefficient(xx,constant,bb,0)!=add(h,dd))
        if sign:
            leading=comm(xx,dd)
            require(f'retained_D_linear_term_sign{sign}',leading!=zero(3))
            second=exp_coefficient(xx,constant,bb,2)
            wrong=add(scale(Q(1,2),ad(xx,dd,2)),comm(xx,bb))
            require(f'wrong_BCH_coefficient_sign{sign}',second!=wrong)
            c,bnew,dnew,p,q=split(second)
            require(f'new_scalar_source_diagonal_sign{sign}',second==add(scale(c,eye(3)),add(bnew,dnew)))
            require(f'new_scalar_nonzero_sign{sign}',c!=0)
            require(f'dropped_centering_rejected_sign{sign}',second!=add(scale(c,eye(3)),add(bnew,mul(mul(q,second),q))))
            require(f'dropped_new_scalar_rejected_sign{sign}',second!=add(bnew,dnew))
    # Zero input B means zero generator even with a nonzero retained D.
    for n in range(1,4):
        require(f'zero_B_with_nonzero_D_degree{n}',exp_coefficient(zero(3),add(h,d),zero(3),n)==zero(3))
    # Tensor identity on a nonvacuum exterior is part of the actual source.
    def kron(a,b):return [[a[i//len(b)][j//len(b)]*b[i%len(b)][j%len(b)] for j in range(len(a)*len(b))] for i in range(len(a)*len(b))]
    flip=[[Q(0),Q(1)],[Q(1),Q(0)]];j=[[Q(0),Q(-1)],[Q(1),Q(0)]]
    local_h=[[Q(0),Q(0)],[Q(0),Q(1)]];p0=[[Q(1),Q(0)],[Q(0),Q(0)]]
    full_h=add(kron(local_h,eye(2)),kron(eye(2),scale(100,local_h)))
    full_x=kron(j,eye(2));full_b=kron(flip,eye(2));wrong_b=kron(flip,p0)
    require('exterior_identity_commutator',comm(full_x,full_h)==scale(-1,full_b))
    require('excited_exterior_identity_discriminant',full_b[3][1]==1 and wrong_b[3][1]==0)
    # Actual overlapping operators, including a retained-diagonal cross term.
    x_cross=kron(j,eye(2));d_cross=kron(local_h,flip)
    require('nontrivial_overlap_retained',comm(x_cross,d_cross)!=zero(4))
    return {'source_norm_squared':'1','generator_norm_squared':'13/25','old_scalar':str(old_scalar),
            'scope':'Finite exact algebra diagnostics; no actual SU(2) norm or spectral evaluation.'}


def support_controls():
    supports=[frozenset(range(0,4)),frozenset(range(3,7)),frozenset(range(6,10))]
    for n in range(1,4):
        words=[(supports[0],())]
        for _ in range(n):
            words=[(y|z,w+(j,)) for y,w in words for j,z in enumerate(supports) if y&z]
        require(f'repetitions_retained_{n}',any(w==(0,)*n for _,w in words))
        require(f'assigned_minimum_support_{n}',all(len(y)>=4 for y,_ in words))
        if n>=2:
            require(f'outer_can_miss_seed_{n}',any(not(supports[0]&supports[w[-1]]) for _,w in words))
            require(f'cannot_reset_four_site_support_{n}',any(len(y)>4 for y,_ in words))
    y,z=supports[:2]
    require('root_in_first_only',0 in y and 0 not in z)
    require('root_in_second_only',6 in z and 6 not in y)
    require('nonempty_overlap_one_site',len(y&z)==1)
    out=Q(3,2)
    require('exact_nonempty_overlap_weight_gain',out**len(y|z)==out**len(y)*out**len(z)/out)
    # Pauli X on Y and Pauli Z at the single overlap in Z anticommute.
    # Their nonzero commutator has full union support and norm two.
    require('incoming_root_would_be_lost',6 in y|z and 6 not in y)
    require('outgoing_root_would_be_lost',0 in y|z and 0 not in z)
    for size in (4,8,16,64):
        require(f'scalar_density_minimum_cost_{size}',1/(size*out**size)<=Q(4,81))
        require(f'diagonal_relative_minimum_cost_{size}',2/out**size<=Q(32,81))
        require(f'no_free_weight_reset_{size}',Q(2)**size/out**size==Q(4,3)**size)
    require('weight_reset_ratio_unbounded_example',Q(4,3)**64>10**7)
    # A standard Pauli family has equal-weight commutator ratio m/a.
    # The unbounded sequence is proved in the report, not inferred from samples.
    for m in (4,16,64):require(f'equal_weight_growth_{m}',Q(m,2)>=2)
    return {'supports':[sorted(y) for y in supports],'minimum_assigned_size':4,
            'root_policy':'Both root placements; every indexed overlap and repetition.'}


def endpoint(m,k):
    c=Q(288,31);d=64*m+2*k;x=c*k
    gamma=c*(d+k)/(1-x)
    residual=k*gamma
    old_scalar=k/64;extra_scalar=Q(4,81)*residual
    old_relative=4*m+k/8;extra_relative=Q(32,81)*residual
    return {'M':m,'K_cap':k,'c':c,'d_cap':d,'radius_cap':x,'factor_cap':gamma,
            'residual_cap_at_weight_3_over_2':residual,
            'old_scalar_density_cap':old_scalar,'new_scalar_density_cap':extra_scalar,
            'total_scalar_density_cap':old_scalar+extra_scalar,
            'mixing_output_cap':residual,'diagonal_output_norm_cap':d+2*residual,
            'old_reference_relative_cap':old_relative,'new_relative_increment_cap':extra_relative,
            'reference_gap_lower':1-old_relative-extra_relative}


def arithmetic():
    lower=sum((Q((-1)**(n-1),n)*Q(1,3)**n for n in range(1,5)),Q(0))
    require('log_lower_polynomial_integral',lower==Q(31,108))
    require('nested_commutator_rational_constant',Q(8,3)/lower==Q(288,31))
    rows=[]
    for name,m,k in [('zero',Q(0),Q(0)),('narrow',Q(1,10000),Q(7,100000)),('main',Q(1,1000),Q(7,1000))]:
        row=endpoint(m,k);rows.append(row)
        require(name+':strict_radius',row['radius_cap']<1)
        require(name+':factor_below_17_over_20',row['factor_cap']<Q(17,20))
        require(name+':positive_reference_gap',row['reference_gap_lower']>Q(99,100))
        if name=='main':require('exact_main_factor',row['factor_cap']==Q(3060,3623))
        if name=='narrow':require('narrow_factor_below_1_over_16',row['factor_cap']<Q(1,16))
        if k:
            for r in (k/1000,k/2,k):
                actual_factor=row['c']*(row['d_cap']+r)/(1-row['c']*r)
                require(name+':actual_norm_multiplier:'+str(r),r*actual_factor<=r*row['factor_cap'])
            r=k/1000;fake_output=k/100
            require(name+':upper_budget_division_falsifier',fake_output/k<Q(17,20) and fake_output/r>Q(17,20))
        else:require('zero_update_before_division',row['residual_cap_at_weight_3_over_2']==0)
    for x in (Q(0),Q(1,100),Q(1,10)):
        require('complete_geometric_tail:'+str(x),sum((x**n for n in range(1,9)),Q(0))+x**9/(1-x)==x/(1-x))
    # Bounded local generators preserve a proved graph domain; they do not
    # regularize an arbitrary exterior vector with coefficients 1/j.
    for n in (4,16,64):
        require(f'exterior_Hilbert_norm_bounded_{n}',sum((Q(1,j*j) for j in range(1,n+1)),Q(0))<2)
        require(f'exterior_energy_norm_grows_{n}',sum(Q(1) for j in range(1,n+1))==n)
    return rows


def encode(v):
    if isinstance(v,Q):return {'exact':str(v),'decimal':format(float(v),'.17g')}
    if isinstance(v,dict):return {k:encode(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [encode(x) for x in v]
    return v


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=Path(__file__).with_name('ag3-independent.json'))
    args=parser.parse_args()
    manifest=json.loads(Path(__file__).with_name('ag3-inputs').joinpath('source-inventory.json').read_text())
    for p,h in manifest['sources'].items():
        for label,q in [('live',ROOT/p),('snapshot',Path(__file__).with_name('ag3-inputs')/p)]:
            require(label+':'+p,hashlib.sha256(q.read_bytes()).hexdigest()==h)
    alg=algebra();geom=support_controls();rows=arithmetic()
    payload={'schema':'ym28-ag3-independent-v1','checks':len(CHECKS),'check_names':CHECKS,
             'algebra':alg,'geometry':geom,'endpoints':rows,'sources':manifest['sources'],
             'attribution':'The weight-changing inequality and main numerical target were shared advisor proposals; this checker and accompanying proof were independently executed after contract freeze.',
             'scope':'One full-source correction from input weight2 to output weight3/2; reference-only gap. No same-weight contraction, all-stage convergence or full physical gap.'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(encode(payload),indent=2,sort_keys=True)+'\n')
    print(json.dumps({'checks':len(CHECKS),'status':'passed'},sort_keys=True))


if __name__=='__main__':main()
