#!/usr/bin/env python3
"""Exact S2 filter/support controls, separated from all-order operator proofs."""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import math

ROOT=Path(__file__).absolute().parents[4]
BASE='research/round23/forward/s2/'
CONTRACT='research/round23/contracts/s2.json'
CONTRACT_SHA='a339228a20375c197f01901e34806fd827cc22fd1e930b740475c15262cd21c2'

def need(c,m):
    if not c: raise ValueError(m)

def digest(p):
    for x in (p,*p.parents): need(not x.is_symlink(),'symlink rejected')
    need(p.is_file(),'missing source '+str(p))
    return hashlib.sha256(p.read_bytes()).hexdigest()

def save(p,x): p.write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
def zero(n): return [[F(0) for j in range(n)] for i in range(n)]
def scale(c,a): return [[c*x for x in row] for row in a]
def add(a,b): return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def mm(a,b): return [[sum((a[i][k]*b[k][j] for k in range(len(b))),F(0)) for j in range(len(b))] for i in range(len(a))]
def comm(a,b): return add(mm(a,b),scale(-1,mm(b,a)))
def transpose(a): return [list(row) for row in zip(*a)]

def integral_monomial(k,theta): return theta**(k+1)/F(k+1)
def triangle_monomial(k,theta):
    return integral_monomial(k,theta)-integral_monomial(k+1,theta)/theta

def sinc_poly(omega,theta,N):
    return sum(((-1)**k*(omega*theta)**(2*k)/F(math.factorial(2*k+1)) for k in range(N+1)),F(0))

def ell_integrated_poly(omega,theta,N):
    return sum((F((-1)**j,math.factorial(2*j+1))*omega**(2*j+1)*triangle_monomial(2*j+1,theta)
                for j in range(N)),F(0))

def filter_controls():
    theta=F(1,16); N=7
    energies=[F(0),F(1),F(3)]
    A=[[F(1),F(2),F(-1)],[F(2),F(0),F(3)],[F(-1),F(3),F(2)]]
    G=zero(3)
    for j,e in enumerate(energies): G[j][j]=e
    L=zero(3); R=zero(3); max_tail=F(0)
    for i in range(3):
        for j in range(3):
            omega=energies[i]-energies[j]
            L[i][j]=ell_integrated_poly(omega,theta,N)*A[i][j]
            R[i][j]=sinc_poly(omega,theta,N)*A[i][j]
            need(-omega*L[i][j]==-A[i][j]+R[i][j],'integrated filter commutator sign/coefficient')
            x=abs(omega*theta)
            tail=x**(2*N+2)/F(math.factorial(2*N+3))
            max_tail=max(max_tail,tail*abs(A[i][j]))
            if omega:
                need(L[i][j]==((1-sinc_poly(omega,theta,N))/omega)*A[i][j],'direct frequency versus independent polynomial integration')
            else:
                need(L[i][j]==0 and R[i][j]==A[i][j],'zero frequency retained exactly')
    need(comm(L,G)==add(scale(-1,A),R),'whole matrix commutator')
    need(transpose(L)==scale(-1,L) and transpose(R)==R,'skew and symmetric exact controls')
    need(comm(scale(-1,L),G)!=add(scale(-1,A),R),'wrong overall sign rejected')
    need(comm(L,G)!=scale(-1,A),'omitted residual rejected')
    need(max_tail<F(1,10**25),'explicit alternating-series arithmetic error')
    # Exact resonance fixture; it is not a physical SU2 spectrum.
    resonance_energies=[F(0),F(1),F(1)]
    omega=resonance_energies[1]-resonance_energies[2]
    need(sinc_poly(omega,theta,N)==1 and ell_integrated_poly(omega,theta,N)==0,'gapped resonance survives')
    # Directed rational enclosure of one genuine nonzero fixture frequency.
    lo=sinc_poly(F(1),theta,7); hi=sinc_poly(F(1),theta,8)
    need(F(0)<lo<hi<F(1),'strict controlled nonzero-frequency enclosure')
    need(lo!=hi,'finite truncation not passed off as exact sinc')
    return {'theta_fixture':str(theta),'sinc_one_interval':[str(lo),str(hi)],
            'max_matrix_sinc_tail_upper':str(max_tail),'polynomial_order':14,
            'retained_resonance_multiplier':'1','resonance_generator_multiplier':'0',
            'matrix_scope':'rational algebra fixture, not actual SU2 spectral data'}

