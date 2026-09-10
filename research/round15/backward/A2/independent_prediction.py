"""Backward prediction from independent character integrals, before producer replay."""
from fractions import Fraction as Q
from pathlib import Path
import hashlib
import importlib.util
import json

BASE=Path(__file__).resolve().parent.parent/'A1'
PIN='e9719af63663b3456b43c5c8c4d07ec6bfcc8d5c619bcff1bd5b80e2a18374aa'
data=(BASE/'verify_cover.py').read_bytes()
if hashlib.sha256(data).hexdigest()!=PIN:
    raise ValueError('accepted A1 independent evaluator changed')
spec=importlib.util.spec_from_file_location('ym15_A1_independent',BASE/'verify_cover.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)


def predict():
    edges=[Q(1,8)+Q(i,64) for i in range(9)]
    stages=[]
    for iteration in range(9):
        cells=[];newedges=[edges[0]]
        for left,right in zip(edges,edges[1:]):
            center=(left+right)/2
            point=json.loads(old.point.exact_data(Q(1),Q(1),center,24))
            lower=Q(point['enclosures']['covariance'][0])-(right-left)
            cells.append({'left':str(left),'right':str(right),'lower':str(lower)})
            if lower<=0:newedges.append(center)
            newedges.append(right)
        failed=[i for i,c in enumerate(cells) if Q(c['lower'])<=0]
        stages.append({'iteration':iteration,'cell_count':len(cells),'failed':failed,
          'minimum_lower':min((c['lower'] for c in cells),key=Q),'cells':cells})
        if not failed:
            return {'status':'positive independent prediction','stages':stages}
        edges=newedges
    raise ValueError('prediction cap exhausted')


if __name__=='__main__':
    result=predict();out=Path(__file__).resolve().parent/'prediction.json'
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps([{'cells':s['cell_count'],'failed':len(s['failed']),
                      'minimum_lower_display':float(Q(s['minimum_lower']))} for s in result['stages']]))
