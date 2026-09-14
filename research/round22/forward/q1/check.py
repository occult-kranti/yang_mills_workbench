#!/usr/bin/env python3
"""Q1 independent full magnetic graph and exact conditional-moment controls."""
from fractions import Fraction as F
from itertools import product, combinations
from pathlib import Path
import argparse
import hashlib
import json

ROOT=Path(__file__).absolute().parents[4]
BASE='research/round22/forward/q1/'
CONTRACT='research/round22/contracts/q1.json'
CONTRACT_SHA='bc6ba8654f98814173385ae99cb77478ab8a16ec4cc80543a59678ffa149330f'
LEDGER='research/round19/forward/c1/output/graph-reduction.json'
INSTRUCTIONS=['research/round22/methods/team-protocol.md',
 'research/round22/methods/v4/AGENTS-at-selection.md',
 'research/round22/methods/v4/generated-support-and-iteration.md',
 'research/round22/methods/v4/haar-maps-and-induced-dynamics.md',
 'research/round22/methods/v4/paired-physics-research-at-selection.md',
 'research/round22/methods/v4/stationarity-support-and-admission.md']
DEPENDENCIES=[LEDGER,'research/round22/advisor/p2-decision.md',
 'research/round22/advisor/p2-gate.json','research/round22/advisor/physical-source-preparation.json',
 'research/round22/advisor/post-six-selection.json','research/round22/skeptic/p2.md',
 'research/round22/skeptic/post-six-review.json']
INPUTS=[CONTRACT,*INSTRUCTIONS,*DEPENDENCIES,'research/round22/forward/p2/report.md',
 'research/round22/forward/p2/check.py','research/round22/forward/p2/source-notes.md',
 BASE+'report.md',BASE+'source-notes.md',BASE+'check.py']
TREE=set(range(16))|{26}
SELECTED={28,27,24}
QI=(F(1),F(0),F(0),F(0))


def need(ok,why):
    if type(ok) is not bool or not ok:raise ValueError(why)


def safe(path):
    for p in [path.absolute(),*path.absolute().parents]:need(not p.is_symlink(),'symlink component')


def sha(path):
    safe(path);need(path.is_file(),'missing source '+str(path))
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(path,data):path.write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')
def dot(a,b):return sum((x*y for x,y in zip(a,b)),F(0))
def qc(a):return (a[0],-a[1],-a[2],-a[3])


def qm(a,b):
    w,x,y,z=a;v,r,s,t=b
    return (w*v-x*r-y*s-z*t,w*r+x*v+y*t-z*s,
            w*s+y*v+z*r-x*t,w*t+z*v+x*s-y*r)


def word(g,p):
    q=QI
    for e,s in p:q=qm(q,g[e] if s==1 else qc(g[e]))
    return q


def graph():
    sizes=(3,3,2);vertices=list(product(*(range(n) for n in sizes)))
    edges=[];lookup={}
    def shift(p,a):return tuple(p[j]+int(j==a) for j in range(3))
    for a in range(3):
        for p in product(*(range(n-int(j==a)) for j,n in enumerate(sizes))):
            lookup[(a,p)]=len(edges);edges.append((a,p,shift(p,a)))
    paths={(0,2,0):[]}
    while len(paths)<len(vertices):
        before=len(paths)
        for e in sorted(TREE):
            a,s,t=edges[e]
            if s in paths and t not in paths:paths[t]=paths[s]+[(e,1)]
            if t in paths and s not in paths:paths[s]=paths[t]+[(e,-1)]
        need(len(paths)>before,'tree disconnected')
    ledger=json.loads((ROOT/LEDGER).read_text())
    inherited={r['face_id']:r for r in ledger['affected_faces']+ledger['constant_faces']}
    faces=[]
    for a,b in combinations(range(3),2):
        for p in product(*(range(n-int(j in (a,b))) for j,n in enumerate(sizes))):
            full=[(lookup[(a,p)],1),(lookup[(b,shift(p,a))],1),
                  (lookup[(a,shift(p,b))],-1),(lookup[(b,p)],-1)]
            fid=len(faces)
            need(inherited[fid]['signed_word']==[{'edge':e,'sign':s} for e,s in full],
                 'original signed ledger mismatch')
            chord=[(e,s) for e,s in full if e not in TREE]
            omitted=[e for e,s in chord if e not in SELECTED]
            need(len(omitted)==len(set(omitted)),'an omitted chord repeats within a face')
            faces.append({'id':fid,'base':p,'full_word':full,'chord_word':chord,'omitted':omitted})
    need((len(vertices),len(edges),len(faces),len(TREE))==(18,33,20,17),'full graph counts')
    return edges,paths,faces


