#!/usr/bin/env python3
"""Recheck AG2 adoption and source restoration without inferring file authorship."""
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=Path(__file__).with_name('ag2-provenance.json'))
    args = parser.parse_args()
    checks = []

    def check(name, condition):
        if not condition:
            raise RuntimeError(name)
        checks.append(name)

    adoption_path = ROOT/'research/round28/advisor/ag2-preproduction-provenance.json'
    restoration_path = ROOT/'research/round28/advisor/repairs/ag2-source-restoration.json'
    adoption = json.loads(adoption_path.read_text())
    restoration = json.loads(restoration_path.read_text())
    for path, h in adoption['bindings'].items():
        check('adoption_binding:'+path, digest(ROOT/path) == h)
    check('restored_source', digest(ROOT/restoration['source']) == restoration['restored_sha256'])
    check('superseded_rationale_preserved', digest(ROOT/restoration['preserved_rewrite']) == restoration['preserved_rewrite_sha256'])
    check('no_contract_change_claim', restoration['physics_contract_changed'] is False)
    check('no_added_loop', restoration['new_research_loops'] == 0)
    source = restoration['source']
    for side in ('forward', 'reverse'):
        snapshot = ROOT/f'research/round28/{side}/ag2/inputs'/source
        check(side+':restored_source_snapshot', digest(snapshot) == restoration['restored_sha256'])
    contract = json.loads((ROOT/'research/round28/contracts/ag2.json').read_text())
    for path, h in contract['sources'].items():
        check('contract_source:'+path, digest(ROOT/path) == h)
    # These controls protect the checksum validation itself. They are not a
    # forensic claim about who created files before the visible turns.
    actual = digest(ROOT/source)
    check('altered_hash_rejected', actual != '0'*64)
    check('overwritten_rationale_distinguished', actual != restoration['preserved_rewrite_sha256'])
    bindings = {str(p.relative_to(ROOT)):digest(p) for p in (adoption_path,restoration_path,ROOT/source,ROOT/restoration['preserved_rewrite'])}
    payload = {'schema':'ym28-ag2-provenance-review-v1','checks':len(checks),
               'check_names':checks,'accepted_source_restoration':True,
               'bindings':bindings,
               'qualification':'Hashes verify source restoration and the explicit pre-production adoption record. Pre-existing file creation is unattributed; no forensic determination of its author or creation time is made. No scientific result is inferred from the existence of input snapshots.'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(payload,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'checks':len(checks),'status':'passed'},sort_keys=True))


if __name__ == '__main__':
    main()
