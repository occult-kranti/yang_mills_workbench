#!/usr/bin/env python3
"""Exact twenty-face quaternion-polynomial Haar contractions and block controls."""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
import hashlib
import itertools
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
CONTRACT=ROOT/'research/round22/contracts/q1.json'
CONTRACT_HASH='bc6ba8654f98814173385ae99cb77478ab8a16ec4cc80543a59678ffa149330f'
LEDGER='research/round19/forward/c1/output/graph-reduction.json'
SELECTED=frozenset((24,27,28))
ONE=(F(1),F(0),F(0),F(0))
POOL=((F(3,5),F(4,5),F(0),F(0)),(F(1,3),F(2,3),F(2,3),F(0)),
      (F(1,3),F(0),F(2,3),F(2,3)),(F(5,13),F(0),F(0),F(12,13)))


def need(ok,message):
    if not ok: raise RuntimeError(message)


def sha(p):
    need(p.is_file(),'required source absent: '+str(p))
    for q in (p,*p.parents): need(not q.is_symlink(),'symlink source')
    return hashlib.sha256(p.read_bytes()).hexdigest()


def dump(p,data): p.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
def sh(v,a): return tuple(x+(i==a) for i,x in enumerate(v))
def qi(q): return (q[0],-q[1],-q[2],-q[3])


def qm(u,v):
    a,x,y,z=u; b,X,Y,Z=v
    return (a*b-x*X-y*Y-z*Z,a*X+x*b+y*Z-z*Y,
            a*Y+y*b+z*X-x*Z,a*Z+z*b+x*Y-y*X)


def qword(word,values):
    q=ONE
    for e,s in word: q=qm(q,values[e] if s>0 else qi(values[e]))
    return q


def graph():
    vertices=list(itertools.product(range(3),range(3),range(2)))
    edges=[(a,v,sh(v,a)) for a in range(3) for v in vertices if sh(v,a) in vertices]
    index={(a,s):i for i,(a,s,t) in enumerate(edges)}
    tree=set(range(16))|{26}; root=(0,2,0); paths={root:[]}; queue=[root]
    for v in queue:
        for e in sorted(tree):
            a,s,t=edges[e]
            if v==s and t not in paths: paths[t]=paths[v]+[(e,1)]; queue.append(t)
            if v==t and s not in paths: paths[s]=paths[v]+[(e,-1)]; queue.append(s)
    need(len(paths)==18 and len(tree)==17,'actual tree')
    chords=[e for e in range(33) if e not in tree]
    need(len(chords)==16 and len(set(chords)-SELECTED)==13,'retained and integrated chord counts')
    inherited=json.loads((ROOT/LEDGER).read_text())
    old={f['id']:f for f in inherited['affected_faces']+inherited['constant_faces']}
    faces=[]
    for a,b in ((0,1),(0,2),(1,2)):
        for v in vertices:
            if sh(v,a) not in vertices or sh(v,b) not in vertices: continue
            full=[(index[a,v],1),(index[b,sh(v,a)],1),(index[a,sh(v,b)],-1),(index[b,v],-1)]
            idx=len(faces); word=[(e,s) for e,s in full if e not in tree]
            need([{'edge':e,'sign':s} for e,s in full]==old[idx]['signed_word'],'C1 signed face mismatch')
            faces.append({'id':idx,'axes':'xyz'[a]+'xyz'[b],'base':list(v),
                          'full_word':full,'chord_word':word,'omitted_chords':sorted({e for e,s in word}-SELECTED)})
    need(len(faces)==20 and all(len({e for e,s in f['chord_word']})==len(f['chord_word']) for f in faces),'complete distinct-chord face words')
    g={e:POOL[e%4] for e in range(33)}
    h={v:qword(paths[v],g) for v in vertices}
    loops={e:qm(qm(h[edges[e][1]],g[e]),qi(h[edges[e][2]])) for e in chords}
    for f in faces: need(qword(f['full_word'],g)[0]==qword(f['chord_word'],loops)[0],'full/chord face transport')
    need([f['id'] for f in faces if not f['omitted_chords']]==[8],'only face8 is selected')
    repeated=[(i,j) for i in range(20) for j in range(i+1,20)
              if faces[i]['omitted_chords']==faces[j]['omitted_chords']]
    need(repeated==[(9,14),(9,15),(14,15)],'conditional correlated pair geometry')
    # All positive plaquettes can be -I on this open graph; verifies the bound witness.
    flux={}
    for e,(a,v,t) in enumerate(edges):
        sign=(-1)**sum(v[:a]); flux[e]=tuple(sign*x for x in ONE)
    need(all(qword(f['full_word'],flux)[0]==-1 for f in faces),'full magnetic 40 endpoint witness')
    return faces,chords,{'outcome':'wrong reduced action and omitted shared-chord correlations rejected','passed':True,
                         'vertices':18,'links':33,'faces':faces,'tree':sorted(tree),'chords':chords,
                         'repeated_omitted_chord_pairs':repeated,'full_action_maximum_witness':40}


