"""Build Round28's additive presentation only from selected, source-bound records.

The default build supports an active cycle. --require-complete is the release gate:
ten distinct selected investigations, ten final evidence gates, complete summaries,
the final network, and an explicit next-goal/proof-obligation assessment.
This presentation check complements, rather than replaces, the research validator.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
ROUND = Path('research/round28')
ID = re.compile(r'[a-z][a-z0-9]*(?:-[a-z0-9]+)*\Z')
SHA = re.compile(r'[a-f0-9]{64}\Z')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def load(path, default=None):
    return json.loads(path.read_text()) if path.is_file() else default


def local(root, path):
    require(isinstance(path, str) and path and not Path(path).is_absolute(), 'invalid relative source path')
    require(not any(part in ('', '.', '..') for part in path.split('/')), 'unsafe source path ' + path)
    resolved = (root / path).resolve()
    require(resolved.is_relative_to(root.resolve()), 'source leaves repository ' + path)
    require(resolved.is_file(), 'missing source ' + path)
    return resolved


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def text(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return ' '.join(text(item) for item in value)
    if isinstance(value, dict):
        return '; '.join(f'{key}: {text(item)}' for key, item in value.items())
    return str(value) if value is not None else ''


def source_url(value):
    if not isinstance(value, str) or re.search(r'[\s\\<>"\x00-\x1f\x7f]', value):
        return False
    try:
        url = urlparse(value)
        return url.scheme == 'https' and bool(url.hostname) and not url.username and not url.password
    except ValueError:
        return False


def check_gate(root, loop, sequence, gate):
    require(gate.get('loop') == loop, 'gate loop mismatch ' + loop)
    require(gate.get('sequence') == sequence, 'gate sequence mismatch ' + loop)
    verdict = gate.get('verdict', '')
    require(isinstance(verdict, str) and bool(re.match(r'^(accepted|limited|insufficient|rejected|failed)(?:$|[_ -])', verdict)), 'gate is not a final reviewed outcome ' + loop)
    require(bool(gate.get('completed_at')), 'gate completion not recorded ' + loop)
    require(isinstance(gate.get('accepted'), str) and gate['accepted'].strip(), 'gate scope missing ' + loop)
    require(isinstance(gate.get('limitations'), list) and len(gate['limitations']) > 0, 'gate limitations missing ' + loop)
    require(all(isinstance(item, str) and item.strip() for item in gate['limitations']), 'invalid gate limitation ' + loop)
    bindings = gate.get('bindings')
    require(isinstance(bindings, dict) and bindings, 'gate bindings missing ' + loop)
    required = [f'{ROUND}/contracts/{loop}.json', f'{ROUND}/forward/{loop}/report.md', f'{ROUND}/reverse/{loop}/report.md', f'{ROUND}/skeptic/{loop}.md']
    require(all(path in bindings for path in required), 'gate must bind contract, both reports and skeptic review ' + loop)
    for path, expected in bindings.items():
        require(isinstance(expected, str) and SHA.fullmatch(expected), 'invalid binding hash ' + path)
        require(digest(local(root, path)) == expected, 'changed gate input ' + path)
    return required + [f'{ROUND}/advisor/{loop}-gate.json']


def make_survey(root):
    ledger_specs = [
        ('sources.json', 'source-survey.md', 'Initial source survey'),
        ('source-supplement.json', 'source-supplement.md', 'Supplemental source review'),
    ]
    rows, screening, unread, source_links, origins = [], [], [], [], []
    all_ids, interpretation_limits, discrepancies = set(), [], []
    original = {}
    for filename, narrative, title in ledger_specs:
        ledger = load(root / ROUND / 'experts' / filename, {})
        if not ledger:
            continue
        if filename == 'sources.json':
            original = ledger
        for binding in ledger.get('input_bindings', []):
            require(digest(local(root, binding['path'])) == binding['sha256'], 'changed survey input ' + binding['path'])
        readings = ledger.get('reading_records', [])
        screens = ledger.get('screening_records', [])
        leads = ledger.get('unread_leads', [])
        for item in readings + screens + leads:
            record_id = item.get('record_id', item.get('id'))
            require(isinstance(record_id, str) and record_id, 'source record ID missing in ' + filename)
            require(record_id not in all_ids, 'duplicate source record ID ' + record_id)
            all_ids.add(record_id)
        urls = set(url for item in readings for url in item.get('recorded_urls', []))
        screen_urls = set(item.get('url') for item in screens)
        unread_urls = set(item.get('url') for item in leads)
        require(all(source_url(url) for url in urls | screen_urls | unread_urls), 'invalid survey source URL in ' + filename)
        computed = {
            'formal_reading_records': len(readings),
            'unique_recorded_urls': len(urls),
            'screening_or_reopen_records': len(screens),
            'screening_unique_urls': len(screen_urls),
            'unique_urls_including_screening': len(urls | screen_urls),
            'unread_lead_records': len(leads),
            'unique_urls_including_screening_and_unread_leads': len(urls | screen_urls | unread_urls),
        }
        counts = ledger.get('counts', {})
        for key, value in computed.items():
            if key in counts:
                label = 'reading-count' if key == 'formal_reading_records' else 'URL-count' if key == 'unique_recorded_urls' else key
                require(counts[key] == value, 'source ' + label + ' mismatch in ' + filename)
        for lens, lens_counts in counts.get('by_lens', {}).items():
            lens_readings = [item for item in readings if item['lens'] == lens]
            require(lens_counts.get('reading_records') == len(lens_readings), 'source lens reading-count mismatch ' + lens)
            require(lens_counts.get('unique_recorded_urls') == len(set(url for item in lens_readings for url in item['recorded_urls'])), 'source lens URL-count mismatch ' + lens)
        if 'by_category' in counts:
            categories = {}
            for item in readings:
                category = item.get('category', 'Recorded source')
                categories[category] = categories.get(category, 0) + 1
            require(counts['by_category'] == categories, 'source category-count mismatch in ' + filename)
        if 'unique_recorded_urls' in ledger:
            require(set(ledger['unique_recorded_urls']) == urls, 'source URL inventory mismatch in ' + filename)
        for item in readings:
            record = item.get('original_record', {})
            recorded_urls = item.get('recorded_urls', [])
            require(recorded_urls, 'reading source URL missing ' + item['record_id'])
            rows.append({
                'id': item['record_id'], 'lens': item['lens'],
                'title': record.get('title') or record.get('claim_used') or recorded_urls[0],
                'urls': recorded_urls, 'category': item.get('category', 'Recorded source'),
                'depth': item.get('reading_depth', ''),
                'change_status': item.get('change_status', ''),
                'change_basis': item.get('change_status_basis', ''),
                'use': text(record.get('application') or record.get('application_status') or record.get('admitted_use') or record.get('proposed_use') or record.get('workbench_inference') or record.get('record_vs_interpretation') or record.get('claim_used') or record.get('explicit_scope_observation') or ''),
                'limits': text(record.get('not_licensed') or record.get('not_admitted') or record.get('limits') or record.get('claim_scope') or record.get('status') or record.get('not_established_here') or ''),
                'ledger': item.get('source_ledger', ''),
                'survey_ledger': f'{ROUND}/experts/{filename}',
            })
        screening.extend(screens)
        unread.extend(leads)
        interpretation_limits.extend(ledger.get('interpretation_limits', []))
        discrepancies.extend(ledger.get('bibliographic_discrepancies', []))
        source_links.extend([
            {'path': f'{ROUND}/experts/{narrative}', 'title': title},
            {'path': f'{ROUND}/experts/{filename}', 'title': title + ' · reading ledger'},
        ])
        origins.append({'title': title, 'scope': ledger.get('scope', ''), 'counts': computed})
    unique_urls = set(url for row in rows for url in row['urls'])
    screen_urls = set(item['url'] for item in screening)
    unread_urls = set(item['url'] for item in unread)
    return {
        'records': rows, 'screening': screening, 'unread_leads': unread,
        'counts': {'readings': len(rows), 'urls': len(unique_urls), 'screening': len(screening), 'screening_urls': len(screen_urls), 'urls_including_screening': len(unique_urls | screen_urls), 'unread_leads': len(unread), 'urls_including_screening_and_unread': len(unique_urls | screen_urls | unread_urls)},
        'ledgers': origins,
        'counting_rules': original.get('counting_rules', {}),
        'interpretation_limits': list(dict.fromkeys(interpretation_limits)),
        'government_context': original.get('inherited_government_context', {}),
        'discrepancies': discrepancies,
        'sources': source_links,
    }


def check_network(root, network):
    nodes, edges = network.get('nodes', []), network.get('edges', [])
    ids = [node.get('id') for node in nodes]
    require(all(isinstance(item, str) and item for item in ids) and len(ids) == len(set(ids)), 'duplicate or invalid network IDs')
    require(all(edge.get('from') in ids and edge.get('to') in ids for edge in edges), 'dangling network edge')
    require(all(edge.get('type') in ('proven-dependency', 'proposed-transfer', 'review-selection') for edge in edges), 'unrecognized network edge type')
    for node in nodes:
        for source in node.get('sources', []):
            path = source if isinstance(source, str) else source.get('path')
            if path and not path.startswith('https://'):
                local(root, path)


def build(root=ROOT, require_complete=False):
    root = Path(root)
    base = root / ROUND
    sequence_record = load(base / 'advisor/sequence.json')
    require(isinstance(sequence_record, dict), 'selected loop sequence missing')
    selected = sequence_record.get('loops', [])
    requested = sequence_record.get('target_loops')
    require(requested == 10, 'Round28 requires exactly ten new investigations')
    require(isinstance(selected, list) and len(selected) <= requested and len(selected) == len(set(selected)), 'invalid or duplicate selected sequence')
    require(all(isinstance(loop, str) and ID.fullmatch(loop) for loop in selected), 'invalid loop identifier')
    summaries = load(base / 'advisor/summaries.json', {})
    progress_input = load(base / 'advisor/progress.json', {})
    metadata = summaries.get('_presentation', {})
    records, completed = [], []
    for number, loop in enumerate(selected, start=1):
        contract = load(base / f'contracts/{loop}.json')
        require(isinstance(contract, dict) and contract.get('loop') == loop, 'selected contract missing or mismatched ' + loop)
        gate = load(base / f'advisor/{loop}-gate.json')
        if gate is None:
            # Deliberately do not inspect producer reports or present proposed equations.
            records.append({'id': loop, 'goal': contract.get('goal', ''), 'title': f'{loop.upper()} · selected investigation', 'stage': 'in-progress' if progress_input.get('active_loop') == loop else 'selected', 'verdict': 'Review pending', 'accepted': '', 'limitations': [], 'equations': [], 'bullets': [], 'sources': [f'{ROUND}/contracts/{loop}.json']})
            continue
        require(len(completed) == number - 1, 'a later gate precedes an unfinished selected investigation')
        sources = check_gate(root, loop, number, gate)
        summary = summaries.get(loop, {})
        if require_complete:
            require(summary.get('title') and isinstance(summary.get('bullets'), list) and isinstance(summary.get('equations'), list), 'final presentation summary missing ' + loop)
        records.append({
            'id': loop, 'goal': contract.get('goal', ''), 'stage': 'reviewed',
            'title': summary.get('title') or f'{loop.upper()} · reviewed investigation',
            'verdict': gate['verdict'], 'accepted': gate['accepted'],
            'model': gate.get('model', ''), 'limitations': gate['limitations'],
            'equations': summary.get('equations', []), 'bullets': summary.get('bullets', []),
            'derivation_steps': summary.get('derivation_steps', []),
            'applications': summary.get('applications', []),
            'sources': sources, 'gate_sha256': digest(base / f'advisor/{loop}-gate.json')
        })
        completed.append(loop)
    claimed = progress_input.get('completed_loops', [])
    require(isinstance(claimed, list) and all(loop in completed for loop in claimed), 'progress claims an investigation without a valid final gate')
    pair_record = load(base / 'advisor/goal-pairs.json', {})
    cycle = load(base / 'advisor/cycle.json', {})
    targets = {item['goal']: item.get('target', '') for item in cycle.get('initial_goal_order', [])}
    pairs = []
    for pair in pair_record.get('initial_goals', []) + pair_record.get('later_goals', []):
        loops = pair.get('loops', [])
        pairs.append({'id': pair['id'], 'target': pair.get('target') or targets.get(pair['id'], ''), 'loops': loops, 'completed': sum(loop in completed for loop in loops), 'selected': sum(loop in selected for loop in loops)})
    roadmap = load(base / 'advisor/roadmap.json', {})
    panel = load(base / 'advisor/panel-progress.json', progress_input)
    network = load(base / 'network.json')
    if network is not None:
        check_network(root, network)
    if require_complete:
        require(len(selected) == requested and len(completed) == requested, 'ten source-bound reviewed gates required for final release')
        require(len(pairs) == 5 and all(len(pair['loops']) == 2 and pair['completed'] == 2 for pair in pairs), 'five completed goal pairs required')
        require(set(loop for pair in pairs for loop in pair['loops']) == set(completed), 'goal pairs do not match completed sequence')
        require(network is not None, 'final Round28 network missing')
        require(all(any(node.get('route') == 'round28-' + loop for node in network['nodes']) for loop in completed), 'final network must contain each reviewed loop route')
        require(isinstance(roadmap.get('next_goals'), list), 'final next-goal roadmap missing')
        require(panel.get('percentage_statement') and panel.get('obligations'), 'final proof-obligation assessment missing')
    addendum = metadata.get('addendum')
    if addendum is None and (root / 'dist/ym-round28-addendum.pdf').is_file():
        addendum = {'url': 'ym-round28-addendum.pdf', 'title': 'Round28 research addendum'}
    if addendum:
        url = addendum.get('url', '')
        require(source_url(url) or local(root, 'dist/' + url), 'invalid addendum URL')
    result = {
        'schema': 'ym28-public-research-v1',
        'title': metadata.get('title', 'Follow each result to its remaining premise.'),
        'summary': metadata.get('summary', 'Five goal pairs, selected through independent derivation, reconstruction and skeptical review. Each result retains its model, sources and limitations.'),
        'loops': records, 'goal_pairs': pairs, 'survey': make_survey(root),
        'roadmap': roadmap,
        'progress': {'requested': requested, 'completed': len(completed), 'selected': len(selected), 'remaining': requested - len(completed), 'cycle_complete': len(completed) == requested, 'percentage_statement': panel.get('percentage_statement', 'No new percentage assessment is recorded. Investigation counts do not measure the fraction of a Yang–Mills proof completed.'), 'obligations': panel.get('obligations', [])},
        'addendum': addendum, 'network': network,
        'sources': [f'{ROUND}/advisor/sequence.json', f'{ROUND}/advisor/goal-pairs.json'],
    }
    return result


def write_bundle(data, output):
    encoded = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', r'<\/').replace('\u2028', r'\u2028').replace('\u2029', r'\u2029')
    output.write_text('window.ROUND28_DATA = ' + encoded + ';\nif(window.ROUND26_DATA && window.ROUND28_DATA.network) window.ROUND26_DATA.network = window.ROUND28_DATA.network;\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--require-complete', action='store_true', help='Refuse a final release unless all ten reviewed gates and final assessments exist')
    parser.add_argument('--check', action='store_true', help='Validate without writing the browser bundle')
    args = parser.parse_args()
    data = build(require_complete=args.require_complete)
    if not args.check:
        write_bundle(data, ROOT / 'dist/research-round28-data.js')
    print(json.dumps({'status': 'passed', 'mode': 'final' if args.require_complete else 'active-cycle', 'completed': data['progress']['completed'], 'requested': data['progress']['requested'], 'selected': data['progress']['selected'], 'source_readings': data['survey']['counts']['readings'], 'network_nodes': len(data['network']['nodes']) if data['network'] else 0}))


if __name__ == '__main__':
    main()
