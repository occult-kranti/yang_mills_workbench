"""Compare frozen forward JSON with the already derived independent A1 oracle."""
import argparse,hashlib,json
from pathlib import Path
from fractions import Fraction as F
from check import trial,haar_x_moment,build_graph,validate_graph


def main(source,evidence,output):
    source,evidence,output=map(Path,(source,evidence,output));output.mkdir(parents=True,exist_ok=False)
    digest=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();record=json.loads((evidence/'evidence.json').read_text());checks=[]
    def check(name,condition):
        if not condition:raise RuntimeError(name)
        checks.append({'name':name,'passed':True})
    check('forward evidence binds actual reviewed source',record['source_sha256']==digest(source/'projectors.py'))
    check('all declared Haar moments agree independently',record['moments']=={str(n):str(haar_x_moment(n)) for n in range(5)})
    check('complete sixteen projector sectors',len(record['occupancy'])==16 and {tuple(r['link_excitation_flags']) for r in record['occupancy']}=={tuple((mask>>i)&1 for i in range(4)) for mask in range(16)} and all(r['Qp']==int(any(r['link_excitation_flags'])) and r['sum_qe']==sum(r['link_excitation_flags']) for r in record['occupancy']))
    check('Casimir and vacuum labels agree',all(F(r['Casimir'])==F(r['j'])*(F(r['j'])+1) and r['q']==int(F(r['j'])>0) for r in record['casimir_checks']))
    expected_trials=[('1','1/2','0'),('1','0','0'),('1','0','1/8'),('1','1/2','1/4'),('1','1/2','-1/4'),('1','-1/2','1/4'),('2','-1/2','-1/8')]
    check('complete declared signed trial inventory',[(r['alpha'],r['lambda'],r['t']) for r in record['trials']]==expected_trials)
    for r in record['trials']:
        ours=trial(r['alpha'],r['lambda'],r['t']);absolute=None if ours['signed_ratio'] is None else str(abs(F(ours['signed_ratio'])))
        check('trial values '+str((r['alpha'],r['lambda'],r['t'])),r['norm_squared_before_normalization']==ours['norm_squared'] and r['free_energy']==ours['electric'] and r['magnetic_energy']==ours['magnetic'] and r['total_energy']==str(F(ours['electric'])+F(ours['magnetic'])) and r['absolute_relative_ratio']==absolute and F(r['vacuum_image_norm_squared'])==F(r['lambda'])**2/4)
    c=record['local_constants'];a,l=F(c['alpha']),F(c['lambda'])
    check('local operator norm constants',c['PXP']=='0' and c['QXP_norm']==c['offdiagonal_X_norm']=='1/2' and c['diagonal_X_norm_upper']=='1')
    check('physical versus unprojected local energies',F(c['full_link_free_gap'])==3*a/4 and F(c['fundamental_loop_energy'])==3*a)
    check('diagonal form coefficient retains physical units',F(c['diagonal_form_coefficient_against_sum_C'])==F(16,3)*abs(l) and F(c['diagonal_relative_coefficient_against_H0'])==F(16,3)*abs(l)/a)
    check('all three claimed relative constants falsified',len(record['relative_counterexamples'])==3 and all(F(r['actual_ratio'])==abs(F(trial(1,'1/2',r['trial_t'])['signed_ratio']))==2*F(r['claimed_bound']) for r in record['relative_counterexamples']))
    check('entire exact small-amplitude sequence',len(record['small_t_sequence'])==6 and all(F(r['t'])==F(1,2**r['k']) and r['free_energy']==trial(1,'1/2',r['t'])['electric'] and r['magnetic_energy']==trial(1,'1/2',r['t'])['magnetic'] and F(r['ratio'])==abs(F(trial(1,'1/2',r['t'])['signed_ratio'])) for r in record['small_t_sequence']))
    for r in record['graphs']:
        graph=build_graph(r['n']);edges,inc=validate_graph(graph);overlaps=[len(set().union(*(set(inc[e]) for e,_ in f['word']))) for f in graph['faces']]
        check('independent graph counts and overlaps n='+str(r['n']),r['vertices']==len(graph['vertices']) and r['edges']==len(edges) and r['plaquettes']==len(graph['faces']) and r['maximum_link_incidence']==max(map(len,inc.values())) and r['maximum_overlapping_plaquettes_including_self']==max(overlaps) and r['maximum_other_overlapping_plaquettes']==max(overlaps)-1)
    check('vertex-only contact is separate from edge overlap',[r['relation'] for r in record['support_relations']]==['shared-link','shared-vertex-only'] and [len(r['shared_links']) for r in record['support_relations']]==[1,0] and [len(r['shared_vertices']) for r in record['support_relations']]==[2,1])
    check('dense target remains explicitly open',record['dense_uniform_gap_status'].startswith('open;'))
    result={'schema':'ym17-independent-a1-comparison-v1','status':'passed','checks_count':len(checks),'checks':checks,'reviewed_input_sha256':{'producer/projectors.py':digest(source/'projectors.py'),'producer/check.py':digest(source/'check.py'),'producer/report.md':digest(source/'report.md'),'producer-output/evidence.json':digest(evidence/'evidence.json')},'discrepancies':[],'scope':'Read-only comparison after independent derivation; no forward source imported.'}
    (output/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'passed','checks_count':len(checks)}))


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--producer',required=True);p.add_argument('--evidence',required=True);p.add_argument('--output',required=True);a=p.parse_args();main(a.producer,a.evidence,a.output)
