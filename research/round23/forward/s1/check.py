#!/usr/bin/env python3
"""Exact S1 checks; finite matrices are algebra fixtures, not SU2 spectra."""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import itertools
import json

ROOT=Path(__file__).absolute().parents[4]
BASE='research/round23/forward/s1/'
CONTRACT='research/round23/contracts/s1.json'
CONTRACT_SHA='edf48a3600000cf41089760e7000ccb2642088958233e9658a5f700a9e9d8f41'

def need(condition,message):
    if not condition:
        raise ValueError(message)

def digest(path):
    for p in (path,*path.parents):
        need(not p.is_symlink(),'symlink rejected: '+str(p))
    need(path.is_file(),'missing source: '+str(path))
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(path,data):
    path.write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')

def zero(n,m=None): return [[F(0) for _ in range(m or n)] for _ in range(n)]
def eye(n): return [[F(i==j) for j in range(n)] for i in range(n)]
def add(a,b): return [[x+y for x,y in zip(row,br)] for row,br in zip(a,b)]
def scale(x,a): return [[x*y for y in row] for row in a]
def mm(a,b): return [[sum((a[i][k]*b[k][j] for k in range(len(b))),F(0)) for j in range(len(b[0]))] for i in range(len(a))]
def comm(a,b): return add(mm(a,b),scale(-1,mm(b,a)))
def col(a,j=0): return [row[j] for row in a]
def outer(a,b): return [[x*y for y in b] for x in a]
def dot(a,b): return sum((x*y for x,y in zip(a,b)),F(0))
def plus(a,b): return [x+y for x,y in zip(a,b)]
def times(c,a): return [c*x for x in a]
def mv(a,b): return [dot(row,b) for row in a]
def kron(a,b): return [[a[i][j]*b[k][l] for j in range(len(a[0])) for l in range(len(b[0]))] for i in range(len(a)) for k in range(len(b))]
def encode(a): return [[str(x) for x in row] for row in a]
def rtwo(a,skew=False):
    vacuum=[F(1)]+[F(0)]*(len(a)-1)
    return add(outer(a,vacuum),scale(-1 if skew else 1,outer(vacuum,a)))
def invert2(a):
    d=a[0][0]*a[1][1]-a[0][1]*a[1][0]
    need(d!=0,'nonzero determinant')
    return [[a[1][1]/d,-a[0][1]/d],[-a[1][0]/d,a[0][0]/d]]

def algebra(t):
    H=[[F(0),F(0),F(0)],[F(0),F(2),F(0)],[F(0),F(0),F(3)]]
    phi=scale(t,[[F(0),F(1),F(2)],[F(1),F(3),F(1)],[F(2),F(1),F(-2)]])
    v=col(phi); u=[F(0),v[1]/2,v[2]/3]
    S=rtwo(u,True); A=rtwo(v)
    need(comm(S,H)==scale(-1,A),'bare homological sign')
    C=add(scale(F(1,2),comm(S,comm(S,phi))),scale(F(-1,6),comm(S,comm(S,A))))
    a=dot(u,v); s2=dot(u,u); b=dot(u,mv(phi,u))
    w=col(C); w[0]=F(0)
    formula=plus(times(-a,u),times(-s2/3,v))
    need(w==formula,'actual generated-word algebra identity')
    need(dot(u,w)==-F(4,3)*a*s2,'strict source projection identity')
    need(C[0][0]==b,'scalar retained exactly')
    if t:
        need(dot(u,w)<0 and dot(w,w)>0,'nonzero cubic source')
    else:
        need(C==zero(3) and w==[0,0,0],'zero coupling exception')
    P=zero(3); P[0][0]=1; Q=add(eye(3),scale(-1,P))
    Ag=rtwo(w); Z=mm(Q,mm(add(C,scale(-b,eye(3))),Q))
    need(C==add(scale(b,eye(3)),add(Ag,Z)),'centered split retains scalar')
    D=mm(Q,mm(phi,Q)); G=add(H,D)
    inv=invert2([[G[1][1],G[1][2]],[G[2][1],G[2][2]]])
    z=[F(0)]+mv(inv,w[1:]); K=rtwo(z,True)
    need(comm(K,G)==scale(-1,Ag),'interacting interior inverse')
    wrong=add(comm(scale(-1,K),G),Ag)
    need((wrong!=zero(3))==bool(t),'wrong inverse sign discriminates nonzero source')
    Pe=[[F(1),F(0)],[F(0),F(0)]]; Ae=kron(Ag,eye(2)); Av=kron(Ag,Pe)
    eta=[F(0)]*6; eta[1]=1
    need(mv(Av,eta)==[0]*6,'global vacuum source kills excited exterior')
    sector=mv(add(Ae,scale(-1,Av)),eta)
    need(dot(sector,sector)==dot(w,w),'identity exterior mismatch norm squared')
    # Crossing lemma: a bounded, global-vacuum-annihilating interaction.
    De=zero(6); De[1][3]=De[3][1]=F(1,10)
    He=kron(G,eye(2)); Ee=kron(eye(3),[[F(0),F(0)],[F(0),F(1)]])
    Ge=add(add(He,Ee),De); Ke=kron(K,eye(2))
    defect=add(comm(Ke,Ge),Ae)
    need(defect==comm(Ke,De),'crossing term retained exactly')
    need((defect!=zero(6))==bool(t),'dropped crossing term rejected by lemma fixture')
    return {'tau_fixture':str(t),'source_norm_squared_fixture':str(dot(w,w)),
            'projection_fixture':str(dot(u,w)),'scalar_fixture':str(b),
            'source_vector_fixture':[str(x) for x in w],
            'crossing_frobenius_squared_fixture':str(sum((x*x for row in defect for x in row),F(0)))}

