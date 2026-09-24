#!/usr/bin/env python3
"""Jung/Pauli lens, Round32 sub-round 5, assistant-5 script 2 of 3: a whole-round
forbidden-phrase sweep (panel-update-4.md item 7, Jung update-4.md section 4
item 4, calling task item 2).

Counts zero research loops. Not a producer, contract, gate or skeptical
review; nothing computed here is read back into any of those. Human project
author: Hruday N M (BUNZEEY); AI-assisted. Standard library only. Does not
import `forward/*/check.py`, `reverse/*/check.py`, or any other
producer/skeptic module.

Scope (whole-word, case-insensitive): every file under `research/round32/`
matching `*.md` or `*.json` (report/review/gate/contract/`advisor/
findings.json`, `research/round32/HANDOFF.md` -- absent when the calling task
was written, present by the time this script ran: a live, concurrently-
advancing repository, the same situation assistant-4's README documented for
`ay2-gate.json`), every `*.tex` file directly under `papers/round32-addendum/`,
the repository root `README.md` and `research/round32/README.md` (the second
is already inside the first glob; named again for an explicit, standalone
hit). This script's own output directory (`experts/jung/assistant-5/`) is
excluded from the swept set: scanning a results.json this same run is still
writing would be circular (its own findings necessarily quote every forbidden
phrase to report on it) and is not part of the round's scientific record.

Nine phrase patterns (the calling task's list): `the AQ state`, `the
thermodynamic limit`, bare `unique`/`uniqueness` without `not`/`n't` in the
same sentence, `the continuum limit exists`, `fraction of the (continuum)
problem`, `predicts`, `confirms the Z^3 value`, `first certified` (always
flagged, never silently classified away), and the proximity pattern
`solves`/`solved` in the same sentence as `mass gap`.

**Deduplication.** `AGENTS.md`'s producer closures require byte-identical
snapshots of every declared premise inside `forward/*/inputs/` and
`reverse/*/inputs/`; the same handful of shared source files (e.g.
`research/round21/forward/i1/report.md`, `research/round29/forward/am2/
report.md`) are therefore snapshotted, unchanged, into ten or more producers'
`inputs/` trees by design, not by accident. Scanning every path independently
would count the same underlying sentence ten-plus times and make the round
look far noisier than it is. This script groups files by SHA-256 content
hash, scans one representative per distinct content, and records every path
sharing that hash as `also_at` -- so nothing is hidden (every path is still
listed in `files_scanned`), but a single sentence is one finding, not ten.

**Classification.** Every hit is one of:

  (i)   `excluded_list_or_code_span` -- inside a JSON `claim_exclusions`/
        `forbidden_phrasings`/`exclusions`-style array (no code-span
        mechanism applies to JSON, so any occurrence there is this category
        by construction, per assistant-4's precedent); or, in markdown/tex,
        inside a backtick code span, a fenced ``` code block, a straight
        `"..."` double-quote span, or (tex only) a LaTeX ``...'' quote span.
        Quoting a phrase to name or discuss it is not asserting it, whether
        or not a negation cue also happens to be nearby.
  (ii)  `negated_in_prose` -- not quoted/excluded, but a negation cue is
        present in the surrounding sentence/window (assistant-4's own
        `PHRASE_NEGATION_CUES`, extended here with a few more natural-language
        negations this whole-round corpus actually uses -- `nothing`, `none`,
        `fails to`, `cannot`, `remains? open`, `left open` -- checked against
        the window with markdown emphasis markers (`**`, `_`) stripped first,
        so `does **not** claim` still matches). This is a classification-time
        judgement, broader than the mechanical "literal 'not' in the same
        sentence" trigger the round's own rule uses to flag a candidate in the
        first place (that literal, narrower trigger is what decides whether
        `bare_unique` is even a candidate at all, per loop2-response.md's own
        wording).
  (iii) `AFFIRMATIVE_needs_review` -- none of the above. **Only this category
        is a defect.**

Bookkeeping categories, kept distinct from (iii) so a legitimate structure is
never counted as a defect:

  `obligations_table_entry`, `mutation_or_control_description`,
  `scan_or_review_metadata_field` (a JSON `.phrase`/`.matched_text`-style field
  that itself IS the name of a phrase a scan/review found and already
  classified -- e.g. a skeptic review's own forbidden-phrase-scan check
  output), `off_topic_different_admitted_fact` (`unique`/`uniqueness`
  describing a DIFFERENT, already-admitted mathematical fact this project
  itself proved -- a finite-volume Hamiltonian's unique ground state or a
  contraction map's unique fixed point (AM2/AQ1's own theorem) -- not "the AQ
  state"/"any subsequential limit" being unique, the actually-forbidden sense),
  `third_party_literature_description` (`unique`/`predicts` describing what a
  cited external paper claims, in a literature-survey file, not this
  project's own claim), `off_topic_ordinary_usage` (`predicts` used in its
  ordinary English sense, e.g. a shared methodology reference file's worked
  example, with none of the round's own topic markers nearby).

`first_certified` hits are always listed under their own section regardless
of classification (the calling task: "flag; the advisor removed one
overclaim") -- this script does not assume which of a possible past overclaim
and the current text the calling task refers to; it reports both what git
history (`git log -p -S"first certified"`) and the current text show, and
lets the advisor read them side by side.

Usage: python3 -B forbidden_phrase_sweep.py
"""
import hashlib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common5 as K  # noqa: E402

