#!/usr/bin/env python3
"""Shared helpers for the Jung/Pauli lens, Round32 sub-round 5, assistant-5 scripts.

Standing (calling task; panel-update-4.md item 7, Jung update-4.md section 4: "the
final integration audit"): these are audits and tests for the lens, closing
Round32. **They count zero research loops.** Nothing here is a producer, a
contract, a gate or a skeptical review, and nothing computed here is read back
into any of those. Human project author: Hruday N M (BUNZEEY); AI-assisted.

Copied from (reuses the logic of, does not import) `research/round32/experts/jung/
assistant-4/common4.py`, exactly the way assistant-4's docstring generalised
assistant-3's `common3.py`: the generic utilities (`AuditError`, `require`,
`expect_rejected`, `load_json`, `rat`, `is_rational`, `s`, `merge_results`,
`load_contract`/`load_contract_any_status`), the closed pre-registration
vocabularies, the plan.json extension pieces, the sub-round-4 path constants,
`GATE_FIELD_BOOL_NAMES`/`GATE_FIELD_VALUE_NAMES`, the JSON key/string walkers
and the markdown code-span/negation-cue classifier are kept verbatim from
common4.py (this file started as a literal copy of it, per the calling task's
instruction), so a change to either module's shared logic is visible as a diff,
not a shared dependency, and each assistant's directory stays a self-contained
closure. It does not import `forward/*/check.py`, `reverse/*/check.py`, any
other producer/skeptic module, or any earlier assistant's scripts (only reads
their prose/results by path where the calling task names them as inputs), per
the same isolation discipline.

**What was new in sub-round 4 (kept verbatim below):**
path constants for the AY1/AY2 forward, reverse, gate, skeptic and skeptic
pre-comparison artifacts named by the calling task; `research/round32/experts/
jung/loop2-response.md` (section 4, the observation-map rule for AY, is the
mandatory-sentence and gate-field source the calling task names); the six-name
union of gate-field booleans the calling task asks to be checked everywhere
(`GATE_FIELD_BOOL_NAMES`: three come from loop2-response.md section 4 verbatim
--`uniqueness_claimed`, `whole_sequence_claimed`, `rate_in_N_claimed`--and three
were added later by AY1's own contract item 4 and panel-update-3.md item 2
--`rate_claimed`, `translation_invariance_claimed`,
`boundary_independence_of_dynamics_claimed`; see `sentence_and_gate_field_audit.py`
for where each is attested); the four gate-adjacent value fields
`GATE_FIELD_VALUE_NAMES` (`states_compared`, `region`, `topology`,
`closeness_order`); a generic recursive JSON key-walker (`walk_json`) used to find
every occurrence of a key by name at any nesting depth, distinguishing a real
`{"key": value}` export from the key's name merely appearing as a *string value*
inside some other list (e.g. a mutation-description or a "which fields this
control checks" list) -- only the former counts as an export; the forbidden-phrase
scan constants and the markdown code-span/negation-cue classifier
(`classify_phrase_occurrence`) used by `sentence_and_gate_field_audit.py`, adapted
from assistant-3's `forbidden_wording_grep.py` `classify()` (re-implemented here
for a different phrase set: `the AQ state`/`uniqueness of the AQ state`, `the
thermodynamic limit`, bare `unique` without a `not` in the same sentence, and the
required phrase `a chosen subsequential`).

**What is new here (sub-round 5's own additions):** `ALL_TEN_IDS` and per-id
path constants (contract, gate, forward report/results, reverse report/results
where a reverse exists, skeptic .md/.json) for every one of the ten Round32
investigations AV1 through AZ2, not just AY1/AY2/AZ1/AZ2; `AZ1_GATE_FIELD_NAMES`
and `AZ2_GATE_FIELD_NAMES` (the topic-specific gate-field unions panel-update-4.md
decisions 2-3 and Jung update-4.md section 3 add for the continuum-trajectory and
finite-graph loops, distinct from the six-name state-identification union);
`round_wide_md_and_json_paths()`, a filesystem walk of every `research/round32/
**/*.md` and `**/*.json` file (the calling task's item 2 scope) plus the addendum
`.tex` files under `papers/round32-addendum/` and the two `README.md` files
(repo root and `research/round32/`), so the forbidden-phrase sweep is not a
hardcoded file list; `sentence_has_not` (moved here from assistant-4's own
script body, unchanged, since two sub-round-5 scripts now need it) for the
sentence-scoped negation check on bare `unique`/`uniqueness`; `FORBIDDEN_PHRASE_PATTERNS_R5`,
the calling task's nine phrase patterns (the two assistant-4 already had, plus
`the continuum limit exists`, `fraction of the problem`, `predicts`, `confirms
the Z^3 value`, `first certified`, and the two-word proximity phrase `solves`/
`solved` near `mass gap`); `walk_all_strings` (moved here from assistant-4's
`preregistration_audit_4.py`, unchanged) for the generic JSON string walk used
by both the placeholder listing and the phrase sweep's JSON side.

Usage: each sibling script imports this module (``import common5 as K``) after
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


# ---------------------------------------------------------------------------
# Sub-round 4 additions: paths named by the calling task.
# ---------------------------------------------------------------------------
JUNG_LOOP2_RESPONSE = HERE.parent / 'loop2-response.md'

AY1_CONTRACT = CONTRACTS / 'ay1.json'
AY2_CONTRACT = CONTRACTS / 'ay2.json'
AZ1_CONTRACT = CONTRACTS / 'az1.json'
AZ2_CONTRACT = CONTRACTS / 'az2.json'

AY1_GATE = ADVISOR / 'ay1-gate.json'
AY2_GATE = ADVISOR / 'ay2-gate.json'  # sub-round 4 note ("may not exist yet") is now
    # stale: as of sub-round 5 every one of the ten Round32 gates exists on disk
    # (confirmed below by ALL_TEN_IDS path construction + existence checks in the
    # sub-round-5 scripts); kept as AY2_GATE for path-name continuity with common4.py.

FORWARD_AY1_REPORT = FORWARD / 'ay1' / 'report.md'
REVERSE_AY1_REPORT = REVERSE / 'ay1' / 'report.md'
FORWARD_AY1_RESULTS = FORWARD / 'ay1' / 'output' / 'results.json'
REVERSE_AY1_RESULTS = REVERSE / 'ay1' / 'output' / 'results.json'
FORWARD_AY1_CHECK = FORWARD / 'ay1' / 'check.py'
REVERSE_AY1_CHECK = REVERSE / 'ay1' / 'check.py'

FORWARD_AY2_REPORT = FORWARD / 'ay2' / 'report.md'
FORWARD_AY2_RESULTS = FORWARD / 'ay2' / 'output' / 'results.json'
FORWARD_AY2_CHECK = FORWARD / 'ay2' / 'check.py'

SKEPTIC_AY1_JSON = SKEPTIC / 'ay1.json'
SKEPTIC_AY1_MD = SKEPTIC / 'ay1.md'
SKEPTIC_AY2_INDEPENDENT_RESULTS = SKEPTIC / 'ay2-independent' / 'results.json'

# The calling task's six-name union of gate-field booleans. Three are named
# verbatim in loop2-response.md section 4 ("Mandatory gate fields"):
# uniqueness_claimed, whole_sequence_claimed, rate_in_N_claimed. Three more were
# added later, first appearing in AY1's own contract item 4 and recorded as a
# panel decision in advisor/panel-update-3.md item 2 ("uniqueness, whole-sequence,
# rate, translation invariance, boundary independence of dynamics all false"):
# rate_claimed, translation_invariance_claimed, boundary_independence_of_dynamics_claimed.
# Recording both provenances rather than picking one is the point of this audit
# (see sentence_and_gate_field_audit.py finding on the rate_claimed/rate_in_N_claimed
# name split, already self-noted as wording defect W3 by the AY1 forward producer
# and by the AY1 gate).
GATE_FIELD_BOOL_NAMES = (
    'uniqueness_claimed', 'whole_sequence_claimed', 'rate_claimed', 'rate_in_N_claimed',
    'translation_invariance_claimed', 'boundary_independence_of_dynamics_claimed',
)
GATE_FIELD_BOOL_NAMES_LOOP2_ORIGIN = ('uniqueness_claimed', 'whole_sequence_claimed', 'rate_in_N_claimed')
GATE_FIELD_BOOL_NAMES_AY1_CONTRACT_ADDED = (
    'rate_claimed', 'translation_invariance_claimed', 'boundary_independence_of_dynamics_claimed')

# The four gate-adjacent value fields the calling task asks be compared for
# agreement across forward/reverse/skeptic/gate.
GATE_FIELD_VALUE_NAMES = ('states_compared', 'region', 'topology', 'closeness_order')

REQUIRED_PHRASE = 'a chosen subsequential'
FORBIDDEN_PHRASE_AQ_STATE = 'the AQ state'
FORBIDDEN_PHRASE_UNIQUENESS_OF_AQ_STATE = 'uniqueness of the AQ state'
FORBIDDEN_PHRASE_THERMODYNAMIC_LIMIT = 'the thermodynamic limit'


# ---------------------------------------------------------------------------
# Generic recursive JSON key-walker: every {"key": value} pair at any nesting
# depth, with its dotted/bracketed json-path, distinguishing a real export
# (the key of a dict) from the key's name occurring only as a *string value*
# somewhere (e.g. inside a "which controls this validates" or a mutation-name
# list) -- callers decide separately whether a string-value occurrence counts.
# ---------------------------------------------------------------------------
def walk_json_items(obj, path=''):
    """Yields (path, key, value) for every dict entry anywhere in obj."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = (path + '.' + k) if path else k
            yield (p, k, v)
            yield from walk_json_items(v, p)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            p = path + '[%d]' % i
            yield from walk_json_items(v, p)


