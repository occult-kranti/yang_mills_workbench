#!/usr/bin/env python3
"""Execute the documented calculator examples and retain JSON plus a run log."""
import json
from pathlib import Path
import subprocess
import sys

HERE=Path(__file__).resolve().parent
EXAMPLES={
 'jacobi':['jacobi','--ratio','10','--alpha','1','--dimension','24','--refine'],
 'static':['static','--kappa','2','--moments','6'],
 'series':['series','--degree','7','--epsilon','1/100'],
 'window':['window','--q','999/1000','--eta','1/2','--ell','1','--beta','1/2','--gamma','1'],
 'gaussian':['filter','--kind','gaussian','--M','35/1664','--duration','4','--omega','0'],
 'triangle':['filter','--kind','triangle','--M','1/1000','--duration','3','--omega','1/10'],
 'wilson':['wilson','--z','1/1000000'],
 'heat':['heat','--cap','1/100','--eta','1/100','--sigma','13/5'],
 'heat-certificates':['heat-certificates'],
}


def main():
    (HERE/'output').mkdir(exist_ok=True)
    log=[]
    for name,args in EXAMPLES.items():
        outfile=HERE/'output'/(name+'.json')
        command=[sys.executable,str(HERE/'ym_calculators.py'),'--output',str(outfile),*args]
        run=subprocess.run(command,text=True,capture_output=True)
        if run.returncode:
            raise RuntimeError(name+': '+run.stderr)
        result=json.loads(outfile.read_text())
        if not result:raise ValueError('empty result: '+name)
        log.append({'example':name,'arguments':args,'output':'output/'+name+'.json','returncode':run.returncode})
    (HERE/'output/example-runs.json').write_text(json.dumps({'status':'passed','count':len(log),'examples':log},indent=2)+'\n')
    print(json.dumps({'status':'passed','example_count':len(log)}))


if __name__=='__main__':main()
