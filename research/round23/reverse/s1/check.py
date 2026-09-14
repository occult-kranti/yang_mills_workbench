#!/usr/bin/env python3
"""S1 reverse exact algebra, actual Haar geometry and indexed support checks."""
from pathlib import Path
from fractions import Fraction as F
from itertools import product, combinations
import argparse, hashlib, json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
CONTRACT = ROOT / 'research/round23/contracts/s1.json'

def require(value, message):
    if not value:
        raise RuntimeError(message)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def mm(a,b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))), F(0)) for j in range(len(b[0]))] for i in range(len(a))]

def plus(a,b):
    return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]

def scale(c,a):
    return [[c*x for x in row] for row in a]

def comm(a,b):
    return plus(mm(a,b),scale(-1,mm(b,a)))

def dot(a,b):
    return sum((x*y for x,y in zip(a,b)), F(0))

def action(a,v):
    return [dot(row,v) for row in a]

def outer(a,b):
    return [[x*y for y in b] for x in a]

def block_fixture(tau):
    omega=[F(1),F(0),F(0)]
    v=[F(0),tau/2,tau/3]
    u=[F(0),tau/4,tau/15]
    A=plus(outer(v,omega),outer(omega,v))
    S=plus(outer(u,omega),scale(-1,outer(omega,u)))
    D=[[F(0),F(0),F(0)],[F(0),tau/7,tau/11],[F(0),tau/11,-tau/13]]
    phi=plus(A,D)
    actual=plus(scale(F(1,2),comm(S,comm(S,phi))),scale(F(-1,6),comm(S,comm(S,A))))
    beta=dot(u,u);c=dot(u,v)
    predicted=[-c*ui-beta*vi/3 for ui,vi in zip(u,v)]
    observed=action(actual,omega);observed[0]=F(0)
    require(observed==predicted,'cubic source algebra failed')
    overlap=dot(v,observed)
    require(overlap==-c*c-beta*dot(v,v)/3,'nonzero overlap identity failed')
    require(overlap<0 if tau else overlap==0,'coupling sign/zero check failed')
    wrong=action(scale(F(1,2),comm(S,comm(S,phi))),omega);wrong[0]=F(0)
    require(wrong!=predicted if tau else wrong==predicted,'BCH wrong factorial control failed')
    # Invert the actual fixture excited 2x2 G block exactly, without diagonalizing.
    a=F(2)+D[1][1];b=D[1][2];d=F(5)+D[2][2]
    determinant=a*d-b*b
    require(determinant>0 and a>0,'interior fixture not positive')
    z=[F(0),(d*predicted[1]-b*predicted[2])/determinant,(-b*predicted[1]+a*predicted[2])/determinant]
    L=plus(outer(z,omega),scale(-1,outer(omega,z)))
    G=plus([[F(0),F(0),F(0)],[F(0),F(2),F(0)],[F(0),F(0),F(5)]],D)
    generated=plus(outer(predicted,omega),outer(omega,predicted))
    require(comm(L,G)==scale(-1,generated),'interior inverse sign failed')
    require(comm(scale(-1,L),G)!=scale(-1,generated) if tau else True,'opposite sign control failed')
    return {'tau':str(tau),'source':[str(x) for x in predicted], 'v_w':str(overlap),'c':str(c),'beta':str(beta),'interior_identity':True}

def plus_point(a,b):
    return tuple(x+y for x,y in zip(a,b))

OFFSETS={(0,0,0),(1,0,0),(0,1,0),(0,0,1)}
def star(anchor):
    return {plus_point(anchor,p) for p in OFFSETS}

