#!/usr/bin/env python3
"""Additional isolated source and collection-boundary review; no historical edits."""
from pathlib import Path
import copy
import contextlib
import hashlib
import io
import json
import sys
import tempfile


def main(collection_file, producer_file, output_dir):
    here=Path(__file__).resolve().parent
    source=(here/'verify_certificate.py').read_bytes()
    oracle=(here/'oracle.py').read_bytes()
    collection=json.loads(Path(collection_file).read_text())
    producer_sha=hashlib.sha256(Path(producer_file).read_bytes()).hexdigest()
    selected=next(e['certificate'] for e in collection['certificates']
                  if e['certificate']['parameters']=={'k1':'1','k2':'1','eta':'1/4'}
                  and e['certificate']['degree']==24)
    checks=[]
    def gate(name,condition):
        if not condition:raise ValueError(name)
        checks.append({'name':name,'passed':True})
    def reject(name,fn):
        try:fn()
        except ValueError:gate(name,True);return
        raise ValueError('accepted '+name)
    with tempfile.TemporaryDirectory(prefix='boundary-',dir=here) as directory:
        tmp=Path(directory);vpath=tmp/'verify_certificate.py';opath=tmp/'oracle.py'
        vpath.write_bytes(source);opath.write_bytes(oracle)
        ns={'__name__':'isolated_verifier_boundary','__file__':str(vpath)}
        exec(compile(source,str(vpath),'exec'),ns)
        gate('copied frozen source executes exact central replay',
             ns['verify'](selected,producer_source_sha256=producer_sha) is True)
        opath.write_bytes(oracle+b'\n# isolated mutation\n')
        reject('changed oracle bytes after cache warmup',lambda:ns['verify'](selected,producer_source_sha256=producer_sha))
        opath.write_bytes(oracle)
        vpath.write_bytes(source+b'\n# isolated mutation\n')
        reject('changed evaluator bytes after cache warmup',lambda:ns['verify'](selected,producer_source_sha256=producer_sha))
        vpath.write_bytes(source)
        gate('exact-data cache exposes immutable strings',type(ns['exact_data'](1,1,ns['Q'](1,4),24)) is str)
        for bad in (None,True,'x'*64,'0'*63,'A'*64):
            reject('invalid expected hash '+repr(bad),lambda bad=bad:ns['verify'](selected,producer_source_sha256=bad))
        cases=[]
        c=copy.deepcopy(collection);c['certificates']=[];cases.append(('empty collection',c))
        c=copy.deepcopy(collection);del c['status'];cases.append(('missing outer status',c))
        c=copy.deepcopy(collection);c['status']=True;cases.append(('Boolean outer status',c))
        c=copy.deepcopy(collection);c['additional']='hidden premise';cases.append(('extra outer field',c))
        c=copy.deepcopy(collection);c['producer_source_sha256']='0'*64;cases.append(('wrong collection source',c))
        c=copy.deepcopy(collection);c['certificates'].append(c['certificates'][0]);cases.append(('duplicate fixture ID',c))
        c=copy.deepcopy(collection);c['certificates'][0]['id']=True;cases.append(('Boolean fixture ID',c))
        c=copy.deepcopy(collection);c['certificates'][0]['extra']='hidden premise';cases.append(('extra fixture field',c))
        for name,c in cases:
            candidate=tmp/'mutant.json';candidate.write_text(json.dumps(c)+'\n')
            with contextlib.redirect_stdout(io.StringIO()):
                reject(name,lambda:ns['audit'](candidate,producer_file,tmp/'review'))
    result={'schema':'ym14-verifier-boundary-review-v1','status':'passed','phase':'loop2',
            'check_count':len(checks),'checks':checks,
            'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            'reviewed_source_hashes':{'backward/verify_certificate.py':hashlib.sha256(source).hexdigest(),
                                     'backward/oracle.py':hashlib.sha256(oracle).hexdigest(),
                                     'forward/loop2_certificate.py':producer_sha},
            'scope':'Exact evaluator source/cache and complete collection-envelope boundaries; no physics extension.'}
    out=Path(output_dir);out.mkdir(parents=True,exist_ok=True)
    (out/'verifier_boundary_review.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'passed','check_count':len(checks)}))


if __name__=='__main__':
    if len(sys.argv)!=4:raise SystemExit('usage: test_verifier_boundary.py COLLECTION PRODUCER OUTPUT')
    main(*sys.argv[1:])
