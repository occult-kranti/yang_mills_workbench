#!/usr/bin/env python3
"""Round32 AZ2 skeptic post-comparison review checker (single+skeptic loop).

Written after the AZ2 forward producer froze (dc817d8) and after the skeptic pre-comparison package was
committed (4bae265). Standard library only (ast, concurrent.futures, fractions, hashlib, json, re, shutil,
subprocess, tempfile). Exact Fraction arithmetic decides every Boolean; decimals are labelled previews.
Model-agent skeptic with correlated ancestry; not human peer review, not formal verification.

What it does:
  * binds the frozen producer closure (freeze.json, every listed source, the 28 declared snapshots against the
    repository), the skeptic pre-comparison package (unchanged since its freeze), and the contract;
  * resolves the model question: the producer computed H_FG = K - tau_FG (W_1 + W_2) (both faces coupled
    equally); the pre-comparison derivation took the second face uncoupled. The contract text fixes neither;
    the producer disclosed its model. The checker identifies the computed model from the exact coefficients
    (-187/33696 and E_2=-1/6 belong to the two-face model; -5/864 and -1/12 to the one-face model);
  * recomputes the two-face Rayleigh-Schroedinger coefficients (untruncated, Round11 monomials) and certifies
    independent full-graph enclosures of <W_1> in the two-face model from a degree-12 RS vector with the exact
    complete residual and the Weyl separation 3-2|tau_FG| (Davis-Kahan); every producer enclosure must intersect
    it; the one-face pre-comparison enclosures are certified disjoint (the two-body shift tau^3/4212 + ...);
  * checks the leading-order omitted residual and its channel split independently (exact Gram projections of
    (x+y) psi_D onto the first omitted shell, sectors verified orthogonal) against the producer ledger;
  * checks thresholds, ledger parts (a)-(e), gate fields, the mandatory sentence, a whole-word forbidden-phrase
    scan, the Arb preview, check.py's imports (AST), and the producer's wording defects D1-D8;
  * validates the producer's exported results with its own validator and rejects damaged packets;
  * runs source-edit mutations on temporary copies of the producer closure (outside the checkout, always with
    python -B): an unmutated copy must reproduce output/ byte for byte; each of the 20 contract controls is
    weakened (its validator made to return True) and the copy must abort at that control; six semantic edits
    are recorded.

Usage: python3 -B research/round32/skeptic/az2_postreview_check.py --output /absolute/fresh/dir
"""
import argparse
import ast
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction as F
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[3]
R32 = 'research/round32'
FWD_REL = R32 + '/forward/az2'
FWD = ROOT / FWD_REL
CONTRACT_REL = R32 + '/contracts/az2.json'
CONTRACT_SHA256 = '2861d5c59841b5b8e688712aab4faf3edf9f9f8ee2079d8ebbda07fabb7461c3'
PRODUCER = {
    'freeze.json': '5f08f196de03c827e091e7b5cbbf92e606c999f77ecd6283929f742893fd25c3',
    'check.py': '4ad3a9f8127ed983a3af9343a4697b77a35bec26f4cd75f1683e32307cab1c7d',
    'report.md': '7521fd9486e081da00302e1ee6778f5f82920c72c80a39ca86c36876d366ac96',
    'output/results.json': '96d7b88d8e92f3f4b2f8c25f394d45f323dbcf459b88c46cc83a4df3d2b1ca64',
    'output/source-manifest.json': '56e2453591b0cb6a685033af5a476143f02bff7be061f625911f64efd99e4a4c',
    'arb_preview.py': 'd218ffc58c0072a472a67b6284dd7d70d9beddbac72654e3f5d3da962872edc2',
    'preview/arb_preview.json': 'a5dcbbc4e18181fe14104e1562ac9412bb46155299b07ad3827016dd70d2dd32',
}
PRE_CHECK_REL = R32 + '/skeptic/az2_check.py'
PRE_CHECK_SHA256 = '6369a169c2ff76dfd738535940fc9aefc1abbb5d28952a289459fc939a729f21'
PRE_FREEZE_REL = R32 + '/skeptic/az2-independent-freeze.json'
PRE_FREEZE_SHA256 = '33f6077ad2902a3a0c726a2676415e91895ce59a2bf0ba561778a55ac4117251'
PRE_RESULTS_REL = R32 + '/skeptic/az2-independent/results.json'
PRE_RESULTS_SHA256 = '30917f54bf41dd5c468b37c9a17fc1809f7c41ee0d0852f102941e9d9c46ea0f'
LOOP2_REL = R32 + '/experts/modern/loop2-response.md'
LOOP2_SHA256 = '2735d029791d12f03e9bcb56d729e8e91d107555e380712e19535320f7fcd73f'
GRID = (F(1, 1000), F(1, 100), F(1, 10))
RS_ORDER = 12                      # degree of the independent two-face trial vector (not a cutoff-D certificate)
OUT_DEN = 10 ** 60
ALLOWED_IMPORTS = {'argparse', 'decimal', 'hashlib', 'json', 're', 'fractions', 'functools', 'math', 'pathlib'}
TWO_FACE_HAMILTONIAN = 'H_FG = K - tau_FG (W_1 + W_2), alpha units, K = sum of the seven link Casimirs j(j+1) (Round11 rho=1)'


class ReviewFailure(RuntimeError):
    """A required post-review check failed."""


class Refused(Exception):
    """Raised by this review's validator when a packet is refused."""


CHECKS = []


def need(ok, cid, **detail):
    if ok is not True:
        raise ReviewFailure(cid)
    if any(r['id'] == cid for r in CHECKS):
        raise ReviewFailure('duplicate check id ' + cid)
    row = {'id': cid, 'passed': True}
    row.update(detail)
    CHECKS.append(row)


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha(path):
    return sha_bytes(Path(path).read_bytes())


def q(x):
    return str(x)


def preview(x, digits=13):
    return format(float(x), '.%de' % digits)


