#!/usr/bin/env python3
"""P2 exact graph, quaternion jets, electric incidence and reserved moments."""
from fractions import Fraction as F
from itertools import product, combinations
from math import factorial
from pathlib import Path
import argparse
import hashlib
import json

ROOT=Path(__file__).absolute().parents[4]
BASE='research/round22/forward/p2/'
CONTRACT='research/round22/contracts/p2.json'
CONTRACT_SHA='2eb4ae79a730a2c9ede7661d7024668800b9b15641eaaa44afd9aa5011e62ae1'
LEDGER='research/round19/forward/c1/output/graph-reduction.json'
INSTRUCTIONS=['research/round22/methods/team-protocol.md',
 'research/round22/methods/v3/AGENTS-at-selection.md',
 'research/round22/methods/v3/generated-support-and-iteration.md',
 'research/round22/methods/v3/paired-physics-research-at-selection.md',
 'research/round22/methods/v3/stationarity-support-and-admission.md']
DEPENDENCIES=['research/round19/advisor/c1-gate.json',LEDGER,
 'research/round21/advisor/k1-gate.json','research/round22/advisor/p1-decision.md',
 'research/round22/advisor/p1-gate.json',
 'research/round22/advisor/physical-source-preparation.json','research/round22/skeptic/p1.md']
INPUTS=[CONTRACT,*INSTRUCTIONS,*DEPENDENCIES,'research/round21/forward/k1/report.md',
 'research/round22/forward/p1/report.md','research/round22/forward/p1/source-notes.md',
 'research/round22/forward/p1/check.py',BASE+'report.md',BASE+'source-notes.md',BASE+'check.py']
TREE=list(range(16))+[26]
SELECTED=[28,27,24]
Q0=(F(0),)*4
QI=(F(1),F(0),F(0),F(0))


def need(ok,why):
    if type(ok) is not bool or not ok:raise ValueError(why)


def safe(path):
    for p in [path.absolute(),*path.absolute().parents]:need(not p.is_symlink(),'symlink component')


def sha(path):
    safe(path);need(path.is_file(),'missing source '+str(path))
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path,data):path.write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
def encode(q):return [str(x) for x in q]
def qadd(a,b):return tuple(x+y for x,y in zip(a,b))
def qscale(c,a):return tuple(c*x for x in a)
def qconj(a):return (a[0],-a[1],-a[2],-a[3])


def qm(a,b):
    w,x,y,z=a;v,r,s,t=b
    return (w*v-x*r-y*s-z*t,w*r+x*v+y*t-z*s,
            w*s+y*v+z*r-x*t,w*t+z*v+x*s-y*r)


def jet(q):return (q,Q0,Q0)


def jm(a,b):
    out=[]
    for n in range(3):
        q=Q0
        for k in range(n+1):q=qadd(q,qm(a[k],b[n-k]))
        out.append(q)
    return tuple(out)


def jc(a):return tuple(qconj(x) for x in a)


def je(axis,sign=1):
    tangent=tuple(F(sign,2) if j==axis+1 else F(0) for j in range(4))
    return (QI,tangent,qscale(-F(sign*sign,8),QI))


def jword(g,word):
    value=jet(QI)
    for e,s in word:value=jm(value,g[e] if s==1 else jc(g[e]))
    return value


