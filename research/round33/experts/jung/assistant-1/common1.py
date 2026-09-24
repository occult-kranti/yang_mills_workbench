#!/usr/bin/env python3
"""Shared helpers for the Jung/Pauli lens, Round33 sub-round 1, assistant-1 scripts.

Standing (calling task; `research/round33/experts/jung/loop2-response.md` section 3,
"What this lens's research assistant should test after sub-round 1"): these are
audits over BA1/BA2's frozen evidence. **They count zero research loops.** Nothing
here is a producer, a contract, a gate or a skeptical review, and nothing computed
here is read back into any of those -- BA1 and BA2 are already `accepted_within_scope`
per their own gates (`research/round33/advisor/ba1-gate.json`,
`research/round33/advisor/ba2-gate.json`); only those gates and the skeptic's reviews
ever decided that. Human project author: Hruday N M (BUNZEEY); AI-assisted.

Standard library only (`json`, `re`, `hashlib`, `pathlib`). Run every script with
`python3 -B`. Does **not** import `forward/*/check.py`, `reverse/*/check.py`, any
other producer/skeptic module, or any earlier round's assistant scripts -- only
`research/round33/tools/phrase_scan.py`, named explicitly in the calling task as
importable ("you may import research/round33/tools/phrase_scan.py as a library"),
which is itself infrastructure (computes no scientific result; rule R6 of the
Round32 closing panel) rather than a producer or skeptic module.

Mirrors the file layout and self-contained-closure discipline of
`research/round32/experts/jung/assistant-5/` (`common5.py` + three per-task scripts
+ merged `results.json`), adapted to Round33's single-sub-round, two-loop (BA1/BA2)
scope named by the calling task, rather than Round32's ten-investigation, whole-round
scope assistant-5 covered.
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]  # assistant-1 -> jung -> experts -> round33 -> research -> ROOT
R33 = ROOT / 'research' / 'round33'
CONTRACTS = R33 / 'contracts'
ADVISOR = R33 / 'advisor'
SKEPTIC = R33 / 'skeptic'
FORWARD = R33 / 'forward'
REVERSE = R33 / 'reverse'
TOOLS = R33 / 'tools'

PLAN_JSON = ADVISOR / 'plan.json'
ADMISSION_SPEC = ADVISOR / 'admission-spec.json'

LOOPS = ('ba1', 'ba2')

CONTRACT_PATHS = {loop: CONTRACTS / (loop + '.json') for loop in LOOPS}
GATE_PATHS = {loop: ADVISOR / (loop + '-gate.json') for loop in LOOPS}
SKEPTIC_MD_PATHS = {loop: SKEPTIC / (loop + '.md') for loop in LOOPS}
SKEPTIC_JSON_PATHS = {loop: SKEPTIC / (loop + '.json') for loop in LOOPS}
FORWARD_REPORT_PATHS = {loop: FORWARD / loop / 'report.md' for loop in LOOPS}
REVERSE_REPORT_PATHS = {loop: REVERSE / loop / 'report.md' for loop in LOOPS}
FORWARD_RESULTS_PATHS = {loop: FORWARD / loop / 'output' / 'results.json' for loop in LOOPS}
REVERSE_RESULTS_PATHS = {loop: REVERSE / loop / 'output' / 'results.json' for loop in LOOPS}

# Every text artifact the calling task's item (a) names for the phrase-scan dry run:
# "every BA1/BA2 producer report, results.json, skeptic review (...) and gate (...)".
# Both producers exist for both loops (BA1 and BA2 are both `direction: "paired"`),
# so this is eight files per loop, sixteen total.
SCAN_TARGETS = {}
for _loop in LOOPS:
    SCAN_TARGETS[_loop] = {
        'forward_report': FORWARD_REPORT_PATHS[_loop],
        'reverse_report': REVERSE_REPORT_PATHS[_loop],
        'forward_results': FORWARD_RESULTS_PATHS[_loop],
        'reverse_results': REVERSE_RESULTS_PATHS[_loop],
        'skeptic_md': SKEPTIC_MD_PATHS[_loop],
        'skeptic_json': SKEPTIC_JSON_PATHS[_loop],
        'gate': GATE_PATHS[_loop],
    }


def load_json(path):
    return json.loads(Path(path).read_bytes().decode('utf-8'))


def load_text(path):
    return Path(path).read_text(encoding='utf-8', errors='replace')


def load_plan():
    return load_json(PLAN_JSON)


def load_contract(loop):
    return load_json(CONTRACT_PATHS[loop])


def load_gate(loop):
    return load_json(GATE_PATHS[loop])


def load_skeptic_json(loop):
    return load_json(SKEPTIC_JSON_PATHS[loop])


def merge_results(path, key, payload):
    """Read-modify-write results.json, keeping the other scripts' sections (the
    same convention as research/round32/experts/jung/assistant-5/common5.py)."""
    data = {}
    if Path(path).exists():
        try:
            data = load_json(path)
        except Exception:
            data = {}
    data[key] = payload
    Path(path).write_text(json.dumps(data, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    return data


# ---------------------------------------------------------------------------
# Generic recursive JSON walkers (unchanged pattern from assistant-5's common5.py).
# ---------------------------------------------------------------------------
def walk_json_items(obj, path=''):
    """Yields (json_path, key, value) for every dict entry anywhere in obj."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = (path + '.' + k) if path else k
            yield (p, k, v)
            yield from walk_json_items(v, p)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            p = path + '[%d]' % i
            yield from walk_json_items(v, p)


def walk_all_strings(obj, path=''):
    """Yields (json_path, string_value) for every plain string anywhere in obj."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk_all_strings(v, (path + '.' + k) if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_all_strings(v, path + '[%d]' % i)
    elif isinstance(obj, str):
        yield path, obj


def find_key_occurrences(obj, key_name):
    """All (json_path, value) where a dict key equals key_name, anywhere in obj."""
    return [(p, v) for (p, k, v) in walk_json_items(obj) if k == key_name]


# ---------------------------------------------------------------------------
# Sentence/clause helpers shared by the "unique" and "rate" hand-audits (task
# items (b) and (c)), built on the same clause-splitting rule
# tools/phrase_scan.py uses for its own whole-sentence, negation-aware scan, so
# "same clause" means the same thing here as it does to the real R6 scanner.
# ---------------------------------------------------------------------------
CLAUSE_SPLIT_RE = re.compile(r'(?<=[.!?])\s+|;\s*|:\s+')


def normalize(text):
    return re.sub(r'\s+', ' ', str(text)).strip()


def clauses(text):
    return [c for c in CLAUSE_SPLIT_RE.split(text) if c.strip()]


def clause_containing(text, pos):
    """The single clause (phrase_scan.py's own clause-splitting rule) that
    contains character offset `pos` in the *normalized* text `text`."""
    for c in clauses(text):
        start = text.find(c)
        if start != -1 and start <= pos < start + len(c):
            return c
    # Fallback: pos not resolvable against a clause boundary (should not
    # happen for a match `re.finditer` found inside `text` itself) -- return
    # a wide window instead of raising, so a caller still gets *something* to
    # classify by hand.
    return text[max(0, pos - 120):pos + 120]
