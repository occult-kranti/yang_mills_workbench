#!/usr/bin/env python3
"""O2 exact homological controls and loss-majorant obstruction."""
from __future__ import annotations
import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
CONTRACT=ROOT/'research/round22/contracts/o2.json'
CONTRACT_HASH='86895d53f2e0944ab4c0a93eb969018dd213d9a2a5c27d1107d10e10338e15a6'
INITIAL_C=Q(25460736,25)


def need(ok,message):
    if not ok: raise RuntimeError(message)


def sha(p):
    need(p.is_file(),'required source absent: '+str(p))
    for node in (p,*p.parents): need(not node.is_symlink(),'symlink input')
    return hashlib.sha256(p.read_bytes()).hexdigest()


def mat(rows): return [[Q(x) for x in row] for row in rows]
def mm(a,b): return [[sum((x*y for x,y in zip(row,col)),Q()) for col in zip(*b)] for row in a]
def add(a,b): return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def scale(a,c): return [[c*x for x in row] for row in a]
def minus(a,b): return add(a,scale(b,-1))
def comm(a,b): return minus(mm(a,b),mm(b,a))


def split_control():
    h=mat([[0,0,0],[0,1,0],[0,0,3]])
    residual=scale(mat([[2,1,2],[1,3,-1],[2,-1,-2]]),Q(1,10))
    eye=mat([[1,0,0],[0,1,0],[0,0,1]])
    q=mat([[0,0,0],[0,1,0],[0,0,1]])
    c=residual[0][0]
    a=mat([[0,Q(1,10),Q(1,5)],[Q(1,10),0,0],[Q(1,5),0,0]])
    z=mm(mm(q,minus(residual,scale(eye,c))),q)
    s=mat([[0,Q(-1,10),Q(-1,15)],[Q(1,10),0,0],[Q(1,15),0,0]])
    need(add(add(scale(eye,c),a),z)==residual,'complete scalar-diagonal split')
    need(comm(s,h)==scale(a,-1),'arbitrary-support bare homological equation')
    need(all(row[0]==0 for row in z),'updated diagonal must annihilate vacuum')
    wrong_z=mm(mm(q,residual),q)
    wrong=add(add(scale(eye,c),a),wrong_z)
    need(minus(wrong,residual)==scale(q,c),'double-counted scalar control')
    need(add(a,z)!=residual,'dropped scalar control')
    vnorm=Q(1,10)**2+Q(1,5)**2
    unorm=Q(1,10)**2+Q(1,15)**2
    need(unorm==Q(13,900)<=vnorm==Q(1,20),'bare inverse norm control')
    return {'outcome':'wrong scalar/diagonal bookkeeping rejected','scalar':str(c),
            'v_norm_squared':str(vnorm),'u_norm_squared':str(unorm),
            'correct_Z':[[str(x) for x in row] for row in z],
            'wrong_split_extra':'c*Q','homological_commutator_exact':True,
            'local_bare_inverse_gap_lower':'1'}


def equal_weight_control():
    g={(0,0,0),(1,0,0),(0,1,0),(0,0,1)}
    rows=[]
    for n in (1,2,3,10,100):
        support={(x+i,y,z) for i in range(n) for x,y,z in g}
        m=len(support)
        need(m==3*n+1,'generated union-star cardinality')
        amplitude=Q(1,2**m)
        k_norm=(2**m)*amplitude
        d_norm_upper=4*16*Q(1,64)
        comm_norm=(2**m)*amplitude*m/Q(64)
        homological_comm=(2**m)*(amplitude/m)*m/Q(64)
        need(k_norm==d_norm_upper==1,'equal-weight unit upper norms')
        need(comm_norm==Q(m,64) and homological_comm==Q(1,64),'large-support commutator and inverse cancellation')
        rows.append({'stars':n,'support_sites':m,'K_norm':'1','D_norm_upper':'1',
                     'commutator_weighted_norm_lower':str(comm_norm),
                     'homological_pair_weighted_commutator':str(homological_comm)})
    need(Q(rows[-1]['commutator_weighted_norm_lower'])>1,'equal-weight growth control vacuous')
    return {'outcome':'universal equal-weight bound rejected; structured inverse exception retained',
            'rows':rows,'growth_formula':'(3*N+1)/64','generic_bilinear_constant_exists':False,
            'homological_equal_weight_impossibility_claimed':False}


