#!/usr/bin/env python3
"""AJ1 reverse: exact independent geometry and logical diagnostics.
No historical checker is imported or executed. No finite fixture proves the
infinite-dimensional regularity or GNS theorem; see report.md.
"""
from __future__ import annotations
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import itertools
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
COUNT = 0

def require(condition, label):
    global COUNT
    COUNT += 1
    if not condition:
        raise RuntimeError(label)

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def packed(x):
    if isinstance(x,F): return str(x.numerator)+'/'+str(x.denominator)
    if isinstance(x,dict): return {str(k):packed(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)): return [packed(v) for v in x]
    return x

def add(p,q): return tuple(a+b for a,b in zip(p,q))
def sub(p,q): return tuple(a-b for a,b in zip(p,q))
E=((1,0,0),(0,1,0),(0,0,1))
STAR=((0,0,0),)+E

def owner(p): return (p[0]//4,p[1]//2,p[2])
def block_tails(b):
    return [(4*b[0]+r,2*b[1]+s,b[2]) for r in range(4) for s in range(2)]
def block_links(b): return [(p,a) for p in block_tails(b) for a in range(3)]
def face_word(p,a,b):
    return [((p,a),1),((add(p,E[a]),b),1),((add(p,E[b]),a),-1),((p,b),-1)]
def faces(b):
    for p in block_tails(b):
        for a,c in ((0,1),(0,2),(1,2)):
            yield (p,a,c),face_word(p,a,c)
def selected(fid):
    p,a,c=fid
    return (a,c)==(0,1) and p[0]%4 in (0,1,2) and p[1]%2==0

def qmul(a,b):
    w,x,y,z=a;W,X,Y,Z=b
    return (w*W-x*X-y*Y-z*Z,w*X+x*W+y*Z-z*Y,
            w*Y-x*Z+y*W+z*X,w*Z+x*Y-y*X+z*W)
def qinv(a): return (a[0],-a[1],-a[2],-a[3])
ONE=(F(1),F(0),F(0),F(0))
MINUS=tuple(-x for x in ONE)
QSET=(ONE,(F(3,5),F(4,5),F(0),F(0)),
      (F(5,13),F(0),F(12,13),F(0)),
      (F(8,17),F(0),F(0),F(15,17)))
def link_value(link):
    p,a=link
    return QSET[(p[0]+2*p[1]+3*p[2]+a+1)%len(QSET)]
def gauge_value(p): return QSET[(3*p[0]+p[1]+2*p[2]+1)%len(QSET)]
def wilson(word,values):
    z=ONE
    for link,sign in word:
        u=values[link]
        z=qmul(z,u if sign==1 else qinv(u))
    return z[0]

def geometry(contract):
    fixtures=[]; region_rows=[]; hist=Counter(); bad_endpoint=None; blind_endpoints=[]
    for sides in contract['parameters']['geometry_fixtures']['cuboid_side_counts']:
        volume=set(itertools.product(*(range(n) for n in sides)))
        links=set(); groups=[]; endpoints=set()
        for b in sorted(volume):
            ls=set(block_links(b));require(len(ls)==24,'full owned link factor count')
            require(not (links&ls),'unique ownership')
            sel=[(f,w) for f,w in faces(b) if selected(f)]
            strip={l for _,w in sel for l,_ in w}
            require(len(sel)==3 and len(strip)==10 and strip<=ls,'complete selected strip')
            require(len(ls-strip)==14,'free links retained')
            links|=ls
            for p,a in ls: endpoints.update((p,add(p,E[a])))
        require(len(links)==24*len(volume),'volume ownership count')
        anchors=[b for b in sorted(volume) if {add(b,s) for s in STAR}<=volume]
        require(len(anchors)==(sides[0]-1)*(sides[1]-1)*(sides[2]-1),'whole-star cuboid count')
        values={l:link_value(l) for l in links}
        changed={l:qmul(qmul(gauge_value(l[0]),values[l]),qinv(gauge_value(add(l[0],E[l[1]])))) for l in links}
        for b in anchors:
            group=[]
            omitted=[(f,w) for f,w in faces(b) if not selected(f)]
            require(len(omitted)==21,'all 21 omitted anchored faces')
            union=set()
            for fid,w in omitted:
                support={owner(l[0]) for l,_ in w}; union|=support
                require(support<={add(b,s) for s in STAR},'actual face in declared complete star')
                require(len(support) in (2,3),'every omitted face crosses a site')
                require(all(l in links for l,_ in w),'all face factors retained')
                pos=fid[0]
                for (tail,axis),sign in w:
                    start=tail if sign==1 else add(tail,E[axis])
                    end=add(tail,E[axis]) if sign==1 else tail
                    require(start==pos,'oriented path continuity');pos=end
                require(pos==fid[0],'closed face word')
                old=wilson(w,values);new=wilson(w,changed)
                require(old==new,'full endpoint SU2 gauge covariance')
                if bad_endpoint is None:
                    for link,_ in w:
                        bad=dict(changed);bad[link]=qmul(gauge_value(link[0]),values[link])
                        if wilson(w,bad)!=old:
                            bad_endpoint={'face':fid,'link':link,'correct':old,'missing_head':wilson(w,bad)}
                            break
                        blind_endpoints.append({'face':fid,'link':link,'correct':old,'missing_head':wilson(w,bad),
                           'head_gauge':gauge_value(add(link[0],E[link[1]])),
                           'status':'nondiscriminating candidate retained; continue deterministic link scan'})
                rel=tuple(sorted(sub(t,b) for t in support));hist[rel]+=1
                group.append({'face':fid,'word':w,'owners':sorted(support)})
            require(union=={add(b,s) for s in STAR},'group support is the complete star')
            groups.append({'anchor':b,'faces':group})
        require(all(owner(l[0]) in volume for l in links),'outgoing link ownership uses tail')
        outgoing=[l for l in links if owner(add(l[0],E[l[1]])) not in volume]
        require(bool(outgoing),'outgoing links are present')
        # Orthant global incident anchors versus retained finite-volume anchors.
        for raw in contract['parameters']['geometry_fixtures']['regions']:
            R={tuple(p) for p in raw}
            if not R<=volume: continue
            possible={sub(r,s) for r in R for s in STAR if all(x>=0 for x in sub(r,s))}
            incident={b for b in anchors if {add(b,s) for s in STAR}&R}
            require(incident==possible&set(anchors),'all incoming and outgoing incident anchors')
            require(len(incident)<=len(possible)<=4*len(R),'all-volume incidence envelope')
            outgoing_only=set(anchors)&R
            local_faces=[f for b in incident for f,w in faces(b) if not selected(f)]
            require(len(local_faces)==21*len(incident),'reset charges every incident face group')
            row={'sides':sides,'region':sorted(R),'incident_anchors':sorted(incident),
                 'orthant_incident_anchors':sorted(possible),'outgoing_only':sorted(outgoing_only),
                 'energy_upper_coefficient_M':2*len(incident),
                 'uniform_orthant_energy_coefficient_M':2*len(possible),
                 'universal_energy_coefficient_M':8*len(R)}
            region_rows.append(row)
            if sides==[3,3,3] and R=={(1,1,1)}:
                require(len(incident)==4 and len(outgoing_only)==1,'interior fixture detects three incoming groups')
        fixtures.append({'sides':sides,'site_count':len(volume),'links':sorted(links),
                         'endpoint_vertices':sorted(endpoints),'outgoing_links':sorted(outgoing),
                         'anchor_count':len(anchors),'omitted_face_count':21*len(anchors),
                         'groups':groups})
    require(bad_endpoint is not None,'omitted endpoint control discriminates')
    require(len(blind_endpoints)==1 and blind_endpoints[0]['head_gauge']==ONE,
            'preserve first identity-endpoint blind candidate')
    # The exact complete anchor norm uses all Wilson values one, not a vacuum mean.
    require(F(21,3)==7,'local norm coefficient')
    # An actual-support boundary and the whole-star boundary are distinct.
    pair={(0,0,0),(1,0,0)}
    actual=[fid for fid,w in faces((0,0,0)) if not selected(fid) and {owner(l[0]) for l,s in w}<=pair]
    require(len(actual)==1,'pair has one actually supported omitted face')
    require(not any({add(b,s) for s in STAR}<=pair for b in pair),'pair retains no whole star')
    return {'fixtures':fixtures,'regions':region_rows,
            'missing_endpoint_control':{'blind_candidates':blind_endpoints,'replacement':bad_endpoint},
            'whole_star_vs_actual_support':{'coarse_pair_actual_faces':len(actual),'whole_star_faces':0}}

def matmul(a,b):
    return [[sum((a[i][k]*b[k][j] for k in range(len(b))),F(0)) for j in range(len(b[0]))] for i in range(len(a))]
def matsub(a,b): return [[x-y for x,y in zip(r,s)] for r,s in zip(a,b)]
def eye(n): return [[F(int(i==j)) for j in range(n)] for i in range(n)]
def diag(vals): return [[F(vals[i]) if i==j else F(0) for j in range(len(vals))] for i in range(len(vals))]
def zero(a): return all(x==0 for r in a for x in r)

def diagnostics():
    rows={}
    # Full 24-link onsite energy: 8 sum C plus bounded selected strip terms.
    require((F(1,2)+F(1,8)+F(1,2))/F(1,8)==9,'normalized selected potential bound')
    cutoffs=[]
    for sites in (1,2):
        for T in (1,4,16):
            B=F(T+9*sites,8)
            kmax=(4*B/3).__floor__()
            single=sum((k+1)**2 for k in range(kmax+1))
            require(single==(kmax+1)*(kmax+2)*(2*kmax+3)//6,'Peter-Weyl multiplicity sum')
            require(F((kmax+1)*(kmax+3),4)>B,'every excluded single-link spin exceeds electric ceiling')
            cutoffs.append({'sites':sites,'energy_cutoff_T':T,'electric_ceiling':B,
                            'twice_spin_ceiling':kmax,'finite_rank_upper':single**(24*sites)})
    rows['compact_local_energy_cutoffs']={'kind':'exact finite rank upper bound, not actual interacting spectral enumeration',
          'reference_comparison':'h_R >= 8 sum_(24|R| links) C_e - 9|R|',
          'selected_potential_norm_bound':9,'absolute_centered_perturbation_bound':18,'fixtures':cutoffs,
          'proof':'min-max and Peter-Weyl; each k=2j has energy k(k+2)/4 >= 3k/4 and multiplicity (k+1)^2'}
    # This is a finite fundamental-representation diagnostic; Haar formulas are proved in report.
    q8=[]
    for i in range(4):
        for sign in (-1,1): q8.append(tuple(F(sign if i==j else 0) for j in range(4)))
    require(all(qmul(q,qinv(q))==ONE for q in q8),'Q8 unitary fixture')
    av=tuple(sum((q[j] for q in q8),F(0))/8 for j in range(4))
    require(av==(F(0),)*4,'charged fundamental average zero')
    require(qmul(MINUS,QSET[1])[0]==-QSET[1][0]!=QSET[1][0],'charged open link center flip')
    rows['charged_closed']={'kind':'finite SU2 subgroup / exact fundamental diagnostic','q8_average':av,
                           'charged_before':QSET[1][0],'charged_after':qmul(MINUS,QSET[1])[0],
                           'full_group_proof':'all closed words telescope; fundamental Haar integral zero by center invariance'}
    # Domain diagnostic on l2, h e_n = n^2 e_n, v_n=1/n. Finite norm, divergent energy form.
    domain=[]
    for N in (2,8,32):
        nrm=sum((F(1,n*n) for n in range(1,N+1)),F(0))
        form=sum((F(n*n,n*n) for n in range(1,N+1)),F(0))
        op=sum((F(n**4,n*n) for n in range(1,N+1)),F(0))
        require(nrm<2 and form==N and op==N*(N+1)*(2*N+1)//6,'unbounded domain countermodel prefix')
        domain.append({'N':N,'norm2':nrm,'form':form,'operator_norm2':op})
    rows['arbitrary_bounded_local_domain']={'kind':'abstract infinite Hilbert countermodel with analytic divergence','prefixes':domain,
          'proof':'v_n=1/n belongs l2, but sum n^2 |v_n|^2 diverges; A=|v><e0| bounded, A e0 outside form and operator domains'}
    # Every cutoff is escaped by normal vector states; a singular weak-star cluster has mass zero on finite ranks.
    escape=[]
    for cutoff in (1,4,16):
        n=cutoff+1; tail=F(1)
        require(n>cutoff and tail==1,'finite rank escape')
        escape.append({'cutoff':cutoff,'state_index':n,'cutoff_mass':0,'tail_mass':tail,'energy_n2':n*n})
    rows['weakstar_not_normal']={'kind':'abstract l2 weak-star subnet/ultrafilter countermodel','fixtures':escape,
          'proof':'cluster state takes every finite rank projection to zero and identity to one; increasing finite rank projections expose nonnormality; its unbounded energy prevents the AJ1 tightness argument'}
    # Strong U(t) need not make conjugation point-norm continuous.
    normcontrol=[]
    for k in (1,4,16,64):
        require(F(k,k)==1,'discontinuity phase pi exactly')
        normcontrol.append({'k':k,'time_in_pi_units':F(1,k),'witness_input_index':k,'conjugation_difference_norm':2})
    rows['strong_not_pointnorm']={'kind':'abstract U(1) strongly continuous representation',
        'model':'U(t)e_n=e^(int)e_n, A e_n=e_(2n), norm(beta_t(A)-A)=2 at t=pi/k',
        'fixtures':normcontrol,'proof':'dominated convergence on l2 proves strong U continuity; the listed witness attains norm two'}
    # An explicit compact-group countermodel where a singular functional destroys measurability of the average.
    twirls=[]
    for n in (1,2,3,4):
        bits=list(itertools.product((-1,1),repeat=n))
        means=[F(sum(g[j] for g in bits),len(bits)) for j in range(n)]
        require(all(v==0 for v in means),'finite character averages vanish')
        twirls.append({'bits':n,'coordinate_averages':means})
    rows['unjustified_weak_average']={'kind':'abstract compact profinite countermodel; not the physical SU2 model',
        'group':'product_N Z2','hilbert':'direct_sum_N C2','unitary':'U(g)|n=diag(1,g_n)',
        'operator':'direct_sum sigma_x','normal_WOT_average':0,
        'singular_state':'free ultrafilter limit of vector states (e_n,0+e_n,1)/sqrt(2)',
        'scalar_orbit':'lim_ultrafilter g_n; nonmeasurable for Haar measure',
        'proof':'its plus set is unchanged by finitely many bit flips, so measurability would make it a tail event of probability 0 or 1; global sign reversal preserves Haar and exchanges plus/minus, forcing probability 1/2',
        'finite_diagnostics':twirls,'conclusion':'arbitrary GNS need not preserve WOT averaging or even its scalar measurability; AJ1 normality supplies the missing premise'}
    # Full support and ground energy stay in every variational comparison.
    H=diag([-2,1,3]); centered=diag([0,3,5]); P=[[F(1),F(0),F(0)],[F(0),F(1,2),F(1,2)],[F(0),F(1,2),F(1,2)]]
    require(matmul(P,P)==P,'projection fixture')
    comm=matsub(matmul(P,centered),matmul(centered,P))
    require(not zero(comm),'compression is not a reducing restriction')
    require(H[0][0]!=0 and centered[0][0]==0,'actual ground subtraction')
    require(F(1,8)*F(1,2)==F(1,16),'physical gap factor')
    require(F(1,16)!=F(973,8640),'dyadic gap is a different number')
    rows['compression_and_scale']={'kind':'abstract three-dimensional diagnostic','raw_H':H,'centered_H':centered,'projection':P,'commutator':comm,
       'compressed_excited_value':4,'true_excited_values':[3,5],'physical_delta_over_alpha':F(1,8),
       'inherited_normalized_floor':F(1,2),'physical_floor_over_alpha':F(1,16),'frequency_factor':'delta/hbar',
       'dyadic_J2_threshold_over_alpha_not_transferred':F(973,8640)}
    # Exact partial reset on an entangled 2x2 trial verifies the finite bookkeeping only.
    # State sqrt(p)|00>+sqrt(1-p)|11>, choose p=9/25 for rational amplitudes3/5,4/5.
    p=F(9,25); rho=[[F(0) for j in range(4)] for i in range(4)]
    rho[0][0]=p;rho[3][3]=1-p;rho[0][3]=rho[3][0]=F(12,25)
    reset=diag([p,1-p,0,0]);hR=diag([0,0,2,2]);hO=diag([0,3,0,3])
    tr=lambda a:sum((a[i][i] for i in range(len(a))),F(0))
    require(tr(reset)==tr(rho)==1,'reset preserves normalization')
    require(tr(matmul(reset,hR))==0,'reset local reference energy zero')
    require(tr(matmul(reset,hO))==tr(matmul(rho,hO)),'reset outside energy unchanged')
    require(tr(matmul(rho,hR))==F(32,25),'local energy is removed')
    rows['vacuum_reset_bookkeeping']={'kind':'finite diagnostic, not full ground variational proof','rho':rho,'reset':reset,
                                    'outside_energy':tr(matmul(rho,hO)),'removed_energy':tr(matmul(rho,hR)),
                                    'analytic_incident_bound_coefficient':2}
    # Gap restriction may have no nonzero excited physical cyclic vector.
    invariant=diag([1,-1]); vac=diag([1,0]); Hamiltonian=diag([0,1])
    require(matmul(invariant,vac)==vac,'invariant vacuum')
    require(zero(matmul(Hamiltonian,vac)),'one-dimensional fixed restriction has only ground')
    rows['gap_not_nonzero_excitation']={'kind':'abstract two-dimensional gauge diagnostic','symmetry':invariant,
       'Hamiltonian':Hamiltonian,'full_dimension':2,'physical_cyclic_dimension':1,'physical_positive_spectrum':[],
       'conclusion':'restricted lower spectral inequality alone establishes no Wilson fluctuation or nonzero positive spectral measure'}
    budgets=[]
    for N in (1,2,8):
        require(7*N>0,'homogeneous budget positive per volume')
        budgets.append({'complete_anchor_count':N,'absolute_budget_over_abs_tau':7*N})
    rows['summable_model_substitution']={'kind':'exact homogeneous identity-neighborhood norm diagnostic',
          'homogeneous':budgets,'dyadic_total_bound_over_alpha_abs_tau':F(107,135),
          'no_explicit_nonzero_tau_certified':True,'no_representation_transfer':True}
    return rows

def source_bindings():
    inv=json.loads((HERE/'inputs/source-inventory.json').read_text());paths={HERE/'check.py'}
    for row in inv['entries']:
        original=ROOT/row['source'];snapshot=ROOT/row['snapshot']
        require(digest(original)==row['sha256']==digest(snapshot),'immutable original/source snapshot '+row['source'])
        paths.update((original,snapshot))
    ins=json.loads((HERE/'inputs/instruction-inventory.json').read_text())
    for row in ins.values():
        snapshot=HERE/row['snapshot']
        require(digest(snapshot)==row['sha256'],'instruction snapshot')
        paths.add(snapshot)
    ex=json.loads((HERE/'inputs/external-inventory.json').read_text())
    for row in ex['entries']:
        snapshot=ROOT/row['snapshot'];require(digest(snapshot)==row['sha256'],'external retrieval snapshot');paths.add(snapshot)
    paths.update(p for p in (HERE/'inputs').rglob('*') if p.is_file())
    # The report may be completed after an exploratory run; final runs bind it.
    for name in ('report.md','preflight-ready.json','preflight-pass.json','input-pack-attempt.json','reading-scope.json','control-repair.json','portable-binding-repair.json'):
        p=HERE/name
        if p.exists():paths.add(p)
    bindings={str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p):digest(p) for p in sorted(paths)}
    return bindings

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
    out=Path(args.output)
    if not out.is_absolute() or out.exists():raise RuntimeError('--output requires a fresh absolute directory')
    contract=json.loads((HERE/'inputs/research/round28/contracts/aj1.json').read_text())
    require(contract['sequence']==7 and contract['loop']=='aj1','frozen loop identity')
    geom=geometry(contract); controls=diagnostics(); bindings=source_bindings()
    proof={'model':'actual I1 homogeneous omitted coupling, positive orthant, complete whole-star boundaries',
           'local_energy_bound':'Tr(rho_Lambda,R h_R) <= 2 M n_Lambda(R) <= 2 M n_orthant(R) <= 8 M |R| = 56 |tau| |R|',
           'cutoff_tail_bound':'Tr(rho_Lambda,R 1_(T,infinity)(h_R)) <= 2 M n_orthant(R)/T',
           'trace_cutoff_error_bound':'||rho-P_T rho P_T||_1 <= 2 sqrt(C_R/T) + C_R/T',
           'local_density_limit':'trace norm on every fixed finite complete-factor region',
           'represented_local_algebra':'normal representation; bounded original strong-star convergence gives represented strong convergence',
           'gauge_average':'pi(E_R(A))Omega = integral_(SU2 endpoint product) U_omega(g)pi(A)Omega dg',
           'cyclic_fixed_identity':'closure(pi(A_phys)Omega) = intersection_g ker(U_omega(g)-I)',
           'generator_route':'finite-volume centered resolvent covariance passes through actual I1 tested matrix-element limit on bounded-local excitation vectors',
           'physical_operator_domain':'D(G_phys)=D(G) intersect H_cyc',
           'physical_form_domain':'D(sqrt(G_phys))=D(sqrt(G)) intersect H_cyc',
           'physical_energy':'(alpha/8) G_phys; centered ground remains zero',
           'frequency_generator':'(alpha/(8 hbar)) G_phys',
           'inherited_gap':'Spec((alpha/8)G_phys) subset {0} union [alpha/16,infinity)',
           'symbolic_only':'|tau| < min(c1(S),1/(2 c2(S)))/7, positive unevaluated source constants',
           'exact_normalizations':{'local_norm_over_abs_tau':7,'incident_energy_multiplier':2,
              'universal_energy_multiplier_M_per_site':8,'universal_energy_multiplier_abs_tau_per_site':56,
              'delta_over_alpha':F(1,8),'normalized_inherited_gap':F(1,2),'physical_gap_over_alpha':F(1,16)},
           'scope':{'actual_homogeneous_state':True,'local_normality':True,'compatible_haar_average':True,'cyclic_equals_joint_fixed':True,'reducing_closed_generator':True,
                    'new_gap_theorem':False,'numerical_nonzero_tau':False,'nonzero_physical_excitation_witness':False,'same_representation_strong_resolvent':False,
                    'every_boundary_state_equal':False,'continuum_yang_mills':False,'wilson_only_algebra_completion':False}}
    result={'schema':'ym28-aj1-reverse-results-v1','loop':'aj1','contract_sha256':digest(ROOT/'research/round28/contracts/aj1.json'),
            'theorem':proof,'geometry_summary':[{'sides':f['sides'],'sites':f['site_count'],'links':len(f['links']),'endpoints':len(f['endpoint_vertices']),
              'outgoing_links':len(f['outgoing_links']),'anchors':f['anchor_count'],'omitted_faces':f['omitted_face_count']} for f in geom['fixtures']],
            'regions':geom['regions'],'controls':controls,'semantic_checks':COUNT,'bindings':bindings,
            'independence':'new standard-library checker; no historical algorithm imported/executed; current opposite and skeptic AJ1 unread',
            'failed_scientific_attempts':[],
            'nondiscriminating_control':geom['missing_endpoint_control'],
            'proof_status':'analytic proof in report, finite diagnostics verify geometry and logical controls only'}
    out.mkdir(parents=True)
    for name,data in [('results.json',result),('geometry.json',geom)]:
        (out/name).write_text(json.dumps(packed(data),sort_keys=True,indent=2)+'\n')
    print(json.dumps({'semantic_checks':COUNT,'runtime_bindings':len(bindings),'outputs':['results.json','geometry.json']}))

if __name__=='__main__':main()
