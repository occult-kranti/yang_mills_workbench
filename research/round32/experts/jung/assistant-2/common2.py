#!/usr/bin/env python3
"""Shared helpers for the Jung/Pauli lens, Round32 sub-round 2, assistant-2 scripts.

Standing (calling task; `update-1.md` section 5): these are pre-registration audits
and tests for the lens, run after AW1/AW2 and before AX1/AX2/AY1/AY2/AZ1/AZ2 leave
`status: draft`. They count zero research loops. Nothing here is a producer, a
contract, a gate or a skeptical review, and nothing computed here is read back into
any of those. Human project author: Hruday N M (BUNZEEY); AI-assisted.

Every admission-relevant Boolean is decided in exact ``fractions.Fraction``
arithmetic; decimal strings are truncated, labelled previews only and never decide
anything. This module re-implements the small set of generic utilities
`research/round32/experts/jung/assistant-1/common.py` already used for sub-round 1
(``AuditError``, ``require``, ``expect_rejected``, ``load_json``, ``rat``, ``s``,
``merge_results``) so assistant-2 stays a self-contained closure, and generalises
assistant-1's `preregistration_audit.py` structural checks (per the calling task:
"reuse preregistration_audit.py logic") from AV1/AV2-only to any contract in this
round. It does not import `forward/*/check.py`, `reverse/*/check.py` or any other
producer/skeptic module, and it does not import assistant-1's scripts (only reads
its own inputs by path), per the same isolation discipline assistant-1 documents.

Usage: each sibling script imports this module (``import common2 as K``) after
adding this directory to ``sys.path``; run every script with ``python3 -B``.
"""
import json
import re
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]  # assistant-2 -> jung -> experts -> round32 -> research -> ROOT
RESEARCH = ROOT / 'research' / 'round32'
CONTRACTS = RESEARCH / 'contracts'
ADVISOR = RESEARCH / 'advisor'
SKEPTIC = RESEARCH / 'skeptic'
FORWARD = RESEARCH / 'forward'
REVERSE = RESEARCH / 'reverse'

AW1_CONTRACT = CONTRACTS / 'aw1.json'
AW2_CONTRACT = CONTRACTS / 'aw2.json'
AW1_GATE = ADVISOR / 'aw1-gate.json'
SKEPTIC_AW1_MD = SKEPTIC / 'aw1.md'
SKEPTIC_AW1_JSON = SKEPTIC / 'aw1.json'
FORWARD_AW1_CHECK = FORWARD / 'aw1' / 'check.py'
REVERSE_AW1_CHECK = REVERSE / 'aw1' / 'check.py'
FORWARD_AW1_RESULTS = FORWARD / 'aw1' / 'output' / 'results.json'
REVERSE_AW1_RESULTS = REVERSE / 'aw1' / 'output' / 'results.json'
FORWARD_AW2_CHECK = FORWARD / 'aw2' / 'check.py'
FORWARD_AW2_RESULTS = FORWARD / 'aw2' / 'output' / 'results.json'

DRAFT_IDS = ('AX1', 'AX2', 'AY1', 'AY2', 'AZ1', 'AZ2')
DRAFT_CONTRACT_PATHS = {i: CONTRACTS / (i.lower() + '.json') for i in DRAFT_IDS}


class AuditError(Exception):
    """An audit or a test condition failed, or a damaging mutation was accepted."""


def require(condition, message):
    if not condition:
        raise AuditError(message)


def expect_rejected(fn, *args, **kwargs):
    """Run a damaging mutation / a mislabelled admission attempt; it must raise
    AuditError. Returns the caught message; raises AuditError itself if the
    mutation was wrongly accepted."""
    try:
        fn(*args, **kwargs)
    except AuditError as exc:
        return str(exc)
    raise AuditError('damaging mutation or mislabelled admission was accepted')


def load_json(path):
    return json.loads(Path(path).read_bytes().decode('utf-8'))


def load_text(path):
    return Path(path).read_text(encoding='utf-8')


def rat(value):
    """Exact rational parser: int, Fraction, or an integer/ratio string. No floats,
    no symbolic strings (e.g. 'tau/24' is rejected, deliberately: see
    preregistration_audit_2's AX1/AX2 finding)."""
    if isinstance(value, bool) or isinstance(value, float):
        raise AuditError('non-exact input rejected: ' + repr(value))
    if isinstance(value, (int, Q)):
        return Q(value)
    if isinstance(value, str) and re.fullmatch(r'-?\d+(/\d+)?', value):
        return Q(value)
    raise AuditError('malformed rational rejected: ' + repr(value))