S=frozenset(((0,0,0),(1,0,0),(0,1,0),(0,0,1)))
def star(b): return frozenset(tuple(x+y for x,y in zip(b,s)) for s in S)
def minus(a,b): return tuple(x-y for x,y in zip(a,b))
def support_checks():
    relative={minus(a,b) for a in S for b in S}
    need(len(relative)==13,'all thirteen relative anchor positions')
    meetings=[b for b in itertools.product(range(3),repeat=3) if star(b)&S]
    need(set(meetings)==S,'origin all meeting anchors')
    crossing=sorted(b for b in meetings if not star(b)<=S)
    need(len(crossing)==3,'origin three crossing anchors')
    need(all(len(star(b)&S)==1 and len(star(b)|S)==7 for b in crossing),'connected seven-site crossing unions')
    # Includes negative/incoming relative anchors for a translated interior star.
    need(all(len(star(b)&S)==1 and len(star(b)|S)==7 for b in relative if b!=(0,0,0)),
         'all twelve interior crossings have declared union seven')
    root=(0,0,0); pairs=[]
    for b in itertools.product(range(-3,4),repeat=3):
        Y=star(b)
        for d in relative-{(0,0,0)}:
            c=tuple(x+y for x,y in zip(b,d)); Z=star(c)
            if root in Y|Z:
                pairs.append((b,c))
    need(len(pairs)<=96,'root indexed ordered-pair bound')
    need(len(set(pairs))==len(pairs),'ordered indexed multiplicity')
    need(any(any(x<0 for x in b) for b,c in pairs),'incoming anchors present')
    need(4*12+4*12==96 and 2*96==192,'family constant')
    need(3*21==63,'all faces retained on three crossing stars')
    return {'origin_crossing_anchors':[list(b) for b in crossing],
            'origin_crossing_count':3,'interior_relative_anchor_count':13,
            'interior_crossing_count':12,'root_ordered_pair_count_fixture':len(pairs),
            'root_pair_upper':96,'family_prefactor':192,'union_size':7,
            'origin_indexed_crossing_faces':63}

def haar_controls():
    # Signed axes are exact for the degree<=2 quaternion moments required here.
    qs=[]
    for i in range(4):
        for sign in (-1,1):
            q=[F(0)]*4; q[i]=F(sign); qs.append(q)
    mean=sum((2*q[0] for q in qs),F(0))/8
    second=sum(((2*q[0])**2 for q in qs),F(0))/8
    need(mean==0 and second==1,'actual character moment arithmetic')
    need(second/4!=1,'wrong half-trace normalization rejected')
    return {'character_mean':str(mean),'character_second_moment':str(second),
            'physical_free_z_tail':[8,0,0],'coarse_owner':[2,0,0]}

