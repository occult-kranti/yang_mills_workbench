#!/usr/bin/env python3
"""Exact O1 local-majorant and rejecting controls; not a lattice gap proof."""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import itertools
import json
import math

ROOT=Path(__file__).absolute().parents[4]
BASE='research/round22/forward/o1/'
CONTRACT='research/round22/contracts/o1.json'
CONTRACT_SHA='4e6385405be66cec6c91c28108006f4106372e66a280103d22567ad574982004'
INPUTS=[CONTRACT,
 'research/round22/methods/team-protocol.md',
 'research/round22/methods/AGENTS-at-selection.md',
 'research/round22/methods/paired-physics-research-at-selection.md',
 'research/round21/advisor/i1-gate.json','research/round21/advisor/i2-gate.json',
 'research/round22/advisor/homogeneous-source-preparation.json',
 'research/round22/advisor/n2-decision.md','research/round22/advisor/n2-gate.json',
 'research/round22/skeptic/n2.md',
 'research/round21/forward/i1/report.md','research/round21/forward/i2/report.md',
 BASE+'report.md',BASE+'source-notes.md',BASE+'check.py']


def need(ok,message):
    if type(ok) is not bool or not ok:
        raise ValueError(message)


def safe(path):
    for p in [path.absolute(),*path.absolute().parents]:
        need(not p.is_symlink(),'symlink component rejected')


def sha(path):
    safe(path)
    need(path.is_file(),'missing source: '+str(path))
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path,data):
    path.write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')


S={(0,0,0),(1,0,0),(0,1,0),(0,0,1)}


def star(b):
    return frozenset(tuple(x+y for x,y in zip(b,s)) for s in S)


def matrix(n):
    return [[F(0) for _ in range(n)] for _ in range(n)]


def eye(n):
    a=matrix(n)
    for i in range(n):
        a[i][i]=F(1)
    return a


def mm(a,b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))),F(0))
             for j in range(len(b[0]))] for i in range(len(a))]


def add(a,b):
    return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]


def scale(c,a):
    return [[c*x for x in row] for row in a]


def comm(a,b):
    return add(mm(a,b),scale(-1,mm(b,a)))


def kron(a,b):
    return [[a[i][j]*b[k][l] for j in range(len(a[0])) for l in range(len(b[0]))]
            for i in range(len(a)) for k in range(len(b))]


def encode(a):
    return [[str(x) for x in row] for row in a]


