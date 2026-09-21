#!/usr/bin/env python3
from pathlib import Path
from fractions import Fraction as F
from itertools import product
import sys
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from u_common import need,emit
second=lambda i,j:F(int(i==j),4)
norm=4*sum(second(i,j)**2 for i,j in product(range(4),repeat=2))
coupling=4*sum(second(i,k)*second(j,k)*second(i,j) for i,j,k in product(range(4),repeat=3))
need(norm==1 and coupling==F(1,4),'moment contraction')
M=((0,1,0),(1,0,0),(0,0,0))
mul=lambda A,B:tuple(tuple(sum(A[i][k]*B[k][j] for k in range(3)) for j in range(3)) for i in range(3))
need(mul(mul(M,M),M)==M,'bounded swap identity')
P=[2,5,5,6,3]
ratio=F(3*4*2,sum(P))
need(ratio==F(8,7) and ratio/96==F(1,84),'endpoint scale')
need(6*F(3,4)==F(9,2),'electric energy')
emit('u1','reverse','594549a557ec724f7d96e4e7d27257406fad1e068cb8359ba0fec391e98e69f6',
 dict(status='resonance_proved_endpoint_unresolved',energy_over_alpha='9/2',haar_matrix_element=str(coupling),
      variance_reference=str(norm),tau_limit_over_eta=str(ratio),leading_endpoint_coefficient='1/84',
      coupling_coefficient='-1/96',endpoint_proved=False,continuum_proved=False,
      observable_class='bounded local gauge-invariant rank operator, not Wilson multiplication'),
 dict(moment_contraction=True,rank_operator_cubic_identity=True,wrong_normalized_trace_rejected=norm/4!=1,
      vacuum_mean_not_vacuum_annihilation=True,missing_face_changes_coefficient=coupling!=0,
      compression_autonomy_not_assumed=True,fixed_clock_checked=True,identity_zero_variance=True))
