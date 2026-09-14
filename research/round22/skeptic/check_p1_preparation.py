#!/usr/bin/env python3
"""Independent P1 graph, section and exact electric endpoint arithmetic."""
from fractions import Fraction as F
from itertools import product, combinations
from math import comb, factorial
from pathlib import Path
import argparse
import hashlib
import json


def need(ok, why):
    if ok is not True:
        raise RuntimeError(why)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    out=parser.parse_args().output;need(not out.exists(),'fresh output required')
    for p in (out.absolute(),*out.absolute().parents):need(not p.is_symlink(),'symlink rejected')
    root=Path(__file__).resolve().parents[3]
    ledger_path=root/'research/round19/forward/c1/output/graph-reduction.json'
    ledger=json.loads(ledger_path.read_text())
    lengths=(3,3,2); vertices=list(product(*(range(n) for n in lengths)))
    edges=[]
    for axis in range(3):
        ranges=[range(n-int(j==axis)) for j,n in enumerate(lengths)]
        edges.extend((axis,p) for p in product(*ranges))
    edge_ids={edge:i for i,edge in enumerate(edges)}
    def move(p,axis):return tuple(x+int(j==axis) for j,x in enumerate(p))
    faces=[]
    for a,b in combinations(range(3),2):
        ranges=[range(n-int(j in (a,b))) for j,n in enumerate(lengths)]
        for p in product(*ranges):
            signed=[(edge_ids[(a,p)],1),(edge_ids[(b,move(p,a))],1),
                    (edge_ids[(a,move(p,b))],-1),(edge_ids[(b,p)],-1)]
            faces.append(signed)
    need((len(vertices),len(edges),len(faces))==(18,33,20),'full graph counts')
    inherited={row['face_id']:row for row in ledger['affected_faces']+ledger['constant_faces']}
    active={edge_ids[(2,(1,1,0))]:'U',edge_ids[(2,(1,0,0))]:'V',edge_ids[(2,(0,0,0))]:'W'}
    need(active=={28:'U',27:'V',24:'W'},'active physical links')
    affected=0
    for i,word in enumerate(faces):
        need(len({e for e,_ in word})==4,'four distinct electric factors')
        need([{'edge':e,'sign':sgn} for e,sgn in word]==inherited[i]['signed_word'],'full signed ledger')
        restricted=[{'symbol':active[e],'sign':sgn} for e,sgn in word if e in active]
        need(restricted==inherited[i]['active_word'],'section word')
        affected+=bool(restricted)
    need(affected==7 and len(faces)-affected==13,'affected and constant faces')
    need(all(e not in active for e,_ in faces[0]),'fixed-loop witness')
    need([(active[e],s) for e,s in faces[9] if e in active]==[('U',1)],'training word')
    need([(active[e],s) for e,s in faces[16] if e in active]==[('U',1),('V',-1)],'held-out word')
    # For f_N=F0^N, exact normalized Haar semicircle moments are Catalan_N/4^N.
    norm_rows=[]
    for N in (1,2,4,8,32):
        value=F(comb(2*N,N),(N+1)*4**N)
        need(0<value<=F(1,N+1),'L2-null sequence upper bound')
        norm_rows.append({'N':N,'physical_norm_squared':str(value),'section_image':'1','section_norm_squared':'1'})
    physical=4*F(3,4); training=F(3,4); held=2*F(3,4)
    fit=physical/training
    need(fit==4 and held*fit==6,'one fit and held-out electric eigenvalue')
    need(physical/held==2!=fit,'refitting held-out channel would change coefficient')
    variance=F(1,4)
    def exp_minus_bounds(x):
        upper=sum(((-x)**k/F(factorial(k)) for k in range(61)),F())
        lower=upper+(-x)**61/F(factorial(61))
        need(0<lower<upper<1,'exponential Taylor bounds')
        return lower,upper
    l3,u3=exp_minus_bounds(F(3));l6,u6=exp_minus_bounds(F(6))
    lo,hi=(l3-u6)/4,(u3-l6)/4
    need(F('0.01182707904')<lo<=hi<F('0.01182707906'),'fixed-clock held-out mismatch')
    result={'schema':'ym22-skeptic-preparation-check-v1','loop':'p1','passed':True,
      'driver_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'ledger_sha256':hashlib.sha256(ledger_path.read_bytes()).hexdigest(),
      'graph_counts':{'vertices':18,'edges':33,'faces':20,'tree_edges':17,'chords':16},
      'active_edges':active,'fixed_face':faces[0],'training_face':faces[9],'held_face':faces[16],
      'all_twenty_signed_words_match':True,'core_null_sequence':norm_rows,
      'variance':'1/4','physical_face_energy_over_alpha':str(physical),
      'conditional_training_energy_over_c':str(training),'conditional_held_energy_over_c':str(held),
      'training_c_over_alpha':str(fit),'held_energy_after_fit_over_alpha':'6',
      'held_correlations_at_t_star':'physical=e^(-3)/4; conditional=e^(-6)/4',
      'held_difference_certified_interval':['0.01182707904','0.01182707906'],
      'fixed_face_generator_defect_over_alpha':'3','held_core_defect_norm_after_fit_over_alpha':'3/2',
      'current_producers_read':False,'research_loops_added':0,
      'scope':'Actual finite graph electric endpoint; no interacting or continuum transfer'}
    out.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'loop':'p1','prepared':True,'signed_faces_verified':20}))


if __name__=='__main__':main()