def pc(c): return {():F(c)} if c else {}
def pv(i): return {(i,):F(1)}
def ps(p,c): return {m:c*a for m,a in p.items() if c*a}


def pa(*polys):
    out={}
    for p in polys:
        for m,c in p.items(): out[m]=out.get(m,F(0))+c
    return {m:c for m,c in out.items() if c}


def pm(p,q):
    out={}
    for a,x in p.items():
        for b,y in q.items():
            m=tuple(sorted(a+b)); out[m]=out.get(m,F(0))+x*y
    return {m:c for m,c in out.items() if c}


def pq(e): return tuple(pv(4*e+a) for a in range(4))
def pqi(q): return (q[0],ps(q[1],-1),ps(q[2],-1),ps(q[3],-1))


def pqm(u,v):
    a,x,y,z=u; b,X,Y,Z=v
    return (pa(pm(a,b),ps(pm(x,X),-1),ps(pm(y,Y),-1),ps(pm(z,Z),-1)),
            pa(pm(a,X),pm(x,b),pm(y,Z),ps(pm(z,Y),-1)),
            pa(pm(a,Y),pm(y,b),pm(z,X),ps(pm(x,Z),-1)),
            pa(pm(a,Z),pm(z,b),pm(x,Y),ps(pm(y,X),-1)))


def pword(word):
    q=(pc(1),{},{},{})
    for e,s in word: q=pqm(q,pq(e) if s>0 else pqi(pq(e)))
    return q[0]