def graph():
    sizes=(3,3,2);vertices=list(product(*(range(n) for n in sizes)))
    edges=[];lookup={}
    def shift(p,a):return tuple(p[j]+int(j==a) for j in range(3))
    for a in range(3):
        for p in product(*(range(n-int(j==a)) for j,n in enumerate(sizes))):
            lookup[(a,p)]=len(edges);edges.append((p,shift(p,a)))
    root=(0,2,0);paths={root:[]}
    while len(paths)<len(vertices):
        before=len(paths)
        for e in TREE:
            s,t=edges[e]
            if s in paths and t not in paths:paths[t]=paths[s]+[(e,1)]
            if t in paths and s not in paths:paths[s]=paths[t]+[(e,-1)]
        need(len(paths)>before,'tree disconnected')
    need(len(TREE)==len(vertices)-1,'tree edge count')
    chords=[e for e in range(len(edges)) if e not in TREE]
    words={e:paths[s]+[(e,1)]+[(b,-o) for b,o in reversed(paths[t])]
           for e,(s,t) in enumerate(edges) if e in chords}
    def eta(b,v):return next((o for e,o in paths[v] if e==b),0)
    cuts={b:[(eta(b,edges[e][0]),-eta(b,edges[e][1])) for e in chords] for b in TREE}
    inherited=json.loads((ROOT/LEDGER).read_text())
    rows={x['face_id']:x for x in inherited['affected_faces']+inherited['constant_faces']}
    count=0
    for a,b in combinations(range(3),2):
        for p in product(*(range(n-int(j in (a,b))) for j,n in enumerate(sizes))):
            word=[(lookup[(a,p)],1),(lookup[(b,shift(p,a))],1),
                  (lookup[(a,shift(p,b))],-1),(lookup[(b,p)],-1)]
            need(rows[count]['signed_word']==[{'edge':e,'sign':s} for e,s in word],
                 'inherited face orientation mismatch')
            count+=1
    need((len(vertices),len(edges),count,len(chords))==(18,33,20,16),'actual graph counts')
    return vertices,edges,paths,chords,words,cuts


def padd(a,b):return [(a[j] if j<len(a) else F(0))+(b[j] if j<len(b) else F(0))
                     for j in range(max(len(a),len(b)))]
def pscale(c,a):return [c*x for x in a]
def pmul(a,b):
    out=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):out[i+j]+=x*y
    return out
def deriv(a):return [i*a[i] for i in range(1,len(a))] or [F(0)]
def haar(p):
    total=F(0);moment=F(1)
    for j in range(0,len(p),2):
        if j:moment*=F(j-1,j+2)
        total+=p[j]*moment
    return total