S=frozenset(((0,0,0),(1,0,0),(0,1,0),(0,0,1)))
def star(b): return frozenset(tuple(x+y for x,y in zip(b,s)) for s in S)
def support_controls():
    anchors=[(0,1,1),(1,1,1),(2,1,1),(1,2,1),(2,2,1)]
    stars=[star(b) for b in anchors]
    states=[((j,),stars[j]) for j in range(len(stars))]
    counts=[]; maxima=[]
    previous=F(64) # r*=M=1 normalization of coefficient fixture
    reset_lost=0
    for n in range(4):
        sums={}
        for word,Y in states:
            need(len(Y)<=4+3*n,'connected support all-depth size')
            for root in Y: sums[root]=sums.get(root,F(0))+F(2**len(Y))*2**n
        actual=max(sums.values())
        major=F(64)
        for k in range(n): major*=64*(8+3*k)
        need(actual<=major,'root coefficient majorant')
        if n: need(actual<=64*(8+3*(n-1))*previous,'single recurrence fixture')
        previous=actual
        counts.append(len(states)); maxima.append(str(actual))
        if n<3:
            extended=[]
            for word,Y in states:
                for j,Z in enumerate(stars):
                    if Y&Z:
                        extended.append((word+(j,),Y|Z))
                        if not stars[word[0]]&Z: reset_lost+=1
            states=extended
    need(reset_lost>0,'restricting all later stars to seed loses connected words')
    # Ordered words including repetitions have different multiplicity from sets.
    need(any(len(set(word))<len(word) for word,Y in states),'repeated anchors retained')
    need(len(states)>len({tuple(sorted(set(word))) for word,Y in states}),'set grouping loses indexed multiplicity')
    need(not (stars[0]&stars[2]) and (stars[0]|stars[1])&stars[2],'concrete outer-only-generated-support witness')
    # Different nested orderings can be different operators.
    A=[[F(0),F(1),F(0)],[F(1),F(0),F(0)],[F(0),F(0),F(0)]]
    D1=[[F(1),F(0),F(0)],[F(0),F(0),F(1)],[F(0),F(1),F(0)]]
    D2=[[F(0),F(0),F(1)],[F(0),F(2),F(0)],[F(1),F(0),F(0)]]
    need(comm(D1,comm(D2,A))!=comm(D2,comm(D1,A)),'ordered commutator control discriminates')
    return {'word_counts_depth0_to3':counts,'root_sums_depth0_to3':maxima,
            'seed_reset_lost_extensions':reset_lost,'retained_repetitions':True}

def coefficient_controls():
    theta=F(1,16)
    rows=[]
    for n in range(7):
        by_integration=triangle_monomial(n,theta)/math.factorial(n)
        compact=theta**(n+1)/math.factorial(n+2)
        residual=integral_monomial(n,theta)/(theta*math.factorial(n))
        need(by_integration==compact,'exact triangular simplex coefficient')
        need(residual==theta**n/math.factorial(n+1),'exact residual simplex coefficient')
        need(by_integration!=integral_monomial(n,theta)/math.factorial(n),'omitting triangular taper changes coefficients')
        rows.append({'n':n,'generator_factor':str(compact),'residual_factor':str(residual)})
    M=F(35,1664); x=192*M*theta
    need(x==F(105,416) and x<1,'frozen all-order radius')
    rational_envelope=(1-x)**-3
    need(rational_envelope==F(416,311)**3,'rational envelope')
    # Binomial coefficients obey the derived ODE; no numerical function fit.
    p=F(8,3); b=F(1)
    for n in range(10):
        next_b=b*(p+n)/F(n+1)
        need((n+1)*next_b==(n+p)*b,'all-order binomial recurrence coefficient fixture')
        b=next_b
    # Positive coefficient series at x>1 cannot be integrated as convergent.
    wrong_x=F(2); ratio=wrong_x*(p+20)/21
    need(ratio>1 and wrong_x>1,'out-of-radius positive majorant rejected')
    return {'x_max':str(x),'weight':'2^support_size','p':'8/3',
            'rational_envelope':str(rational_envelope),'filter_simplex_coefficients':rows,
            'outside_radius_term_ratio_fixture':str(ratio)}

