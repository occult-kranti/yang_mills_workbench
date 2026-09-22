#!/usr/bin/env python3
"""Source-bound Draft03 build. A new build always invalidates visual review."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

def require(condition, message):
    if not condition:
        raise ValueError(message)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def group(text, start):
    require(text[start] == '{', 'Expected a TeX group')
    depth = 0
    for i in range(start, len(text)):
        if text[i] in '{}':
            backslashes, j = 0, i - 1
            while j >= 0 and text[j] == '\\':
                backslashes += 1
                j -= 1
            if backslashes % 2:
                continue
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:
                return text[start + 1:i], i + 1
    raise ValueError('Unbalanced LaTeX auxiliary group')

def labels(aux):
    numbers, pages = {}, {}
    for match in re.finditer(r'\\newlabel\{([^}]+)\}\{', aux):
        payload, _ = group(aux, match.end() - 1)
        if not payload.startswith('{'):
            continue
        value, pos = group(payload, 0)
        while value.startswith('{'):
            inner, end = group(value, 0)
            if end != len(value):
                break
            value = inner
        numbers[match[1]] = value
        if pos < len(payload) and payload[pos] == '{':
            page, _ = group(payload, pos)
            if page.isdigit():
                pages[match[1]] = int(page)
    return numbers, pages

def validate_sources():
    manifest = HERE / 'round30-inputs.json'
    require(manifest.exists(), 'Final Round30 integration is required.')
    sources = json.loads(manifest.read_text())
    require(len(sources['admitted_loops']) == 3, 'Exactly three reviewed loops required.')
    for name, digest in sources['sha256'].items():
        path = ROOT / name
        require(path.exists() and sha(path) == digest, f'Editorial source mismatch: {name}')
    for rnd, expected in [('round29', 10), ('round30', 3)]:
        findings = json.loads((ROOT / f'research/{rnd}/advisor/findings.json').read_text())
        require(len(findings['loops']) == expected, f'Wrong {rnd} investigation count')
        for item in findings['loops']:
            evidence = item['evidence'] if isinstance(item['evidence'], list) else [item['evidence']]
            gates = [name for name in evidence if name.endswith('-gate.json')]
            require(len(gates) == 1, f'Expected one reviewed gate for {item["id"]}')
            gate_path = ROOT / gates[0]
            gate = json.loads(gate_path.read_text())
            require(gate.get('bindings'), f'Missing bindings {gate_path}')
            for name, digest in gate['bindings'].items():
                path = ROOT / name
                require(path.exists() and sha(path) == digest, f'Gate source mismatch: {name}')
    require('integration in progress' not in (HERE / 'sections/round30.tex').read_text(), 'Unfinished editorial scaffold')

def source_inventory():
    paths = sorted(list(HERE.rglob('*.tex')) + list(HERE.rglob('*.bib')) +
                   [p for p in (HERE / 'figures').rglob('*') if p.is_file()] +
                   [p for p in (HERE / 'addenda').rglob('*') if p.is_file() and p.suffix in {'.png', '.pdf', '.jpg', '.jpeg', '.svg'}])
    return {str(p.relative_to(ROOT)): sha(p) for p in paths}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--draft', action='store_true', help='Editorial build; never a publication receipt')
    args = parser.parse_args()
    # Even editorial mode cannot synthesize missing scientific admissions.
    validate_sources()
    registry_path = HERE / 'registry/hnm-registry.json'
    registry = json.loads(registry_path.read_text())
    require(registry['human_author'] == 'Hruday N M (BUNZEEY)', 'Incorrect author')
    require(registry.get('new_axioms_count') == 0, 'Unexpected new axiom')
    with tempfile.TemporaryDirectory(prefix='hnm-draft03-') as temp:
        work = Path(temp) / 'paper'
        shutil.copytree(HERE, work, ignore=shutil.ignore_patterns('main.pdf', 'main.bbl', '__pycache__', '*.pyc', 'artifact-manifest.json', 'pdf-qa.json', 'qa-render', 'build-log.txt'))
        environment = dict(os.environ)
        environment['SOURCE_DATE_EPOCH'] = '1790035200'
        environment['FORCE_SOURCE_DATE'] = '1'
        process = subprocess.run(['latexmk', '-pdf', '-bibtex', '-interaction=nonstopmode', '-halt-on-error', 'main.tex'], cwd=work, capture_output=True, text=True, env=environment)
        (HERE / 'build-log.txt').write_text(process.stdout + process.stderr)
        if process.returncode:
            raise RuntimeError((process.stdout + process.stderr)[-7000:])
        log = (work / 'main.log').read_text()
        unresolved = [line for line in log.splitlines() if ('undefined' in line.lower() and ('reference' in line.lower() or 'citation' in line.lower())) or 'multiply defined' in line]
        require(not unresolved, f'Unresolved or duplicated references: {unresolved}')
        overfull = [line for line in log.splitlines() if 'Overfull' in line]
        require(not overfull, f'Fix overflow before releasing: {overfull}')
        numbers, pages = labels((work / 'main.aux').read_text())
        for equation in registry['equations']:
            if equation.get('label_kind') == 'source_equation':
                continue
            locator = numbers.get(equation['legacy_label'])
            require(locator, f'Missing equation label {equation["legacy_label"]}')
            require(not any(c in locator for c in '{}'), f'Malformed locator {locator}')
            equation['printed_locator'] = locator
            equation['printed_page'] = pages.get(equation['legacy_label'])
        registry_path.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + '\n')
        shutil.copy2(work / 'main.pdf', HERE / 'main.pdf')
        shutil.copy2(work / 'main.bbl', HERE / 'main.bbl')
        current_labels = {key: value for key, value in pages.items() if key.startswith(('r30:', 'stmt:AT', 'sec:r30', 'sec:round30'))}
        (HERE / 'build-pages.json').write_text(json.dumps({'current_labels': current_labels, 'all_labels': pages}, indent=2) + '\n')
        qa = dict(schema='hnm-draft03-qa-v1', status='rendering_required', mode='editorial_draft' if args.draft else 'final_source_build',
                  pdf_sha256=sha(HERE / 'main.pdf'), references_resolved=True, overfull_warnings=overfull,
                  source_inventory=source_inventory(), contributions=len(registry['contributions']), equation_aliases=len(registry['equations']),
                  quantity_aliases=len(registry['quantities']), statement_aliases=len(registry['statements']), human_author=registry['human_author'],
                  rendered_pages=[], inspected_pages=[], all_page_geometry_checked=False,
                  coverage='Current build resets visual review. Carried historical audit files do not certify this PDF.')
        (HERE / 'pdf-qa.json').write_text(json.dumps(qa, indent=2) + '\n')
        print(json.dumps({key: qa[key] for key in ['status', 'pdf_sha256', 'references_resolved', 'overfull_warnings', 'contributions', 'equation_aliases']}))

if __name__ == '__main__':
    main()