def retained_d_control():
    d,r=Q(1,100),Q(1,1000000)
    # Exact sine/cosine Taylor inequalities give this all-real small-r enclosure.
    error=(Q(8,3)+Q(2,3)*d)*r**3
    lower,upper=-d*r-error,-d*r+error
    need(upper<-d*r/2<0,'retained D linear term not discriminating')
    need(-upper>r*r,'false unit quadratic-only estimate passed')
    return {'outcome':'dropping retained D and purely quadratic residual recurrence rejected',
            'd':str(d),'r':str(r),'exact_offdiagonal_formula':'r*cos(2*r)-(1+d)*sin(2*r)/2',
            'offdiagonal_lower':str(lower),'offdiagonal_upper':str(upper),
            'error_from_minus_d_r_upper':str(error),'limit_offdiagonal_over_r':'-d',
            'scope':'one-qubit operator lemma control, not the SU2 model'}


def log2_bounds(n=12):
    x=Q(1,3)
    lower=2*sum((x**(2*k+1)/(2*k+1) for k in range(n)),Q())
    upper=lower+2*x**(2*n+1)/((2*n+1)*(1-x*x))
    need(Q(2,3)<lower<upper<Q(7,10),'controlled logarithm enclosure')
    return lower,upper


def step(r,b,loss):
    if any(type(x) is not Q for x in (r,b,loss)) or r<0 or b<0 or loss<=0:
        raise ValueError('nonnegative rational bounds and positive rational loss required')
    if 4*r>=loss: raise ValueError('all-order radius 4r<loss failed')
    u=4*r/loss
    return u/(1-u)*(b+Q(3,2)*r)


def enclosure(x,digits=70):
    unit=10**digits
    n=x.numerator*unit//x.denominator
    lo,hi=Q(n,unit),Q(n+1,unit)
    need(lo<=x<=hi,'rational display enclosure')
    return {'lower':str(lo),'upper':str(hi)}


