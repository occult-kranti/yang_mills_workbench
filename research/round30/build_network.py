#!/usr/bin/env python3
"""Extend the current evidence graph without rewriting historical networks."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
R = ROOT / 'research/round30'


def main():
    findings = json.loads((R / 'advisor/findings.json').read_text())
    if findings['completed'] != 3 or len(findings['loops']) != 3:
        raise ValueError('Exactly three reviewed investigations required')
    net = json.loads((ROOT / 'research/round29/network.json').read_text())
    registry = json.loads((ROOT / 'papers/draft-03/registry/hnm-registry.json').read_text())
    nodes, edges = net['nodes'], net['edges']
    existing = {x['id'] for x in nodes}

    def node(record):
        if record['id'] in existing:
            raise ValueError('Duplicate node ' + record['id'])
        existing.add(record['id'])
        nodes.append(record)

    def edge(start, end, kind, detail):
        if start not in existing or end not in existing:
            raise ValueError('Missing edge endpoint')
        edges.append({'from': start, 'to': end, 'type': kind, 'label': detail})

    byid = {x['legacy_id'].upper(): x for x in registry['contributions']}
    for row in findings['loops']:
        lid = row['id'].lower()
        gate_path = f'research/round30/advisor/{lid}-gate.json'
        gate = json.loads((ROOT / gate_path).read_text())
        for name, sha in gate['bindings'].items():
            if hashlib.sha256((ROOT / name).read_bytes()).hexdigest() != sha:
                raise ValueError('Changed admitted evidence ' + name)
        alias = byid[row['id'].upper()]
        node({'id': 'r30-' + lid, 'title': alias['display_name'], 'kind': 'loop',
              'status': gate['verdict'], 'summary': gate['accepted'],
              'detail': ' '.join(gate['limitations']), 'sources': alias['source_paths'],
              'route': 'round30-' + lid, 'hnm_alias': alias['id'],
              'hnm_aliases': [alias['id']] + alias.get('statement_ids', [])})
        for dependency in row.get('dependencies', []):
            edge(dependency, 'r30-' + lid, 'proven-dependency', 'Same-model admitted premise; see contract')
        for pattern in row.get('method_patterns', []):
            edge(pattern, 'r30-' + lid, 'review-selection', 'Proof pattern only; no state identification')
        if row['sequence'] > 1:
            prev = findings['loops'][row['sequence'] - 2]['id'].lower()
            edge('r30-' + prev, 'r30-' + lid, 'review-selection', 'Selected after the preceding review')
        for eq in registry['equations']:
            if alias['id'] not in eq.get('contribution_ids', []):
                continue
            node({'id': 'r30-eq-' + eq['id'].lower(), 'title': eq['id'],
                  'kind': 'equation', 'status': gate['verdict'],
                  'summary': eq.get('scope', 'Equation alias in the scoped derivation'),
                  'detail': 'A record locator, not a separate discovery.',
                  'sources': alias['source_paths'], 'route': 'round30-' + lid,
                  'hnm_alias': eq['id']})
            edge('r30-' + lid, 'r30-eq-' + eq['id'].lower(), 'recorded-equation', 'Recorded derivation')
    if 'r29-next-at' in existing:
        edge('r29-next-at', 'r30-at1', 'review-selection',
             'Bounded planned continuation executed; actual response data remain a future goal')
    for folder, relative in [('historical', 'experts/historical/sources.json'),
                             ('modern', 'experts/modern/sources.json'),
                             ('method', 'editorial/method-source-addendum.json')]:
        path = R / relative
        ledger = json.loads(path.read_text())
        records = ledger if isinstance(ledger, list) else ledger.get('sources', ledger.get('records', []))
        for index, source in enumerate(records):
            sid = f'r30-source-{folder}-{index + 1}'
            node({'id': sid, 'title': source.get('title', source.get('id', sid)),
                  'kind': 'literature', 'status': 'source-reviewed',
                  'summary': source.get('claim_used', source.get('relevance', source.get('use', 'See reading record'))),
                  'detail': 'Selected reading or recorded access limitation. Cultural claims are not physics premises.',
                  'sources': [str(path.relative_to(ROOT))], 'route': 'round30-sources'})
            target = 'r30-at3' if folder == 'method' else 'r30-at1'
            edge(sid, target, 'review-selection',
                 'Panel reading and bounded triage; not automatic theorem evidence')
    roadmap = json.loads((R / 'advisor/roadmap.json').read_text())
    for goal in roadmap['goals']:
        sid = 'r30-next-' + goal['id'].lower()
        node({'id': sid, 'title': goal['title'], 'kind': 'open', 'status': 'planned',
              'summary': goal['target'], 'detail': goal.get('missing_premise', ''),
              'sources': ['research/round30/advisor/roadmap.json'], 'route': 'round30-roadmap'})
        for dep in goal.get('dependencies', []):
            edge(dep, sid, 'proposed-transfer', 'Future target; not executed in this cycle')
    net['current_round'] = 30
    net['human_author'] = 'Hruday N M (BUNZEEY)'
    net['scope'] = 'Current evidence network. Graph layout and node counts have no physical or proof-completion meaning.'
    net['counts'] = {'nodes': len(nodes), 'edges': len(edges)}
    (R / 'network.json').write_text(json.dumps(net, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps(net['counts']))


if __name__ == '__main__':
    main()
