#!/usr/bin/env python3
"""Package reviewed manuscript sources and reproducibility artifacts."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parent
EXCLUDED_AUDIT_DIRS = {
    'skeptic-output-normal', 'skeptic-output-middle',
    'skeptic-output-document',
}

def main():
    files = []
    for name in ['main.tex', 'main.bbl', 'README.md', 'calculators.html',
                 'build_appendices.py', 'build_contribution_appendix.py',
                 'audit_document.py', 'build_bundle.py']:
        p = ROOT / name
        if not p.is_file():
            raise FileNotFoundError(p)
        files.append(p)
    for directory in ['sections', 'sources', 'figures', 'calculators', 'audit']:
        for p in (ROOT / directory).rglob('*'):
            if not p.is_file() or '__pycache__' in p.parts or p.suffix == '.pyc':
                continue
            if directory == 'audit' and any(x in p.parts for x in EXCLUDED_AUDIT_DIRS):
                continue
            files.append(p)
    manifest = {
        'scope': 'Exact bundled source bytes; mathematical disposition is in audit/skeptic-review.json',
        'files': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in sorted(files)}
    }
    target = ROOT / 'output/yang_mills_reproducibility_bundle.zip'
    target.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED) as z:
        for p in sorted(files):
            z.write(p, str(p.relative_to(ROOT)))
        z.writestr('MANIFEST.sha256.json', json.dumps(manifest, indent=2) + '\n')
    with zipfile.ZipFile(target) as z:
        if z.testzip() is not None:
            raise ValueError('Archive integrity failure')
        for name, expected in manifest['files'].items():
            if hashlib.sha256(z.read(name)).hexdigest() != expected:
                raise ValueError('Archived hash mismatch: ' + name)
    print(json.dumps({'path': str(target), 'files': len(files) + 1,
                      'bytes': target.stat().st_size,
                      'sha256': hashlib.sha256(target.read_bytes()).hexdigest()}))

if __name__ == '__main__':
    main()
