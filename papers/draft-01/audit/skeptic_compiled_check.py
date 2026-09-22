"""Final PDF representation checks after the written mathematical review.

These checks bind the final presentation. They add no mathematical stress tests
to the separately recorded 158-check total and do not perform visual layout QA.
"""
from pathlib import Path
from collections import Counter
import argparse
import hashlib
import json
import re
import subprocess

B = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads((B / path).read_text())


parser = argparse.ArgumentParser()
parser.add_argument('--pdf-sha256', required=True)
args = parser.parse_args()
checks = []


def require(name, condition, detail):
    if not condition:
        raise ValueError((name, detail))
    checks.append({'name': name, 'result': 'pass', 'detail': detail})


pdf = B / 'main.pdf'
text_path = B / 'output/final-paper.txt'
require('specified_final_pdf', sha(pdf) == args.pdf_sha256, sha(pdf))
extracted = subprocess.run(['pdftotext', '-layout', str(pdf), '-'],
                           check=True, capture_output=True).stdout
require('independent_final_text_extraction', extracted == text_path.read_bytes(),
        'Fresh pdftotext -layout bytes equal the integrator extraction.')
text = extracted.decode('utf-8')
pdfinfo = subprocess.run(['pdfinfo', str(pdf)], check=True,
                         capture_output=True, text=True).stdout
pages = int(re.search(r'^Pages:\s+(\d+)', pdfinfo, re.M).group(1))
require('page_count', pages == 92 and text.count('\f') == 92, pages)

review = read('audit/skeptic-review.json')
catalog = read('audit/contribution-catalog.json')
history = read('audit/history-ledger.json')
require('source_review_status',
        review['verdict'] == 'accepted_within_declared_scope_for_author_review'
        and review['blocking_issues'] == [], review['verdict'])
source_mismatch = [p for p, h in review['manuscript_sha256'].items()
                   if sha(B / p) != h]
require('final_review_source_bindings', not source_mismatch, source_mismatch)
require('catalog_input_bindings',
        all(sha(B / p) == h for p, h in catalog['input_sha256'].items()),
        'Final early, middle and recent author ledgers match the compiled catalog.')
review_ids = {x['id'] for x in review['contributions']}
catalog_ids = {x['id'] for x in catalog['contributions']}
require('catalog_review_identity', review_ids == catalog_ids and len(review_ids) == 114,
        '17 early groups + 62 middle entries + 35 recent groups = 114.')
missing = [i for i in sorted(catalog_ids)
           if not re.search(r'(?<![A-Za-z0-9])' + re.escape(i) + r'\*\*', text)]
require('all_contribution_ids_rendered', not missing, {'count': 114, 'missing': missing})

history_head = list(re.finditer(r'^B\s+Complete historical record\s*$', text, re.M))[-1]
history_text = text[history_head.end():]
history_text = history_text[:re.search(r'^C\s+Reproduction and manuscript build',
                                      history_text, re.M).start()]
# R1 and R2 are also two printed loop identifiers within Round22. They are
# excluded here; the independently surviving historical rounds are R3--R26.
rounds = [int(n) for n in re.findall(r'^R(\d+)\s+', history_text, re.M)
          if 3 <= int(n) <= 26]
expected_rounds = Counter(x['round'] for x in history['entries'])
require('complete_history_rows_by_round', Counter(rounds) == expected_rounds
        and len(rounds) == 121,
        {'records': len(rounds), 'counts_by_round': dict(sorted(Counter(rounds).items()))})
require('history_scope_rendered',
        'not\na list of 121 new discoveries' in history_text
        and 'does not claim that\nevery old production simulation was rerun' in history_text,
        'Historical inclusion does not assert discovery count or fresh production replay.')

bad_tokens = [(m.start(), m.group()) for m in
              re.finditer(r'\?\?|\bundefined\b|qquad|mathcal|\bTODO\b|PLACEHOLDER|frac\{', text)]
require('no_unresolved_or_literal_tex_markers', not bad_tokens, bad_tokens)
bbl = (B / 'main.bbl').read_text()
bib_keys = re.findall(r'\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}', bbl)
require('bibliography_count', len(bib_keys) == 24 and len(set(bib_keys)) == 24
        and all(re.search(r'^\s*\[' + str(i) + r'\]', text, re.M) for i in range(1, 25)),
        '24 unique bibliography records render with numeric labels 1 through 24.')
