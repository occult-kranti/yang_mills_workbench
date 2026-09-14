#!/usr/bin/env python3
"""Independent exact tree/Haar/electric P2 controls, with quaternion 2-jets."""
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
CONTRACT=ROOT/'research/round22/contracts/p2.json'
CONTRACT_HASH='2eb4ae79a730a2c9ede7661d7024668800b9b15641eaaa44afd9aa5011e62ae1'
LEDGER='research/round19/forward/c1/output/graph-reduction.json'
ZERO=(Q(0),)*4
ONE=(Q(1),Q(0),Q(0),Q(0))
POOL=((Q(3,5),Q(4,5),Q(0),Q(0)),(Q(1,3),Q(2,3),Q(2,3),Q(0)),
      (Q(1,3),Q(0),Q(2,3),Q(2,3)),(Q(5,13),Q(0),Q(0),Q(12,13)))


def need(ok,message):
    if not ok: raise RuntimeError(message)


def sha(p):
    need(p.is_file(),'required source absent: '+str(p))
    for x in (p,*p.parents): need(not x.is_symlink(),'symlink source')
    return hashlib.sha256(p.read_bytes()).hexdigest()


def dump(p,x): p.write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def sh(v,a): return tuple(x+(i==a) for i,x in enumerate(v))
def qa(u,v): return tuple(x+y for x,y in zip(u,v))
def qs(u,c): return tuple(c*x for x in u)
def qi(u): return (u[0],-u[1],-u[2],-u[3])


def qm(u,v):
    a,x,y,z=u; b,X,Y,Z=v
    return (a*b-x*X-y*Y-z*Z,a*X+x*b+y*Z-z*Y,
            a*Y+y*b+z*X-x*Z,a*Z+z*b+x*Y-y*X)


def jp(q): return (q,ZERO,ZERO)
def ji(j): return tuple(qi(q) for q in j)


def jm(u,v):
    return tuple(tuple(sum((qm(u[k],v[n-k])[a] for k in range(n+1)),Q(0))
                       for a in range(4)) for n in range(3))


def jt(axis,sign=1):
    first=[Q(0)]*4; first[axis+1]=Q(sign,2)
    return (ONE,tuple(first),qs(ONE,Q(-1,8)))


def product(word,values,jet=False):
    r=jp(ONE) if jet else ONE
    for e,s in word:
        q=values[e]
        if s<0: q=ji(q) if jet else qi(q)
        r=jm(r,q) if jet else qm(r,q)
    return r


