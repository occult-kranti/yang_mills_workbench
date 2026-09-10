"""Two targeted accepted-layout checks, separate from scientific gate counts."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys,tempfile


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--producer',type=Path,required=True);ap.add_argument('--evidence',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ns=ap.parse_args()
    own=Path(__file__).resolve().parent;out=ns.output.resolve()
    if out.is_relative_to(own):raise ValueError('output outside source required')
    with tempfile.TemporaryDirectory(prefix='ym18-c1-portable-') as td:
        base=Path(td);producer=base/'producer';shutil.copytree(ns.producer,producer,ignore=shutil.ignore_patterns('__pycache__','output','output-optimized','comparison','comparison-optimized'))
        shutil.copytree(ns.evidence,producer/'output')
        def run(src,evidence,dest):
            return subprocess.run([sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])+[str(own/'compare.py'),'--producer',str(src),'--evidence',str(evidence),'--output',str(dest)],capture_output=True,text=True)
        original,relocated=run(ns.producer,ns.evidence,base/'original'),run(producer,producer/'output',base/'relocated')
        if original.returncode or relocated.returncode or (base/'original/results.json').read_bytes()!=(base/'relocated/results.json').read_bytes():raise ValueError('accepted layout changed independent evidence')
        (producer/'undeclared.py').write_text('unexpected = True\n');bad=run(producer,producer/'output',base/'invalid')
        if bad.returncode==0 or 'complete frozen source inventory' not in bad.stderr:raise ValueError('undeclared source was not rejected at inventory')
    checks=[{'name':'accepted nested output layout replays byte-identical comparison','passed':True},{'name':'undeclared source remains rejected after output exclusions','passed':True}]
    result={'schema':'ym18-independent-c1-portability-v1','status':'passed','checks_count':2,'checks':checks,
      'reviewed_source_sha256':{n:hashlib.sha256((own/n).read_bytes()).hexdigest() for n in ('coordinates.py','compare.py','portability.py')}}
    out.mkdir(parents=True,exist_ok=True);(out/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'passed','checks_count':2}))


if __name__=='__main__':main()
