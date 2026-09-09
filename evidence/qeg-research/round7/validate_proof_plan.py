#!/usr/bin/env python3
"""Check that the new evidence binding fails closed on changed references."""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys
import tempfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
spec=importlib.util.spec_from_file_location('r7_evidence_audit',ROOT/'round6/code/evidence_guard.py')
guard=importlib.util.module_from_spec(spec);sys.modules[spec.name]=guard;spec.loader.exec_module(guard)
manifest=json.loads((HERE/'proof_manifest.json').read_text())
checks=[]
for label,rel in [('changed equation contract','round7/variable_contract.md'),
                  ('changed planner implementation','round6/code/proof_search.py'),
                  ('changed inference library','round7/proof_library.json')]:
    modified=json.loads(json.dumps(manifest));modified['files'][rel]='0'*64
    with tempfile.TemporaryDirectory(dir=HERE) as tmp:
        p=Path(tmp)/'manifest.json';p.write_text(json.dumps(modified))
        try:
            guard.bound_plan(HERE/'proof_library.json',p,ROOT)
        except guard.EvidenceFailure as exc:
            checks.append({'name':label,'passed':True,'evidence':str(exc)})
        else:
            raise RuntimeError('Guard accepted '+label)
result=guard.bound_plan(HERE/'proof_library.json',HERE/'proof_manifest.json',ROOT)
if result['status']!='proved' or not result['evidence_guard']['passed']:
    raise RuntimeError('Untampered proof snapshot failed')
checks.append({'name':'unchanged snapshot succeeds','passed':True})
for key in ('missing_Maxwell_certificate','common_quantum_closure'):
    r=result['scenario_results'][key]
    if r['status']!='not_derivable' or r.get('certified_proof'):
        raise RuntimeError('Unproved branch was accepted: '+key)
    checks.append({'name':key+' is underivable without a certificate','passed':True})
out={'passed':True,'checks':checks,'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
     'scope':'Evidence binding and finite inference-library failure behavior; not mathematical kernel verification.'}
(HERE/'proof_validation.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'passed':True,'checks':len(checks)}))