def is_rational(value):
    try:
        rat(value)
        return True
    except AuditError:
        return False


def dec(q, digits=10):
    """Truncated scientific-decimal preview of an exact rational. Never decides
    anything admission-relevant."""
    q = Q(q)
    if q == 0:
        return '0'
    sign = '-' if q < 0 else ''
    q = abs(q)
    e = 0
    while q >= Q(10) ** (e + 1):
        e += 1
    while q < Q(10) ** e:
        e -= 1
    scaled = q / Q(10) ** (e - digits + 1)
    m = str(scaled.numerator // scaled.denominator)
    return sign + m[0] + '.' + m[1:] + 'e' + str(e)


def s(q):
    return str(Q(q))


def merge_results(path, key, payload):
    """Read-modify-write results.json, keeping the other scripts' sections."""
    data = {}
    if Path(path).exists():
        try:
            data = load_json(path)
        except Exception:
            data = {}
    data[key] = payload
    Path(path).write_text(json.dumps(data, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    return data


def match(pattern, text, label):
    m = re.search(pattern, text)
    require(m is not None, 'not parsed: ' + label)
    return m


# ---------------------------------------------------------------------------
# Contract loaders.
# ---------------------------------------------------------------------------
def load_contract(cid, path, expected_status):
    c = load_json(path)
    require(c.get('id') == cid, 'contract id mismatch for ' + str(path))
    require(c.get('status') == expected_status,
            '%s: expected status %r, found %r' % (cid, expected_status, c.get('status')))
    require(c.get('round') == 32, 'contract not round 32: ' + str(path))
    return c


def aw1_contract():
    return load_contract('AW1', AW1_CONTRACT, 'frozen_before_production')


def aw2_contract():
    return load_contract('AW2', AW2_CONTRACT, 'frozen_before_production')


def draft_contract(cid):
    return load_contract(cid, DRAFT_CONTRACT_PATHS[cid], 'draft')


# ---------------------------------------------------------------------------
# Pre-registration closed vocabularies, as validated for AV1/AV2/AW1/AW2 by
# assistant-1's `preregistration_audit.py` (sub-round 1) -- re-declared here,
# not imported, so a change to either audit is visible as a diff, not a shared
# dependency. Any drift found against these lists in the six draft contracts is
# a genuine pre-production finding (see preregistration_audit_2.py), not a bug
# in this list, unless the lens's own sign-off notes have amended it (this task
# does not include loop2-response.md/loop3-signoff.md section 2 verbatim, so the
# amendment cannot be confirmed here and is reported as an open finding).
# ---------------------------------------------------------------------------
ALLOWED_MODEL_ID_PREFIXES = ('AQ_patterned_zero_selected', 'AQ_uniform_routeB', 'FG(')
ALLOWED_STATE_PROVENANCE_PREFIXES = (
    'AQ1_centered_whole_star_subsequence', 'finite_volume_N=', 'finite_graph_ground')
ALLOWED_CENTERING = ('vector', 'none')
ALLOWED_REFERENCE_ROUTE = ('haar', 'selected_strip', 'own_finite_graph')
ALLOWED_COMPARATOR = ('<=', '>=')
ALLOWED_DIRECTION = ('paired', 'single+skeptic', 'statement-only')
EXPECTED_OUTCOME_TYPES = ['accepted_within_scope', 'limited', 'insufficient']
SUB_LABELS_ALLOWED = ['reference_unresolved', 'sign_certified_finite_graph', 'sign_certified_below_cap',
                       'static_not_dynamic', 'uniform_local_closeness_not_uniqueness']
TEMPLATE_CLAIM_EXCLUSIONS = {
    'free reference inside enclosure => no interaction claim', 'uniqueness of the AQ state',
    'whole-sequence convergence or rate in N', 'continuum or weak coupling',
    'transfer from a finite graph', 'relabelling a static shift as dynamical', 'scientific priority'}
HASH_BINDING_FIELDS = ('contract_sha256_in_producer_inputs', 'check_py_reads_target_and_reference_from_contract',
                        'check_py_sha256_recorded_before_full_size_evaluation')
ERROR_TERMS_RULE_TEXT = 'an entry may be not_applicable only with a stated reason'
