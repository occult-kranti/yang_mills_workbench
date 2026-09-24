#!/usr/bin/env python3
"""Shared helpers for the Jung/Pauli lens, Round32 sub-round 3, assistant-3 scripts.

Standing (calling task; `update-2.md` section 5): these are pre-registration audits
and tests for the lens, run after AX1/AX2 and before AY1/AY2/AZ1/AZ2 leave
`status: draft`. They count zero research loops. Nothing here is a producer, a
contract, a gate or a skeptical review, and nothing computed here is read back into
any of those. Human project author: Hruday N M (BUNZEEY); AI-assisted.

Generalises (reuses the logic of, does not import) `research/round32/experts/jung/
assistant-2/common2.py` and `preregistration_audit_2.py`, exactly the way
assistant-2's docstring generalised assistant-1's `common.py`/
`preregistration_audit.py`: the generic utilities (`AuditError`, `require`,
`expect_rejected`, `load_json`, `rat`, `is_rational`, `s`, `merge_results`,
`load_contract`/`load_contract_any_status`) and the closed pre-registration
vocabularies are re-declared here, not imported, so a change to any of the three
audits is visible as a diff, not a shared dependency, and each assistant's
directory stays a self-contained closure. It does not import `forward/*/check.py`,
`reverse/*/check.py`, any other producer/skeptic module, or assistant-1's or
assistant-2's scripts (only reads their prose/results by path where the calling
task names them as inputs), per the same isolation discipline.

**What is new here (the calling task's "extended vocabulary from plan.json"):**
`research/round32/advisor/plan.json`'s `preregistration_vocabulary_extensions`
block (dated 2026-09-24, recorded after the Jung assistant-2 audit found three
schema gaps in the AX1..AZ2 drafts) amends four of assistant-2's closed fields:

  - `selected_triple_alpha_units` may now be an exact expression in tau (a
    3-element list of tau-linear strings such as `'tau/24'`, not only exact
    rationals) or the sentinel string `'n/a (finite graph)'` when `model_id`
    names the finite graph (starts with `'FG('`).
  - `direction` gains a fourth allowed value, `'statement+skeptic'`.
  - `observable.reference_route` gains `'n/a'`, restricted to statement loops
    (`direction` in `{statement-only, statement+skeptic}`) with the reason
    recorded in `error_terms_itemized`.
  - `tau.value` may be an exact rational (unchanged), the string `'grid'` with
    the grid enumerated in `parameters.tau_FG_grid` (finite-graph loops), or a
    rule-reference string (accepted leniently; no drift in this round's six
    contracts uses this third case, so it is not exercised by AX1/AX2/AY1/AY2/
    AZ1/AZ2, only implemented for completeness against the plan.json text).

Every other field keeps assistant-2's exact closed-vocabulary check unchanged.

Usage: each sibling script imports this module (``import common3 as K``) after
adding this directory to ``sys.path``; run every script with ``python3 -B``.
"""
import json
import re
from fractions import Fraction as Q
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]  # assistant-3 -> jung -> experts -> round32 -> research -> ROOT
RESEARCH = ROOT / 'research' / 'round32'
CONTRACTS = RESEARCH / 'contracts'
ADVISOR = RESEARCH / 'advisor'
SKEPTIC = RESEARCH / 'skeptic'
FORWARD = RESEARCH / 'forward'
REVERSE = RESEARCH / 'reverse'

PLAN_JSON = ADVISOR / 'plan.json'

AX1_CONTRACT = CONTRACTS / 'ax1.json'
AX2_CONTRACT = CONTRACTS / 'ax2.json'
AX1_GATE = ADVISOR / 'ax1-gate.json'
SKEPTIC_AX1_JSON = SKEPTIC / 'ax1.json'
SKEPTIC_AX1_MD = SKEPTIC / 'ax1.md'
FORWARD_AX1_CHECK = FORWARD / 'ax1' / 'check.py'
REVERSE_AX1_CHECK = REVERSE / 'ax1' / 'check.py'
FORWARD_AX1_REPORT = FORWARD / 'ax1' / 'report.md'
REVERSE_AX1_REPORT = REVERSE / 'ax1' / 'report.md'
FORWARD_AX1_RESULTS = FORWARD / 'ax1' / 'output' / 'results.json'
REVERSE_AX1_RESULTS = REVERSE / 'ax1' / 'output' / 'results.json'
FORWARD_AX1_FREEZE = FORWARD / 'ax1' / 'freeze.json'
REVERSE_AX1_FREEZE = REVERSE / 'ax1' / 'freeze.json'

DRAFT_IDS = ('AY1', 'AY2', 'AZ1', 'AZ2')
FROZEN_IDS = ('AX1', 'AX2')
ALL_SIX_IDS = FROZEN_IDS + DRAFT_IDS
CONTRACT_PATHS = {i: CONTRACTS / (i.lower() + '.json') for i in ALL_SIX_IDS}


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
    """Exact rational parser: int, Fraction, or an integer/ratio string. No floats.
    Deliberately still rejects symbolic strings ('tau/24') -- those are handled by
    `is_tau_linear`, a distinct, explicitly-typed acceptance path, not folded into
    this generic rational parser, so that a caller asking for an exact rational
    never silently receives a formula."""
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