def main():
    p=argparse.ArgumentParser(); p.add_argument('--output',required=True)
    out=Path(p.parse_args().output)
    need(out.is_absolute() and not out.exists(),'fresh absolute output required')
    need(digest(ROOT/CONTRACT)==CONTRACT_SHA,'frozen contract hash')
    con=json.loads((ROOT/CONTRACT).read_text())
    for name,h in con['dependencies'].items(): need(digest(ROOT/name)==h,'changed inherited dependency '+name)
    names=set(con['dependencies'])|set(con['instruction_inputs'])|{
        CONTRACT,BASE+'check.py',BASE+'report.md',BASE+'source-notes.md',
        'research/round23/forward/s1/source-notes.md','research/round23/skeptic/s1.md'}
    inputs={name:digest(ROOT/name) for name in sorted(names)}
    freq=filter_controls(); supports=support_controls(); coefficients=coefficient_controls()
    rejected=[]
    for label,value in [('theta_zero',F(0)),('theta_negative',F(-1)),('theta_above_cap',F(1,8))]:
        try: need(0<value<=F(1,16),'Theta outside frozen interval')
        except ValueError: rejected.append(label)
        else: raise ValueError('invalid Theta admitted')
    for label,value in [('energy_reference',F(0)),('hbar',F(0)),('alpha_over_reference',F(0))]:
        try: need(value>0,'positive physical scale required')
        except ValueError: rejected.append(label)
        else: raise ValueError('invalid physical scale admitted')
    zero_source=F(4,3)**2*F(7,12)**3*F(0)**6
    need(zero_source==0,'actual cubic source zero exception')
    need(F(-1,4096)**6==F(1,4096)**6,'coupling-sign source-norm symmetry')
    results={'schema':'ym23-producer-results-v1','loop':'s2','direction':'forward','status':'proved_regulated_identity_connected_certificate','passed':True,
             'target_verdict':'accepted_regulated_only','full_source_identity':'[L_Theta,G]=-A+R_Theta',
             'residual_multiplier':'sinc(omega*Theta)','resonance_retained':True,
             'source_operator':'actual S1 generated source tensor exterior identity',
             'graph_domain_preserved':True,'connected_weight':'2^support_size',
             'infinite_R2_identification':'proved_by_absolute_form_tail_strong_resolvent_and_local_Dyson_limits',
             'unregulated_inverse_proved':False,'homogeneous_gap_proved':False,
             'frequency_controls':freq,'support_controls':supports,'coefficient_controls':coefficients,
             'next_missing_premise':'actual source low-frequency control and a regulator-removal certificate'}
    controls={'schema':'ym23-producer-controls-v1','loop':'s2','direction':'forward','status':'exact_controls_passed','passed':True,
              'wrong_filter_sign_rejected':True,'missing_residual_rejected':True,'equal_energy_residual_retained':True,
              'wrong_triangle_or_simplex_coefficient_rejected':True,'ordered_multiplicity_loss_rejected':True,
              'seed_support_reset_rejected':True,'out_of_radius_positive_series_rejected':True,
              'zero_source_valid_exception':True,'coupling_sign_symmetry_preserved':True,
              'truncation_error_retained':True,'rejected_parameters':rejected,
              'matrix_fixture_is_not_actual_SU2_obstruction':True}
    out.mkdir(parents=True); save(out/'results.json',results); save(out/'controls.json',controls)
    save(out/'source-manifest.json',{'schema':'ym23-producer-source-manifest-v1','loop':'s2','direction':'forward',
         'inputs':inputs,'outputs':{n:digest(out/n) for n in ['results.json','controls.json']}})
    print(json.dumps({'passed':True,'loop':'s2','direction':'forward','target_verdict':'accepted_regulated_only','output':str(out)},sort_keys=True))

if __name__=='__main__': main()