def walk_json_strings(obj, path=''):
    """Yields (path, string_value) for every plain string found anywhere in obj
    (dict values, list entries, or scalars), used to find a name mentioned only
    as data (e.g. a rejected-mutation label) rather than exported as a key."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = (path + '.' + k) if path else k
            yield from walk_json_strings(v, p)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            p = path + '[%d]' % i
            yield from walk_json_strings(v, p)
    elif isinstance(obj, str):
        yield (path, obj)


def find_key_occurrences(obj, key_name):
    """All (path, value) where a dict key equals key_name, anywhere in obj --
    the 'real export' sense (a JSON key binding), not a string mention."""
    return [(p, v) for (p, k, v) in walk_json_items(obj) if k == key_name]


# ---------------------------------------------------------------------------
# Forbidden/required-phrase scan: shared negation-cue vocabulary (adapted from
# assistant-3's forbidden_wording_grep.py NEGATION_CUES, extended with cues
# specific to this phrase set) and a markdown code-span detector.
# ---------------------------------------------------------------------------
PHRASE_NEGATION_CUES = (
    'never', 'not ', 'not\n', 'no ', "n't", 'false', 'reject', 'forbidden', 'exclu', 'without',
    'quoted only', 'quoted verbatim', 'verbatim, in code spans', 'is not asserted', 'not claimed',
    'not admitted', 'does not assert', 'not the whole-box', 'is never described', 'phrasing rule',
    'checker rejects', 'checker scans', 'claim_exclusions', 'claim exclusions', 'rejected_for',
    'mutation', 'damaging', 'forbidden phrasing', 'overclaim', 'missing', 'obligation', 'unproved',
    'unproven', 'candidate route', 'no premise',
)


def in_code_span(text, start, end):
    """True iff text[start:end] is enclosed by a pair of single backticks on the
    same line (a markdown inline code span) -- i.e. there is an odd number of
    backticks before `start` since the start of the enclosing line, and the next
    backtick after `end` (on the same line) closes it. A simple, line-scoped
    heuristic (no fenced-block handling needed: none of the scanned files put
    these phrases inside fenced code blocks)."""
    line_start = text.rfind('\n', 0, start) + 1
    line_end = text.find('\n', end)
    if line_end == -1:
        line_end = len(text)
    line = text[line_start:line_end]
    rel_start = start - line_start
    rel_end = end - line_start
    before = line[:rel_start]
    after = line[rel_end:]
    return (before.count('`') % 2 == 1) and ('`' in after)


def classify_phrase_occurrence(text, start, end, radius=200):
    """Classifies one match of a forbidden phrase found at text[start:end] inside
    a markdown file: returns (kind, cues) where kind is one of
    'whitelisted_code_span_negated' (verbatim, negated, AND inside a code span --
    the calling task's whitelist), 'negated_outside_code_span' (negated but not
    inside a code span -- outside the letter of the whitelist though not read as
    an affirmative claim; recorded, not silently passed), or
    'AFFIRMATIVE_needs_review' (no negation cue nearby)."""
    window = text[max(0, start - radius):min(len(text), end + radius)].lower()
    cues = [c for c in PHRASE_NEGATION_CUES if c in window]
    negated = bool(cues)
    spanned = in_code_span(text, start, end)
    if negated and spanned:
        return 'whitelisted_code_span_negated', cues
    if negated:
        return 'negated_outside_code_span', cues
    return 'AFFIRMATIVE_needs_review', cues


def normalize_sentence(text):
    """Strips markdown inline-code backticks and collapses whitespace, so a
    backtick-marked template (as loop2-response.md writes it) can be compared
    against a plain-prose rendering of the same sentence (as e.g. the reverse
    report renders it, with the backticks removed)."""
    return re.sub(r'\s+', ' ', text.replace('`', '')).strip()


# ---------------------------------------------------------------------------
# Sub-round 5 additions: all ten investigations, the whole-round file sweep,
# and the two AZ-specific gate-field unions. Everything below is new in
# assistant-5 (see module docstring).
# ---------------------------------------------------------------------------
ALL_TEN_IDS = ('AV1', 'AV2', 'AW1', 'AW2', 'AX1', 'AX2', 'AY1', 'AY2', 'AZ1', 'AZ2')

# Which of the ten have a reverse producer (paired direction only; the
# single+skeptic/statement+skeptic loops AW2, AX2, AY2, AZ1, AZ2 have none --
# confirmed by directory listing, not assumed).
REVERSE_EXISTS = {'AV1': True, 'AV2': True, 'AW1': True, 'AW2': False, 'AX1': True,
                  'AX2': False, 'AY1': True, 'AY2': False, 'AZ1': False, 'AZ2': False}

TEN_CONTRACT_PATHS = {cid: CONTRACTS / (cid.lower() + '.json') for cid in ALL_TEN_IDS}
TEN_GATE_PATHS = {cid: ADVISOR / (cid.lower() + '-gate.json') for cid in ALL_TEN_IDS}
TEN_FORWARD_REPORT_PATHS = {cid: FORWARD / cid.lower() / 'report.md' for cid in ALL_TEN_IDS}
TEN_FORWARD_RESULTS_PATHS = {cid: FORWARD / cid.lower() / 'output' / 'results.json' for cid in ALL_TEN_IDS}
TEN_REVERSE_REPORT_PATHS = {cid: REVERSE / cid.lower() / 'report.md' for cid in ALL_TEN_IDS if REVERSE_EXISTS[cid]}
TEN_REVERSE_RESULTS_PATHS = {cid: REVERSE / cid.lower() / 'output' / 'results.json'
                             for cid in ALL_TEN_IDS if REVERSE_EXISTS[cid]}
TEN_SKEPTIC_JSON_PATHS = {cid: SKEPTIC / (cid.lower() + '.json') for cid in ALL_TEN_IDS}
TEN_SKEPTIC_MD_PATHS = {cid: SKEPTIC / (cid.lower() + '.md') for cid in ALL_TEN_IDS}

# The topic-specific gate-field unions panel-update-4.md decisions 2/3 and
# Jung update-4.md section 3 name for AZ1 (continuum-trajectory statement) and
# AZ2 (finite-graph loop), distinct from the six-name state-identification
# union (`GATE_FIELD_BOOL_NAMES` above, which applies where a loop's subject is
# state identification -- AY1/AY2, and, per plan.json's second extension note,
# is "not universal across every contract").
AZ1_GATE_FIELD_NAMES = ('continuum_claim', 'uniform_in_a_claimed', 'weak_coupling_claim',
                        'loop_count_fraction_claimed')
AZ2_GATE_FIELD_NAMES = ('transfers_to_aq', 'model_is_finite_graph', 'fg_coefficients_fitted')
# Expected boolean value for each name in the two AZ unions (all false except
# AZ2's model_is_finite_graph, which the AZ2 contract itself requires true).
AZ_GATE_FIELD_REQUIRED_VALUE = {
    'continuum_claim': False, 'uniform_in_a_claimed': False, 'weak_coupling_claim': False,
    'loop_count_fraction_claimed': False, 'transfers_to_aq': False, 'model_is_finite_graph': True,
    'fg_coefficients_fitted': False,
}
GATE_FIELD_BOOL_REQUIRED_VALUE = {name: False for name in GATE_FIELD_BOOL_NAMES}

PAPERS_ADDENDUM = ROOT / 'papers' / 'round32-addendum'
ROOT_README = ROOT / 'README.md'
ROUND32_README = RESEARCH / 'README.md'


def round_wide_md_and_json_paths():
    """Every `research/round32/**/*.md` and `**/*.json` file on disk (the
    calling task's item 2 scope: "report/review/gate/contract/findings/HANDOFF
    if present" names *examples* of what these two globs cover, not an
    exhaustive hand list -- so this walks the filesystem instead of hardcoding
    a file list, the same discipline `draft_placeholder_listing` in
    assistant-4's `preregistration_audit_4.py` used for JSON fields). Returns a
    sorted list of Path objects, deterministic across runs and Python builds
    (`sorted()` on POSIX path strings)."""
    md = sorted(RESEARCH.rglob('*.md'))
    js = sorted(RESEARCH.rglob('*.json'))
    return md + js


def addendum_tex_paths():
    """Every `.tex` file directly under `papers/round32-addendum/` (not the
    `tmp/` build-artifact subdirectory)."""
    return sorted(PAPERS_ADDENDUM.glob('*.tex'))


def extra_readme_paths():
    """The two README.md files the calling task names outside the
    `research/round32/**` glob (the repository root) or as an explicit
    duplicate-safe inclusion inside it (`research/round32/README.md` -- already
    covered by `round_wide_md_and_json_paths()`, listed again here only for
    callers that want the root README on its own)."""
    return [ROOT_README]


def walk_all_strings(obj, path=''):
    """Yields (json_path, string_value) for every plain string anywhere in obj
    (dict values, list entries, or scalars). Moved here, unchanged, from
    assistant-4's `preregistration_audit_4.py` (`draft_placeholder_listing`'s
    helper) since two sub-round-5 scripts need it now."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from walk_all_strings(v, (path + '.' + k) if path else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_all_strings(v, path + '[%d]' % i)
    elif isinstance(obj, str):
        yield path, obj


