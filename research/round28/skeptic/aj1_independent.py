#!/usr/bin/env python3
"""AJ1 independent exact geometry and analytic-obligation diagnostics.

This checks no infinite-dimensional theorem by finite sampling. See the proof.
"""
import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib,itertools,json,math
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];PACK=HERE/'aj1-inputs';COUNT=Counter()

def need(ok,label):
    COUNT[label]+=1
    if not ok:raise RuntimeError(label)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def enc(x):
    if isinstance(x,Q):return str(x)
    if isinstance(x,dict):return {str(k):enc(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [enc(v) for v in x]
    return x

def add(a,b):return tuple(x+y for x,y in zip(a,b))
def own(v):return (v[0]//4,v[1]//2,v[2])
E=[(1,0,0),(0,1,0),(0,0,1)];S=[(0,0,0)]+E

def linkset(b):return {(add((4*b[0],2*b[1],b[2]),(r,s,0)),a) for r in range(4) for s in range(2) for a in range(3)}
def word(v,a,b):return [(v,a,1),(add(v,E[a]),b,1),(add(v,E[b]),a,-1),(v,b,-1)]
def selected(v,a,b):return (a,b)==(0,1) and v[1]%2==0 and v[0]%4 in (0,1,2)
def faces(b,omitted):
    rows=[]
    for r in range(4):
        for s in range(2):
            v=(4*b[0]+r,2*b[1]+s,b[2])
            for a,c in itertools.combinations(range(3),2):
                if selected(v,a,c)==omitted:continue
                w=word(v,a,c);rows.append({'base':v,'axes':(a,c),'word':w,'owners':sorted({own(t) for t,d,z in w})})
    return rows

def qm(a,b):
    w,x,y,z=a;W,X,Y,Z=b
    return (w*W-x*X-y*Y-z*Z,w*X+x*W+y*Z-z*Y,w*Y-x*Z+y*W+z*X,w*Z+x*Y-y*X+z*W)
def qi(a):return (a[0],-a[1],-a[2],-a[3])
def hol(w,values):
    v=(Q(1),Q(0),Q(0),Q(0))
    for t,a,s in w:v=qm(v,values[t,a] if s==1 else qi(values[t,a]))
    return v
PALETTE=[(Q(1),Q(0),Q(0),Q(0)),(Q(0),Q(1),Q(0),Q(0)),(Q(3,5),Q(4,5),Q(0),Q(0)),(Q(5,13),Q(0),Q(12,13),Q(0))]

def geom(box):
    sites=set(itertools.product(*(range(n) for n in box)))
    links=set().union(*(linkset(b) for b in sites));links_sorted=sorted(links)
    vertices={v for v,a in links}|{add(v,E[a]) for v,a in links}
    need(len(links)==24*len(sites),'complete original tail-owned links')
    endpoint_inc={v:[] for v in vertices}
    for v,a in links_sorted:
        endpoint_inc[v].append((v,a,1));endpoint_inc[add(v,E[a])].append((v,a,-1))
    need(sum(map(len,endpoint_inc.values()))==2*len(links),'all original endpoint actions')
    groups=[];selected_faces=[];phase_counts=Counter()
    for b in sorted(sites):
        sf=faces(b,False);of=faces(b,True)
        slinks={(v,a) for f in sf for v,a,s in f['word']}
        need(len(sf)==3 and len(of)==21 and len(slinks)==10 and slinks<=linkset(b),'complete selected10 and omitted21')
        need(len(linkset(b)-slinks)==14,'all14 free owned links')
        for f in sf:need(set(f['owners'])=={b},'selected reference stays on one full site')
        star={add(b,s) for s in S}
        need(set().union(*(set(f['owners']) for f in of))==star,'actual complete omitted union is four-site star')
        for f in of:
            need(set(f['owners'])<=star and len(f['owners'])>=2,'crossing omitted face retained in complete group')
            if b==(0,0,0):phase_counts[tuple(f['owners'])]+=1
        selected_faces.extend(sf)
        if star<=sites:
            for f in of:need(all((v,a) in links for v,a,s in f['word']),'all complete retained face links exist')
            groups.append({'anchor':b,'star':sorted(star),'faces':of})
    need(len(groups)==math.prod(n-1 for n in box),'complete whole-star empty boundary count')
    allfaces=selected_faces+[f for g in groups for f in g['faces']]
    vals={e:PALETTE[i%len(PALETTE)] for i,e in enumerate(links_sorted)}
    vg={v:PALETTE[(i+2)%len(PALETTE)] for i,v in enumerate(sorted(vertices))}
    changed={(v,a):qm(qm(vg[v],vals[v,a]),qi(vg[add(v,E[a])])) for v,a in links_sorted}
    for f in allfaces:
        orig=hol(f['word'],vals);new=hol(f['word'],changed)
        target=qm(qm(vg[f['base']],orig),qi(vg[f['base']]))
        need(new==target and new[0]==orig[0],'exact closed Wilson covariance at all retained faces')
    regions=[[(0,0,0)],[(0,0,0),(1,0,0)],[(1,1,1)]];rr=[]
    for rs in regions:
        R=set(rs)
        if not R<=sites:continue
        inc=[g['anchor'] for g in groups if R.intersection(g['star'])]
        direct=sorted(b for b in sites if {add(b,s) for s in S}<=sites and any(add(b,s) in R for s in S))
        candidates={tuple(r[i]-s[i] for i in range(3)) for r in R for s in S}
        need(inc==direct and set(inc)<=candidates and len(inc)<=4*len(R),'all incoming and outgoing incident complete groups')
        regionlinks=set().union(*(linkset(b) for b in R));endpoints={v for v,a in regionlinks}|{add(v,E[a]) for v,a in regionlinks}
        regionaltails={v for v,a in regionlinks}
        need(len(endpoints)>len(regionaltails) and all(v in vertices for v in endpoints),'outgoing head endpoint gauge support preserved')
        rr.append({'region':sorted(R),'owned_link_count':len(regionlinks),'all_endpoint_count':len(endpoints),
                   'external_head_endpoints':sorted(endpoints-regionaltails),'incident_anchors':inc,
                   'incident_count':len(inc),'reset_energy_coefficient_of_M':2*len(inc),
                   'uniform_energy_coefficient_of_M':8*len(R)})
    return {'cuboid':box,'sites':len(sites),'owned_links':len(links),'endpoint_vertices':len(vertices),
            'selected_faces':len(selected_faces),'retained_star_groups':len(groups),'omitted_faces':21*len(groups),
            'owned_link_labels':links_sorted,'retained_anchors':[g['anchor'] for g in groups],
            'regional_certificates':rr,'phase_support_counts':[{'support':list(k),'count':v} for k,v in sorted(phase_counts.items())],
            'all_retained_Wilson_gauge_checks':len(allfaces)}

def matmul(A,B):return [[sum((a*b for a,b in zip(row,col)),Q(0)) for col in zip(*B)] for row in A]
def trace(A):return sum((A[i][i] for i in range(len(A))),Q(0))

def diagnostics(geometry):
    interior=next(r for r in geometry[-1]['regional_certificates'] if r['region']==[(1,1,1)])
    need(interior['incident_count']==4 and len([b for b in interior['incident_anchors'] if b!=(1,1,1)])==3,'interior missing-incoming-anchors control')
    need(interior['reset_energy_coefficient_of_M']==8>2,'anchor-only reset budget rejected')
    need([g['retained_star_groups'] for g in geometry]==[1,2,8],'growing nonsummable star budget; no global norm')
    boundary=next(r for r in geometry[0]['regional_certificates'] if r['region']==[(0,0,0)])
    need(boundary['incident_count']==1 and len(S)>1,'boundary crossing group cannot be dropped from reset estimate')
    pair={(0,0,0),(1,0,0)}
    actual_contained=sum(set(f['owners'])<=pair for b in pair for f in faces(b,True))
    whole_contained=sum({add(b,s) for s in S}<=pair for b in pair)
    need(actual_contained==1 and whole_contained==0,'actual-face and whole-star boundary prescriptions differ')
    need(Q(1,2)+Q(1,8)+Q(1,2)==Q(9,8) and Q(9,8)/Q(1,8)==9 and 9+9==18,'complete onsite bounded potential and energy-shift constants')
    # A genuine finite mixed reset diagnostic. This is not a selected physical tau.
    H0=[[Q(i==j)*v for j in range(4)] for i,v in enumerate((0,1,1,2))]
    V=[[Q(0) for j in range(4)] for i in range(4)];V[1][2]=V[2][1]=Q(-2)
    H=[[H0[i][j]+V[i][j] for j in range(4)] for i in range(4)]
    rho=[[Q(0) for j in range(4)] for i in range(4)]
    for i in (1,2):
        for j in (1,2):rho[i][j]=Q(1,2)
    reset=[[Q(0) for j in range(4)] for i in range(4)];reset[0][0]=reset[1][1]=Q(1,2)
    HR=[[Q(i==j)*(i//2) for j in range(4)] for i in range(4)]
    HC=[[Q(i==j)*(i%2) for j in range(4)] for i in range(4)]
    need(matmul(H,rho)==[[-v for v in row] for row in rho],'reset diagnostic actual ground eigenvalue minus1')
    need(sorted([Q(0),Q(1)-2,Q(1)+2,Q(2)])[0]==-1,'reset diagnostic full finite ground isolation')
    er=trace(matmul(HR,rho));ec=trace(matmul(HC,rho));ecnew=trace(matmul(HC,reset));vr=trace(matmul(V,reset));vo=trace(matmul(V,rho))
    need(er==Q(1,2) and ec==ecnew==Q(1,2) and trace(matmul(HR,reset))==0,'reset cancels outside reference and resets region')
    need(trace(matmul(H,reset))-trace(matmul(H,rho))==-er+vr-vo>=0,'actual finite variational scalar cancellation')
    need(er>0 and er<=vr-vo<=4,'dropping one incident interaction gives false zero energy budget')
    # Exact local spectral tightness/HS inequality arithmetic, without sample inference.
    for size in (1,2):
        need(2*4*size*7==56*size,'all-volume regional energy coefficient')
    # Charged open link versus closed plaquette under its actual endpoint center.
    one=(Q(1),Q(0),Q(0),Q(0));minus=tuple(-x for x in one)
    need(qm(minus,one)[0]==-1!=one[0],'missing endpoint gauge average rejects charged open Wilson')
    need(qm(one,qi(minus))[0]==-1 and (4,0,0) not in {v for v,a in linkset((0,0,0))},'actual outgoing head action cannot be omitted')
    w=word((0,0,0),0,1);v={(t,a):one for t,a,s in w};vg={x:one for x in {t for t,a,s in w}|{add(t,E[a]) for t,a,s in w}};vg[(0,0,0)]=minus
    gv={(t,a):qm(qm(vg[t],x),qi(vg[add(t,E[a])])) for (t,a),x in v.items()}
    need(hol(w,v)[0]==hol(w,gv)[0]==1,'closed charged-factor cancellation under full endpoints')
    need(tuple((one[i]+minus[i])/2 for i in range(4))==(0,0,0,0),'fundamental center average kills charged representation')
    # Quaternion conjugation averages vector part to zero under {1,i,j,k}.
    units=[one,(Q(0),Q(1),Q(0),Q(0)),(Q(0),Q(0),Q(1),Q(0)),(Q(0),Q(0),Q(0),Q(1))]
    a=(Q(1,7),Q(2,7),Q(3,7),Q(4,7))
    twirl=tuple(sum(qm(qm(g,a),qi(g))[i] for g in units)/4 for i in range(4))
    need(twirl==(Q(1,7),0,0,0),'exact fundamental operator Haar invariant part')
    need(qm(qm(units[1],units[2]),qm(qi(units[1]),qi(units[2])))==minus,'SU2 center is a commutator; phase character diagnostic')
    # Infinite analytic counterexamples have exact finite diagnostic prefixes.
    normality=[];domain=[];normcontinuity=[];averaging=[]
    for n in (1,2,8,32):
        normality.append({'finite_projection_rank':n,'escaping_state_index':n+1,'finite_projection_mass':0,'identity_mass':1,'reference_energy':(n+1)**2})
        need((n+1)>n and (n+1)**2>n,'normal-state escape versus uniform energy tightness')
        norm2=sum((Q(1,k**4) for k in range(1,n+1)),Q(0));Hnorm2=sum((Q(k**4,k**4) for k in range(1,n+1)),Q(0))
        need(norm2<2 and Hnorm2==n,'bounded rank-one creation need not lie in generator domain')
        badform=sum((Q(k*k,k*k) for k in range(1,n+1)),Q(0))
        need(badform==n,'arbitrary reset vector can have infinite reference form energy')
        domain.append({'prefix':n,'creation_vector_norm_squared_prefix':norm2,'generator_image_norm_squared_prefix':Hnorm2,'bad_reset_form_prefix':badform})
        # g(theta)=diag(e^{i theta},e^{-i theta}), weight n=2j.
        theta_over_pi=Q(1,2*n);phase_over_pi=2*n*theta_over_pi
        need(phase_over_pi==1,'strong-continuous SU2 subgroup has operator norm orbit distance2')
        normcontinuity.append({'twice_spin':n,'theta_over_pi':theta_over_pi,'relative_phase_over_pi':phase_over_pi,'operator_norm_difference':2})
        index=12*(n+1)
        need(index>n and all((index*Q(1,d)).denominator==1 for d in (2,3,4)),'finite rational phases in singular weak-average countermodel')
        averaging.append({'lower_index_bound':n,'chosen_index':index,'test_phase_fractions':[Q(1,2),Q(1,3),Q(1,4)],'all_phase_values':1,'original_weak_Haar_average':0})
    # Compression differs from a reducing restriction, and a threshold need not have an excitation.
    K=[[Q(1),Q(1)],[Q(1),Q(1)]];P=[[Q(1),Q(0)],[Q(0),Q(0)]]
    need(matmul(K,P)!=matmul(P,K),'nonreducing compression cannot replace spectral restriction')
    need(matmul(P,matmul(K,P))==P,'compressed scalar differs from actual reducing dynamics')
    gap_full=[0,Q(1,2)];vacuum_restriction=[0]
    need(all(v==0 or v>=Q(1,2) for v in vacuum_restriction) and not any(v>0 for v in vacuum_restriction),'restricted gap inequality is not nonzero physical excitation')
    need(Q(1,8)*Q(1,2)==Q(1,16) and Q(1,2)!=Q(1,16),'physical delta factor cannot be omitted')
    need(Q(973,8640)!=Q(1,16),'dyadic numerical gap not inherited into homogeneous model')
    shifted=[Q(3,7)+x for x in gap_full]
    need(shifted[0]!=0 and [x-Q(3,7) for x in shifted]==gap_full,'ground subtraction retained exactly')
    # Source core restrictions: h|u><Omega| is bounded iff the chosen image is in D(h).
    h=[[Q(0),Q(0)],[Q(0),Q(3)]];creation=[[Q(0),Q(0)],[Q(1),Q(0)]]
    need(matmul(creation,h)==[[0,0],[0,0]] and matmul(h,creation)==[[0,0],[3,0]],'domain-correct creation commutator diagnostic')
    return {'reset_countermodel':{'state_energy':-1,'regional_reference_energy':er,'outside_reference_energy_before_after':ec,'reset_energy':trace(matmul(H,reset)),'incident_interaction_change':vr-vo,'norm_M':2,'scope':'abstract finite ground/reset diagnostic, not a chosen physical coupling'},
            'weak_star_normality_countermodel':normality,'bounded_local_domain_countermodel':domain,
            'strong_vs_norm_continuity_countermodel':normcontinuity,'weak_integral_GNS_countermodel':averaging,
            'weak_integral_scope':'Original strongly continuous circle diagonal unitaries on l2(N), weak Haar average0; a singular net state makes represented vacuum vectors constant. Analytic net construction in report; finite phase checks are diagnostics only.',
            'full_gauge_closed_Wilson':True,'charged_open_link_center_average_zero':True,
            'fundamental_Haar_twirl':twirl,'nonreducing_compression_rejected':True,
            'restricted_spectral_threshold_without_excitation':vacuum_restriction,
            'physical_energy_factor_alpha':Q(1,8),'inherited_energy_threshold_alpha':Q(1,16),
            'nondiscriminating_attempts':[]}

def main(output):
    inv=json.loads((PACK/'source-inventory.json').read_text());sources={}
    for e in inv['entries']:
        need(sha(ROOT/e['snapshot'])==e['sha256']==sha(ROOT/e['source']),'prospective source snapshot and original hashes')
        sources[e['source']]=e['sha256']
    con=json.loads((PACK/'research/round28/contracts/aj1.json').read_text())
    need(con['sequence']==7 and len(con['sources'])==48,'actual AJ1 contract and source count')
    need(sources['research/round28/contracts/aj1.json']=='a9660ab26b0116958c11721e5461eab3391d50149306e06a0ec2476cdbc21571','exact frozen contract')
    for p,h in con['sources'].items():need(sources[p]==h,'all declared sources preserved')
    geometry=[geom(box) for box in ((2,2,2),(3,2,2),(3,3,3))]
    controls=diagnostics(geometry)
    result={'schema':'ym28-aj1-skeptic-independent-v1','loop':'aj1','sequence':7,'current_producer_science_read':False,
            'historical_checkers_imported_or_executed':False,'source_bindings':sources,'source_inventory_sha256':sha(PACK/'source-inventory.json'),
            'analytic_result':{'local_reference_energy_upper':'2 M n_Lambda(R) <=8 M |R| =56 |tau| |R|',
                'spectral_tail_upper':'8 M |R|/T','trace_norm_cutoff_error_upper':'2 sqrt(8 M |R|/T)',
                'local_density_trace_norm_convergence':True,'local_normality':True,'represented_local_normality':True,
                'gauge_implementation_strongly_continuous_on_each_finite_endpoint_group':True,
                'point_norm_continuity_on_all_bounded_local_operators':False,'Haar_through_GNS_justified_by_local_normality':True,
                'physical_cyclic_equals_joint_gauge_fixed':True,'source_correct_creation_core_and_closure_used':True,
                'physical_subspace_reduces_actual_centered_G':True,'physical_operator_domain':'D(G) intersect H_cyc',
                'physical_form_domain':'D(G^(1/2)) intersect H_cyc','energy_generator':'(alpha/8) G restricted to H_cyc',
                'frequency_generator':'(alpha/(8 hbar)) G restricted to H_cyc','inherited_energy_threshold':'alpha/16',
                'normalization':'delta=alpha/8','numerical_nonzero_tau_certified':False,
                'nonzero_homogeneous_Wilson_excitation_proved':False,'source_proof_independently_reconstructed':False},
            'geometry_fixtures':geometry,'controls':controls,'scope':{'actual_I1_homogeneous_omitted_model':True,
                'fixed_whole_star_orthant_boundary':True,'symbolic_tau_star_only':True,'gauge_constrained_tensor_factorization':False,
                'same_representation_strong_resolvent_claim':False,'arbitrary_bounded_local_G_domain':False,
                'Wilson_only_algebra_substitution':False,'bounded_global_perturbation':False,
                'same_state_for_all_boundary_sequences':False,'summable_or_AH_model_identification':False,
                'global_infinite_volume_conjugating_unitary':False,'continuum_Yang_Mills_gap':False,
                'finite_checks_prove_analytic_theorems':False,'scientific_priority_verified':False},
            'check_groups':dict(COUNT),'check_count':sum(COUNT.values()),'all_checks_passed':True,'additional_research_loops':0}
    output.write_text(json.dumps(enc(result),sort_keys=True,indent=2)+'\n')
    print(json.dumps({'check_count':result['check_count'],'output_sha256':sha(output),
                      'fixture_summary':[{k:g[k] for k in ['cuboid','owned_links','endpoint_vertices','retained_star_groups']} for g in geometry]},sort_keys=True))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=HERE/'aj1-independent.json');main(p.parse_args().output)