aux = (B / 'main.aux').read_text()
unresolved_equations = [x['label'] for x in review['equations']
                       if r'\newlabel{' + x['label'] + '}' not in aux]
require('all_reviewed_equation_labels_resolve', not unresolved_equations,
        {'reviewed_displayed_labels': len(review['equations']),
         'missing': unresolved_equations})
compact = re.sub(r'\s+', ' ', text)
require('critical_scope_repairs_rendered',
        all(p in compact for p in [
            'complete strict low-electric-energy sector',
            'not a complete ambient energy cutoff',
            'C > 0, γ ≥ 0',
            '0 < z ≤ 10−6',
            'not external peer review or formal verification',
            '--input-vector PATH']),
        'P21/P293 distinction, nonnegative time exponent, small-z endpoint range, '
        'review status and executable argument spacing are visible.')
require('test_count_and_mode_scope_rendered',
        '194 checks' in compact and '158 checks (90 general, 12 early, 33 middle, and 23 recent)'
        in compact and '15 additional checks' in compact
        and 'not counts of independently proved theorems' in compact,
        '194 calculator, 158 skeptic, and 15 HTML checks are distinct counts.')

bindings = ['main.pdf', 'output/final-paper.txt', 'main.tex', 'main.bbl', 'main.aux',
            'sections/reproduction.tex', 'sections/contribution-appendix.tex',
            'sections/history-appendix.tex', 'audit/contribution-catalog.json',
            'audit/skeptic-review.json', 'audit/skeptic-review.md',
            'audit/skeptic_finalize.py', 'audit/skeptic_compiled_check.py']
receipt = {
    'schema': 'ym-manuscript-skeptic-compiled-v1',
    'verdict': 'accepted_within_declared_scope_for_author_review',
    'blocking_issues': [],
    'reviewer': 'Independent skeptic model agent; not external peer review.',
    'pages': pages,
    'scope': 'Final representation consistency following the separately recorded '
             'written mathematical review. Selected critical compiled passages, '
             'the catalog, history appendix, bibliography and reproduction '
             'instructions were inspected. No claim of a fresh word-by-word '
             'mathematical rereview of the full 92-page extraction is made.',
    'checks': checks,
    'presentation_consistency_check_count': len(checks),
    'fresh_mathematical_stress_checks': 158,
    'additional_mathematical_stress_checks_in_this_receipt': 0,
    'visual_layout_qa': 'Owned and reported separately by the integrator; this '
                        'receipt does not certify every page visually.',
    'sha256': {p: sha(B / p) for p in bindings},
    'remaining_limits': review['unverified'],
}
(B / 'audit/skeptic-compiled-review.json').write_text(json.dumps(receipt, indent=2) + '\n')
(B / 'audit/skeptic-compiled-review.md').write_text(
    '# Final compiled-text consistency receipt\n\n'
    'The final 92-page manuscript is accepted for author review within the '
    'mathematical scope of `skeptic-review.json`. No blocking issue remains.\n\n'
    f'PDF SHA-256: `{sha(pdf)}`.\n\n'
    'A fresh text extraction matches the integrator extraction byte for byte. '
    'All 114 contribution identifiers, all 137 reviewed displayed-equation labels, '
    '121 history rows with the correct per-round counts, and 24 bibliography '
    'records are present and resolved. The endpoint domain, N2 time exponent, '
    'P21/P293 distinction, test counts, and command argument spacing remain '
    'correct in the compiled text. The machine-readable receipt binds the final '
    'PDF, text, catalog, source audit and relevant compiled inputs.\n\n'
    'This is a representation check, separate from the 158 exact mathematical '
    'stress checks. It is neither a new research loop nor external peer review. '
    'The integrator owns visual layout QA. Historical production, priority and '
    'physical-limit limitations remain those stated in the mathematical audit.\n')
print(json.dumps({'verdict': receipt['verdict'], 'pages': pages,
                  'presentation_checks': len(checks), 'pdf_sha256': sha(pdf)}))