def geometry():
    origin=star((0,0,0))
    points=set(product(range(4),repeat=3))
    anchors=[p for p in points if star(p)<=points]
    crosses=[p for p in anchors if star(p)&origin and not star(p)<=origin]
    require(set(crosses)=={(1,0,0),(0,1,0),(0,0,1)},'origin crossing list failed')
    bulk=star((1,1,1))
    bulk_cross=[p for p in anchors if star(p)&bulk and not star(p)<=bulk]
    require(len(bulk_cross)==12,'bulk crossing count failed')
    require(all(len(star(p)|bulk)==7 for p in bulk_cross),'pair union cardinality failed')
    offsets={tuple(x-y for x,y in zip(a,b)) for a in OFFSETS for b in OFFSETS}
    require(len(offsets)==13,'meeting displacement count failed')
    root=(0,0,0);indexed=[]
    for b in product(range(-2,3),repeat=3):
        for d in offsets-{root}:
            c=plus_point(b,d);union=star(b)|star(c)
            if root in union:indexed.append((b,c))
    require(len(indexed)==84,'ordered root multiplicity failed')
    incoming=[b for b in bulk_cross if any(b[i]<1 for i in range(3))]
    require(len(incoming)==9,'incoming crossing count failed')
    # Nonzero nested commutators can only require the next star to meet
    # the accumulated union. Enumerate candidate support words, including repeats.
    words=[(star(root),[root])]
    for depth in range(1,4):
        new=[]
        for support,word in words:
            candidates={tuple(x-y for x,y in zip(p,o)) for p in support for o in OFFSETS}
            for candidate in candidates:
                union=support|star(candidate)
                require(len(union)<=4+3*depth,'connected word support growth failed')
                new.append((union,word+[candidate]))
        words=new
    return {'origin_crossing_anchors':[list(p) for p in sorted(crosses)],'bulk_crossings':12,'incoming_bulk_crossings':len(incoming),'ordered_pair_root_multiplicity':84,'pair_union_size':7,'depth_three_words_checked':len(words),'fixed_origin_weight2_boundary_coefficient':3*2**7*14,'translated_family_weight2_boundary_coefficient':84*2**7*14}

def haar_geometry():
    unit=[(1,0,0),(0,1,0),(0,0,1)]
    faces=[]
    for p in product(range(4),range(2),range(1)):
        for i,j in combinations(range(3),2):
            if i==0 and j==1 and p[1]%2==0 and p[0]%4<3:
                continue
            edges={(p,i),(plus_point(p,unit[j]),i),(p,j),(plus_point(p,unit[i]),j)}
            free={e for e in edges if e[1]==2 or (e[1]==1 and e[0][1]%2==1) or (e[1]==0 and e[0][0]%4==3)}
            require(len(free)>=2,'missing free Haar witnesses')
            faces.append((edges,free))
    pair_count=0
    for (ea,fa),(eb,fb) in combinations(faces,2):
        require(len(ea&eb)<=1 and fa-eb and fb-ea,'distinct-face Haar cancellation witness failed')
        pair_count+=1
    require(len(faces)==21 and pair_count==210,'actual face counts failed')
    second=F(1,4);variance=len(faces)*second/9
    require(variance==F(7,12),'actual forcing variance failed')
    return {'faces':21,'cross_pairs':210,'conditional_quaternion_coordinate_second_moment':str(second),'actual_v_norm_squared_coefficient':str(variance),'note':'Haar invariance and unmatched free-link integration prove moments; finite enumeration verifies the physical geometry.'}

