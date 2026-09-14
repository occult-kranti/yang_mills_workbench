#!/usr/bin/env python3
"""N2 independent exact geometry and controlled protocol checks."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
CONTRACT=ROOT/'research/round22/contracts/n2.json'
CONTRACT_HASH='a2b0fd55d55a393dc0d70911fa91819f75576211be68d83766c53f5357511db8'


def need(value,message):
    if not value:
        raise RuntimeError(message)


def sha(path):
    need(path.is_file(),'required input absent: '+str(path))
    for p in (path,*path.parents):
        need(not p.is_symlink(),'symlink source: '+str(p))
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_inputs(q,L):
    if type(q) is not Q or not 0<q<1 or type(L) is not int or L<1:
        raise ValueError('q must be rational in (0,1), L a positive non-Boolean integer')


def total_budget(q):
    check_inputs(q,1)
    return (2+5*q+5*q*q+6*q**3+3*q**4)/(24*(1-q)**3*(1+q)**2*(1+q*q))


def factor(q,L):
    check_inputs(q,L)
    return (1-q**(4*L))*(1-q**(2*L))*(1-q**L)


def finite_sum(q,L):
    check_inputs(q,L)
    def s(q,n):
        return sum((q**j for j in range(n)),Q())
    return (3*s(q,4*L)*s(q,2*L)*s(q,L)-(1+q+q*q)*s(q**4,L)*s(q*q,L)*s(q,L))/24


def shift(v,a):
    out=list(v); out[a]+=1
    return tuple(out)


def edge(v,a):
    return (v,shift(v,a))


def square(v,a,b):
    return frozenset((edge(v,a),edge(v,b),edge(shift(v,a),b),edge(shift(v,b),a)))


def is_selected(v,a,b):
    return (a,b)==(0,1) and v[0]%4<3 and v[1]%2==0


def geometry(L):
    vertices=set(itertools.product(range(4*L),range(2*L),range(L)))
    owned={edge(v,a) for v in vertices for a in range(3)}
    independently_owned=set()
    strips=[]
    for i,j,k in itertools.product(range(L),repeat=3):
        block={edge((4*i+r,2*j+s,k),a) for r in range(4) for s in range(2) for a in range(3)}
        strip={edge((4*i+r,2*j+s,k),0) for r in range(3) for s in range(2)} | {edge((4*i+r,2*j,k),1) for r in range(4)}
        need(len(block)==24 and len(strip)==10 and strip<=block,'complete block factors')
        need(not independently_owned & block,'nonunique tail owner')
        independently_owned.update(block); strips.append(strip)
    need(independently_owned==owned and len(owned)==24*L**3,'tail-block union')
    clipped={e for e in owned if e[1] in vertices}
    need(len(owned)-len(clipped)==14*L*L,'outgoing-link count')
    incident={}; clipped_incident={}; contained={}
    # Enumerate one extra positive layer; faces based there must not meet owned links.
    for v in itertools.product(range(4*L+1),range(2*L+1),range(L+1)):
        for a,b in ((0,1),(0,2),(1,2)):
            edges=square(v,a,b)
            need(bool(edges & owned)==(v in vertices),'all-L incidence characterization fixture')
            if is_selected(v,a,b):
                continue
            key=(a,b,*v)
            if edges & owned: incident[key]=edges
            if edges & clipped: clipped_incident[key]=edges
            if edges<=owned: contained[key]=edges
    need(len(incident)==21*L**3,'incident omitted count')
    need(len(contained)==21*L**3-28*L**2+7*L,'contained-only count')
    need(set(contained)<set(incident) and set(clipped_incident)<set(incident),'boundary controls were vacuous')
    # Each factor is complete despite vertex heads outside the selected rectangle.
    need(all(len(strip & owned)==10 for strip in strips),'cut selected factor')
    weights=[]
    for q in (Q(1,2),Q(3,4)):
        direct=sum((q**sum(f[2:])/24 for f in incident),Q())
        clipped_weight=sum((q**sum(f[2:])/24 for f in clipped_incident),Q())
        inside_weight=sum((q**sum(f[2:])/24 for f in contained),Q())
        need(direct==finite_sum(q,L)==total_budget(q)*factor(q,L),'independent exact weighted face sum')
        need(inside_weight<direct and clipped_weight<direct<total_budget(q),'wrong budget control')
        weights.append({'q':str(q),'D_L':str(direct),'D_clipped_links':str(clipped_weight),
                        'D_contained_faces':str(inside_weight),'infinite_budget':str(total_budget(q)),
                        'F_L':str(factor(q,L))})
    return {'L':L,'owned_links':len(owned),'clipped_links':len(clipped),'complete_strip_count':len(strips),
            'free_factors':14*L**3,'omitted_incident_faces':len(incident),
            'omitted_contained_faces':len(contained),'clipped_incident_faces':len(clipped_incident),
            'crossing_face_witness':list(sorted(set(incident)-set(contained))[0]),'weights':weights}


def exp_negative_bounds(x,n=48):
    # Taylor remainder: derivative magnitude of exp(-x) on [0,x] is at most one.
    term=Q(1); partial=term
    for j in range(1,n+1):
        term*= -x/j; partial+=term
    error=abs(term)*x/(n+1)
    need(n%2==0,'even truncation needed')
    lower,upper=partial-error,partial
    need(0<lower<upper<1,'exponential enclosure')
    return lower,upper


def log_two_bounds(n=32):
    # log(2)=2 sum x^(2j+1)/(2j+1), x=1/3; geometric positive tail bound.
    x=Q(1,3)
    lower=2*sum((x**(2*j+1)/(2*j+1) for j in range(n)),Q())
    tail=2*x**(2*n+1)/((2*n+1)*(1-x*x))
    need(Q(2,3)<lower<lower+tail<Q(7,10),'logarithm enclosure')
    return lower,lower+tail


def protocols():
    # At epsilon=1/n^2, half-integer beta makes epsilon^-beta an integer.
    rows=[]; ell=Q(3,2)
    for beta in (Q(0),Q(1,2),Q(1),Q(3,2)):
        for n in (2,4):
            eps=Q(1,n*n); raw=ell*n**int(2*beta)
            L=max(1,raw.numerator//raw.denominator)
            if beta==0:
                need(L==1 and Q(L)**3!=ell**3,'fixed-support floor control')
            else:
                need(raw-1<L<=raw,'floor error bound')
            f=factor(1-eps,L)
            # Bernoulli/geometric upper bound and exponential lower bound are proof tools.
            need(0<f<1 and f<=8*L**3*eps**3,'finite product bounds')
            rows.append({'beta':str(beta),'n':n,'ell':str(ell),'L':L,'epsilon_L':str(eps*L),
                         'F_L':str(f),'F_over_8_L_cubed_epsilon_cubed':str(f/(8*L**3*eps**3))})
    regions=[]
    for beta,gamma in ((Q(0),Q(5,2)),(Q(0),Q(3)),(Q(1,2),Q(1)),
                       (Q(1,2),Q(3,2)),(Q(1),Q(0)),(Q(3,2),Q(0))):
        vanishes=beta<1 and gamma<3*(1-beta)
        regions.append({'beta':str(beta),'gamma':str(gamma),'certificate_vanishes':vanishes})
    exps=[exp_negative_bounds(Q(a)) for a in (4,2,1)]
    flo=fhi=Q(1)
    for lo,hi in exps:
        flo*=1-hi; fhi*=1-lo
    need(0<flo<fhi<1,'critical-support certificate is positive')
    critical=[]
    for n in (4,8,16):
        f=factor(1-Q(1,n),n)
        need(f>fhi,'critical finite profile should exceed limiting product')
        critical.append({'q':str(1-Q(1,n)),'L':n,'F_L':str(f)})
    lnlo,lnhi=log_two_bounds()
    logarithmic=[]
    for n in (2,4,8,16):
        eps=Q(1,2**n)
        raw=Q(1,8)*factor(1-eps,1)/eps**3 # eta=1/2, C=1.
        need(0<raw<1,'fixed-L endpoint coefficient fixture')
        logarithmic.append({'minus_log2_epsilon':n,'unshortened_dynamic_certificate':str(raw),
                            'k_one_shortened_lower':str(raw/(n*lnhi)),
                            'k_one_shortened_upper':str(raw/(n*lnlo))})
    # Scalar B=I has exact zero centered correlation for every stationary state.
    for mean_astar in (Q(-2),Q(0),Q(3,7)):
        need(mean_astar-mean_astar*1==0,'identity-observable counterexample')
    return {'floor_and_scale_rows':rows,'certificate_region_rows':regions,
            'critical_ell_one_F_limit_enclosure':{'lower':str(flo),'upper':str(fhi)},
            'critical_profile_rows':critical,'logarithmic_fixed_L_rows':logarithmic,
            'fixed_L_ell_three_halves_actual_L':1,'incorrect_fixed_L_ell_cubed':'27/8',
            'positive_certificate_implies_actual_nonconvergence':False,
            'identity_connected_correlations':'0',
            'outcome':'floor, infinite-budget, endpoint and actual-nonconvergence inferences rejected'}


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',required=True)
    args=parser.parse_args(); out=Path(args.output).absolute()
    for p in (out,*out.parents): need(not p.is_symlink(),'symlink output path')
    need(not out.exists(),'fresh output directory required')
    need(sha(CONTRACT)==CONTRACT_HASH,'frozen contract mismatch')
    contract=json.loads(CONTRACT.read_text())
    for p,h in contract['dependencies'].items(): need(sha(ROOT/p)==h,'dependency changed: '+p)
    geometry_rows=[geometry(L) for L in (1,2,3)]
    need(finite_sum(Q(1,2),1)==Q(107,384),'named finite fixture')
    rejected=[]
    for label,q,L in [('q0',Q(0),1),('q1',Q(1),1),('q_bool',True,1),('L0',Q(1,2),0),('L_bool',Q(1,2),True),('L_fraction',Q(1,2),Q(3,2))]:
        try: factor(q,L)
        except ValueError: rejected.append(label)
        else: raise RuntimeError('invalid input admitted: '+label)
    controls={'schema':'ym22-reverse-n2-controls-v1','loop':'n2','direction':'reverse','status':'passed','passed':True,
              'geometry':{'outcome':'wrong boundaries and infinite-budget substitution rejected','rows':geometry_rows,
                          'controls':['clipping_outgoing_links','omitting_crossing_faces','replacing_finite_by_infinite_budget']},
              'protocols':protocols(),'invalid_inputs_rejected':rejected}
    results={'schema':'ym22-reverse-n2-results-v1','loop':'n2','direction':'reverse','status':'proved_scoped','passed':True,
             'claims':{'owned_links':'24*L^3','complete_strips':'L^3','free_factors':'14*L^3',
                       'omitted_incident_faces':'21*L^3','incident_iff_face_base_in_tail_rectangle':True,
                       'D_L':'B(q)*(1-q^(4L))*(1-q^(2L))*(1-q^L)',
                       'D_L_at_one':'7*L^3/8','tau_D_L':'eta*(1-q^(4L))*(1-q^(2L))*(1-q^L)/8',
                       'normalized_dynamic_certificate':'C*eta*epsilon^(-gamma)*F_L(q)/4',
                       'certificate_vanishing_region':'0<=beta<1 and 0<=gamma<3*(1-beta)',
                       'boundary_beta_zero_limit':'2*C*eta*L0^3','boundary_beta_between_zero_one_limit':'2*C*eta*ell^3',
                       'beta_one_gamma_zero_limit':'C*eta*(1-exp(-4*ell))*(1-exp(-2*ell))*(1-exp(-ell))/4',
                       'beta_above_one_gamma_zero_limit':'C*eta/4',
                       'fixed_L_log_shortened_gamma_three':'all k>0 sufficient',
                       'necessity_scope':'this normalized nonnegative certificate only',
                       'actual_endpoint_nonconvergence_proved':False,'model_changed':False},
             'proof_boundary':'Exact fixtures support an all-L incidence proof and all-q asymptotic derivation; no actual error lower bound.',
             'next_loop_selected':False}
    inputs=[CONTRACT,HERE/'check.py',HERE/'report.md',HERE/'independence.json',HERE/'source-review.json']
    inputs += [ROOT/p for p in contract['dependencies']]
    inputs += [ROOT/p for p in contract['instruction_inputs']]
    inputs += [ROOT/'research/round21/reverse/i1/report.md',ROOT/'research/round22/reverse/n1/report.md',
               ROOT/'research/round22/reverse/n1/source-review.json',ROOT/'research/round22/reverse/n1/inputs/paired-finite-observations.md',
               ROOT/'research/round22/reverse/n1/inputs/advisor-finite-observations.md']
    hashes={str(p.relative_to(ROOT)):sha(p) for p in sorted(set(inputs))}
    out.mkdir(parents=True)
    for name,payload in [('results.json',results),('controls.json',controls)]:
        (out/name).write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
    manifest={'schema':'ym22-source-manifest-v1','inputs':hashes,
              'outputs':{n:sha(out/n) for n in ('results.json','controls.json')}}
    (out/'source-manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'loop':'n2','direction':'reverse','status':'proved_scoped','passed':True,'geometry_fixtures':3}))


if __name__=='__main__': main()
