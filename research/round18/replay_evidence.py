"""Independent scientific executions over the exact admitted byte snapshot."""
from pathlib import Path
import json,subprocess,sys
HERE=Path(__file__).resolve().parent
LOOPS=('a1','a2','b1','b2','c1','c2')
def main(output):
    reports={}
    for loop in LOOPS:
        target=HERE/('fresh-'+loop)
        proc=subprocess.run([sys.executable,str(HERE/'backward'/loop/'check.py'),'--output',str(target)],cwd=HERE,capture_output=True,text=True,timeout=180)
        if proc.returncode:raise ValueError('Independent '+loop+' failed: '+proc.stderr[-1800:])
        actual=json.loads((target/'results.json').read_bytes());expected=json.loads((HERE/'backward'/loop/'output/results.json').read_bytes())
        if actual.get('status')!='passed' or type(actual.get('checks_count')) is not int or actual['checks_count']<=0 or actual!=expected:
            raise ValueError('Independent semantic replay mismatch '+loop)
        comparison=HERE/('fresh-comparison-'+loop)
        proc=subprocess.run([sys.executable,str(HERE/'backward'/loop/'compare.py'),'--producer',str(HERE/'forward'/loop),'--evidence',str(HERE/'forward'/loop/'output'),'--output',str(comparison)],cwd=HERE,capture_output=True,text=True,timeout=180)
        if proc.returncode:raise ValueError('Independent producer comparison '+loop+' failed: '+proc.stderr[-1800:])
        checked=json.loads((comparison/'results.json').read_bytes());expected_comparison=json.loads((HERE/'backward'/loop/'comparison/results.json').read_bytes())
        if checked.get('status')!='passed' or type(checked.get('checks_count')) is not int or checked['checks_count']<=0 or checked!=expected_comparison:raise ValueError('Incomplete independent comparison '+loop)
        reports[loop]={'status':'passed','checks_count':actual['checks_count'],'comparison_checks_count':checked['checks_count']}
    result={'status':'passed','gates':[x+'_gate' for x in LOOPS],'independent':reports,'scope':'Six independently implemented exact finite computations plus their reviewed conventional arguments. Source hashes alone do not admit scientific premises.'}
    Path(output).write_text(json.dumps(result,indent=2)+'\n');return result
if __name__=='__main__':
    if len(sys.argv)!=2:raise SystemExit('usage: replay_evidence.py OUTPUT_JSON')
    main(sys.argv[1])
