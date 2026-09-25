#!/usr/bin/env python3
"""BC1 post-comparison skeptic checks (statement loop, single forward producer).

Human project author: Hruday N M (BUNZEEY). Model-agent skeptic with correlated ancestry (same model family as the advisor,
the lenses and the producer; the frozen BC1 texts carry the skeptic's pre-freeze edits); not human peer review or formal
verification.

Adds to the frozen pre-comparison package (bc1_check.py; values final at 04:53:13Z, committed at 5ec599f after the forward
commit 5816e0b):
  * integrity: the contract hash; the unchanged pre-comparison package and a byte replay of bc1_check.py; the forward freeze
    closure file by file (44 files); the forward inventory on the real snapshots (40 files, equal to the contract-derived
    list and to the inventory recorded before production, byte-identical to the repository); replays of the producer
    reproducing output/ byte for byte (normal, or -O when this program runs under -O); the frozen artifacts pinned;
  * every producer value against an independent recomputation (never from a producer value): the AV2 datum, radius and
    interval, the AW2 constant, endpoints and mirror, C', N_sign, the widening table, the widened enclosures at both signs,
    the gate margins, the ratio L/(C' q^3), the widened exclusion margin, the tau/100 information, the AV2 consistency
    replays (own Machin pi, own e^{-3} series) and the N4 preview 1/(144 K_2' tau) from the AY2 gate;
  * the obligations table: the producer's 18 rows parsed and reconciled with the skeptic's pre-comparison rows; the
    reviewed table with the O1 decision (closed only in the narrow form; uniqueness of any ground state open);
  * text: the round phrase tool (subprocess) and a mirror on the report, the template once as one unbroken line, every
    clause mentioning uniqueness classified, and fixtures showing the vocabulary gap of the phrase list for the O1 wording;
  * source-edit runs on temporary copies outside the checkout: one validator weakening per contract control (25 runs; the
    producer checker must abort with 'damaging mutation accepted: <label>'), must-abort edits (including the two report
    edits the producer disclosed as formerly silent), and silent edits (the producer's disclosed non-damaging one, and
    three edits of labelled report numbers or the O1 scope that the producer checker does not pin, which this review's
    report validator must catch).

Standard library only; exact Fractions decide every Boolean; failures are explicit exceptions (never assert), so the output
bytes match under python -O.

Usage: python3 -B research/round33/skeptic/bc1_postreview_check.py --output /abs/fresh/dir
"""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction as F
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import bc1_check as pre  # noqa: E402  (the skeptic's own frozen pre-comparison module)

ROOT = HERE.parents[2]
R33 = ROOT / 'research/round33'
CONTRACT = R33 / 'contracts/bc1.json'
CONTRACT_SHA = '3fb84ed3135c48670d26643f120ef2ef74f5888174cf11e7395919e408a279bd'
FWD = R33 / 'forward/bc1'
PRE_SCRIPT = HERE / 'bc1_check.py'
PRE_RESULTS = HERE / 'bc1-independent/results.json'
PRE_FREEZE = HERE / 'bc1-independent-freeze.json'
PHRASE_TOOL = R33 / 'tools/phrase_scan.py'
PHRASE_TOOL_SHA = '1c31a4958c4a44144c5d4f256db551385d216b86309eadc54a608c5e2a4ff0e2'
FROZEN = {  # frozen producer artifacts (sha256 at review time; commit 5816e0b)
    'check.py': '976e08e94920d8420b2ace5cd87c0f7a98bddea7de975c8f0cfbabe5f1833cb8',
    'report.md': 'a455f4eab2bfbebaf7cd72203f6f43028d6c0926218c56c0d8493696e6e40f7f',
    'freeze.json': '6039cfe67b8b002b5891eddea6705625a399d35b506cee497b34aa79fc4c12c4',
    'output/results.json': '3a42525ba369d232a4a8afb82d9a5ffcf69622fd20e33ddb007dba220f0e9958',
    'output/source-manifest.json': '6e3928d9e5eb272dcf26e43a9cafaeb30d06d8ec4b99788e791dd83b813e2f11',
}
AY2_F = 'research/round32/forward/ay2/report.md'
AV2_F = 'research/round32/forward/av2/report.md'
BB2_F = 'research/round33/forward/bb2/report.md'
TAU = F(1, 10 ** 8)
Q = F(1, 64)


class ReviewFailure(RuntimeError):
    """A post-review check failed."""


class Rejected(Exception):
    """The skeptic's report and value validator refused a producer packet."""


CHECKS = []


def need(ok, cid, **detail):
    if ok is not True:
        raise ReviewFailure(cid)
    if any(row['id'] == cid for row in CHECKS):
        raise ReviewFailure('duplicate check id ' + cid)
    row = {'id': cid, 'passed': True}
    row.update(detail)
    CHECKS.append(row)


def q_(x):
    return str(F(x))


def preview(x, digits=12):
    return format(float(x), '.%de' % digits)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def rat(value):
    if isinstance(value, bool) or isinstance(value, float):
        raise Rejected('non-exact value in producer results: ' + repr(value))
    if isinstance(value, int):
        return F(value)
    if isinstance(value, str) and re.fullmatch(r'-?\d+(/\d+)?', value):
        return F(value)
    raise Rejected('malformed exact value: ' + repr(value))


# ------------------------------------------------------------ independent enclosures
def atan_bracket(z, terms=80):
    s, prev = F(0), None
    for k in range(terms + 1):
        prev = s
        s += (-1) ** k * z ** (2 * k + 1) / (2 * k + 1)
    return min(s, prev), max(s, prev)


def pi_bracket():
    a, b = atan_bracket(F(1, 5)), atan_bracket(F(1, 239))
    return 16 * a[0] - 4 * b[1], 16 * a[1] - 4 * b[0]