def rdown(x, den=OUT_DEN):
    return F((x.numerator * den) // x.denominator, den)


def rup(x, den=OUT_DEN):
    return F(-((-x.numerator * den) // x.denominator), den)


def load_pre_module():
    b = (ROOT / PRE_CHECK_REL).read_bytes()
    if sha_bytes(b) != PRE_CHECK_SHA256:
        raise ReviewFailure('pre-comparison checker changed')
    spec = importlib.util.spec_from_file_location('az2_pre_comparison', str(ROOT / PRE_CHECK_REL))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------- exact algebra (pre-comparison primitives, hash-pinned)
def rs_vectors(pm, V, order):
    """Untruncated Rayleigh-Schroedinger vectors psi_n (intermediate normalisation) for H = K + tau V."""
    psi, E = [pm.ONE], [F(0)]
    for n in range(1, order + 1):
        Vp = pm.pmul(V, psi[n - 1])
        E.append(pm.mean(Vp))
        rhs = pm.pscale(Vp, F(-1))
        for k in range(1, n + 1):
            rhs = pm.padd(rhs, psi[n - k], E[k])
        f, p = dict(rhs), {}
        while f:
            top = pm.deg(f)
            if top == 0:
                if any(f.values()):
                    raise ReviewFailure('RS solvability')
                break
            part = {k: v / pm.eps(*k) for k, v in f.items() if sum(k) == top}
            p = pm.padd(p, part)
            f = pm.padd(f, pm.kinetic(part), F(-1))
        m = pm.mean(p)
        p = pm.padd(p, {(0, 0, 0): -m}) if m else p
        if pm.padd(pm.kinetic(p), rhs, F(-1)) != {}:
            raise ReviewFailure('RS resolvent equation not exact')
        psi.append(p)
    return psi, E


def ip(pm, p, r):
    prod = {}
    for k1, v1 in p.items():
        for k2, v2 in r.items():
            k = (k1[0] + k2[0], k1[1] + k2[1], k1[2] + k2[2])
            prod[k] = prod.get(k, 0) + v1 * v2
    return sum((v * pm.mom(*k) for k, v in prod.items()), F(0))


def series(pm, psi, O, order):
    A = [sum((ip(pm, psi[i], pm.pmul(O, psi[n - i])) for i in range(n + 1)), F(0)) for n in range(order + 1)]
    N = [sum((ip(pm, psi[i], psi[n - i]) for i in range(n + 1)), F(0)) for n in range(order + 1)]
    out = []
    for n in range(order + 1):
        out.append((A[n] - sum((out[k] * N[n - k] for k in range(n)), F(0))) / N[0])
    return out


def two_face_enclosure(pm, psi, V, tau):
    """Certified full-graph enclosure of <W_1> for H = K + tau V, V=-(x+y), from v = sum_{n<=12} tau^n psi_n."""
    v = {}
    for n, p in enumerate(psi):
        v = pm.padd(v, pm.pscale(p, tau ** n))
    Hv = pm.padd(pm.kinetic(v), pm.pmul(V, v), tau)
    nv = ip(pm, v, v)
    rho = ip(pm, v, Hv) / nv
    r2 = ip(pm, Hv, Hv) / nv - rho * rho
    w = ip(pm, v, pm.pmul(pm.PX, v)) / nv
    b = 3 - 2 * abs(tau)                               # Weyl: E_1 >= m_1 - ||tau (x+y)|| = 3 - 2|tau|
    if not (r2 >= 0 and rho < b):
        raise ReviewFailure('separation or residual')
    s = pm.sqrt_up(r2) / (b - rho)                     # sin(theta) <= ||r||/(b-rho)
    half = 2 * s                                       # |Tr((P_psi - P_v) x)| <= 2 sin(theta) ||x||
    return {'w': w, 'rho': rho, 'r2': r2, 'half': half, 'lower': rdown(w - half), 'upper': rup(w + half)}


class GramProjector:
    """Exact projection onto P_D (Gram block-diagonal in the parity classes (a+c, b+c) mod 2), own LDL."""

    def __init__(self, pm, D):
        self.pm = pm
        self.bs = pm.basis(D)
        self.blocks = {}
        for i, m in enumerate(self.bs):
            self.blocks.setdefault(((m[0] + m[2]) % 2, (m[1] + m[2]) % 2), []).append(i)
        self.fac = {}
        for key, idx in self.blocks.items():
            M = [[pm.mom(*(a + b for a, b in zip(self.bs[i], self.bs[j]))) for j in idx] for i in idx]
            n = len(idx)
            L = [[F(0)] * n for _ in range(n)]
            d = [F(0)] * n
            for j in range(n):
                d[j] = M[j][j] - sum(L[j][k] ** 2 * d[k] for k in range(j))
                if not d[j] > 0:
                    raise ReviewFailure('Gram block not positive definite')
                L[j][j] = F(1)
                for i in range(j + 1, n):
                    L[i][j] = (M[i][j] - sum(L[i][k] * L[j][k] * d[k] for k in range(j))) / d[j]
            self.fac[key] = (L, d)

    def coeffs(self, f):
        pm = self.pm
        return [sum((v * pm.mom(m[0] + k[0], m[1] + k[1], m[2] + k[2]) for k, v in f.items()), F(0)) for m in self.bs]

    def solve(self, c):
        z = [F(0)] * len(c)
        for key, idx in self.blocks.items():
            L, d = self.fac[key]
            y = [c[i] for i in idx]
            n = len(y)
            for i in range(n):
                y[i] -= sum(L[i][j] * y[j] for j in range(i))
            y = [y[i] / d[i] for i in range(n)]
            for i in range(n - 1, -1, -1):
                y[i] -= sum(L[j][i] * y[j] for j in range(i + 1, n))
            for t, i in enumerate(idx):
                z[i] = y[t]
        return z


def leading_leak(pm, psi, V, D):
    """||Q_D V psi_D||^2 and its split over the orthogonal shell-(D+1) sectors (leading order in tau)."""
    P = GramProjector(pm, D)
    f = pm.pmul(V, psi[D])
    c = P.coeffs(f)
    z = P.solve(c)
    total = ip(pm, f, f) - sum(a * b for a, b in zip(c, z))
    secs = [(a, b, D + 1 - a - b) for a in range(D + 2) for b in range(D + 2 - a)]
    B = {s: [pm.mom(m[0] + s[0], m[1] + s[1], m[2] + s[2]) for m in P.bs] for s in secs}
    Y = {s: P.solve(B[s]) for s in secs}
    sig = {s: pm.mom(2 * s[0], 2 * s[1], 2 * s[2]) - sum(a * b for a, b in zip(B[s], Y[s])) for s in secs}
    off = sum(1 for i, s in enumerate(secs) for t in secs[i + 1:]
              if pm.mom(*(a + b for a, b in zip(s, t))) - sum(a * b for a, b in zip(B[s], Y[t])))
    w = {}
    for s in secs:
        g = sum((v * pm.mom(k[0] + s[0], k[1] + s[1], k[2] + s[2]) for k, v in f.items()), F(0)) - sum(a * b for a, b in zip(Y[s], c))
        w[s] = g * g / sig[s]
    half = F(D, 2)
    cls = {'j': F(0), 'k': F(0), 'ell': F(0), 'product': F(0)}
    for (a, b, cc), wt in w.items():
        hit = False
        for name, lab in (('j', F(a + cc, 2)), ('k', F(b + cc, 2)), ('ell', F(a + b, 2))):
            if lab > half:
                cls[name] += wt
                hit = True
        if not hit:
            cls['product'] += wt
    return {'total': total, 'sector_sum': sum(w.values(), F(0)), 'classes': cls, 'sectors': len(secs), 'offdiag_nonzero': off}


# ---------------------------------------------------------------- report scanning
def strip_code(text):
    text = re.sub(r'```.*?```', ' ', text, flags=re.S)
    return re.sub(r'`[^`\n]*`', ' ', text)


def whole_word_hits(text, phrases):
    hits = {}
    for ph in phrases:
        n = len(re.findall(r'(?<![A-Za-z])' + re.escape(ph) + r'(?![A-Za-z])', text, re.I))
        if n:
            hits[ph] = n
    return hits


# ---------------------------------------------------------------- this review's validator of the exported producer packet
def validate_producer(res, truth):
    for k, v in truth['gate_fields'].items():
        if res.get(k) is not v:
            raise Refused('gate field ' + k)
    if res['sub_labels'] != ['sign_certified_finite_graph', 'static_not_dynamic']:
        raise Refused('sub-labels')
    hd = res['headline']
    ham = hd['hamiltonian']
    model = 'two_face' if ham == TWO_FACE_HAMILTONIAN else ('one_face' if 'K - tau_FG W_1' in ham or 'K - tau_FG x' in ham else None)
    if model is None:
        raise Refused('model not named')
    coeff = truth['coefficients'][model]
    if hd['higher_order']['W_1_tau3'] != coeff['a3'] or hd['second_order_coefficients']['E_0'] != coeff['e2'] \
            or hd['higher_order']['E_0_tau4'] != coeff['e4']:
        raise Refused('model-coefficient mismatch: the coefficients belong to the other face-coupling model')
    if hd['derivative_at_zero'] != {'6': ['1/6', '1/6'], '8': ['1/6', '1/6']} or hd['derivative_tail_term'] != '0':
        raise Refused('derivative at zero')
    if hd['free_reference'] != {'6': ['0', '0'], '8': ['0', '0']}:
        raise Refused('own free reference')
    if hd['second_order_coefficients']['W_1'] != '0' or res['fg_coefficients_fitted'] is not False:
        raise Refused('second-order coefficient or fitting')
    if hd['tail_lower'] != {'6': '45', '8': '69'}:
        raise Refused('tail_lower')
    for key, (lo, hi) in hd['wilson_enclosures'].items():
        tl, th = truth['enclosures'][model][key]
        if not (F(lo) <= F(hi) and F(lo) <= th and F(hi) >= tl):
            raise Refused('enclosure disjoint from the certified enclosure: ' + key)
        t = F(res['points'][key]['tau_FG'])
        if not ((t > 0 and F(lo) > 0) or (t < 0 and F(hi) < 0)):
            raise Refused('sign not certified: ' + key)
    for key, rec in res['points'].items():
        ld = rec['ledger']
        for part in ('a_per_link_representation_tail', 'b_joint_product_channel', 'c_gauge_invariant_projection',
                     'd_ritz_eigenvector_residual', 'e_arithmetic'):
            if part not in ld:
                raise Refused('ledger part missing: ' + part)
        if sorted(ld['a_per_link_representation_tail']) != sorted(['h1', 'h2', 'h3', 'h4', 'vL', 'vM', 'vR']):
            raise Refused('per-link rows')
        c = ld['c_gauge_invariant_projection']
        if c.get('value') != '0' or 'Gauss' not in c.get('reason', ''):
            raise Refused('gauge item')
        b = ld['b_joint_product_channel']
        if b['product_channel_threshold'] != truth['product_threshold'][str(rec['D'])] or 'interference_2XY_bracket' not in b:
            raise Refused('joint product channel')
    if res['mandatory_sentence'] != truth['sentence']:
        raise Refused('mandatory sentence')
    if hd['dictionary'] != {'tau_FG': 'tau/24', 'fg_first_order': '1/6', 'matched_value': '1/144', 'z3_first_order': '1/144',
                            'relation': 'consistent_with'}:
        raise Refused('dictionary')
    return True


# ---------------------------------------------------------------- source-edit mutations on temporary copies
def ret_true(def_line):
    return (def_line, def_line + '        return True\n')


CONTROL_WEAKENINGS = [
    ('missing_incoming_stars', '    def validate_terms(faces, kin):\n', 'incoming_face_W2_coupling_omitted'),
    ('full_original_wilson_cover', '    def validate_observable(path_links, closed, basis_has_z):\n', 'three_drawn_links_open_path'),
    ('wrong_delta_alpha_hbar_clock', '    def validate_units(face_coeff_per_tau, w_energy, clock):\n', 'tau_over_18_normalized_face_with_alpha_Casimir'),
    ('vector_versus_scalar_centering', '    def validate_centering(obs_centering, sigma_kind, sigma_sq):\n', 'scalar_subtraction_as_centring_bound'),
    ('first_order_mean_charged', '    def validate_first(coef, encl):\n', 'first_order_mean_set_to_zero_by_parity'),
    ('tau_scaling_exponent', '    def validate_exponent(label, interval):\n', 'remainder_labelled_second_order'),
    ('changed_model_relabelled', '    def validate_model(mdl):\n', 'anisotropic_shared_link_rho2'),
    ('coherent_evidence_tampering', '    def validate_packet(pk, inv):\n', 'control_boolean_flipped_hash_rebound'),
    ('insufficient_verdict_retained', '    def validate_verdict(reported, *args):\n', 'tail_only_at_D6_relabelled_accepted'),
    ('exact_arithmetic_admission', None, 'float_input'),
    ('root_n_misuse', '    def validate_joint(total, parts):\n', 'rss_of_face_channels_without_interference'),
    ('no_priority_or_continuum_claim', '    def validate_packet_flags(fl):\n', 'continuum_true'),
    ('finite_graph_model_id', '    def validate_label(lb):\n', 'model_is_finite_graph_false'),
    ('complete_residual_all_channels', '    def validate_complete(total_sq, parts, direct=None):\n', 'y_channel_dropped'),
    ('certified_representation_tail', '    def validate_tail(D, tau, tail_value, kind):\n', 'last_retained_shell_m_D_as_tail'),
    ('own_free_reference', '    def validate_reference(ref_value, route):\n', 'Z3_first_order_imported_as_reference'),
    ('no_transfer_to_aq', '    def validate_aq(x):\n', 'transfers_to_aq_true'),
    ('fg_coefficients_not_fitted', '    def validate_coefficient(value, provenance):\n', 'least_squares_slope_through_grid'),
    ('sign_convention_fixture', '    def validate_sign(sign, label):\n', 'flipped_sign_gives_minus_one_sixth'),
    ('complete_residual_ledger_itemized', '    def validate_ledger(ld, verdict):\n', 'joint_product_channel_not_itemized'),
]
RAT_OLD = "        raise AdmissionError('non-exact input rejected: ' + repr(value))\n"
RAT_NEW = "        return Q(value)\n"
SEMANTIC_EDITS = [
    ('rs_series_one_face_default', dict(edits=[("def rs_series(order, D, faces=((1, 0, 0), (0, 1, 0)), sign=-1, model='R11_rho1'):",
                                                "def rs_series(order, D, faces=((1, 0, 0),), sign=-1, model='R11_rho1'):")]),
     'abort', 'failed check rs_exact_full_space'),
    ('certificate_hamiltonian_one_face', dict(edits=[('    t = padd(xv, yv)\n', '    t = dict(xv)\n')]), 'abort', None),
    ('free_gap_4', dict(edits=[('WEYL_FREE_GAP = Q(3) ', 'WEYL_FREE_GAP = Q(4) ')]), 'abort', 'failed check round11_conventions_bound'),
    ('omitted_residual_dropped', dict(edits=[('    rhoQ2 = tau * tau * PQ\n', '    rhoQ2 = 0 * PQ\n')]), 'abort', 'failed check ritz_certificates_complete'),
    ('report_phrase_predicts', dict(report_append='\nThe finite graph predicts the matched coefficient.\n'), 'abort',
     'forbidden phrasing in the report: predicts'),
    ('arb_preview_output_removed', dict(remove='preview/arb_preview.json'), 'completes', None),
]


def mutated_run(edits=(), report_append=None, remove=None):
    with tempfile.TemporaryDirectory(prefix='hnm-r32-az2-skeptic-mut-') as tmp, \
            tempfile.TemporaryDirectory(prefix='hnm-r32-az2-skeptic-out-') as otmp:
        dst = Path(tmp) / FWD_REL
        shutil.copytree(FWD, dst, ignore=shutil.ignore_patterns('output', '__pycache__'))
        src = (dst / 'check.py').read_text(encoding='utf-8')
        for old, new in edits:
            if src.count(old) != 1:
                raise ReviewFailure('edit anchor not unique: ' + old[:60])
            src = src.replace(old, new)
        (dst / 'check.py').write_text(src, encoding='utf-8')
        if report_append:
            with open(dst / 'report.md', 'a', encoding='utf-8') as fh:
                fh.write(report_append)
        if remove:
            (dst / remove).unlink()
        out = Path(otmp) / 'output'
        done = subprocess.run([sys.executable, '-B', str(dst / 'check.py'), '--output', str(out)], capture_output=True, text=True)
        if any(dst.rglob('*.pyc')):
            raise ReviewFailure('interpreter cache written into a mutated copy')
        last = (done.stderr.strip().splitlines() or [''])[-1]
        outs = {p.name: p.read_bytes() for p in out.glob('*')} if out.exists() else {}
        return done.returncode, outs, last


# ---------------------------------------------------------------- main review
def run():
    pm = load_pre_module()
    contract_bytes = (ROOT / CONTRACT_REL).read_bytes()
    need(sha_bytes(contract_bytes) == CONTRACT_SHA256, 'contract_sha256_bound')
    contract = json.loads(contract_bytes)
    pre = contract['preregistration']

    # ---------------- producer closure
    for rel, digest in PRODUCER.items():
        if sha(FWD / rel) != digest:
            raise ReviewFailure('producer file changed: ' + rel)
    freeze = json.loads((FWD / 'freeze.json').read_text())
    listed = {k[len(FWD_REL) + 1:]: v for k, v in freeze['sources'].items()}
    actual = {p.relative_to(FWD).as_posix() for p in FWD.rglob('*') if p.is_file() and p.name != 'freeze.json'}
    need(freeze['loop'] == 'AZ2' and freeze['direction'] == 'forward' and freeze['contract_sha256'] == CONTRACT_SHA256
         and set(listed) == actual and all(sha(FWD / n) == d for n, d in listed.items())
         and not any(n.endswith('.pyc') or '__pycache__' in n for n in actual)
         and {'arb_preview.py', 'preview/arb_preview.json'} <= set(listed),
         'producer_freeze_closure_verified', closure_files=len(listed), freeze_sha256=PRODUCER['freeze.json'],
         note='every listed file hashed; closure equals the directory; arb_preview.py and preview/arb_preview.json are inside it')
    declared = sorted(['AGENTS.md', CONTRACT_REL] + contract['shared_premises'])
    inputs = sorted(p.relative_to(FWD / 'inputs').as_posix() for p in (FWD / 'inputs').rglob('*') if p.is_file())
    need(inputs == declared and len(inputs) == 28
         and all((FWD / 'inputs' / r).read_bytes() == (ROOT / r).read_bytes() for r in declared)
         and not any(r.startswith(R32 + '/skeptic/') or r.startswith(R32 + '/forward/az1') for r in inputs),
         'premise_inventory_28_identical', note='AGENTS.md + contract + 26 shared premises; no skeptic/az2 or AZ1 file')

    # ---------------- pre-comparison package unchanged
    pf = json.loads((ROOT / PRE_FREEZE_REL).read_text())
    need(sha(ROOT / PRE_FREEZE_REL) == PRE_FREEZE_SHA256 and pf['contract_sha256'] == CONTRACT_SHA256 and pf['stage'] == 'pre_comparison'
         and all(sha(ROOT / f) == d for f, d in pf['files'].items()) and pf['files'][PRE_RESULTS_REL] == PRE_RESULTS_SHA256
         and pf['files'][PRE_CHECK_REL] == PRE_CHECK_SHA256, 'pre_comparison_package_unchanged',
         note='committed in 4bae265 before the producer commit dc817d8; four files byte-identical to their freeze')
    pre_res = json.loads((ROOT / PRE_RESULTS_REL).read_text())

    # ---------------- check.py imports (AST) and preview handling
    tree = ast.parse((FWD / 'check.py').read_text(encoding='utf-8'))
    mods = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods |= {a.name.split('.')[0] for a in node.names}
        elif isinstance(node, ast.ImportFrom):
            mods.add((node.module or '').split('.')[0])
    src = (FWD / 'check.py').read_text(encoding='utf-8')
    need(mods <= ALLOWED_IMPORTS and 'importlib' not in src and '__import__' not in src and 'exec(' not in src
         and "(BASE / 'arb_preview.py').read_text" in src and "json.loads((BASE / 'preview' / 'arb_preview.json').read_text" in src,
         'check_py_never_imports_preview_or_solver', imports=sorted(mods),
         note='arb_preview.py is read only for its PREVIEW ONLY label; preview/arb_preview.json is parsed only for a comparison')

    res = json.loads((FWD / 'output/results.json').read_text())
    gate = pre['gate_fields_required']
    need(all(res[k] is v for k, v in gate.items()) and res['continuum_claim'] is False and res['scientific_priority_verified'] is False
         and res['weak_coupling_claim'] is False and res['roadmap_goal_2_resolved'] is False and res['resolved_interaction_shift'] is False
         and res['sub_labels'] == ['sign_certified_finite_graph', 'static_not_dynamic'] and res['check_count'] == 35
         and res['rejected_mutation_total'] == 90 and res['rejected_mutations_in_control_checks'] == 80
         and sorted(res['contract_controls_covered']) == sorted(contract['controls']), 'producer_gate_fields_and_counts',
         gate_fields=gate, producer_checks=35, producer_rejected_mutations=90)

    hd = res['headline']
    # ---------------- first order, free reference, dictionary
    need(hd['derivative_at_zero'] == {'6': ['1/6', '1/6'], '8': ['1/6', '1/6']} and hd['derivative_tail_term'] == '0'
         and pre_res['first_order']['derivative_at_zero'] == '1/6' and pre_res['first_order']['D6'] == '1/6' == pre_res['first_order']['D8'],
         'derivative_matches_prediction', producer=hd['derivative_at_zero'], predicted='1/6 exactly at D=6 and D=8')
    need(hd['free_reference'] == {'6': ['0', '0'], '8': ['0', '0']}, 'free_reference_exactly_zero')
    need(F(hd['dictionary']['fg_first_order']) / 24 == F(1, 144) == F(hd['dictionary']['matched_value'])
         and hd['dictionary']['relation'] == 'consistent_with', 'dictionary_consistency_only')

    # ---------------- model resolution
    X = {(1, 0, 0): F(1)}
    V2 = {(1, 0, 0): F(-1), (0, 1, 0): F(-1)}
    V1 = {(1, 0, 0): F(-1)}
    psi2, E2 = rs_vectors(pm, V2, RS_ORDER)
    psi1, E1 = rs_vectors(pm, V1, 6)
    W2s = series(pm, psi2[:6], X, 5)
    W1s = series(pm, psi1[:6], X, 5)
    x2s = series(pm, psi2[:5], {(2, 0, 0): F(1)}, 4)
    xys = series(pm, psi2[:5], {(1, 1, 0): F(1)}, 4)
    zs = series(pm, psi2[:5], {(0, 0, 1): F(1)}, 4)
    rc = res['rs_coefficients']
    need(W2s == [F(x) for x in rc['W_1']] and E2[:6] == [F(x) for x in rc['E_0']] and x2s == [F(x) for x in rc['W_1_squared']]
         and xys == [F(x) for x in rc['W_1_W_2']] and zs == [F(x) for x in rc['outer_loop_z']]
         and W2s[:6] == [0, F(1, 6), 0, F(-187, 33696), 0, F(767713, 2523156480)] and E2[2] == F(-1, 6) and E2[4] == F(187, 67392),
         'two_face_rs_coefficients_recomputed', W_1=[q(x) for x in W2s], E_0=[q(x) for x in E2[:6]],
         second_order={'W_1': '0', 'E_0': '-1/6', 'W_1_squared': q(x2s[2]), 'W_1_W_2': q(xys[2]), 'outer_loop_z': q(zs[2])})
    loop2 = (ROOT / LOOP2_REL).read_text()
    nd = contract['parameters']['normalization_dictionary']
    need(W1s[:4] == [0, F(1, 6), 0, F(-5, 864)] and E1[2] == F(-1, 12)
         and hd['higher_order']['W_1_tau3'] == '-187/33696' and hd['second_order_coefficients']['E_0'] == '-1/6'
         and hd['hamiltonian'] == TWO_FACE_HAMILTONIAN and res['model']['round11_equivalence'] == 'H_FG = H_R11(alpha=1, lambda1=lambda2=tau_FG, rho=1) - 2 tau_FG'
         and pre_res['coefficients']['both_faces_variant_third_order_W'].startswith('-187/33696')
         and pre_res['coefficients']['third_order_W'] == '-5/864' and pre_res['coefficients']['second_order_E'] == '-1/12'
         and "the two-plaquette graph's own coupling multiplies one face" in nd and contract['model'].count('coupling tau_FG') == 1
         and 'lambda2' not in json.dumps(contract) and sha(ROOT / LOOP2_REL) == LOOP2_SHA256
         and '`H/alpha=K+kappa_1(1-x)+kappa_2(1-y)`' in loop2,
         'model_resolution_two_face_computed_and_disclosed',
         producer_model=TWO_FACE_HAMILTONIAN, skeptic_pre_comparison_model='H_FG = K - tau_FG W_1 (second face uncoupled)',
         identification='producer a3=-187/33696 and E_2=-1/6 equal the two-face values; the one-face values are -5/864 and -1/12',
         contract_text='the model string names one coupling tau_FG without saying which faces carry it; the only face wording is the '
                       'dictionary parenthetical "the two-plaquette graph\'s own coupling multiplies one face"; the shared premise '
                       'loop2-response.md specifies H/alpha=K+kappa_1(1-x)+kappa_2(1-y) with two couplings',
         reading='not fixed by the contract: both readings are admissible; the producer disclosed its model in the verdict, section 1 and '
                 'results.model; non-blocking wording defect; the gate must name the two-face model exactly')
    delta3 = F(-187, 33696) - F(-5, 864)
    need(delta3 == F(1, 4212) and W2s[2] == 0 == W1s[2] and W2s[1] == W1s[1] == F(1, 6), 'two_body_shift_coefficient_exact',
         delta_tau3='1/4212', note='<W_1>_{two-face} - <W_1>_{one-face} = tau^3/4212 + O(tau^5); first and second order agree')

    # ---------------- independent certified two-face enclosures (degree-12 RS vector, Davis-Kahan)
    parity_ok = all((k[0] + k[1] - n) % 2 == 0 for n, p in enumerate(psi2) for k in p)
    mine = {}
    for t in GRID:
        mine[t] = two_face_enclosure(pm, psi2, V2, t)
    need(parity_ok and all(mine[t]['lower'] > 0 for t in GRID), 'independent_two_face_enclosures_certified',
         rs_vector_degree=RS_ORDER, separation='3-2|tau_FG| (Weyl, free gap 3)', mirror='psi_n has vM-flip parity (-1)^n exactly, '
         'so the -tau_FG enclosure is the exact negation', half_width_preview={q(t): preview(mine[t]['half'], 4) for t in GRID})
    enc = hd['wilson_enclosures']
    truth_two = {}
    for t in GRID:
        for sgn, name in ((1, '+'), (-1, '-')):
            lo, hi = (mine[t]['lower'], mine[t]['upper']) if sgn > 0 else (-mine[t]['upper'], -mine[t]['lower'])
            for D in (6, 8):
                truth_two['D%d_tau%s%s' % (D, name, q(t))] = (lo, hi)
    inter = {k: F(v[0]) <= truth_two[k][1] and F(v[1]) >= truth_two[k][0] for k, v in enc.items()}
    contain = {k: F(v[0]) <= truth_two[k][0] and truth_two[k][1] <= F(v[1]) for k, v in enc.items()}
    need(len(enc) == 12 and all(inter.values()) and all(contain.values()), 'producer_enclosures_intersect_independent',
         intersect=12, contain_skeptic_interval=sum(contain.values()),
         note='the skeptic interval is narrower than every producer interval and lies inside each')
    nest = all(F(enc['D6' + k[2:]][0]) <= F(enc[k][0]) and F(enc[k][1]) <= F(enc['D6' + k[2:]][1]) for k in enc if k.startswith('D8'))
    need(nest, 'producer_D8_inside_D6')

    # the one-face pre-comparison enclosures are certified disjoint: the two-body shift
    one = {}
    for D in (6, 8):
        for key, row in pre_res['points'].items():
            if key.startswith('D%d_' % D):
                tt = key.split('tau_')[1]
                name = ('-' + tt[1:]) if tt.startswith('-') else ('+' + tt)
                one['D%d_tau%s' % (D, name)] = (F(row['enclosure_lower_1e-60']), F(row['enclosure_upper_1e-60']))
    shift = {}
    disjoint = True
    for k, (lo2, hi2) in truth_two.items():
        lo1, hi1 = one[k]
        dlo, dhi = lo2 - hi1, hi2 - lo1
        shift[k] = (dlo, dhi)
        pl, ph = F(enc[k][0]), F(enc[k][1])
        disjoint = disjoint and (ph < lo1 or pl > hi1)
    pos = all((shift[k][0] > 0) if '+' in k else (shift[k][1] < 0) for k in shift)
    t10 = shift['D8_tau+1/10']
    need(disjoint and pos and F(2369, 10 ** 10) < t10[0] < t10[1] < F(2371, 10 ** 10), 'one_face_enclosures_disjoint_two_body_shift_certified',
         shift_preview={k: preview((v[0] + v[1]) / 2, 10) for k, v in sorted(shift.items()) if k.startswith('D8')},
         note='the producer (two-face) and pre-comparison (one-face) enclosures do not intersect at any of the 12 points; '
              'the difference is the certified second-square shift, sign(tau_FG) tau^3/4212 + O(tau^5)')

    # ---------------- widths: which is tighter and why
    def half(v):
        return (F(v[1]) - F(v[0])) / 2
    prod_half = {k: half(v) for k, v in enc.items()}
    pre_half = {k: (one[k][1] - one[k][0]) / 2 for k in one}
    mine_half = {k: (v[1] - v[0]) / 2 for k, v in truth_two.items()}
    ratio_dk = {}
    for k, rec in res['points'].items():
        if F(rec['tau_FG']) != 0:
            d = rec['ledger']['d_ritz_eigenvector_residual']
            ratio_dk[k] = F(d['sin_theta_davis_kahan_complete_residual_upper']) / F(d['sin_theta_eckart_tail_comparison_upper'])
    need(all(pre_half[k] < prod_half[k] for k in enc) and all(mine_half[k] < prod_half[k] for k in enc)
         and all(F(37, 10) <= r <= F(49, 10) for r in ratio_dk.values()), 'width_comparison_recorded',
         producer_half={k: preview(v, 3) for k, v in sorted(prod_half.items()) if '+' in k},
         pre_comparison_one_face_half={k: preview(v, 3) for k, v in sorted(pre_half.items()) if '+' in k},
         skeptic_two_face_degree12_half={k: preview(v, 3) for k, v in sorted(mine_half.items()) if '+' in k and k.startswith('D8')},
         producer_davis_kahan_over_eckart={k: preview(v, 3) for k, v in sorted(ratio_dk.items()) if '+' in k},
         reading='the one-face pre-comparison widths are narrower because that model leaks one spin-network component; the two-face '
                 'leak spreads over the shell (vM channel x^a y^b) and is about 115 times larger at D=6; in the same model the producer\'s '
                 'Eckart/tail-comparison angle is 3.7-4.9 times sharper than Davis-Kahan; the degree-12 skeptic vector is not a cutoff-D '
                 'certificate; all intervals are valid')

    # ---------------- leading-order omitted residual and its channel split
    leak = {}
    for D in (6, 8):
        leak[D] = leading_leak(pm, psi2, V2, D)
    ok_leak = True
    rows = {}
    for D in (6, 8):
        L = leak[D]
        p3 = res['points']['D%d_tau+1/1000' % D]['ledger']['b_joint_product_channel']
        p2 = res['points']['D%d_tau+1/100' % D]['ledger']['b_joint_product_channel']
        scale = F(1, 1000) ** (2 * D + 2)
        tot3 = F(p3['complete_omitted_residual_squared_upper'])
        ell3 = F(p3['per_link_class_weights_upper']['ell'])
        j3 = F(p3['per_link_class_weights_upper']['j'])
        prod3, prod2 = F(p3['product_channel_weight_upper']), F(p2['product_channel_weight_upper'])
        rel = abs(tot3 / (L['total'] * scale) - 1)
        relj = abs(j3 / (L['classes']['j'] * scale) - 1)
        rell = abs(ell3 / (L['classes']['ell'] * scale) - 1)
        ok_leak = ok_leak and L['offdiag_nonzero'] == 0 and L['sector_sum'] == L['total'] and L['classes']['product'] == 0 \
            and L['classes']['j'] == L['classes']['k'] and rel < F(1, 10 ** 4) and relj < F(1, 10 ** 4) and rell < F(1, 10 ** 4) \
            and F(99, 100) * 10 ** (2 * D + 4) < prod2 / prod3 < F(101, 100) * 10 ** (2 * D + 4)
        rows[str(D)] = {'leading_coefficient': preview(L['total'], 6), 'sectors': L['sectors'], 'ell_class': preview(L['classes']['ell'], 6),
                        'j_class': preview(L['classes']['j'], 6), 'product_leading': '0',
                        'producer_over_leading_at_1_1000': preview(tot3 / (L['total'] * scale), 8),
                        'producer_product_ratio_1_100_over_1_1000': preview(prod2 / prod3, 6)}
    need(ok_leak, 'omitted_residual_leading_order_independent', rows=rows,
         note='||Q_D (x+y) psi_D||^2 by exact Gram projection (own LDL, parity blocks), sectors verified orthogonal; the producer '
              'rho_Q^2 at tau=1/1000 equals it times tau^(2D+2) to relative 1e-4; the product channel vanishes at leading order and '
              'enters at tau^(2D+4) (ratio 10^(2D+4) per decade)')

    # ---------------- thresholds and ledger
    thr = {str(D): pre_res['per_channel_floors'][str(D)] for D in (6, 8)}
    lrow = {D: res['points']['D%d_tau+1/10' % D]['ledger'] for D in (6, 8)}
    need(all(lrow[D]['a_per_link_representation_tail'][e]['threshold_free_energy'] == thr[str(D)]['A'] for D in (6, 8) for e in ('h1', 'vL', 'h3'))
         and all(lrow[D]['a_per_link_representation_tail'][e]['threshold_free_energy'] == thr[str(D)]['B'] for D in (6, 8) for e in ('h2', 'vR', 'h4'))
         and all(lrow[D]['a_per_link_representation_tail']['vM']['threshold_free_energy'] == thr[str(D)]['S'] for D in (6, 8))
         and all(lrow[D]['b_joint_product_channel']['product_channel_threshold'] == thr[str(D)]['joint'] for D in (6, 8))
         and all(lrow[D]['b_joint_product_channel']['joint_threshold_tail_lower'] == {6: '45', 8: '69'}[D] for D in (6, 8))
         and thr['6'] == {'A': '123/2', 'B': '123/2', 'S': '45', 'joint': '48'} and thr['8'] == {'A': '96', 'B': '96', 'S': '69', 'joint': '145/2'},
         'thresholds_match_prediction', thresholds=thr)
    parts_ok = True
    for key, rec in res['points'].items():
        ld = rec['ledger']
        parts_ok = parts_ok and set(ld) == {'a_per_link_representation_tail', 'b_joint_product_channel', 'c_gauge_invariant_projection',
                                            'd_ritz_eigenvector_residual', 'e_arithmetic'} \
            and len(ld['a_per_link_representation_tail']) == 7 and ld['c_gauge_invariant_projection']['value'] == '0' \
            and 'Gauss' in ld['c_gauge_invariant_projection']['reason'] and 'product_channel_weight_upper' in ld['b_joint_product_channel'] \
            and 'interference_2XY_bracket' in ld['b_joint_product_channel'] and 'directed_sqrt_width_upper' in ld['e_arithmetic']
    need(parts_ok and len(res['points']) == 14, 'ledger_five_parts_present_all_points', points=14)

    # ---------------- report: sentence, forbidden phrases (whole word), consistent-with
    report = (FWD / 'report.md').read_text(encoding='utf-8')
    sentence = pre['mandatory_sentence_template']
    prose_hits = whole_word_hits(strip_code(report), pre['forbidden_phrasings'])
    all_hits = whole_word_hits(report, pre['forbidden_phrasings'])
    need(sentence in report and res['mandatory_sentence'] == sentence and prose_hits == {} and 'consistent with' in report
         and whole_word_hits(sentence, pre['forbidden_phrasings']) == {}, 'mandatory_sentence_and_whole_word_scan',
         prose_hits=prose_hits, quoted_in_code_spans=all_hits,
         note='whole-word, case-insensitive; the only occurrences are the forbidden phrases quoted in code spans in section 9')

    # ---------------- Arb preview
    arb = json.loads((FWD / 'preview/arb_preview.json').read_text())
    balls = arb['wilson_balls']
    arb_ok = arb['label'] == 'PREVIEW ONLY - python-flint Arb/fmpq cross-check; never an admission value' and len(balls) == 14
    dist = {}
    for k, (blo, bhi) in balls.items():
        if k in enc:
            lo, hi = F(enc[k][0]), F(enc[k][1])
            arb_ok = arb_ok and lo <= F(blo) and F(bhi) <= hi
            tl, th = truth_two[k]
            dist[k] = max(tl - F(bhi), F(blo) - th, F(0))
    need(arb_ok and 'PREVIEW ONLY' in (FWD / 'arb_preview.py').read_text(), 'arb_preview_labelled_and_consistent',
         flint_version=arb['flint_version'], balls=len(balls),
         ritz_ball_distance_from_full_graph_value_preview={k: preview(v, 3) for k, v in sorted(dist.items()) if '+' in k},
         note='every Ritz ball lies inside the producer enclosure; a ball is a truncated-matrix value, so it may sit a certified '
              'distance from the full-graph value; never an admission input')

    # ---------------- producer defects and the update-4 correction
    dids = [d['id'] for d in res['contract_wording_defects']]
    need(dids == ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8'] and 'exact_bracket' not in src and 'heuristic' not in report.lower()
         and '/(tail_lower' not in report and 'tau_FG^2/66' not in report, 'producer_defects_and_update4_route', defects=dids,
         note='the producer certifies with the complete residual and the tail comparison; it uses neither update-4 truncated brackets '
              'nor its tau^2/(tail-3) heuristic')

    # ---------------- this review's validator and damaged packets
    truth = {'gate_fields': gate, 'sentence': sentence,
             'coefficients': {'two_face': {'a3': '-187/33696', 'e2': '-1/6', 'e4': '187/67392'},
                              'one_face': {'a3': '-5/864', 'e2': '-1/12', 'e4': '5/3456'}},
             'enclosures': {'two_face': truth_two, 'one_face': one},
             'product_threshold': {'6': '48', '8': '145/2'}}
    need(validate_producer(res, truth), 'producer_packet_validates')

    def dmg(fn):
        pk = json.loads(json.dumps(res))
        fn(pk)
        try:
            validate_producer(pk, truth)
        except Refused as exc:
            return str(exc)
        return None
    damaged = [
        ('hamiltonian_relabelled_one_face', lambda p: p['headline'].__setitem__('hamiltonian', 'H_FG = K - tau_FG W_1 (second face uncoupled)')),
        ('one_face_energy_with_two_face_series', lambda p: p['headline']['second_order_coefficients'].__setitem__('E_0', '-1/12')),
        ('model_unnamed', lambda p: p['headline'].__setitem__('hamiltonian', 'H_FG = K - tau_FG V')),
        ('derivative_1_144', lambda p: p['headline']['derivative_at_zero'].__setitem__('6', ['1/144', '1/144'])),
        ('free_reference_quarter', lambda p: p['headline']['free_reference'].__setitem__('8', ['1/4', '1/4'])),
        ('second_order_nonzero', lambda p: p['headline']['second_order_coefficients'].__setitem__('W_1', '1/1000')),
        ('fitted_true', lambda p: p.__setitem__('fg_coefficients_fitted', True)),
        ('transfers_true', lambda p: p.__setitem__('transfers_to_aq', True)),
        ('tail_56', lambda p: p['headline']['tail_lower'].__setitem__('8', '56')),
        ('enclosure_shifted_to_one_face', lambda p: p['headline']['wilson_enclosures'].__setitem__('D8_tau+1/10', [q(one['D8_tau+1/10'][0]), q(one['D8_tau+1/10'][1])])),
        ('sign_lost', lambda p: p['headline']['wilson_enclosures'].__setitem__('D6_tau+1/1000', ['-1/10000000000', '1/1000'])),
        ('joint_ledger_dropped', lambda p: p['points']['D6_tau-1/100']['ledger'].pop('b_joint_product_channel')),
        ('gauge_reason_dropped', lambda p: p['points']['D8_tau+1/10']['ledger']['c_gauge_invariant_projection'].__setitem__('reason', '')),
        ('vM_row_dropped', lambda p: p['points']['D8_tau+1/100']['ledger']['a_per_link_representation_tail'].pop('vM')),
        ('product_threshold_45', lambda p: p['points']['D6_tau+1/10']['ledger']['b_joint_product_channel'].__setitem__('product_channel_threshold', '45')),
        ('sentence_altered', lambda p: p.__setitem__('mandatory_sentence', p['mandatory_sentence'].replace('is consistent with', 'confirms'))),
        ('dictionary_as_prediction', lambda p: p['headline']['dictionary'].__setitem__('relation', 'predicts')),
        ('sub_label_dropped', lambda p: p.__setitem__('sub_labels', ['sign_certified_finite_graph'])),
    ]
    refused = [(label, dmg(fn)) for label, fn in damaged]
    need(all(reason for _, reason in refused), 'damaged_packets_refused', count=len(refused),
         refusals={label: reason for label, reason in refused})

    # ---------------- source-edit mutations on temporary copies (python -B, outside the checkout)
    specs = [('unmutated', dict())]
    for cid, anchor, _ in CONTROL_WEAKENINGS:
        specs.append(('ctl_' + cid, dict(edits=[(RAT_OLD, RAT_NEW)] if anchor is None else [ret_true(anchor)])))
    for label, spec, _, _ in SEMANTIC_EDITS:
        specs.append(('sem_' + label, spec))
    with ThreadPoolExecutor(max_workers=4) as pool:
        outcomes = list(pool.map(lambda sp: mutated_run(**sp[1]), specs))
    runs = dict(zip([s[0] for s in specs], outcomes))
    frozen = {p.name: p.read_bytes() for p in (FWD / 'output').glob('*')}
    rc0, outs0, _ = runs['unmutated']
    need(rc0 == 0 and outs0 == frozen, 'unmutated_copy_reproduces_frozen_outputs',
         note='copy outside the checkout; results.json and source-manifest.json byte-identical to output/')
    ctl_rows = {}
    for cid, anchor, first_label in CONTROL_WEAKENINGS:
        rc_, _, last = runs['ctl_' + cid]
        ctl_rows[cid] = {'exit': rc_, 'last_error': last}
        if not (rc_ != 0 and last == 'AdmissionError: damaging mutation accepted: ' + first_label):
            raise ReviewFailure('control weakening not caught at its control: ' + cid + ' / ' + last)
    need(len(ctl_rows) == 20 and sorted(ctl_rows) == sorted(contract['controls']), 'contract_controls_source_edit_weakenings_abort',
         runs=ctl_rows, note='each validator made to return True (rat made to accept non-exact input); the copy aborts with '
                             '"damaging mutation accepted" at that control')
    sem_rows = {}
    for label, _, expect, msg in SEMANTIC_EDITS:
        rc_, outs, last = runs['sem_' + label]
        if expect == 'abort':
            ok = rc_ != 0 and last.startswith('AdmissionError') and (msg is None or last == 'AdmissionError: ' + msg)
        else:
            res_m = json.loads(outs['results.json']) if 'results.json' in outs else None
            ok = rc_ == 0 and res_m is not None and outs.get('results.json') != frozen['results.json'] \
                and res_m['headline'] == res['headline'] and res_m['points'] == res['points']
        if not ok:
            raise ReviewFailure('semantic edit ' + label + ': ' + last)
        sem_rows[label] = {'exit': rc_, 'last_error': last} if expect == 'abort' else \
            {'exit': rc_, 'outcome': 'completes; headline and points unchanged; only the preview comparison record differs'}
    need(True, 'semantic_source_edits', runs=sem_rows,
         note='one-face RS default, one-face certificate Hamiltonian, free gap 4, omitted residual dropped and a forbidden phrase abort; '
              'removing the Arb preview output changes no admission value')

    return {
        'loop': 'AZ2', 'stage': 'post_comparison', 'role': 'skeptic post-comparison review (single+skeptic admission input)',
        'standing': 'model-agent skeptic with correlated ancestry; not human peer review, not formal verification',
        'human_author': 'Hruday N M (BUNZEEY)',
        'checker_sha256': sha(Path(__file__)), 'contract_sha256': CONTRACT_SHA256, 'producer_sha256': PRODUCER,
        'pre_comparison': {'checker_sha256': PRE_CHECK_SHA256, 'freeze_sha256': PRE_FREEZE_SHA256, 'results_sha256': PRE_RESULTS_SHA256},
        'model_resolution': {
            'computed_by_producer': TWO_FACE_HAMILTONIAN,
            'pre_comparison_reading': 'H_FG = K - tau_FG W_1 (second face uncoupled; spectator identity with the AW1 one-plaquette fixture)',
            'contract': 'fixes neither; non-blocking wording defect; the gate names the two-face model',
            'identification': {'two_face': {'a3': '-187/33696', 'E_2': '-1/6', 'E_4': '187/67392'},
                               'one_face': {'a3': '-5/864', 'E_2': '-1/12', 'E_4': '5/3456'}},
            'common': {'derivative_at_zero': '1/6', 'second_order_W': '0', 'dictionary': '1/6 -> 1/144'},
            'two_body_shift_tau3': '1/4212',
            'spectator_identity': 'holds only for the one-face model; the two-face model differs from the AW1 fixture at third order'},
        'independent_enclosures_two_face': {q(t): {'lower_1e-60': q(mine[t]['lower']), 'upper_1e-60': q(mine[t]['upper']),
                                                   'half_width_preview': preview(mine[t]['half'], 4)} for t in GRID},
        'producer_enclosures_decimal_32': {k: [pm.dec(F(v[0]), 32, False), pm.dec(F(v[1]), 32, True)] for k, v in sorted(enc.items())},
        'two_body_shift_intervals_D8': {k: [q(rdown(v[0], 10 ** 40)), q(rup(v[1], 10 ** 40))] for k, v in sorted(shift.items()) if k.startswith('D8')},
        'counts': {'checks': None, 'damaged_packets_refused': len(refused), 'source_edit_runs': len(specs),
                   'contract_control_weakenings': 20, 'semantic_edits': len(SEMANTIC_EDITS)},
        'checks': CHECKS,
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--output', required=True)
    args = ap.parse_args()
    out = Path(args.output)
    if not out.is_absolute():
        raise SystemExit('--output must be an absolute path')
    if ROOT in out.resolve().parents:
        raise SystemExit('--output must lie outside the checkout')
    if out.exists() and any(out.iterdir()):
        raise SystemExit('--output must be fresh (absent or empty)')
    result = run()
    result['counts']['checks'] = len(result['checks'])
    out.mkdir(parents=True, exist_ok=True)
    (out / 'results.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'checks': result['counts']['checks'], 'source_edit_runs': result['counts']['source_edit_runs'],
                      'damaged_packets_refused': result['counts']['damaged_packets_refused']}))


if __name__ == '__main__':
    main()
