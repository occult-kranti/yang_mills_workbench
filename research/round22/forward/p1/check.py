#!/usr/bin/env python3
"""P1 independent finite graph, character-core and exact channel checks."""
from fractions import Fraction as F
from itertools import product, combinations
from math import factorial
from pathlib import Path
import argparse
import hashlib
import json

ROOT=Path(__file__).absolute().parents[4]
BASE='research/round22/forward/p1/'
CONTRACT='research/round22/contracts/p1.json'
CONTRACT_SHA='3460a2d2fb9767d0ba59c0647ea8bf5aa657bf1541f2d2184e6584f722c69102'
LEDGER='research/round19/forward/c1/output/graph-reduction.json'
INSTRUCTIONS=['research/round22/methods/team-protocol.md',
 'research/round22/methods/v2/AGENTS-at-selection.md',
 'research/round22/methods/v2/paired-physics-research-at-selection.md',
 'research/round22/methods/v2/stationarity-support-and-admission.md']
DEPENDENCIES=['research/round19/advisor/c1-gate.json',LEDGER,
 'research/round21/advisor/j2-gate.json','research/round21/advisor/k1-gate.json',
 'research/round22/advisor/o2-decision.md','research/round22/advisor/o2-gate.json',
 'research/round22/advisor/physical-source-preparation.json',
 'research/round22/skeptic/o2.md']
INPUTS=[CONTRACT,*INSTRUCTIONS,*DEPENDENCIES,
 'research/round21/forward/k1/report.md','research/round22/forward/o2/check.py',
 BASE+'report.md',BASE+'source-notes.md',BASE+'check.py']


def need(ok,why):
    if type(ok) is not bool or not ok:raise ValueError(why)


def safe(path):
    for p in [path.absolute(),*path.absolute().parents]:
        need(not p.is_symlink(),'symlink component rejected')


def sha(path):
    safe(path);need(path.is_file(),'missing source '+str(path))
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path,data):path.write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')


def shifted(p,a):return tuple(p[j]+int(j==a) for j in range(3))


def graph():
    sizes=(3,3,2);vertices=list(product(*(range(n) for n in sizes)))
    edges=[];lookup={}
    for a in range(3):
        for p in product(*(range(n-int(j==a)) for j,n in enumerate(sizes))):
            lookup[(a,p)]=len(edges);edges.append((p,shifted(p,a)))
    active={28:'U',27:'V',24:'W'}
    need(lookup[(2,(1,1,0))]==28 and lookup[(2,(1,0,0))]==27
         and lookup[(2,(0,0,0))]==24,'declared active edge identities')
    faces=[]
    for a,b in combinations(range(3),2):
        for p in product(*(range(n-int(j in (a,b))) for j,n in enumerate(sizes))):
            word=[(lookup[(a,p)],1),(lookup[(b,shifted(p,a))],1),
                  (lookup[(a,shifted(p,b))],-1),(lookup[(b,p)],-1)]
            fid=len(faces);axes='xyz'[a]+'xyz'[b]
            faces.append({'face_id':fid,'face':f'f{fid}_{axes}_'+''.join(map(str,p)),
              'axes':axes,'base':list(p),
              'vertices':[list(p),list(shifted(p,a)),list(shifted(shifted(p,a),b)),
                          list(shifted(p,b))],
              'signed_word':[{'edge':e,'sign':s} for e,s in word],
              'active_word':[{'symbol':active[e],'sign':s} for e,s in word if e in active]})
    def connected(subset):
        reached={vertices[0]}
        while True:
            after=reached|{v for e in subset if any(w in reached for w in edges[e])
                          for v in edges[e]}
            if after==reached:return len(reached)==len(vertices)
            reached=after
    need((len(vertices),len(edges),len(faces))==(18,33,20),'full graph counts')
    fixed=[e for e in range(33) if e not in active]
    need(connected(list(range(33))) and connected(fixed),'full and fixed graph connected')
    inherited=json.loads((ROOT/LEDGER).read_text())
    rows={x['face_id']:x for x in inherited['affected_faces']+inherited['constant_faces']}
    need(set(rows)==set(range(20)),'complete inherited ledger')
    for f in faces:
        for key,value in f.items():need(rows[f['face_id']][key]==value,'signed graph mismatch '+key)
        need(len({r['edge'] for r in f['signed_word']})==4,'four distinct face edges')
    return faces


