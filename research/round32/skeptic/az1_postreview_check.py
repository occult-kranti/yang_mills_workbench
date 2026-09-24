#!/usr/bin/env python3
"""AZ1 post-comparison skeptic checks, written after the single forward producer froze.

Human project author: Hruday N M (BUNZEEY). Model-agent skeptic with correlated
ancestry (same model family as the advisor and the producer; five AZ1 control ids
come from the skeptic's own prospective controls and its AX1 review is a shared
premise); not human peer review or formal verification.

AZ1 is a statement+skeptic loop (producers=["forward"],
single_direction_independent_replay): admission rests on the forward producer plus
the skeptic's frozen pre-comparison package (az1_check.py,
az1-independent/results.json, committed 649db92 before the producer commit 8359876).
This file adds:
  * integrity: contract, AX1 and AL1 gate hashes; the forward closure file by file
    (replay_loop.verify_freeze, imported unchanged) with the frozen hashes pinned;
    the 29-file premise inventory, each byte-identical to its repository source, no
    skeptic/az1* input, no reverse/az1 package; the source manifest; the unchanged
    pre-comparison package and its byte-identical replay;
  * the producer replayed under normal and -O Python into fresh directories outside
    the checkout (byte-for-byte against output/) and tools/freeze.py verify, with
    the unchanged replay_loop functions (replay_loop.py always replays a reverse
    package and replay_declared.py refuses direction statement+skeptic);
  * exact comparison of every producer headline with the skeptic's predictions and
    own re-derivations (the pre-comparison module is imported from its pinned bytes;
    nothing is imported from the producer): the eleven dictionary identities as
    rational-function identities, the cap g^4, the four crossover indices and their
    neighbouring g^4 and tau values, the labelled extra crossovers, the directed
    lattice-units floor, the gap examples, the rescaling invariances and exponents;
  * gate fields and flags; a negation-aware scan of report.md (the producer's
    exclusion of the mandatory sentence and of code spans analysed; forbidden
    phrases, fractions, the two senses of "uniform", scoping to g_n->0, the
    "not found" sentence with the Faizal-Shabir disclosure);
  * source-edit mutations on temporary copies of the closure outside the checkout:
    one validator weakening per contract control (the producer's own damaging
    mutation must then be accepted and abort the run), value, input and report
    edits; the unmutated copy must reproduce output/ byte for byte; silent edits are
    accounted for; this review's own validator rejects damaged packets.

Standard library only; exact Fractions decide every Boolean; failures are explicit
exceptions (never assert), so the output bytes match under python -O.

Usage: python3 -B research/round32/skeptic/az1_postreview_check.py --output /abs/fresh/dir
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

CONTRACT_REL = 'research/round32/contracts/az1.json'
CONTRACT_SHA = '91c828a7aa6ef9bd4d3dbf762363b7558faa6922c23e1aff476cd098d4177078'
AX1_GATE_REL = 'research/round32/advisor/ax1-gate.json'
AX1_GATE_SHA = '1b8fb152696659439bb01fc7df429fc76fa3132d4936df450d8131256015d177'
AL1_GATE_REL = 'research/round29/advisor/al1-gate.json'
AL1_GATE_SHA = 'e415203cc6b6ebca6cea5fcd1230a7eb0e20b7ab2d2e6c99dc8aa2dd3052a75b'
AM2_GATE_SHA = 'be4ec35a004c831f8ea0771df84bf8e3e6aa02681107b57265a0ddc82d45211d'
MOD4_REL = 'research/round32/experts/modern/update-4.md'
REPLAY_LOOP_SHA = 'e627df048d9db128ae622dfd5030b887be442645b787d1fb29b4b2fec79ced66'
FREEZE_TOOL_SHA = '85a5462e649e3f10073c4125ac05f9a468b28b47d5de23e12ca50d0351b0bcd4'
FWD_REL = 'research/round32/forward/az1'
FWD = ROOT / FWD_REL
FROZEN = {  # forward closure, as frozen and committed (8359876)
    'freeze.json': 'a7a910a7b19451ca1c84834f3400e782cbbc483a5725881a65709c670a7b4e9f',
    'check.py': 'd69eb05ff420dfbed2cb543c020fa9156d35c662e1f6df2cfe4f26b50afb5c4a',
    'report.md': '0270e36dfd179b7622b40d89fede50db46c874e1be5c8c28bb1ef0b7d4829878',
    'output/results.json': '185cca20e0eaab251c649eeeb403cdf12a19562af253f2818dd9c8e9a6d908ea',
    'output/source-manifest.json': '6e3979415ae1e2b4d9ab1ae6afe0e9c63118025dc8589e9ae538becd05e5eb21',
}
PRE_FREEZE_REL = 'research/round32/skeptic/az1-independent-freeze.json'
PRE_FREEZE_SHA = '88603b8b6a78012f835d243e69bcb592f604f6afc2fa611cd127cb9eefededfa'
PRE_CHECK_REL = 'research/round32/skeptic/az1_check.py'
PRE_CHECK_SHA = 'c31cea4630fad66a5440488718178129a942196f41157da92e40c8a3f2842f7e'
PRE_RESULTS_REL = 'research/round32/skeptic/az1-independent/results.json'
TAU = F(1, 10 ** 8)
CAP_G4 = F(9600000000)
BRIDGE_G4 = F(32)
SCOPE = 'volume-uniform at fixed a, strong bare coupling'
IDENTITIES = ['alpha/16=g^2/(32a)', 'tau=96/g^4', 'alpha*lambda*a^2=1', 'r=4/g^4', 'alpha*tau/24=lambda',
              '(alpha/8)*(tau/3)=lambda', '7*tau=672/g^4', 'tau/144=2/(3g^4)', '(alpha/8)/2=g^2/(32a)',
              'a*alpha/16=g^2/32', 'tau*g^4=96']
GATE_FALSE = ('continuum_claim', 'uniform_in_a_claimed', 'weak_coupling_claim', 'loop_count_fraction_claimed')
FLAGS_FALSE = ('uniform_wilson_claim', 'resolved_interaction_shift', 'scientific_priority_verified')


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


def dec_value(text):
    mant, _, ex = text.partition('e')
    ex = int(ex or '0')
    decimals = len(mant.split('.')[1]) if '.' in mant else 0
    return F(mant) * F(10) ** ex, F(10) ** (ex - decimals)


def trunc_ok(text, lo, hi=None):
    """text is the truncation toward zero of a positive value in [lo, hi] (hi=lo for an exact value)."""
    hi = lo if hi is None else hi
    val, unit = dec_value(text)
    return val <= lo and hi < val + unit


def load_pre_module():
    path = ROOT / PRE_CHECK_REL
    if sha(path) != PRE_CHECK_SHA:
        raise ReviewFailure('pre-comparison checker bytes changed')
    spec = importlib.util.spec_from_file_location('az1_skeptic_pre_comparison', str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ------------------------------------------------------------ own identity engine (pre-comparison RF class)
def identity_table(pm):
    """The eleven producer identity strings, each mapped to an explicit pair of rational functions in (G=g^2, a)."""
    RF = pm.RF
    alpha, lam = RF.mono(F(1, 2), 1, -1), RF.mono(2, -1, -1)
    tau = (lam / alpha).scale(24)
    a_, g2 = RF.mono(1, 0, 1), RF.mono(1, 1, 0)
    one = RF.mono(1, 0, 0)
    return {
        'alpha/16=g^2/(32a)': (alpha.scale(F(1, 16)), RF.mono(F(1, 32), 1, -1)),
        'tau=96/g^4': (tau, RF.mono(96, -2, 0)),
        'alpha*lambda*a^2=1': (alpha * lam * a_ * a_, one),
        'r=4/g^4': (lam / alpha, RF.mono(4, -2, 0)),
        'alpha*tau/24=lambda': ((alpha * tau).scale(F(1, 24)), lam),
        '(alpha/8)*(tau/3)=lambda': (alpha.scale(F(1, 8)) * tau.scale(F(1, 3)), lam),
        '7*tau=672/g^4': (tau.scale(7), RF.mono(672, -2, 0)),
        'tau/144=2/(3g^4)': (tau.scale(F(1, 144)), RF.mono(F(2, 3), -2, 0)),
        '(alpha/8)/2=g^2/(32a)': (alpha.scale(F(1, 8)).scale(F(1, 2)), RF.mono(F(1, 32), 1, -1)),
        'a*alpha/16=g^2/32': (a_ * alpha.scale(F(1, 16)), RF.mono(F(1, 32), 1, 0)),
        'tau*g^4=96': (tau * g2 * g2, RF.mono(96, 0, 0)),
    }, {'alpha': alpha, 'lambda': lam, 'tau': tau, 'gap': alpha.scale(F(1, 16)), 'lattice_gap': a_ * alpha.scale(F(1, 16)),
        'r': lam / alpha}


def degrees(rf, idx):
    """Homogeneity degree of a rational function in variable idx (0: G=g^2, 1: a); None if not homogeneous."""
    dn = {k[idx] for k in rf.num}
    dd = {k[idx] for k in rf.den}
    if len(dn) != 1 or len(dd) != 1:
        return None
    return dn.pop() - dd.pop()


# ------------------------------------------------------------ report scans (this review's rules)
def strip_code(text):
    text = re.sub(r'```.*?```', ' ', text, flags=re.S)
    return re.sub(r'`[^`\n]*`', ' ', text)


BROAD_NEG = re.compile(r'\b(not|no|never|none|nor|fails?|failed|failure|without|missing|requires?|required|cannot|'
                       r'unproved|excluded?|exclusions?|forbidden)\b')


def sentence_split(text):
    return [s for s in re.split(r'(?<=[.!?])\s+|\n', text) if s.strip()]


def report_scan(rep, template, pm):
    """Returns a dict of findings; raises Rejected on a violation of the contract rules."""
    if rep.count(template) != 1:
        raise Rejected('mandatory sentence must occur exactly once')
    body = rep.replace(template, ' ', 1)
    low_body = body.lower()
    lines = body.splitlines()
    # forbidden claims outside the template: each in a negated frame, or inside the verbatim claim-exclusion list
    outside = []
    for name, pat in pm.CLAIM_PATTERNS:
        for m in pat.finditer(low_body):
            ln = low_body[:m.start()].count('\n')
            line = lines[ln]
            start_of_line = low_body.rfind('\n', 0, m.start()) + 1
            sent_start = max(low_body.rfind('. ', 0, m.start()) + 2, start_of_line)
            prefix = low_body[sent_start:m.start()]
            in_exclusion_list = line.startswith('- **Contract, verbatim:**') or line.startswith('- **Preregistration, verbatim:**')
            in_code = any(mm.start() <= m.start() - start_of_line < mm.end() for mm in re.finditer(r'`[^`\n]*`', line.lower()))
            negated = bool(pm.NEG_FRAME.search(prefix)) or bool(re.search(r'\b(no|not|never)\b', prefix.replace('not only', '')))
            if not ((in_exclusion_list and in_code) or negated):
                if name == 'fraction of the problem':
                    raise Rejected('loop count is not a fraction: ' + line[:80])
                raise Rejected('forbidden phrasing: ' + name + ': ' + line[:80])
            outside.append({'phrase': name, 'line': ln + 1,
                            'context': 'verbatim claim-exclusion list (code span)' if (in_exclusion_list and in_code) else 'negated sentence'})
    for sent in sentence_split(strip_code(body).lower()):
        if 'limit exists' in sent and not BROAD_NEG.search(sent):
            raise Rejected('"limit exists" asserted: ' + sent[:80])
    # two senses of "uniform": never shared without the N-qualifier; the a-sense never asserted (prose);
    # scope to g_n->0 read with code spans kept (the scope often sits in a code span)
    shared, a_unneg, unscoped, codespan_a = [], [], [], set()
    for ln, line in enumerate(body.splitlines(), 1):
        for keep_code, text in ((True, line), (False, strip_code(line))):
            for sent in sentence_split(text):
                for clause in pm.sentences(sent):
                    kinds = {k for k, _ in pm.uniform_tokens(clause)[1]}
                    if 'a' in kinds and 'bare' in kinds and 'N' not in kinds:
                        shared.append((ln, clause[:90]))
                masked, toks = pm.uniform_tokens(sent)
                a_toks = [st for k, st in toks if k == 'a']
                if not a_toks:
                    continue
                if keep_code:
                    for st in a_toks:
                        if masked.startswith('uniform along a_n', st) and not pm.SCOPE_G0.search(masked):
                            unscoped.append({'line': ln, 'sentence': sent.strip()[:160]})
                    if not any(k == 'a' for k, _ in pm.uniform_tokens(strip_code(sent))[1]):
                        codespan_a.add(ln)
                elif not BROAD_NEG.search(masked.replace('not only', '')):
                    a_unneg.append((ln, sent[:90]))
    if shared:
        raise Rejected('uniform senses share a sentence without the qualifier: %r' % shared[:2])
    if a_unneg:
        raise Rejected('uniform in a claimed: %r' % a_unneg[:2])
    return {'forbidden_outside_template': outside, 'unscoped_along_a_n': unscoped,
            'code_span_a_sense_lines': sorted(set(codespan_a))}


# ------------------------------------------------------------ own validator of producer packets
def validate_producer(res, truth):
    if res.get('contract_sha256') != CONTRACT_SHA or res.get('ax1_gate_sha256') != AX1_GATE_SHA \
            or res.get('al1_gate_sha256') != AL1_GATE_SHA or res.get('am2_gate_sha256') != AM2_GATE_SHA:
        raise Rejected('contract or gate hash differs')
    h = res['headline']
    if h['identities_verified'] != IDENTITIES or not all(truth['identities'][i] for i in h['identities_verified']):
        raise Rejected('identity list differs or an identity fails')
    if F(h['tau_cap']) != TAU or F(h['g4_at_cap']) != CAP_G4 or F(h['bridge_g4']) != BRIDGE_G4:
        raise Rejected('cap or bridge coupling differs')
    cr = h['crossovers']
    got = (cr['cap_declared_g0^4=9600000000']['n*_cap'], cr['cap_declared_g0^4=9600000000']['n*_bridge'],
           cr['panel_rehearsal_g0=1000']['n*_cap'], cr['panel_rehearsal_g0=1000']['n*_bridge'])
    if got != truth['n_star'] or F(cr['cap_declared_g0^4=9600000000']['g0_4']) != CAP_G4 \
            or F(cr['panel_rehearsal_g0=1000']['g0_4']) != 10 ** 12:
        raise Rejected('crossover indices differ')
    fl = F(h['lattice_units_floor_lower'])
    if not ((32 * fl) ** 2 <= CAP_G4 and fl > F(306186, 100) and truth['floor_hi'] - fl < F(1, 10 ** 29)):
        raise Rejected('lattice-units floor is not a directed lower bound of 1250 sqrt 6')
    ge = h['gap_example']
    if F(ge['gap_fm_inverse']) != F(ge['g2']) / (32 * F(ge['a_fm'])) or F(ge['g2']) ** 2 < CAP_G4 \
            or F(ge['gap_over_E_star']) != F(ge['gap_fm_inverse']):
        raise Rejected('gap example differs from g^2/(32a) or lies outside the admitted regime')
    gf = res['gate_fields']
    for k in GATE_FALSE:
        if gf.get(k) is not False or res.get(k) is not False:
            raise Rejected('gate field claimed: ' + k)
    if gf.get('uniform_in_N_claimed') is not True or gf.get('uniform_in_N_scope') != SCOPE or res.get('uniform_in_N_scope') != SCOPE:
        raise Rejected('uniform_in_N field or scope string')
    for k in FLAGS_FALSE:
        if res.get(k) is not False:
            raise Rejected('claim flag set: ' + k)
    if res['mandatory_sentence'] != truth['template']:
        raise Rejected('mandatory sentence differs from the contract template')
    est = res['estimates']
    if len(est) != 1 or est[0]['cited_not_rederived'] is not True or est[0]['uniform_in'] != 'N (volume) at fixed a' \
            or est[0]['uniform_along_a_n'] is not False or est[0]['citation_sha256'] != AX1_GATE_SHA or F(est[0]['regime_g4']) != CAP_G4:
        raise Rejected('the one estimate is not the cited volume-uniform gap')
    rq = res['requirements']
    if [r['requirement'] for r in rq] != ['uniform-in-a estimates', 'reconstruction hypotheses', 'physical scale control'] \
            or any(r['status'] != 'missing' or len(r['missing_premise']) < 60 for r in rq):
        raise Rejected('requirements table')
    ld = res['leads_recorded']
    if len(ld) != 1 or ld[0]['audited'] is not False or ld[0]['imported'] is not False or '2606.19362' not in ld[0]['source']:
        raise Rejected('lead imported or audited')
    tr = res['trajectory']
    if tr['derived'] is not False or 'hypothesis' not in tr['status'] or tr['claimed_physical_trajectory'] is not False:
        raise Rejected('trajectory not a hypothesis')
    rt = res['retained_failures']
    if (rt['cap_declared_toy_leaves_admitted_regime'], rt['cap_declared_toy_leaves_bridge'], rt['panel_toy_leaves_admitted_regime'],
            rt['panel_toy_leaves_bridge']) != ('n*=2', 'n*=132', 'n*=4', 'n*=421') or 'al1_frozen_path_fails_bridge_every_n' not in rt:
        raise Rejected('retained failures')
    if not res['proposed_forward_verdict'].startswith('accepted_within_scope ') or res['controls_with_damaging_mutations'] != 21 \
            or res['controls_deferred'] != {}:
        raise Rejected('verdict or controls')
    return True


# ------------------------------------------------------------ source-mutation replays
CHK, REP = 'check.py', 'report.md'


def mutated_run(edits=(), input_edits=(), extra_input=None, remove_input=None, report_append=None, report_drop_prefix=None):
    """Copy the frozen closure outside the checkout, apply one edit set, run check.py once."""
    with tempfile.TemporaryDirectory(prefix='hnm-r32-az1-skeptic-mut-') as tmp:
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
            path.write_bytes(raw.replace(old, new))
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
        report_text = texts[REP]
        return done.returncode, outputs, last.replace(tmp, '<tmp>'), report_text


def ret_true(anchor):
    """Insert 'return True' right after a validator's def line (or before an anchored first statement)."""
    indent = '        ' if anchor.startswith('    def ') else '    '
    return (CHK, anchor, anchor + indent + 'return True\n')