def recurrence_controls():
    lnlo,lnhi=log2_bounds()
    tau=Q(1,100000000)
    r=INITIAL_C*tau*tau; b=448*tau; a=28*tau
    energy=Q(); initial=(r,b,a)
    rows=[]
    for n in range(4):
        # Lower loss yields a conservative upper recurrence for the exact schedule.
        delta=lnlo/(2*(n+1)*(n+2))
        nr=step(r,b,delta)
        need(0<nr<r and a<1,'explicit early contraction fixture')
        need(delta>4*b+10*r,'exact contraction inequality')
        rows.append({'stage':n,'r_upper_enclosure':enclosure(r),
                     'next_r_upper_enclosure':enclosure(nr),'b_upper_enclosure':enclosure(b),
                     'a_relative_upper_enclosure':enclosure(a),'4r_over_loss_upper_enclosure':enclosure(4*r/delta)})
        energy+=r; b+=2*r; a+=2*r; r=nr
    threshold=Q(7,40)/initial[1]
    stage=0
    while (stage+1)*(stage+2)<threshold: stage+=1
    need(stage==197,'quantified eventual doubling stage')
    delta_upper=Q(7,10)/(2*(stage+1)*(stage+2))
    factor_lower=4*initial[1]/delta_upper
    need(factor_lower>=2,'eventual ratio lower bound')
    need(stage*(stage+1)<threshold,'minimal coarse doubling index')
    # Verify the exact algebraic shrink test and the retained-D difference.
    tests=[]
    for delta in (Q(1,10),Q(1,100),Q(1,1000)):
        rr,bb=Q(1,100000),Q(1,1000)
        value=step(rr,bb,delta)
        need((value<rr)==(delta>4*bb+10*rr),'exact step contraction equivalence')
        need(value-step(rr,Q(),delta)==4*rr*bb/(delta-4*rr),'retained-D term missing')
        tests.append({'loss':str(delta),'contracts':value<rr,'ratio':str(value/rr)})
    # Sum losses telescopes exactly as a rational multiple of log(2).
    for n in (1,2,10,100):
        multiple=sum((Q(1,2*(j+1)*(j+2)) for j in range(n)),Q())
        need(multiple==Q(1,2)-Q(1,2*(n+1)),'cumulative loss schedule')
    invalid=[]
    for label,args in [('zero_loss',(Q(1),Q(1),Q())),('radius_endpoint',(Q(1,4),Q(1),Q(1))),
                       ('negative_r',(Q(-1),Q(1),Q(1))),('boolean',(True,Q(1),Q(1)))]:
        try: step(*args)
        except ValueError: invalid.append(label)
        else: raise RuntimeError('invalid recurrence premise admitted')
    need(step(Q(),Q(),Q(1))==0,'zero coupling exception')
    return {'outcome':'early shrink certified and infinite positive-tau majorant closure rejected',
            'tau':str(tau),'r0':str(initial[0]),'b0':str(initial[1]),'a0':str(initial[2]),
            'log2_lower':str(lnlo),'log2_upper':str(lnhi),'early_stages':rows,
            'partial_scalar_density_absolute_upper_enclosure':enclosure(energy),
            'coarse_doubling_stage':stage,'ratio_lower_at_doubling_stage':str(factor_lower),
            'contraction_equivalence_tests':tests,'invalid_inputs_rejected':invalid,
            'total_loss':'log(2)/2','limiting_weight':'log(2)/2',
            'infinite_scalar_recurrence_admissible_for_nonzero_tau':False,
            'actual_algorithm_failure_proved':False,'actual_gap_failure_proved':False,
            'zero_tau_is_exact_exception':True}


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',required=True)
    args=parser.parse_args(); out=Path(args.output).absolute()
    for p in (out,*out.parents): need(not p.is_symlink(),'symlink output')
    need(not out.exists(),'fresh output directory required')
    need(sha(CONTRACT)==CONTRACT_HASH,'frozen O2 contract changed')
    contract=json.loads(CONTRACT.read_text())
    for rel,digest in contract['dependencies'].items(): need(sha(ROOT/rel)==digest,'dependency changed: '+rel)
    controls={'schema':'ym22-reverse-o2-controls-v1','loop':'o2','direction':'reverse','status':'passed','passed':True,
              'homological_split':split_control(),'equal_weight':equal_weight_control(),
              'retained_diagonal':retained_d_control(),'recurrence':recurrence_controls()}
    results={'schema':'ym22-reverse-o2-results-v1','loop':'o2','direction':'reverse','status':'proved_majorant_obstruction_gap_limited','passed':True,
             'claims':{'arbitrary_support_bare_inverse_gap':'1','scalar_bound':'r','A_bound':'r','S_bound':'r','Z_bound':'2*r',
                       'operator_domain_preserved':True,'all_support_commutator_loss_constant':'4/(e*delta)',
                       'nested_divided_factorial_bound':'(4*s/delta)^n*norm(K)',
                       'step_radius':'4*r<delta','step_majorant':'[4*r/(delta-4*r)]*(b+3*r/2)',
                       'diagonal_norm_update':'b+2*r','diagonal_relative_update':'a+2*r','scalar_density_increment_upper':'r',
                       'strict_majorant_contraction_iff':'delta>4*b+10*r',
                       'baseline_loss':'log(2)/(2*(n+1)*(n+2))','positive_limit_weight':'log(2)/2',
                       'positive_tau_baseline_majorant_closes':False,'tau_example':'1/100000000',
                       'eventual_doubling_coarse_stage_example':'197','actual_algorithm_failure_proved':False,
                       'numerical_homogeneous_gap_proved':False,'actual_homogeneous_gap_failure_proved':False,
                       'structured_homological_exception_retained':True,'infinite_global_unitary_proved':False},
             'target_verdict':'Homological/loss estimates proved; the complete retained-D scalar majorant cannot certify infinitely many stages at nonzero tau.',
             'next_loop_selected':False}
    rels=list(contract['dependencies'])+contract['instruction_inputs']+[
        'research/round22/reverse/o1/report.md','research/round22/reverse/o1/source-review.json',
        'research/round22/reverse/n1/inputs/advisor-finite-observations.md',
        'research/round22/reverse/n1/inputs/paired-admission-matching.md']
    inputs=[CONTRACT,HERE/'report.md',HERE/'check.py',HERE/'independence.json',HERE/'source-review.json']+[ROOT/p for p in rels]
    hashes={str(p.relative_to(ROOT)):sha(p) for p in sorted(set(inputs))}
    need(all(p in hashes for p in contract['instruction_inputs']),'instruction closure incomplete')
    out.mkdir(parents=True)
    for name,payload in [('results.json',results),('controls.json',controls)]:
        (out/name).write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
    manifest={'schema':'ym22-source-manifest-v1','inputs':hashes,
              'outputs':{n:sha(out/n) for n in ('results.json','controls.json')}}
    (out/'source-manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'loop':'o2','direction':'reverse','status':'proved_majorant_obstruction_gap_limited','passed':True}))


if __name__=='__main__': main()
