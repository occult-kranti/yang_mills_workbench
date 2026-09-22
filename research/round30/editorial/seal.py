#!/usr/bin/env python3
"""Bind a visually reviewed Draft03 artifact; this script cannot grant visual review."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[3]
PAPER = ROOT / 'papers/draft-03'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def require(ok, message):
    if not ok:
        raise ValueError(message)

def main():
    qa = json.loads((PAPER / 'pdf-qa.json').read_text())
    registry = json.loads((PAPER / 'registry/hnm-registry.json').read_text())
    review = ROOT / 'research/round30/editorial/pdf-review.md'
    require(qa.get('status') == 'passed' and qa.get('visual_review') == 'passed', 'Actual image review is required')
    require(review.exists(), 'Current written image-review record is required')
    require(qa.get('all_page_geometry_checked') and not qa['geometry']['out_of_media_text'], 'Unresolved page geometry')
    require(qa.get('references_resolved') and not qa.get('overfull_warnings'), 'Unresolved TeX checks')
    require(set(qa['rendered_pages']) <= set(qa['inspected_pages']), 'Every selected rendered page must have been visually inspected')
    require(qa['pdf_sha256'] == sha(PAPER / 'main.pdf'), 'PDF changed after review')
    for name, digest in qa['source_inventory'].items():
        require(sha(ROOT / name) == digest, f'PDF source changed: {name}')
    files = [path for path in PAPER.rglob('*') if path.is_file() and path.name not in {'artifact-manifest.json', 'build-log.txt'}
             and '__pycache__' not in path.parts and 'qa-render' not in path.parts and path.suffix != '.pyc']
    manifest = {
        'schema': 'hnm-integrated-draft03-v1', 'human_author': registry['human_author'],
        'scope': 'Complete integrated manuscript plus exactly three reviewed Round30 investigations; inherited audit records retain historical scope. Hashes establish provenance, not mathematical correctness.',
        'pdf_sha256': qa['pdf_sha256'], 'pages': qa['page_count'],
        'contributions': len(registry['contributions']), 'equation_aliases': len(registry['equations']),
        'statement_aliases': len(registry['statements']), 'quantity_aliases': len(registry['quantities']),
        'new_axioms': registry['new_axioms_count'],
        'review_record': str(review.relative_to(ROOT)), 'review_sha256': sha(review),
        'references_resolved': qa['references_resolved'], 'overfull_warnings': qa['overfull_warnings'],
        'all_page_geometry_checked': qa['all_page_geometry_checked'],
        'rendered_pages': qa['rendered_pages'], 'inspected_pages': qa['inspected_pages'],
        'full_size_inspected_pages': qa['full_size_inspected_pages'], 'visual_coverage': qa['coverage'],
        'source_inventory': qa['source_inventory'],
        'sha256': {str(path.relative_to(ROOT)): sha(path) for path in sorted(files)},
    }
    (PAPER / 'artifact-manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({'pdf_sha256': manifest['pdf_sha256'], 'pages': manifest['pages'], 'bound_files': len(files)}))

if __name__ == '__main__':
    main()
