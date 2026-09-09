#!/usr/bin/env python3
"""Build a relocatable GitHub project-site tree from recorded static assets."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import shutil

ROOT=Path(__file__).resolve().parents[1]

def build(base='/yang_mills_workbench/'):
    if not re.fullmatch(r'/[A-Za-z0-9_-]+/',base):
        raise ValueError('Base must be one absolute project-directory segment')
    source=ROOT/'dist'; destination=ROOT/'docs'
    destination.mkdir(exist_ok=True)
    assets={p.name:p for p in source.iterdir() if p.is_file() and not p.name.startswith('test_')}
    pattern=re.compile(r'(?P<quote>[\"\'])/(?P<asset>'+ '|'.join(re.escape(x) for x in sorted(assets,key=len,reverse=True))+r')(?=[\"\'])')
    for name,p in assets.items():
        data=p.read_bytes()
        if p.suffix in ('.js','.html','.css','.json'):
            text=data.decode()
            text=pattern.sub(lambda m:m['quote']+base+m['asset'],text)
            if name=='workbench-runtime.js':
                text=text.replace('staticOnly:false','staticOnly:true')
            data=text.encode()
        (destination/name).write_bytes(data)
    (destination/'.nojekyll').write_text('')
    allowed=set(assets)|{'.nojekyll','build-manifest.json'}
    for p in destination.iterdir():
        if p.is_file() and p.name not in allowed:p.unlink()
    manifest={'base':base,'source':'dist','static_only':True,'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(destination.iterdir()) if p.is_file() and p.name!='build-manifest.json'}}
    (destination/'build-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'status':'built','directory':str(destination),'assets':len(assets),'base':base}))
    return manifest

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--base',default='/yang_mills_workbench/')
    build(parser.parse_args().base)