CONTRACT_EDIT = (CONTRACT_REL, b'"stop": "Investigation 9 of 10."', b'"stop": "Investigation 9 of 11."', 1)
MUST_ABORT = [
    # one validator weakening per contract control: the producer's own damaging mutation must then be accepted
    ('ctl_missing_incoming_stars', dict(edits=[ret_true('    def validate_incidence(inc, j_per_tau):\n')]),
     'damaging mutation accepted: outgoing_stars_only (2 anchors, per-site sum 8|tau|)'),
    ('ctl_full_original_wilson_cover', dict(edits=[ret_true('    def validate_cover(region, links):\n')]),
     'damaging mutation accepted: single_factor_cover_0'),
    ('ctl_wrong_delta_alpha_hbar_clock', dict(edits=[ret_true('    def validate_gap_units(normalized_gap, unit_over_alpha):\n')]),
     'damaging mutation accepted: normalized_gap_read_in_alpha_units (alpha/2)'),
    ('ctl_vector_versus_scalar_centering', dict(edits=[ret_true('    def validate_centering(kind):\n')]),
     'damaging mutation accepted: vector_centering_imposed_on_a_statement'),
    ('ctl_first_order_mean_charged', dict(edits=[ret_true('    def validate_first_order(coef_over_tau):\n')]),
     'damaging mutation accepted: first_order_mean_set_to_zero'),
    ('ctl_tau_scaling_exponent', dict(edits=[ret_true('    def validate_exponents(claimed):\n')]),
     'damaging mutation accepted: tau_read_as_96_over_g2'),
    ('ctl_changed_model_relabelled', dict(edits=[ret_true('    def validate_model(mdl):\n')]),
     'damaging mutation accepted: patterned_zero_selected_model'),
    ('ctl_coherent_evidence_tampering', dict(edits=[(CHK, "            require(cid in ids and ids[cid]['passed'] is True, 'required control missing or failed: ' + cid)\n",
                                                     '            pass\n')]),
     'damaging mutation accepted: control_boolean_flipped_hash_rebound'),
    ('ctl_insufficient_verdict_retained', dict(edits=[ret_true('    def validate_verdict(reported, *args):\n')]),
     'damaging mutation accepted: missing_citation_relabelled_accepted'),
    ('ctl_exact_arithmetic_admission', dict(edits=[(CHK, "    raise AdmissionError('malformed rational rejected: ' + repr(value))\n", '    return Q(0)\n')]),
     'damaging mutation accepted: nan_input'),
    ('ctl_root_n_misuse', dict(edits=[ret_true('    def validate_root_route(kind, n_claim, g04, T):\n')]),
     'damaging mutation accepted: square_root_index_11'),
    ('ctl_no_priority_or_continuum_claim', dict(edits=[(CHK, '        for k1, v1 in FLAGS.items():\n            require(',
                                                        "        for k1, v1 in FLAGS.items():\n            if k1 == 'continuum_claim':\n"
                                                        '                continue\n            require(')]),
     'damaging mutation accepted: continuum_true'),
    ('ctl_trajectory_named', dict(edits=[ret_true('    def validate_trajectory(tr):\n')]),
     'damaging mutation accepted: trajectory_claimed_derived'),
    ('ctl_bridge_obstruction_retained', dict(edits=[ret_true('    def validate_bridge(threshold, retained, rescaling_moves_tau):\n')]),
     'damaging mutation accepted: bridge_obstruction_dropped'),
    ('ctl_one_uniform_estimate_identified', dict(edits=[ret_true('    def validate_estimates(lst):\n')]),
     'damaging mutation accepted: no_estimate_identified'),
    ('ctl_e_star_fixed_no_plateau', dict(edits=[ret_true('    def validate_scales(e_star, e_star_varies, plateau_fit, node_selection):\n')]),
     'damaging mutation accepted: E_star_zero'),
    ('ctl_loop_count_not_fraction', dict(edits=[ret_true('    def validate_no_fraction(pk):\n')]),
     'damaging mutation accepted: investigation_index_as_fraction_field'),
    ('ctl_uniform_label_strong_coupling', dict(edits=[ret_true('    def validate_label(lb):\n')]),
     'damaging mutation accepted: weak_coupling_label'),
    ('ctl_uniform_in_N_not_in_a', dict(edits=[ret_true('    def scan_uniform(text):\n')]),
     'damaging mutation accepted: unqualified_uniform_sentence'),
    ('ctl_dictionary_arithmetic_exact', dict(edits=[ret_true('def validate_dictionary(env, identities):\n')]),
     'damaging mutation accepted: alpha_without_factor_two (alpha=g^2/a)'),
    ('ctl_toy_trajectory_crossover_exact', dict(edits=[(CHK, '    g04, T = rat(g04), rat(T)\n    require(isinstance(n_claim, int)',
                                                        '    return True\n    g04, T = rat(g04), rat(T)\n    require(isinstance(n_claim, int)')]),
     'damaging mutation accepted: cap_boundary_n1_counted_as_crossover'),
    # value and logic edits
    ('val_identity_tau_g4_95', dict(edits=[(CHK, "             'tau*g^4=96',\n", "             'tau*g^4=95',\n")]),
     'dictionary identity fails: tau*g^4=95'),
    ('val_crossover_root_plus_two', dict(edits=[(CHK, '        n = iroot(F, p) + 1\n', '        n = iroot(F, p) + 2\n')]),
     'crossover bracket'),
    ('val_example_spacing_one_fifth', dict(edits=[(CHK, 'A0_FM = Q(1, 10)', 'A0_FM = Q(1, 5)')]),
     'failed check gap_physical_units_example'),
    ('val_sqrt_scale_10_2', dict(edits=[(CHK, 'SQRT_SCALE = 10 ** 30', 'SQRT_SCALE = 10 ** 2')]),
     'report does not carry the exact value'),
    ('val_continuum_flag_true', dict(edits=[(CHK, "    FLAGS = {'continuum_claim': False,", "    FLAGS = {'continuum_claim': True,")]),
     'failed check gate_fields_exported'),
    ('val_scope_string_edit', dict(edits=[(CHK, "UNIFORM_IN_N_SCOPE = 'volume-uniform at fixed a, strong bare coupling'",
                                           "UNIFORM_IN_N_SCOPE = 'volume-uniform, strong bare coupling'")]),
     'scope string'),
    ('val_p1_detection_disabled', dict(edits=[(CHK, '    g3_int, g3_rem = divmod(10 ** 12, 81)\n', '    g3_int, g3_rem = divmod(10 ** 12 + 6, 81)\n')]),
     'failed check contract_wording_defects_recorded'),
    # inputs
    ('inp_contract_byte_edit', dict(input_edits=[CONTRACT_EDIT]), 'contract snapshot bytes differ from the frozen AZ1 contract'),
    ('inp_ax1_gate_gap_alpha_over_8', dict(input_edits=[(AX1_GATE_REL, b'(alpha/16 physical)', b'(alpha/8 physical)', 1)]),
     'failed check ax1_gate_fields_and_verdict'),
    ('inp_al1_gate_bridge_31', dict(input_edits=[(AL1_GATE_REL, b'requires g^4>=32;', b'requires g^4>=31;', 1)]),
     'failed check gate_bindings_match_snapshots'),
    ('inp_modern_update4_421_to_420', dict(input_edits=[(MOD4_REL, b'first fails at **`n*=421`**', b'first fails at **`n*=420`**', 1)]),
     'failed check toy_trajectory_crossover_exact'),
    ('inp_undeclared_skeptic_az1_input', dict(extra_input='research/round32/skeptic/az1-independent-derivation.md'),
     'failed check premise_inventory_bound'),
    ('inp_premise_snapshot_removed', dict(remove_input='research/round29/forward/aq2/report.md'), 'failed check premise_inventory_bound'),
    # report
    ('rep_R3_row_removed', dict(report_drop_prefix='| R3 |'), 'exactly three requirement rows'),
    ('rep_template_negation_removed', dict(edits=[(REP, 'this is not a statement that the continuum limit exists',
                                                   'this is a statement that the continuum limit exists')]),
     'mandatory sentence (contract template) missing from the report'),
    ('rep_continuum_phrase_appended', dict(report_append='\nThe continuum limit exists along the toy.\n'),
     'forbidden phrasing in the report: the continuum limit exists'),
    ('rep_uniform_in_a_appended', dict(report_append='\nThe gap is uniform in a.\n'), 'uniform qualifier rule violated'),
    ('rep_bridge_index_132_to_131', dict(edits=[(REP, 'n*=132', 'n*=131')]), 'crossover index missing from the report: 132'),
    ('rep_map_row_removed', dict(report_drop_prefix='| `root_n_misuse` | §§'), 'map lacks rows for root_n_misuse'),
    ('rep_lead_paragraph_removed', dict(report_drop_prefix='**The one recorded lead.**'), 'required statement missing: unaudited'),
]
SILENT = [
    ('rep_percentage_of_the_problem_appended', dict(report_append='\nRound32 has settled 90% of the continuum problem.\n'),
     'report_scan', 'the producer scan tests the literal phrase "fraction of the problem" only; this review\'s pattern scan rejects it'),
    ('rep_fraction_of_the_continuum_problem_appended', dict(report_append='\nThis loop resolves a fraction of the continuum problem.\n'),
     'report_scan', 'the literal "fraction of the problem" misses "fraction of the continuum problem"; this review\'s pattern scan rejects it'),
    ('rep_unscoped_along_a_n_appended', dict(report_append='\nThe fixed-spacing family supplies no estimate uniform along a_n->0.\n'),
     'unscoped', 'wording level: at fixed g the AX1 bounds hold at every a_n; this review lists the unscoped sentence'),
    ('inp_ax1_gate_unparsed_field', dict(input_edits=[(AX1_GATE_REL, b'"reviewer_path": "research/round32/skeptic/ax1.md"',
                                                       b'"reviewer_path": "research/round32/skeptic/ax1.md "', 1)]),
     'validator', 'the AX1 gate is not pinned in check.py (no gate binds it); caught by replay_loop.verify_freeze (snapshot versus source) '
                  'and by this review\'s validator (pinned AX1 gate sha256 in results)'),
]
CONTROL_LABEL_MAP = {m[0][4:]: m[2].split(': ', 1)[1] for m in MUST_ABORT if m[0].startswith('ctl_')}