def sentence_has_not(text, pos):
    """For a bare forbidden/flagged word at text[pos]: is there a 'not' (or
    "n't") in the same sentence? A sentence is approximated as the span
    between the nearest '.', ';', '\\n' (or start/end of text) on either side
    of pos. Moved here, unchanged, from assistant-4's
    `sentence_and_gate_field_audit.py` since two sub-round-5 scripts need it."""
    start = 0
    for sep in '.;\n':
        i = text.rfind(sep, 0, pos)
        if i > start:
            start = i
    end = len(text)
    for sep in '.;\n':
        i = text.find(sep, pos)
        if i != -1 and i < end:
            end = i
    sentence = text[start:end].lower()
    return 'not' in sentence or "n't" in sentence


# ---------------------------------------------------------------------------
# The calling task's nine forbidden/flagged phrase patterns (item 2). The
# first three (`the_AQ_state`, `the_thermodynamic_limit`, `bare_unique`) are
# assistant-4's own patterns, carried over unchanged; the other six are new in
# sub-round 5. `mass_gap_solves` is a proximity pattern, not a fixed phrase:
# it fires when 'solves'/'solved' and 'mass gap' occur in the same sentence
# (the same sentence-window `sentence_has_not` already uses for 'not'),
# regardless of which comes first.
# ---------------------------------------------------------------------------
FORBIDDEN_PHRASE_PATTERNS_R5 = {
    'the_AQ_state': re.compile(re.escape('the AQ state'), re.I),
    'the_thermodynamic_limit': re.compile(re.escape('the thermodynamic limit'), re.I),
    'bare_unique': re.compile(r'\bunique(?:ness)?\b', re.I),
    'the_continuum_limit_exists': re.compile(re.escape('the continuum limit exists'), re.I),
    'fraction_of_the_problem': re.compile(r'fraction of the (?:continuum )?problem', re.I),
    'predicts': re.compile(r'\bpredicts?\b', re.I),
    'confirms_the_Z3_value': re.compile(r"confirms? the Z\^?3 value", re.I),
    'first_certified': re.compile(re.escape('first certified'), re.I),
}
MASS_GAP_RE = re.compile(r'\bmass gap\b', re.I)
SOLVES_SOLVED_RE = re.compile(r'\bsolv(?:es|ed)\b', re.I)
