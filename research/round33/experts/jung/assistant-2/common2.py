#!/usr/bin/env python3
"""Shared helpers for the Jung/Pauli lens, Round33 sub-round 2, assistant-2 scripts.

Standing (calling task: the coordinating agent's assignment for "Round33 sub-round
2 of the SU(2) lattice gauge theory workbench, JUNG/PAULI lens assistant"): these
are audits over the four frozen BB1/BB2 producer packets, run before any BB1/BB2
gate exists. **They count zero research loops.** Nothing here is a producer, a
contract, a gate or a skeptical review, and nothing computed here is read back
into any of those or used as admission evidence -- BB1 and BB2 are not yet gated
(no `research/round33/advisor/bb1-gate.json` or `bb2-gate.json` exists at the time
this package was written); only a future advisor gate and the skeptic's own review
ever decide BB1/BB2's outcome. Human project author: Hruday N M (BUNZEEY);
AI-assisted.

Standard library only (`json`, `re`, `pathlib`). Run every script with `python3
-B`. Does **not** import `forward/*/check.py`, `reverse/*/check.py`, any other
producer/skeptic module, or any earlier round's or sub-round's assistant scripts
-- only `research/round33/tools/phrase_scan.py`, named explicitly in the calling
task as importable ("you may import research/round33/tools/phrase_scan.py as a
library"), which is itself infrastructure (computes no scientific result; rule R6
of the Round32 closing panel) rather than a producer or skeptic module.

Mirrors the file layout and self-contained-closure discipline of
`research/round33/experts/jung/assistant-1/` (`common1.py` + per-task scripts +
merged `results.json`), adapted to sub-round 2's two loops (BB1/BB2) and the
calling task's own, different item list (phrase/rate audit, template+gate-field
audit including BB2's before/after-discharge blocks, vocabulary mirror including
route/assembly/dynamics_level, and a new hypotheses map -- BB1/BB2 have no gate or
skeptic review yet, so this package's input scope is narrower than assistant-1's:
only the two contracts, the four report.md/results.json packets, plan.json and
`skeptic/bb2-replays.json`, exactly as the calling task names).
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]  # assistant-2 -> jung -> experts -> round33 -> research -> ROOT
R33 = ROOT / 'research' / 'round33'
CONTRACTS = R33 / 'contracts'
ADVISOR = R33 / 'advisor'
SKEPTIC = R33 / 'skeptic'
FORWARD = R33 / 'forward'
REVERSE = R33 / 'reverse'
TOOLS = R33 / 'tools'

PLAN_JSON = ADVISOR / 'plan.json'
BB2_REPLAYS_JSON = SKEPTIC / 'bb2-replays.json'

LOOPS = ('bb1', 'bb2')

CONTRACT_PATHS = {loop: CONTRACTS / (loop + '.json') for loop in LOOPS}
FORWARD_REPORT_PATHS = {loop: FORWARD / loop / 'report.md' for loop in LOOPS}
REVERSE_REPORT_PATHS = {loop: REVERSE / loop / 'report.md' for loop in LOOPS}
FORWARD_RESULTS_PATHS = {loop: FORWARD / loop / 'output' / 'results.json' for loop in LOOPS}
REVERSE_RESULTS_PATHS = {loop: REVERSE / loop / 'output' / 'results.json' for loop in LOOPS}

# Every text artifact the calling task names for the phrase-scan dry run: "each
# of the four reports and ... every string field of each results.json" -- the
# report is scanned as one text blob (as record_gate.py / phrase_scan.py would
# scan a report), the results.json is scanned string field by string field
# (walk_all_strings), since a "clause" inside a JSON string is what the calling
# task's own phrasing ("every string field") asks for, not the raw JSON text
# (braces/quotes/keys would otherwise pollute the clause split).
SCAN_TARGETS = {}
for _loop in LOOPS:
    SCAN_TARGETS[_loop] = {
        'forward_report': FORWARD_REPORT_PATHS[_loop],
        'reverse_report': REVERSE_REPORT_PATHS[_loop],
        'forward_results': FORWARD_RESULTS_PATHS[_loop],
        'reverse_results': REVERSE_RESULTS_PATHS[_loop],
    }


def load_json(path):
    return json.loads(Path(path).read_bytes().decode('utf-8'))


def load_text(path):
    return Path(path).read_text(encoding='utf-8', errors='replace')


def load_plan():
    return load_json(PLAN_JSON)


def load_contract(loop):
    return load_json(CONTRACT_PATHS[loop])


def load_bb2_replays():
    return load_json(BB2_REPLAYS_JSON)


def merge_results(path, key, payload):
    """Read-modify-write results.json, keeping the other scripts' sections (the
    same convention as research/round33/experts/jung/assistant-1/common1.py and,
    before it, research/round32/experts/jung/assistant-5/common5.py)."""
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
# Generic recursive JSON walkers (unchanged pattern from assistant-1's common1.py
# and, before it, assistant-5's common5.py).
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


def dicts_with_key(obj, key_name, path=''):
    """Yields (json_path, dict) for every dict anywhere in obj that itself has
    a member named key_name (so its sibling keys can be inspected)."""
    if isinstance(obj, dict):
        if key_name in obj:
            yield (path, obj)
        for k, v in obj.items():
            yield from dicts_with_key(v, key_name, (path + '.' + k) if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from dicts_with_key(v, key_name, path + '[%d]' % i)


# ---------------------------------------------------------------------------
# Clause helpers shared by the phrase/rate audits, built on the same
# clause-splitting rule tools/phrase_scan.py uses for its own whole-sentence,
# negation-aware scan (sentence end, semicolon or colon), so "same clause" means
# the same thing here as it does to the real R6 scanner and to assistant-1's own
# audit before it.
# ---------------------------------------------------------------------------
CLAUSE_SPLIT_RE = re.compile(r'(?<=[.!?])\s+|;\s*|:\s+')


def normalize(text):
    return re.sub(r'\s+', ' ', str(text)).strip()


def clauses(text):
    return [c for c in CLAUSE_SPLIT_RE.split(text) if c.strip()]