def reference():
    """The skeptic's own values from the gates (bc1_check parsers; nothing from the producer)."""
    gates = {rel: json.loads((ROOT / rel).read_text()) for rel in pre.GATES}
    for rel, want in pre.GATES.items():
        if sha(ROOT / rel) != want:
            raise ReviewFailure('gate hash ' + rel)
    av2 = pre.parse_av2(gates['research/round32/advisor/av2-gate.json'])
    aw2 = pre.parse_aw2(gates['research/round32/advisor/aw2-gate.json'])
    bb2 = pre.parse_bb2(gates['research/round33/advisor/bb2-gate.json'])
    cp, lo, hi = bb2['C_prime'], aw2['lo'], aw2['hi']
    ns = pre.n_sign_of(cp, lo)
    rows = {}
    for n in range(2, 9):
        w = cp * Q ** (n - 1)
        rows[n] = {'widening': w, 'lower_plus': lo - w, 'upper_plus': hi + w, 'upper_minus': -lo + w,
                   'certified': (lo - w) > 0 and (-lo + w) < 0}
    ay2 = gates['research/round32/advisor/ay2-gate.json']['accepted']
    k2p = F(re.search(r"K_2'=(\d+/\d+) \(~13417\.5275440\)", ay2).group(1))
    av1 = gates['research/round32/advisor/av1-gate.json']['accepted']
    d_av1 = F(re.search(r"D_ii=(\d+/\d+) \(~1\.3612e-8; exact rational", av1).group(1))
    w4 = rows[ns]['widening']
    kt2 = aw2['K2'] * TAU ** 2
    return {'gates': gates, 'av2': av2, 'aw2': aw2, 'bb2': bb2, 'C_prime': cp, 'N_sign': ns, 'rows': rows,
            'K2_prime': k2p, 'D': d_av1, 'Kt2': kt2,
            'ratio_L_over_w': lo / w4, 'widened_exclusion': rows[ns]['lower_plus'] / (kt2 + w4),
            'n4_sign_margin_preview': 1 / (144 * k2p * TAU), 'n4_exclusion_preview': (TAU / 144 - k2p * TAU ** 2) / (k2p * TAU ** 2)}


# ------------------------------------------------------------ the reviewed obligations table (O1 decision)
O1_NARROW = ('all subsequential limits of F1 and F2 coincide on every finite region (one limit of the named '
             'constructions, omega_inf)')
O1_OPEN = ('uniqueness of any ground state (every infinite-volume ground state), states outside the named constructions '
           'and other boundary conditions')


def reviewed_table(prod_rows):
    """The producer's 18 rows with the O1 row split, plus two rows from Round33 gate limitations (added by review)."""
    by = {r['id']: r for r in prod_rows}
    out = [
        {'id': 'O1a', 'ay2_row': 'O1 (uniqueness of the limit)', 'obligation': O1_NARROW, 'status': 'closed_within_scope',
         'closing_gate_and_scope': 'BB2 gate items 2-3 (every AQ1 and every F2 subsequential limit equals omega_inf on every '
                                   'finite region); scope: the named constructions F1 and F2 only, zero-selected family, '
                                   'fixed spacing, |tau| at most 10^-8, both signs',
         'missing_premise': 'none within the scope', 'candidate_route': 'executed in BB2 (item-1 Cauchy bound, BB1 c3)'},
        {'id': 'O1b', 'ay2_row': 'O1 (uniqueness of the limit), general part', 'obligation': O1_OPEN, 'status': 'open',
         'closing_gate_and_scope': 'none (open)',
         'missing_premise': 'a statement covering every ground state: a two-state estimate or a classification of every '
                            'state in the class (AY2 O1), or a comparison of an arbitrary ground state or boundary '
                            'prescription with omega_inf (row N1)',
         'candidate_route': 'HTW-type local stability or a Dobrushin-type condition with evaluated constants at the cap; or '
                            'a BB1-type comparison for a pre-frozen class of boundary prescriptions (row N1); not executed'},
    ]
    for rid in ['O%d' % k for k in range(2, 7)] + ['N%d' % k for k in range(1, 13)]:
        r = dict(by[rid])
        out.append({'id': rid, 'obligation': r['obligation'], 'status': r['status'],
                    'closing_gate_and_scope': r['closing_gate_and_scope'], 'missing_premise': r['missing_premise'],
                    'candidate_route': r['candidate_route']})
    for row in out:
        if row['id'] == 'N4':
            row['candidate_route'] = row['candidate_route'].replace(
                'about 51.76 (labelled preview, not claimed)',
                'about 51.76 (labelled preview, not claimed and not admitted: it rests on an ungated box-level reading of '
                'AY1 F13-F14 and on the untruncated F2 passage)')
    out += [
        {'id': 'N13', 'obligation': 'analyticity of the reduced density in the coupling (added by review; BA1 and BB1 '
                                    'gate limitations)', 'status': 'open', 'closing_gate_and_scope': 'none (open)',
         'missing_premise': 'a zero-free region of the complexified normalization; the BA1 disc controls coefficients only',
         'candidate_route': 'a lower bound on the complexified norm on the BA1 disc; not formulated'},
        {'id': 'N14', 'obligation': 'untruncated creation coefficients (added by review; BA1 gate limitation)',
         'status': 'open', 'closing_gate_and_scope': 'none (open)',
         'missing_premise': 'coefficient bounds after the on-site cutoff is removed (BA1 is per cutoff space)',
         'candidate_route': 'AM2 section 6 applied to the coefficient collection; not needed by BB1, BB2 or BC1'},
    ]
    return out