SYMBOLIC_TAU_RE = re.compile(r'^-?(\d+(/\d+)?\*)?tau(/\d+(/\d+)?)?$')


def is_tau_linear(value):
    """True iff `value` is a string of the exact-expression-in-tau shape the
    plan.json extension names (e.g. 'tau/24', 'tau', '-tau/144'): an optional
    leading '-' and/or exact-rational coefficient times 'tau', with an optional
    exact-rational divisor. Not a general symbolic-algebra parser -- deliberately
    narrow, matching only the linear-in-tau shape actually used in this round's
    contracts, so a genuinely unrelated symbolic string is still rejected."""
    return isinstance(value, str) and SYMBOLIC_TAU_RE.match(value) is not None


def dec(q, digits=10):
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
# Contract loaders (same behaviour as common2.py's; re-declared, not imported).
# ---------------------------------------------------------------------------
def load_contract(cid, path, expected_status):
    c = load_json(path)
    require(c.get('id') == cid, 'contract id mismatch for ' + str(path))
    require(c.get('status') == expected_status,
            '%s: expected status %r, found %r' % (cid, expected_status, c.get('status')))
    require(c.get('round') == 32, 'contract not round 32: ' + str(path))
    return c


def load_contract_any_status(cid, path, allowed_statuses=('draft', 'frozen_before_production')):
    c = load_json(path)
    require(c.get('id') == cid, 'contract id mismatch for ' + str(path))
    require(c.get('status') in allowed_statuses,
            '%s: status %r is neither draft nor frozen_before_production' % (cid, c.get('status')))
    require(c.get('round') == 32, 'contract not round 32: ' + str(path))
    return c


def ax1_contract():
    return load_contract('AX1', AX1_CONTRACT, 'frozen_before_production')


def ax2_contract():
    return load_contract('AX2', AX2_CONTRACT, 'frozen_before_production')


def draft_contract(cid):
    """Loads one of AY1/AY2/AZ1/AZ2 at whatever status is currently on disk."""
    return load_contract_any_status(cid, CONTRACT_PATHS[cid])


def any_contract(cid):
    """Loads any of the six (AX1/AX2/AY1/AY2/AZ1/AZ2) at whatever status is
    currently on disk -- used for the single per-contract structural loop that
    treats all six uniformly, recording the observed status rather than assuming
    one (same live-repository caution as common2.py's `load_contract_any_status`
    docstring)."""
    return load_contract_any_status(cid, CONTRACT_PATHS[cid])


# ---------------------------------------------------------------------------
# Pre-registration closed vocabularies. Unchanged fields are re-declared exactly
# as common2.py had them (verbatim from assistant-1's sub-round-1 schema). The
# four fields plan.json amended (selected_triple_alpha_units, direction,
# reference_route, tau.value) get their *extended* acceptance rules below,
# separately named (_EXT / is_*) so the amendment is visible as an addition, not
# a silent widening of the original names.
# ---------------------------------------------------------------------------
ALLOWED_MODEL_ID_PREFIXES = ('AQ_patterned_zero_selected', 'AQ_uniform_routeB', 'FG(')
ALLOWED_STATE_PROVENANCE_PREFIXES = (
    'AQ1_centered_whole_star_subsequence', 'finite_volume_N=', 'finite_graph_ground')
ALLOWED_CENTERING = ('vector', 'none')
ALLOWED_COMPARATOR = ('<=', '>=')
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

# Pre-extension vocabularies (kept for reference / regression comparison against
# assistant-2's findings -- `preregistration_audit_3.py` reports both the
# pre-extension and post-extension verdicts for the four amended fields so the
# extension's effect is visible, not just its outcome).
ALLOWED_DIRECTION = ('paired', 'single+skeptic', 'statement-only')
ALLOWED_REFERENCE_ROUTE = ('haar', 'selected_strip', 'own_finite_graph')

# plan.json extension, verbatim source: advisor/plan.json ->
# preregistration_vocabulary_extensions (dated 2026-09-24).
ALLOWED_DIRECTION_EXT = ('paired', 'single+skeptic', 'statement-only', 'statement+skeptic')
ALLOWED_REFERENCE_ROUTE_EXT_BASE = ('haar', 'selected_strip', 'own_finite_graph')
STATEMENT_DIRECTIONS = ('statement-only', 'statement+skeptic')


def load_plan():
    return load_json(PLAN_JSON)


def plan_extension_covers(plan):
    """True iff advisor/plan.json actually carries the four-field extension this
    module implements (defensive: if the plan changes again, this audit should
    say so rather than silently keep applying a stale extension)."""
    ext = plan.get('preregistration_vocabulary_extensions') or {}
    keys = {'selected_triple_alpha_units', 'direction', 'reference_route', 'tau.value'}
    return keys <= set(ext)
