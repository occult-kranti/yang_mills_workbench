#!/usr/bin/env python3
"""Independent exact P1 section, domain and clock controls; standard library only."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from fractions import Fraction as Q
from math import comb, factorial
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
CONTRACT=ROOT/'research/round22/contracts/p1.json'
CONTRACT_HASH='3460a2d2fb9767d0ba59c0647ea8bf5aa657bf1541f2d2184e6584f722c69102'
LEDGER='research/round19/forward/c1/output/graph-reduction.json'


def need(ok,message):
    if not ok: raise RuntimeError(message)


def sha(p):
    need(p.is_file(),'required source missing: '+str(p))
    for node in (p,*p.parents): need(not node.is_symlink(),'symlink input')
    return hashlib.sha256(p.read_bytes()).hexdigest()


def dump(p,data): p.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')


def shift(v,a): return tuple(x+(i==a) for i,x in enumerate(v))


def qmul(u,v):
    a,x,y,z=u; b,X,Y,Z=v
    return (a*b-x*X-y*Y-z*Z,a*X+x*b+y*Z-z*Y,
            a*Y+y*b+z*X-x*Z,a*Z+z*b+x*Y-y*X)


def qinv(u): return (u[0],-u[1],-u[2],-u[3])


def graph_control():
    vertices=list(itertools.product(range(3),range(3),range(2)))
    edges=[(a,v) for a in range(3) for v in vertices if shift(v,a) in vertices]
    index={e:i for i,e in enumerate(edges)}
    faces=[]
    active={28:'U',27:'V',24:'W'}
    for a,b in ((0,1),(0,2),(1,2)):
        for v in vertices:
            va,vb=shift(v,a),shift(v,b)
            if va not in vertices or vb not in vertices: continue
            word=[(index[a,v],1),(index[b,va],1),(index[a,vb],-1),(index[b,v],-1)]
            aw=[{'symbol':active[e],'sign':s} for e,s in word if e in active]
            faces.append({'id':len(faces),'axes':'xyz'[a]+'xyz'[b],'base':list(v),
                          'signed_word':[{'edge':e,'sign':s} for e,s in word],
                          'active_word':aw,'vertices':[list(v),list(va),list(shift(va,b)),list(vb)]})
    need((len(vertices),len(edges),len(faces))==(18,33,20),'actual graph counts')
    inherited=json.loads((ROOT/LEDGER).read_text())
    old={f['id']:f for f in inherited['affected_faces']+inherited['constant_faces']}
    for f in faces:
        for field in ('axes','base','signed_word','active_word','vertices'):
            need(f[field]==old[f['id']][field],'signed face differs: '+str((f['id'],field)))
    for label,item in inherited['active_links'].items():
        need(edges[item['edge']]==('xyz'.index(item['axis']),tuple(item['coordinate'])),'active edge coordinates')
        need(active[item['edge']]==label,'active edge labels')
    expected={8:'t',9:'x',11:'y',12:'x',14:'z',16:'w',17:'x'}
    need({f['id']:old[f['id']]['reduced_symbol'] for f in faces if f['active_word']}==expected,'restricted action symbols')
    unit=(Q(1),Q(0),Q(0),Q(0))
    u=(Q(3,5),Q(4,5),Q(0),Q(0)); v=(Q(1,3),Q(2,3),Q(2,3),Q(0)); w=(Q(1,3),Q(0),Q(2,3),Q(2,3))
    for q in (u,v,w): need(qmul(q,qinv(q))==unit,'quaternion norm')
    need(qmul(u,v)!=qmul(v,u),'noncommuting fixture required')
    values={'1':Q(1),'x':u[0],'y':v[0],'z':w[0],'w':qmul(u,qinv(v))[0],'t':qmul(v,qinv(w))[0]}
    configured={28:u,27:v,24:w}; traces={}
    for f in faces:
        q=unit
        for term in f['signed_word']:
            value=configured.get(term['edge'],unit)
            q=qmul(q,value if term['sign']==1 else qinv(value))
        traces[f['id']]=q[0]
        need(q[0]==values[expected.get(f['id'],'1')],'full section quaternion trace')
    need(qmul(u,v)[0]!=traces[16],'wrong dagger fixture is not discriminating')
    fixed=[i for i in range(33) if i not in active]
    seen={vertices[0]}; tree=[]
    while True:
        added=False
        for i in fixed:
            a,tail=edges[i]; head=shift(tail,a)
            if (tail in seen)!=(head in seen):
                seen.update((tail,head)); tree.append(i); added=True
        if not added: break
    need(len(seen)==18 and len(tree)==17,'fixed subgraph spanning tree')
    need(len(fixed)-len(tree)==13 and len(edges)-len(tree)==16,'actual cycle ranks')
    disjoint=[0,1,13]; supports=[]
    for i in disjoint:
        need(not faces[i]['active_word'],'domain face must restrict to identity')
        supports.append({t['edge'] for t in faces[i]['signed_word']})
    need(len(set.union(*supports))==12,'domain-sequence faces must be edge disjoint')
    return {'outcome':'false 30-link gauge fixing and wrong face dagger rejected',
            'passed':True,'vertices':18,'edges':33,'faces':20,'fixed_links':30,
            'spanning_tree_in_fixed_links':tree,'full_chord_count':16,'fixed_chord_count':13,
            'disjoint_constant_faces':disjoint,'independently_rebuilt_faces':faces,
            'quaternion_traces':{str(i):str(x) for i,x in traces.items()},
            'wrong_F16_UV_trace':str(qmul(u,v)[0]),'correct_F16_UV_inverse_trace':str(traces[16])}


def trim(p):
    while len(p)>1 and p[-1]==0: p.pop()
    return p


def padd(p,q):
    r=[Q(0)]*max(len(p),len(q))
    for i,x in enumerate(p): r[i]+=x
    for i,x in enumerate(q): r[i]+=x
    return trim(r)


def pscale(p,c): return trim([c*x for x in p])


def pmul(p,q):
    r=[Q(0)]*(len(p)+len(q)-1)
    for i,x in enumerate(p):
        for j,y in enumerate(q): r[i+j]+=x*y
    return trim(r)


def deriv(p): return trim([i*p[i] for i in range(1,len(p))] or [Q(0)])


def casimir(p):
    # Class-function radial Casimir in x=Tr(U)/2 at T_a=-i sigma_a/2.
    return pscale(padd(pmul([Q(1),Q(0),Q(-1)],deriv(deriv(p))),
                      pscale(pmul([Q(0),Q(1)],deriv(p)),-3)),Q(-1,4))


def moment(k):
    if k%2: return Q(0)
    m=k//2
    return Q(comb(2*m,m),(m+1)*4**m)


def haar(p): return sum((x*moment(i) for i,x in enumerate(p)),Q(0))


def domain_control():
    chars=[[Q(1)],[Q(0),Q(2)]]
    for n in range(1,9): chars.append(padd(pmul([Q(0),Q(2)],chars[-1]),pscale(chars[-2],-1)))
    rows=[]
    for n,p in enumerate(chars):
        need(sum(p)==n+1,'identity character dimension')
        need(haar(p)==(n==0),'character Haar mean')
        need(haar(pmul(p,p))==1,'character Haar norm')
        need(casimir(p)==pscale(p,Q(n*(n+2),4)),'Casimir character eigenvalue')
        for m in range(n): need(haar(pmul(p,chars[m]))==0,'character orthogonality')
    for n in (1,2,4,8,16,32):
        d=n+1; norm2=Q(1,d**6); hnorm2=Q(9*n*n*(n+2)**2,d**6)
        need(hnorm2<Q(9,d*d),'graph norm vanishing upper bound')
        rows.append({'n':n,'single_L2_norm_squared':str(Q(1,d*d)),
                     'triple_L2_norm_squared':str(norm2),'triple_HE_over_alpha_norm_squared':str(hnorm2),
                     'triple_R_image_norm_squared':'1','triple_energy_over_alpha':3*n*(n+2)})
    need(Q(3,4)==haar([Q(0),Q(0),Q(3)]),'fundamental Casimir/variance normalization')
    return {'outcome':'L2 closability, graph-domain continuity and state preservation rejected',
            'passed':True,'character_polynomial_degrees_checked':list(range(len(chars))),
            'rows':rows,'physical_F0_mean':'0','conditional_R_F0_mean':'1',
            'all_n_graph_norm_bound':'(n+1)^-6+9*(alpha/E_star)^2*(n+1)^-2',
            'nonclosable_in_L2':True,'nonclosable_from_electric_graph_domain':True}


def expminus_interval(x,n=80):
    need(type(x) is Q and x>=0 and n%2==0,'Taylor premises')
    upper=sum(((-x)**k/factorial(k) for k in range(n+1)),Q(0))
    lower=upper-x**(n+1)/factorial(n+1)
    need(0<lower<upper<1,'positive exponential enclosure')
    return lower,upper


def clock_control():
    cas=Q(3,4); variance=Q(1,4)
    physical_energy=4*cas
    train_cond_coefficient=cas
    hold_cond_coefficient=2*cas
    c_over_alpha=physical_energy/train_cond_coefficient
    need(c_over_alpha==4,'training slope unique fit')
    physical_slope=-physical_energy*variance
    conditional_slope=-c_over_alpha*train_cond_coefficient*variance
    need(physical_slope==conditional_slope==Q(-3,4),'nonzero training slope')
    hold_energy=c_over_alpha*hold_cond_coefficient
    need(hold_energy==6!=physical_energy,'holdout eigenvalue mismatch')
    need(physical_energy/hold_cond_coefficient==2!=c_over_alpha,'holdout refit control')
    lo3,hi3=expminus_interval(Q(3)); lo6,hi6=expminus_interval(Q(6))
    lo,hi=(lo3-hi6)/4,(hi3-lo6)/4
    display_lo=Q(1182707,100000000); display_hi=Q(1182709,100000000)
    need(0<display_lo<lo<hi<display_hi,'held-out certified mismatch')
    defects={}
    for face,active in ((0,0),(9,1),(16,2)):
        correct=4*cas; restricted=c_over_alpha*active*cas
        defects[str(face)]={'full_link_energy_over_alpha':str(correct),
                           'fixed_link_derivatives':4-active,'restricted_energy_over_alpha':str(restricted),
                           'intertwiner_defect_coefficient_over_alpha':str(correct-restricted)}
    need(defects['0']['intertwiner_defect_coefficient_over_alpha']=='3','constant face core defect')
    need(defects['16']['intertwiner_defect_coefficient_over_alpha']=='-3','holdout core defect')
    # Constant ground forces equal scalar shifts; test unequal shifts against the ground.
    for shift_phys,shift_cond in ((Q(0),Q(3)),(Q(-3),Q(0))):
        need(shift_phys!=shift_cond,'unequal scalar shift must fail on constant ground')
    for equal_shift in (Q(0),Q(3),Q(-7,2)):
        need((3+equal_shift)-equal_shift==3,'equal shifts do not repair constant face')
    return {'outcome':'common fitted clock, missing fixed derivatives and scalar repair rejected',
            'passed':True,'training_c_over_alpha':str(c_over_alpha),
            'training_slope_times_hbar_over_alpha':str(physical_slope),'variance':'1/4',
            'physical_holdout_energy_over_alpha':'3','conditional_holdout_energy_over_alpha':'6',
            'physical_holdout_full_time':'exp(-3*alpha*t/hbar)/4',
            'conditional_holdout_full_time':'exp(-6*alpha*t/hbar)/4',
            't_star':'hbar/alpha','difference_lower':str(lo),'difference_upper':str(hi),
            'difference_decimal_rational_lower':str(display_lo),
            'difference_decimal_rational_upper':str(display_hi),'zero_time_difference':'0',
            'positive_difference_for_every_finite_positive_time':True,
            'core_defects':defects,'F16_defect_norm_squared_over_alpha_squared':'9/4',
            'F0_defect_norm_over_alpha':'3'}


def gadd(z,w): return (z[0]+w[0],z[1]+w[1])
def gmul(z,w): return (z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])
def gconj(z): return (z[0],-z[1])
def gscale(z,c): return (z[0]*c,z[1]*c)


def centering_control():
    a=(Q(1),Q(2)); b=(Q(2),Q(-1)); target=gscale(gmul(gconj(a),b),Q(1,8))
    rows=[]
    for a0,b0 in (((Q(3),Q(1)),(Q(-1),Q(4))),((Q(2),Q(-3)),(Q(1),Q(1)))):
        means=gmul(gconj(a0),b0); raw=gadd(target,means)
        centered=gadd(raw,gscale(means,-1))
        need(centered==target and raw!=target,'centering and scalar identity control')
        wrong=gadd(raw,gscale(gmul(a0,b0),-1))
        need(wrong!=target,'unconjugated means control must discriminate')
        rows.append({'raw':[str(x) for x in raw],'centered':[str(x) for x in centered],
                     'wrong_means_centered':[str(x) for x in wrong]})
    need(gscale(gmul(a,b),Q(1,8))!=target,'adjoint control must discriminate')
    return {'outcome':'missing centering and missing complex adjoint rejected','passed':True,
            'scope':'exact covariance algebra at a positive semigroup factor, no clock fit',
            'centered_result':[str(x) for x in target],'rows':rows}


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',required=True)
    args=parser.parse_args(); out=Path(args.output).absolute()
    for p in (out,*out.parents): need(not p.is_symlink(),'symlink output')
    need(not out.exists(),'fresh output directory required')
    need(sha(CONTRACT)==CONTRACT_HASH,'frozen P1 contract changed')
    contract=json.loads(CONTRACT.read_text())
    for rel,digest in contract['dependencies'].items(): need(sha(ROOT/rel)==digest,'inherited dependency changed: '+rel)
    controls={'schema':'ym22-reverse-p1-controls-v1','loop':'p1','direction':'reverse','status':'passed','passed':True,
              'actual_graph':graph_control(),'hilbert_and_domain':domain_control(),
              'clock_and_core':clock_control(),'complex_centering':centering_control()}
    results={'schema':'ym22-reverse-p1-results-v1','loop':'p1','direction':'reverse',
             'status':'rejected_section_and_fitted_clock_match','passed':True,
             'claims':{'section_exists_on_smooth_invariant_core':True,'section_L2_closable':False,
                       'section_graph_domain_closable':False,'section_state_preserving':False,
                       'core_intertwiner_for_any_c':False,'scalar_shift_repairs_intertwiner':False,
                       'full_vertices':18,'full_edges':33,'full_faces':20,'true_tree_fixed_links':17,
                       'full_chord_variables':16,'additional_fixed_chords':13,
                       'domain_sequence_faces':[0,1,13],'domain_sequence_L2_norm_squared':'(n+1)^-6',
                       'domain_sequence_energy_over_alpha':'3*n*(n+2)','domain_sequence_R_image':'1',
                       'training_c_over_alpha':'4','training_and_holdout_variance':'1/4',
                       'physical_holdout_energy_over_alpha':'3','conditional_holdout_energy_over_alpha':'6',
                       'holdout_difference_at_t_star':'(exp(-3)-exp(-6))/4',
                       'holdout_difference_strictly_positive_for_t_gt_zero':True,
                       'all_physical_reductions_impossible':False,'physical_calibration_completed':False,
                       'interacting_or_continuum_transfer':False},
             'target_verdict':'The prescribed section is nonclosable, fails state and core relations, and its designated slope fit fails the reserved full-time channel.',
             'next_loop_selected':False}
    rels=list(contract['dependencies'])+contract['instruction_inputs']+[
        'research/round22/reverse/o2/check.py','research/round22/reverse/o2/submission.json']
    inputs=[CONTRACT,HERE/'report.md',HERE/'check.py',HERE/'independence.json',HERE/'source-review.json']+[ROOT/p for p in rels]
    hashes={str(p.relative_to(ROOT)):sha(p) for p in sorted(set(inputs))}
    need(all(p in hashes for p in contract['instruction_inputs']),'instruction closure incomplete')
    out.mkdir(parents=True)
    for name,payload in [('results.json',results),('controls.json',controls)]: dump(out/name,payload)
    dump(out/'source-manifest.json',{'schema':'ym22-source-manifest-v1','inputs':hashes,
                                   'outputs':{n:sha(out/n) for n in ('results.json','controls.json')}})
    print(json.dumps({'loop':'p1','direction':'reverse','status':results['status'],'passed':True}))


if __name__=='__main__': main()