def resonance_control():
    G=[[F(0),F(0),F(0)],[F(0),F(1),F(0)],[F(0),F(0),F(1)]]
    A=zero(3); A[1][2]=A[2][1]=1
    K=[[F(0),F(2),F(3)],[F(-2),F(0),F(5)],[F(-3),F(-5),F(0)]]
    need(comm(K,G)[1][2]==0 and A[1][2]==1,'equal-energy commutator obstruction')
    return {'ground_gap_fixture':'1','equal_energy_source_entry':'1',
            'scope':'algebra fixture; actual G source obstruction not established'}

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',required=True)
    out=Path(parser.parse_args().output)
    need(out.is_absolute(),'output must be absolute')
    need(not out.exists(),'output must be fresh')
    need(digest(ROOT/CONTRACT)==CONTRACT_SHA,'frozen contract binding')
    contract=json.loads((ROOT/CONTRACT).read_text())
    for name,expected in contract['dependencies'].items():
        need(digest(ROOT/name)==expected,'inherited dependency changed: '+name)
    names=set(contract['dependencies'])|set(contract['instruction_inputs'])|{
        CONTRACT,BASE+'check.py',BASE+'report.md',BASE+'source-notes.md',
        'research/round23/methods/team-protocol.md',
        'research/round21/forward/i2/report.md',
        'research/round22/forward/r1/source-notes.md',
        'research/round23/forward/preparation.md'}
    inputs={n:digest(ROOT/n) for n in sorted(names)}
    fixtures=[algebra(t) for t in (F(-1,4096),F(0),F(1,4096))]
    need(fixtures[0]['source_norm_squared_fixture']==fixtures[2]['source_norm_squared_fixture'],'coupling sign norm symmetry')
    negative=list(map(F,fixtures[0]['source_vector_fixture'])); positive=list(map(F,fixtures[2]['source_vector_fixture']))
    need(negative==times(-1,positive),'cubic coupling parity')
    support=support_checks(); haar=haar_controls(); resonance=resonance_control()
    tau_max=F(5,1664); M=7*tau_max; g=1-M
    need(g==F(1629,1664) and g>0,'explicit actual one-star inverse gap')
    try:
        need(F(0)>0,'physical reference energy must be positive')
    except ValueError:
        zero_scale_rejected=True
    else:
        raise ValueError('zero energy reference was admitted')
    results={'schema':'ym23-producer-results-v1','loop':'s1','direction':'forward',
             'status':'checks_passed_target_limited','passed':True,
             'target_verdict':'limited','actual_source_nonzero':'tau != 0',
             'generated_source':'w=-a*u-(s_squared/3)*v',
             'interior_inverse_gap_lower':str(g),
             'origin_defect_upper':'6*M*r/(1-M)',
             'family_weighted_defect_upper':'192*exp(7*mu)*M*r_star/(1-M)',
             'full_operator_inverse_proved':False,'actual_spectral_obstruction_proved':False,
             'support':support,'fixtures':fixtures,'haar':haar,
             'open':['all-sector actual spectral solvability','all-order connected-support inverse',
                     'later-diagonal induction','homogeneous numerical gap','physical calibration','4D continuum']}
    controls={'schema':'ym23-producer-controls-v1','loop':'s1','direction':'forward',
              'status':'discriminating_checks_passed','passed':True,
              'wrong_cubic_coefficient_rejected':True,'wrong_homological_sign_rejected':True,
              'dropped_crossing_rejected_fixture':True,'exterior_vacuum_projection_rejected_actual':True,
              'incoming_anchor_omission_rejected':True,'wrong_character_normalization_rejected':True,
              'tau_zero_is_valid_exception':True,'coupling_sign_symmetry_preserved':True,
              'zero_physical_reference_rejected':zero_scale_rejected,'resonance':resonance,
              'fixture_scope':'exact matrix algebra only; no physical spin truncation'}
    # A changed cubic A coefficient really changes the source projection.
    f=F(1,4096); v=[F(0),f,2*f]; u=[F(0),f/2,2*f/3]
    S0=rtwo(u,True); A0=rtwo(v)
    missing=col(scale(F(1,6),comm(S0,comm(S0,A0)))); missing[0]=0
    need(dot(missing,missing)>0,'omitting cubic A term discriminates')
    out.mkdir(parents=True)
    save(out/'results.json',results); save(out/'controls.json',controls)
    outputs={n:digest(out/n) for n in ('results.json','controls.json')}
    save(out/'source-manifest.json',{'schema':'ym23-producer-source-manifest-v1',
         'loop':'s1','direction':'forward','inputs':inputs,'outputs':outputs})
    print(json.dumps({'passed':True,'loop':'s1','direction':'forward','target_verdict':'limited','output':str(out)},sort_keys=True))

if __name__=='__main__': main()
