#!/usr/bin/env python3
"""O1 independent connected-word majorant and exact cross-star controls."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from fractions import Fraction as Q
from math import factorial
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
CONTRACT=ROOT/'research/round22/contracts/o1.json'
CONTRACT_HASH='4e6385405be66cec6c91c28108006f4106372e66a280103d22567ad574982004'
STAR=frozenset(((0,0,0),(1,0,0),(0,1,0),(0,0,1)))
TAU0=Q(5,1664)
C_REMAINDER=Q(1970176,5)


def need(ok,message):
    if not ok: raise RuntimeError(message)


def sha(path):
    need(path.is_file(),'missing input: '+str(path))
    for p in (path,*path.parents): need(not p.is_symlink(),'symlink input: '+str(p))
    return hashlib.sha256(path.read_bytes()).hexdigest()


def addv(a,b): return tuple(x+y for x,y in zip(a,b))
def subv(a,b): return tuple(x-y for x,y in zip(a,b))
def star(b): return frozenset(addv(b,s) for s in STAR)


def word_controls():
    differences={subv(a,b) for a in STAR for b in STAR}
    need(len(differences)==13,'star overlap translation count')
    words=[((0,0,0),STAR)]
    rows=[]
    # Histories are retained as separate records even when their union agrees.
    unions=[STAR]
    for n in range(4):
        count=len(unions)
        translated_weight=sum(len(y)*2**len(y) for y in unions)
        count_bound=13**n*factorial(n)
        weight_bound=16*(4+3*n)*104**n*factorial(n)
        need(count<=count_bound and translated_weight<=weight_bound,'ordered connected word majorant')
        need(all(len(y)<=4+3*n for y in unions),'generated support size')
        rows.append({'order':n,'relative_ordered_candidates':count,'candidate_count_upper':count_bound,
                     'rooted_translation_weight_sum':translated_weight,'rooted_weight_upper':weight_bound,
                     'largest_support':max(map(len,unions))})
        if n<3:
            next_unions=[]
            for y in unions:
                candidates={subv(v,s) for v in y for s in STAR}
                need(len(candidates)<=13*(n+1),'one insertion anchor count')
                next_unions.extend(y|star(b) for b in sorted(candidates))
            unions=next_unions
    b1,b2=(1,0,0),(2,0,0)
    need(not STAR & star(b2) and bool((STAR|star(b1)) & star(b2)),'generated-support chain control')
    need(len(STAR|star(b1)|star(b2))==10,'second insertion support growth')
    cube=set(itertools.product(range(4),repeat=3))
    anchors=[b for b in cube if star(b)<=cube]
    overlaps={x:sum(x in star(b) for b in anchors) for x in cube}
    need(max(overlaps.values())==4 and overlaps[(1,1,1)]==4,'full diagonal overlap factor')
    return {'outcome':'incomplete multiplicity and fixed-support counts rejected','rows':rows,
            'star_difference_set':[list(x) for x in sorted(differences)],
            'second_generator_disjoint_from_base':True,'second_generator_meets_generated_support':True,
            'generated_chain_support_size':10,'interior_site_overlap':4,
            'controls':['independent_nonoverlapping_rotations','four_site_support_at_all_orders',
                        'missing_ordered_multiplicity','omitted_root_translation_factor','diagonal_overlap_one']}


def majorant(tau):
    if type(tau) is not Q or abs(tau)>=Q(5,832):
        raise ValueError('rational tau inside the strict majorant radius required')
    t=abs(tau); z=Q(832,5)*t
    return 16*Q(37,5)*t*z*(7-4*z)/(1-z)**2


def scalar_controls():
    need(Q(4,5)**2>Q(7,12),'rational norm enclosure')
    need(Q(832,5)*TAU0==Q(1,2),'explicit interval endpoint')
    need(16*Q(37,5)*20*Q(832,5)==C_REMAINDER,'evaluated remainder constant')
    rows=[]
    for z in (Q(1,8),Q(1,4),Q(1,2)):
        whole=z*(7-4*z)/(1-z)**2
        cutoff=8
        partial=sum(((4+3*n)*z**n for n in range(1,cutoff+1)),Q())
        tail=z**(cutoff+1)*((4+3*(cutoff+1))/(1-z)+3*z/(1-z)**2)
        need(partial+tail==whole,'exact scalar-series tail identity')
        need(whole<=20*z,'uniform z<=half simplification')
        rows.append({'z':str(z),'sum':str(whole),'partial_order_eight':str(partial),'exact_tail':str(tail)})
    samples=[]
    for tau in (Q(-1,2000),Q(0),Q(1,2000),TAU0):
        bound=majorant(tau)
        need(bound<=C_REMAINDER*tau*tau,'uniform quadratic bound')
        samples.append({'tau':str(tau),'scalar_majorant':str(bound),'quadratic_upper':str(C_REMAINDER*tau*tau)})
    need(C_REMAINDER/Q(2000)<Q(448,2),'first-step upper-budget shrink')
    rejected=[]
    for tau in (True,Q(5,832),Q(-5,832),Q(1)):
        try: majorant(tau)
        except ValueError: rejected.append(str(tau))
        else: raise RuntimeError('invalid series radius admitted')
    return {'outcome':'series radius and scalar bounds checked','series_rows':rows,'tau_rows':samples,
            'tau0':str(TAU0),'quadratic_constant':str(C_REMAINDER),'invalid_radius_inputs_rejected':rejected,
            'first_step_budget_shrink_at_one_over_2000':True,'iterative_contraction_claimed':False}


# Sparse exact matrices have keys (row,column) in the computational basis.
def clean(a): return {k:v for k,v in a.items() if v}
def scale(a,c): return clean({k:c*v for k,v in a.items()})
def plus(a,b):
    out=dict(a)
    for k,v in b.items(): out[k]=out.get(k,Q())+v
    return clean(out)
def minus(a,b): return plus(a,scale(b,-1))
def times(a,b):
    br={}
    for (k,j),v in b.items(): br.setdefault(k,[]).append((j,v))
    out={}
    for (i,k),v in a.items():
        for j,w in br.get(k,[]): out[(i,j)]=out.get((i,j),Q())+v*w
    return clean(out)
def comm(a,b): return minus(times(a,b),times(b,a))
def adj(a): return {(j,i):v for (i,j),v in a.items()}


def local_flip(support,target,amplitude,skew=False,n=7):
    others=sum(1<<i for i in support if i!=target)
    out={}
    for col in range(2**n):
        if col & others: continue
        out[(col^(1<<target),col)]=amplitude*(-1 if skew and col&(1<<target) else 1)
    return out


def spin_control():
    # Physical arrangement is G and e_x+G; bit 1 is their unique common site.
    left,right=(0,1,2,3),(1,4,5,6)
    pb=local_flip(left,0,Q(1,2)); pc=local_flip(right,1,Q(1,2))
    sb=local_flip(left,0,Q(1,2),True); sc=local_flip(right,1,Q(1,4),True)
    phi=plus(pb,pc); x=plus(sb,sc)
    h={(n,n):Q(sum((2 if j==1 else 1) for j in range(7) if n&(1<<j))) for n in range(1,128)}
    need(comm(sb,h)==scale(pb,-1) and comm(sc,h)==scale(pc,-1),'local bounded first commutators')
    need(comm(x,h)==scale(phi,-1),'simultaneous first commutator')
    need(adj(x)==scale(x,-1) and adj(phi)==phi,'skew/self adjoints')
    cross=comm(sb,pc)
    need(cross.get((3,0))==Q(-1,4),'actual cross-star action')
    support_witness=[]
    for bit in range(7):
        fullflip={(col^(1<<bit),col):Q(1) for col in range(128)}
        need(bool(comm(cross,fullflip)),'cross term missing claimed support site')
        support_witness.append(bit)
    r2=scale(comm(x,phi),Q(1,2))
    need(r2.get((0,0))==Q(-3,8) and r2.get((3,0))==Q(-1,16),'second-order retained remainder')
    independent_r2=scale(plus(comm(sb,pb),comm(sc,pc)),Q(1,2))
    need(independent_r2.get((3,0),Q())==0,'cross-star deletion control')
    # H0+Phi has A=Phi,D=0 for this fixture. Higher terms have coefficient n/(n+1)!.
    # ||X||<=3|tau|/4, ||Phi||<=|tau|. For n>=2 use n/(n+1)!<=1/n!.
    tau=Q(1,100); u=Q(3,2)*tau
    exp_upper=1/(1-u) # e^u<=sum u^n for 0<=u<1.
    tail=Q(9,8)*exp_upper*tau**3
    diagonal_upper=Q(-3,8)*tau*tau+tail
    mixing_abs_lower=Q(1,16)*tau*tau-tail
    need(diagonal_upper<0 and mixing_abs_lower>0,'exact remainder tail does not discriminate')
    wrong_first=plus(phi,scale(comm(x,h),-1))
    need(wrong_first==scale(phi,2),'reversed rotation cancellation control')
    return {'outcome':'cross-star deletion, wrong sign and pure-relative residual rejected',
            'fixture_scope':'seven qubits obeying norm/domain lemma hypotheses, not SU2 physical simulation',
            'common_site':1,'nontrivial_commutator_support_sites':support_witness,
            'cross_commutator_vacuum_to_double_coefficient':'-1/4',
            'R_second_order_vacuum_diagonal':'-3/8','R_second_order_vacuum_to_double':'-1/16',
            'tau':str(tau),'higher_order_operator_tail_upper':str(tail),
            'actual_vacuum_diagonal_upper':str(diagonal_upper),'actual_mixing_magnitude_lower':str(mixing_abs_lower),
            'R_vacuum_annihilating':False,'R_pure_relative':False,'scalar_subtraction_repairs_offdiagonal':False,
            'wrong_sign_leaves_twice_first_order_phi':True}


def gap_scope_control():
    # Negative onsite vacuum projectors expose local/global norm distinction.
    r=Q(1,1000); rows=[]
    for size in (1,10,1000):
        local=2*r; global_norm=size*r
        need(global_norm==size*local/2,'extensive global norm')
        if size>2: need(global_norm>local,'local/global norm falsifier')
        tau=Q(1,2000)
        coarse_gap=1-28*tau-2*size*C_REMAINDER*tau*tau
        rows.append({'sites':size,'weighted_local_norm':str(local),'global_operator_norm':str(global_norm),
                     'actual_onsite_control_gap':str(1+r),'unproved_substitution_gap_expression':str(coarse_gap)})
    need(Q(rows[-1]['unproved_substitution_gap_expression'])<0,'volume-deteriorating certificate control')
    return {'outcome':'local norm substitution in global spectral perturbation rejected','rows':rows,
            'actual_gap_failure_claimed':False,'numerical_model_stability_threshold_proved':False,
            'missing':'support-indexed iterative vacuum removal with domain, weight and inverse-gap control'}


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',required=True)
    args=parser.parse_args(); out=Path(args.output).absolute()
    for p in (out,*out.parents): need(not p.is_symlink(),'symlink output')
    need(not out.exists(),'fresh output directory required')
    need(sha(CONTRACT)==CONTRACT_HASH,'frozen contract changed')
    contract=json.loads(CONTRACT.read_text())
    for rel,expected in contract['dependencies'].items(): need(sha(ROOT/rel)==expected,'dependency changed: '+rel)
    controls={'schema':'ym22-reverse-o1-controls-v1','loop':'o1','direction':'reverse','status':'passed','passed':True,
              'connected_words':word_controls(),'scalar_majorant':scalar_controls(),
              'cross_star_and_remainder':spin_control(),'gap_inference':gap_scope_control()}
    results={'schema':'ym22-reverse-o1-results-v1','loop':'o1','direction':'reverse',
             'status':'proved_remainder_gap_limited','passed':True,
             'claims':{'simultaneous_rotation_preserves_operator_domain':True,'unbounded_H0_norm_series_used':False,
                       'first_commutator':'[X,H0]=-sum A_b','star_overlap_translates':'13','site_star_overlap':'4',
                       'relative_ordered_word_count_upper':'13^n*n!','generated_support_upper':'4+3*n',
                       'rooted_weighted_commutator_upper':'16*(4+3*n)*(208*s)^n*n!*sup_norm_K',
                       'remainder_majorant':'16*(v+a/2)*z*(7-4*z)/(1-z)^2; z=208*s',
                       'series_radius_tau_open':'5/832','quadratic_interval_tau_closed':str(TAU0),
                       'quadratic_remainder_constant':str(C_REMAINDER),'diagonal_relative_coefficient':'28*abs(tau)',
                       'first_step_upper_budget_shrink_interval':'abs(tau)<=1/2000',
                       'iterative_contraction_proved':False,'numerical_homogeneous_gap_proved':False,
                       'remainder_automatically_vacuum_annihilating':False,'infinite_global_unitary_proved':False},
             'target_verdict':'Explicit volume-uniform one-step remainder proved; numerical homogeneous stability remains limited.',
             'next_loop_selected':False}
    rels=list(contract['dependencies'])+contract['instruction_inputs']+[
        'research/round21/reverse/i1/report.md','research/round21/reverse/i2/report.md',
        'research/round21/reverse/i2/source-review.json',
        'research/round22/reverse/n1/inputs/advisor-admission-matching.md',
        'research/round22/reverse/n1/inputs/paired-admission-matching.md']
    inputs=[CONTRACT,HERE/'report.md',HERE/'check.py',HERE/'source-review.json',HERE/'independence.json']+[ROOT/p for p in rels]
    hashes={str(p.relative_to(ROOT)):sha(p) for p in sorted(set(inputs))}
    out.mkdir(parents=True)
    for name,payload in [('results.json',results),('controls.json',controls)]:
        (out/name).write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
    manifest={'schema':'ym22-source-manifest-v1','inputs':hashes,
              'outputs':{name:sha(out/name) for name in ('results.json','controls.json')}}
    (out/'source-manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'loop':'o1','direction':'reverse','status':'proved_remainder_gap_limited','passed':True}))


if __name__=='__main__': main()