# ------------------------------------------------------------ the review's report and value validator
def validate_producer(report, res, ref):
    """Refuse a producer packet whose values, labelled numbers or O1 scope differ from the independent recomputation."""
    hd = res['headline']
    a2, w2 = ref['av2'], ref['aw2']
    if [rat(hd['av2_node']['d']), rat(hd['av2_node']['R'])] != [a2['d'], a2['R']] \
            or [rat(x) for x in hd['av2_node']['interval']] != [a2['lo'], a2['hi']]:
        raise Rejected('AV2 values differ from the gate')
    if rat(hd['aw2_enclosure']['K2_plus']) != w2['K2'] or [rat(x) for x in hd['aw2_enclosure']['plus']] != [w2['lo'], w2['hi']] \
            or [rat(x) for x in hd['aw2_enclosure']['minus']] != [w2['mirror_lo'], w2['mirror_hi']]:
        raise Rejected('AW2 values differ from the gate')
    fb = hd['finite_box_sign']
    ns = ref['N_sign']
    row = ref['rows'][ns]
    if rat(fb['C_prime']) != ref['C_prime'] or rat(fb['q']) != Q or fb['N_sign'] != ns \
            or rat(fb['widening_at_N_sign']) != row['widening']:
        raise Rejected('finite-box constants differ')
    if [rat(x) for x in fb['widened_plus_at_N_sign']] != [row['lower_plus'], row['upper_plus']] \
            or [rat(x) for x in fb['widened_minus_at_N_sign']] != [-row['upper_plus'], -row['lower_plus']]:
        raise Rejected('widened enclosure differs')
    table = {c['id']: c for c in res['checks']}['f2_finite_box_sign_corollary']['table']
    for t in table:
        r = ref['rows'][t['N']]
        if rat(t['widening']) != r['widening'] or rat(t['lower_plus']) != r['lower_plus'] or t['certified'] != r['certified']:
            raise Rejected('widening table differs at N=%d' % t['N'])
    if res['gate_fields'] != ref['gate_fields']:
        raise Rejected('gate fields differ from the contract')
    # labelled report numbers that the producer checker does not pin
    labelled = [(r"The ratio `L/\(C' q\^3\)` is about (\d+\.\d+)", ref['ratio_L_over_w']),
                (r"is about (\d+\.\d+) \(labelled information\)", ref['widened_exclusion']),
                (r"sign margin 1/\(144 K_2' tau\) about (\d+\.\d+) \(labelled preview, not claimed\)", ref['n4_sign_margin_preview'])]
    for pattern, value in labelled:
        m = re.search(pattern, report)
        if m is None:
            raise Rejected('labelled report number missing: ' + pattern)
        digits = len(m.group(1).split('.')[1])
        if abs(F(m.group(1)) - value) > F(1, 2 * 10 ** digits):
            raise Rejected('labelled report number differs from the recomputation: ' + m.group(0)[:60])
    if 'labelled preview, not claimed' not in report:
        raise Rejected('N4 preview without its label')
    o1 = [r for r in res['obligations_table'] if r['id'] == 'O1'][0]
    if 'scope: the named constructions F1 and F2 only' not in o1['closing_gate_and_scope'] or 'see row N1' not in o1['missing_premise'] \
            or 'uniqueness of every infinite-volume ground state' not in o1['missing_premise']:
        raise Rejected('O1 row without its named-construction scope or its pointer to the open row')
    outside = report.split('## 11. ')[0] + report.split('## 12. ')[1]
    n_signs = [int(x) for cl in pre.clauses(pre.normalize(outside)) if 'rejected' not in cl
               for x in re.findall(r'N_sign ?= ?(\d+)', cl)]
    if any(x != ns for x in n_signs):
        raise Rejected('the report states an N_sign other than the recomputed value')
    return True


# ------------------------------------------------------------ closure, replays, mutation harness
def verify_closure():
    freeze = json.loads((FWD / 'freeze.json').read_text())
    prefix = FWD.relative_to(ROOT).as_posix() + '/'
    sources = freeze['sources']
    files = {p.relative_to(ROOT).as_posix() for p in FWD.rglob('*') if p.is_file() and p != FWD / 'freeze.json'}
    ok = (freeze['loop'] == 'BC1' and freeze['direction'] == 'forward' and freeze['contract_sha256'] == CONTRACT_SHA
          and all(n.startswith(prefix) for n in sources) and set(sources) == files and len(sources) == 44
          and all(sha(ROOT / n) == d for n, d in sources.items())
          and not any('__pycache__' in n or n.endswith('.pyc') for n in files)
          and freeze['normal_optimized_identical'] is True and freeze['independent_before_current_counterpart_exchange'] is True
          and freeze['verdict'].startswith('accepted_within_scope'))
    inputs = sorted(p.relative_to(FWD / 'inputs').as_posix() for p in (FWD / 'inputs').rglob('*') if p.is_file())
    snapshots_equal = all((FWD / 'inputs' / n).read_bytes() == (ROOT / n).read_bytes() for n in inputs)
    return ok, inputs, snapshots_equal, freeze


def replay(script, pre_mode=False):
    with tempfile.TemporaryDirectory(prefix='hnm-r33-bc1-skeptic-replay-') as tmp:
        out = Path(tmp) / 'out'
        flags = ['-B'] + (['-O'] if sys.flags.optimize else [])
        done = subprocess.run([sys.executable] + flags + [str(script), '--output', str(out)],
                              capture_output=True, text=True, cwd=str(ROOT))
        if done.returncode != 0:
            raise ReviewFailure('replay failed: ' + str(script) + ' ' + done.stderr[-300:])
        return {p.relative_to(out).as_posix(): sha(p) for p in sorted(out.rglob('*')) if p.is_file()}, \
            ((out / 'results.json').read_bytes() if pre_mode else None)


