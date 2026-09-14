#!/usr/bin/env python3
"""Independent P2 preparation: fixed tree, every cut, mobility moments and reserve."""
import argparse
from collections import deque
from fractions import Fraction as F
import hashlib
from itertools import combinations, product
import json
from math import comb, factorial
from pathlib import Path


def need(value, why):
    if value is not True:
        raise RuntimeError(why)


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',type=Path,required=True)
    output=parser.parse_args().output.absolute()
    need(not output.exists(),'fresh output required')
    for p in (output,*output.parents):need(not p.is_symlink(),'symlink rejected')
    root=Path(__file__).resolve().parents[3]
    ledger_path=root/'research/round19/forward/c1/output/graph-reduction.json'
    ledger=json.loads(ledger_path.read_text())
    vertices=list(product(range(3),range(3),range(2)))
    edges=[(axis,v,tuple(x+int(i==axis) for i,x in enumerate(v)))
           for axis in range(3) for v in vertices if v[axis]<(2,2,1)[axis]]
    need(len(edges)==33,'actual full graph')
    edge_ids={(axis,s):i for i,(axis,s,t) in enumerate(edges)}
    def shift(v,a):return tuple(x+int(i==a) for i,x in enumerate(v))
    faces=[]
    for a,b in combinations(range(3),2):
        for v in vertices:
            if v[a]<(2,2,1)[a] and v[b]<(2,2,1)[b]:
                faces.append([(edge_ids[(a,v)],1),(edge_ids[(b,shift(v,a))],1),
                              (edge_ids[(a,shift(v,b))],-1),(edge_ids[(b,v)],-1)])
    reference={r['face_id']:r for r in ledger['affected_faces']+ledger['constant_faces']}
    for i,word in enumerate(faces):
        need([{'edge':e,'sign':s} for e,s in word]==reference[i]['signed_word'],
             'signed graph mismatch')
    tree=set(range(16))|{26}; chords=sorted(set(range(33))-tree)
    selected=[28,27,24]; origin=(0,2,0)
    adjacency={v:[] for v in vertices}
    for i in tree:
        a,s,t=edges[i];adjacency[s].append((t,i,1));adjacency[t].append((s,i,-1))
    paths={origin:[]};queue=deque([origin])
    while queue:
        v=queue.popleft()
        for w,i,sign in adjacency[v]:
            if w not in paths:paths[w]=paths[v]+[(i,sign)];queue.append(w)
    need(len(paths)==18 and len(tree)==17 and len(chords)==16,'genuine full tree')
    need(set(selected).issubset(chords),'selected variables are chords')
    loops={}
    for e in chords:
        a,s,t=edges[e]
        loops[e]=paths[s]+[(e,1)]+[(i,-sign) for i,sign in reversed(paths[t])]
        need(sum(i==e for i,sign in loops[e])==1,'exclusive chord Haar variable')
    need([len(loops[e]) for e in selected]==[6,8,6],'new observable completions')
    need(loops[28]!=faces[9],'old section equality is not physical equality')
    cuts=[]
    for e in sorted(tree):
        branch={v for v,path in paths.items() if any(i==e for i,sign in path)}
        epsilon=next(sign for path in paths.values() for i,sign in path if i==e)
        coeff={str(j):[epsilon*int(edges[j][1] in branch),
                       -epsilon*int(edges[j][2] in branch)] for j in chords}
        need(len(coeff)==16,'all chord incidences retained')
        cuts.append({'tree_edge':e,'epsilon':epsilon,'branch':sorted(branch),
                     'left_right_coefficients':coeff})
    # On a one-link class function, left and right derivatives agree.
    effective_lengths=[]
    for e in selected:
        length=1+sum(sum(row['left_right_coefficients'][str(e)])**2 for row in cuts)
        effective_lengths.append(length)
    need(effective_lengths==[6,8,6],'all tree derivatives reproduce loop energy')
    # A shared cut must act on V and W together, retaining its cross derivative.
    row12=next(r for r in cuts if r['tree_edge']==12)
    need(row12['left_right_coefficients']['27']==[-1,0] and
         row12['left_right_coefficients']['24']==[-1,0], 'shared left derivative')
    row13=next(r for r in cuts if r['tree_edge']==13)
    need(row13['left_right_coefficients']['27']==[0,1] and
         row13['left_right_coefficients']['24']==[0,1], 'shared right derivative')
    moment=lambda n:F(0) if n%2 else F(comb(n,n//2),(n//2+1)*2**n)
    mean_x2=moment(2);variance_x2=moment(4)-mean_x2**2
    need((mean_x2,variance_x2)==(F(1,4),F(1,16)),'Haar moments')
    ex,ey,ez=[F(3,4)*n for n in effective_lengths]
    fit=ex/F(3,4)
    need((ex,ey,ez,fit)==(F(9,2),F(6),F(9,2),F(6)), 'training clock')
    physical_curvature=ex**2/4
    conditional_constant=fit**2*F(9,64)
    conditional_zeta2=fit**2*variance_x2
    need(physical_curvature==conditional_constant==F(81,16), 'curvature constant')
    need(conditional_zeta2==F(9,4)>0,'reserved curvature forces zeta zero')
    need(F(3,4)*fit!=ey, 'y remains mismatched after reserved curvature')
    need(F(4)!=fit, 'old P1 clock reuse rejected')
    # e^{-1/2} from a positive series and geometric tail, independent of exp floats.
    N=30; half=F(1,2)
    s=sum((half**k/F(factorial(k)) for k in range(N+1)),F(0))
    tail=half**(N+1)/F(factorial(N+1))/(1-half/F(N+2))
    lo,hi=1/(s+tail),1/s
    dlo,dhi=(lo**9-hi**12)/4,(hi**9-lo**12)/4
    interval=['0.0021575610903939','0.0021575610903941']
    need(F(interval[0])<dlo<dhi<F(interval[1]),'reserved common-time discrepancy')
    # Omitting the divergence drift leaves a nonzero Haar mean on x.
    need(F(3,4)*moment(2)==F(3,16)>0,'missing-mobility-drift control')
    result={'schema':'ym22-skeptic-preparation-check-v1','loop':'p2','passed':True,
      'driver_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'ledger_sha256':hashlib.sha256(ledger_path.read_bytes()).hexdigest(),
      'current_producers_read':False,'producer_imports':False,'research_loops_added':0,
      'tree_edges':sorted(tree),'root':origin,'chords':chords,
      'all_twenty_signed_faces_match':True,
      'tree_paths':{str(v):paths[v] for v in vertices},
      'all_chord_loop_words':loops,'all_tree_cut_coefficients':cuts,
      'selected_lengths':effective_lengths,'selected_energies_over_alpha':list(map(str,[ex,ey,ez])),
      'training_c_over_alpha':str(fit),
      'physical_training_curvature_times_hbar_squared_over_alpha_squared':str(physical_curvature),
      'conditional_training_curvature_same_units':'81/16+(9/4)*zeta^2',
      'reserved_curvature_match_zeta':'0',
      'y_physical_correlation':'exp(-6 alpha t/hbar)/4',
      'y_conditional_correlation_after_reserve':'exp(-(9/2) alpha t/hbar)/4',
      'conditional_minus_physical_at_t_star':'(exp(-9/2)-exp(-6))/4',
      'strict_difference_interval':interval,
      'controls':{'full_tree_required':True,'changed_completion_detected':True,
       'cross_derivatives_retained':True,'old_P1_clock_rejected':True,
       'nonzero_mobility_curvature_rejected':True,'missing_divergence_drift_rejected':True,
       'held_y_match_rejected':True},
      'scope':'Independent preparation, not a producer verdict or a six-loop reassessment'}
    output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'loop':'p2','prepared':True,'tree_cuts':len(cuts),'chords':len(chords)}))


if __name__=='__main__':main()
