"""Run the reproducible round-5 gates and retain exact stdout/stderr and hashes."""
from pathlib import Path
import hashlib
import json
import platform
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def main():
    commands = [
        ['symbolic_checks.py'],
        ['counterexamples.py'],
        ['test_proof_search.py'],
        ['verify_proof_search_independent.py'],
        ['proof_search.py', 'search_fixture.json', '--output', 'search_results.json'],
        ['coefficient_certificate.py'],
    ]
    records = []
    for args in commands:
        proc = subprocess.run([sys.executable] + args, cwd=ROOT, text=True, capture_output=True)
        record = {'args': args, 'exit_code': proc.returncode,
                  'stdout': proc.stdout, 'stderr': proc.stderr,
                  'source_sha256': hashlib.sha256((ROOT/args[0]).read_bytes()).hexdigest()}
        if args[0]=='test_proof_search.py':
            match=re.search(r'Ran (\d+) tests?',proc.stderr)
            record['unit_test_count']=int(match.group(1)) if match else None
        records.append(record)
        print(f'{args[0]}: '+('PASS' if proc.returncode==0 else 'FAIL'),flush=True)
    result={'python':platform.python_version(),'platform':platform.platform(),
            'all_commands_passed':all(x['exit_code']==0 for x in records),'commands':records,
            'scope':'Exact identity/counterexample checks and finite-library proof-planning verification. No continuum QED, trajectory interval enclosure, or formal proof-assistant claim.'}
    (ROOT/'validation_run.json').write_text(json.dumps(result,indent=2)+'\n')
    return 0 if result['all_commands_passed'] else 1


if __name__=='__main__': raise SystemExit(main())