def mutated_run(edits=(), report_edits=(), report_append=None, extra_input=None, input_edit=None):
    with tempfile.TemporaryDirectory(prefix='hnm-r33-bc1-skeptic-mut-') as tmp:
        repo = Path(tmp) / 'repo'
        dst = repo / 'research/round33/forward/bc1'
        shutil.copytree(FWD, dst, ignore=shutil.ignore_patterns('output', 'freeze.json', '__pycache__'))
        code = (dst / 'check.py').read_text()
        for old, new in edits:
            if code.count(old) != 1:
                raise ReviewFailure('mutation anchor not unique (%d): %r' % (code.count(old), old[:80]))
            code = code.replace(old, new)
        (dst / 'check.py').write_text(code)
        if report_edits or report_append is not None:
            rp = dst / 'report.md'
            text = rp.read_text()
            for old, new in report_edits:
                if text.count(old) != 1:
                    raise ReviewFailure('report mutation anchor not unique: %r' % old[:70])
                text = text.replace(old, new)
            if report_append is not None:
                text += report_append
            rp.write_text(text)
        if extra_input is not None:
            extra = dst / 'inputs' / extra_input
            extra.parent.mkdir(parents=True, exist_ok=True)
            extra.write_text('skeptic mutation fixture\n')
        if input_edit is not None:
            rel, old, new = input_edit
            ip = dst / 'inputs' / rel
            raw = ip.read_bytes()
            if raw.count(old) != 1:
                raise ReviewFailure('input mutation anchor not unique')
            ip.write_bytes(raw.replace(old, new))
        out = Path(tmp) / 'out'
        flags = ['-B'] + (['-O'] if sys.flags.optimize else [])
        done = subprocess.run([sys.executable] + flags + [str(dst / 'check.py'), '--output', str(out)],
                              capture_output=True, text=True, cwd=str(repo))
        results = json.loads((out / 'results.json').read_text()) if (out / 'results.json').is_file() else None
        report = (dst / 'report.md').read_text()
        last = done.stderr.strip().splitlines()[-1] if done.stderr.strip() else ''
        if any(p.name == '__pycache__' or p.suffix == '.pyc' for p in dst.rglob('*')):
            raise ReviewFailure('interpreter cache written into a mutated copy')
        return done.returncode, results, report, last.replace(tmp, '<tmp>')


def weaken(line):
    head = line[:len(line) - len(line.lstrip())]
    rest = line.lstrip()
    if not rest.startswith('require('):
        raise ReviewFailure('not a require line')
    tail = rest[len('require('):]
    depth, cut, quote, i = 0, None, None, 0
    while i < len(tail):
        ch = tail[i]
        if quote:
            if ch == '\\':
                i += 2
                continue
            if ch == quote:
                quote = None
        elif ch in '\'"':
            quote = ch
        elif ch in '([{':
            depth += 1
        elif ch in ')]}':
            depth -= 1
        elif ch == ',' and depth == 0:
            cut = i
            break
        i += 1
    if cut is None:
        raise ReviewFailure('require line without a message argument')
    return (line, head + 'require(True, ' + tail[cut + 1:].lstrip())


