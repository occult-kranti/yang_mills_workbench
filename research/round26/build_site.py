"""Build the current results and evidence network from reviewed records."""
import argparse
import json
from pathlib import Path
from admission import ROOT, R, LOOPS, gate, digest, require, hashes


def state(verdict):
    if 'insufficien' in verdict or 'limited' in verdict:
        return 'limited'
    if verdict.startswith('accepted'):
        return 'proved-in-model'
    if 'conditional' in verdict:
        return 'conditional'
    return 'limited'


def build(partial=False):
    history = json.loads((ROOT / 'research/round25/all-results.json').read_text())
    hashes(history['source_sha256'])
    summary_path = R / 'advisor/summaries.json'
    summaries = json.loads(summary_path.read_text()) if summary_path.exists() else {}
    if not partial:
        require(set(summaries) == set(LOOPS), 'all ten presentation summaries required')
        for item in summaries.values():
            require(bool(item.get('title')) and bool(item.get('bullets')) and bool(item.get('equations')), 'incomplete loop presentation')
    nodes, edges, loops = [], [], []
    source_node = {}
    for round_ in history['rounds']:
        for item in round_['runs']:
            node_id = f"r{round_['round']}-{item['id']}"
            nodes.append({'id': node_id, 'title': f"R{round_['round']} · {item['id'].upper()} · {item['title']}",
                          'kind': 'history', 'status': state(item['verdict']),
                          'summary': item['bullets'][0], 'detail': '\n'.join(item['bullets'][1:]),
                          'sources': item['sources'], 'route': 'all-results'})
            for p in item['sources']:
                source_node[p] = node_id
    # Recover historical provenance from actual recorded path bindings. Do not
    # invent a mathematical dependency merely because two loops are adjacent.
    historical_links = set()
    def bound_paths(value):
        if isinstance(value, dict):
            for key, child in value.items():
                if key in source_node:
                    yield key
                yield from bound_paths(child)
        elif isinstance(value, list):
            for child in value:
                yield from bound_paths(child)
        elif isinstance(value, str) and value in source_node:
            yield value
    for round_ in history['rounds']:
        for item in round_['runs']:
            destination = f"r{round_['round']}-{item['id']}"
            for name in item['sources']:
                if name.endswith('-gate.json'):
                    record = json.loads((ROOT / name).read_text())
                    for path in bound_paths(record):
                        origin = source_node[path]
                        pair = (origin, destination)
                        if origin != destination and pair not in historical_links:
                            historical_links.add(pair)
                            edges.append({'from': origin, 'to': destination,
                                          'type': 'proven-dependency',
                                          'label': 'recorded source dependency',
                                          'detail': f'{name} binds {path}. This is provenance, not an automatic transfer of model conclusions.'})
    for loop in LOOPS:
        if not (R / f'advisor/{loop}-gate.json').exists():
            require(partial, 'missing final reviewed loop ' + loop)
            continue
        g = gate(loop)
        c = json.loads((R / f'contracts/{loop}.json').read_text())
        info = summaries.get(loop, {})
        title = info.get('title', g['accepted'])
        sources = [f'research/round26/advisor/{loop}-gate.json',
                   f'research/round26/contracts/{loop}.json',
                   f'research/round26/forward/{loop}/report.md',
                   f'research/round26/reverse/{loop}/report.md',
                   f'research/round26/skeptic/{loop}.md',
                   f'research/round26/forward/{loop}/output/results.json',
                   f'research/round26/reverse/{loop}/output/results.json']
        if (R / f'advisor/{loop}-inventory-repair.json').exists():
            sources.append(f'research/round26/advisor/{loop}-inventory-repair.json')
        item = {'loop': loop, 'goal': loop[:-1].upper(), 'title': title,
                'model': c['model'], 'verdict': g['verdict'], 'accepted': g['accepted'],
                'bullets': info.get('bullets', [g['accepted']]),
                'limitations': g['limitations'], 'equations': info.get('equations', []),
                'sources': sources, 'gate_sha256': digest(R / f'advisor/{loop}-gate.json')}
        loops.append(item)
        nodes.append({'id': loop, 'title': loop.upper() + ' · ' + title,
                      'kind': 'loop', 'status': state(g['verdict']), 'summary': g['accepted'],
                      'detail': '\n'.join(g['limitations']), 'model': c['model'],
                      'sources': sources, 'route': 'round26-' + loop})
        for p in sources:
            source_node[p] = loop
        for i, equation in enumerate(item['equations']):
            eq = equation if isinstance(equation, str) else equation['expression']
            label = f'{loop.upper()}.{i + 1}' if isinstance(equation, str) else equation.get('label', f'{loop.upper()}.{i + 1}')
            eq_id = f'{loop}-equation-{i + 1}'
            nodes.append({'id': eq_id, 'title': label, 'kind': 'equation',
                          'status': 'proved-in-model', 'summary': eq, 'equation': eq,
                          'detail': 'Use only under the model, hypotheses and scope in the linked reports. Scientific priority unverified.',
                          'model': c['model'], 'sources': sources[2:5], 'route': 'round26-' + loop})
            edges.append({'from': loop, 'to': eq_id, 'type': 'proven-dependency',
                          'label': 'derived within stated scope'})
    for loop in loops:
        c = json.loads((R / f"contracts/{loop['loop']}.json").read_text())
        seen = set()
        for p in c['dependencies']:
            origin = source_node.get(p)
            if origin and origin != loop['loop'] and origin not in seen:
                seen.add(origin)
                feedback = origin.startswith(loop['loop'][:-1]) and origin.endswith('1') and loop['loop'].endswith('2')
                edges.append({'from': origin, 'to': loop['loop'],
                              'type': 'review-selection' if feedback else 'proven-dependency',
                              'label': 'review selects next test' if feedback else 'declared inherited premise',
                              'detail': p})
    extra = R / 'advisor/network-extensions.json'
    if extra.exists():
        x = json.loads(extra.read_text()); nodes.extend(x['nodes']); edges.extend(x['edges'])
    ids = [n['id'] for n in nodes]
    require(len(ids) == len(set(ids)), 'duplicate graph node')
    for e in edges:
        require(e['from'] in ids and e['to'] in ids, 'dangling graph edge')
        require(e['type'] in ['proven-dependency', 'proposed-transfer', 'review-selection'], 'edge type')
    for n in nodes:
        for s in n.get('sources', []):
            path = s if isinstance(s, str) else s.get('path')
            if path and not path.startswith('https:'):
                require((ROOT / path).is_file(), 'missing graph source ' + path)
    roadmap = R / 'advisor/roadmap.json'
    if not partial:
        require(roadmap.is_file(), 'final prospective roadmap required')
        plan = json.loads(roadmap.read_text())
        require(len(plan.get('next_goals', [])) == 3, 'three next goals required')
        require(all(x.get('status') == 'planned' for x in plan['next_goals']), 'future goals must remain planning only')
        hashes(plan['source_sha256'])
    data = {'title': 'Ten reviewed loops. Connected evidence.',
            'summary': 'Five goals follow two reviewed loops each. Open parent problems remain visible beside the accepted results.',
            'scope': 'Three distinct fixed-spacing models. No continuum mass-gap solution or established scientific priority.',
            'review': 'Separate forward, reverse and skeptic model agents, coordinated by the advisor; not external peer review.',
            'loops': loops, 'network': {'nodes': nodes, 'edges': edges}, 'history': history,
            'roadmap': json.loads(roadmap.read_text()) if roadmap.exists() else {'next_goals': []}}
    text = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', r'<\/')
    (ROOT / 'dist/research-round26-data.js').write_text('window.ROUND26_DATA = ' + text + ';\n')
    (R / 'network.json').write_text(json.dumps(data['network'], ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'loops': len(loops), 'nodes': len(nodes), 'edges': len(edges)}))


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('--partial', action='store_true')
    build(p.parse_args().partial)
