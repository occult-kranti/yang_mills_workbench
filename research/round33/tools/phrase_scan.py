#!/usr/bin/env python3
"""Round33 forbidden-phrase scanner (rule R6 of the Round32 closing panel).

The contract's mandatory_sentence_template is one quoted literal and is removed
before scanning. Every other clause (split at sentence ends, semicolons and
colons) is scanned whole-word and case-insensitively; a hit is affirmative only
when its clause carries no explicit negation frame. Infrastructure only; it
computes no scientific result.

  python3 -B research/round33/tools/phrase_scan.py <contract.json> <text file>...
"""
import json
import re
import sys
from pathlib import Path

ROUND_FORBIDDEN = [
    'the AQ state', 'the infinite-volume ground state', 'uniqueness of the infinite-volume ground state',
    'the continuum limit exists', 'fraction of the problem', 'confirms the Z^3 value', 'predicts',
    'solves the mass gap', 'solved the mass gap', 'proves the mass gap',
    'unique ground state', 'the unique ground state', 'a unique limit', 'the unique limit',
    'unique infinite-volume', 'uniqueness of the ground state', 'uniquely determines the ground state',
    'the thermodynamic limit', 'correlation length',
]
NEGATION = re.compile(r"\b(not|never|no|nor|neither|without|excludes?|excluded|exclusion|forbidden|"
                      r"cannot|does not|is not|are not|nothing|none)\b", re.I)


def normalize(text):
    return re.sub(r'\s+', ' ', str(text)).strip()


def clauses(text):
    return [c for c in re.split(r'(?<=[.!?])\s+|;\s*|:\s+', text) if c.strip()]


def scan(text, forbidden, template=None):
    body = normalize(text)
    if template:
        body = body.replace(normalize(template), ' ')
    hits = []
    for clause in clauses(body):
        for phrase in forbidden:
            if re.search(r'(?<![\w])' + re.escape(phrase) + r'(?![\w])', clause, re.I):
                hits.append({'phrase': phrase, 'clause': clause[:240], 'negated': bool(NEGATION.search(clause))})
    return hits


def affirmative(hits):
    return [h for h in hits if not h['negated']]


def contract_terms(contract):
    pre = contract.get('preregistration', {})
    return ROUND_FORBIDDEN + list(pre.get('forbidden_phrasings', [])), pre.get('mandatory_sentence_template')


def main():
    contract = json.loads(Path(sys.argv[1]).read_text())
    forbidden, template = contract_terms(contract)
    out = {}
    for name in sys.argv[2:]:
        out[name] = affirmative(scan(Path(name).read_text(errors='replace'), forbidden, template))
    print(json.dumps(out, indent=2))
    if any(out.values()):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