WEAK = [
    ('coherent_evidence_tampering', [weaken("            require(cid in ids and ids[cid]['passed'] is True, 'required control missing or failed: ' + cid)")],
     'control_boolean_flipped_hash_rebound'),
    ('exact_arithmetic_admission', [("        raise AdmissionError('non-exact input rejected: ' + repr(value))", "        return Q(value)")], 'float_input'),
    ('no_priority_or_continuum_claim', [weaken("            require(fl.get(k1) is v1, 'claim flag ' + k1 + ' must be false')")], 'continuum_true'),
    ('changed_model_relabelled', [weaken("        require(mdl['model_id'] == 'AQ_patterned_zero_selected', 'model id')")], 'uniform_route_B_model'),
    ('insufficient_verdict_retained', [weaken("        require(reported == forward_verdict(*args), 'reported verdict differs from the contract acceptance rule')")],
     'differing_constant_relabelled_accepted'),
    ('wrong_delta_alpha_hbar_clock', [weaken("        require(clock == 's=alpha*t_E/hbar' and exponent == 3, 'free Wilson energy 3 in the alpha clock (24 only with u=s/8)')")],
     'exponent_24_with_the_s_clock'),
    ('placeholder_span_rejected', [weaken("        require(not placeholder_spans(list(strings_of(contract_obj)) + extra), 'placeholder span in the contract or packet strings')")],
     'preceding_gate_placeholder_in_contract'),
    ('negation_aware_phrase_scan', [weaken("        require(not affirmative(phrase_hits(text, FORBIDDEN, template)), 'affirmative forbidden phrasing')")],
     'affirmative_thermodynamic_limit'),
    ('parameters_declare_metric_weights_window', [weaken("            require(k1 in p and str(p[k1]).strip(), 'parameters must declare ' + k1)")],
     'window_removed'),
    ('named_construction_not_uniqueness', [weaken("        require(nm['uniqueness_of_ground_state_claimed'] is False, 'no uniqueness of any ground state')")],
     'uniqueness_flag_true'),
    ('common_clock', [weaken("        require(pk['node']['tau'] == pk['enclosure']['tau'] == tau, 'same coupling for the node and the enclosure')")],
     'enclosure_at_tau_over_10'),
    ('topology_named', [weaken("        require(tp['states'] == 'trace norm on B(H_R)' and tp['representations'] == 'GNS strong topology', 'state and representation topologies')")],
     'weak_star_for_states'),
    ('limit_identified_with_aq1_limits', [weaken("        require(steps[0] == ('identify', 'BB2 items 2-3'), 'identification (BB2 items 2-3) first')")],
     'restatement_from_uniform_local_closeness'),
    ('certificate_values_unchanged', [weaken("        require(rs['d'] == d_g and rs['R'] == R_g, 'restated datum or radius differs from the AV2 gate')")],
     'radius_rerounded_up'),
    ('post_hoc_node_rejected', [weaken("        require(nodes == V['nodes'], 'only the preregistered node s=1')")], 'node_s_2'),
    ('finite_box_sign_from_whole_sequence', [weaken("        require(kind == FINITE_BOX['kind'], 'only the BB2 whole-sequence bound (sup over M, then M to infinity) reaches omega_inf')")],
     'n_to_n_plus_1_bound_alone'),
    ('mirror_sign_replay_not_confirmation', [weaken("        require(mr['confirmations'] == 1, 'the minus sign is a replay, never a second confirmation')")],
     'minus_sign_counted_as_second_confirmation'),
    ('reference_unresolved_retained', [weaken("        require(rf['correlation_shift_resolved'] is False, 'no interaction shift of C(s)')")],
     'correlation_shift_resolved_true'),
    ('obligations_table_complete', [weaken("            require(r1['status'] == 'open' and r1['closing_gate_and_scope'] == 'none (open)', 'new row must be open: ' + r1['id'])")],
     'N1_states_outside_marked_closed'),
    ('rate_range_stated', [weaken("        require(not rate_scan(text), 'a rate in N stated without its range: ' + '; '.join(rate_scan(text))[:200])")],
     'unqualified_O_1_over_N'),
    ('round32_gates_untouched', [weaken("            require(sha_bytes(byts[name]) == GATES[name][1] and cross[name], 'Round32 gate bytes differ from the pinned and cross-bound value: ' + name)")],
     'restatement_written_into_the_AV2_gate'),
    ('route_b_not_restated', [weaken("            require(v1 == 'omega_inf of F1 and F2 (AQ_patterned_zero_selected)', 'restated only for the limit of the named constructions: ' + k1)")],
     'av2_restated_for_route_B'),
    ('same_state_not_different_states', [weaken("        require(gg['gns_dynamics_equality_claimed'] is False, 'no equality of GNS dynamics of different states')")],
     'gns_dynamics_equality_true'),
    ('second_order_remainder_kept', [weaken("        require(lo == tau / 144 - Kt2 - w, 'lower endpoint must keep K_2^+ tau^2 and the widening')")],
     'K2_plus_dropped_at_lower_end'),
    ('finite_box_node_only_from_record', [weaken("        require(nc['finite_box_node_claimed'] is False, 'no finite-box node is claimed')")],
     'finite_box_node_claimed_true'),
]
TEMPLATE_ANCHOR = 'For the zero-selected patterned family at tau=10^-8, the limit of the named construction families F1 and F2 admitted in BB2'
MUST_ABORT = [
    ('report_N_sign_claim_site_to_3 (formerly silent, disclosed)', {'report_edits': [('So **`N_sign = 4`**.', 'So **`N_sign = 3`**.')]},
     'the report states an N_sign other than the computed value'),
    ('report_repeated_preview_last_digit (formerly silent, disclosed)',
     {'report_edits': [('the widened lower end is `-9.22954527941e-10`', 'the widened lower end is `-9.22954527942e-10`')]},
     'is not an exact truncation or a quoted gate decimal'),
    ('report_O6_marked_open', {'report_edits': [('| O6 | dynamics of the padded family itself | closed_within_scope |',
                                                 '| O6 | dynamics of the padded family itself | open |')]}, 'AY2 row status: O6'),
    ('report_O1_marked_open (the reviewed status cannot enter the frozen packet)',
     {'report_edits': [('| O1 | uniqueness of the limit | closed_within_scope |', '| O1 | uniqueness of the limit | open |')]},
     'AY2 row status: O1'),
    ('report_row_N3_removed', {'report_edits': [('\n| N3 |', '\n| XX |')]}, 'obligation rows missing, added or reordered'),
    ('report_forbidden_phrase', {'report_append': '\nThe limit of the named constructions is the thermodynamic limit.\n'},
     'affirmative forbidden phrasing'),
    ('report_template_altered', {'report_edits': [(TEMPLATE_ANCHOR, 'For the patterned family, the limit of the named construction families F1 and F2 admitted in BB2')]},
     'the template must appear exactly once'),
    ('check_widening_exponent_N', {'edits': [('        return C * qq ** (N - 1)', '        return C * qq ** N')]}, 'failed check f2_finite_box_sign_corollary'),
    ('check_C_prime_union', {'edits': [('    Cp = Cp_acc', '    Cp = Cp_union')]}, 'failed check bb2_whole_sequence_constant'),
    ('input_bb2_gate_edited', {'input_edit': ('research/round33/advisor/bb2-gate.json', b'C\'=4/984375 (about 4.0635e-06; exact_first_order',
                                              b'C\'=4/984376 (about 4.0635e-06; exact_first_order')},
     'gate snapshot hash differs from the pinned value: BB2'),
    ('input_contract_edited', {'input_edit': ('research/round33/contracts/bc1.json', b'"N_min": "2"', b'"N_min": "3"')}, 'contract'),
    ('input_undeclared_file', {'extra_input': 'research/round33/forward/bc2/report.md'}, 'failed check premise_inventory_bound'),
]
SILENT = [
    ('producer_disclosed_least_N_rule_L_over_4 (non-damaging)', {'edits': [('        while not (widen(N, C, qq) < lower):',
                                                                           '        while not (widen(N, C, qq) < lower / 4):')]},
     None),
    ('report_O1_scope_widened (O1 scope not pinned by the producer)',
     {'report_edits': [('scope: the named constructions F1 and F2 only', 'scope: every ground state')]},
     'O1 row without its named-construction scope'),
    ('report_N4_preview_changed (labelled number not pinned)', {'report_edits': [('about 51.76', 'about 99.76')]},
     'labelled report number differs from the recomputation'),
    ('report_ratio_L_over_widening_changed (labelled number not pinned)', {'report_edits': [('is about 4.4584', 'is about 9.4584')]},
     'labelled report number differs from the recomputation'),
]


