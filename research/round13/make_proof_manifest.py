#!/usr/bin/env python3
"""Explicitly record current bytes only after the scientific ledger matches.

This is an intentional packaging operation, never an automatic repair of a
failed replay. No existing acceptance records are rewritten.
"""
import argparse
import json
from pathlib import Path
import proof_routes as routes


def create(root):
    frozen = {name: routes.read_regular(root, name) for name in routes.EXPECTED}
    reviewed = routes.validate_ledger(frozen)
    routes.specifications(frozen, reviewed)
    if routes.digest(frozen['proof_search.py']) != routes.CORE_SHA256:
        raise routes.ContractError('Historical search core changed')
    if routes.digest(frozen['proof_routes.py']) != routes.EXECUTING_ADAPTER_SHA256:
        raise routes.ContractError('Copied adapter and executing adapter differ')
    path = Path(root) / 'proof_manifest.json'
    if path.is_symlink():
        raise routes.ContractError('Symlink manifest rejected')
    manifest = {'sha256': {name: routes.digest(frozen[name]) for name in sorted(frozen)}}
    path.write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({'status': 'manifest-written', 'inputs': len(frozen), 'note': 'Scientific acceptance unchanged; execute proof_routes.py to verify evidence.'}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=routes.HERE)
    create(parser.parse_args().root)
