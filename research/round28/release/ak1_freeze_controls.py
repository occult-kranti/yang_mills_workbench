"""Read-only actual AK1 freeze namespace and full owned-coverage mutations."""
import argparse
import copy
import json
from pathlib import Path
import sys
sys.dont_write_bytecode=True
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from reproduce import Validator,PREFIX,require


def run(spec_name):
    validator=Validator();spec=validator.load(spec_name);contract=validator.contract('ak1')
    rejected=[]
    for side in ['forward','reverse']:
        base=PREFIX+side+'/ak1/';configuration=spec['producers'][side]
        result=validator.load(base+'output/results.json');original=validator.load(base+'freeze.json')
        closure,_,_=validator.manifests('ak1',side,configuration['source_manifests'],configuration['instruction_manifests'])
        gate_bindings={**closure,**result['bindings'],**original['files']}
        validator.producer('ak1',side,contract,configuration,gate_bindings)
        nested=base+('inputs-current-freeze.json' if side=='forward' else 'inputs/freeze.json')
        require(nested in original['files'],'owned input freeze missing from baseline')
        class AlteredFreeze(Validator):
            def load(self,name):
                return frozen if name==base+'freeze.json' else super().load(name)
        def attack(label,change_spec=None,change_freeze=None):
            nonlocal frozen
            frozen=copy.deepcopy(original);changed=copy.deepcopy(configuration)
            if change_spec:change_spec(changed)
            if change_freeze:change_freeze(frozen)
            try:AlteredFreeze().producer('ak1',side,contract,changed,gate_bindings)
            except ValueError:rejected.append(side+'/'+label)
            else:raise ValueError('invalid AK1 freeze accepted: '+side+'/'+label)
        def rename(record,old,new):record['files'][new]=record['files'].pop(old)
        frozen=None
        attack('wrong-producer-namespace',lambda c:c.update(freeze_path_base='producer'))
        attack('unknown-namespace',lambda c:c.update(freeze_path_base='repo'))
        attack('foreign-producer',change_freeze=lambda r:rename(r,base+'check.py',PREFIX+('reverse' if side=='forward' else 'forward')+'/ak1/check.py'))
        attack('escaping-member',change_freeze=lambda r:rename(r,base+'check.py',base+'inputs/../check.py'))
        attack('absolute-member',change_freeze=lambda r:rename(r,base+'check.py',str(validator.root/base/'check.py')))
        attack('missing-owned-input-freeze' if side=='forward' else 'missing-nested-input-freeze',change_freeze=lambda r:r['files'].pop(nested))
        attack('missing-owned-file',change_freeze=lambda r:r['files'].pop(base+'check.py'))
        attack('changed-owned-file-hash',change_freeze=lambda r:r['files'].__setitem__(base+'check.py','0'*64))
    return {'status':'passed','valid_actual_closures':2,'freeze_mutations_rejected':len(rejected),'controls':rejected,
            'producer_executions':0,'new_research_loops':0,'scope':'Actual frozen records read; mutations affect in-memory freeze/spec projections only.'}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--spec',default=PREFIX+'advisor/ak1-admission.json');args=parser.parse_args()
    print(json.dumps(run(args.spec),sort_keys=True))