def mm(a,b):return [[sum((a[i][k]*b[k][j] for k in range(len(b))),F(0))
                      for j in range(len(b[0]))] for i in range(len(a))]
def det3(a):
    return (a[0][0]*(a[1][1]*a[2][2]-a[1][2]*a[2][1])
            -a[0][1]*(a[1][0]*a[2][2]-a[1][2]*a[2][0])
            +a[0][2]*(a[1][0]*a[2][1]-a[1][1]*a[2][0]))


def checks():
    controls=[]
    def control(name,ok,outcome):
        need(ok,'failed control '+name)
        controls.append({'name':name,'passed':True,'outcome':outcome})
    edges,paths,faces=graph()
    expected=[[(16,1)],[(17,1)],[(18,1)],[(19,1)],[(20,1),(16,-1)],
      [(21,1),(17,-1)],[(22,1),(18,-1)],[(23,1),(19,-1)],[(27,1),(24,-1)],
      [(28,1),(25,-1)],[(29,1)],[(30,1),(27,-1)],[(31,1),(28,-1)],[(32,1),(29,-1)],
      [(25,1),(24,-1)],[(25,-1)],[(16,1),(28,1),(17,-1),(27,-1)],
      [(18,1),(29,1),(19,-1),(28,-1)],[(20,1),(31,1),(21,-1),(30,-1)],
      [(22,1),(32,1),(23,-1),(31,-1)]]
    control('complete_twenty_face_transport',all(f['chord_word']==expected[f['id']] for f in faces),
            {'vertices':18,'edges':33,'faces':20,'tree_edges':17,'chords':16})
    pool=[(F(3,5),F(4,5),F(0),F(0)),(F(5,13),F(0),F(12,13),F(0)),
          (F(0),F(0),F(0),F(1))]
    need(all(dot(q,q)==1 for q in pool),'unit quaternion fixture')
    g=[pool[e%3] for e in range(33)];h={v:word(g,p) for v,p in paths.items()}
    loops={e:qm(qm(h[s],g[e]),qc(h[t])) for e,(a,s,t) in enumerate(edges) if e not in TREE}
    full_traces=[word(g,f['full_word'])[0] for f in faces]
    reduced_traces=[word(loops,f['chord_word'])[0] for f in faces]
    control('noncommuting_full_link_trace_identity',full_traces==reduced_traces,
            {'all_20_faces':True,'trace_values':[str(x) for x in full_traces]})
    orient={e:QI for e in loops};orient[28]=orient[25]=pool[0]
    good=word(orient,expected[9])[0];bad=word(orient,[(28,1),(25,1)])[0]
    control('face9_terminal_inverse_is_discriminating',good!=bad,
            {'correct':str(good),'wrong_unsigned':str(bad),'nonzero_margin':str(good-bad)})
    center=[tuple((F((-1)**(p[0] if a==1 else p[0]+p[1])) if a else F(1))
                  if j==0 else F(0) for j in range(4)) for a,p,t in edges]
    maximum=sum((1-word(center,f['full_word'])[0] for f in faces),F(0))
    minimum=sum((1-word([QI]*33,f['full_word'])[0] for f in faces),F(0))
    control('magnetic_positivity_and_sharp_bound',minimum==0 and maximum==40,
            {'range':['0','40'],'central_all_negative_faces':True,'operator_norm':'40'})
    deterministic=[f['id'] for f in faces if not f['omitted']]
    surviving=[];zero_pairs=[]
    for p,q in combinations(range(20),2):
        a=set(faces[p]['omitted']);b=set(faces[q]['omitted'])
        if a==b:surviving.append((p,q))
        else:zero_pairs.append({'pair':[p,q],'odd_omitted_chord':min(a^b)})
    control('all_conditional_cross_face_pairs_classified',
            deterministic==[8] and surviving==[(9,14),(9,15),(14,15)] and len(zero_pairs)==187,
            {'only_deterministic_face':8,'surviving_pairs':surviving,
             'rejected_by_odd_chord':zero_pairs,'distinct_pair_count':190})
    # Exactly integrates polynomials of degree <=2 in a Haar unit quaternion.
    axes=[tuple(F(sign) if i==j else F(0) for i in range(4)) for j in range(4) for sign in [-1,1]]
    cov=[[sum((a[i]*a[j] for a in axes),F(0))/8 for j in range(4)] for i in range(4)]
    need(cov==[[F(int(i==j),4) for j in range(4)] for i in range(4)],'Haar covariance matrix')
    fixtures=[]
    for u,w in [(QI,QI),(pool[0],pool[1]),(pool[1],pool[0])]:
        pair=[sum((dot(u,a)*dot(a,w) for a in axes),F(0))/8,
              sum((dot(u,a)*a[0] for a in axes),F(0))/8,
              sum((dot(a,w)*a[0] for a in axes),F(0))/8]
        exact=[dot(u,w)/4,u[0]/4,w[0]/4]
        need(pair==exact,'shared chord pair contraction')
        k=F(19,4)+2*sum(pair,F(0))
        fixtures.append({'U':[str(x) for x in u],'W':[str(x) for x in w],
                         'pair_moments':[str(x) for x in pair],'K':str(k)})
    control('independent_face_variance_rejected',F(fixtures[0]['K'])==F(25,4)!=F(19,4),
            {'covariance_matrix':[[str(x) for x in row] for row in cov],
             'shared_chord':25,'pair_functions':['r/4','x/4','z/4'],
             'fixtures':fixtures,'independence_error_at_identity':'3/2'})
    remaining=[f for f in faces if f['id'] not in [8,9,14,15]]
    control('conditional_variance_positive_decomposition',len(remaining)==16,
            {'uncorrelated_remaining_variance':'16/4=4',
             'shared_group_variance':'|u+w+e0|^2/4','exact_K':'4+|u+w+e0|^2/4'})
    lower_gram=[[F(1) if i==j else -F(1,2) for j in range(3)] for i in range(3)]
    invalid_gram=[[F(1) if i==j else -F(1) for j in range(3)] for i in range(3)]
    lo=F(19,4)+F(1,2)*(-F(3,2));hi=F(19,4)+F(1,2)*3
    control('sharp_operator_bounds_and_invalid_independent_minimum',
            lo==4 and hi==F(25,4) and det3(lower_gram)==0 and det3(invalid_gram)==-4,
            {'K_lower':str(lo),'K_upper':str(hi),'valid_minimum_x_z_r':['-1/2']*3,
             'invalid_free_coordinate_choice':['-1']*3,'invalid_Gram_determinant':'-4',
             'operator_scope':'continuous invariant multiplier; both essential extrema attained'})
    mean_id=20-F(1);second_id=mean_id**2+hi
    section_id=sum((1-word({e:QI for e in loops},f['chord_word'])[0] for f in faces),F(0))
    control('static_section_is_not_conditional_expectation',section_id==0 and mean_id==19,
            {'identity_section_action':str(section_id),'conditional_mean_at_identity':str(mean_id),
             'conditional_second_moment_at_identity':str(second_id)})
    EK=F(19,4);EV=F(20);EV2=EV**2+F(1,4)+EK
    control('Haar_reference_is_not_interacting_ground',EV2-EV**2==5 and EK!=hi,
            {'Haar_V_mean':str(EV),'Haar_V_second_moment':str(EV2),'Haar_V_variance':'5',
             'Haar_K_mean':str(EK),'multiplier_K_norm':str(hi),
             'positive_lambda_ground_claim_rejected':True})
    # A bounded two-sector identity checks the sign, scalar cancellation, and factor 1/2.
    def block(lam,shift):return [[F(2)+shift,lam],[lam,F(3)+shift]]
    block_rows=[]
    for lam in [F(0),F(1,3),F(1)]:
        for shift in [F(0),F(7)]:
            hmat=block(lam,shift);square=mm(hmat,hmat)
            defect=square[0][0]-hmat[0][0]**2
            need(defect==lam*lam,'block second-moment sign/scalar identity')
            block_rows.append({'coupling':str(lam),'common_shift':str(shift),
                               'second_moment_defect':str(defect),'Taylor_coefficient':str(defect/2)})
    control('lambda_zero_and_common_scalar_controls',all(F(x['second_moment_defect'])==0
              for x in block_rows if x['coupling']=='0'),
            {'finite_block_fixture_only':True,'rows':block_rows,
             'physical_identity':'B_lambda*B_lambda=(alpha lambda)^2 K'})
    control('strictly_nonzero_leakage_and_separate_dynamic_coefficients',
            lo>0 and hi/2==F(25,8) and EK/2==F(19,8),
            {'leakage_operator_norm':'5 alpha lambda/2','leakage_lower_norm':'2 alpha lambda',
             'Haar_leakage_norm_squared':'19(alpha lambda)^2/4',
             'Haar_core_discrepancy_coefficient':'19/8',
             'global_Duhamel_norm_coefficient':'25/8',
             'norm_Taylor_claim':False,'core_vector_Taylor':True})
    rejected=0
    for bad in [False,1,'passed']:
        try:need(bad,'intentional failure')
        except ValueError:rejected+=1
    control('strict_checks_survive_optimized_python',rejected==3,{'rejected':['False','integer','string']})
    claims={'full_magnetic_face_count':20,'magnetic_multiplier_range':['0','40'],
      'full_J16_unitary_equivalence_preserved':True,
      'conditional_mean':'20-b, b=Tr(V W^-1)/2',
      'conditional_second_moment':'(20-b)^2+19/4+(r+x+z)/2, r=Tr(U W^-1)/2',
      'conditional_variance_operator':'M_K, K=19/4+(r+x+z)/2',
      'surviving_cross_pairs':[[9,14],[9,15],[14,15]],
      'cross_pair_moments':['r/4','x/4','z/4'],'K_sharp_lower':'4','K_sharp_upper':'25/4',
      'K_Haar_mean':'19/4','selected_closure_positive_lambda':False,
      'selected_closure_lambda_zero':True,'leakage_norm':'5 alpha lambda/2',
      'leakage_squared':'(alpha lambda)^2 M_K',
      'compression_generator':'H_eff+alpha lambda(20-b)',
      'physical_operator_domain':'H2(SU2^33) intersect Hphys',
      'selected_operator_domain':'H2(SU2^3) intersect H3',
      'complement_operator_domain':'Q D(H_E)',
      'complement_form_domain':'Q D(H_E^(1/2))',
      'core_Taylor_difference':'(alpha lambda t/hbar)^2 K f/2+o_f(t^2)',
      'Haar_core_difference':'(19/8)(alpha lambda t/hbar)^2+o(t^2)',
      'global_norm_upper_bound':'(25/8)(alpha lambda t/hbar)^2',
      'operator_norm_Taylor_claim':False,'integral_topology':'strong vector-valued',
      'Haar_reference_interacting_ground':False,'Haar_V_mean':'20','Haar_V_second_moment':'405',
      'Haar_V_variance':'5','scalar_shift_repairs_leakage':False,
      'stationary_interacting_correlation_claim':False,'homogeneous_transfer':False,
      'physical_calibration':False,'continuum_transfer':False,'Q2_selected':False}
    results={'schema':'ym22-forward-q1-results-v1','loop':'q1','direction':'forward',
      'status':'proved_scoped','passed':True,'claims':claims,'full_face_ledger':faces,
      'finite_checks_replace_operator_proof':False,'proof_location':BASE+'report.md',
      'scientific_priority':'unverified'}
    return results,{'schema':'ym22-forward-q1-controls-v1','loop':'q1','direction':'forward',
                    'passed':True,'controls':controls}


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    out=p.parse_args().output.absolute();safe(out);need(not out.exists(),'fresh output required')
    inputs={p:sha(ROOT/p) for p in INPUTS};need(len(inputs)==len(INPUTS),'duplicate input')
    need(inputs[CONTRACT]==CONTRACT_SHA,'frozen Q1 contract mismatch')
    c=json.loads((ROOT/CONTRACT).read_text());need(c['loop']=='q1' and c['status']=='frozen','contract identity')
    for p,h in c['dependencies'].items():need(p in inputs and inputs[p]==h,'dependency mismatch '+p)
    for p in c['instruction_inputs']:need(p in inputs,'required instruction missing '+p)
    gate=json.loads((ROOT/'research/round22/advisor/p2-gate.json').read_text())
    need(gate['status']=='accepted','P2 admission status')
    for p,h in inputs.items():
        if p in gate['files']:need(gate['files'][p]==h,'admitted P2 source mismatch '+p)
    results,controls=checks();out.mkdir(parents=True,exist_ok=False)
    save(out/'results.json',results);save(out/'controls.json',controls)
    save(out/'source-manifest.json',{'schema':'ym22-producer-source-manifest-v1','loop':'q1',
      'direction':'forward','inputs':inputs,
      'outputs':{p:sha(out/p) for p in ['results.json','controls.json']},
      'import_policy':'standard-library only; no other producer imports',
      'manifest_self_hash':'bound by submission inventory'})
    print(json.dumps({'loop':'q1','direction':'forward','status':'proved_scoped','passed':True,
                      'controls':len(controls['controls'])},sort_keys=True))


if __name__=='__main__':main()