SELF_DIR = Path(__file__).resolve().parent
TOPIC_MARKERS = ('z^3', 'z3', '1/144', '1/6', 'confirms', 'consistent with')
EXCLUSION_PATH_RE = re.compile(r'(?:claim_exclusions|forbidden_phrasings|exclusions?)(?:\[\d+\])?$', re.I)
OBLIGATIONS_PATH_RE = re.compile(r'\bobligations\[\d+\]')
MUTATION_OR_CONTROL_PATH_RE = re.compile(
    r'\bmutations\[\d+\]|rejected_for|required_false|\.mutation$|\bchecks\[\d+\]\.id$|contract_defects|'
    r'\bdefects\[\d+\]|rejected_mutations|runs\.report_phrase|\bmutation\b')
SCAN_METADATA_PATH_RE = re.compile(r'\.phrase(\[\d+\])?$|occurrences_outside_template|matched_text$', re.I)

LITERATURE_FILE_MARKERS = ('sota-table.md', 'sources.json', '/memo.md')
# The actually-forbidden sense of "unique"/"uniqueness" (loop2-response.md
# section 4: the state-identification loops' own vocabulary) is narrow and
# distinctive: whether the infinite-volume limit the AQ/I1 construction
# selects, among possibly many subsequential limits, is a single one. Every
# other sense found in this corpus during development of this script -- a
# FINITE Hamiltonian's unique ground state or unique fixed point (a linear-
# algebra/contraction-mapping fact, AM2/AQ1's own admitted theorem, a
# different property entirely: "a unique gauge-invariant ground and gap",
# "the strip ground state is unique", "unique Haar vacuum", "the kernel is
# the constants and the solution is unique"), Euclidean division's unique
# quotient/remainder ("unique i,r with x=4i+r"), an external paper's own
# uniqueness result (`experts/modern/sota-table.md`, a literature survey),
# or an earlier and entirely unrelated research round's own result (the root
# README's round13 summary: "a proved complete compact-hierarchy uniqueness
# result") -- is a legitimate, different use of the same English word.
# Enumerating every legitimate off-topic sense is impractical (they are
# numerous and varied, as the examples above show); this list instead
# enumerates the round's own ON-topic vocabulary and requires one of these
# markers nearby before a bare `unique`/`uniqueness` occurrence is even
# eligible for AFFIRMATIVE_needs_review -- the same "positive topic-
# relevance" design already used for `predicts` below, just as the primary
# filter here rather than a secondary one, since off-topic uses of "unique"
# heavily outnumber on-topic ones once the sweep covers the whole round
# instead of only the AY-family files assistant-4 scoped its own scan to.
ON_TOPIC_UNIQUE_MARKERS = (
    'aq state', 'aq-state', 'aq1 state', 'subsequential', 'infinite-volume state', 'infinite volume state',
    'infinite-volume limit', 'infinite volume limit', 'infinite-volume limiting', 'the limit selected',
    'which state', 'which limit', 'f1 and f2', 'f1, f2', 'construction famil', 'boundary condition',
    'state identification', 'the state (', 'the ay state',
)
# Higher-priority than ON_TOPIC_UNIQUE_MARKERS: the modifier immediately
# following "unique"/"uniqueness" names a FIXED, FINITE Hamiltonian's own
# ground state, fixed point or similar linear-algebra object -- a real,
# different, already-admitted fact (AM2/AQ1/AX1's own theorem) -- even when an
# on-topic word like "subsequential" happens to occur later in the SAME
# sentence for an unrelated reason (confirmed: `forward/az1/output/
# results.json`'s own estimate statement reads "...has a unique gauge-
# invariant ground and full-space gap >= 1/2...; the gap passes to the AQ
# subsequential states" -- "subsequential" describes what the GAP transfers
# to, not what is unique). Checked first, before the wider on-topic window.
IMMEDIATE_GROUND_STATE_FOLLOWERS = (
    'ground', 'gauge-invariant ground', 'fixed point', 'haar vacuum', 'solution', 'i,r', 'j,s',
)
EXTRA_NEGATION_CUES = ('nothing', 'none ', 'fails to', 'cannot', 'remain open', 'remains open', 'left open',
                       'still open', 'unresolved', 'open question')
