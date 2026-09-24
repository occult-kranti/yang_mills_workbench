#!/usr/bin/env python3
"""AY2 post-comparison skeptic checks, written after the single forward producer froze.

Human project author: Hruday N M (BUNZEEY). Model-agent skeptic with correlated
ancestry (same model family as the advisor and the producer; the skeptic's own AY1
review, a shared premise, already lists the obligations and the two-sided tier);
not human peer review or formal verification.

AY2 is a statement+skeptic loop (producers=["forward"],
single_direction_independent_replay): admission rests on the forward producer plus
the skeptic's frozen pre-comparison package (ay2_check.py,
ay2-independent/results.json). This file adds:
  * integrity: contract and AY1 gate hashes; the forward closure file by file
    (replay_loop.verify_freeze, imported unchanged) with the frozen hashes
    pinned; the 23-file premise inventory, each byte-identical to its repository
    source, no skeptic/ay2* input, no reverse/ay2 package; the source manifest;
    the unchanged pre-comparison package and its byte-identical replay;
  * the producer replayed under normal and -O Python into fresh directories
    outside the checkout (byte-for-byte against output/), tools/freeze.py verify.
    replay_loop.py always replays two directions and replay_declared.py accepts
    only direction "single+skeptic", so neither applies unchanged to a
    "statement+skeptic" contract; the same steps are executed here with the
    unchanged replay_loop functions;
  * exact comparison of every producer headline with the skeptic's predictions
    and with own re-derivations (the pre-comparison module is imported from its
    pinned bytes; nothing is imported from the producer): the AY1 constants,
    rho^(1)_R, both directed sqrt(10) brackets (10^-30 producer, 10^-40 skeptic)
    and the resulting tier ends, the relative width and the 1/100 target, the
    +-tau separation, the falsifying witness rebuilt by explicit Haar
    integration (every admitted constraint, including the reset energy), the
    obligations table, the mandatory sentence, a forbidden-phrase scan of
    report.md, gate fields, flags, the 21 controls and their meanings;
  * source-edit mutations on temporary copies of the closure outside the
    checkout: every must-abort edit must abort with the intended message, the
    unmutated copy must reproduce output/ byte for byte, and the silent edits
    are accounted for; this review's own validator rejects damaged packets.

Standard library only; exact Fractions decide every Boolean; failures are explicit
exceptions (never assert), so the output bytes match under python -O.

Usage: python3 -B research/round32/skeptic/ay2_postreview_check.py --output /abs/fresh/dir
"""
import argparse
import hashlib
import importlib.util
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
ROOT = HERE.parents[2]
R32 = ROOT / 'research/round32'
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import replay_loop as base  # noqa: E402  (unchanged shared tool, sha256 e627df04...)

CONTRACT_REL = 'research/round32/contracts/ay2.json'
CONTRACT_SHA = '8e55e8e9d54b26520ab0fa10c1c6a967a616aabb4dc8c47988ff687d14d96b38'
AY1_GATE_REL = 'research/round32/advisor/ay1-gate.json'
AY1_GATE_SHA = 'd1d3f921b1465d6ef3e6d5539dd24ea4f83cbf5e18635fb50f0f8a33a9ac78e5'
AY1_REVIEW_JSON_REL = 'research/round32/skeptic/ay1.json'
AY1_REVIEW_JSON_SHA = 'f04ba8bfdd40cab410eec5d484dcb2e5de6895579c0cf086282756a1faa7b90a'
REPLAY_LOOP_SHA = 'e627df048d9db128ae622dfd5030b887be442645b787d1fb29b4b2fec79ced66'
FWD_REL = 'research/round32/forward/ay2'
FWD = ROOT / FWD_REL
FROZEN = {  # forward closure, as frozen and committed (ce6bca8)
    'freeze.json': 'f2fccf3aa126c2b1a961331fcc2ea13524a1efb03209c7ca6b891b9305488eac',
    'check.py': '2aab3349e4d2c72611f9e9bd8f6a626f1d90d4b188d510aab6b6a7cfe3025345',
    'report.md': '527ce2f2700764d76f98efd245fd5f5fa95444f97ca81e323aaff48fac781e6b',
    'output/results.json': 'a2d55af6a0f87e8525cd7dfbe00fb1b3dbd9ffc467a3ebd9b295f38076723ec5',
    'output/source-manifest.json': 'a5b1286811f34767dce1de9a734661629c24edba9c14a03fb48394b4bcd8e80f',
}
PRE_FREEZE_REL = 'research/round32/skeptic/ay2-independent-freeze.json'
PRE_FREEZE_SHA = '7a22def1565fd20e8cae90ecbd209608a4c8e597276faa0cdfe71a6b2dfae1c7'
PRE_CHECK_REL = 'research/round32/skeptic/ay2_check.py'
PRE_RESULTS_REL = 'research/round32/skeptic/ay2-independent/results.json'
TAU = F(1, 10 ** 8)
FIVE = ('uniqueness_claimed', 'whole_sequence_claimed', 'rate_claimed', 'translation_invariance_claimed',
        'boundary_independence_of_dynamics_claimed')
SIX = FIVE + ('rate_in_N_claimed',)
FLAGS_FALSE = ('continuum_claim', 'uniform_wilson_claim', 'resolved_interaction_shift', 'scientific_priority_verified',
               'weak_coupling_claim')


class ReviewFailure(RuntimeError):
    """A review check failed."""


class Rejected(Exception):
    """This review's validator refused a packet."""


CHECKS = []


def need(ok, cid, **detail):
    if ok is not True:
        raise ReviewFailure('failed review check ' + cid)
    if any(c['id'] == cid for c in CHECKS):
        raise ReviewFailure('duplicate review check id ' + cid)
    row = {'id': cid, 'passed': True}
    row.update(detail)
    CHECKS.append(row)


def q(x):
    return str(x)


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha(path):
    return sha_bytes(Path(path).read_bytes())


def preview(x, digits=12):
    return format(float(x), '.%de' % (digits - 1))


def trunc_ok(text, exact):
    """text is a truncated (toward zero) decimal of the positive exact value: text <= exact < text + one unit."""
    mant, _, ex = text.partition('e')
    ex = int(ex or '0')
    val = F(mant) * F(10) ** ex
    decimals = len(mant.split('.')[1]) if '.' in mant else 0
    unit = F(10) ** (ex - decimals)
    return val <= exact < val + unit


