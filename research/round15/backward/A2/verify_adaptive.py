"""Independent replay of every source-bound failed-cell bisection transition."""
from fractions import Fraction as Q
from pathlib import Path
import copy
import hashlib
import importlib.util
import json
import shutil
import sys
import tempfile

HERE=Path(__file__).resolve().parent
A1=HERE.parent/'A1'
PIN='e9719af63663b3456b43c5c8c4d07ec6bfcc8d5c619bcff1bd5b80e2a18374aa'
if hashlib.sha256((A1/'verify_cover.py').read_bytes()).hexdigest()!=PIN:
    raise ValueError('accepted A1 independent evaluator changed')
spec=importlib.util.spec_from_file_location('ym15_A1_replay',A1/'verify_cover.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
SOURCE_BYTES=Path(__file__).read_bytes()
A1_SOURCE='c0850838befc29a730f40e1fc3cffa32dd316264ab7fce191fc5eebf747a7f9a'
A1_EVIDENCE='b27eb6f20363912422e3febe0500ec1aef2e2b64f9ba21b3663652f8d3d4ac2a'


class Review:
    def __init__(self,forward_root):
        self.root=Path(forward_root)
        self.cover=old.Review(self.root/'A1')
        self.paths={'adaptive':self.root/'A2/refine.py','A1_evidence':self.root/'A1/output/cover.json',
                    'self':Path(__file__)}
        self.snapshot={name:old.Review.read(path) for name,path in self.paths.items()}
        self.hashes={name:hashlib.sha256(data).hexdigest() for name,data in self.snapshot.items()}
        if self.hashes['A1_evidence']!=A1_EVIDENCE or self.cover.hashes['cover.py']!=A1_SOURCE:
            raise ValueError('A1 starting evidence changed')
        if self.snapshot['self']!=SOURCE_BYTES:
            raise ValueError('independent adaptive source changed')
        self.initial=json.loads(self.snapshot['A1_evidence'])
        self.cover.verify(self.initial)

    def unchanged(self):
        self.cover.unchanged()
        if any(old.Review.read(path)!=self.snapshot[name] for name,path in self.paths.items()):
            raise ValueError('adaptive required input changed')

    def verify(self,record):
        self.unchanged()
        if type(record) is not dict:
            raise ValueError('adaptive object required')
        cap=record.get('max_iterations');maxcells=record.get('max_cells')
        if type(cap) is not int or not 0<=cap<=16 or type(maxcells) is not int or not 8<=maxcells<=4096:
            raise ValueError('strict bounded integer caps required')
        levels=record.get('levels');transitions=record.get('transitions')
        if type(levels) is not list or not levels or type(transitions) is not list:
            raise ValueError('nonempty levels and transitions required')
        if len(levels)!=len(transitions)+1 or len(transitions)>cap:
            raise ValueError('level/transition/iteration counts inconsistent')
        if not old.same(levels[0],self.initial):
            raise ValueError('initial level is not the accepted A1 evidence')
        expected_transitions=[]
        for level in levels:
            self.cover.verify(level)
            if level['degree']!=24:
                raise ValueError('point degree changed')
        for step,(before,after) in enumerate(zip(levels,levels[1:])):
            failed=[i for i,c in enumerate(before['cells']) if Q(c['transported_lower'])<=0]
            if not failed:
                raise ValueError('cannot refine after positive cover stop')
            if before['cell_count']+len(failed)>maxcells:
                raise ValueError('transition exceeds cell cap')
            expected_edges=[Q(before['cells'][0]['left'])]
            for index,cell in enumerate(before['cells']):
                if index in failed:
                    expected_edges.append((Q(cell['left'])+Q(cell['right']))/2)
                expected_edges.append(Q(cell['right']))
            actual_edges=[Q(after['cells'][0]['left'])]+[Q(c['right']) for c in after['cells']]
            if actual_edges!=expected_edges:
                raise ValueError('transition does not bisect exactly failed cells')
            expected_transitions.append({'from_level':step,'bisected_indices':failed,
               'previous_cell_count':before['cell_count'],'new_cell_count':after['cell_count']})
        last=levels[-1]
        if last['status']=='certified-positive-cover':
            stop='positive-cover'
        elif len(transitions)==cap:
            stop='iteration-cap'
        elif last['cell_count']+len(last['insufficient_indices'])>maxcells:
            stop='cell-cap'
        else:
            raise ValueError('unjustified premature adaptive stop')
        expected={'schema':'ym15-adaptive-cover-v1','source_sha256':self.hashes['adaptive'],
          'a1_source_sha256':A1_SOURCE,'a1_evidence_sha256':A1_EVIDENCE,
          'policy':'bisect only cells with nonpositive exact transported lower',
          'max_iterations':cap,'max_cells':maxcells,'levels':levels,'transitions':expected_transitions,
          'stop_reason':stop,'completed_refinements':len(expected_transitions),
          'total_evaluated_cells':sum(v['cell_count'] for v in levels),
          'status':last['status'],'final_cell_count':last['cell_count'],
          'final_minimum_lower':last['minimum_lower']}
        if not old.same(record,expected):
            raise ValueError('adaptive source, policy, transition or final status mismatch')
        self.unchanged()
        return {'status':last['status'],'cells':last['cell_count'],'minimum_lower':last['minimum_lower'],
          'stop_reason':stop,'refinements':len(transitions),
          'counts':[v['cell_count'] for v in levels],
          'failed_counts':[len(v['insufficient_indices']) for v in levels]}


def audit(forward_root,output_dir):
    root=Path(forward_root);review=Review(root);checks=[]
    def gate(name,test=True):
        if not test:raise ValueError(name)
        checks.append({'name':name,'passed':True})
    records={name:json.loads((root/'A2/output'/name).read_bytes()) for name in ('refinement.json','cap0.json','cap1.json','cell_cap.json')}
    outcomes={}
    for name,record in records.items():
        outcomes[name]=review.verify(record);gate('independently replayed '+name)
    result=outcomes['refinement.json'];good=records['refinement.json']
    gate('original target fully positive',result['status']=='certified-positive-cover' and Q(result['minimum_lower'])>0)
    gate('actual predicted transition8 to16 to21',result['counts']==[8,16,21] and result['failed_counts']==[8,5,0])
    gate('both iteration caps retain insufficiency',all(outcomes[n]['status']=='insufficient-cover' and outcomes[n]['stop_reason']=='iteration-cap' for n in ('cap0.json','cap1.json')))
    gate('cell cap retains insufficiency',outcomes['cell_cap.json']['status']=='insufficient-cover' and outcomes['cell_cap.json']['stop_reason']=='cell-cap')
    prediction=json.loads((HERE/'prediction.json').read_bytes())
    gate('independent pre-replay prediction agrees exactly',
         [s['minimum_lower'] for s in prediction['stages']]==[s['minimum_lower'] for s in good['levels']])
    def reject(name,mutation):
        try:review.verify(mutation)
        except ValueError:gate(name);return
        raise ValueError('accepted mutation '+name)
    for field,value in [('schema','bad'),('source_sha256','0'*64),('a1_source_sha256','0'*64),
       ('a1_evidence_sha256','0'*64),('policy','bisect arbitrary cells'),('max_iterations',True),
       ('max_cells',True),('completed_refinements',0),('total_evaluated_cells',0),
       ('stop_reason','iteration-cap'),('status','insufficient-cover'),('final_cell_count',22),
       ('final_minimum_lower','1'),('max_iterations',1),('max_cells',20)]:
        mutation=copy.deepcopy(good);mutation[field]=value;reject('metadata '+field+' '+str(value),mutation)
    for field,value in [('from_level',False),('bisected_indices',[0]),('previous_cell_count',True),('new_cell_count',0)]:
        mutation=copy.deepcopy(good);mutation['transitions'][0][field]=value;reject('transition mutation '+field,mutation)
    mutation=copy.deepcopy(good);mutation['levels'][1]['cells'][0]['certificate']['parameters']['eta']='1/8';reject('changed intermediate point action',mutation)
    mutation=copy.deepcopy(good);mutation['levels']=[good['levels'][0],good['levels'][2]];mutation['transitions']=good['transitions'][:1];reject('skipped required intermediate failed-cell stage',mutation)
    mutation=copy.deepcopy(good);mutation['levels'][2]['cells'].pop();mutation['levels'][2]['cell_count']-=1;reject('missing final endpoint cell',mutation)
    mutation=copy.deepcopy(good);mutation['levels'][2]['lipschitz']='1';reject('weakened final transport theorem',mutation)
    mutation=copy.deepcopy(good);mutation['levels']=[];mutation['transitions']=[];reject('empty adaptive evidence',mutation)
    mutation=copy.deepcopy(records['cap1.json']);mutation['status']='certified-positive-cover';mutation['stop_reason']='positive-cover';reject('capped insufficiency forged positive',mutation)
    mutation=copy.deepcopy(good);mutation['extra']='uniform Hamiltonian gap';reject('extra physical claim',mutation)
    for filename in ('A2/refine.py','A1/output/cover.json'):
        with tempfile.TemporaryDirectory() as temp:
            target=Path(temp)/'forward';shutil.copytree(root/'A1',target/'A1');shutil.copytree(root/'A2',target/'A2')
            local=Review(target);local.verify(good);path=target/filename;path.write_bytes(path.read_bytes()+b'\n')
            try:local.verify(good)
            except ValueError:gate('warmed source mutation '+filename)
            else:raise ValueError('changed source accepted')
    review.unchanged();gate('source bytes unchanged at completion')
    output={'schema':'ym15-A2-independent-review-v1','status':'passed','checks_count':len(checks),
       'checks':checks,'result':result,'capped_outcomes':outcomes,'source_sha256':hashlib.sha256(SOURCE_BYTES).hexdigest(),
       'reviewed_inputs':review.hashes,'accepted_A1_independent_source':PIN,
       'scientific_claim':'C(eta)>0 throughout the complete closed eta interval[1/8,1/4] at k1=k2=1 in the fixed finite Euclidean measure.',
       'limits':['Exact rational point-plus-transport certificate; no physical time or continuum claim.',
                 'Normal and optimized reruns are the same independent gates, not two separate reviews.']}
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=True);(out/'independent_review.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'status':'passed','checks':len(checks),'cells':result['cells'],
                      'minimum_lower_display':float(Q(result['minimum_lower']))}))
    return output


if __name__=='__main__':
    if len(sys.argv)!=3:raise SystemExit('usage: verify_adaptive.py FORWARD_ROOT OUTPUT_DIR')
    audit(*sys.argv[1:])
