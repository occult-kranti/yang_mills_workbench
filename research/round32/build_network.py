#!/usr/bin/env python3
"""Add reviewed Round32 nodes without rewriting inherited evidence nodes."""
import argparse
import copy
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROUND = ROOT / 'research/round32'


def build():
    inherited = json.loads((ROOT / 'research/round31/network.json').read_text())
    network = copy.deepcopy(inherited)
    findings = json.loads((ROUND / 'advisor/findings.json').read_text())
    if findings.get('completed') != 10 or len(findings.get('loops', [])) != 10:
        raise ValueError('Exactly ten reviewed investigations required')
    nodes, edges = network['nodes'], network['edges']
    known = {row['id'] for row in nodes}
    previous = 'r31-at6'
    for row in findings['loops']:
        lid = row['id'].lower()
        path = ROOT / row['gate_path']
        gate = json.loads(path.read_text())
        if gate['accepted'] != row['accepted'] or not gate.get('bindings'):
            raise ValueError('Unreviewed or changed finding: ' + lid)
        for name, expected in gate['bindings'].items():
            p = ROOT / name
            if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest() != expected:
                raise ValueError('Changed gate input: ' + name)
        nid = 'r32-' + lid
        if nid in known:
            raise ValueError('Duplicate node: ' + nid)
        nodes.append({'id': nid, 'title': row['title'], 'kind': 'result',
                      'status': gate['verdict'], 'summary': gate['accepted'],
                      'detail': '; '.join(gate['limitations']),
                      'model': row['model'], 'sources': [row['gate_path'], gate['reviewer_path']],
                      'route': 'round32-' + lid, 'hnm_alias': row['contribution_id'],
                      'subround': row['subround']})
        known.add(nid)
        edges.append({'from': previous, 'to': nid, 'type': 'review-selection',
                      'label': 'Selected after preceding review'})
        for dependency in row.get('dependencies', []):
            if dependency not in known:
                raise ValueError('Missing dependency: ' + dependency)
            edges.append({'from': dependency, 'to': nid, 'type': 'proven-dependency',
                          'label': 'Scoped mathematical premise'})
        previous = nid
    roadmap = json.loads((ROUND / 'advisor/roadmap.json').read_text())
    for goal in roadmap['goals']:
        nid = 'r32-next-' + goal['id'].lower()
        nodes.append({'id': nid, 'title': goal['title'], 'kind': 'planned',
                      'status': 'planned_not_executed', 'summary': goal['target'],
                      'detail': goal['missing_premise'], 'sources': ['research/round32/advisor/roadmap.json'],
                      'route': 'round32-roadmap'})
        edges.append({'from': previous, 'to': nid, 'type': 'proposed-transfer',
                      'label': 'Planned only; not an admitted implication'})
    ids = [row['id'] for row in nodes]
    if len(ids) != len(set(ids)):
        raise ValueError('Duplicate graph node')
    for edge in edges:
        source = edge.get('source', edge.get('from'))
        target = edge.get('target', edge.get('to'))
        if source not in ids or target not in ids:
            raise ValueError('Dangling graph edge')
    if nodes[:len(inherited['nodes'])] != inherited['nodes']:
        raise ValueError('Historical nodes were changed')
    network.update(current_round=32, human_author='Hruday N M (BUNZEEY)',
                   scope=findings.get('scope_statement', 'Ten reviewed investigations; fixed-lattice families, not a continuum construction.'),
                   counts={'nodes': len(nodes), 'edges': len(edges), 'new_research_loops': 10})
    return json.dumps(network, indent=2, ensure_ascii=False) + '\n'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    content = build()
    path = ROUND / 'network.json'
    if args.check:
        if not path.is_file() or path.read_text() != content:
            raise ValueError('Network rebuild differs')
    else:
        path.write_text(content)
    print(json.dumps({'status': 'passed', 'mode': 'check' if args.check else 'build'}))