def run(args):
    # 1. contract, pre-comparison package unchanged and replayed ------------------------------------------------------
    need(sha(CONTRACT) == CONTRACT_SHA, 'contract_sha256_pinned', sha256=CONTRACT_SHA)
    pf = json.loads(PRE_FREEZE.read_text())
    ok_pf = pf['contract_sha256'] == CONTRACT_SHA and pf['loop'] == 'BC1' and pf['stage'] == 'pre_comparison' \
        and all(sha(ROOT / p) == h for p, h in pf['files'].items())
    _, pre_bytes = replay(PRE_SCRIPT, pre_mode=True)
    need(ok_pf and pre_bytes == PRE_RESULTS.read_bytes(), 'pre_comparison_package_unchanged_and_replayed',
         freeze=pf['files'], note='the committed pre-comparison package (5ec599f) is unchanged; bc1_check.py reproduces '
                                  'bc1-independent/results.json byte for byte in this interpreter mode')

    # 2. closure, inventory, replays, pinned artifacts -----------------------------------------------------------------
    ok, inputs, snaps, freeze = verify_closure()
    con = json.loads(CONTRACT.read_text())
    declared = sorted(set(['AGENTS.md', 'research/round33/contracts/bc1.json'] + con['shared_premises']))
    need(ok and inputs == declared and snaps and inputs == sorted(pre.OBSERVED_INPUTS)
         and all(sha(FWD / 'inputs' / n) == pre.OBSERVED_INPUTS[n] for n in inputs),
         'producer_closure_and_inventory', closure_files=len(freeze['sources']), inputs=len(inputs),
         note='44 closure files verified one by one; 40 inputs equal the contract-derived list and the inventory recorded '
              'before production; every snapshot byte-identical to the repository')
    need(all(sha(FWD / p) == h for p, h in FROZEN.items()), 'frozen_artifacts_pinned', pinned=FROZEN)
    outs, _ = replay(FWD / 'check.py')
    frozen_out = {p: sha(FWD / 'output' / p) for p in ('results.json', 'source-manifest.json')}
    need(outs == frozen_out and frozen_out['results.json'] == FROZEN['output/results.json']
         and frozen_out['source-manifest.json'] == FROZEN['output/source-manifest.json'],
         'producer_replay_byte_identical', outputs=outs,
         note='the producer replay in this interpreter mode (-B, or -B -O when this program runs under -O) reproduces output/')
    res = json.loads((FWD / 'output/results.json').read_text())
    report = (FWD / 'report.md').read_text()

    # 3. values against the independent recomputation -------------------------------------------------------------------
    ref = reference()
    ref['gate_fields'] = con['preregistration']['gate_fields_required']
    pre_res = json.loads(PRE_RESULTS.read_text())
    need(validate_producer(report, res, ref) is True and pre_res['finite_box_sign']['N_sign'] == ref['N_sign'] == 4
         and pre_res['restated']['av2']['R'] == q_(ref['av2']['R']) and pre_res['restated']['aw2']['plus'] == [q_(ref['aw2']['lo']), q_(ref['aw2']['hi'])],
         'producer_values_equal_independent_recomputation',
         N_sign=ref['N_sign'], C_prime=q_(ref['C_prime']),
         widened_plus_at_N_sign=[q_(ref['rows'][4]['lower_plus']), q_(ref['rows'][4]['upper_plus'])],
         previews={'ratio_L_over_widening': preview(ref['ratio_L_over_w'], 8), 'widened_exclusion_margin': preview(ref['widened_exclusion'], 8),
                   'N4_sign_margin_preview': preview(ref['n4_sign_margin_preview'], 8)},
         note='every restated rational, the widening table N=2..8, the widened enclosures at both signs, the gate fields and '
              'three labelled report numbers equal the recomputation; the pre-comparison prediction (N_sign=4) holds')
    hd = res['headline']['aw2_enclosure']
    need(F(hd['exclusion_margin_preview']) - ref['aw2']['exclusion_margin'] < F(1, 10 ** 5)
         and abs(F(hd['sign_margin_preview']) - ref['aw2']['sign_margin']) < F(1, 10 ** 5), 'producer_gate_margins',
         exclusion=hd['exclusion_margin_preview'], sign=hd['sign_margin_preview'])
    # AV2 consistency replays with own pi and e^{-3}
    pi_lo, pi_hi = pi_bracket()
    av2f = (ROOT / AV2_F).read_text()
    m = re.search(r'\| `kernel_dynamics` = `k M_1\^\+` = `49\|tau\|/pi\^-` \| `(\d+)/(\d+)` \|', av2f)
    k_fwd = F(int(m.group(1)), int(m.group(2)))
    half = F(1, 4 * 10 ** 40)
    d_, R_ = ref['av2']['d'], ref['av2']['R']
    e_lo_formula = 2 * (ref['D'] + ref['D'] ** 2) + 49 * TAU / pi_lo + half
    e_hi_pi = 2 * (ref['D'] + ref['D'] ** 2) + 49 * TAU / pi_hi + half
    r_fwd = 2 * (ref['D'] + ref['D'] ** 2) + k_fwd + half
    e3 = pre.exp_bracket(3)
    ref_lo, ref_hi = 1 / (4 * e3[1]), 1 / (4 * e3[0])
    dist = max(abs(d_ - ref_lo), abs(d_ - ref_hi))
    need(F(333, 106) < pi_lo < pi_hi < F(355, 113) and e_lo_formula <= R_ and R_ - e_hi_pi < F(1, 10 ** 40)
         and e_hi_pi <= r_fwd <= R_ and R_ - r_fwd < F(1, 10 ** 40) and dist <= F(102, 10 ** 45),
         'producer_consistency_replays_reproduced', R_minus_formula=preview(R_ - e_hi_pi, 4), R_minus_forward=preview(R_ - r_fwd, 4),
         d_minus_reference=preview(dist, 4), note='own Machin pi (alternating partial sums) and own e^3 series: the producer '
                                                  'statements (below 10^-40; |d-e^{-3}/4| at most 1.02e-43) hold')
    # N4 preview and its premise
    ay2f = (ROOT / AY2_F).read_text()
    ay2g = ref['gates']['research/round32/advisor/ay2-gate.json']['accepted']
    n4_ok = ('AY1 forward F13 is an exact decomposition of `r_R=rho_R-P_R-rho^(1)_R` in every box of either family at every cutoff `L>=24`' in ay2f
             and 'uniformly in `N`, cutoff and family' in ay2f and 'for a chosen subsequential limit of either family, every one separately' in ay2g
             and 'Tr(rho^(1)_R W)=+tau/144' in ay2g)
    need(n4_ok and F(5175, 100) < ref['n4_sign_margin_preview'] < F(5176, 100), 'n4_preview_recomputed_and_labelled',
         K2_prime=q_(ref['K2_prime']), sign_margin_preview=preview(ref['n4_sign_margin_preview'], 8),
         exclusion_margin_preview=preview(ref['n4_exclusion_preview'], 8),
         note='1/(144 K_2\' tau) from the AY2 gate K_2\'; the box-level form of the AY1 remainder (F13-F14) is quoted in the '
              'AY2 forward report but the gates admit K_2\' for subsequential limits only, so the preview is a labelled '
              'reading of an ungated route: admissible as a labelled candidate-route number, not as a claim')
    bb2f = (ROOT / BB2_F).read_text()
    a_n, n_first = F(0), 1
    while a_n <= 4:
        n_first += 1
        a_n += F(1, n_first)
    a119 = sum((F(1, k) for k in range(2, 120)), F(0))
    need('exceeds 4 at `N=119`' in bb2f and n_first == 83 and a119 > 4, 'premise_observation_P1',
         first_exceedance=n_first, a_119=preview(a119, 6),
         note='the BB2 forward sentence is literally true (a_119 > 4) but reads as a first exceedance; the first is N=83; no '
              'BB2 constant or gate text depends on it')

    # 4. obligations: the producer rows, the reconciliation and the reviewed table -------------------------------------
    prows = res['obligations_table']
    ids = [r['id'] for r in prows]
    pre_rows = {r['id']: r for r in pre_res['obligations']}
    mapping = {'N1': 'N1', 'N2': 'N2', 'N3': 'N3', 'N4': 'N4', 'N5': 'N5', 'N6': 'N6', 'N7': 'N7', 'N8': 'N8', 'N9': 'N9',
               'N10': 'N12', 'N11': 'N13'}
    rev = reviewed_table(prows)
    gtext = {k: re.sub(r'\s+', ' ', g['accepted'] + ' ' + g['decision']) for k, g in ref['gates'].items()}
    need(ids == ['O%d' % k for k in range(1, 7)] + ['N%d' % k for k in range(1, 13)]
         and [r['status'] for r in prows[:6]] == ['closed_within_scope'] * 6 and all(r['status'] == 'open' for r in prows[6:])
         and pre_rows['O1']['status'] == 'open' and all(pre_rows['O%d' % k]['status'] == 'closed_within_scope' for k in range(2, 7))
         and all(pre_rows[v]['status'] in ('open', 'pending_bc2_gate') for v in mapping.values())
         and 'N12' in ids and 'an interaction shift, sign or coefficient of the Euclidean correlation C(s)' in prows[17]['obligation']
         and [r['id'] for r in rev][:2] == ['O1a', 'O1b'] and len(rev) == 21
         and 'this limit coincides with every AQ1 subsequential limit and every F2 subsequential limit' in gtext['research/round33/advisor/bb2-gate.json']
         and 'AY2 row O6 closed within scope' in gtext['research/round33/advisor/ba2-gate.json'],
         'obligations_reconciled',
         producer_rows=len(prows), skeptic_pre_rows=len(pre_rows), reviewed_rows=len(rev),
         agreement='O2-O6 closed within the same gates and scopes; N1-N9 identical in content; producer N10/N11 = skeptic N12/N13',
         differences={'O1': 'producer closed_within_scope, skeptic open; reviewed: split (O1a closed in the narrow form, O1b open)',
                      'producer_only': 'N12 (interaction shift of C(s), carried from Round32): kept',
                      'skeptic_only': 'analyticity of the reduced density, untruncated creation coefficients: added as N13, N14'},
         reviewed_table=rev)

    # 5. text: phrase tool, template, the uniqueness clauses ------------------------------------------------------------
    need(sha(PHRASE_TOOL) == PHRASE_TOOL_SHA, 'phrase_tool_pinned')
    done = subprocess.run([sys.executable, '-B', str(PHRASE_TOOL), str(CONTRACT), str(FWD / 'report.md')],
                          capture_output=True, text=True, cwd=str(ROOT))
    tool_out = json.loads(done.stdout)
    template = con['preregistration']['mandatory_sentence_template']
    forbidden = pre.ROUND_FORBIDDEN + con['preregistration']['forbidden_phrasings']
    mirror_hits = pre.affirmative_hits(report, forbidden, template)
    need(done.returncode == 0 and list(tool_out.values()) == [[]] and mirror_hits == []
         and pre.normalize(report).count(pre.normalize(template)) == 1
         and sum(1 for ln in report.splitlines() if ln.strip() == template) == 1
         and res['mandatory_sentence']['template_verbatim'] == template, 'phrase_scan_and_template',
         tool_exit=done.returncode, template_lines=1)
    sec11 = report.split('## 11. ', 1)[1].split('\n## 12. ', 1)[0]
    uniq = []
    for part, text in (('section 11 (damaging-mutation descriptions)', sec11), ('rest of the report', report.replace(sec11, ''))):
        for cl in pre.clauses(pre.normalize(text)):
            if not re.search(r'unique', cl, re.I):
                continue
            if part.startswith('section 11'):
                kind = 'description of a rejected damaging mutation'
            elif 'uniqueness of the limit | closed_within_scope' in cl:
                kind = 'O1 row name with status closed_within_scope'
            elif pre.NEGATION.search(cl) or 'stays excluded' in cl:
                kind = 'negated or excluded'
            elif 'see row N1' in cl:
                kind = 'pointer to the open row N1'
            elif 'claim exclusions (verbatim)' in cl:
                kind = 'claim-exclusion list quoted verbatim'
            elif re.search(r'uniqueness_of_ground_state_claimed|named_construction_not_uniqueness', cl):
                kind = 'field or control identifier'
            else:
                kind = 'other'
            uniq.append({'clause': cl[:160], 'kind': kind})
    others = [u for u in uniq if u['kind'] == 'other']
    o1_hits = [u for u in uniq if u['kind'].startswith('O1 row')]
    gap = {
        'O1 row wording, affirmative': pre.affirmative_hits('O1 uniqueness of the limit is closed within scope.', forbidden),
        'every-ground-state wording, affirmative': pre.affirmative_hits('Uniqueness of every infinite-volume ground state is proved.', forbidden),
        'listed wording, affirmative': pre.affirmative_hits('Uniqueness of the infinite-volume ground state is proved.', forbidden),
        'listed wording, negated': pre.affirmative_hits('This is not uniqueness of the infinite-volume ground state.', forbidden),
    }
    need(not others and len(o1_hits) == 1 and gap['O1 row wording, affirmative'] == [] and gap['every-ground-state wording, affirmative'] == []
         and gap['listed wording, affirmative'] != [] and gap['listed wording, negated'] == [],
         'uniqueness_wording_classified', clauses=uniq, vocabulary_gap_fixture={k: v for k, v in gap.items()},
         note='every uniqueness clause in the report is negated or excluded, a field or control identifier, or the single O1 '
              'row "uniqueness of the limit | closed_within_scope"; the phrase list does not contain the O1 wording or '
              '"uniqueness of every infinite-volume ground state", so the negation-aware scan is silent on them by '
              'vocabulary, not by negation: the scan cannot guard the O1 row, the reviewed wording does')

    # 6. source-edit runs --------------------------------------------------------------------------------------------------
    weak_rows = []
    for cid, edits, label in WEAK:
        rc, _, _, last = mutated_run(edits=edits)
        if rc == 0 or ('damaging mutation accepted: ' + label) not in last:
            raise ReviewFailure('weakening of %s not exposed: %s' % (cid, last))
        weak_rows.append({'control': cid, 'exposed_mutation': label})
    need(sorted(w['control'] for w in weak_rows) == sorted(con['controls']), 'control_validator_weakenings',
         runs=len(weak_rows), rows=weak_rows,
         note='one validator weakened per contract control on a temporary copy; each run aborts with the expected '
              '"damaging mutation accepted" label')
    abort_rows = []
    for label, kw, expect in MUST_ABORT:
        rc, _, _, last = mutated_run(**kw)
        if rc == 0 or expect not in last:
            raise ReviewFailure('must-abort edit ran or aborted elsewhere: %s: %s' % (label, last))
        abort_rows.append({'edit': label, 'aborted_with': expect})
    need(len(abort_rows) == len(MUST_ABORT), 'must_abort_edits', runs=len(abort_rows), rows=abort_rows)
    silent_rows = []
    for label, kw, expect in SILENT:
        rc, out_res, out_report, last = mutated_run(**kw)
        if rc != 0 or out_res is None:
            raise ReviewFailure('silent edit aborted: %s: %s' % (label, last))
        if expect is None:
            same = {k: v for k, v in out_res.items() if k not in ('check_py_sha256_recorded_before_evaluation', 'checks')} == \
                {k: v for k, v in res.items() if k not in ('check_py_sha256_recorded_before_evaluation', 'checks')}
            if not same or validate_producer(out_report, out_res, ref) is not True:
                raise ReviewFailure('non-damaging silent edit changed an exported value')
            silent_rows.append({'edit': label, 'producer': 'ran', 'review_validator': 'accepted (non-damaging: every exported '
                                                                                      'value unchanged, N_sign=4)'})
            continue
        try:
            validate_producer(out_report, out_res, ref)
        except Rejected as exc:
            if expect not in str(exc):
                raise ReviewFailure('silent edit rejected for the wrong reason: ' + str(exc))
            silent_rows.append({'edit': label, 'producer': 'ran', 'review_validator': 'rejected: ' + expect})
            continue
        raise ReviewFailure('silent edit not caught by the review validator: ' + label)
    need(len(silent_rows) == len(SILENT), 'silent_edits_accounted', rows=silent_rows)

    n_mut = sum(len(c.get('rows', [])) for c in CHECKS if c['id'] in ('control_validator_weakenings', 'must_abort_edits',
                                                                        'silent_edits_accounted'))
    return {
        'loop': 'BC1', 'stage': 'post_comparison', 'human_author': 'Hruday N M (BUNZEEY)',
        'reviewer': 'skeptic (model agent, correlated ancestry; not human review)',
        'contract_sha256': CONTRACT_SHA, 'producer': 'forward (single producer, statement+skeptic)',
        'o1_decision': {'producer': 'O1 uniqueness of the limit: closed_within_scope (BB2 items 2-3; scope the named constructions; '
                                    'beyond it row N1)',
                        'reviewed': 'O1 is closed only in the narrow form "' + O1_NARROW + '" (row O1a); "' + O1_OPEN +
                                    '" remains open (row O1b, with N1); the producer status and its verdict sentence "AY2 rows '
                                    'O1-O6 are closed within named scopes" are not adopted for the gate text'},
        'source_edit_runs': n_mut,
        'checks': CHECKS,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    out = Path(args.output)
    if not out.is_absolute():
        raise SystemExit('--output must be an absolute path')
    if out.exists() and any(out.iterdir()):
        raise SystemExit('--output must be fresh (absent or empty)')
    result = run(args)
    out.mkdir(parents=True, exist_ok=True)
    (out / 'results.json').write_text(json.dumps(result, indent=2, sort_keys=True, default=str) + '\n')
    print(json.dumps({'checks': len(result['checks']), 'source_edit_runs': result['source_edit_runs']}))


if __name__ == '__main__':
    main()
