#!/usr/bin/env python3
"""Preserve large planner traces byte-for-byte without loading them in the UI."""
from pathlib import Path
import gzip
import hashlib
import json

HERE=Path(__file__).resolve().parent

def sha(data):return hashlib.sha256(data).hexdigest()

def safe(path):
    path=Path(path)
    if path.is_symlink() or not path.resolve().is_relative_to(HERE):
        raise ValueError('Unsafe trace path')
    return path

def record_bytes(path):
    path=safe(path);packed=safe(Path(str(path)+'.gz'))
    raw=path.read_bytes() if path.is_file() else None
    if packed.is_file():
        unpacked=gzip.decompress(packed.read_bytes())
        if raw is not None and raw!=unpacked:raise ValueError('Stale compressed trace')
        return unpacked
    if raw is None:raise FileNotFoundError(path)
    return raw

def read_json(path):return json.loads(record_bytes(path))

def verify_archives():
    records=json.loads((HERE/'trace-archives.json').read_text())['files']
    if not records:raise ValueError('Missing trace inventory')
    for rel,item in records.items():
        path=safe(HERE/rel);packed=safe(Path(str(path)+'.gz'))
        compressed=packed.read_bytes();raw=record_bytes(path)
        if sha(compressed)!=item['gzip_sha256'] or len(compressed)!=item['gzip_bytes'] or sha(raw)!=item['original_sha256'] or len(raw)!=item['original_bytes']:
            raise ValueError('Trace inventory mismatch: '+rel)
    return records

def main():
    inventory=HERE/'trace-archives.json'
    records=json.loads(inventory.read_text())['files'] if inventory.is_file() else {}
    # A fresh checkout has compressed-only historical traces. Preserve those
    # entries when a researcher regenerates just the current raw trace.
    for rel,item in records.items():
        packed=safe(Path(str(safe(HERE/rel))+'.gz'))
        compressed=packed.read_bytes();original=gzip.decompress(compressed)
        if sha(compressed)!=item['gzip_sha256'] or len(compressed)!=item['gzip_bytes'] or sha(original)!=item['original_sha256'] or len(original)!=item['original_bytes']:
            raise ValueError('Existing trace archive is invalid: '+rel)
    for path in sorted(HERE.rglob('proof_results.json')):
        path=safe(path);raw=path.read_bytes();packed=safe(Path(str(path)+'.gz'))
        compressed=gzip.compress(raw,compresslevel=9,mtime=0)
        if gzip.decompress(compressed)!=raw:raise ValueError('Trace round trip failed')
        packed.write_bytes(compressed)
        records[str(path.relative_to(HERE))]={'original_sha256':sha(raw),'original_bytes':len(raw),
            'gzip_sha256':sha(compressed),'gzip_bytes':len(compressed)}
    if not records:
        records=verify_archives()
    else:
        inventory.write_text(json.dumps({'format':'gzip; original JSON bytes unchanged','files':records},indent=2)+'\n')
        verify_archives()
    print(json.dumps({'trace_files':len(records),'original_bytes':sum(x['original_bytes'] for x in records.values()),
        'gzip_bytes':sum(x['gzip_bytes'] for x in records.values())}))

if __name__=='__main__':main()