def checks():
    controls=[]
    def control(name,ok,outcome):
        need(ok,'failed control: '+name)
        controls.append({'name':name,'passed':True,'outcome':outcome})

    differences={tuple(x-y for x,y in zip(a,b)) for a in S for b in S}
    need(len(differences)==13,'four-star overlap displacement count')
    anchors=list(itertools.product(range(2),repeat=3))
    stars={b:star(b) for b in anchors}
    all_sites=set().union(*stars.values())
    membership={x:sum(x in sb for sb in stars.values()) for x in all_sites}
    need(max(membership.values())==4,'full site overlap multiplicity')
    words=[((b,),sb) for b,sb in stars.items()]
    rows=[]
    prior=None
    recurrence_majorant=F(64)
    for n in range(4):
        per_site={x:0 for x in all_sites}
        for ordered,Y in words:
            need(len(Y)<=4+3*n,'generated-support growth')
            for x in Y:
                per_site[x]+=2**len(Y)*2**n  # s=b=1 triangle majorants
        norm=max(per_site.values())
        need(norm<=recurrence_majorant,'all-word recurrence majorant')
        if prior is not None:
            need(norm<=64*(8+3*(n-1))*prior,'direct recurrence check')
        unique_supports=len({Y for _,Y in words})
        rows.append({'depth':n,'ordered_word_count':len(words),
                     'distinct_declared_supports':unique_supports,
                     'max_support_size':max(len(Y) for _,Y in words),
                     'weighted_triangle_norm_s_b_one':norm,
                     'proved_recurrence_majorant':str(recurrence_majorant)})
        prior=norm
        if n<3:
            words=[(ordered+(b,),Y|sb) for ordered,Y in words
                   for b,sb in stars.items() if Y & sb]
            recurrence_majorant*=64*(8+3*n)
    control('ordered_words_not_unordered_support_sets',
            rows[2]['ordered_word_count']>rows[2]['distinct_declared_supports'],rows)
    Y=stars[(0,0,0)]|stars[(1,0,0)]
    control('fixed_four_site_support_rejected',len(Y)==7 and 2**len(Y)>2**4,
            {'union_sites':[list(x) for x in sorted(Y)],'correct_weight':128,'wrong_weight':16})
    control('diagonal_overlap_one_rejected',max(membership.values())==4,
            {'max_stars_containing_site':4,'relative_coefficient_per_abs_tau':28,
             'incorrect_single_star_coefficient':7})

    # Two overlapping rank-two pair dressings on three qubits, h_i=|1><1|.
    pa=matrix(4); pa[0][3]=pa[3][0]=F(1)
    sa=matrix(4); sa[3][0]=F(1,2); sa[0][3]=F(-1,2)
    p12,p23=kron(pa,eye(2)),kron(eye(2),pa)
    s12,s23=kron(sa,eye(2)),kron(eye(2),sa)
    h=matrix(8)
    for i in range(8):
        h[i][i]=F(i.bit_count())
    need(comm(s12,h)==scale(-1,p12),'pair one commutator cancellation')
    need(comm(s23,h)==scale(-1,p23),'pair two commutator cancellation')
    cross=add(comm(s12,p23),comm(s23,p12))
    need(cross!=matrix(8),'cross-star commutator nonzero')
    qx=[[F(0),F(1)],[F(1),F(0)]]
    support_nontrivial=[]
    for site in range(3):
        probe=[[F(1)]]
        for j in range(3):
            probe=kron(probe,qx if site==j else eye(2))
        support_nontrivial.append(comm(cross,probe)!=matrix(8))
    control('cross_star_terms_and_generated_support_retained',all(support_nontrivial),
            {'cross_matrix':encode(cross),'acts_nontrivially_on_all_three_sites':support_nontrivial,
             'scope':'rank-two lemma fixture; not a full-link SU2 simulation'})

    # One-spin exact formal coefficients through total order four.
    h1=[[F(0),F(0)],[F(0),F(1)]]
    phi1=[[F(0),F(1)],[F(1),F(0)]]
    s1=[[F(0),F(-1)],[F(1),F(0)]]
    need(comm(s1,h1)==scale(-1,phi1),'correct first-order sign')
    ad=phi1; coeffs=[]
    for n in range(1,4):
        ad=comm(s1,ad)
        coeffs.append(scale(F(1,math.factorial(n))-F(1,math.factorial(n+1)),ad))
    need(coeffs[0][0][0]==-1,'quadratic vacuum mean')
    need(coeffs[1][0][1]==F(-4,3),'cubic vacuum mixing survives scalar subtraction')
    control('remainder_is_not_pure_relative_or_only_scalar',
            coeffs[0][0][0]!=0 and coeffs[1][0][1]!=0,
            {'order_2':encode(coeffs[0]),'order_3':encode(coeffs[1]),'order_4':encode(coeffs[2]),
             'scope':'exact Taylor coefficients; report proves actual-model nonzero mean separately'})
    t=F(1,10)
    original=add(h1,scale(t,phi1))
    determinant=original[0][0]*original[1][1]-original[0][1]*original[1][0]
    control('deleting_remainder_changes_spectrum',determinant==F(-1,100),
            {'original_and_exact_unitary_determinant':str(determinant),
             'H0_plus_first_diagonal_only_determinant':'0'})
    control('wrong_rotation_sign_rejected',
            add(phi1,comm(scale(-1,s1),h1))==scale(2,phi1),
            'reversed conjugation doubles the first-order vacuum mixing')

    C=F(64*14*37*768,25)
    tau0=F(5,1536)
    need(C==F(25460736,25),'evaluated quadratic constant')
    need(F(768,5)*tau0==F(1,2),'explicit majorant interval')
    need(C/F(4096**2)==F(777,12800),'numerical interior remainder')
    need(C/F(2**22)==F(777,3200)<F(1,4),'small scalar remainder ratio')
    coeff=F(1)
    scalar_rows=[]
    for n in range(1,9):
        coeff*=F(3*(n-1)+8,3*n)
        need(coeff<=F((n+1)*(n+2),2),'generalized-binomial majorant')
        scalar_rows.append({'n':n,'binomial_exponent_8_over_3_coefficient':str(coeff),
                            'integer_exponent_3_coefficient':str(F((n+1)*(n+2),2))})
    for r in [F(0),F(1,4),F(1,2)]:
        left=14*r*(1-r)**3-(1-(1-r)**3)
        factored=r*(1-2*r)*(7*r*r-17*r+11)
        need(left==factored and left>=0,'rational factorization of 14r upper bound')
    control('majorant_threshold_is_not_a_gap_threshold',True,
            {'series_sufficient_tau0':str(tau0),'quadratic_constant':str(C),
             'actual_numerical_gap_interval':'not_proved','small_remainder_ratio': '777/3200',
             'missing':'closed generated-support vacuum-mixing iteration and uniform inverse estimates'})
    eps=F(1,1000); volume=2000
    control('local_norm_is_not_global_operator_norm',
            2*eps<F(1,2) and volume*eps>F(1,2),
            {'example':'R=epsilon sum_x I_x','weighted_local_norm':str(2*eps),
             'global_norm':str(volume*eps),'volume':volume,
             'actual_gap_change':'0; this is a failed norm inference, not gap failure'})
    # Local rank-one smoothing leaves an exterior vector outside D(H_ext).
    exterior=[]
    for n in [4,16]:
        vnorm=sum((F(1,k*k) for k in range(1,n+1)),F(0))
        hnorm=sum((F(k*k,k*k) for k in range(1,n+1)),F(0))
        need(vnorm<2 and hnorm==n,'exterior domain counterexample')
        exterior.append({'N':n,'vector_norm_squared':str(vnorm),'energy_image_norm_squared':str(hnorm)})
    control('local_rotation_does_not_smooth_arbitrary_exterior_vectors',True,
            {'w_n':'1/n','H_ext_e_n':'n e_n','exact_partial_sums':exterior,
             'correct_statement':'S_b preserves D(H0), not a map of the whole Hilbert space into D(H0)'})
    rejected=0
    for bad in [False,'passed']:
        try:
            need(bad,'intentional rejection')
        except ValueError:
            rejected+=1
    control('optimized_mode_retains_strict_admission',rejected==2,
            'False and truthy non-Boolean statuses rejected by explicit exceptions')

    results={'schema':'ym22-forward-o1-results-v1','loop':'o1','direction':'forward',
     'status':'limited','passed':True,'claims':{
       'finite_volume_domain_preserved':True,'unbounded_H0_norm_series_used':False,
       'rotation_identity':'exp(X)(H0+Phi)exp(-X)=H0+D+R',
       'remainder_series':'sum_n>=1 ad_X^n(Phi)/n!-ad_X^n(A)/(n+1)!',
       'ordered_support_size_bound':'4+3*n','maximum_site_star_overlap':4,
       'maximum_star_overlap_displacements':13,
       'weighted_norm_recurrence':'N_(n+1)<=64*s*(8+3*n)*N_n; N_0<=64*b',
       'scalar_majorant':'64*(M+a0/2)*((1-192*s)^(-8/3)-1)',
       's_bound':'4*abs(tau)/5','relative_diagonal_coefficient':'28*abs(tau)',
       'quadratic_constant':'25460736/25','tau_interval_closed':'abs(tau)<=5/1536',
       'remainder_at_tau_1_over_4096':'777/12800',
       'diagonal_relative_at_tau_1_over_4096':'7/1024',
       'remainder_ratio_at_tau_2_power_minus_22':'777/3200',
       'actual_remainder_pure_relative':False,
       'actual_vacuum_mean_leading':'-tau^2*<U1,H0 U1>, strictly negative coefficient for a nonempty anchor set',
       'numerical_homogeneous_gap_proved':False,'iteration_contraction_proved':False,
       'infinite_global_unitary_or_ITP_transfer_proved':False},
     'finite_connected_word_checks':rows,'scalar_coefficients':scalar_rows,
     'finite_checks_are_infinite_proof':False,'infinite_proof_location':BASE+'report.md',
     'scientific_priority':'unverified'}
    return results,{'schema':'ym22-forward-o1-controls-v1','loop':'o1','direction':'forward',
                    'passed':True,'controls':controls}


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    out=p.parse_args().output.absolute();safe(out)
    need(not out.exists(),'output must be fresh')
    inputs={p:sha(ROOT/p) for p in INPUTS}
    need(len(inputs)==len(INPUTS),'duplicate source')
    need(inputs[CONTRACT]==CONTRACT_SHA,'frozen O1 contract mismatch')
    contract=json.loads((ROOT/CONTRACT).read_text())
    need(contract['status']=='frozen' and contract['loop']=='o1','contract identity')
    for p,h in contract['dependencies'].items():
        need(p in inputs and inputs[p]==h,'dependency mismatch: '+p)
    for p in contract['instruction_inputs']:
        need(p in inputs,'missing frozen instruction input')
    for path,status in [('research/round21/advisor/i1-gate.json','limited'),
                        ('research/round21/advisor/i2-gate.json','limited'),
                        ('research/round22/advisor/n2-gate.json','accepted')]:
        gate=json.loads((ROOT/path).read_text());need(gate['status']==status,'inherited gate status')
        for source,h in inputs.items():
            if source in gate['files']:
                need(gate['files'][source]==h,'admitted source changed: '+source)
    results,controls=checks()
    out.mkdir(parents=True,exist_ok=False)
    save(out/'results.json',results);save(out/'controls.json',controls)
    save(out/'source-manifest.json',{'schema':'ym22-producer-source-manifest-v1',
         'loop':'o1','direction':'forward','inputs':inputs,
         'outputs':{p:sha(out/p) for p in ['results.json','controls.json']},
         'import_policy':'standard-library only; no other producer imports',
         'manifest_self_hash':'bound by submission inventory'})
    print(json.dumps({'loop':'o1','direction':'forward','status':'limited','passed':True,
                      'controls':len(controls['controls'])},sort_keys=True))


if __name__=='__main__':
    main()
