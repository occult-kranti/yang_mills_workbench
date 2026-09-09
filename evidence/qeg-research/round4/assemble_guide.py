#!/usr/bin/env python3
"""Assemble a source-faithful guide from reviewed project chapters.

Original research files remain untouched. Normalizes source citations and heading
levels only, apart from explicitly documented presentational formula wrapping.
The final build is coordinated by the root; this script alone does not approve
physics results or the UI implementation.
"""
from pathlib import Path
from collections import OrderedDict
import argparse, hashlib, json, re

ROOT = Path(__file__).resolve().parent
CHAPTERS = [
    'advisor_pipeline.md', 'advisor_skill_forward_test.md', 'response_contract.md',
    'response_verifier.md', 'response_advisor_review.md',
    'physics_completion_roadmap.md', 'targeted_solver_prompt.md', 'ux_spec.md'
]


def records(path):
    raw = json.loads(path.read_text())
    return raw.get('records', []) if isinstance(raw, dict) else raw


def references():
    refs = OrderedDict()
    for filename in ['advisor_sources.json', 'response_sources.json', 'ux_sources.json']:
        for r in records(ROOT / filename):
            ident = r['id']
            if ident in refs:
                raise ValueError(f'Duplicate source ID {ident}')
            refs[ident] = {
                'title': r['title'],
                'authors': r.get('authors', r.get('organization', '')),
                'date': r.get('date') or 'Date not specified',
                'url': r['url'],
                'role': r.get('used_for', r.get('use', r.get('supports', ''))),
                'readdepth': 'Reading record: ' + r.get('reading_depth', r.get('read_depth', 'Not recorded')),
                'access': 'Checked ' + r.get('accessed', r.get('access_date', r.get('checked', '2026-09-09'))) + '. ' + r.get('limitations', r.get('limitation', '')),
            }
    return refs


def normalize(text, filename, refs):
    if filename == 'advisor_pipeline.md':
        text = re.split(r'(?m)^## Sources\s*$', text)[0]
        def numeric(m):
            entries = re.split(r'\s*,\s*', m.group(1))
            nums = []
            for e in entries:
                if re.fullmatch(r'\d+\s*[–-]\s*\d+', e):
                    first, last = map(int, re.split(r'\s*[–-]\s*', e))
                    nums.extend(range(first, last + 1))
                elif e.isdigit(): nums.append(int(e))
                else: return m.group(0)
            if not all(1 <= n <= 13 for n in nums): return m.group(0)
            return '[' + '; '.join(f'@R4A{n:02d}' for n in nums) + ']'
        text = re.sub(r'\[(\d+(?:\s*(?:,|–|-)\s*\d+)*)\](?!\()', numeric, text)
    if filename in ['response_contract.md', 'physics_completion_roadmap.md', 'targeted_solver_prompt.md']:
        text = re.sub(r'\[(R\d{2})\](?!\()', r'[@\1]', text)
    by_url = {r['url'].rstrip('/'): i for i, r in refs.items()}
    def link(m):
        ident = by_url.get(m.group(2).rstrip('/'))
        if ident:
            return m.group(1) + ' [@' + ident + ']'
        return m.group(0)
    text = re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)', link, text)
    # The document title is a distinct cover. Chapter h1 becomes h2, and every
    # existing subheading is shifted one level for an unambiguous outline.
    text = re.sub(r'(?m)^(#{1,5})(\s+)', r'#\1\2', text)
    return text.strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--overview', default='guide_overview.md')
    args = parser.parse_args()
    refs = references()
    intro = ROOT / args.overview
    sources = ([args.overview] if intro.exists() else []) + CHAPTERS
    parts = ['# Advisor and research guide\n\nCausal quantum backreaction research • 9 September 2026\n\nA documented advisor pipeline, complete response contract, independent checks, and staged route toward coupled electromagnetic–quantum–gravity calculations.']
    for filename in sources:
        text = (ROOT / filename).read_text()
        parts.append(normalize(text, filename, refs))
    text = '\n\n\n'.join(parts) + '\n'
    used = set(re.findall(r'@([A-Za-z][A-Za-z0-9]+)', text))
    missing = sorted(used - set(refs))
    if missing:
        raise ValueError(f'Unknown citation IDs: {missing}')
    # References are retained in deterministic source-ledger order. A source
    # ledger record can be present as documented coverage without a prose quote.
    (ROOT / 'guide.md').write_text(text)
    (ROOT / 'guide_references.json').write_text(json.dumps(refs, indent=2, ensure_ascii=False) + '\n')
    manifest = {
        'title': 'Advisor and research guide',
        'inputs': [{
            'path': name,
            'sha256': hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),
            'words': len((ROOT/name).read_text().split()),
        } for name in sources],
        'output_words': len(text.split()), 'sources': len(refs),
        'cited_ids': sorted(used), 'missing_citations': missing,
        'overview_present': intro.exists(),
        'normalization': ['Numbered advisor citations → stable R4A IDs', 'Response [Rxx] → Pandoc citation IDs', 'Matching UX primary links → citation IDs', 'Heading levels shifted; source files unchanged', 'Advisor local source list omitted in favor of consolidated bibliography'],
        'evidence_hashes': {name: hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ['physics_acceptance.json', 'response_results.json', 'response_verification.json', 'response_production_comparison.json'] if (ROOT/name).exists()},
        'approval': 'Assembly alone is not scientific or UI acceptance; root authorizes final content.'
    }
    (ROOT/'guide_assembly_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps({k:manifest[k] for k in ['output_words','sources','missing_citations','overview_present']}))

if __name__ == '__main__':
    main()
