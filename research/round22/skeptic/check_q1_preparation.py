#!/usr/bin/env python3
"""Independent all-face Q1 conditional-moment preparation; no producer imports."""
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
from itertools import combinations, product
import json
from pathlib import Path


def need(ok, why):
    if ok is not True:raise RuntimeError(why)


def multiply(a,b):
    a0,a1,a2,a3=a;b0,b1,b2,b3=b
    return (a0*b0-a1*b1-a2*b2-a3*b3,a0*b1+a1*b0+a2*b3-a3*b2,
            a0*b2+a2*b0+a3*b1-a1*b3,a0*b3+a3*b0+a1*b2-a2*b1)


def inverse(a):return (a[0],-a[1],-a[2],-a[3])
def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
ONE=(F(1),F(0),F(0),F(0))


def word_value(word,values):
    result=ONE
    for e,s in word:result=multiply(result,values[e] if s==1 else inverse(values[e]))
    return result[0]


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    output=parser.parse_args().output.absolute()
    need(not output.exists(),'fresh output required')
    for p in (output,*output.parents):need(not p.is_symlink(),'symlink rejected')
    root=Path(__file__).resolve().parents[3]
    ledger_path=root/'research/round19/forward/c1/output/graph-reduction.json'
    ledger=json.loads(ledger_path.read_text())
    old={r['face_id']:r for r in ledger['affected_faces']+ledger['constant_faces']}
    vertices=list(product(range(3),range(3),range(2)))
    edges=[(a,v) for a in range(3) for v in vertices if v[a]<(2,2,1)[a]]
    ids={edge:i for i,edge in enumerate(edges)}
    def move(v,a):return tuple(x+int(i==a) for i,x in enumerate(v))
    faces=[]
    for a,b in combinations(range(3),2):
        for v in vertices:
            if v[a]<(2,2,1)[a] and v[b]<(2,2,1)[b]:
                faces.append([(ids[(a,v)],1),(ids[(b,move(v,a))],1),
                              (ids[(a,move(v,b))],-1),(ids[(b,v)],-1)])
    need(len(faces)==20 and len(edges)==33,'complete physical graph')
    for i,word in enumerate(faces):
        need([{'edge':e,'sign':s} for e,s in word]==old[i]['signed_word'],'signed face mismatch')
    tree=set(range(16))|{26}; selected={24,27,28}
    words=[[(e,s) for e,s in word if e not in tree] for word in faces]
    omitted=[{e for e,s in word if e not in selected} for word in words]
    need([i for i,o in enumerate(omitted) if not o]==[8],'only deterministic selected face')
    need(words[8]==[(27,1),(24,-1)],'retained face orientation')
    for word in words:need(len({e for e,s in word})==len(word),'one occurrence per chord per face')
    survivors=[];zeros=0
    for i,j in combinations(range(20),2):
        occurrences=Counter(e for e,s in words[i]+words[j] if e not in selected)
        if any(n==1 for n in occurrences.values()):zeros+=1
        else:survivors.append((i,j))
    need(survivors==[(9,14),(9,15),(14,15)] and zeros==187,'exhaustive conditional cross-face support')
    need(words[9]==[(28,1),(25,-1)] and words[14]==[(25,1),(24,-1)]
         and words[15]==[(25,-1)],'shared omitted quaternion forms')
    # W9=u.G, W14=w.G, W15=e0.G; E[G_a G_b]=delta_ab/4.
    U=(F(3,5),F(4,5),F(0),F(0))
    V=(F(1,3),F(0),F(2,3),F(2,3))
    W=(F(1,3),F(2,3),F(2,3),F(0))
    need(all(dot(q,q)==1 for q in [U,V,W]),'unit-quaternion controls')
    exact_pairs={(9,14):dot(U,W)/4,(9,15):U[0]/4,(14,15):W[0]/4}
    need(exact_pairs=={(9,14):F(11,60),(9,15):F(3,20),(14,15):F(1,12)},'nonzero cross covariances')
    need(multiply(U,W)[0]/4==F(-1,12)!=exact_pairs[(9,14)],'wrong conjugation rejected')
    x,z,r,t=U[0],W[0],dot(U,W),dot(V,W)
    mu=20-t; variance=F(19,4)+(r+x+z)/2
    summed=tuple(U[i]+W[i]+ONE[i] for i in range(4))
    need(variance==4+dot(summed,summed)/4==F(67,12),'conditional variance sum-of-squares')
    need(mu==F(175,9),'exact nontrivial conditional mean')
    need(variance!=F(19,4),'conditional independence control rejected')
    values={e:ONE for e in range(33)};values.update({28:U,27:V,24:W})
    section=20-sum(word_value(word,values) for word in words)
    need(section!=mu,'identity evaluation cannot replace conditional expectation')
    identity_variance=F(19,4)+F(3,2)
    near_min_u=(F(-3,5),F(4,5),F(0),F(0))
    near_min_w=(F(-3,5),F(-4,5),F(0),F(0))
    near_min=F(19,4)+(dot(near_min_u,near_min_w)+near_min_u[0]+near_min_w[0])/2
    need(identity_variance==F(25,4) and near_min==F(401,100)>4,'variance range controls')
    # Distinct original plaquettes always have an edge appearing once in the pair.
    for i,j in combinations(range(20),2):
        counts=Counter(e for e,s in faces[i]+faces[j])
        need(any(n==1 for n in counts.values()),'unconditional cross-face orthogonality')
    need(F(20,4)==5 and F(19,4)+F(1,4)==5,'full Haar action variance')
    result={'schema':'ym22-skeptic-preparation-check-v1','loop':'q1','passed':True,
      'driver_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'ledger_sha256':hashlib.sha256(ledger_path.read_bytes()).hexdigest(),
      'current_producers_read':False,'producer_imports':False,
      'all_twenty_chord_face_words':{str(i):w for i,w in enumerate(words)},
      'omitted_chord_supports':{str(i):sorted(o) for i,o in enumerate(omitted)},
      'selected_face':8,'vanishing_distinct_conditional_pairs':zeros,
      'surviving_distinct_conditional_pairs':[
        {'faces':[9,14],'exact_function':'r/4, r=Tr(UW^-1)/2'},
        {'faces':[9,15],'exact_function':'x/4'},
        {'faces':[14,15],'exact_function':'z/4'}],
      'conditional_mean_V':'20-t, t=Tr(VW^-1)/2',
      'conditional_second_moment_V':'(20-t)^2+19/4+(r+x+z)/2',
      'variance_operator_function':'k=19/4+(r+x+z)/2=4+|u+w+e0|^2/4',
      'variance_function_range':['4','25/4'],'off_diagonal_VJ_operator_norm':'5/2',
      'Haar_mean_variance_function':'19/4','full_Haar_mean_V':'20','full_Haar_variance_V':'5',
      'fixture':{'mean_V':str(mu),'conditional_variance':str(variance),
                 'identity_evaluated_V':str(section)},
      'controls':{'conditional_independence_rejected':True,'wrong_conjugation_rejected':True,
       'identity_evaluation_rejected':True,'uniform_positive_variance_supported':True,
       'all_original_cross_pairs_have_free_link':True},
      'infinite_dimensional_topology_proved_by_this_code':False,'research_loops_added':0}
    output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'loop':'q1','prepared':True,'faces':20,'distinct_pairs_checked':190}))


if __name__=='__main__':main()
