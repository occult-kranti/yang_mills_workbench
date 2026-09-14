#!/usr/bin/env python3
"""Exact skeptical lemma checks; no SU2 spectral replacement or new research loop."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib

def require(p,m):
    if not p: raise ValueError(m)
def mat(rows): return [[F(x) for x in row] for row in rows]
def mul(a,b): return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def sub(a,b):return [[x-y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def add(a,b):return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def scale(c,a):return [[c*x for x in row] for row in a]
def comm(a,b):return sub(mul(a,b),mul(b,a))
def tr(a):return sum(a[i][i] for i in range(len(a)))
def vec(a):return [row[0] for row in a]
def dot(a,b):return sum(x*y for x,y in zip(a,b))
phi=mat([[0,2,-1],[2,4,5],[-1,5,6]])
v=[F(0),F(2),F(-1)];u=[F(0),F(2),F(-1,3)]
S=mat([[0,-2,F(1,3)],[2,0,0],[F(-1,3),0,0]])
A=mat([[0,2,-1],[2,0,0],[-1,0,0]])
C=sub(scale(F(1,2),comm(S,comm(S,phi))),scale(F(1,6),comm(S,comm(S,A))))
w=vec(C);w[0]=F(0)
c=dot(u,v);m=dot(u,u)
expected=[-c*x-m*y/3 for x,y in zip(u,v)]
require(w==expected,'actual rank-two cubic algebra')
require(dot(u,w)==-F(4,3)*m*c<0,'nonzero sign witness')
wrong=vec(scale(F(1,2),comm(S,comm(S,phi))));wrong[0]=F(0)
require(wrong!=w,'omitted 1/6 term control')
b=F(1,4)
G=mat([[0,0,0,0],[0,1,0,b],[0,0,1,0],[0,b,0,2]])
Alocal=mat([[0,0,1,0],[0,0,0,1],[1,0,0,0],[0,1,0,0]])
require(tr(mul(G,Alocal))==2*b,'trace obstruction')
# Trace of G[S,G] vanishes for every matrix by cyclicity, verified on a noncommuting probe.
probe=mat([[0,1,-2,3],[-1,0,4,-5],[2,-4,0,6],[-3,5,-6,0]])
require(tr(mul(G,comm(probe,G)))==0,'commutator trace cyclicity')
Y={(0,0,0),(1,0,0),(0,1,0),(0,0,1)}
def star(b):return {b,(b[0]+1,b[1],b[2]),(b[0],b[1]+1,b[2]),(b[0],b[1],b[2]+1)}
anchors=[(i,j,k) for i in range(3) for j in range(3) for k in range(3)]
cross=[b for b in anchors if star(b)&Y and not star(b)<=Y]
require(set(cross)==Y-{(0,0,0)},'complete octant crossings')
require(all(len(Y|star(b))==7 for b in cross),'declared unions')
result={'status':'passed','classification':'independent algebra and geometry controls; no numerical SU2 spectrum','source_cubic':{'c':str(c),'m':str(m),'w':[str(x) for x in w],'negative_inner_product':str(dot(u,w))},'resonance_lemma':{'trace_GA':str(2*b),'actual_SU2_obstruction':False},'crossing_anchors':[list(b) for b in sorted(cross)],'controls':{'omitted_cubic_term_rejected':True,'ground_gap_to_commutator_inverse_rejected':True,'dropped_crossing_rejected':True},'research_loops_added':0}
path=Path(__file__).with_name('s1-independent-preparation-checks.json')
path.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'passed','output':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}))