def checks():
    controls=[]
    def control(name,ok,outcome):
        need(ok,'failed control '+name)
        controls.append({'name':name,'passed':True,'outcome':outcome})
    vertices,edges,paths,chords,words,cuts=graph()
    expected={28:[(14,-1),(2,1),(28,1),(3,-1),(15,1),(26,-1)],
      27:[(14,-1),(12,-1),(0,1),(27,1),(1,-1),(13,1),(15,1),(26,-1)],
      24:[(14,-1),(12,-1),(24,1),(13,1),(15,1),(26,-1)]}
    control('full_tree_and_physical_completions',all(words[e]==w for e,w in expected.items()),
            {'tree':TREE,'chords':chords,'root':[0,2,0],
             'selected_words':{str(e):words[e] for e in SELECTED},'all_20_faces_checked':True})
    pool=[(F(3,5),F(4,5),F(0),F(0)),(F(5,13),F(0),F(12,13),F(0)),
          (F(0),F(0),F(0),F(1))]
    need(all(qm(q,qconj(q))==QI for q in pool),'unit quaternions')
    g=[pool[e%3] for e in range(33)]
    gj=[jet(q) for q in g]
    hv={v:jword(gj,p)[0] for v,p in paths.items()}
    loops={e:jword(gj,words[e])[0] for e in chords}
    reconstructed=list(g)
    for e in chords:
        s,t=edges[e];reconstructed[e]=qm(qm(qconj(hv[s]),loops[e]),hv[t])
    gauge={v:pool[i%3] for i,v in enumerate(vertices)}
    transformed=[qm(qm(gauge[s],g[e]),qconj(gauge[t])) for e,(s,t) in enumerate(edges)]
    transformed_loops={e:jword([jet(q) for q in transformed],words[e])[0] for e in chords}
    root_gauge=gauge[(0,2,0)]
    equivariance=all(transformed_loops[e]==qm(qm(root_gauge,loops[e]),qconj(root_gauge)) for e in chords)
    fixed=[qm(qm(hv[s],g[e]),qconj(hv[t])) for e,(s,t) in enumerate(edges)]
    control('haar_coordinates_inverse_and_gauge_equivariance',
            reconstructed==g and equivariance and all(fixed[e]==QI for e in TREE)
            and all(fixed[e]==loops[e] for e in chords),
            {'all_33_inverse_coordinates':True,'all_16_root_conjugations':True,'all_17_tree_links_identity':True})
    wrong=[e for e in chords if qm(qm(hv[edges[e][0]],g[e]),hv[edges[e][1]])!=loops[e]]
    control('missing_terminal_inverse_rejected',len(wrong)>0,{'mismatching_chords':wrong})
    # On each invariant test x+y*o, omitted o is independent normalized trace.
    var=haar([F(0),F(0),F(1)])
    original_norm=var+var*var;projection_norm=var;evaluation_norm=2*var
    control('haar_projection_is_not_identity_evaluation',
            projection_norm<=original_norm<evaluation_norm and var==F(1,4),
            {'test':'x+y*o, o an omitted chord trace',
             'full_norm_squared':str(original_norm),'projected_norm_squared':str(projection_norm),
             'identity_evaluation_norm_squared':str(evaluation_norm),'omitted_variables_integrated':13})
    # Full second-order transport on all 16 chords, every 17 tree links and axis.
    config=[jet(QI) if e in TREE else jet(pool[e%3]) for e in range(33)]
    base_loops={e:jword(config,words[e]) for e in chords}
    cases=0
    for b in TREE:
        for a in range(3):
            varied=list(config);varied[b]=je(a)
            for k,e in enumerate(chords):
                left,right=cuts[b][k]
                expected_jet=jm(jm(je(a,left),base_loops[e]),je(a,right))
                need(jword(varied,words[e])==expected_jet,'electric signed jet transport')
                cases+=1
    control('all_tree_derivatives_and_signs_retained',cases==17*3*16,
            {'exact_second_order_jet_cases':cases,'coefficient_order':2,'axes':3,'tree_links':17,'chords':16})
    selected_cuts={b:[cuts[b][chords.index(e)] for e in SELECTED] for b in TREE}
    gram=[[F(int(i==j and i%2==0)) for j in range(6)] for i in range(6)]
    for row in selected_cuts.values():
        v=[x for pair in row for x in pair]
        for i in range(6):
            for j in range(6):gram[i][j]+=v[i]*v[j]
    diagonal=[gram[2*j][2*j]+gram[2*j+1][2*j+1] for j in range(3)]
    control('selected_full_electric_form_not_bare_chord_sum',diagonal==[6,8,6],
            {'basis':['ell_U','r_U','ell_V','r_V','ell_W','r_W'],
             'gram_matrix':[[str(x) for x in row] for row in gram],
             'single_variable_coefficients':[str(x) for x in diagonal],
             'tree_cuts':{str(b):selected_cuts[b] for b in TREE}})
    cross_config=[jet(QI) for e in range(33)]
    pure=(F(0),F(1),F(0),F(0));cross_config[28]=cross_config[27]=jet(pure)
    electric_xy=F(0)
    for e in range(33):
        for a in range(3):
            varied=list(cross_config);varied[e]=jm(je(a),cross_config[e])
            xu=[q[0] for q in jword(varied,words[28])]
            yv=[q[0] for q in jword(varied,words[27])]
            electric_xy-=2*sum(xu[k]*yv[2-k] for k in range(3))
    incidence_xy=-F(1,2)*(gram[0][2]+gram[1][3])
    control('shared_tree_cross_terms_cannot_be_dropped',electric_xy==incidence_xy==-F(3,2),
            {'test':'xy at U=V=-i sigma1,W=I','full_33_link_value_over_alpha':str(electric_xy),
             'induced_incidence_value_over_alpha':str(incidence_xy),'diagonal_only_value':'0'})
    lengths=[len(words[e]) for e in SELECTED]
    need(all(len({b for b,s in words[e]})==len(words[e]) for e in SELECTED),'simple selected loops')
    energies=[F(3,4)*n for n in lengths]
    control('old_section_completion_and_clock_rejected',lengths==[6,8,6] and energies[0]!=3,
            {'loop_lengths':lengths,'energies_over_alpha':[str(x) for x in energies],
             'P1_F9_energy_over_alpha':'3'})
    x=[F(0),F(1)];one_minus_x2=[F(1),F(0),F(-1)]
    Cx=padd(pscale(F(3,4),pmul(x,deriv(x))),pscale(-F(1,4),pmul(one_minus_x2,deriv(deriv(x)))))
    mobility_part=padd(pmul(x,Cx),pscale(-F(1,4),pmul(one_minus_x2,deriv(x))))
    mean=haar(mobility_part);a=haar(pmul(Cx,Cx));b=haar(pmul(Cx,mobility_part));d=haar(pmul(mobility_part,mobility_part))
    control('mobility_divergence_drift_required',mean==0 and haar(pmul(x,Cx))==F(3,16),
            {'A_zeta_x_constant_part':[str(v) for v in Cx],
             'A_zeta_x_zeta_part':[str(v) for v in mobility_part],
             'wrong_driftless_mean_over_zeta':'3/16','correct_mean':'0'})
    physical_rate=energies[0]*var;conditional_rate=haar(pmul(x,Cx));fit=physical_rate/conditional_rate
    control('training_slope_fits_c_but_leaves_zeta',fit==6 and haar(pmul(x,mobility_part))==0,
            {'physical_rate_over_alpha':str(physical_rate),'conditional_rate_over_c':str(conditional_rate),
             'c_over_alpha':str(fit),'zeta_from_slope':'all (-1,1)'})
    phys_curvature=energies[0]**2*var;cond_const=fit*fit*a;cond_zeta2=fit*fit*d
    control('reserved_curvature_rejects_nonzero_zeta',
            b==0 and phys_curvature==cond_const==F(81,16) and cond_zeta2==F(9,4),
            {'physical_curvature_times_hbar_squared_over_alpha_squared':str(phys_curvature),
             'conditional_curvature_constant':str(cond_const),'conditional_zeta_squared_coefficient':str(cond_zeta2),
             'remaining_zeta':'0 only'})
    cond_y=fit*F(3,4);phys_y=energies[1]
    control('reserved_y_full_curve_cannot_match_any_remaining_zeta',
            cond_y==F(9,2) and phys_y==6 and cond_y*var!=phys_y*var,
            {'physical_y_energy_over_alpha':str(phys_y),'conditional_y_energy_at_zeta_zero_over_alpha':str(cond_y),
             'all_zeta_conditional_y_rate_over_alpha':str(cond_y*var),
             'physical_y_rate_over_alpha':str(phys_y*var)})
    lo=sum((F((-1)**k,2**k*factorial(k)) for k in range(32)),F(0))
    hi=lo+F(1,2**32*factorial(32))
    dlo=(lo**9-hi**12)/4;dhi=(hi**9-lo**12)/4
    dec_lo='0.00215756109039398701827449';dec_hi='0.00215756109039398701827450'
    control('positive_full_time_defect_certified',F(0)<F(dec_lo)<dlo<dhi<F(dec_hi),
            {'t_star':'hbar/alpha','difference':'(exp(-9/2)-exp(-6))/4',
             'strict_decimal_interval':[dec_lo,dec_hi],
             'exp_minus_half_bounds':[str(lo),str(hi)],'rational_defect_bounds':[str(dlo),str(dhi)]})
    refit=phys_y/F(3,4)
    control('heldout_refit_and_scalar_repair_rejected',refit==8 and refit*conditional_rate!=physical_rate,
            {'forbidden_y_refit_c_over_alpha':str(refit),'training_required_c_over_alpha':str(fit),
             'allowed_scalar_from_constant_ground':'0'})
    rejects=0
    for bad in [False,1,'passed']:
        try:need(bad,'deliberate rejection')
        except ValueError:rejects+=1
    control('strict_checks_survive_optimized_python',rejects==3,{'rejected':['False','integer','string']})
    claims={'full_Haar_identification_unitary_onto':True,'selected_map_isometry':True,
      'selected_adjoint':'Haar integration over 13 omitted chords after J16 inverse',
      'selected_image_reduces_electric_operator':True,'state_and_ground_preserved':True,
      'full_tree_derivatives_retained':17,'full_chords_retained':16,
      'full_operator':'alpha(sum_chord C-sum_tree,a D_tree,a^2)',
      'selected_operator':'alpha(3CU+3CV+CW+KL(VW)+KR(VW)+KL(UVW)+2KR(UVW))',
      'form_domain':'H1 intersect simultaneous-Ad invariant sector',
      'operator_domain':'H2 intersect simultaneous-Ad invariant sector',
      'exact_graph_norm_isometry':True,'exact_semigroup_intertwining':True,
      'mapped_x_energy':'9 alpha/2','mapped_y_energy':'6 alpha','mapped_z_energy':'9 alpha/2',
      'mapped_x_is_P1_F9':False,'training_c_over_alpha':'6','zeta_after_slope':'(-1,1)',
      'curvature_defect_times_hbar_squared':'9 alpha^2 zeta^2/4','zeta_after_curvature':'0',
      'reserved_y_physical_correlation':'exp(-6 alpha t/hbar)/4',
      'reserved_y_conditional_correlation_after_curvature':'exp(-9 alpha t/(2 hbar))/4',
      'reserved_positive_time_defect':'(exp(-9s/2)-exp(-6s))/4, s=alpha t/hbar>0',
      't_star_defect_interval':[dec_lo,dec_hi],'conditional_family_match':False,
      'physical_calibration':'open','measured_calibration':False,'interacting_transfer':False,
      'continuum_transfer':False,'Q_R_selected':False}
    results={'schema':'ym22-forward-p2-results-v1','loop':'p2','direction':'forward',
      'status':'proved_scoped','passed':True,'claims':claims,
      'tree_paths':{''.join(map(str,v)):paths[v] for v in sorted(paths)},
      'complete_electric_incidence':{str(b):{str(e):cuts[b][i] for i,e in enumerate(chords)} for b in TREE},
      'selected_physical_words':{str(e):words[e] for e in SELECTED},
      'fixtures_replace_domain_proof':False,'proof_location':BASE+'report.md','scientific_priority':'unverified'}
    return results,{'schema':'ym22-forward-p2-controls-v1','loop':'p2','direction':'forward',
                    'passed':True,'controls':controls}


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    out=p.parse_args().output.absolute();safe(out);need(not out.exists(),'fresh output required')
    inputs={p:sha(ROOT/p) for p in INPUTS};need(len(inputs)==len(INPUTS),'duplicate input')
    need(inputs[CONTRACT]==CONTRACT_SHA,'frozen P2 contract mismatch')
    c=json.loads((ROOT/CONTRACT).read_text());need(c['loop']=='p2' and c['status']=='frozen','contract identity')
    for p,h in c['dependencies'].items():need(p in inputs and inputs[p]==h,'dependency mismatch '+p)
    for p in c['instruction_inputs']:need(p in inputs,'required instruction missing '+p)
    for p in ['research/round19/advisor/c1-gate.json','research/round21/advisor/k1-gate.json',
              'research/round22/advisor/p1-gate.json']:
        gate=json.loads((ROOT/p).read_text())
        need(gate['status']=='accepted','inherited accepted gate')
        for k,h in inputs.items():
            if k in gate['files']:need(gate['files'][k]==h,'admitted source mismatch '+k)
    results,controls=checks();out.mkdir(parents=True,exist_ok=False)
    save(out/'results.json',results);save(out/'controls.json',controls)
    save(out/'source-manifest.json',{'schema':'ym22-producer-source-manifest-v1',
      'loop':'p2','direction':'forward','inputs':inputs,
      'outputs':{p:sha(out/p) for p in ['results.json','controls.json']},
      'import_policy':'standard-library only; no other producer imports',
      'manifest_self_hash':'bound by submission inventory'})
    print(json.dumps({'loop':'p2','direction':'forward','status':'proved_scoped','passed':True,
                      'controls':len(controls['controls'])},sort_keys=True))


if __name__=='__main__':main()
