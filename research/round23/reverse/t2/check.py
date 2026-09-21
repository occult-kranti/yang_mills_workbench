#!/usr/bin/env python3
"""Exact polynomial margin and spectral-derivative algebra; same T2 author."""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import sys
sys.dont_write_bytecode = True
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from t2_common import need, emit


def padd(a,b):
    return [(a[i] if i<len(a) else 0)+(b[i] if i<len(b) else 0) for i in range(max(len(a),len(b)))]


def pmul(a,b):
    c=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]+=x*y
    return c


def scale(x,a): return [[x*v for v in row] for row in a]
def add(a,b): return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def mm(a,b): return [[sum(a[i][k]*b[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
def enc(a): return [[str(v) for v in row] for row in a]


def main():
    # x=100 lambda lies in [0,1]. Prove the whole cubic margin by its Bernstein coefficients.
    d=[F(3),-F(2,5)]; g=[F(3),-F(17,40)]
    poly=padd([60*x for x in pmul(pmul(d,d),g)],[-400*x for x in d])
    poly=padd(poly,[0,-F(5,2)])
    n=len(poly)-1
    bern=[sum(poly[k]*F(comb(i,k),comb(n,k)) for k in range(i+1)) for i in range(n+1)]
    need(all(x>0 for x in bern),'positive complete-interval Bernstein margin')
    need(sum(poly)==F(48,25),'endpoint margin recomputed')
    # A rational orthonormal eigenbasis gives exact derivatives without root enclosures.
    r=F(1,400); cs=(1-r*r)/(1+r*r); sn=2*r/(1+r*r)
    psi=[cs,sn]; excited=[-sn,cs]
    I=[[F(1),F(0)],[F(0),F(1)]]; Q=[[F(0),F(0)],[F(0),F(1)]]
    G=[[x*y for y in psi] for x in psi]; R=add(I,scale(-1,G))
    gap=F(3); energy=F(1,5); H=add(scale(energy,I),scale(gap,R))
    lam=F(1,100); W=scale(20*lam,Q); ep=20*lam*sn*sn
    X=add(W,scale(-ep,I)); Z=[[F(0),F(0)],[F(0),F(0)]]
    need(mm(G,G)==G and mm(G,R)==Z,'spectral projection algebra')
    need(mm(mm(G,X),G)==Z,'centered ground-ground cancellation')
    wrong=mm(mm(G,W),G)
    need(wrong==scale(ep,G) and wrong!=Z,'omitted centering secular witness')
    GP=scale(-1/gap,add(mm(mm(R,W),G),mm(mm(G,W),R)))
    need(add(mm(H,GP),mm(W,G))==add(mm(GP,H),mm(G,W)),'differentiated commutation')
    need(add(mm(G,GP),mm(GP,G))==GP,'differentiated projection identity')
    need(mm(Q,R)[1][0]==-mm(Q,G)[1][0]!=0,'initial excited leakage retained')
    need(H[0][0]>=19*lam and H[1][1]>=3 and abs(H[1][0])<=F(5,2)*lam,'fixture structural bounds')
    need(ep>0 and GP[0][0]!=0,'ground equality control discriminates')
    # Removing leakage loses one power: general perturbation norm=20lambda, not O(lambda^2).
    need(W[1][1]/lam==20 and W[1][1]/lam**2==2000,'unprojected linear budget distinguished')
    # A scalar small absolute error cannot bound relative error at a vanishing denominator.
    small=F(1,10**12); diff=F(1,10**6)
    need(diff<60*lam**2 and diff/small>10**5,'relative ratio inference rejected')
    emit('reverse', {'uniform_centered_coefficient':'60','excitation_gap_over_alpha':'103/40',
        'energy_shift_coefficient':'6250/169','projector_shift_coefficient':'20000/1339',
        'margin_polynomial':[str(x) for x in poly],'bernstein_coefficients':[str(x) for x in bern],
        'energy_derivative_fixture':str(ep),'ground_projection_derivative_fixture':enc(GP),
        'wrong_centering_secular_matrix':enc(wrong),'relative_error_proved':False,
        'continuum_proved':False,'fixture_scope':'rational block algebra; not an SU2 cutoff'},
        {'whole_interval_margin_proved':True,'ground_ground_cancellation_checked':True,
         'common_ground_assumption_rejected':True,'missing_centering_rejected':True,
         'missing_initial_projection_rejected':True,'missing_leakage_budget_rejected':True,
         'relative_ratio_inference_rejected':True,'spectral_derivative_identities_checked':True})


if __name__=='__main__': main()