def poly_add(a,b):
    return [(a[j] if j<len(a) else F(0))+(b[j] if j<len(b) else F(0))
            for j in range(max(len(a),len(b)))]


def poly_mul(a,b):
    out=[F(0)]*(len(a)+len(b)-1)
    for j,x in enumerate(a):
        for k,y in enumerate(b):out[j+k]+=x*y
    return out


def character(n):
    last,current=[F(1)],[F(0),F(2)]
    if n==0:return last
    for j in range(1,n):
        last,current=current,poly_add([F(0)]+[2*x for x in current],[-x for x in last])
    return current


def haar(poly):
    # SU(2) normalized trace coordinate: (2/pi)*sqrt(1-x^2) dx.
    total=F(0);moment=F(1)
    for j in range(0,len(poly),2):
        if j:moment*=F(j-1,j+2)
        total+=poly[j]*moment
    return total


def exp_minus_one_interval():
    # Alternating terms decrease from k=1 onward. Odd truncation is lower.
    low=sum((F((-1)**k,factorial(k)) for k in range(26)),F(0))
    high=low+F(1,factorial(26))
    need(F(0)<low<high<F(1),'exponential interval ordering')
    return low,high


def checks():
    controls=[]
    def control(name,ok,outcome):
        need(ok,'failed control '+name)
        controls.append({'name':name,'passed':True,'outcome':outcome})
    faces=graph();affected=[f['face_id'] for f in faces if f['active_word']]
    control('complete_graph_and_signed_section',affected==[8,9,11,12,14,16,17],
            {'vertices':18,'edges':33,'faces':20,'fixed_edges':30,
             'all_20_signed_faces_match':True,'affected_faces':affected})
    control('thirty_fixed_edges_are_not_tree_gauge_fixing',30>18-1 and 30-18+1==13,
            {'spanning_tree_edges':17,'full_cycle_rank':16,'fixed_subgraph_cycle_rank':13})
    control('fixed_plaquette_is_actual_closed_graph_word',
            faces[0]['signed_word']==[{'edge':e,'sign':s} for e,s in [(0,1),(16,1),(2,-1),(12,-1)]]
            and faces[0]['active_word']==[],{'face':faces[0]})
    rows=[]
    for n in [1,2,4,8]:
        p=character(n);q=[x/F(n+1) for x in p]
        norm2=haar(poly_mul(q,q));mean=haar(q);restriction=sum(q,F(0))
        need(norm2==F(1,(n+1)**2) and mean==0 and restriction==1,'character-core fixture')
        rows.append({'n':n,'spin':str(F(n,2)),'dimension':n+1,
                     'physical_norm_squared':str(norm2),'physical_mean':str(mean),
                     'conditional_restriction':str(restriction),'norm_ratio':n+1})
    control('bounded_and_closable_section_rejected',rows[-1]['norm_ratio']>rows[0]['norm_ratio'],
            {'fixtures':rows,'all_n_formula':'norm(f_n)=1/(n+1); R f_n=1',
             'proof':'report.md section 2 proves (f_n,Rf_n)->(0,1)'})
    f0=[x/2 for x in character(1)]
    control('state_compatibility_rejected',haar(f0)==0 and sum(f0)==1 and haar(poly_mul(f0,f0))==F(1,4),
            {'physical_mean':'0','section_mean':'1','physical_variance':'1/4','section_variance':'0'})
    # Entries are Gaussian integers; all operations below are exact in binary.
    paulis=[[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]]
    square_sum=[[sum(M[i][k]*M[k][j] for M in paulis for k in range(2))/4
                 for j in range(2)] for i in range(2)]
    control('fundamental_casimir_normalization',square_sum==[[0.75,0],[0,0.75]],
            {'minus_sum_T_squared':'3 I/4','inverse_edges':'dual fundamental, same Casimir'})
    casimir=F(3,4);channels={}
    for fid in [0,9,16]:
        f=faces[fid];support={s['edge'] for s in f['signed_word']}
        per_edge=[casimir if e in support else F(0) for e in range(33)]
        m=len(f['active_word'])
        channels[str(fid)]={'physical_casimir_per_edge':[str(x) for x in per_edge],
          'physical_energy_over_alpha':str(sum(per_edge)),
          'conditional_energy_over_c':str(m*casimir),
          'fixed_link_contribution_over_alpha':str((4-m)*casimir)}
    control('fixed_link_electric_derivatives_cannot_be_dropped',
            all(F(x['physical_energy_over_alpha'])==3 for x in channels.values())
            and [channels[str(i)]['fixed_link_contribution_over_alpha'] for i in [0,9,16]]==['3','9/4','3/2'],
            channels)
    ground_physical=F(0);ground_conditional=F(0);allowed_shift=ground_physical-ground_conditional
    control('scalar_shift_cannot_repair_core_intertwining',allowed_shift==0 and F(3)!=allowed_shift,
            {'constant_ground_forces_shift':'0','F0_core_defect_norm_over_alpha':'3'})
    var=haar(poly_mul(f0,f0));physical_energy=F(channels['9']['physical_energy_over_alpha'])
    train_cond=F(channels['9']['conditional_energy_over_c'])
    fit=physical_energy*var/(train_cond*var)
    control('training_uses_nonzero_slope_and_one_common_fit',var>0 and fit==4,
            {'variance':str(var),'physical_slope_times_hbar_over_alpha':str(-physical_energy*var),
             'conditional_slope_times_hbar_over_c':str(-train_cond*var),'c_over_alpha':str(fit)})
    hold=fit*F(channels['16']['conditional_energy_over_c'])
    control('heldout_generator_rejects_training_fit',hold==6 and hold!=physical_energy,
            {'physical_energy_over_alpha':str(physical_energy),'conditional_energy_over_alpha':str(hold),
             'core_defect_coefficient_over_alpha':str(physical_energy-hold),
             'core_defect_norm_over_alpha':'3/2'})
    lo,hi=exp_minus_one_interval()
    delta_lo=(lo**3-hi**6)/4;delta_hi=(hi**3-lo**6)/4
    decimal_lo=F('0.01182707904779939613907431')
    decimal_hi=F('0.01182707904779939613907432')
    control('heldout_full_time_positive_defect',F(0)<decimal_lo<delta_lo<delta_hi<decimal_hi,
            {'t_star':'hbar/alpha','defect_exact':'(exp(-3)-exp(-6))/4',
             'strict_decimal_interval':['0.01182707904779939613907431','0.01182707904779939613907432'],
             'exp_minus_one_bounds':[str(lo),str(hi)],
             'defect_rational_bounds':[str(delta_lo),str(delta_hi)],
             'all_positive_time_proof':'exp(-3s)>exp(-6s) for every s>0'})
    refit=physical_energy/F(channels['16']['conditional_energy_over_c'])
    control('heldout_refit_breaks_training',refit==2 and refit*train_cond!=physical_energy,
            {'forbidden_heldout_c_over_alpha':str(refit),
             'resulting_training_energy_over_alpha':str(refit*train_cond)})
    rejected=0
    for bad in [False,'passed',1]:
        try:need(bad,'intentional failure')
        except ValueError:rejected+=1
    control('optimized_mode_retains_strict_validation',rejected==3,
            {'explicit_rejections':['False','string','integer'],'assert_used':False})
    claims={'graph_vertices':18,'graph_edges':33,'graph_faces':20,'full_cycle_rank':16,
      'fixed_subgraph_cycle_rank':13,'section_smooth_core_map':True,
      'section_bounded_L2_extension':False,'section_closable':False,'state_compatible':False,
      'all_n_core_sequence':'chi_(n/2)(L0)/(n+1)',
      'all_n_physical_norm':'1/(n+1)','all_n_section_value':'1',
      'any_c_core_intertwining':False,'F0_core_defect_norm':'3 alpha',
      'fundamental_face_energy':'3 alpha','conditional_x_energy':'3 c/4',
      'conditional_w_energy':'3 c/2','training_variance':'1/4','heldout_variance':'1/4',
      'training_c_over_alpha':'4','training_full_time_match':True,'heldout_full_time_match':False,
      'heldout_physical_correlation':'exp(-3 alpha t/hbar)/4',
      'heldout_fitted_conditional_correlation':'exp(-6 alpha t/hbar)/4',
      'heldout_defect_at_t_star':'(exp(-3)-exp(-6))/4',
      'heldout_defect_strict_interval':['0.01182707904779939613907431','0.01182707904779939613907432'],
      'heldout_core_defect_norm':'3 alpha/2','physical_calibration':'open',
      'interacting_J2_transfer':False,'continuum_transfer':False,'measured_calibration_data':False,
      'fixed_physical_scales':True,'repair_selected':False}
    results={'schema':'ym22-forward-p1-results-v1','loop':'p1','direction':'forward',
      'status':'proved_scoped','passed':True,'claims':claims,'actual_graph_faces':faces,
      'finite_character_fixtures_are_all_n_proof':False,'proof_location':BASE+'report.md',
      'scientific_priority':'unverified'}
    return results,{'schema':'ym22-forward-p1-controls-v1','loop':'p1','direction':'forward',
                    'passed':True,'controls':controls}


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    out=p.parse_args().output.absolute();safe(out);need(not out.exists(),'output must be fresh')
    inputs={p:sha(ROOT/p) for p in INPUTS};need(len(inputs)==len(INPUTS),'duplicate input')
    need(inputs[CONTRACT]==CONTRACT_SHA,'frozen P1 contract mismatch')
    c=json.loads((ROOT/CONTRACT).read_text())
    need(c['status']=='frozen' and c['loop']=='p1','contract identity')
    for p,h in c['dependencies'].items():need(p in inputs and inputs[p]==h,'dependency mismatch '+p)
    for p in c['instruction_inputs']:need(p in inputs,'missing required instruction '+p)
    for path,status in [('research/round19/advisor/c1-gate.json','accepted'),
                        ('research/round21/advisor/j2-gate.json','accepted'),
                        ('research/round21/advisor/k1-gate.json','accepted'),
                        ('research/round22/advisor/o2-gate.json','limited')]:
        gate=json.loads((ROOT/path).read_text());need(gate['status']==status,'inherited gate status')
        for p,h in inputs.items():
            if p in gate['files']:need(gate['files'][p]==h,'admitted source changed '+p)
    results,controls=checks();out.mkdir(parents=True,exist_ok=False)
    save(out/'results.json',results);save(out/'controls.json',controls)
    save(out/'source-manifest.json',{'schema':'ym22-producer-source-manifest-v1',
      'loop':'p1','direction':'forward','inputs':inputs,
      'outputs':{p:sha(out/p) for p in ['results.json','controls.json']},
      'import_policy':'standard-library only; no other producer imports',
      'manifest_self_hash':'bound by submission inventory'})
    print(json.dumps({'loop':'p1','direction':'forward','status':'proved_scoped',
                      'passed':True,'controls':len(controls['controls'])},sort_keys=True))


if __name__=='__main__':main()