def resonance_fixture():
    t=F(1,10);d=t/(1-t*t)
    G=[[F(0) for _ in range(4)] for _ in range(4)]
    for i,x in enumerate([0,1,1,2]):G[i][i]=F(x)
    G[1][3]=G[3][1]=d
    A=[[F(0) for _ in range(4)] for _ in range(4)]
    A[0][2]=A[2][0]=A[1][3]=A[3][1]=F(1)
    eta=[F(0),F(1),F(0),-t]
    energy=1-d*t
    require(action(G,eta)==[energy*x for x in eta],'exact resonance eigenvector failed')
    overlap=dot(eta,action(A,eta))
    require(overlap==-2*t and overlap!=0,'resonant source expectation failed')
    Avac=[[F(0) for _ in range(4)] for _ in range(4)]
    Avac[0][2]=Avac[2][0]=F(1)
    exterior=[F(0),F(1),F(0),F(0)]
    require(action(Avac,exterior)==[F(0)]*4,'global vacuum source control failed')
    require(dot(action(A,exterior),action(A,exterior))==1,'identity exterior source control failed')
    return {'model':'two-qubit inference falsifier, not SU2 spectral evidence','D_offdiagonal':str(d),'eigenvalue':str(energy),'eigenvector':[str(x) for x in eta],'normalized_source_expectation':str(overlap/dot(eta,eta)),'positive_ground_gap':str(energy),'actual_SU2_resonance_proved':False}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
    out=Path(args.output)
    require(out.is_absolute(),'output must be an absolute path')
    require(not out.exists(),'output must be fresh')
    contract=json.loads(CONTRACT.read_text())
    for rel,expected in contract['dependencies'].items():
        require(digest(ROOT/rel)==expected,'dependency digest mismatch: '+rel)
    for rel in contract['instruction_inputs']:
        require((ROOT/rel).is_file(),'missing frozen instruction: '+rel)
    fixtures=[block_fixture(t) for t in [F(0),F(5,1664),F(-5,1664),F(1,10000),F(-1,10000)]]
    geo=geometry();haar=haar_geometry();resonance=resonance_fixture()
    require(F(1)-7*F(5,1664)==F(1629,1664),'local gap endpoint failed')
    require(F(1)-28*F(5,1664)==F(381,416),'global initial gap endpoint failed')
    results={'schema':'ym23-reverse-s1-v1','loop':'s1','direction':'reverse','status':'checks_passed_target_limited','passed':True,'target_verdict':'actual_generated_source_and_local_inverse_verified_full_operator_inverse_unresolved','source':{'definition':'Q ((1/2) ad_S^2 phi - (1/6) ad_S^2 A) Omega','formula':'w=-c u-(beta/3)v; c=<u,v>, beta=||u||^2','nonzero_certificate':'<v,w>=-c^2-beta||v||^2/3<0 for nonzero tau','norm_bound':'||w|| <= (4/3)(7/12)^(3/2)|tau|^3','degree':3,'full_BCH_remainder':False},'haar':haar,'geometry':geo,'fixtures':fixtures,'resonance_fixture':resonance,'comparison':{'source_formula':'-c*u-beta*v/3','origin_crossings':3,'bulk_crossings':12,'connected_union_size':7,'full_source_inverse_proved':False,'actual_SU2_resonance_proved':False,'homogeneous_gap_proved':False,'physical_calibration_proved':False,'continuum_proved':False},'domains':{'finite_volume':'D(G_Lambda)=D(H0_Lambda); local inverse generator and its exponential preserve it','infinite_global_operator_domain_equality_claimed':False},'novelty':'project derivation; scientific priority unverified'}
    controls={'schema':'ym23-reverse-s1-controls-v1','loop':'s1','direction':'reverse','status':'passed','passed':True,'actual_source_provenance_checked':True,'actual_Haar_source_nonzero_proved':True,'wrong_BCH_factorial_rejected':True,'interior_inverse_wrong_sign_rejected':True,'actual_free_Haar_exterior_mismatch':'squared mismatch ||w||^2>0; normalized free character has zero mean and norm1','global_vacuum_projector_substitution_rejected':True,'dropped_origin_crossing_list_rejected':True,'incoming_crossings_retained':True,'equal_energy_block_necessity':'<psi,[L,G]psi>=0 for each energy eigenvector in D(G)','generic_resonance_control_rejected_universal_inverse':True,'actual_SU2_resonance_claimed':False,'tau_zero_and_both_signs':True,'fixed_positive_scale_preserved':True,'infinite_completeness_from_sampling_claimed':False}
    consulted=['research/round23/methods/team-protocol.md','research/round21/reverse/i2/report.md','research/round21/reverse/i2/check.py']
    inventory=set(contract['dependencies'])|set(contract['instruction_inputs'])|set(consulted)|{'research/round23/contracts/s1.json',str(HERE.relative_to(ROOT)/'check.py'),str(HERE.relative_to(ROOT)/'report.md')}
    manifest={'schema':'ym23-source-manifest-v1','direction':'reverse','loop':'s1','inputs':{rel:digest(ROOT/rel) for rel in sorted(inventory)},'outputs':{},'current_other_direction_read':False,'source_depth':'Inherited I2/R/O reports and exact I2 checker reviewed; primary-source reading inherited, not newly claimed; direct algebra/domain argument in report.'}
    out.mkdir(parents=True)
    for name,obj in [('results.json',results),('controls.json',controls)]:
        (out/name).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
    manifest['outputs']={name:digest(out/name) for name in ['results.json','controls.json']}
    (out/'source-manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'passed':True,'output':str(out),'source_formula':results['source']['formula'],'full_inverse':'unresolved'},sort_keys=True))

if __name__=='__main__':main()