# Pure external-literature ledgers: every record in these files is, by the
# file's own purpose, a note about what a CITED source says, never this
# project's own claim (unlike a memo.md, which also discusses this project's
# own methodology and premises in the same file -- confirmed:
# `experts/historical/memo.md` line 128 genuinely uses the forbidden "the AQ
# state" phrase about THIS project's own AT4 hypotheses, so memo.md files are
# NOT given this unconditional treatment, only sota-table.md/sources.json).
PURE_LITERATURE_FILE_SUFFIXES = ('sota-table.md', 'sources.json')
# Files recording a still-`planned_not_executed` roadmap/network item: naming
# a future proof target ("uniqueness of ...") is not a claim that it holds.
PLANNED_GOAL_FILE_SUFFIXES = ('advisor/roadmap.json', 'network.json')


def relpath(p):
    try:
        return str(p.relative_to(K.ROOT))
    except ValueError:
        return str(p)


def topic_relevant(window_lower):
    return any(m in window_lower for m in TOPIC_MARKERS)


CITATION_YEAR_RE = re.compile(r'\((?:19|20)\d{2}[a-z]?\)|\b(?:19|20)\d{2}[,;)]')


def looks_like_citation_context(window):
    """True iff window contains an arXiv id or a parenthetical/attached
    publication-year citation (e.g. "(2024)", "JSP 2005", "CMP 2006") --
    evidence a nearby phrase is describing what a CITED external source says,
    not this project's own claim. Not every citation style is "arXiv": this
    corpus also cites journals directly (Nat. Comm., JHEP, PRD, JSP, CMP)."""
    wl = window.lower()
    return 'arxiv' in wl or bool(CITATION_YEAR_RE.search(window))


def quoted_span_in_string(value, start, end):
    """Straight-double-quote pair check scoped to the whole string value (a
    JSON string has no line/paragraph structure of its own to bound a
    window by, and is normally short enough that the whole value is a safe
    scope) -- catches a phrase quoted inside prose a JSON string carries,
    e.g. a skeptic review's own meta-note 'the literal "fraction of the
    problem" misses the template's ...', which `EXCLUSION_PATH_RE` (a
    json_path check) cannot see since this is not a `claim_exclusions` array,
    just a quoted phrase inside an ordinary string value."""
    before, after = value[:start], value[end:]
    return before.count('"') % 2 == 1 and '"' in after


def strip_markdown_emphasis(s):
    return re.sub(r'[*_`]{1,3}', '', s)


def window_has_extra_negation(text, start, end, radius=220):
    window = strip_markdown_emphasis(text[max(0, start - radius):min(len(text), end + radius)]).lower()
    return [c.strip() for c in EXTRA_NEGATION_CUES if c in window]


def in_fenced_code_block(text, pos):
    """True iff pos falls between an odd/even pair of ``` fence markers (a
    markdown fenced code block spans the whole enclosed region, not just one
    line, unlike the single-backtick inline-span check)."""
    fences_before = len(re.findall(r'^```', text[:pos], re.M))
    return fences_before % 2 == 1


