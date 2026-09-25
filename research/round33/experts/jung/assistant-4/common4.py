#!/usr/bin/env python3
"""Shared helpers for the Jung/Pauli lens, Round33 applications stage, assistant-4
scripts.

Standing (calling task: the coordinating agent's assignment for "Round33
applications stage of the SU(2) lattice gauge theory workbench, JUNG/PAULI lens
assistant-4"): these are audits over the frozen BD1/BD2 producer packets, their
gates, their skeptical reviews, and the round-level `advisor/findings.json` and
`advisor/roadmap.json`. **They count zero research loops.** Nothing here is a
producer, a contract, a gate or a skeptical review; nothing computed here is
read back into any contract, gate or skeptical review; nothing here decides
whether BD1/BD2 are accepted (they already are: both gates are
`accepted_within_scope`, read here only as frozen text). Human project author:
Hruday N M (BUNZEEY); AI-assisted.

Standard library only (`json`, `re`, `hashlib`, `pathlib`). Run every script
with `python3 -B`. Does **not** import `forward/*/check.py`, `reverse/*/check.py`,
any other producer/skeptic module, or any other assistant's scripts -- only
`research/round33/tools/phrase_scan.py`, named explicitly in the calling task
as importable ("you may import research/round33/tools/phrase_scan.py"), which
is itself infrastructure (computes no scientific result; rule R6 of the
Round32 closing panel) rather than a producer or skeptic module.

Mirrors the file layout and self-contained-closure discipline of
`research/round33/experts/jung/assistant-3/` (sub-round 3), adapted to this
package's own, different task list (a phrase scan of the BD1/BD2 packets plus
the round-level findings/roadmap text, re-applying the sub-round-3
vocabulary-gap and heading-list-severance audits to this new text, and a new
transfer-language audit; a template-and-gate-field audit against the plan
vocabulary; an applications-ledger audit of `findings.json#/applications`).

Path layout
-----------
`research/round33/experts/jung/assistant-4/common4.py` -> parents[4] is the
repo root (assistant-4 -> jung -> experts -> round33 -> research -> ROOT).
"""
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]  # assistant-4 -> jung -> experts -> round33 -> research -> ROOT
R33 = ROOT / 'research' / 'round33'
CONTRACTS = R33 / 'contracts'
ADVISOR = R33 / 'advisor'
SKEPTIC = R33 / 'skeptic'
FORWARD = R33 / 'forward'
REVERSE = R33 / 'reverse'
TOOLS = R33 / 'tools'

PLAN_JSON = ADVISOR / 'plan.json'
FINDINGS_JSON = ADVISOR / 'findings.json'
ROADMAP_JSON = ADVISOR / 'roadmap.json'

# The two loops this assistant's calling task is about.
LOOPS = ('bd1', 'bd2')

CONTRACT_PATHS = {loop: CONTRACTS / (loop + '.json') for loop in LOOPS}
GATE_PATHS = {loop: ADVISOR / (loop + '-gate.json') for loop in LOOPS}
REVIEW_JSON_PATHS = {loop: SKEPTIC / (loop + '.json') for loop in LOOPS}
REVIEW_MD_PATHS = {loop: SKEPTIC / (loop + '.md') for loop in LOOPS}
FORWARD_REPORT_PATHS = {loop: FORWARD / loop / 'report.md' for loop in LOOPS}
# Only bd1 has a reverse producer (bd1 direction: paired); bd2 is single+skeptic
# (direction "single+skeptic"), so no research/round33/reverse/bd2 exists.
REVERSE_REPORT_PATHS = {
    loop: REVERSE / loop / 'report.md'
    for loop in LOOPS
    if (REVERSE / loop / 'report.md').exists()
}
FORWARD_RESULTS_PATHS = {loop: FORWARD / loop / 'output' / 'results.json' for loop in LOOPS}


def load_json(path):
    return json.loads(Path(path).read_bytes().decode('utf-8'))


def load_text(path):
    return Path(path).read_text(encoding='utf-8', errors='replace')


def load_plan():
    return load_json(PLAN_JSON)


def load_findings():
    return load_json(FINDINGS_JSON)


def load_roadmap():
    return load_json(ROADMAP_JSON)


def load_contract(loop):
    return load_json(CONTRACT_PATHS[loop])


def load_gate(loop):
    return load_json(GATE_PATHS[loop])


def load_review(loop):
    return load_json(REVIEW_JSON_PATHS[loop])


def rel(path):
    return str(Path(path).resolve().relative_to(ROOT))


def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def merge_results(path, key, payload):
    """Read-modify-write results.json, keeping the other scripts' sections (the
    same convention as assistant-1's common1.py, assistant-2's common2.py and
    assistant-3's common3.py before it)."""
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
# Generic recursive JSON walkers (unchanged pattern from assistant-1's,
# assistant-2's and assistant-3's common modules).
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
# Clause helpers shared by the phrase audits, built on the same clause-
# splitting rule tools/phrase_scan.py uses for its own whole-sentence,
# negation-aware scan (sentence end, semicolon or colon), so "same clause"
# means the same thing here as it does to the real R6 scanner and to
# assistant-1's, assistant-2's and assistant-3's own audits before it.
# ---------------------------------------------------------------------------
CLAUSE_SPLIT_RE = re.compile(r'(?<=[.!?])\s+|;\s*|:\s+')


def normalize(text):
    return re.sub(r'\s+', ' ', str(text)).strip()


def clauses(text):
    return [c for c in CLAUSE_SPLIT_RE.split(text) if c.strip()]
