#!/usr/bin/env python3
"""Exercise the Round21 replay boundary with isolated I1 admission mutations."""
import argparse
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    args=p.parse_args()
    if args.output.exists():raise ValueError('fresh output required')
    spec=importlib.util.spec_from_file_location('replay_review',HERE.parent/'reproduce.py')
    if spec is None or spec.loader is None:raise ValueError('validator unavailable')
    v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
    accepted=v.gate('i1')
    original_gate=ROOT/'research/round21/advisor/i1-gate.json'
    rows=[]
    def rejects(name,call):
        try:call()
        except (ValueError,FileNotFoundError) as err:
            rows.append({'name':name,'rejected':True,'reason':str(err).split(': ')[0]})
        else:raise RuntimeError('mutation survived: '+name)
    with tempfile.TemporaryDirectory(prefix='ym21-replay-controls-') as temp:
        temp=Path(temp);clone=temp/'repo'
        for name in [*accepted['files'],'research/round21/advisor/i1-gate.json']:
            dest=clone/name;dest.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ROOT/name,dest)
        v.ROOT=clone;v.HERE=clone/'research/round21'
        v.gate('i1')
        gatefile=clone/'research/round21/advisor/i1-gate.json'
        before=gatefile.read_bytes()
        for label,edit in [
            ('missing_required_manifest',lambda d:d['files'].pop('research/round21/forward/i1/output/source-manifest.json')),
            ('missing_actual_scientific_input',lambda d:d['files'].pop('research/round21/reverse/i1/source-dictionary.json')),
            ('missing_auxiliary_output',lambda d:d['files'].pop('research/round21/forward/i1/output/controls.json')),
            ('tampered_expected_result_hash',lambda d:d['files'].update({'research/round21/forward/i1/output/results.json':'0'*64})),
            ('missing_reviewed_comparison',lambda d:d['files'].pop('research/round21/advisor/i1-comparison.json')),
        ]:
            d=deepcopy(accepted);edit(d);gatefile.write_text(json.dumps(d))
            rejects(label,lambda:v.gate('i1'));gatefile.write_bytes(before)
        # Directory aliases preserve all final-file bytes, distinguishing a real
        # parent-symlink check from merely testing Path.is_symlink() on the leaf.
        for relative in ['research/round21/reverse/i1','research/round21/reverse',
                         'research/round21/advisor','research/round21']:
            directory=clone/relative
            moved=temp/('moved-'+relative.replace('/','-'))
            directory.rename(moved);directory.symlink_to(moved,target_is_directory=True)
            rejects('parent_symlink:'+relative,lambda:v.gate('i1'))
            directory.unlink();moved.rename(directory)
        gatefile.unlink();gatefile.symlink_to(original_gate)
        rejects('byte_identical_gate_symlink',lambda:v.gate('i1'))
        gatefile.unlink();gatefile.write_bytes(before)
        for token in ('../i1','i1/../../i1',True):
            rejects('invalid_loop:'+str(token),lambda token=token:v.gate(token))
        fresh=temp/'fresh-forward'
        shutil.copytree(clone/'research/round21/forward/i1/output',fresh)
        v.fresh_outputs('i1','forward',fresh,accepted)
        changed=fresh/'results.json';saved=changed.read_bytes()
        d=json.loads(saved);d['comparison']['omitted_anchor_face_count']=20
        changed.write_text(json.dumps(d))
        rejects('wrong_equation_with_preserved_success_status',lambda:v.fresh_outputs('i1','forward',fresh,accepted))
        changed.write_bytes(saved)
        changed=fresh/'controls.json';saved=changed.read_bytes()
        changed.write_text('{}')
        rejects('missing_auxiliary_control_content',lambda:v.fresh_outputs('i1','forward',fresh,accepted))
        changed.write_bytes(saved)
        comparison=temp/'comparison.json'
        shutil.copyfile(clone/'research/round21/advisor/i1-comparison.json',comparison)
        v.fresh_comparison('i1',comparison,accepted)
        d=json.loads(comparison.read_text());d['mutation_controls']=[]
        comparison.write_text(json.dumps(d))
        rejects('forged_accepted_comparison_without_controls',lambda:v.fresh_comparison('i1',comparison,accepted))
        v.gate('i1')
    report={'schema':'ym21-replay-admission-controls-v1','status':'completed',
            'validator_sha256':hashlib.sha256((HERE.parent/'reproduce.py').read_bytes()).hexdigest(),
            'reviewed_i1_gate_sha256':hashlib.sha256(original_gate.read_bytes()).hexdigest(),
            'controls':rows,'rejected_count':len(rows),'historical_mutations':0,
            'research_loops_added':0}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'completed','rejected_controls':len(rows)}))


if __name__=='__main__':main()