def producer_replays():
    """replay_declared.py steps for the declared forward direction, with the unchanged replay_loop functions."""
    src = FWD
    closure = base.verify_freeze(src, 'az1')
    before = base.sha(src / 'freeze.json')
    expected = {p.relative_to(src / 'output').as_posix(): p.read_bytes() for p in (src / 'output').rglob('*') if p.is_file()}
    receipts = []
    for mode in ('normal', 'optimized'):
        with tempfile.TemporaryDirectory(prefix='hnm-r32-az1-forward-%s-' % mode) as temporary:
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
                             'stdout_sha256': sha_bytes(done.stdout.strip().encode())})
    tool = [sys.executable, '-B', str(R32 / 'tools/freeze.py'), 'verify', FWD_REL]
    fv = subprocess.run(tool, capture_output=True, text=True, cwd=str(ROOT))
    base.verify_freeze(src, 'az1')
    return closure, before, receipts, fv.returncode, fv.stdout.strip().splitlines()[-1] if fv.stdout.strip() else '', base.sha(src / 'freeze.json')


# ------------------------------------------------------------ main computation
def run():
    # ---------------- integrity
    con_raw = (ROOT / CONTRACT_REL).read_bytes()
    con = json.loads(con_raw)
    need(sha_bytes(con_raw) == CONTRACT_SHA and sha(ROOT / AX1_GATE_REL) == AX1_GATE_SHA and sha(ROOT / AL1_GATE_REL) == AL1_GATE_SHA
         and con['producers'] == ['forward'] and con['direction'] == 'statement+skeptic'
         and con['single_direction_independent_replay'] is True and sha(HERE / 'replay_loop.py') == REPLAY_LOOP_SHA
         and sha(R32 / 'tools/freeze.py') == FREEZE_TOOL_SHA, 'contract_gates_and_tools_pinned',
         contract_sha256=CONTRACT_SHA, ax1_gate_sha256=AX1_GATE_SHA, al1_gate_sha256=AL1_GATE_SHA, replay_loop_sha256=REPLAY_LOOP_SHA,
         freeze_tool_sha256=FREEZE_TOOL_SHA)
    frozen_ok = all(sha(FWD / k) == v for k, v in FROZEN.items())
    freeze = json.loads((FWD / 'freeze.json').read_text())
    listed = {k[len(FWD_REL) + 1:] for k in freeze['sources']}
    closure_files = {p.relative_to(FWD).as_posix() for p in FWD.rglob('*') if p.is_file()}
    need(frozen_ok and closure_files - {'freeze.json'} == listed and len(listed) == 33
         and all(sha(ROOT / k) == v for k, v in freeze['sources'].items()) and freeze['contract_sha256'] == CONTRACT_SHA
         and freeze['loop'] == 'AZ1' and freeze['direction'] == 'forward' and freeze['normal_optimized_identical'] is True,
         'forward_closure_frozen', closure_files=len(listed), freeze_json_sha256=FROZEN['freeze.json'])
    declared = sorted(['AGENTS.md', CONTRACT_REL] + list(con['shared_premises']))
    inputs = sorted(p.relative_to(FWD / 'inputs').as_posix() for p in (FWD / 'inputs').rglob('*') if p.is_file())
    need(inputs == declared and len(inputs) == 29 and all((FWD / 'inputs' / n).read_bytes() == (ROOT / n).read_bytes() for n in inputs)
         and not any(n.startswith('research/round32/skeptic/az1') for n in inputs)
         and not (R32 / 'reverse/az1').exists(), 'inventory_29_declared_identical',
         inputs=29, skeptic_inputs=[n for n in inputs if '/skeptic/' in n], reverse_package_present=False)
    manifest = json.loads((FWD / 'output/source-manifest.json').read_text())
    res = json.loads((FWD / 'output/results.json').read_text())
    need(all(sha(FWD / k) == v for k, v in manifest['sources'].items()) and len(manifest['sources']) == 31
         and manifest['outputs']['results.json'] == FROZEN['output/results.json']
         and res['check_py_sha256_recorded_before_evaluation'] == FROZEN['check.py'], 'source_manifest_and_check_sha',
         manifest_sources=len(manifest['sources']))
    closure, fz_before, receipts, fv_rc, fv_out, fz_after = producer_replays()
    need(closure['closure_files'] == 33 and closure['inputs'] == 29 and closure['inventory_equals_declared'] is True
         and all(r['byte_identical_to_frozen_output'] for r in receipts) and len(receipts) == 2 and fv_rc == 0
         and json.loads(fv_out)['status'] == 'verified' and fz_before == fz_after == FROZEN['freeze.json'],
         'producer_replays_byte_identical', replays=receipts, freeze_verify=json.loads(fv_out), closure=closure,
         method='replay_declared.py steps with the unchanged replay_loop.verify_freeze (replay_declared.py refuses '
                'direction statement+skeptic; replay_loop.py always replays a reverse package)')
    pre_freeze_raw = (ROOT / PRE_FREEZE_REL).read_bytes()
    pre_freeze = json.loads(pre_freeze_raw)
    need(sha_bytes(pre_freeze_raw) == PRE_FREEZE_SHA and pre_freeze['contract_sha256'] == CONTRACT_SHA
         and pre_freeze['stage'] == 'pre_comparison' and pre_freeze['loop'] == 'AZ1'
         and all(sha(ROOT / k) == v for k, v in pre_freeze['files'].items()) and pre_freeze['files'][PRE_CHECK_REL] == PRE_CHECK_SHA,
         'pre_comparison_package_unchanged', freeze_sha256=PRE_FREEZE_SHA, files=len(pre_freeze['files']))
    with tempfile.TemporaryDirectory(prefix='hnm-r32-az1-skeptic-pre-') as tmp:
        out = Path(tmp) / 'pre'
        flags = ['-B'] + (['-O'] if sys.flags.optimize else [])
        done = subprocess.run([sys.executable] + flags + [str(ROOT / PRE_CHECK_REL), '--output', str(out)],
                              capture_output=True, text=True, cwd=str(ROOT))
        pre_bytes = (out / 'results.json').read_bytes() if (out / 'results.json').is_file() else b''
    need(done.returncode == 0 and pre_bytes == (ROOT / PRE_RESULTS_REL).read_bytes(), 'pre_comparison_replay_byte_identical',
         results_sha256=sha_bytes(pre_bytes))
    pre = json.loads((ROOT / PRE_RESULTS_REL).read_text())
    pm = load_pre_module()
    template = con['preregistration']['mandatory_sentence_template']

    # ---------------- the eleven identities
    table, objs = identity_table(pm)
    ident_ok = {k: lhs.same(rhs) for k, (lhs, rhs) in table.items()}
    h = res['headline']
    pre_ids = pre['dictionary']['identities_verified']
    covered = {'alpha_over_16_equals_g2_over_32a': 'alpha/16=g^2/(32a)', 'tau_equals_96_over_g4': 'tau=96/g^4',
               'alpha_lambda_a2_equals_1': 'alpha*lambda*a^2=1', 'r_equals_4_over_g4': 'r=4/g^4',
               'nu_equals_lambda': 'alpha*tau/24=lambda', 'nu_over_delta_equals_tau_over_3': '(alpha/8)*(tau/3)=lambda',
               'local_norm_7tau_equals_672_over_g4': '7*tau=672/g^4', 'physical_gap_delta_times_normalized_gap': '(alpha/8)/2=g^2/(32a)',
               'inverse_g4_equals_4alpha_over_lambda': None}
    wrong = pm.RF.mono(1, 1, -1) * pm.RF.mono(2, -1, -1) * pm.RF.mono(1, 0, 1) * pm.RF.mono(1, 0, 1)
    need(h['identities_verified'] == IDENTITIES and len(set(IDENTITIES)) == 11 and all(ident_ok.values())
         and sorted(pre_ids) == sorted(covered) and not wrong.same(pm.RF.mono(1, 0, 0))
         and all(pm.dictionary_identities(pm.REF_DICT).values()), 'eleven_identities_rational_function',
         identities=IDENTITIES, method='explicit pairs of rational functions in (G=g^2, a) from the pre-comparison RF class; '
                                       'num1*den2-num2*den1 is the zero polynomial for each',
         pre_comparison_identities=len(pre_ids), shared_with_pre=sorted(v for v in covered.values() if v),
         new_in_producer=['tau/144=2/(3g^4)', 'a*alpha/16=g^2/32', 'tau*g^4=96'],
         skeptic_only=['g^4=4 alpha/lambda (inverse map)'], discriminator='alpha=g^2/a gives alpha*lambda*a^2=2')
    # rescaling invariances and exponents by homogeneity degree (valid for every scale factor c>0)
    deg = {k: (degrees(v, 0), degrees(v, 1)) for k, v in objs.items()}
    exp_p = res['checks'][[c['id'] for c in res['checks']].index('tau_scaling_exponent')]['exponents']
    resc = res['checks'][[c['id'] for c in res['checks']].index('dictionary_identities_symbolic')]['rescaling']
    samples_ok = all(objs['tau'].at(F(97979), c * F(7, 3)) == objs['tau'].at(F(97979), F(7, 3))
                     and objs['gap'].at(F(97979), c * F(7, 3)) == objs['gap'].at(F(97979), F(7, 3)) / c for c in (F(1, 3), F(5), F(10 ** 6)))
    need(deg == {'alpha': (1, -1), 'lambda': (-1, -1), 'tau': (-2, 0), 'gap': (1, -1), 'lattice_gap': (1, 0), 'r': (-2, 0)}
         and exp_p == {'tau': {'g': -4, 'a': 0}, 'alpha': {'g': 2, 'a': -1}, 'lambda': {'g': -2, 'a': -1},
                       'gap alpha/16': {'g': 2, 'a': -1}, 'lattice gap a*alpha/16': {'g': 2, 'a': 0}}
         and all(v is True for v in resc.values()) and len(resc) == 5 and samples_ok, 'rescaling_invariances_and_exponents',
         degrees_in_G_and_a={k: list(v) for k, v in deg.items()}, producer_exponents_in_g_and_a=exp_p, producer_rescaling=resc,
         reading='tau and r have degree 0 in a (a->c a leaves them fixed for every c>0); alpha, lambda and the gap have degree -1; '
                 'common rescaling of (alpha, lambda) is a->a/s at fixed g; g-exponents are twice the G-degrees')

    # ---------------- cap, bridge, crossovers
    tr = res['checks'][[c['id'] for c in res['checks']].index('toy_trajectory_crossover_exact')]['crossovers']
    own = {}
    for tag, g04 in (('cap_declared', CAP_G4), ('panel_rehearsal', F(10 ** 12))):
        for thr_tag, thr in (('cap', CAP_G4), ('bridge', BRIDGE_G4)):
            n = pm.n_star(g04, thr)
            if n != pm.n_star_brute(g04, thr):
                raise ReviewFailure('own crossover routes disagree')
            row = tr[tag][thr_tag]
            ok = (row['n_star'] == n and F(row['g_n_star^4']) == g04 / F(n) ** 4
                  and (row['g_last^4'] is None if n == 1 else F(row['g_last^4']) == g04 / F(n - 1) ** 4)
                  and F(row['tau_n_star']) == 96 * F(n) ** 4 / g04 and F(row['threshold_g4']) == thr)
            if not ok:
                raise ReviewFailure('producer crossover row differs: %s %s' % (tag, thr_tag))
            own[tag + '_' + thr_tag] = n
    pre_toy = pre['toy_trajectory']
    need(own == {'cap_declared_cap': 2, 'cap_declared_bridge': 132, 'panel_rehearsal_cap': 4, 'panel_rehearsal_bridge': 421}
         and pre_toy['declared']['cap']['n_star'] == 2 and pre_toy['declared']['bridge']['n_star'] == 132
         and pre_toy['rehearsal_g0_1000']['cap']['n_star'] == 4 and pre_toy['rehearsal_g0_1000']['bridge']['n_star'] == 421
         and F(h['g4_at_cap']) == CAP_G4 == 96 / TAU and F(h['tau_cap']) == TAU and F(h['bridge_g4']) == BRIDGE_G4
         and F(pre['regime']['admitted_g4_min']) == CAP_G4, 'cap_bridge_and_crossovers_equal_predictions',
         n_star=own, g4_at_cap=h['g4_at_cap'], tau_at_crossings=[tr['cap_declared']['cap']['tau_n_star'], tr['cap_declared']['bridge']['tau_n_star'],
                                                              tr['panel_rehearsal']['cap']['tau_n_star'], tr['panel_rehearsal']['bridge']['tau_n_star']],
         prediction='pre-comparison: declared 2 and 132, g_0=1000: 4 and 421 (exact)')
    sens = res['checks'][[c['id'] for c in res['checks']].index('fixed_cap_sensitivity_not_admitted')]['sensitivity']
    anyg = res['checks'][[c['id'] for c in res['checks']].index('any_g_to_zero_path_leaves_regime')]
    excl_g4 = 96 / F(1, 20416)
    need(sens['selfmap_only']['n*_cap_declared_toy'] == pm.n_star(CAP_G4, F(26370048, 7)) == 8
         and sens['selfmap_only']['n*_panel_toy'] == pm.n_star(F(10 ** 12), F(26370048, 7)) == 23
         and sens['exclusion_only']['n*_cap_declared_toy'] == pm.n_star(CAP_G4, excl_g4) == 9
         and sens['exclusion_only']['n*_panel_toy'] == pm.n_star(F(10 ** 12), excl_g4) == 27
         and F(sens['selfmap_only']['tau_bound']) == F(7, 274688) and F(sens['exclusion_only']['tau_bound']) == F(1, 20416)
         and all(v['admitted'] is False for v in sens.values())
         and anyg['slower_toy']['n*_cap'] == pm.n_star(F(10 ** 12), CAP_G4, power=1) == 105
         and anyg['slower_toy']['n*_bridge'] == 31250000001 and F(10 ** 12) / 31250000001 < 32 <= F(10 ** 12) / 31250000000
         and pre_toy['declared']['route_radius_labelled']['n_star'] == 8 and pre_toy['rehearsal_g0_1000']['route_radius_labelled']['n_star'] == 23,
         'labelled_extra_crossovers', selfmap=[8, 23], exclusion=[9, 27], slower_toy=[105, 31250000001],
         note='labelled, not admitted; the skeptic pre-comparison printed the self-map crossovers 8 and 23')

    # ---------------- lattice-units floor and physical examples
    s6_lo, s6_hi = pm.sqrt_bracket(6, 10 ** 40)
    fl_p = F(h['lattice_units_floor_lower'])
    fl_lo, fl_hi = 1250 * s6_lo, 1250 * s6_hi
    truth = {'floor_hi': fl_hi, 'template': template, 'n_star': (2, 132, 4, 421), 'identities': ident_ok}
    need((32 * fl_p) ** 2 <= CAP_G4 and fl_p <= fl_hi and fl_hi - fl_p < F(1, 10 ** 30) and fl_p > F(306186, 100)
         and fl_lo ** 2 <= F(9375000) <= fl_hi ** 2 and F(pre['regime']['lattice_gap_floor_sq']) == 9375000
         and h['lattice_units_floor_preview'] == '3.06186217847e3' and trunc_ok('3.06186217847e3', fl_p, fl_hi),
         'lattice_units_floor_directed', producer=q(fl_p), skeptic_bracket=[q(fl_lo), q(fl_hi)], exact='1250 sqrt 6 = sqrt(9.6x10^9)/32',
         relation='producer lower end (10^-30 sqrt bracket) <= 1250 sqrt 6 and within 10^-30 of it; > 3061.86')
    ge = h['gap_example']
    gp = res['checks'][[c['id'] for c in res['checks']].index('gap_physical_units_example')]
    hbarc = F(1973269804, 10 ** 7)
    along = res['checks'][[c['id'] for c in res['checks']].index('toy_gap_along_path')]['along']
    cap_lo_p = F(gp['cap_example']['gap_over_E_star_lower'])
    need(F(ge['g2']) == 10 ** 6 and F(ge['a_fm']) == F(1, 10) and F(ge['gap_fm_inverse']) == 312500 == F(10 ** 6) / (32 * F(1, 10))
         and trunc_ok(ge['gap_MeV_preview'], 312500 * hbarc) and F(gp['alpha'].split()[0]) == 5000000
         and 10 * fl_p == cap_lo_p and trunc_ok('3.06186217847e4', cap_lo_p, 10 * fl_hi)
         and [x['gap_over_E_star_lower'] for x in along] == ['312500', '156250', '312500/3', None, None]
         and F(pre['physical_example']['gap_lower_MeV']) == 31250 * hbarc, 'gap_examples',
         producer_example='g^2=10^6 (g_0=1000, n=1), a=1/10 fm: Delta>=312500 fm^-1 = 312500 E_star (E_star=hbar c/fm), preview 6.1664681e7 MeV',
         skeptic_example='g^2=10^5, a=1/10 fm: Delta>=31250 fm^-1, 493317451/80 MeV',
         along_rehearsal_toy='Delta_n/E_star >= 312500/n for n=1,2,3; none certified from n=4',
         cap_example_over_E_star=q(cap_lo_p), reading='different declared examples; both are g^2/(32a) exactly')
    # decimals printed in the report are truncations of the exact values
    rep = (FWD / 'report.md').read_text(encoding='utf-8')
    g2_lo, g2_hi = 40000 * s6_lo, 40000 * s6_hi
    dec_pairs = [('9.79795897113e4', g2_lo, g2_hi), ('3.06186217847e3', fl_p, fl_hi), ('32.5976318343', CAP_G4 / 131 ** 4, None),
                 ('31.6209933039', CAP_G4 / 132 ** 4, None), ('1.23456790123e10', F(10 ** 12, 81), None),
                 ('32.1368154215', F(10 ** 12) / 420 ** 4, None), ('31.8325636884', F(10 ** 12) / 421 ** 4, None),
                 ('3.03595776', 96 * F(132) ** 4 / CAP_G4, None), ('3.01577971977', 96 * F(421) ** 4 / 10 ** 12, None),
                 ('6.1664681e7', 312500 * hbarc, None), ('3.06186217847e4', cap_lo_p, 10 * fl_hi), ('2.4576e-8', F(6, 244140625), None)]
    need(all(txt in rep and trunc_ok(txt, lo, hi) for txt, lo, hi in dec_pairs), 'report_decimals_truncations', pairs=len(dec_pairs),
         rule='each report preview is the truncation toward zero of the exact (or directed-bracketed) value')
    # common rescaling and the AL1 path
    al1p = anyg['al1_frozen_path']
    need(al1p['law'] == 'a_n=a_0/n, g_n^2=1/n' and al1p['tau_n'] == '96n^2' and al1p['bridge_fails_for_every_n_checked'] is True
         and all(96 * n * n > 3 for n in range(1, 1001)) and res['retained_failures']['al1_frozen_path_fails_bridge_every_n'] == 'g_n^4=1/n^2<32',
         'al1_path_and_bridge_retained', note='tau_n=96n^2>3 (bridge tau<=3) for every n>=1')
    mod4 = (ROOT / MOD4_REL).read_text(encoding='utf-8')
    p1 = res['premise_arithmetic_notes'][0]
    need('`g_3^4=10^12/81=12345679012+34/81' in mod4 and divmod(10 ** 12, 81) == (12345679012, 28) and 81 * 12345679012 == 999999999972
         and p1['id'] == 'P1' and p1['claimed_correct'] is False and p1['exact'] == 'g_3^4=10^12/81=12345679012+28/81'
         and F(10 ** 12, 81) >= CAP_G4, 'panel_arithmetic_slip_P1',
         finding='modern update-4 section 3 writes 12345679012+34/81; the remainder is 28/81; no index is affected (g_3^4 >= the cap either way)',
         missed_by_skeptic_pre_comparison=True)

    # ---------------- gate fields, flags, estimate, requirements, lead
    gf = res['gate_fields']
    need(all(gf[k] is False and res[k] is False for k in GATE_FALSE) and gf['uniform_in_N_claimed'] is True and res['uniform_in_N_claimed'] is True
         and gf['uniform_in_N_scope'] == SCOPE == res['uniform_in_N_scope'] and all(res[k] is False for k in FLAGS_FALSE)
         and sorted(gf) == sorted(GATE_FALSE + ('uniform_in_N_claimed', 'uniform_in_N_scope'))
         and res['model']['selected_coefficient_alpha_units'] == 'tau/24' and res['model']['model_id'] == 'AQ_uniform_routeB along (a_n,g_n)'
         and res['label'] == 'uniform Kogut–Susskind SU(2) at fixed spacing, strong bare coupling', 'gate_fields_and_flags',
         gate_fields=gf, flags_false=list(FLAGS_FALSE), selected_coefficient='tau/24 (uniform model; the preregistered zero triple is D6)')
    need(validate_producer(res, truth), 'own_validator_accepts_frozen_packet')

    # ---------------- report: template, exclusion analysis, phrases, senses, scope, disclosure, fraction
    tmpl_n = rep.count(template)
    prod_body = strip_code(rep.replace(template, ' '))
    only_template = rep.replace(template, ' ', 1)
    raw_counts = {ph: rep.lower().count(ph) for ph in ('the continuum limit exists', 'fraction of the problem')}
    after_template = {ph: only_template.lower().count(ph) for ph in raw_counts}
    after_producer = {ph: prod_body.lower().count(ph) for ph in raw_counts}
    excl_line = [ln for ln in rep.splitlines() if ln.startswith('- **Contract, verbatim:**')]
    codespans = re.findall(r'`[^`\n]*`', rep)
    need(tmpl_n == 1 and res['mandatory_sentence'] == template and raw_counts == {'the continuum limit exists': 2, 'fraction of the problem': 1}
         and after_template == {'the continuum limit exists': 1, 'fraction of the problem': 1}
         and after_producer == {'the continuum limit exists': 0, 'fraction of the problem': 0}
         and len(excl_line) == 1 and '`the continuum limit exists (phrase)`' in excl_line[0] and '`fraction of the problem (phrase)`' in excl_line[0]
         and sum(1 for cs in codespans if 'the continuum limit exists' in cs.lower() or 'fraction of the problem' in cs.lower()) == 2,
         'mandatory_sentence_and_exclusion_analysis', template_occurrences=1, raw_counts=raw_counts, after_removing_the_template_once=after_template,
         after_producer_exclusion=after_producer,
         finding='the producer scan removes the template (its single occurrence) AND every inline code span and fenced block '
                 '(strip_code), which is broader than D1 states; in this report the only forbidden-phrase text inside code spans is '
                 'the verbatim contract claim-exclusion list of section 5.3, so the extra exclusion hides no assertion')
    scan = report_scan(rep, template, pm)
    unscoped_lines = [u['line'] for u in scan['unscoped_along_a_n']]
    need(sorted({(o['phrase'], o['context']) for o in scan['forbidden_outside_template']}) ==
         [('fraction of the problem', 'negated sentence'), ('fraction of the problem', 'verbatim claim-exclusion list (code span)'),
          ('the continuum limit exists', 'verbatim claim-exclusion list (code span)')]
         and 'No number in this report is a fraction of the continuum problem.' in rep
         and 'investigation 9 of 10 of Round32; that is an index of executed investigations, not a measure of progress' in rep
         and not re.search(r'\d+ ?%|\bpercent of\b|\d+ ?/ ?\d+ of the (\w+ )?problem', strip_code(rep).lower()),
         'forbidden_phrases_and_fractions_scan', occurrences_outside_template=scan['forbidden_outside_template'],
         rule='this review keeps code spans and removes the template once; every remaining forbidden-claim match (continuum-limit phrase; '
              'fraction of the [continuum] problem, percentages, n/m of the problem) must be negated or inside the verbatim exclusion list')
    need(unscoped_lines == [81, 87, 185, 218] and scan['code_span_a_sense_lines'] == [174, 211]
         and 'every trajectory with `g_n->0` leaves the admitted regime at a finite index' in rep
         and 'A finite physical gap along `a_n->0` requires `a_n*Delta_n->0`, which is impossible inside the admitted regime.' in rep
         and 'This is failure of a sufficient certificate, not absence of a gap' in rep and 'Along the named trajectory (a_n,g_n)' in template,
         'two_senses_of_uniform_and_scope', shared_sentences=0, a_sense_asserted=0,
         code_span_a_sense_lines={'174': 'verbatim claim-exclusion list', '211': 'quoted rejected mutations'},
         unscoped_along_a_n=scan['unscoped_along_a_n'],
         finding='no sentence shares the two senses without "volume-uniform"; the a-sense is never asserted; four negated '
                 '"uniform along a_n->0" sentences carry no g_n->0 scope in the sentence itself (line 87 is scoped by the preceding '
                 'sentence; lines 81 and 218 say the other AX1 constants are not uniform along a_n->0, which at fixed g is false for '
                 'D\'_ii, a function of tau alone; line 185 is the definition of the a-sense); wording level, non-blocking')
    sec34 = rep.split('### 3.4 ', 1)[1].split('\n## 4.', 1)[0]
    notfound = ("No rigorous construction of a genuine asymptotic-freedom trajectory satisfying either bound uniformly along the "
                "trajectory was found in this or any prior sub-round's source search.")
    paras = [p for p in sec34.split('\n\n') if p.strip()]
    need(notfound in sec34 and paras[1].startswith(notfound) and paras[2].startswith('**The one recorded lead.** Faizal and Shabir (arXiv:2606.19362')
         and 'It is unaudited and not imported' in paras[2] and 'abstract depth only' in paras[2]
         and 'this producer ran no source search of its own' in paras[1], 'not_found_sentence_discloses_lead',
         placement='the disclosure opens the paragraph that follows the not-found sentence, inside section 3.4',
         reading='the skeptic contract review asked for the disclosure in the same sentence or the next one; satisfied')

    # ---------------- producer controls, defects, map
    ids = {c['id']: c for c in res['checks']}
    controls = con['controls']
    labels_ok = all(any(lbl.startswith(CONTROL_LABEL_MAP[c]) for lbl in ids[c]['rejected_mutations']) for c in controls)
    need(res['check_count'] == 42 == len(res['checks']) and all(c['passed'] is True for c in res['checks'])
         and sorted(res['contract_controls_covered']) == sorted(controls) and all(ids[c].get('rejected_mutations') for c in controls)
         and res['rejected_mutations_in_control_checks'] == 107 == sum(len(ids[c]['rejected_mutations']) for c in controls)
         and res['rejected_mutation_total'] == 121 and res['controls_with_damaging_mutations'] == 21 and labels_ok, 'producer_controls_21_damaging',
         checks=42, control_rejections=107, total_rejections=121,
         note='every contract control carries damaging mutations; the source-edit runs below show each one is live')
    defects = res['contract_wording_defects']
    pre_c = con['preregistration']
    need([d['id'] for d in defects] == ['D%d' % k for k in range(1, 10)]
         and 'the continuum limit exists' in template and 'supplies exactly one uniform estimate' in template
         and 'the AM2 contraction needs tau<=10^-8' in con['parameters']['failed'] and 'failure of common rescaling' in con['required'][3]
         and not any('al2' in p for p in con['shared_premises']) and 'the AL1 bridge condition g^4>=32 also fails' in con['parameters']['failed']
         and pre_c['selected_triple_alpha_units'] == ['0', '0', '0'] and 'a_n' not in con['parameters']['toy_trajectory']
         and pre_c['tau']['signs_evaluated'] == ['+', '-'] and 'finite_volume uniform bound' in pre_c['state_provenance'],
         'producer_contract_defects_verified', defects=[d['id'] for d in defects],
         reconciliation={'D1': 'skeptic readings 3 and 4', 'D2': 'skeptic reading 6', 'D3': 'skeptic reading 7', 'D4': 'skeptic reading 13',
                         'D5': 'skeptic reading 7 (eventual violation), bridge form new', 'D6': 'skeptic reading 1 (different reading, same model)',
                         'D7': 'skeptic reading 11', 'D8': 'skeptic reading 14', 'D9': 'new (skeptic did not flag state_provenance)'})

    # ---------------- source-edit mutations
    rc, outs, _, _ = mutated_run()
    need(rc == 0 and outs.get('results.json') == (FWD / 'output/results.json').read_bytes()
         and outs.get('source-manifest.json') == (FWD / 'output/source-manifest.json').read_bytes(), 'unmutated_copy_reproduces')
    aborted = []
    for name, kw, reason in MUST_ABORT:
        rc, outs, last, _ = mutated_run(**kw)
        if rc == 0 or reason not in last:
            raise ReviewFailure('must-abort edit %s: rc=%s last=%s' % (name, rc, last))
        aborted.append({'edit': name, 'aborted_with': reason})
    n_ctl = sum(1 for a in aborted if a['edit'].startswith('ctl_'))
    need(len(aborted) == len(MUST_ABORT) == 41 and n_ctl == 21 and sorted(a['edit'][4:] for a in aborted if a['edit'].startswith('ctl_')) == sorted(controls),
         'must_abort_source_edits', total=len(aborted), control_weakenings=n_ctl, rows=aborted)
    silent = []
    frozen_res = json.loads((FWD / 'output/results.json').read_text())
    for name, kw, catcher, account in SILENT:
        rc, outs, last, rep_m = mutated_run(**kw)
        if rc != 0:
            raise ReviewFailure('silent edit aborted unexpectedly: ' + name)
        mres = json.loads(outs['results.json'])
        strip = lambda d: {k: v for k, v in d.items() if k not in ('check_py_sha256_recorded_before_evaluation',)}
        same = strip(mres) == strip(frozen_res)
        caught = False
        if catcher == 'report_scan':
            try:
                report_scan(rep_m, template, pm)
            except Rejected:
                caught = True
        elif catcher == 'unscoped':
            caught = len(report_scan(rep_m, template, pm)['unscoped_along_a_n']) == len(unscoped_lines) + 1
        elif catcher == 'validator':
            try:
                validate_producer(mres, truth)
            except Rejected:
                caught = True
        silent.append({'edit': name, 'producer_output_identical': same, 'caught_by_this_review': caught, 'account': account})
    need(len(silent) == 4 and all(s_['caught_by_this_review'] for s_ in silent) and all(s_['producer_output_identical'] for s_ in silent[:3])
         and silent[3]['producer_output_identical'] is False, 'silent_edits_accounted', rows=silent,
         note='report edits leave results.json unchanged (the source manifest binds report.md); the AX1 gate edit changes the recorded gate hash')

    # ---------------- own validator on damaged packets
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
    c1 = 'cap_declared_g0^4=9600000000'
    c2 = 'panel_rehearsal_g0=1000'
    dmg('identity_dropped', lambda p: p['headline'].__setitem__('identities_verified', p['headline']['identities_verified'][:10]))
    dmg('identity_altered', lambda p: p['headline']['identities_verified'].__setitem__(1, 'tau=96/g^2'))
    dmg('cap_decade', lambda p: p['headline'].__setitem__('g4_at_cap', '960000000'))
    dmg('bridge_131', lambda p: p['headline']['crossovers'][c1].__setitem__('n*_bridge', 131))
    dmg('cap_index_1', lambda p: p['headline']['crossovers'][c1].__setitem__('n*_cap', 1))
    dmg('rehearsal_bridge_420', lambda p: p['headline']['crossovers'][c2].__setitem__('n*_bridge', 420))
    dmg('floor_above_1250_sqrt6', lambda p: p['headline'].__setitem__('lattice_units_floor_lower', q(fl_hi + F(1, 10 ** 20))))
    dmg('gap_example_doubled', lambda p: p['headline']['gap_example'].__setitem__('gap_fm_inverse', '625000'))
    dmg('uniform_in_a_claimed', lambda p: p['gate_fields'].__setitem__('uniform_in_a_claimed', True))
    dmg('scope_string_changed', lambda p: p['gate_fields'].__setitem__('uniform_in_N_scope', 'volume-uniform, strong bare coupling'))
    dmg('continuum_claim', lambda p: p.__setitem__('continuum_claim', True))
    dmg('second_estimate', lambda p: p['estimates'].append(dict(p['estimates'][0], id='E2')))
    dmg('requirement_supplied', lambda p: p['requirements'][0].__setitem__('status', 'supplied'))
    dmg('lead_imported', lambda p: p['leads_recorded'][0].__setitem__('imported', True))
    dmg('trajectory_derived', lambda p: p['trajectory'].__setitem__('derived', True))
    dmg('sentence_edited', lambda p: p.__setitem__('mandatory_sentence', p['mandatory_sentence'].replace('fails to supply', 'supplies')))
    dmg('ax1_gate_hash', lambda p: p.__setitem__('ax1_gate_sha256', '0' * 64))
    dmg('verdict_limited', lambda p: p.__setitem__('proposed_forward_verdict', 'limited (tampered)'))
    need(len(damaged) == 18, 'own_validator_rejects_damaged_packets', rows=damaged)

    return {
        'loop': 'AZ1', 'stage': 'post_comparison', 'human_author': 'Hruday N M (BUNZEEY)',
        'reviewer': 'model-agent skeptic with correlated ancestry; not human peer review or formal verification',
        'checker_sha256': sha(Path(__file__)), 'contract_sha256': CONTRACT_SHA, 'ax1_gate_sha256': AX1_GATE_SHA, 'al1_gate_sha256': AL1_GATE_SHA,
        'producer_frozen': FROZEN, 'pre_comparison_freeze_sha256': PRE_FREEZE_SHA,
        'bound_values': {
            'identities': IDENTITIES, 'tau_cap': q(TAU), 'g4_at_cap': q(CAP_G4), 'bridge_g4': q(BRIDGE_G4),
            'n_star': {'declared_g0_4_9600000000': {'cap': 2, 'bridge': 132}, 'rehearsal_g0_1000': {'cap': 4, 'bridge': 421}},
            'g4_neighbours': {'declared_bridge': [q(CAP_G4 / 131 ** 4), q(CAP_G4 / 132 ** 4)],
                              'rehearsal_cap': [q(F(10 ** 12, 81)), q(F(10 ** 12, 256))],
                              'rehearsal_bridge': [q(F(10 ** 12) / 420 ** 4), q(F(10 ** 12) / 421 ** 4)]},
            'lattice_units_floor_lower_producer': q(fl_p), 'lattice_units_floor_bracket_skeptic': [q(fl_lo), q(fl_hi)],
            'gap_example_producer': 'g^2=10^6, a=1/10 fm: 312500 fm^-1', 'uniform_in_N_scope': SCOPE},
        'counts': {'review_checks': len(CHECKS), 'must_abort_edits': 41, 'control_weakenings': 21, 'silent_edits': 4, 'damaged_packets': 18,
                   'source_mutation_runs': 1 + 41 + 4, 'producer_checks': 42, 'producer_control_rejections': 107, 'producer_total_rejections': 121},
        'checks': CHECKS,
        'previews': {'lattice_floor': preview(fl_p), 'g2_at_cap': preview(g2_lo), 'gap_example_MeV': preview(312500 * hbarc),
                     'g4_declared_n131_n132': [preview(CAP_G4 / 131 ** 4), preview(CAP_G4 / 132 ** 4)],
                     'g4_rehearsal_n420_n421': [preview(F(10 ** 12) / 420 ** 4), preview(F(10 ** 12) / 421 ** 4)],
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
    try:
        out.resolve().relative_to(ROOT)
        raise SystemExit('--output must lie outside the checkout')
    except ValueError:
        pass
    result = run()
    out.mkdir(parents=True, exist_ok=True)
    (out / 'results.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'checks': len(result['checks']), 'must_abort': 41, 'control_weakenings': 21, 'silent': 4, 'damaged_packets': 18,
                      'n_star': result['bound_values']['n_star']}))


if __name__ == '__main__':
    main()
