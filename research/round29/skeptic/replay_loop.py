#!/usr/bin/env python3
"""Replay reviewed frozen producer executables into skeptic-owned evidence."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def replay(loop):
 receipts=[]
 for direction in ('forward','reverse'):
  src=ROOT/'research/round29'/direction/loop
  expected=(src/'output/results.json').read_bytes()
  for mode in ('normal','optimized'):
   out=HERE/'replays'/loop/direction/mode
   if out.exists():shutil.rmtree(out)
   cmd=[sys.executable,'-B']+(['-O'] if mode=='optimized' else [])+[str(src/'check.py'),'--output',str(out)]
   result=subprocess.run(cmd,capture_output=True,text=True,check=True)
   actual=(out/'results.json').read_bytes()
   if actual!=expected:raise RuntimeError(f'{loop}/{direction}/{mode} result mismatch')
   receipts.append({'direction':direction,'mode':mode,'results_sha256':hashlib.sha256(actual).hexdigest(),'stdout':result.stdout.strip()})
 return receipts
if __name__=='__main__':print(json.dumps(replay(sys.argv[1]),indent=2))
