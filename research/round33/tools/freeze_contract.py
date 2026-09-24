#!/usr/bin/env python3
"""Stamp a Round33 contract as frozen_before_production after validating its fields.

  python3 -B research/round33/tools/freeze_contract.py research/round33/contracts/ba1.json

Required fields: id, round=33, subround, sequence, title, human_author, model,
parameters, shared_premises (existing repo-relative files), required (non-empty),
controls (non-empty), claim_exclusions (non-empty), producers (["forward","reverse"]
or ["forward"]), direction, preregistration (object), stop.

Round32 closing-panel rules enforced here (research/round32/experts/jung/update-5.md
section 3 and research/round32/advisor/panel-update-5.md item 3):
  R1 no angle-bracket placeholder span (<...> containing whitespace, '|' or 'e.g.');
  R2 a mandatory_sentence_template is required when a required item cites a template;
  R3 a finite-model contract names every Hamiltonian coupling term by term;
  R4 state_provenance/clock/error_terms_itemized may not be copied byte-for-byte from
     another contract of a different declared model family;
  R5 a statement loop states whether its target is a feasibility/format check or a
     blind discriminating threshold;
  R8 a selected_after gate that does not exist yet needs a selected_after_note;
  the preregistration control mirror must equal the controls list (Round32 rule).
The tool refuses to re-freeze a contract whose status is already frozen.
"""
import datetime
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PLACEHOLDER = re.compile(r'<([^<>]*)>')
TEMPLATE_CITES = ('mandatory sentence template', 'mandatory sentence', 'sentence template')
DIRECTIONS = ('paired', 'single+skeptic', 'statement+skeptic', 'statement-only')


def strings(value, path='$'):
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, dict):
        for k, v in value.items():
            yield from strings(v, path + '.' + str(k))
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from strings(v, path + '[' + str(i) + ']')


def placeholder_spans(text):
    out = []
    for m in PLACEHOLDER.finditer(text):
        inner = m.group(1)
        if re.search(r'\s', inner) or '|' in inner or 'e.g.' in inner:
            out.append(m.group(0))
    return out


def fail(msg):
    raise SystemExit('freeze_contract.py: ' + msg)


def main():
    path = ROOT / sys.argv[1]
    c = json.loads(path.read_text())
    if c.get('status') == 'frozen_before_production':
        fail('already frozen: ' + str(path))
    for key in ('id', 'round', 'subround', 'sequence', 'title', 'human_author', 'model', 'parameters',
                'shared_premises', 'required', 'controls', 'claim_exclusions', 'producers', 'direction',
                'preregistration', 'stop'):
        if key not in c:
            fail('missing field ' + key)
    if c['round'] != 33 or c['producers'] not in (['forward', 'reverse'], ['forward']):
        fail('bad round or producers')
    if c['direction'] not in DIRECTIONS:
        fail('direction must be one of ' + ', '.join(DIRECTIONS))
    if (c['producers'] == ['forward', 'reverse']) != (c['direction'] == 'paired'):
        fail('paired direction iff two producers')
    for name in c['shared_premises'] + list(c.get('forward_additional_premises') or []):
        if not (ROOT / name).is_file():
            fail('missing premise ' + name)
    for key in ('required', 'controls', 'claim_exclusions'):
        if not c[key]:
            fail('empty ' + key)
    pre = c['preregistration']
    if pre.get('controls_required', {}).get('ids') != c['controls']:
        fail('preregistration.controls_required.ids must equal controls')
    # R1 placeholders
    spans = [(p, s) for p, text in strings(c) for s in placeholder_spans(text)]
    if spans:
        fail('R1 placeholder spans remain: ' + json.dumps(spans[:5]))
    # R2 template
    req_text = ' '.join(c['required']).lower()
    if any(t in req_text for t in TEMPLATE_CITES) and not str(pre.get('mandatory_sentence_template', '')).strip():
        fail('R2 required items cite a sentence template but preregistration.mandatory_sentence_template is empty')
    # R3 finite models
    finite = bool(pre.get('model_is_finite_graph')) or str(pre.get('model_id', '')).startswith('FG(') \
        or bool(c.get('parameters', {}).get('model_is_finite_graph'))
    if finite:
        couplings = c.get('parameters', {}).get('hamiltonian_terms')
        if not (isinstance(couplings, list) and couplings and all(isinstance(t, dict) and t.get('term') and
                                                                   'coefficient' in t for t in couplings)):
            fail('R3 finite-model contract must list parameters.hamiltonian_terms as [{term, coefficient}] for every coupling')
    # R4 copied vocabulary
    family = str(pre.get('model_id', ''))
    for other in sorted((path.parent).glob('*.json')):
        if other == path:
            continue
        o = json.loads(other.read_text())
        opre = o.get('preregistration', {})
        if str(opre.get('model_id', '')) == family:
            continue
        for key in ('state_provenance', 'clock', 'error_terms_itemized'):
            if key in pre and key in opre and pre[key] == opre[key]:
                fail('R4 ' + key + ' copied byte-for-byte from ' + other.name + ' of a different model family')
    # R5 statement targets
    if c['direction'].startswith('statement'):
        note = str(pre.get('target', {}).get('note', '')).lower()
        if not ('feasibility' in note or 'format check' in note or 'blind' in note or 'discriminating' in note):
            fail('R5 statement loop target.note must say feasibility/format check or blind discriminating threshold')
    # R8 selected_after
    sel = c.get('selected_after')
    if sel and not (ROOT / sel).is_file() and not c.get('selected_after_note'):
        fail('R8 selected_after names a gate that does not exist yet; add selected_after_note')
    c['status'] = 'frozen_before_production'
    c['frozen_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    path.write_text(json.dumps(c, indent=2) + '\n')
    print(json.dumps({'status': 'frozen', 'id': c['id'], 'premises': len(c['shared_premises'])}))


if __name__ == '__main__':
    main()