def quoted_span_same_line(text, start, end, open_marker, close_marker):
    """True iff [start,end) is enclosed by a same-line pair open_marker...
    close_marker (assistant-4's single-backtick `in_code_span` convention: a
    markdown inline code span, in this corpus, never wraps a line)."""
    line_start = text.rfind('\n', 0, start) + 1
    line_end = text.find('\n', end)
    if line_end == -1:
        line_end = len(text)
    line = text[line_start:line_end]
    rel_start, rel_end = start - line_start, end - line_start
    before, after = line[:rel_start], line[rel_end:]
    return before.count(open_marker) % 2 == 1 and open_marker in after


def paragraph_bounds(text, pos):
    """The blank-line-delimited paragraph containing pos (source prose wraps
    at the column width, not at every sentence, so a quoted phrase can span a
    single `\\n` line break -- confirmed in `papers/round32-addendum/
    history.tex` lines 156-157, where a LaTeX ``...'' quote's closing '' falls
    on the next physical line; a line-scoped check alone misses it)."""
    start = text.rfind('\n\n', 0, pos)
    start = 0 if start == -1 else start + 2
    end = text.find('\n\n', pos)
    end = len(text) if end == -1 else end
    return start, end


def quoted_span_in_paragraph(text, start, end, open_marker, close_marker):
    """Paragraph-scoped (not line-scoped) quote-pair check, for the quote
    conventions this corpus' prose actually wraps across a line break with:
    straight double quotes and, in .tex files, LaTeX's ``...'' idiom."""
    p_start, p_end = paragraph_bounds(text, start)
    para = text[p_start:p_end]
    rel_start, rel_end = start - p_start, end - p_start
    before, after = para[:rel_start], para[rel_end:]
    if open_marker == close_marker:
        return before.count(open_marker) % 2 == 1 and open_marker in after
    return (open_marker in before and close_marker in after
           and before.rfind(open_marker) > before.rfind(close_marker))


def in_excluded_by_contract_table(text, pos):
    """True iff pos falls inside a LaTeX `longtable`/`tabular` environment
    whose header text names it an exclusion table ("excluded by the
    contract", "not claimed" -- `papers/round32-addendum/limits.tex`'s
    `tab:limits-gates` table, column 4, "Excluded by the contract": a cell in
    a table column with that header is exactly the LaTeX-table analogue of a
    JSON `claim_exclusions` array, but has no per-cell quoting to detect the
    way `EXCLUSION_PATH_RE` detects a JSON array by its key name."""
    begin = max(text.rfind('\\begin{longtable}', 0, pos), text.rfind('\\begin{tabular}', 0, pos))
    if begin == -1:
        return False
    end_lt = text.find('\\end{longtable}', begin)
    end_tb = text.find('\\end{tabular}', begin)
    ends = [e for e in (end_lt, end_tb) if e != -1]
    end = min(ends) if ends else -1
    if end == -1 or end < pos:
        return False
    header = text[begin:min(pos, begin + 2000)].lower()
    return 'excluded by the contract' in header or 'not claimed' in header


def is_quoted_or_coded(text, start, end, is_tex):
    if in_fenced_code_block(text, start):
        return True, 'fenced_code_block'
    if quoted_span_same_line(text, start, end, '`', '`'):
        return True, 'backtick_span'
    if quoted_span_in_paragraph(text, start, end, '"', '"'):
        return True, 'double_quote_span'
    if is_tex and quoted_span_in_paragraph(text, start, end, '``', "''"):
        return True, 'latex_quote_span'
    if is_tex and in_excluded_by_contract_table(text, start):
        return True, 'excluded_by_contract_table_cell'
    return False, None


def topic_window(text, start, end, is_tex, radius=200):
    """The text used to test topic-relevance markers near a match: the
    ordinary +/-radius character window, narrowed to the current LaTeX
    `\\item` when one is nearby -- a bulleted `\\item` list (e.g.
    `papers/round32-addendum/main.tex`'s highlights list) packs one
    independent clause per item, so a fixed character radius alone can bleed
    in the NEXT, unrelated item's own on-topic vocabulary (confirmed: AX1's
    own "unique ground state" clause sits close enough before AY1's own
    "Local closeness of subsequential limits" clause that a naive 200-char
    window wrongly treated AX1's ground-state uniqueness as on-topic)."""
    lo, hi = max(0, start - radius), min(len(text), end + radius)
    if is_tex:
        item_left = text.rfind('\\item', 0, start)
        item_right = text.find('\\item', end)
        if item_left != -1:
            lo = max(lo, item_left)
        if item_right != -1:
            hi = min(hi, item_right)
    return text[lo:hi]


