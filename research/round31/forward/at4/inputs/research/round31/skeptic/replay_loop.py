#!/usr/bin/env python3
"""Source-bound all-output replay of current Round31 producer packages."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def safe_path(base, name):
    parsed=PurePosixPath(name)
    if parsed.is_absolute() or '..' in parsed.parts:
        raise RuntimeError('unsafe source path: '+name)
    cur=base
    for part in parsed.parts:
        cur=cur/part
        if cur.is_symlink():
            raise RuntimeError('symlink in source closure: '+str(cur))
    if not cur.is_file(): raise RuntimeError('missing source: '+name)
    return cur

def verify_freeze(src):
    freeze=json.loads((src/'freeze.json').read_text())
    if freeze.get('loop')!=src.name.upper() or freeze.get('direction')!=src.parent.name:
        raise RuntimeError('wrong freeze identity: '+str(src))
    sources=freeze.get('sources')
    if not isinstance(sources,dict) or not sources:
        raise RuntimeError('missing frozen file map')
    prefix=src.relative_to(ROOT).as_posix()+'/'
    if any(not name.startswith(prefix) for name in sources):
        raise RuntimeError('freeze source outside producer ownership')
    files={name[len(prefix):]:digest for name,digest in sources.items()}
    actual={str(p.relative_to(src)) for p in src.rglob('*') if p.is_file()
            and p!=src/'freeze.json'}
    if any('__pycache__' in n or n.endswith('.pyc') for n in actual):
        raise RuntimeError('interpreter artifact in source closure')
    if set(files)!=actual:
        raise RuntimeError('frozen closure mismatch: '+str(sorted(set(files)^actual)))
    for name,digest in files.items():
        if sha(safe_path(src,name))!=digest:
            raise RuntimeError('frozen digest mismatch: '+name)
    contract=src/'inputs/research/round31/contracts'/f'{src.name}.json'
    if not contract.is_file() or contract.read_bytes()!=(ROOT/'research/round31/contracts'/f'{src.name}.json').read_bytes():
        raise RuntimeError('missing or changed frozen contract snapshot')
    for required in ('check.py','report.md','output/results.json','inputs/AGENTS.md'):
        if required not in files: raise RuntimeError('required source absent: '+required)
    return freeze

def replay(loop):
    receipts=[]
    for direction in ('forward','reverse'):
        src=ROOT/'research/round31'/direction/loop
        verify_freeze(src)
        before=sha(src/'freeze.json')
        expected={str(p.relative_to(src/'output')):p.read_bytes()
                  for p in (src/'output').rglob('*') if p.is_file()}
        if not expected: raise RuntimeError('no expected outputs')
        for mode in ('normal','optimized'):
            with tempfile.TemporaryDirectory(prefix=f'hnm-r31-{loop}-{direction}-{mode}-') as temporary:
                out=Path(temporary)/'output'
                cmd=[sys.executable,'-B']+(['-O'] if mode=='optimized' else [])+[str(src/'check.py'),'--output',str(out)]
                result=subprocess.run(cmd,capture_output=True,text=True,check=True)
                actual={str(p.relative_to(out)):p.read_bytes() for p in out.rglob('*') if p.is_file()}
                if actual!=expected:
                    bad=sorted(n for n in set(actual)|set(expected) if actual.get(n)!=expected.get(n))
                    raise RuntimeError(f'{loop}/{direction}/{mode} changed outputs: {bad}')
                receipts.append({'direction':direction,'mode':mode,'command':cmd[:-1]+['<fresh-output>'],
                                 'outputs':{n:hashlib.sha256(b).hexdigest() for n,b in sorted(actual.items())},
                                 'stdout':result.stdout.strip().replace(str(out),'<fresh-output>')})
        verify_freeze(src)
        if sha(src/'freeze.json')!=before: raise RuntimeError('freeze changed during replay')
    return receipts

if __name__=='__main__':
    print(json.dumps(replay(sys.argv[1]),indent=2))