def graph():
    vertices=list(itertools.product(range(3),range(3),range(2)))
    edges=[(a,v,sh(v,a)) for a in range(3) for v in vertices if sh(v,a) in vertices]
    edge_id={(a,s):i for i,(a,s,t) in enumerate(edges)}
    old=json.loads((ROOT/LEDGER).read_text())
    inherited={x['id']:x for x in old['affected_faces']+old['constant_faces']}
    faces=[]
    for a,b in ((0,1),(0,2),(1,2)):
        for v in vertices:
            if sh(v,a) not in vertices or sh(v,b) not in vertices: continue
            word=[(edge_id[a,v],1),(edge_id[b,sh(v,a)],1),(edge_id[a,sh(v,b)],-1),(edge_id[b,v],-1)]
            idx=len(faces); faces.append(word)
            need([{'edge':e,'sign':s} for e,s in word]==inherited[idx]['signed_word'],'C1 signed face mismatch')
    tree=set(range(16))|{26}; root=(0,2,0); paths={root:[]}; queue=[root]
    for v in queue:
        for e in sorted(tree):
            a,s,t=edges[e]
            if v==s and t not in paths: paths[t]=paths[v]+[(e,1)]; queue.append(t)
            if v==t and s not in paths: paths[s]=paths[v]+[(e,-1)]; queue.append(s)
    need((len(vertices),len(edges),len(faces),len(paths),len(tree))==(18,33,20,18,17),'actual tree counts')
    chords=[e for e in range(33) if e not in tree]
    words={e:paths[edges[e][1]]+[(e,1)]+[(q,-s) for q,s in reversed(paths[edges[e][2]])] for e in chords}
    selected=(28,27,24)
    need([len(words[e]) for e in selected]==[6,8,6],'new selected physical loop lengths')
    need(all(len({e for e,s in words[c]})==len(words[c]) for c in selected),'selected loops must have distinct links')
    incidence={}
    for q in sorted(tree):
        subtree={v for v,p in paths.items() if any(e==q for e,s in p)}
        epsilon=next(s for p in paths.values() for e,s in p if e==q)
        incidence[q]={e:(epsilon*int(edges[e][1] in subtree),-epsilon*int(edges[e][2] in subtree)) for e in chords}
    def budget(retained):
        counts={q:{e:sum(abs(x) for x in incidence[q][e]) for e in retained} for q in tree}
        m={q:sum(row.values()) for q,row in counts.items()}
        coefficients={e:1+sum(m[q]*counts[q][e] for q in tree) for e in retained}
        return max(coefficients.values()),coefficients
    full_k,full_coeff=budget(chords); selected_k,selected_coeff=budget(selected)
    need(selected_k==16 and selected_coeff=={28:12,27:16,24:14},'selected H1 form budget')
    need([q for q in sorted(tree) if any(incidence[q][e]!=(0,0) for e in selected)]==[0,1,2,3,12,13,14,15,26],'selected full tree contributions')
    # Generic rational gauge configurations: no commuting simplification.
    g={e:POOL[e%len(POOL)] for e in range(33)}
    gauge={v:POOL[(i+1)%len(POOL)] for i,v in enumerate(vertices)}
    gp={e:qm(qm(gauge[s],g[e]),qi(gauge[t])) for e,(a,s,t) in enumerate(edges)}
    for e in chords:
        lhs=product(words[e],gp); base=product(words[e],g)
        rhs=qm(qm(gauge[root],base),qi(gauge[root]))
        need(lhs==rhs,'actual chord root-gauge covariance')
    e=28; s,t=edges[e][1:]
    wrong=qm(qm(product(paths[s],g),g[e]),product(paths[t],g))
    need(wrong!=product(words[e],g),'missing endpoint inverse control')
    old_section={e:ONE for e in range(33)}; old_section[25]=POOL[0]
    need(product(words[28],old_section)[0]==1 and product(faces[9],old_section)[0]==Q(3,5),'new physical completion versus P1 face')
    record={'outcome':'wrong endpoint inverse and reuse of P1 completion rejected','passed':True,
            'tree':sorted(tree),'root':list(root),'chords':chords,
            'paths':{''.join(map(str,v)):paths[v] for v in sorted(paths)},
            'chord_words':{str(e):words[e] for e in chords},
            'full_tree_incidence':{str(q):{str(e):list(pair) for e,pair in row.items() if pair!=(0,0)} for q,row in incidence.items()},
            'full_form_upper_coefficient':full_k,'selected_form_upper_coefficient':selected_k,
            'selected_form_coordinate_coefficients':{str(e):n for e,n in selected_coeff.items()},
            'P1_F9_fixture':'3/5','new_J3_x_fixture':'1'}
    return edges,tree,chords,words,incidence,record