def classify_text_occurrence(text, start, end, phrase_id, is_tex):
    quoted, quote_kind = is_quoted_or_coded(text, start, end, is_tex)
    if quoted:
        return 'excluded_list_or_code_span', ['quoted:' + quote_kind]
    kind, cues = K.classify_phrase_occurrence(text, start, end)
    # K.classify_phrase_occurrence only returns a "negated" reading when it is
    # ALSO in a code span (assistant-4's narrower rule, kept for continuity);
    # since quoting is already handled above, re-derive negation on its own.
    window = text[max(0, start - 200):min(len(text), end + 200)]
    base_cues = [c for c in K.PHRASE_NEGATION_CUES if c in strip_markdown_emphasis(window).lower()]
    extra_cues = window_has_extra_negation(text, start, end)
    all_cues = base_cues + extra_cues
    if all_cues:
        return 'negated_in_prose', all_cues
    return 'AFFIRMATIVE_needs_review', []


def sha256_of(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# Markdown / tex scan (one representative path per distinct content).
# ---------------------------------------------------------------------------
def scan_text_file(path, also_at):
    text = K.load_text(path)
    relp = relpath(path)
    is_tex = path.suffix == '.tex'
    is_methods_ref = '/methods/' in relp.replace('\\', '/')
    is_literature_file = any(marker in relp for marker in LITERATURE_FILE_MARKERS)
    hits = []
    for phrase_id, pattern in K.FORBIDDEN_PHRASE_PATTERNS_R5.items():
        for m in pattern.finditer(text):
            if phrase_id == 'bare_unique' and K.sentence_has_not(text, m.start()):
                continue  # the round's own rule's literal trigger: 'not'/"n't" already in the same sentence
            kind, cues = classify_text_occurrence(text, m.start(), m.end(), phrase_id, is_tex)
            if kind == 'AFFIRMATIVE_needs_review' and phrase_id == 'bare_unique':
                immediate_after = text[m.end():m.end() + 30].lower().lstrip()
                if any(immediate_after.startswith(f) for f in IMMEDIATE_GROUND_STATE_FOLLOWERS):
                    kind = 'off_topic_different_admitted_fact'
                elif any(relp.endswith(suf) for suf in PURE_LITERATURE_FILE_SUFFIXES):
                    kind = 'third_party_literature_description'
                else:
                    window = topic_window(text, m.start(), m.end(), is_tex).lower()
                    if is_literature_file and 'arxiv' in window:
                        kind = 'third_party_literature_description'
                    elif not any(marker in window for marker in ON_TOPIC_UNIQUE_MARKERS):
                        kind = 'off_topic_different_admitted_fact'
            if kind == 'AFFIRMATIVE_needs_review' and phrase_id == 'predicts':
                window = text[max(0, m.start() - 90):min(len(text), m.end() + 90)].lower()
                if is_methods_ref or not topic_relevant(window):
                    kind = 'off_topic_ordinary_usage'
            # General, phrase-independent fallback: any remaining AFFIRMATIVE
            # hit in a literature-survey file, next to a recognisable citation
            # (an arXiv id or a publication-year marker), is describing a
            # CITED source's own claim, not this project's -- checked last so
            # a phrase-specific rule above (e.g. bare_unique's own, tighter
            # arXiv-only check) still applies first where it is more precise.
            if kind == 'AFFIRMATIVE_needs_review' and is_literature_file:
                window = text[max(0, m.start() - 200):min(len(text), m.end() + 200)]
                if looks_like_citation_context(window):
                    kind = 'third_party_literature_description'
            line = text.count('\n', 0, m.start()) + 1
            context = text[max(0, m.start() - 120):min(len(text), m.end() + 120)].replace('\n', ' ').strip()
            hits.append({'phrase': phrase_id, 'matched_text': m.group(0), 'line': line, 'context': context,
                        'classification': kind, 'cues': cues})
    for m in K.MASS_GAP_RE.finditer(text):
        start = 0
        for sep in '.;\n':
            i = text.rfind(sep, 0, m.start())
            if i > start:
                start = i
        end = len(text)
        for sep in '.;\n':
            i = text.find(sep, m.start())
            if i != -1 and i < end:
                end = i
        sentence = text[start:end]
        if K.SOLVES_SOLVED_RE.search(sentence):
            kind, cues = classify_text_occurrence(text, m.start(), m.end(), 'mass_gap', is_tex)
            line = text.count('\n', 0, m.start()) + 1
            hits.append({'phrase': 'solves_or_solved_near_mass_gap', 'matched_text': sentence.strip(),
                        'line': line, 'context': sentence.strip()[:240], 'classification': kind, 'cues': cues})
    return {'path': relp, 'also_at': [relpath(p) for p in also_at], 'kind': 'markdown_or_tex',
            'is_methods_reference': is_methods_ref, 'is_literature_file': is_literature_file, 'occurrences': hits}


# ---------------------------------------------------------------------------
# JSON scan (one representative path per distinct content).
# ---------------------------------------------------------------------------
def scan_json_file(path, also_at):
    relp = relpath(path)
    try:
        data = K.load_json(path)
    except Exception as exc:
        return {'path': relp, 'also_at': [relpath(p) for p in also_at], 'kind': 'json', 'occurrences': [],
                'load_error': str(exc)}
    hits = []
    for str_path, value in K.walk_all_strings(data):
        for phrase_id, pattern in K.FORBIDDEN_PHRASE_PATTERNS_R5.items():
            for m in pattern.finditer(value):
                if phrase_id == 'bare_unique' and K.sentence_has_not(value, m.start()):
                    continue
                if EXCLUSION_PATH_RE.search(str_path):
                    kind, cues = 'excluded_list_or_code_span', ['json_exclusion_array_path']
                elif SCAN_METADATA_PATH_RE.search(str_path):
                    kind, cues = 'scan_or_review_metadata_field', ['json_scan_metadata_path']
                elif OBLIGATIONS_PATH_RE.search(str_path):
                    kind, cues = 'obligations_table_entry', []
                elif MUTATION_OR_CONTROL_PATH_RE.search(str_path):
                    kind, cues = 'mutation_or_control_description', []
                elif phrase_id == 'bare_unique' and any(relp.endswith(suf) for suf in PLANNED_GOAL_FILE_SUFFIXES):
                    kind, cues = 'roadmap_or_network_planned_item_title', ['planned_not_executed_file:' + relp]
                elif any(relp.endswith(suf) for suf in PURE_LITERATURE_FILE_SUFFIXES):
                    kind, cues = 'third_party_literature_description', ['pure_literature_ledger_file:' + relp]
                elif quoted_span_in_string(value, m.start(), m.end()):
                    kind, cues = 'excluded_list_or_code_span', ['quoted_within_json_string_value']
                else:
                    window = strip_markdown_emphasis(str_path + ' ' + value).lower()
                    cues = [c for c in K.PHRASE_NEGATION_CUES if c in window]
                    cues += [c.strip() for c in EXTRA_NEGATION_CUES if c in window]
                    immediate_after = value[m.end():m.end() + 30].lower().lstrip()
                    if cues:
                        kind = 'negated_in_prose'
                    elif phrase_id == 'predicts' and not topic_relevant(
                            value[max(0, m.start() - 90):m.end() + 90].lower()):
                        kind = 'off_topic_ordinary_usage'
                    elif phrase_id == 'bare_unique' and any(
                            immediate_after.startswith(f) for f in IMMEDIATE_GROUND_STATE_FOLLOWERS):
                        kind = 'off_topic_different_admitted_fact'
                    elif phrase_id == 'bare_unique' and not any(
                            marker in window for marker in ON_TOPIC_UNIQUE_MARKERS):
                        kind = 'off_topic_different_admitted_fact'
                    elif looks_like_citation_context(value[max(0, m.start() - 150):m.end() + 150]):
                        kind = 'third_party_literature_description'
                    else:
                        kind = 'AFFIRMATIVE_needs_review'
                hits.append({'phrase': phrase_id, 'json_path': str_path, 'matched_text': m.group(0),
                            'value_excerpt': value[max(0, m.start() - 100):min(len(value), m.end() + 100)],
                            'classification': kind, 'cues': cues})
        for m in K.MASS_GAP_RE.finditer(value):
            start = 0
            for sep in '.;':
                i = value.rfind(sep, 0, m.start())
                if i > start:
                    start = i
            end = len(value)
            for sep in '.;':
                i = value.find(sep, m.start())
                if i != -1 and i < end:
                    end = i
            sentence = value[start:end]
            if K.SOLVES_SOLVED_RE.search(sentence):
                if EXCLUSION_PATH_RE.search(str_path):
                    kind = 'excluded_list_or_code_span'
                else:
                    window = strip_markdown_emphasis(str_path + ' ' + value).lower()
                    kind = 'negated_in_prose' if any(c in window for c in K.PHRASE_NEGATION_CUES) else \
                        'AFFIRMATIVE_needs_review'
                hits.append({'phrase': 'solves_or_solved_near_mass_gap', 'json_path': str_path,
                            'matched_text': sentence.strip(), 'value_excerpt': sentence.strip()[:240],
                            'classification': kind, 'cues': []})
    return {'path': relp, 'also_at': [relpath(p) for p in also_at], 'kind': 'json', 'occurrences': hits}


def dedupe_by_content(paths):
    """Groups paths by SHA-256 content hash; returns a list of
    (representative_path, [other_paths_with_identical_content]), representative
    chosen as the lexicographically-first path for determinism."""
    groups = {}
    for p in paths:
        groups.setdefault(sha256_of(p), []).append(p)
    out = []
    for h, group in groups.items():
        group_sorted = sorted(group, key=lambda p: str(p))
        out.append((group_sorted[0], group_sorted[1:]))
    return sorted(out, key=lambda t: str(t[0]))


def run():
    md_tex_paths = [p for p in K.round_wide_md_and_json_paths() if p.suffix == '.md']
    md_tex_paths += K.addendum_tex_paths()
    md_tex_paths += K.extra_readme_paths()
    md_tex_paths = sorted(set(md_tex_paths))
    json_paths = sorted(p for p in K.round_wide_md_and_json_paths() if p.suffix == '.json')

    def excluded(p):
        return SELF_DIR in p.parents

    md_tex_paths = [p for p in md_tex_paths if not excluded(p)]
    json_paths = [p for p in json_paths if not excluded(p)]

    md_tex_groups = dedupe_by_content(md_tex_paths)
    json_groups = dedupe_by_content(json_paths)

    file_results = []
    for rep, dupes in md_tex_groups:
        file_results.append(scan_text_file(rep, dupes))
    for rep, dupes in json_groups:
        file_results.append(scan_json_file(rep, dupes))

    all_occurrences = []
    for fr in file_results:
        for occ in fr.get('occurrences', []):
            row = dict(occ)
            row['file'] = fr['path']
            row['also_at'] = fr['also_at']
            row['file_kind'] = fr['kind']
            all_occurrences.append(row)

    by_phrase = {}
    for occ in all_occurrences:
        by_phrase.setdefault(occ['phrase'], []).append(occ)
    counts = {}
    for phrase, occs in by_phrase.items():
        c = {}
        for occ in occs:
            c[occ['classification']] = c.get(occ['classification'], 0) + 1
        raw_path_total = sum(1 + len(occ['also_at']) for occ in occs)
        counts[phrase] = {'unique_content_occurrences': len(occs), 'raw_path_occurrences': raw_path_total,
                          'by_classification': c}

    affirmative_defects = [occ for occ in all_occurrences if occ['classification'] == 'AFFIRMATIVE_needs_review']
    first_certified_hits = [occ for occ in all_occurrences if occ['phrase'] == 'first_certified']

    findings = []
    findings.append('Scanned %d distinct-content markdown/tex file(s) (%d total path(s) before dedup) and %d '
                    'distinct-content JSON file(s) (%d total path(s)) under research/round32/**, '
                    'papers/round32-addendum/*.tex and the two README.md files. This script\'s own directory '
                    '(experts/jung/assistant-5/) is excluded from the swept set (see module docstring).'
                    % (len(md_tex_groups), len(md_tex_paths), len(json_groups), len(json_paths)))
    for phrase, c in sorted(counts.items()):
        findings.append('Phrase %r: %d unique-content occurrence(s) (%d raw path occurrence(s) before content-hash '
                        'dedup), by classification: %r.'
                        % (phrase, c['unique_content_occurrences'], c['raw_path_occurrences'], c['by_classification']))
    if affirmative_defects:
        findings.append('%d occurrence(s) classified AFFIRMATIVE_needs_review (DEFECT):' % len(affirmative_defects))
        for occ in affirmative_defects:
            loc = occ.get('json_path') or ('line %d' % occ.get('line', -1))
            findings.append('  DEFECT: %s :: %s :: %s :: %r' % (occ['file'], loc, occ['phrase'],
                                                                 occ.get('context') or occ.get('value_excerpt')))
    else:
        findings.append('0 occurrences classified AFFIRMATIVE_needs_review across the whole round -- no forbidden-'
                        'phrase defect found by this sweep.')
    findings.append('%d occurrence(s) of "first certified" found (always flagged, per the calling task, regardless '
                    'of classification -- see first_certified_hits in results.json for the full record and the '
                    'README for the git-history check).' % len(first_certified_hits))
    n_off_topic_unique = sum(1 for occ in all_occurrences
                             if occ['phrase'] == 'bare_unique'
                             and occ['classification'] in ('off_topic_different_admitted_fact',
                                                           'third_party_literature_description'))
    if n_off_topic_unique:
        findings.append('%d occurrence(s) of bare unique/uniqueness classified off_topic_different_admitted_fact '
                        'or third_party_literature_description (a DIFFERENT, already-admitted uniqueness fact this '
                        'project itself proved -- a finite-volume Hamiltonian\'s unique ground state, AM2/AQ1\'s own '
                        'theorem, or a contraction map\'s unique fixed point -- or an external paper\'s own claim in '
                        'a literature-survey file; not "the AQ state"/"any subsequential limit" being unique, the '
                        'actually-forbidden sense) -- not counted as a defect; see results.json for the full list.'
                        % n_off_topic_unique)
    n_off_topic_predicts = sum(1 for occ in all_occurrences
                               if occ['phrase'] == 'predicts' and occ['classification'] == 'off_topic_ordinary_usage')
    if n_off_topic_predicts:
        findings.append('%d occurrence(s) of "predicts" classified off_topic_ordinary_usage -- not counted as a '
                        'defect.' % n_off_topic_predicts)
    n_mass_gap_solve = sum(1 for occ in all_occurrences if occ['phrase'] == 'solves_or_solved_near_mass_gap')
    findings.append('%d occurrence(s) of "solves"/"solved" in the same sentence as "mass gap" found (0 expected; '
                    'this project\'s standing claim is that the mass-gap problem remains open).' % n_mass_gap_solve)

    passed = len(affirmative_defects) == 0
    return {
        'id': 'forbidden_phrase_sweep',
        'role': 'whole-round forbidden-phrase sweep (panel-update-4.md item 7, Jung update-4.md section 4 item 4, '
                'calling task item 2); zero research loops; audits only, never admission evidence',
        'files_scanned': {'markdown_or_tex_distinct_content': len(md_tex_groups),
                          'markdown_or_tex_total_paths': len(md_tex_paths),
                          'json_distinct_content': len(json_groups), 'json_total_paths': len(json_paths)},
        'phrase_patterns': sorted(K.FORBIDDEN_PHRASE_PATTERNS_R5) + ['solves_or_solved_near_mass_gap'],
        'counts_by_phrase': counts,
        'affirmative_defects': affirmative_defects,
        'first_certified_hits': first_certified_hits,
        'all_occurrences': all_occurrences,
        'passed': passed,
        'findings': findings,
    }


def main():
    result = run()
    out_path = Path(__file__).resolve().parent / 'results.json'
    K.merge_results(out_path, 'forbidden_phrase_sweep', result)
    print('forbidden_phrase_sweep: %s' % ('PASS (0 affirmative defects)' if result['passed']
                                          else 'FAIL (affirmative defects found)'))
    for f in result['findings']:
        print('  -', f)
    if not result['passed']:
        sys.exit(1)


if __name__ == '__main__':
    main()