def load_pre_module():
    path = ROOT / PRE_CHECK_REL
    spec = importlib.util.spec_from_file_location('ay2_skeptic_pre_comparison', str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ------------------------------------------------------------ phrasing
def strip_code(text):
    text = re.sub(r'```.*?```', ' ', text, flags=re.S)
    return re.sub(r'`[^`\n]*`', ' ', text)


def phrase_scan(text):
    """Code spans removed; per line: no 'the thermodynamic limit', 'the limit state', 'converges as n' or
    'uniform in a' (as words); 'the AQ state' only inside the negated verbatim exclusion; every line with
    'uniq' contains 'not'. Returns the offending lines."""
    bad = []
    for line in strip_code(text).splitlines():
        low = line.lower()
        if 'the thermodynamic limit' in low or 'the limit state' in low or 'converges as n' in low:
            bad.append(line)
        elif re.search(r'\buniform in a\b', low):
            bad.append(line)
        elif 'the aq state' in low and not ('uniqueness of the aq state' in low and re.search(r'\bnot\b', low)):
            bad.append(line)
        elif 'uniq' in low and re.search(r'\bnot\b', low) is None:
            bad.append(line)
    return bad


# ------------------------------------------------------------ own validator of producer packets
def validate_producer(res, truth):
    if res.get('contract_sha256') != CONTRACT_SHA or res.get('ay1_gate_sha256') != AY1_GATE_SHA:
        raise Rejected('contract or AY1 gate hash differs')
    h = res['headline']
    for key, val in (('K2_prime', truth['K2']), ('D', truth['D']), ('two_D', truth['twoD']), ('K2_plus', truth['K2plus']),
                     ('two_K2_prime_tau2', truth['twoK2t2']), ('K2_prime_tau2', truth['K2t2'])):
        if F(h[key]) != val:
            raise Rejected('headline %s differs from the AY1 gate' % key)
    lo, hi = F(res['label']['sqrt10_enclosure'][0]), F(res['label']['sqrt10_enclosure'][1])
    if not (lo * lo <= 10 <= hi * hi and hi - lo <= F(1, 10 ** 30)):
        raise Rejected('sqrt(10) enclosure not directed')
    L, U, rem = F(h['tier_lower']), F(h['tier_upper']), truth['K2t2']
    exact_sq = 10 * TAU * TAU / 5184
    if not (L + rem >= 0 and (L + rem) ** 2 <= exact_sq and (U - rem) ** 2 >= exact_sq and U - rem >= 0 and L > 0):
        raise Rejected('tier ends are not directed bounds')
    if L != lo * TAU / 72 - rem or U != hi * TAU / 72 + rem:
        raise Rejected('tier ends differ from their formula')
    if res['label']['lower'] != h['tier_lower'] or res['label']['upper'] != h['tier_upper']:
        raise Rejected('label block differs from the headline')
    rw = F(h['relative_width_upper'])
    if rw != (U - L) / (lo * TAU / 72) or rw > F(1, 100) or h['target_met'] is not True:
        raise Rejected('relative width or target')
    if F(h['plus_minus_tau_separation_lower']) != 2 * L:
        raise Rejected('+-tau separation differs from sqrt(10)|tau|/36 - 2K_2prime tau^2 (directed)')
    if F(h['falsifier_separation_lower']) != (1 - F(2, 10 ** 6)) * truth['twoK2t2']:
        raise Rejected('falsifier separation differs')
    if [o['status'] for o in res['obligations']] != ['unproved'] * 6 or len(res['obligations']) != 6:
        raise Rejected('obligations table incomplete or a row proved')
    for key in SIX:
        if res.get(key) is not False:
            raise Rejected('gate field claimed: ' + key)
    for key in FLAGS_FALSE:
        if res.get(key) is not False:
            raise Rejected('claim flag set: ' + key)
    if res.get('closeness_order') != [1, 2] or res.get('topology') != 'trace norm on B(H_R)':
        raise Rejected('closeness order or topology')
    if res.get('sub_labels') != ['uniform_local_closeness_not_uniqueness', 'static_not_dynamic']:
        raise Rejected('sub-labels')
    lb = res['label']
    if lb['tier'] != 'first_order_distance_from_product' or lb['kind'] != 'static property of the state on R' \
            or any(lb[k] is not False for k in ('dynamical_claim', 'interaction_shift_claim', 'euclidean_node_claim',
                                                 'identifies_the_limit')):
        raise Rejected('tier label is not static')
    return True


# ------------------------------------------------------------ source-mutation replays
CHK, REP = 'check.py', 'report.md'


def mutated_run(edits=(), input_edits=(), extra_input=None, remove_input=None, rehash=None, report_append=None,
                report_drop_prefix=None):
    """Copy the frozen closure outside the checkout, apply one edit set, run check.py once."""
    with tempfile.TemporaryDirectory(prefix='hnm-r32-ay2-skeptic-mut-') as tmp:
        repo = Path(tmp) / 'repo'
        dst = repo / FWD_REL
        shutil.copytree(FWD, dst, ignore=shutil.ignore_patterns('output', 'freeze.json', '__pycache__'))
        texts = {name: (dst / name).read_text(encoding='utf-8') for name in (CHK, REP)}
        for name, old, new in edits:
            if texts[name].count(old) < 1:
                raise ReviewFailure('mutation anchor missing in %s: %r' % (name, old[:60]))
            if name == CHK and texts[name].count(old) != 1:
                raise ReviewFailure('mutation anchor not unique in %s: %r' % (name, old[:60]))
            texts[name] = texts[name].replace(old, new)
        for rel, old, new, count in input_edits:
            path = dst / 'inputs' / rel
            raw = path.read_bytes()
            if raw.count(old) != count:
                raise ReviewFailure('input mutation anchor count differs: ' + rel)
            raw = raw.replace(old, new)
            path.write_bytes(raw)
            if rehash is not None and rehash[0] == rel:
                if texts[CHK].count(rehash[1]) != 1:
                    raise ReviewFailure('pinned hash not unique for ' + rel)
                texts[CHK] = texts[CHK].replace(rehash[1], sha_bytes(raw))
        if report_append is not None:
            texts[REP] = texts[REP] + report_append
        if report_drop_prefix is not None:
            lines = texts[REP].split('\n')
            kept = [ln for ln in lines if not ln.startswith(report_drop_prefix)]
            if len(lines) - len(kept) != 1:
                raise ReviewFailure('report line to drop not unique: ' + report_drop_prefix)
            texts[REP] = '\n'.join(kept)
        for name, text in texts.items():
            (dst / name).write_text(text, encoding='utf-8')
        if extra_input is not None:
            extra = dst / 'inputs' / extra_input
            extra.parent.mkdir(parents=True, exist_ok=True)
            extra.write_text('skeptic mutation fixture\n')
        if remove_input is not None:
            (dst / 'inputs' / remove_input).unlink()
        out = Path(tmp) / 'out'
        flags = ['-B'] + (['-O'] if sys.flags.optimize else [])
        done = subprocess.run([sys.executable] + flags + [str(dst / CHK), '--output', str(out)],
                              capture_output=True, text=True, cwd=str(repo))
        outputs = {p.name: p.read_bytes() for p in out.glob('*.json')} if out.is_dir() else {}
        last = done.stderr.strip().splitlines()[-1] if done.stderr.strip() else ''
        if any(p.name == '__pycache__' or p.suffix == '.pyc' for p in dst.rglob('*')):
            raise ReviewFailure('interpreter cache written into a mutated copy')
        return done.returncode, outputs, last.replace(tmp, '<tmp>')


def weaken(old, new_head='require(True, '):
    """Replace a validator's require(<condition>, ...) head by require(True, ...)."""
    return (CHK, old, new_head)


GATE_K2 = b'966771578474926086618624139557778885954947547760216752246561/72052885697817210754545804931891200000000000000000000000'
GATE_K2_EDIT = b'966771578474926086618624139557778885954947547760216752246562/72052885697817210754545804931891200000000000000000000000'
LOWER_P = '315493271189404369878663368737136921794795815043212654249128159/720528856978172107545458049318912000000000000000000000000000000000000000'
MUST_ABORT = [
    # one validator weakening per contract control (the producer's damaging mutation must then be accepted)
    ('ctl_missing_incoming_stars', dict(edits=[(CHK, "        require(p == pins_g, 'R-local pins differ from the gate itemization (incoming stars must be counted)')\n"
                                                    "        require(ay1_items(tau_cap, F, p)['total'] == it['+']['total'], \"K_2' recomputed from these pins differs from the gate\")\n",
                                               '        pass\n')]),
     'damaging mutation accepted: outgoing_stars_only_42_faces_meeting_R'),
    ('ctl_full_original_wilson_cover', dict(edits=[(CHK, "        require(face_owner_set(Wface) <= region, 'the original xz Wilson loop is not covered by complete factors of the region')\n"
                                                        "        require(set(links) == set(l for b in region for l in factor_links(b)), 'the cover must consist of complete 24-link factors')\n",
                                                   '        pass\n')]),
     'damaging mutation accepted: single_factor_cover_0'),
    ('ctl_wrong_delta_alpha_hbar_clock', dict(edits=[weaken('        require(cf == Q(-1, 72), ', '        require(True, ')]),
     'damaging mutation accepted: tau_over_576_mixed_units'),
    ('ctl_vector_versus_scalar_centering', dict(edits=[weaken("        require(kind == V['centering'], ", '        require(True, ')]),
     'damaging mutation accepted: vector_centering_imposed_on_the_static_density'),
    ('ctl_first_order_mean_charged', dict(edits=[weaken("        require(tsq > 0, ", '        require(True, ')]),
     'damaging mutation accepted: first_order_density_set_to_zero'),
    ('ctl_tau_scaling_exponent', dict(edits=[weaken('        require(lo_ <= ratio <= hi_, ', '        require(True, ')]),
     'damaging mutation accepted: first_order_term_labelled_second_order'),
    ('ctl_changed_model_relabelled', dict(edits=[weaken("        require(abs(mdl['tau']) == tau_cap, ", '        require(True, ')]),
     'damaging mutation accepted: tau_above_the_cap'),
    ('ctl_coherent_evidence_tampering', dict(edits=[weaken("            require(cid in ids and ids[cid]['passed'] is True, ", '            require(True, ')]),
     'damaging mutation accepted: control_boolean_flipped_hash_rebound'),
    ('ctl_insufficient_verdict_retained', dict(edits=[weaken('        require(reported == forward_verdict(*args), ', '        require(True, ')]),
     'damaging mutation accepted: missing_obligation_relabelled_accepted'),
    ('ctl_exact_arithmetic_admission', dict(edits=[(CHK, "    if isinstance(value, bool) or isinstance(value, float):\n        raise AdmissionError('non-exact input rejected: ' + repr(value))\n",
                                                   "    if isinstance(value, float):\n        return Q(value)\n    if isinstance(value, bool):\n        raise AdmissionError('non-exact input rejected: ' + repr(value))\n")]),
     'damaging mutation accepted: float_sqrt10_input'),
    ('ctl_root_n_misuse', dict(edits=[weaken("        require(kind == 'exact orthogonality (Pythagoras over the ten orthonormal e_f)', ", '        require(True, ')]),
     'damaging mutation accepted: sqrt10_as_statistical_root_N'),
    ('ctl_no_priority_or_continuum_claim', dict(edits=[weaken('            require(fl.get(k1) is v1, ', '            require(True, ')]),
     'damaging mutation accepted: continuum_true'),
    ('ctl_topology_named', dict(edits=[weaken("        require(tp['states'] == 'trace norm on B(H_R)' and tp['tier'] == 'trace norm on B(H_R)', ", '        require(True, ')]),
     'damaging mutation accepted: weak_star_for_states'),
    ('ctl_two_families_named', dict(edits=[weaken('        require(tuple(fams) == FAMS, ', '        require(True, ')]),
     'damaging mutation accepted: one_family_only'),
    ('ctl_subsequence_versus_whole_sequence', dict(edits=[weaken("        require(claim == 'subsequential', ", '        require(True, ')]),
     'damaging mutation accepted: whole_sequence_inferred_from_uniform_bounds'),
    ('ctl_local_closeness_not_uniqueness', dict(edits=[weaken("        require(claim == 'closeness', ", '        require(True, ')]),
     'damaging mutation accepted: equality_from_closeness'),
    ('ctl_common_clock', dict(edits=[weaken("        require(pk['tau'][0] == pk['tau'][1], ", '        require(True, ')]),
     'damaging mutation accepted: opposite_signs_first_order_densities_differ'),
    ('ctl_tier_mixing_rejected', dict(edits=[weaken("        require(value == K2p_g, ", '        require(True, ')]),
     'damaging mutation accepted: W_only_K2plus_as_trace_norm_remainder'),
    ('ctl_not_uniform_in_a', dict(edits=[weaken("        require(kind == 'N at fixed lattice spacing a and fixed tau', ", '        require(True, ')]),
     'damaging mutation accepted: uniform_in_a_claimed'),
    ('ctl_lower_bound_is_static_not_dynamic', dict(edits=[weaken("        require(lb['tier'] == 'first_order_distance_from_product' and lb['kind'] == 'static property of the state on R', ",
                                                                  '        require(True, ')]),
     'damaging mutation accepted: tier_relabelled_dynamical'),
    ('ctl_obligations_table_complete', dict(edits=[weaken("        require(len(rows) == 6, ", '        require(True, ')]),
     'damaging mutation accepted: padded_family_dynamics_row_removed'),
    # value and logic edits
    ('val_tier_lower_half_remainder', dict(edits=[(CHK, '        lower = sqrt_lo * abs(tau) / 72 - k_single * tau * tau\n',
                                                   '        lower = sqrt_lo * abs(tau) / 72 - k_single * tau * tau / 2\n')]),
     'lower end is not a lower bound of sqrt(10)|tau|/72 - K_2prime tau^2'),
    ('val_sqrt10_upper_in_lower_end', dict(edits=[(CHK, '    lower, upper = tier(K2p, lo10, hi10)\n', '    lower, upper = tier(K2p, hi10, hi10)\n')]),
     'lower end is not a lower bound of sqrt(10)|tau|/72 - K_2prime tau^2'),
    ('val_am2_item_halved', dict(edits=[(CHK, "    F = {'c_am2': int(m.group(4)),", "    F = {'c_am2': int(m.group(4)) // 2,")]),
     "K_2' differs from the AY1 gate value"),
    ('val_witness_nu_doubled', dict(edits=[(CHK, '    nu = K2p_tau2 * (1 - Q(1, 10 ** 6)) / 4\n', '    nu = K2p_tau2 * (1 - Q(1, 10 ** 6)) / 2\n')]),
     "witness outside the AY1 ball ||rho - P_R - rho^(1)_R||_1 <= K_2' tau^2"),
    ('val_parity_rule_disabled', dict(edits=[(CHK, '    return any(k % 2 for k in count.values())', '    return False')]),
     'only the diagonal pair survives the parity rule here'),
    ('val_first_order_coefficient_1_144', dict(edits=[(CHK, '    coef = Q(1, 72)\n', '    coef = Q(1, 144)\n')]),
     'failed check first_order_density_rank_two'),
    ('val_continuum_flag_true', dict(edits=[(CHK, "    FLAGS = {'continuum_claim': False,", "    FLAGS = {'continuum_claim': True,")]),
     'damaging mutation accepted: continuum_true'),
    ('val_uniqueness_claimed_true', dict(edits=[(CHK, "    CLAIMS = {'uniqueness_claimed': False,", "    CLAIMS = {'uniqueness_claimed': True,")]),
     'preregistered gate fields exported unchanged'),
    ('val_separation_with_sqrt10_upper', dict(edits=[(CHK, '    sep_lower = lo10 * tau_cap / 36 - two_K2\n', '    sep_lower = hi10 * tau_cap / 36 - two_K2\n')]),
     'failed check plus_minus_tau_separation'),
    # inputs
    ('inp_contract_byte_edit_without_rehash', dict(input_edits=[(CONTRACT_REL, b'"stop": "Investigation 8 of 10."', b'"stop": "Investigation 8 of 11."', 1)]),
     'contract snapshot bytes differ from the frozen AY2 contract'),
    ('inp_contract_target_1_1000_rehash', dict(input_edits=[(CONTRACT_REL, b'"value": "1/100"', b'"value": "1/1000"', 1)], rehash=(CONTRACT_REL, CONTRACT_SHA)),
     'failed check contract_snapshot_sha256'),
    ('inp_ay1_gate_K2_digit', dict(input_edits=[(AY1_GATE_REL, GATE_K2, GATE_K2_EDIT, 2)]),
     'failed check ay1_gate_constants_parsed_exact'),
    ('inp_undeclared_skeptic_ay2_input', dict(extra_input='research/round32/skeptic/ay2-independent-derivation.md'),
     'failed check premise_inventory_bound'),
    ('inp_premise_snapshot_removed', dict(remove_input='research/round29/forward/aq2/report.md'),
     'failed check premise_inventory_bound'),
    # report
    ('rep_O1_marked_proved', dict(edits=[(REP, '| O1 | uniqueness of the limit | unproved |', '| O1 | uniqueness of the limit | proved |')]),
     'every obligation stays unproved'),
    ('rep_O6_row_removed', dict(report_drop_prefix='| O6 |'), 'the obligations table must have exactly six rows'),
    ('rep_sentence_negation_removed', dict(edits=[(REP, "It does not assert `omega' = omega''`", "It asserts `omega' = omega''`")]),
     'mandatory sentence (filled template) missing from the report'),
    ('rep_the_AQ_state_appended', dict(report_append='\nThe AQ state is fixed.\n'), 'forbidden phrasing in the report'),
    ('rep_unique_without_not_appended', dict(report_append='\nThe limit on R is unique.\n'), '"unique" without "not" in the report'),
    ('rep_map_row_removed', dict(report_drop_prefix='| `root_n_misuse` | §§4.2, 6.4 |'), 'map lacks rows for root_n_misuse'),
    ('rep_exact_tier_lower_removed', dict(edits=[(REP, LOWER_P, '0/1')]), 'report does not carry the exact value'),
]
SILENT = [
    ('inp_ay1_gate_unparsed_field', dict(input_edits=[(AY1_GATE_REL, b'"reviewer_path": "research/round32/skeptic/ay1.md"',
                                                       b'"reviewer_path": "research/round32/skeptic/ay1.md "', 1)]),
     'gate hash not pinned in check.py; caught by the snapshot-versus-source comparison (replay_loop.verify_freeze) and by this review\'s validator (pinned AY1 gate sha256 in results)'),
    ('val_wilson_face_moved_within_F_R', dict(edits=[(CHK, "    Wface = (ORIGIN, next(k for k in omitted if (k[0], k[1], k[2]) == ('xz', 0, 0)))",
                                                        "    Wface = (ORIGIN, next(k for k in omitted if (k[0], k[1], k[2]) == ('xz', 1, 0)))")]),
     'readout-blind: Tr(rho^(1)_R W_g)=+tau/144 for every g in F_R, so no exported value depends on which of the ten faces is W'),
    ('val_witness_energy_check_removed', dict(edits=[weaken('        require(energy_alpha <= Q(98, 8) * abs(tau), ', '        require(True, ')]),
     'constraint holds with a margin of about 10^12 and exports no value; this review rebuilds the witness and re-checks the reset energy'),
]

CONTROL_MEANING = {
    'missing_incoming_stars': ['outgoing_stars_only_42_faces_meeting_R', 'single_star_at_0_only'],
    'full_original_wilson_cover': ['single_factor_cover_0', 'four_drawn_links_as_cover'],
    'wrong_delta_alpha_hbar_clock': ['tau_over_576_mixed_units', 'tau_over_9_mixed_units', 'normalized_clock'],
    'vector_versus_scalar_centering': ['vector_centering_imposed_on_the_static_density', 'scalar_Wilson_mean_as_tier_centre'],
    'first_order_mean_charged': ['first_order_density_set_to_zero', 'tier_lower_end_set_to_zero'],
    'tau_scaling_exponent': ['first_order_term_labelled_second_order', 'second_order_remainder_labelled_first_order'],
    'changed_model_relabelled': ['tau_above_the_cap', 'nonzero_triple', 'uniform_route_B_model', 'falsifier_fixture_relabelled_as_AQ_data'],
    'coherent_evidence_tampering': ['control_boolean_flipped_hash_rebound', 'tier_lower_end_raised_hash_rebound', 'K2_prime_quartered_hash_rebound',
                                    'obligation_row_removed_hash_rebound', 'ay1_gate_hash_replaced_hash_rebound'],
    'insufficient_verdict_retained': ['missing_obligation_relabelled_accepted', 'overclaim_relabelled_limited', 'uncertified_tier_relabelled_accepted',
                                      'D_ball_tier_retuned_to_pass'],
    'exact_arithmetic_admission': ['float_input', 'decimal_preview_as_admission_value'],
    'root_n_misuse': ['rss_of_two_single_state_remainders', 'sqrt10_as_statistical_root_N', 'linear_face_sum_10_as_trace_norm'],
    'no_priority_or_continuum_claim': ['continuum_true', 'priority_true', 'weak_coupling_true'],
    'topology_named': ['weak_star_for_states', 'one_topology_for_both', 'dynamical_statement_added'],
    'two_families_named': ['one_family_only', 'third_family_added'],
    'subsequence_versus_whole_sequence': ['whole_sequence_inferred_from_uniform_bounds', 'rate_in_N_inferred', 'whole_sequence_flag_true'],
    'local_closeness_not_uniqueness': ['equality_from_closeness', 'equality_from_common_tier', 'uniqueness_flag_true'],
    'common_clock': ['opposite_signs_first_order_densities_differ', 'different_couplings'],
    'tier_mixing_rejected': ['W_only_K2plus_as_trace_norm_remainder', 'labelled_variant_as_headline', 'pair_constant_as_single_state_remainder',
                             'lower_end_from_K2plus_upper_end_from_K2prime'],
    'not_uniform_in_a': ['uniform_in_a_claimed'],
    'lower_bound_is_static_not_dynamic': ['tier_relabelled_dynamical', 'tier_relabelled_interaction_shift', 'tier_relabelled_euclidean_node',
                                          'lower_bound_read_as_identification'],
    'obligations_table_complete': ['padded_family_dynamics_row_removed', 'uniqueness_row_marked_proved', 'cauchy_route_missing'],
}
OBLIGATION_MAP = {'O1': 'uniqueness', 'O2': 'whole_sequence_convergence', 'O3': 'translation_invariance', 'O4': 'rate_in_N',
                  'O5': 'boundary_independence_of_dynamics', 'O6': 'padded_family_dynamics'}


def producer_replays():
    """replay_declared.py steps for the declared forward direction, with the unchanged replay_loop functions."""
    src = FWD
    closure = base.verify_freeze(src, 'ay2')
    before = base.sha(src / 'freeze.json')
    expected = {p.relative_to(src / 'output').as_posix(): p.read_bytes() for p in (src / 'output').rglob('*') if p.is_file()}
    receipts = []
    for mode in ('normal', 'optimized'):
        with tempfile.TemporaryDirectory(prefix='hnm-r32-ay2-forward-%s-' % mode) as temporary:
            out = Path(temporary) / 'output'
            if ROOT in out.resolve().parents:
                raise ReviewFailure('replay directory inside the checkout')
            cmd = [sys.executable, '-B'] + (['-O'] if mode == 'optimized' else []) + [str(src / 'check.py'), '--output', str(out)]
            done = subprocess.run(cmd, capture_output=True, text=True, cwd=str(ROOT))
            if done.returncode != 0:
                raise ReviewFailure('producer replay failed (%s): %s' % (mode, done.stderr[-500:]))
            actual = {p.relative_to(out).as_posix(): p.read_bytes() for p in out.rglob('*') if p.is_file()}
            receipts.append({'mode': mode, 'byte_identical_to_frozen_output': actual == expected,
                             'outputs': {n: sha_bytes(b) for n, b in sorted(actual.items())},
                             'stdout': done.stdout.strip().replace(str(out), '<fresh-external-dir>')})
    tool = [sys.executable, '-B', str(R32 / 'tools/freeze.py'), 'verify', FWD_REL]
    fv = subprocess.run(tool, capture_output=True, text=True, cwd=str(ROOT))
    base.verify_freeze(src, 'ay2')
    return closure, before, receipts, fv.returncode, fv.stdout.strip().splitlines()[-1] if fv.stdout.strip() else '', base.sha(src / 'freeze.json')


# ------------------------------------------------------------ main computation
def run():
    # ---------------- integrity
    con_raw = (ROOT / CONTRACT_REL).read_bytes()
    con = json.loads(con_raw)
    gate_raw = (ROOT / AY1_GATE_REL).read_bytes()
    gate = json.loads(gate_raw)
    need(sha_bytes(con_raw) == CONTRACT_SHA and sha_bytes(gate_raw) == AY1_GATE_SHA and con['producers'] == ['forward']
         and con['direction'] == 'statement+skeptic' and con['single_direction_independent_replay'] is True
         and sha(HERE / 'replay_loop.py') == REPLAY_LOOP_SHA, 'contract_gate_and_tool_pinned',
         contract_sha256=CONTRACT_SHA, ay1_gate_sha256=AY1_GATE_SHA, replay_loop_sha256=REPLAY_LOOP_SHA)
    frozen_ok = all(sha(FWD / k) == v for k, v in FROZEN.items())
    freeze = json.loads((FWD / 'freeze.json').read_text())
    listed = {k[len(FWD_REL) + 1:] for k in freeze['sources']}
    closure_files = {p.relative_to(FWD).as_posix() for p in FWD.rglob('*') if p.is_file()}
    need(frozen_ok and closure_files - {'freeze.json'} == listed and len(listed) == 27
         and all(sha(ROOT / k) == v for k, v in freeze['sources'].items()) and freeze['contract_sha256'] == CONTRACT_SHA
         and freeze['loop'] == 'AY2' and freeze['direction'] == 'forward', 'forward_closure_frozen',
         closure_files=len(listed), freeze_json_sha256=FROZEN['freeze.json'])
    declared = sorted(['AGENTS.md', CONTRACT_REL] + list(con['shared_premises']))
    inputs = sorted(p.relative_to(FWD / 'inputs').as_posix() for p in (FWD / 'inputs').rglob('*') if p.is_file())
    need(inputs == declared and len(inputs) == 23 and all((FWD / 'inputs' / n).read_bytes() == (ROOT / n).read_bytes() for n in inputs)
         and not any(n.startswith('research/round32/skeptic/ay2') for n in inputs)
         and not (R32 / 'reverse/ay2').exists(), 'inventory_23_declared_identical',
         inputs=23, skeptic_inputs=[n for n in inputs if '/skeptic/' in n], reverse_package_present=False)
    manifest = json.loads((FWD / 'output/source-manifest.json').read_text())
    res = json.loads((FWD / 'output/results.json').read_text())
    need(all(sha(FWD / k) == v for k, v in manifest['sources'].items()) and len(manifest['sources']) == 25
         and manifest['outputs']['results.json'] == FROZEN['output/results.json']
         and res['check_py_sha256_recorded_before_evaluation'] == FROZEN['check.py'], 'source_manifest_and_check_sha',
         manifest_sources=len(manifest['sources']))
    closure, fz_before, receipts, fv_rc, fv_out, fz_after = producer_replays()
    need(closure['closure_files'] == 27 and closure['inputs'] == 23 and closure['inventory_equals_declared'] is True
         and all(r['byte_identical_to_frozen_output'] for r in receipts) and len(receipts) == 2 and fv_rc == 0
         and json.loads(fv_out)['status'] == 'verified' and fz_before == fz_after == FROZEN['freeze.json'],
         'producer_replays_byte_identical', replays=receipts, freeze_verify=json.loads(fv_out), closure=closure,
         method='replay_declared.py steps with the unchanged replay_loop.verify_freeze (replay_declared.py refuses '
                'direction statement+skeptic; replay_loop.py always replays a reverse package)')
    pre_freeze_raw = (ROOT / PRE_FREEZE_REL).read_bytes()
    pre_freeze = json.loads(pre_freeze_raw)
    need(sha_bytes(pre_freeze_raw) == PRE_FREEZE_SHA and pre_freeze['contract_sha256'] == CONTRACT_SHA
         and pre_freeze['stage'] == 'pre_comparison' and all(sha(ROOT / k) == v for k, v in pre_freeze['files'].items()),
         'pre_comparison_package_unchanged', freeze_sha256=PRE_FREEZE_SHA, files=len(pre_freeze['files']))
    with tempfile.TemporaryDirectory(prefix='hnm-r32-ay2-skeptic-pre-') as tmp:
        out = Path(tmp) / 'pre'
        flags = ['-B'] + (['-O'] if sys.flags.optimize else [])
        done = subprocess.run([sys.executable] + flags + [str(ROOT / PRE_CHECK_REL), '--output', str(out)],
                              capture_output=True, text=True, cwd=str(ROOT))
        pre_bytes = (out / 'results.json').read_bytes() if (out / 'results.json').is_file() else b''
    need(done.returncode == 0 and pre_bytes == (ROOT / PRE_RESULTS_REL).read_bytes(), 'pre_comparison_replay_byte_identical',
         results_sha256=sha_bytes(pre_bytes))
    pre = json.loads((ROOT / PRE_RESULTS_REL).read_text())
    pm = load_pre_module()

    # ---------------- constants
    acc = gate['accepted']
    k2_g = F(re.search(r"K_2'=(\d+/\d+)", acc).group(1))
    d_g = F(re.search(r'; D=(\d+/\d+)', acc).group(1))
    k2p_g = F(re.search(r'K_2\^\+=(\d+/\d+)', acc).group(1))
    truth = {'K2': k2_g, 'D': d_g, 'twoD': 2 * d_g, 'K2plus': k2p_g, 'K2t2': k2_g * TAU ** 2, 'twoK2t2': 2 * k2_g * TAU ** 2}
    own_k2 = pm.k2_prime(TAU)
    own_d = pm.d_forward(pm.tier_ii(TAU)['eps_F'])
    h = res['headline']
    need(own_k2 == k2_g == F(h['K2_prime']) == F(pre['ay1_constants']['K2_prime']) and own_d == d_g == F(h['D'])
         and F(h['two_D']) == 2 * d_g == F(pre['ay1_constants']['two_D']) and F(h['K2_plus']) == k2p_g == pm.k2_plus_formula(TAU)
         and F(h['two_K2_prime_tau2']) == truth['twoK2t2'] == F(pre['ay1_constants']['two_K2_prime_tau2'])
         and F(h['K2_prime_tau2']) == truth['K2t2'], 'ay1_constants_equal_everywhere',
         K2_prime=q(k2_g), D=q(d_g), K2_plus=q(k2p_g),
         sources=['AY1 gate text', 'producer headline', 'skeptic pre-comparison results', 'own recomputation (tier-(ii) items)'])

    # ---------------- rho^(1)_R
    ids = {c['id']: c for c in res['checks']}
    rk = ids['first_order_density_rank_two']
    faces = sorted([f for b in sorted({pm.sub(r, s) for r in pm.R_COVER for s in pm.S_STAR})
                    for f in pm.omitted_faces(b) if f['owners'] == frozenset(pm.R_COVER)], key=lambda f: (f['orient'], f['base']))
    tr = [pm.trace_poly(f['oriented']) for f in faces]
    basis = [pm.ONE] + tr
    gram = [[pm.expect([basis[i], basis[j]]) for j in range(11)] for i in range(11)]
    ident = [[F(int(i == j)) for j in range(11)] for i in range(11)]
    need(gram == ident and F(rk['trace_norm_over_abs_tau_squared']) == F(10, 5184) and rk['spectrum_over_tau'].endswith('c^2 = 5/10368')
         and F(5, 10368) == F(10, 20736) and F(rk['tr_rho1_W_over_tau']) == F(1, 144)
         and 'relayed_claim_eigenvalues_pm_sqrt10_tau_over_72' in rk['rejected_mutations']
         and 'each_face_piece_called_rank_one' in rk['rejected_mutations'], 'rho1_trace_norm_agrees',
         trace_norm='sqrt(10)|tau|/72 (producer: rank-two spectrum; skeptic: explicit Haar Gram matrix and characteristic polynomial)',
         eigenvalues='+-sqrt(10)tau/144', each_piece='rank two (|W_f Omega_R><Omega_R| plus its adjoint), eigenvalues +-|tau|/144',
         skeptic_wording_correction="the skeptic's pre-comparison note 'ten rank-one pieces' is corrected to rank-two pieces; values unaffected")

    # ---------------- sqrt(10) brackets and the tier ends
    lo30, hi30 = F(res['label']['sqrt10_enclosure'][0]), F(res['label']['sqrt10_enclosure'][1])
    lo40, hi40 = F(pre['tier']['sqrt10_bracket'][0]), F(pre['tier']['sqrt10_bracket'][1])
    Lp, Up = F(h['tier_lower']), F(h['tier_upper'])
    Ls, Us = F(pre['tier']['lower']), F(pre['tier']['upper'])
    rem = truth['K2t2']
    exact_sq = 10 * TAU * TAU / 5184

    def directed(L, U):
        return L > 0 and (L + rem) ** 2 <= exact_sq <= (U - rem) ** 2 and U - rem > 0
    slack = (hi30 - lo30) * TAU / 72
    need(lo30 * lo30 < 10 < hi30 * hi30 and hi30 - lo30 == F(1, 10 ** 30) and lo40 * lo40 <= 10 <= hi40 * hi40
         and hi40 - lo40 == F(1, 10 ** 40) and lo30 <= lo40 and hi40 <= hi30, 'sqrt10_brackets_nested_directed',
         producer_bracket=[q(lo30), q(hi30)], producer_width='10^-30', skeptic_bracket=[q(lo40), q(hi40)], skeptic_width='10^-40')
    ay1rev = json.loads((ROOT / AY1_REVIEW_JSON_REL).read_bytes())
    sup = ay1rev['admitted_values']['supplementary_observation_labelled_only']
    need(sha(ROOT / AY1_REVIEW_JSON_REL) == AY1_REVIEW_JSON_SHA and Lp == lo30 * TAU / 72 - rem and Up == hi30 * TAU / 72 + rem
         and Ls == lo40 * TAU / 72 - rem and Us == hi40 * TAU / 72 + rem and directed(Lp, Up) and directed(Ls, Us)
         and Lp <= Ls <= Us <= Up and Ls - Lp <= slack and Up - Us <= slack and Ls - Lp + Up - Us <= slack
         and F(43786, 10 ** 14) <= Lp and Up <= F(44055, 10 ** 14) and Up < d_g
         and abs(Lp - F(sup['lower_forward'])) < F(1, 10 ** 22) and abs(Up - F(sup['upper_forward'])) < F(1, 10 ** 22),
         'tier_ends_compared', producer=[q(Lp), q(Up)], skeptic=[q(Ls), q(Us)],
         producer_contains_skeptic=True, max_difference=q(max(Ls - Lp, Up - Us)), bound_on_difference='10^-30 |tau|/72',
         both_directed=True, ay1_recorded_observation='[4.3786e-10, 4.4055e-10] contains both',
         recommended_binding='the producer rationals (frozen certificate, 10^-30 bracket); the skeptic rationals are the tighter independent enclosure (10^-40)')

    # ---------------- relative width and target
    rw_p = F(h['relative_width_upper'])
    rw_ideal_sq = (144 * k2_g * TAU) ** 2 / 10
    rw_s_hi = F(pre['tier']['relative_width_bracket'][1])
    target = F(con['preregistration']['target']['value'])
    need(target == F(1, 100) and rw_p == (Up - Lp) / (lo30 * TAU / 72) and rw_p <= target and rw_p ** 2 >= rw_ideal_sq
         and rw_s_hi <= rw_p and rw_p - rw_s_hi < F(1, 10 ** 28) and (14400 * k2_g * TAU) ** 2 <= 10
         and trunc_ok('1.6366846', target / rw_p) and h['target_met'] is True, 'relative_width_and_target',
         producer=q(rw_p), skeptic_upper=q(rw_s_hi), target=q(target), margin_preview=preview(target / rw_p, 9),
         definition='producer (U-L)/(sqrt10_lo |tau|/72) includes the bracket slack and is an upper bound of the ideal 144 K_2prime |tau|/sqrt(10)')

    # ---------------- +-tau separation
    sep_p = F(h['plus_minus_tau_separation_lower'])
    sep_s = F(pre['plus_minus_tau']['separation_lower'])
    need(sep_p == 2 * Lp and sep_s == 2 * Ls and sep_p <= sep_s and sep_p >= F(87572, 10 ** 14)
         and (sep_p + 2 * rem) ** 2 <= 40 * TAU * TAU / 5184 and sep_p < 2 * d_g and Up <= d_g, 'plus_minus_tau_separation',
         producer=q(sep_p), skeptic=q(sep_s), preview=preview(sep_p), each_within='D of P_R (upper tier end below D)')

    # ---------------- falsifying witness, rebuilt by explicit Haar integration
    fw = ids['falsifying_scenario_witness']
    nu = F(fw['nu'])
    t = TAU / 144
    w_face = [i for i, f in enumerate(faces) if f['orient'] == 'xz' and f['base'] == (0, 0, 0)][0]
    wpoly = {k: v / 2 for k, v in tr[w_face].items()}
    MW = [[pm.expect([basis[i], basis[j], wpoly]) for j in range(11)] for i in range(11)]
    yz = {f['base'][0]: i + 1 for i, f in enumerate(faces) if f['orient'] == 'yz'}
    Om = [F(1)] + [F(0)] * 10
    v = [F(0)] + [F(1)] * 10
    wprime = [F(0)] * 11
    for r in range(4):
        wprime[yz[r]] = F((-1) ** r)
    s10_hi = hi40

    def witness(sgn):
        psi = [Om[i] + t * v[i] + sgn * nu * wprime[i] for i in range(11)]
        n2 = sum((x * x for x in psi), F(0))
        rho = [[x * y / n2 for y in psi] for x in psi]
        return psi, n2, rho
    dot = lambda a, b: sum((x * y for x, y in zip(a, b)), F(0))
    orth = dot(v, Om) == 0 and dot(wprime, Om) == 0 and dot(v, wprime) == 0 and dot(wprime, wprime) == 4 and dot(v, v) == 10
    rows = {}
    for sgn in (1, -1):
        psi, n2, rho = witness(sgn)
        ball = (abs(1 - n2) + abs(t * (1 - n2)) * 2 * s10_hi + nu * 2 * 2 + t * t * 10 + t * nu * 2 * s10_hi * 2 + nu * nu * 4) / n2
        omega_w = sum((psi[i] * MW[i][j] * psi[j] for i in range(11) for j in range(11)), F(0)) / n2
        energy = 24 * (n2 - 1) / n2                      # delta units: every e_f carries four spin-1/2 Casimirs, 8*(3/4)*4
        rows[sgn] = {'n2': n2, 'rho': rho, 'ball': ball, 'omega_w': omega_w, 'energy': energy}
    def outer_(a, b):
        return [[x * y for y in b] for x in a]

    def sym_(a, b):
        return [[a[i] * b[j] + b[i] * a[j] for j in range(11)] for i in range(11)]

    def lin(*terms):
        return [[sum((c_ * m_[i][j] for c_, m_ in terms), F(0)) for j in range(11)] for i in range(11)]
    decomposition_ok = True
    for sgn in (1, -1):
        n2_ = rows[sgn]['n2']
        lhs = lin((n2_, rows[sgn]['rho']), (-n2_, outer_(Om, Om)), (-n2_ * t, sym_(v, Om)))
        rhs = lin((1 - n2_, outer_(Om, Om)), (t * (1 - n2_), sym_(v, Om)), (sgn * nu, sym_(wprime, Om)),
                  (t * t, outer_(v, v)), (sgn * t * nu, sym_(v, wprime)), (nu * nu, outer_(wprime, wprime)))
        decomposition_ok = decomposition_ok and lhs == rhs
    test = [[F(0)] * 11 for _ in range(11)]
    for i in range(11):
        test[0][i] += wprime[i] / 2
        test[i][0] += wprime[i] / 2
    t2 = [[sum((test[i][k] * test[k][j] for k in range(11)), F(0)) for j in range(11)] for i in range(11)]
    t3 = [[sum((t2[i][k] * test[k][j] for k in range(11)), F(0)) for j in range(11)] for i in range(11)]
    diff_lo = sum(((rows[1]['rho'][i][j] - rows[-1]['rho'][i][j]) * test[j][i] for i in range(11) for j in range(11)), F(0))
    n2 = rows[1]['n2']
    L_target = (1 - F(2, 10 ** 6)) * truth['twoK2t2']
    need(orth and nu == truth['K2t2'] * (1 - F(1, 10 ** 6)) / 4 and rows[1]['n2'] == rows[-1]['n2']
         and all(rows[s_]['ball'] <= rem for s_ in (1, -1)) and s10_hi * TAU / 72 + rows[1]['ball'] <= d_g and decomposition_ok
         and all(abs(rows[s_]['omega_w'] - TAU / 144) <= k2p_g * TAU ** 2 for s_ in (1, -1))
         and all(rows[s_]['energy'] <= 98 * TAU for s_ in (1, -1)) and t3 == test and diff_lo == 8 * nu / n2
         and diff_lo >= L_target and F(fw['separation_lower']) == L_target, 'falsifying_witness_rebuilt',
         nu=q(nu), ball_upper_preview=preview(rows[1]['ball']), omega_W_deviation_preview=preview(rows[1]['omega_w'] - TAU / 144),
         reset_energy_delta_units_preview=preview(rows[1]['energy']), reset_budget='98|tau| delta units',
         separation_lower_own=q(diff_lo), separation_lower_producer=q(L_target), ratio_own_to_2K2tau2=preview(diff_lo / truth['twoK2t2'], 10),
         method='Gram and W matrix elements by explicit SU(2) Haar integration; norm-one test operator (|w\'><Omega|+h.c.)/2')
    kappa = F(pre['falsifying_scenario']['kappa'])
    n2s = 1 + 10 * t * t + kappa * kappa
    energy_pre = (24 * 10 * t * t + 64 * kappa * kappa) / n2s   # chi_1(U_f1): four spin-1 Casimirs, 8*2*4
    need(energy_pre <= 98 * TAU and F(pre['falsifying_scenario']['fixture_difference_lower']) >= L_target, 'pre_comparison_fixture_energy_retroactive',
         energy_delta_units_preview=preview(energy_pre),
         note='the pre-comparison fixture did not test the reset energy; it satisfies it (and exceeds the producer separation)')

    # ---------------- obligations
    obl = res['obligations']
    names = [o['obligation'] for o in obl]
    item2 = con['required'][1]
    routes_ok = ('HTW' in obl[0]['candidate_route'] and 'not evaluated' in obl[0]['candidate_route'] and 'Dobrushin' in obl[0]['candidate_route']
                 and 'Cauchy' in obl[1]['candidate_route'] and 'translation' in obl[2]['candidate_route'].lower()
                 and 'Lieb-Robinson' in obl[4]['candidate_route'] and 'Nachtergaele-Sims' in obl[5]['candidate_route'])
    aq1_consts = all(s_ in obl[4]['constant_to_evaluate'] for s_ in ('F(r)=(1+r)^-4', 'C<=224', '2268abs(tau)', '1323abs(tau)', 'AQ1'))
    need(len(obl) == 6 and [o['id'] for o in obl] == ['O%d' % k for k in range(1, 7)] and all(o['status'] == 'unproved' for o in obl)
         and all(len(o['missing_premise']) > 20 and len(o['candidate_route']) > 20 and len(o['constant_to_evaluate']) > 10 for o in obl)
         and all(n in item2 for n in names) and routes_ok and aq1_consts
         and 'with the AM2 constants' in obl[4]['candidate_route'], 'obligations_six_rows',
         names=names, map_to_skeptic_rows=OBLIGATION_MAP,
         dynamics_row='the O5 constants column names the AQ1 Nachtergaele-Sims constants (F(r)=(1+r)^-4, C<=224, ||Phi||_F<=2268|tau|) '
                      'and ||Phi\'||_F<=1323|tau|; the route text repeats the contract wording "with the AM2 constants" (J<=28|tau| is common '
                      'to AM2 and AQ1)')

    # ---------------- report phrasing and the mandatory sentence
    rep = (FWD / 'report.md').read_text(encoding='utf-8')
    sentence = res['mandatory_sentence_filled']
    ay1f = (ROOT / 'research/round32/forward/ay1/report.md').read_text(encoding='utf-8')
    jung = next(ln for ln in ay1f.splitlines() if ln.startswith("> For every pair of subsequential limits `omega'`"))
    k1, k2i = jung.index("`|omega'(A) - omega''(A)| <="), jung.index('This is uniform local closeness')
    gate_template = json.loads((ROOT / 'research/round32/contracts/ay1.json').read_bytes())['preregistration']['mandatory_sentence_template']
    bad = phrase_scan(rep)
    need(bad == [] and 'a chosen subsequential' in strip_code(rep) and phrase_scan('The AQ state is identified.') != []
         and phrase_scan('A unique limit exists.') != [] and phrase_scan('The bound is uniform in a.') != [],
         'forbidden_phrase_scan_report', offending_lines=bad,
         rule='code spans removed; no "the thermodynamic limit", "the limit state", "converges as N", "uniform in a"; '
              '"the AQ state" only in the negated verbatim exclusion; every line with "uniq" contains "not"')
    need(sentence in rep and sentence.startswith(jung[2:k1]) and sentence.endswith(jung[k2i:])
         and q(2 * d_g) in sentence and q(truth['twoK2t2']) in sentence and gate_template in acc and gate_template not in rep,
         'mandatory_sentence', form='Jung loop-2 form (the AY1 forward section 6 sentence), constants 2D and 2K_2prime tau^2 exact',
         ay1_contract_template_quoted_in_report=False,
         finding='the AY2 preregistration carries no template; the producer filled the Jung form; the AY1-contract template '
                 '(verbatim in the AY1 gate) is not quoted; the gate should bind the template with the constants filled')

    # ---------------- gate fields, flags, labels
    need(all(res[k] is False for k in SIX) and all(res[k] is False for k in FLAGS_FALSE) and res['closeness_order'] == [1, 2]
         and res['topology'] == 'trace norm on B(H_R)' and res['region'].startswith('R={0,e_z}') and 'states_compared' in res
         and res['sub_labels'] == ['uniform_local_closeness_not_uniqueness', 'static_not_dynamic']
         and res['label']['tier'] == 'first_order_distance_from_product' and res['label']['excludes_P_R_on_R'] is True
         and res['label']['identifies_the_limit'] is False and res['controls_deferred'] == {}, 'gate_fields_flags_labels',
         gate_fields={k: res[k] for k in SIX}, closeness_order=res['closeness_order'])

    # ---------------- the 21 controls
    controls = con['controls']
    meaning_ok = all(set(CONTROL_MEANING[c]) <= set(ids[c].get('rejected_mutations', [])) for c in controls)
    need(len(res['checks']) == 42 == res['check_count'] and all(c['passed'] is True for c in res['checks'])
         and sorted(res['contract_controls_covered']) == sorted(controls) and all(ids[c].get('rejected_mutations') for c in controls)
         and meaning_ok and res['rejected_mutations_in_control_checks'] == 85 == sum(len(ids[c]['rejected_mutations']) for c in controls)
         and res['rejected_mutation_total'] == 114 and res['controls_with_damaging_mutations'] == 21, 'controls_21_damaging',
         checks=42, control_rejections=85, total_rejections=114)
    defects = ids['contract_wording_defects_recorded']['defects']
    need([d['id'] for d in defects] == ['D1', 'D2', 'D3', 'D4', 'D5', 'D6'] and con['selected_after'] == '<preceding gate>'
         and 'uniqueness of the AQ state' in con['preregistration']['claim_exclusions']
         and 'rate_in_N_claimed' not in con['preregistration']['gate_fields_required']
         and 'within 2D of the product' in con['required'][2] and 'certified two-sided distance' in con['selection_reason'],
         'producer_contract_defects_verified', defects=[d['id'] for d in defects])

    # ---------------- report decimals
    dec_pairs = [('4.37863477824e-10', Lp), ('4.40546983333e-10', Up), ('6.10991245541e-3', rw_p), ('8.75726955649e-10', sep_p),
                 ('2.68350014178e-12', L_target), ('1.34175275439e4', k2_g), ('2.68350550879e-12', truth['twoK2t2']),
                 ('1.36124528702e-8', d_g), ('2.72249057405e-8', 2 * d_g), ('3.35480322946e3', k2p_g), ('1.34175275439e-12', rem)]
    need(all(txt in rep and trunc_ok(txt, val) for txt, val in dec_pairs), 'report_decimals_truncations',
         pairs=len(dec_pairs), rule='each report preview is the truncation of the exact value to its last digit')

    # ---------------- source-edit mutations
    rc, outs, _ = mutated_run()
    need(rc == 0 and outs.get('results.json') == (FWD / 'output/results.json').read_bytes()
         and outs.get('source-manifest.json') == (FWD / 'output/source-manifest.json').read_bytes(), 'unmutated_copy_reproduces')
    aborted = []
    for name, kw, reason in MUST_ABORT:
        rc, outs, last = mutated_run(**kw)
        if rc == 0 or reason not in last:
            raise ReviewFailure('must-abort edit %s: rc=%s last=%s' % (name, rc, last))
        aborted.append({'edit': name, 'aborted_with': reason})
    n_ctl = sum(1 for a in aborted if a['edit'].startswith('ctl_'))
    need(len(aborted) == len(MUST_ABORT) == 42 and n_ctl == 21, 'must_abort_source_edits', total=len(aborted), control_weakenings=n_ctl,
         rows=aborted)
    silent = []
    frozen_res = json.loads((FWD / 'output/results.json').read_text())
    for name, kw, account in SILENT:
        rc, outs, last = mutated_run(**kw)
        if rc != 0:
            raise ReviewFailure('silent edit aborted unexpectedly: ' + name)
        mres = json.loads(outs['results.json'])
        strip = lambda d: {k: v for k, v in d.items() if k != 'check_py_sha256_recorded_before_evaluation'}
        same = strip(mres) == strip(frozen_res)
        caught = False
        if not same:
            try:
                validate_producer(mres, truth)
            except Rejected:
                caught = True
        silent.append({'edit': name, 'output_identical_except_check_py_sha256': same, 'caught_by_this_validator': caught,
                       'account': account})
    need(len(silent) == 3 and silent[0]['caught_by_this_validator'] is True
         and silent[1]['output_identical_except_check_py_sha256'] is True
         and silent[2]['output_identical_except_check_py_sha256'] is True, 'silent_edits_accounted', rows=silent,
         note='a source edit always changes the recorded check.py sha256, which freeze.json and the source manifest bind')

    # ---------------- own validator on damaged packets
    need(validate_producer(res, truth), 'own_validator_accepts_frozen_packet')
    damaged = []

    def dmg(label, fn):
        pk = json.loads(json.dumps(res))
        fn(pk)
        try:
            validate_producer(pk, truth)
        except Rejected as exc:
            damaged.append({'packet': label, 'rejected_for': str(exc)})
            return
        raise ReviewFailure('damaged packet accepted: ' + label)
    dmg('tier_lower_raised', lambda p: p['headline'].__setitem__('tier_lower', q(F(p['headline']['tier_lower']) + F(1, 10 ** 20))))
    dmg('tier_upper_lowered', lambda p: p['headline'].__setitem__('tier_upper', q(F(p['headline']['tier_upper']) - F(1, 10 ** 20))))
    dmg('K2_prime_quartered', lambda p: p['headline'].__setitem__('K2_prime', q(F(p['headline']['K2_prime']) / 4)))
    dmg('sqrt10_bracket_swapped', lambda p: p['label'].__setitem__('sqrt10_enclosure', p['label']['sqrt10_enclosure'][::-1]))
    dmg('relative_width_halved', lambda p: p['headline'].__setitem__('relative_width_upper', q(F(p['headline']['relative_width_upper']) / 2)))
    dmg('separation_doubled', lambda p: p['headline'].__setitem__('plus_minus_tau_separation_lower', q(2 * F(p['headline']['plus_minus_tau_separation_lower']))))
    dmg('falsifier_beyond_2K2', lambda p: p['headline'].__setitem__('falsifier_separation_lower', q(truth['twoK2t2'] * 2)))
    dmg('obligation_row_dropped', lambda p: p.__setitem__('obligations', p['obligations'][:5]))
    dmg('uniqueness_claimed', lambda p: p.__setitem__('uniqueness_claimed', True))
    dmg('rate_in_N_claimed', lambda p: p.__setitem__('rate_in_N_claimed', True))
    dmg('resolved_interaction_shift', lambda p: p.__setitem__('resolved_interaction_shift', True))
    dmg('closeness_order_1_only', lambda p: p.__setitem__('closeness_order', [1]))
    dmg('tier_relabelled_dynamical', lambda p: p['label'].__setitem__('kind', 'dynamical'))
    dmg('gate_hash_changed', lambda p: p.__setitem__('ay1_gate_sha256', '0' * 64))
    need(len(damaged) == 14, 'own_validator_rejects_damaged_packets', rows=damaged)

    return {
        'loop': 'AY2', 'stage': 'post_comparison', 'human_author': 'Hruday N M (BUNZEEY)',
        'reviewer': 'model-agent skeptic with correlated ancestry; not human peer review or formal verification',
        'checker_sha256': sha(Path(__file__)), 'contract_sha256': CONTRACT_SHA, 'ay1_gate_sha256': AY1_GATE_SHA,
        'producer_frozen': FROZEN, 'pre_comparison_freeze_sha256': PRE_FREEZE_SHA,
        'bound_values': {
            'tier_label': 'first_order_distance_from_product',
            'tier_lower_producer': q(Lp), 'tier_upper_producer': q(Up),
            'sqrt10_bracket_producer': [q(lo30), q(hi30)],
            'tier_lower_skeptic': q(Ls), 'tier_upper_skeptic': q(Us), 'sqrt10_bracket_skeptic': [q(lo40), q(hi40)],
            'relative_width_upper_producer': q(rw_p), 'target': q(target),
            'plus_minus_tau_separation_lower_producer': q(sep_p), 'falsifier_separation_lower_producer': q(L_target),
            'K2_prime': q(k2_g), 'K2_prime_tau2': q(truth['K2t2']), 'two_K2_prime_tau2': q(truth['twoK2t2']),
            'D': q(d_g), 'two_D': q(2 * d_g), 'K2_plus': q(k2p_g)},
        'counts': {'review_checks': len(CHECKS) + 0, 'must_abort_edits': 42, 'silent_edits': 3, 'damaged_packets': 14,
                   'producer_checks': 42, 'producer_control_rejections': 85, 'producer_total_rejections': 114},
        'checks': CHECKS,
        'previews': {'tier': [preview(Lp), preview(Up)], 'relative_width': preview(rw_p), 'margin': preview(target / rw_p, 8),
                     'separation': preview(sep_p), 'falsifier': preview(L_target), 'own_falsifier': preview(diff_lo),
                     'label': 'floating previews only; no Boolean reads them'},
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
    result = run()
    out.mkdir(parents=True, exist_ok=True)
    (out / 'results.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'checks': len(result['checks']), 'must_abort': 42, 'silent': 3, 'damaged_packets': 14,
                      'tier': result['previews']['tier']}))


if __name__ == '__main__':
    main()