def transport_control(edges,tree,chords,words,incidence):
    base={e:POOL[e%len(POOL)] for e in chords}
    base.update({28:POOL[0],27:POOL[1],24:POOL[2],16:POOL[2]})
    full={e:jp(ONE if e in tree else base[e]) for e in range(33)}
    cas_x=Q(0); cas_y=Q(0); cas_z=Q(0); cas_xy=Q(0)
    wrong_internal=Q(0); actual_internal=Q(0); checks=0
    for q in range(33):
        for a in range(3):
            original=dict(full); original[q]=jm(jt(a),original[q])
            actual={e:product(words[e],original,True) for e in chords}
            predicted={}
            for e in chords:
                if q in tree:
                    left,right=incidence[q][e]
                    value=jp(base[e])
                    if left: value=jm(jt(a,left),value)
                    if right: value=jm(value,jt(a,right))
                else: value=jm(jt(a),jp(base[e])) if e==q else jp(base[e])
                predicted[e]=value
                need(actual[e]==value,'full link second-jet transport mismatch')
                checks+=1
            cas_x-=2*actual[28][2][0]; cas_y-=2*actual[27][2][0]; cas_z-=2*actual[24][2][0]
            cas_xy-=2*sum((actual[28][k][0]*actual[27][2-k][0] for k in range(3)),Q(0))
            if q==14:
                pair=jm(actual[16],ji(actual[28]))
                actual_internal-=2*sum((pair[k][0]*actual[27][2-k][0] for k in range(3)),Q(0))
                # Wrong cut-only prescription removes conjugation of internal chord16.
                wrong_pair=jm(jp(base[16]),ji(actual[28]))
                wrong_internal-=2*sum((wrong_pair[k][0]*actual[27][2-k][0] for k in range(3)),Q(0))
    need(checks==33*3*16,'complete transport variation count')
    need((cas_x,cas_y,cas_z)==(Q(9,2)*base[28][0],6*base[27][0],Q(9,2)*base[24][0]),'actual electric eigenchannels')
    need(cas_x!=Q(3,4)*base[28][0],'dropped tree derivatives control')
    need(actual_internal!=wrong_internal,'internal-chord term control must reject')
    diagonal_xy=Q(21,2)*base[28][0]*base[27][0]
    need(cas_xy==Q(13,10) and diagonal_xy==Q(21,10),'joint mixed derivative fixture')
    return {'outcome':'tree omission, internal-chord omission and mixed-derivative omission rejected','passed':True,
            'exact_chord_second_jet_equalities':checks,'original_link_axis_variations':99,
            'Hx_over_alpha':str(cas_x),'Hy_over_alpha':str(cas_y),'Hz_over_alpha':str(cas_z),
            'actual_Hxy_over_alpha':str(cas_xy),'wrong_diagonal_Hxy_over_alpha':str(diagonal_xy),
            'tree14_joint_internal_chord_actual_C':str(actual_internal),
            'tree14_joint_internal_chord_wrong_C':str(wrong_internal)}


def moment(k):
    if k%2: return Q(0)
    m=k//2
    return Q(comb(2*m,m),(m+1)*4**m)


def inner(p,q):
    return sum((a*b*prod(moment(x+y) for x,y in zip(i,j)) for i,a in p.items() for j,b in q.items()),Q(0))


def prod(xs):
    r=Q(1)
    for x in xs: r*=x
    return r


def haar_project(p):
    r={}
    for powers,c in p.items():
        kept=(*powers[:3],0); coefficient=c*moment(powers[3])
        if coefficient: r[kept]=r.get(kept,Q(0))+coefficient
    return {k:v for k,v in r.items() if v}


def haar_control():
    f={(1,0,0,0):Q(1),(0,1,1,0):Q(2)}
    g={**f,(0,0,0,1):Q(3)}; identity={(0,0,0,0):Q(1)}
    projected=haar_project(g)
    need(projected==f and haar_project(projected)==f,'Haar orthogonal projection')
    need(inner(f,f)==Q(1,2) and inner(g,g)==Q(11,4),'Haar norms')
    need(inner(f,g)==inner(f,projected)==Q(1,2),'Haar adjoint identity')
    need(inner(identity,g)==inner(identity,projected)==0,'Haar state identity')
    evaluated={**f,(0,0,0,0):Q(3)}
    need(inner(identity,evaluated)==3!=inner(identity,g),'evaluation versus averaging control')
    # Gaussian rationals enforce the complex adjoint and both centering means.
    def add(z,w): return (z[0]+w[0],z[1]+w[1])
    def mul(z,w): return (z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0])
    def conj(z): return (z[0],-z[1])
    def scale(z,c): return (z[0]*c,z[1]*c)
    a=(Q(1),Q(2)); b=(Q(2),Q(-1)); target=scale(mul(conj(a),b),Q(1,8))
    values=[]
    for a0,b0 in (((Q(3),Q(1)),(Q(-1),Q(4))),((Q(2),Q(-3)),(Q(1),Q(1)))):
        raw=add(target,mul(conj(a0),b0))
        centered=add(raw,scale(mul(conj(a0),b0),-1))
        need(centered==target and raw!=target,'complex centered scalar invariance')
        need(add(raw,scale(mul(a0,b0),-1))!=target,'unconjugated mean control')
        values.append([str(x) for x in centered])
    need(scale(mul(a,b),Q(1,8))!=target,'missing complex adjoint control')
    return {'outcome':'identity evaluation and incomplete complex centering rejected','passed':True,
            'selected_test_norm_squared':'1/2','full_test_norm_squared':'11/4',
            'adjoint_pairing':'1/2','Haar_projected_mean':'0','wrong_evaluated_mean':'3',
            'complex_centered_values':values,'complex_arithmetic_scope':'exact Gaussian rational fixture'}



