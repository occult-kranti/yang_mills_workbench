"""Regression checks for the skeptic's empty/stale prerequisite-evidence defect."""
import copy
import json
from pathlib import Path
from run_experiments import validate_deterministic_evidence

root = Path(__file__).resolve().parent
valid = json.loads((root/'results'/'deterministic_checks_current.json').read_text())
validate_deterministic_evidence(valid)
cases = {'empty_success':{'successful':True,'tests_run':0,'failures':0,'errors':0}}
for label, key, value in [('missing_test','test_names_run',valid['test_names_run'][:-1]),
                           ('stale_source','source_sha256',{}),
                           ('skipped_test','skipped',1),
                           ('failed_test','failures',1),
                           ('errored_test','errors',1),
                           ('false_success','successful',False)]:
    record = copy.deepcopy(valid)
    record[key] = value
    cases[label] = record
results = []
for label, record in cases.items():
    try:
        validate_deterministic_evidence(record)
    except RuntimeError as error:
        results.append({'case':label,'rejected':True,'reason':str(error)})
    else:
        raise AssertionError(f'invalid deterministic evidence accepted: {label}')
out = {'valid_current_evidence_accepted':True,'invalid_records_rejected':results,
       'stochastic_rerun':False,'source_sha256':valid['source_sha256']}
(root/'results'/'evidence_gate_repair.json').write_text(json.dumps(out,indent=2,allow_nan=False)+'\n')
print('Current source evidence accepted; seven empty/stale/skipped/failed evidence mutations rejected.')
