#!/usr/bin/env python3
"""Create a portable, byte-inventoried round13 research archive."""
from pathlib import Path
import hashlib
import json
import zipfile

HERE = Path(__file__).resolve().parent
DEST = HERE.parents[1] / 'dist/research-round13.zip'


def main():
    files = []
    for path in sorted(HERE.rglob('*')):
        if path.is_symlink():
            raise ValueError('Symlink research input rejected')
        if path.is_file() and '__pycache__' not in path.parts and path.suffix not in ('.pyc', '.zip'):
            files.append(path)
    hashes = {str(p.relative_to(HERE)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
    with zipfile.ZipFile(DEST, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            archive.write(path, 'yangmills-round13/' + str(path.relative_to(HERE)))
        archive.writestr('yangmills-round13/ARCHIVE-CONTENTS.json', json.dumps({'sha256': hashes}, indent=2) + '\n')
    with zipfile.ZipFile(DEST) as archive:
        for path, expected in hashes.items():
            if hashlib.sha256(archive.read('yangmills-round13/' + path)).hexdigest() != expected:
                raise ValueError('Archive bytes disagree with source')
    print(json.dumps({'files': len(files), 'bytes': DEST.stat().st_size, 'path': str(DEST)}))


if __name__ == '__main__':
    main()