def expminus(x,n=80):
    need(type(x) is Q and x>0 and n%2==0,'Taylor premises')
    hi=sum(((-x)**k/factorial(k) for k in range(n+1)),Q(0))
    lo=hi-x**(n+1)/factorial(n+1)
    need(0<lo<hi<1,'exponential enclosure')
    return lo,hi


def clock_control():
    variance=moment(2); ex=Q(9,2); ey=Q(6)
    c=ex/Q(3,4)
    need(c==6 and c!=4,'training clock must use new completion')
    slope=-ex*variance
    need(slope==Q(-9,8)==-c*Q(3,4)*variance,'unique nonzero designated slope')
    qnorm=moment(4)-Q(1,2)*moment(2)+Q(1,16)
    need(qnorm==Q(1,16),'orthogonal even correction norm')
    physical_curvature=ex*ex*variance
    rows=[]
    for zeta in (Q(0),Q(1,3),Q(-1,3),Q(1,2),Q(-1,2)):
        conditional_curvature=c*c*(Q(9,16)*variance+zeta*zeta*qnorm)
        need(conditional_curvature-physical_curvature==Q(9,4)*zeta*zeta,'reserved curvature exact discrepancy')
        need((conditional_curvature==physical_curvature)==(zeta==0),'reserved curvature zero condition')
        wrong_mean=Q(3,4)*zeta*variance
        correct_mean=zeta*(variance-Q(1,4))
        need(correct_mean==0,'divergence generator must preserve Haar ground')
        if zeta: need(wrong_mean!=0,'missing divergence control must reject')
        rows.append({'zeta':str(zeta),'training_slope_times_hbar_over_alpha':str(slope),
                     'reserved_curvature_times_hbar_squared_over_alpha_squared':str(conditional_curvature),
                     'wrong_no_divergence_Haar_mean':str(wrong_mean)})
    need(physical_curvature==Q(81,16),'mapped training curvature')
    need(-ey*variance==Q(-3,2)!=slope,'reserved y slope excludes every zeta after c fit')
    need(ey/Q(3,4)==8!=c,'forbidden y refit')
    lo1,hi1=expminus(ex); lo2,hi2=expminus(ey)
    lo,hi=(lo1-hi2)/4,(hi1-lo2)/4
    unit=10**12; decimal_lo=Q(lo.numerator*unit//lo.denominator,unit)
    decimal_hi=Q(hi.numerator*unit//hi.denominator+1,unit)
    need(0<decimal_lo<lo<hi<decimal_hi,'positive full-time held-out discrepancy')
    return {'outcome':'slope-only mobility identification, missing divergence and conditional-family match rejected',
            'passed':True,'training_c_over_alpha':str(c),'slope_times_hbar_over_alpha':str(slope),
            'slope_zeta_ambiguity':'(-1,1)','curvature_matching_zeta':'0',
            'physical_training_curvature_times_hbar_squared_over_alpha_squared':str(physical_curvature),
            'curvature_samples':rows,'physical_y_full_time':'exp(-6*alpha*t/hbar)/4',
            'conditional_y_full_time_after_curvature':'exp(-(9/2)*alpha*t/hbar)/4',
            't_star':'hbar/alpha','conditional_minus_physical_lower':str(lo),
            'conditional_minus_physical_upper':str(hi),'decimal_rational_lower':str(decimal_lo),
            'decimal_rational_upper':str(decimal_hi),'positive_for_every_finite_positive_time':True,
            'zero_time_discrepancy':'0','any_admissible_zeta_matches_all_reserved_data':False,
            'ground_scalar_shift':'0'}


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',required=True)
    args=parser.parse_args(); out=Path(args.output).absolute()
    for x in (out,*out.parents): need(not x.is_symlink(),'symlink output')
    need(not out.exists(),'fresh output required')
    need(sha(CONTRACT)==CONTRACT_HASH,'frozen P2 contract changed')
    contract=json.loads(CONTRACT.read_text())
    for rel,digest in contract['dependencies'].items(): need(sha(ROOT/rel)==digest,'inherited dependency changed: '+rel)
    edges,tree,chords,words,incidence,geometry=graph()
    controls={'schema':'ym22-reverse-p2-controls-v1','loop':'p2','direction':'reverse','status':'passed','passed':True,
              'actual_tree_and_orientation':geometry,
              'complete_electric_transport':transport_control(edges,tree,chords,words,incidence),
              'Haar_map_and_centering':haar_control(),'fit_and_reserved_data':clock_control()}
    results={'schema':'ym22-reverse-p2-results-v1','loop':'p2','direction':'reverse',
             'status':'proved_exact_electric_reduction_rejected_conditional_family_match','passed':True,
             'claims':{'full_J16_unitary':True,'selected_J3_isometry':True,'selected_adjoint':'Haar integration of other 13 chords',
                       'full_and_selected_state_preserving':True,'selected_image_reduces_HE':True,
                       'selected_projection':'Haar integration over 13 unused original chord links',
                       'full_form_domain':'H1(SU2^16)^Ad','full_operator_domain':'H2(SU2^16)^Ad',
                       'selected_form_domain':'H1(SU2^3)^Ad','selected_operator_domain':'H2(SU2^3)^Ad',
                       'full_form_comparison_upper':geometry['full_form_upper_coefficient'],
                       'selected_form_comparison_upper':16,'form_comparison_lower':1,
                       'selected_graph_isometry':True,'exact_common_clock_semigroup_intertwiner':True,
                       'selected_physical_loop_lengths':[6,8,6],'selected_physical_energies_over_alpha':['9/2','6','9/2'],
                       'training_c_over_alpha':'6','training_variance':'1/4','heldout_variance':'1/4',
                       'slope_zeta_ambiguity':'(-1,1)','reserved_curvature_forces_zeta':'0',
                       'reserved_curvature_excess_times_hbar_squared_over_alpha_squared':'9*zeta^2/4',
                       'heldout_y_discrepancy_at_t_star':'(exp(-9/2)-exp(-6))/4',
                       'conditional_family_matches_all_reserved_data':False,'physical_calibration_completed':False,
                       'interacting_or_continuum_transfer':False},
             'target_verdict':'The Haar tree map and selected electric reduction are exact; the declared scalar-clock affine mobility family fails the reserved data.',
             'next_loop_selected':False}
    rels=list(contract['dependencies'])+contract['instruction_inputs']+[
        'research/round22/reverse/p1/report.md','research/round22/reverse/p1/source-review.json',
        'research/round22/reverse/n1/inputs/advisor-finite-observations.md',
        'research/round22/reverse/n1/inputs/paired-admission-matching.md']
    inputs=[CONTRACT,HERE/'report.md',HERE/'check.py',HERE/'source-review.json',HERE/'independence.json']+[ROOT/r for r in rels]
    hashes={str(p.relative_to(ROOT)):sha(p) for p in sorted(set(inputs))}
    need(all(r in hashes for r in contract['instruction_inputs']),'complete instruction closure required')
    out.mkdir(parents=True)
    for name,payload in [('results.json',results),('controls.json',controls)]: dump(out/name,payload)
    dump(out/'source-manifest.json',{'schema':'ym22-source-manifest-v1','inputs':hashes,
                                   'outputs':{n:sha(out/n) for n in ('results.json','controls.json')}})
    print(json.dumps({'loop':'p2','direction':'reverse','status':results['status'],'passed':True}))


if __name__=='__main__': main()
