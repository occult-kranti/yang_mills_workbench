"""Publish the current HNM presentation; retain source-bound historical evidence.

--require-complete rejects release unless ten sequential reviews, the current
naming registry, final network and full Draft02 exist. This is a presentation
check, not a replacement for the scientific validator.
"""
from __future__ import annotations
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parents[2]
ROUND = Path('research/round29')
AUTHOR = 'Hruday N M (BUNZEEY)'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def load(path, default=None):
    return json.loads(path.read_text()) if path.is_file() else default


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def local(root, path):
    require(isinstance(path, str) and path and not Path(path).is_absolute(), 'invalid relative source')
    require(not any(part in ('', '.', '..') for part in path.split('/')), 'unsafe source ' + path)
    resolved = (root / path).resolve()
    require(resolved.is_relative_to(root.resolve()) and resolved.is_file(), 'missing or unsafe source ' + path)
    return resolved


def build(root=ROOT, require_complete=False):
    root = Path(root)
    base = root / ROUND
    findings = load(base / 'advisor/findings.json', {})
    registry_path = 'papers/draft-02/registry/hnm-registry.json'
    registry = load(root / registry_path, {'contributions': [], 'equations': [], 'quantities': []})
    contributions = registry.get('contributions', [])
    names = {str(item.get('legacy_id', '')).lower(): item for item in contributions}
    loops = []
    for index, item in enumerate(findings.get('loops', []), start=1):
        loop = str(item['id']).lower()
        require(re.fullmatch(r'[a-z][a-z0-9-]*', loop), 'invalid loop ID')
        gate_path = base / f'advisor/{loop}-gate.json'
        gate = load(gate_path)
        if not gate:
            loops.append({'id': loop, 'goal': loop.rstrip('0123456789').upper(), 'title': item.get('title', loop.upper()), 'stage': 'selected', 'verdict': 'Review pending', 'accepted': '', 'limitations': [], 'equations': [], 'sources': [f'{ROUND}/contracts/{loop}.json']})
            continue
        require(str(gate.get('loop', '')).lower() == loop and gate.get('sequence') == index, 'gate sequence/ID mismatch ' + loop)
        require(bool(gate.get('completed_at')), 'gate completion missing ' + loop)
        require(bool(re.match(r'^(accepted|limited|insufficient|rejected|failed)(?:$|[_ -])', gate.get('verdict', ''))), 'nonfinal gate ' + loop)
        require(gate.get('accepted') and gate.get('limitations'), 'gate scope/limitations missing ' + loop)
        bindings = gate.get('bindings', {})
        required = [f'{ROUND}/contracts/{loop}.json', f'{ROUND}/forward/{loop}/report.md', f'{ROUND}/reverse/{loop}/report.md', f'{ROUND}/skeptic/{loop}.md']
        require(all(path in bindings for path in required), 'missing required source bindings ' + loop)
        for path, expected in bindings.items():
            require(digest(local(root, path)) == expected, 'changed gate input ' + path)
        alias = names.get(loop, {})
        equations = item.get('equations', [])
        if not equations:
            report = (base/f'forward/{loop}/report.md').read_text()
            for number, expression in enumerate(re.findall(r'\\\[(.*?)\\\]', report, re.S), start=1):
                tag = re.search(r'\\tag\{([^}]+)\}', expression)
                equations.append({'label': tag.group(1) if tag else f'HNM {loop.upper()} · derivation {number}', 'expression': expression.strip(), 'scope': 'Source-bound forward derivation. The accepted scope and limitations below govern its use.'})
        loops.append({'id': loop, 'goal': loop.rstrip('0123456789').upper(), 'title': alias.get('display_name', item.get('title', loop.upper())), 'stage': 'reviewed', 'current_extensions': alias.get('current_extensions', []), 'statement_ids': alias.get('statement_ids', []), 'verdict': gate['verdict'], 'accepted': gate['accepted'], 'model': gate.get('model', item.get('model', '')), 'limitations': gate['limitations'], 'equations': equations, 'bullets': item.get('bullets', []), 'derivation_steps': item.get('derivation_steps', []), 'applications': item.get('applications', []), 'sources': required + [str(gate_path.relative_to(root))], 'gate_sha256': digest(gate_path)})
    completed = sum(loop['stage'] == 'reviewed' for loop in loops)
    require(len({loop['id'] for loop in loops}) == len(loops), 'duplicate loop')
    require(findings.get('completed', completed) == completed, 'claimed loop count differs from valid reviews')
    pairs = []
    for loop in loops:
        pair = next((pair for pair in pairs if pair['id'] == loop['goal']), None)
        if pair is None:
            pair = {'id': loop['goal'], 'target': loop['title'], 'loops': [], 'completed': 0}; pairs.append(pair)
        pair['loops'].append(loop['id']); pair['completed'] += loop['stage'] == 'reviewed'
    network = load(base / 'network.json', load(root / 'research/round28/network.json'))
    if network:
        ids = [str(node['id']) for node in network['nodes']]
        require(len(ids) == len(set(ids)), 'duplicate network IDs')
        require(all(edge['from'] in ids and edge['to'] in ids for edge in network['edges']), 'dangling network edge')
        require(all(edge['type'] in ('proven-dependency', 'proposed-transfer', 'review-selection', 'source-dependency', 'scope-boundary', 'recorded-equation') for edge in network['edges']), 'unknown network relation')
        for node in network['nodes']:
            candidate = str(node.get('id', '')).lower()
            route = str(node.get('route', ''))
            alias = names.get(candidate) or names.get(re.sub(r'^round\d+-', '', route))
            if alias and not node.get('hnm_alias') and node.get('kind') in ('loop', 'history'):
                node.setdefault('legacy_title', node['title']); node['title'] = alias['display_name']
                node['hnm_id'] = alias['id']
            elif not node.get('hnm_alias') and node.get('kind') in ('equation', 'loop', 'history'):
                node.setdefault('legacy_title', node['title'])
                node['title'] = 'HNM record · ' + node['title']
            for source in node.get('sources', []):
                path = source if isinstance(source, str) else source.get('path')
                if path and not path.startswith('https://'): local(root, path)
    # The previous survey remains available on its own historical route.
    survey = {'records': [], 'screening': [], 'interpretation_limits': ['Historical lenses are research methods, not endorsements. Source review does not establish scientific priority.'], 'sources': []}
    for ledger_path in [base/'experts/sources.json', base/'experts/source-review.json']:
        ledger = load(ledger_path)
        if ledger:
            for row in ledger.get('sources', ledger.get('records', ledger.get('reading_records', []))):
                survey['records'].append({'id': row.get('id', row.get('record_id', '')), 'lens': row.get('lens', 'panel'), 'title': row.get('title', ''), 'category': row.get('category', 'technical_primary'), 'urls': row.get('urls', row.get('recorded_urls', [row['url']] if row.get('url') else [])), 'depth': row.get('reading_depth', row.get('depth', 'See source review')), 'use': row.get('use', row.get('claim_used', '')), 'limits': row.get('limits', row.get('not_licensed', '')), 'ledger': str(ledger_path.relative_to(root))})
            survey['sources'].append(str(ledger_path.relative_to(root)))
    obligations = findings.get('obligations', [
        {'name': 'Infinite-volume identification at the numerical AM2 interval', 'status': 'Open at the numerical interval; symbolic I1 construction retains its own premises', 'missing': 'AM2 supplies a volume-uniform finite-volume full-model gap for |tau| <= 1/100000000. Identification of an infinite-volume physical ground state, its representation and generator at that numerical interval remains separate. The inherited I1 infinite-state construction still requires its unevaluated symbolic smallness interval.'},
        {'name': 'Fixed physical energy and continuum limit', 'status': 'Open', 'missing': 'Control cutoff removal at one fixed positive physical energy reference, with the full action, observables and physical clock matched. Declaring a common reference does not establish that continuum matching.'},
        {'name': 'Clay existence and mass gap', 'status': 'Open', 'missing': 'A nontrivial quantum Yang–Mills theory on R4 for every compact simple gauge group, the required axioms, and a positive mass gap.'}
    ])
    if require_complete:
        require(completed == 10 and len(loops) == 10, 'ten reviewed investigations required')
        require(len(pairs) == 5 and all(pair['completed'] == 2 for pair in pairs), 'five reviewed goal pairs required')
        require(bool(contributions), 'current naming registry missing')
        require(all(loop['id'] in names for loop in loops), 'current registry omits a reviewed R29 contribution')
        require(bool(survey['records']), 'current primary source survey missing')
        require((base/'network.json').is_file(), 'current network missing')
        require(all(any(node.get('route') == 'round29-' + loop['id'] for node in network['nodes']) for loop in loops), 'network omits reviewed loop')
        require(bool(findings.get('planned_next')), 'next-goal assessment missing')
        require((root/'papers/draft-02/main.pdf').is_file(), 'complete current draft missing')
    return {'schema': 'hnm-current-research-v1', 'author': AUTHOR, 'title': 'A research workbench for the Yang–Mills problem.', 'summary': 'Read the derivations, reproduce the checks, and follow each result to the question it leaves open.', 'loops': loops, 'goal_pairs': pairs, 'registry': registry, 'registry_source': registry_path, 'survey': survey, 'network': network, 'roadmap': {'next_goals': findings.get('planned_next', []), 'summary': findings.get('roadmap_summary', '')}, 'progress': {'requested': 10, 'completed': completed, 'selected': len(loops), 'remaining': 10-completed, 'cycle_complete': completed == 10, 'percentage_statement': findings.get('percentage_statement', 'Ten investigations count research work, not a percentage of the Yang–Mills problem solved. The continuum construction and physical mass gap remain open.'), 'obligations': obligations}, 'addendum': {'url': 'ym-draft-02.pdf', 'title': 'The complete HNM draft · Rounds 3–29', 'summary': 'Updated author, current naming, full research history and the newest reviewed addendum.'} if (root/'papers/draft-02/main.pdf').is_file() else None}


def write_bundle(data, output):
    encoded = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', r'<\/').replace('\u2028', r'\u2028').replace('\u2029', r'\u2029')
    output.write_text('window.ROUND29_DATA = ' + encoded + ';\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-complete', action='store_true'); parser.add_argument('--check', action='store_true')
    args = parser.parse_args(); data = build(require_complete=args.require_complete)
    if not args.check:
        write_bundle(data, ROOT/'dist/research-round29-data.js')
        pdf = ROOT/'papers/draft-02/main.pdf'
        if pdf.is_file(): shutil.copyfile(pdf, ROOT/'dist/ym-draft-02.pdf')
        registry = ROOT/'papers/draft-02/registry/hnm-registry.json'
        if registry.is_file(): shutil.copyfile(registry, ROOT/'dist/hnm-registry.json')
    print(json.dumps({'status': 'passed', 'mode': 'final' if args.require_complete else 'active', 'completed': data['progress']['completed'], 'registry_rows': len(data['registry'].get('contributions', [])), 'network_nodes': len(data['network']['nodes']) if data['network'] else 0}))

if __name__ == '__main__': main()