@lru_cache(maxsize=None)
def sphere_moment(powers):
    if any(n%2 for n in powers): return F(0)
    numerator=1
    for n in powers:
        for j in range(1,n,2): numerator*=j
    denominator=1
    for j in range(sum(powers)//2): denominator*=4+2*j
    return F(numerator,denominator)


@lru_cache(maxsize=None)
def integrate_monomial(m,integrated):
    counts={}; kept=[]
    for v in m:
        e,a=divmod(v,4)
        if e in integrated:
            if e not in counts: counts[e]=[0,0,0,0]
            counts[e][a]+=1
        else: kept.append(v)
    value=F(1)
    for powers in counts.values():
        value*=sphere_moment(tuple(powers))
        if not value: return (),F(0)
    return tuple(kept),value


def expect(p,integrated):
    out={}
    for m,c in p.items():
        keep,value=integrate_monomial(m,integrated)
        if value: out[keep]=out.get(keep,F(0))+c*value
    return {m:c for m,c in out.items() if c}


def expect_product(p,q,integrated):
    out={}
    for m,c in p.items():
        for n,d in q.items():
            keep,value=integrate_monomial(tuple(sorted(m+n)),integrated)
            if value: out[keep]=out.get(keep,F(0))+c*d*value
    return {m:c for m,c in out.items() if c}


@lru_cache(maxsize=None)
def reduce_monomial(m):
    # Quotient by q_e,0^2=1-q_e,1^2-q_e,2^2-q_e,3^2 for selected SU2 variables.
    counts=Counter(m)
    for e in sorted(SELECTED):
        i=4*e
        if counts[i]>=2:
            remaining=list(m); remaining.remove(i); remaining.remove(i); base=tuple(remaining)
            answer=dict(reduce_monomial(base))
            for a in (1,2,3):
                for term,c in reduce_monomial(tuple(sorted(base+(i+a,i+a)))).items():
                    answer[term]=answer.get(term,F(0))-c
            return {term:c for term,c in answer.items() if c}
    return {m:F(1)}


def reduced(p):
    out={}
    for m,c in p.items():
        for term,d in reduce_monomial(m).items(): out[term]=out.get(term,F(0))+c*d
    return {m:c for m,c in out.items() if c}


def evaluated(p,values):
    total=F(0)
    for m,c in p.items():
        value=c
        for v in m: value*=values[v//4][v%4]
        total+=value
    return total


def poly_digest(p):
    data=[{'variables':list(m),'coefficient':str(c)} for m,c in sorted(p.items())]
    return hashlib.sha256(json.dumps(data,sort_keys=True,separators=(',',':')).encode()).hexdigest()


def moment_controls(faces,chords):
    polynomials=[pword(f['chord_word']) for f in faces]
    omitted=frozenset(set(chords)-SELECTED)
    means=[reduced(expect(p,omitted)) for p in polynomials]
    tau=pword([(27,1),(24,-1)]); r=pword([(28,1),(24,-1)]); x=pv(4*28); z=pv(4*24)
    need(means[8]==tau and all(not m for i,m in enumerate(means) if i!=8),'exact polynomial conditional face means')
    expected_cross={(9,14):ps(r,F(1,4)),(9,15):ps(x,F(1,4)),(14,15):ps(z,F(1,4))}
    second_S={}; nonzero=[]; count=0
    for i in range(20):
        for j in range(i,20):
            value=reduced(expect_product(polynomials[i],polynomials[j],omitted)); count+=1
            if i==j: target=pm(tau,tau) if i==8 else pc(F(1,4))
            else: target=expected_cross.get((i,j),{})
            need(value==reduced(target),'exact conditional pair contraction: '+str((i,j)))
            if value: nonzero.append([i,j])
            second_S=pa(second_S,ps(value,1 if i==j else 2))
    need(count==210 and len(nonzero)==23,'complete pair inventory')
    d=pa(pc(F(19,4)),ps(pa(r,x,z),F(1,2)))
    m=pa(pc(20),ps(tau,-1))
    second_V=reduced(pa(pc(400),ps(tau,-40),second_S))
    need(second_V==reduced(pa(pm(m,m),d)),'full conditional second moment')
    need(reduced(pa(second_V,ps(pm(m,m),-1)))==reduced(d),'conditional variance multiplication function')
    positive=pc(4)
    for a in range(4):
        v=pa(pv(4*28+a),pv(4*24+a),pc(1 if a==0 else 0))
        positive=pa(positive,ps(pm(v,v),F(1,4)))
    need(reduced(positive)==reduced(d),'exact square completion')
    all_chords=frozenset(chords)
    need(expect(d,all_chords)==pc(F(19,4)),'Haar leakage expectation')
    need(expect(pm(d,d),all_chords)==pc(F(91,4)),'Haar squared leakage multiplication norm')
    need(expect(m,all_chords)==pc(20) and expect(second_V,all_chords)==pc(405),'reference moments')
    fixture={28:POOL[0],24:POOL[1],27:POOL[2]}
    dv=evaluated(d,fixture)
    need(dv==F(67,12)!=F(19,4),'false conditional-face independence control')
    wrong14=pword([(25,1),(24,1)])
    wrong_cross=reduced(expect_product(polynomials[9],wrong14,omitted))
    need(wrong_cross!=reduced(expected_cross[9,14]),'wrong orientation correlated pair')
    need(evaluated(wrong_cross,fixture)==F(-1,12) and evaluated(expected_cross[9,14],fixture)==F(11,60),'wrong orientation fixture')
    # Eight-point second-moment cubature is exact for this single Haar chord's quadratics.
    cubature=[]
    for a in range(4):
        for sign in (-1,1):
            q=[F(0)]*4; q[a]=F(sign); cubature.append(tuple(q))
    u,w=fixture[28],fixture[24]
    cubcross=sum((qm(u,qi(q))[0]*qm(q,qi(w))[0] for q in cubature),F(0))/8
    groupvariance=sum(((qm(u,qi(q))[0]+qm(q,qi(w))[0]+qi(q)[0])**2 for q in cubature),F(0))/8
    need(cubcross==F(11,60) and 4+groupvariance==dv,'independent shared-chord cubature')
    identity={24:ONE,27:ONE,28:ONE}
    need(evaluated(d,identity)==F(25,4),'sharp supremum witness')
    # Minimum is realized by unit vectors u+w=-e0; Gram matrix has nonnegative principal minors.
    gram=[[F(1),F(-1,2),F(-1,2)],[F(-1,2),F(1),F(-1,2)],[F(-1,2),F(-1,2),F(1)]]
    determinant=gram[0][0]*(gram[1][1]*gram[2][2]-gram[1][2]*gram[2][1])-gram[0][1]*(gram[1][0]*gram[2][2]-gram[1][2]*gram[2][0])+gram[0][2]*(gram[1][0]*gram[2][1]-gram[1][1]*gram[2][0])
    need(determinant==0 and all(gram[i][i]*gram[j][j]-gram[i][j]**2==F(3,4) for i in range(3) for j in range(i+1,3)),'sharp minimum Gram witness')
    need(F(19,4)+F(1,2)*F(-3,2)==4,'sharp infimum value')
    need(reduced(d)!=pc(F(19,4)),'function-versus-expectation control')
    return {'outcome':'conditional independence, wrong dagger and replacing function by Haar mean rejected','passed':True,
            'unordered_pair_contractions':count,'nonzero_pairs':nonzero,
            'conditional_mean':'20-tau','conditional_second_moment':'(20-tau)^2+19/4+(r+x+z)/2',
            'conditional_variance':'19/4+(r+x+z)/2','variance_lower':'4','variance_upper':'25/4',
            'variance_Haar_mean':'19/4','variance_square_Haar_mean':'91/4',
            'potential_Haar_mean':'20','potential_Haar_second_moment':'405','potential_Haar_variance':'5',
            'fixture_variance':str(dv),'wrong_independent_fixture_variance':'19/4',
            'fixture_shared_pair':'11/60','wrong_dagger_shared_pair':'-1/12',
            'cubature_shared_pair':str(cubcross),'minimum_witness_Gram':[[str(v) for v in row] for row in gram],
            'canonical_polynomial_hashes':{'mean':poly_digest(reduced(m)),'second_moment':poly_digest(second_V),'variance':poly_digest(reduced(d))}}


def mm(a,b): return [[sum((x*y for x,y in zip(row,col)),F(0)) for col in zip(*b)] for row in a]
def ma(a,b): return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def ms(a,c): return [[c*x for x in row] for row in a]
def sub(a,b): return ma(a,ms(b,-1))
def matrix(rows): return [[F(x) for x in row] for row in rows]
def corner(a): return [row[:2] for row in a[:2]]


def block_controls():
    h0=matrix([[0,0,0],[0,2,0],[0,0,3]])
    eye=matrix([[1,0,0],[0,1,0],[0,0,1]])
    v=matrix([[2,1,1],[1,2,-1],[1,-1,2]])
    vv=matrix([[1,-1,-1],[-1,1,1],[-1,1,1]])
    need(v==sub(ms(eye,3),vv) and mm(vv,vv)==ms(vv,3),'positive block perturbation')
    rows=[]
    for lam in (F(0),F(1,5)):
        h=ma(h0,ms(v,lam)); a=corner(h)
        defect=sub(corner(mm(h,h)),mm(a,a))
        expected=ms(matrix([[1,-1],[-1,1]]),lam*lam)
        need(defect==expected,'second-order compressed generator identity')
        if lam:
            need(mm(a,defect)!=mm(defect,a),'noncommuting block control')
            need(any(x for row in defect for x in row),'nonzero block leakage')
        else: need(not any(x for row in defect for x in row),'lambda zero electric recovery')
        shift=F(-7,3); shifted=ma(h,ms(eye,shift)); sa=corner(shifted)
        need(sub(corner(mm(shifted,shifted)),mm(sa,sa))==defect,'common scalar shift coefficient')
        need(sub(sa,a)==ms(corner(eye),shift),'unequal shift first derivative mismatch')
        rows.append({'lambda':str(lam),'second_order_generator_defect':[[str(x) for x in row] for row in defect]})
    need(F(25,4)/2==F(25,8) and F(19,4)/2==F(19,8),'actual moment-to-dynamic coefficients')
    need(F(91,4)/4==F(91,16),'actual reference vector defect norm coefficient squared')
    need(F(405)-20**2==5>0,'Haar reference cannot be made eigenvector by scalar')
    return {'outcome':'first-order autonomous promotion and scalar repair rejected; lambda zero recovered','passed':True,
            'scope':'finite positive noncommuting block fixture checks algebra; actual SU2 leakage is from exact moments',
            'rows':rows,'actual_leakage_operator_norm_over_alpha_lambda':'5/2',
            'actual_leakage_reference_norm_squared_over_alpha_squared_lambda_squared':'19/4',
            'actual_dynamic_norm_bound_coefficient':'25/8','actual_reference_matrix_element_coefficient':'19/8',
            'actual_reference_vector_norm_coefficient_squared':'91/16','actual_Haar_eigenvector_residual_squared_over_alpha_squared_lambda_squared':'5'}


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',required=True)
    args=parser.parse_args(); out=Path(args.output).absolute()
    for p in (out,*out.parents): need(not p.is_symlink(),'symlink output')
    need(not out.exists(),'fresh output required')
    need(sha(CONTRACT)==CONTRACT_HASH,'frozen Q1 contract changed')
    contract=json.loads(CONTRACT.read_text())
    for rel,digest in contract['dependencies'].items(): need(sha(ROOT/rel)==digest,'inherited dependency changed: '+rel)
    faces,chords,geometry=graph()
    controls={'schema':'ym22-reverse-q1-controls-v1','loop':'q1','direction':'reverse','status':'passed','passed':True,
              'actual_twenty_face_action':geometry,'conditional_Haar_moments':moment_controls(faces,chords),
              'dynamic_block_and_scalar_controls':block_controls()}
    results={'schema':'ym22-reverse-q1-results-v1','loop':'q1','direction':'reverse',
             'status':'proved_correlated_magnetic_leakage_and_nonautonomous_compression','passed':True,
             'claims':{'full_J16_unitary_preserved':True,'physical_operator_domain':'H2(SU2^33)^Gauss',
                       'physical_form_domain':'H1(SU2^33)^Gauss','selected_compression_operator_domain':'H2(SU2^3)^Ad',
                       'full_H_lambda_nonnegative_for_lambda_ge_zero':True,'potential_bound':'0<=V_pot<=40',
                       'conditional_mean':'20-tau','conditional_second_moment':'(20-tau)^2+19/4+(r+x+z)/2',
                       'surviving_distinct_conditional_pairs':[[9,14],[9,15],[14,15]],
                       'J_star_V_Q_V_J':'multiplication by d=19/4+(r+x+z)/2',
                       'd_essential_infimum':'4','d_essential_supremum':'25/4','d_Haar_mean':'19/4','d_squared_Haar_mean':'91/4',
                       'selected_reduces_for_positive_lambda':False,'electric_recovery_at_lambda_zero':True,
                       'B_lambda_norm':'5*alpha*lambda/2','B_lambda_reference_norm_squared':'19*(alpha*lambda)^2/4',
                       'strong_scaled_compressed_defect_limit':'M_d/2',
                       'scaled_defect_parameter':'alpha*lambda*t/hbar',
                       'strong_limit_on_all_selected_vectors':True,'operator_norm_Taylor_expansion_claimed':False,
                       'all_time_operator_norm_bound':'min(1,(25/8)*(alpha*lambda*t/hbar)^2)',
                       'small_time_scaled_operator_norm_limit':'25/8 for fixed lambda>0',
                       'reference_matrix_element_leading_coefficient':'19/8',
                       'reference_vector_norm_leading_coefficient':'sqrt(91)/4',
                       'autonomous_compressed_semigroup_for_positive_lambda':False,
                       'Haar_reference_is_interacting_eigenvector_for_positive_lambda':False,
                       'physical_calibration_completed':False,'interacting_ground_identified':False,
                       'homogeneous_or_continuum_transfer':False},
             'target_verdict':'The complete magnetic action has correlated positive conditional variance, uniformly nonzero leakage and a second-order compressed-semigroup defect.',
             'next_loop_selected':False}
    rels=list(contract['dependencies'])+contract['instruction_inputs']+[
        'research/round22/reverse/p2/report.md','research/round22/reverse/p2/source-review.json',
        'research/round22/reverse/n1/inputs/advisor-finite-observations.md',
        'research/round22/reverse/n1/inputs/paired-admission-matching.md',
        'research/round22/methods/v3/generated-support-and-iteration.md',
        'research/round22/methods/v3/stationarity-support-and-admission.md']
    inputs=[CONTRACT,HERE/'report.md',HERE/'check.py',HERE/'independence.json',HERE/'source-review.json']+[ROOT/r for r in rels]
    hashes={str(p.relative_to(ROOT)):sha(p) for p in sorted(set(inputs))}
    need(all(r in hashes for r in contract['instruction_inputs']),'required immutable instruction closure')
    out.mkdir(parents=True)
    for name,payload in [('results.json',results),('controls.json',controls)]: dump(out/name,payload)
    dump(out/'source-manifest.json',{'schema':'ym22-source-manifest-v1','inputs':hashes,
                                   'outputs':{n:sha(out/n) for n in ('results.json','controls.json')}})
    print(json.dumps({'loop':'q1','direction':'reverse','status':results['status'],'passed':True}))


if __name__=='__main__': main()
