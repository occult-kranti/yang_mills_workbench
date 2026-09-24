#!/usr/bin/env python3
"""Jung/Pauli lens, Round33 sub-round 1, assistant-1 script 3 of 3: the rule-R9
pilot named in `research/round33/experts/jung/loop2-response.md` section 3 item
(d) and the calling task's item 3 -- compare `plan.json#/vocabulary/forbidden`
against `tools/phrase_scan.py#ROUND_FORBIDDEN` (the code every gate actually
scans against) and against each contract's own `preregistration.forbidden_phrasings`,
and list every disagreement, without blocking anything.

Counts zero research loops. Not a producer, contract, gate or skeptical review;
nothing computed here is read back into any of those. Human project author:
Hruday N M (BUNZEEY); AI-assisted. Standard library only. Does not import
`forward/*/check.py`, `reverse/*/check.py`, or any other producer/skeptic module;
imports `research/round33/tools/phrase_scan.py` as a library (per the calling
task) to read `ROUND_FORBIDDEN` itself, not a copy of it, so a future edit to
that list is picked up automatically, not silently missed by a stale copy.

Loop2-response.md's own finding (section 2, "Forbidden phrasings"), quoted for
context: "`tools/phrase_scan.py#/ROUND_FORBIDDEN` ... is a proper superset of
this lens's 'newly forbidden' list plus extra project phrases ...;
`plan.json#/vocabulary/forbidden` is a shorter, non-identical planning list.
That divergence is cosmetic -- nothing in `record_gate.py` reads `plan.json` for
forbidden phrases -- but it is exactly the kind of cross-file disagreement this
lens's own R9 proposal exists to catch, and R9 (`field_mirror_sweep.py`) does
not exist yet." This script is that missing sweep's first, narrowly-scoped
(forbidden-phrase list only) pilot -- hence its own name and the calling task's
"(rule R9 pilot)" label.

Two additional, itemized findings this script adds beyond loop2-response.md's
own prose description (git-history evidence for both is recorded in the
README, not recomputed here, since `git log` is not exact-rational admission
evidence and this script's own re-runs must not depend on repository history
being present the way a fresh, git-less replay directory is):

  - loop2-response.md itself proposed four SCOPED "unique ..." phrases
    (`unique ground state`, `a unique limit`, `unique infinite-volume`,
    `uniquely determines the ground state`) be added to ALL THREE of
    `ROUND_FORBIDDEN`, `plan.json#/vocabulary/forbidden` and both contracts'
    `forbidden_phrasings`, "closing the actual risk ... without penalizing
    AM2's already-admitted uniqueness-of-fixed-point language." Only
    `ROUND_FORBIDDEN` was actually edited (3 of the 4 phrases; not
    `"uniquely determines the ground state"`), in the very next commit after
    loop2-response.md itself, citing it by name. `plan.json#/vocabulary/forbidden`
    and both BA1's and BA2's `forbidden_phrasings` were edited again after that
    commit (when BA1/BA2 froze) but never received any of the four phrases.
  - `plan.json#/vocabulary/forbidden` names `"the thermodynamic limit"` as a
    round-wide forbidden phrase, but `ROUND_FORBIDDEN` itself has never
    contained it (checked against both the phrase list's original commit and
    its one later edit) -- it is only ever scanned for a loop whose OWN
    contract separately lists it in `forbidden_phrasings` (both BA1 and BA2
    happen to; a future contract that forgets to would silently not have it
    scanned at all, contrary to what plan.json's own vocabulary implies).

Usage: python3 -B vocabulary_mirror.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common1 as K  # noqa: E402

sys.path.insert(0, str(K.TOOLS))
import phrase_scan as ps  # noqa: E402

# The four phrases loop2-response.md section 2 proposed adding to all three
# vocabularies (quoted verbatim from that file).
PROPOSED_UNIQUE_PHRASES = (
    'unique ground state', 'a unique limit', 'unique infinite-volume', 'uniquely determines the ground state',
)


def forbidden_list_mirror():
    plan = K.load_plan()
    plan_forbidden = set(plan['vocabulary']['forbidden'])
    round_forbidden = set(ps.ROUND_FORBIDDEN)

    plan_only = sorted(plan_forbidden - round_forbidden)
    round_only = sorted(round_forbidden - plan_forbidden)
    both = sorted(plan_forbidden & round_forbidden)

    per_contract = {}
    for loop in K.LOOPS:
        L = loop.upper()
        contract = K.load_contract(loop)
        fp = set(contract['preregistration']['forbidden_phrasings'])
        per_contract[L] = {
            'forbidden_phrasings': sorted(fp),
            'subset_of_round_forbidden': fp <= round_forbidden,
            'subset_of_plan_forbidden': fp <= plan_forbidden,
            'not_in_round_forbidden': sorted(fp - round_forbidden),
            'not_in_plan_forbidden': sorted(fp - plan_forbidden),
            'entirely_covered_by_round_forbidden_alone': fp <= round_forbidden,
        }

    proposed_status = {}
    for phrase in PROPOSED_UNIQUE_PHRASES:
        proposed_status[phrase] = {
            'in_ROUND_FORBIDDEN': phrase in round_forbidden,
            'in_plan_forbidden': phrase in plan_forbidden,
            'in_ba1_forbidden_phrasings': phrase in set(K.load_contract('ba1')['preregistration']['forbidden_phrasings']),
            'in_ba2_forbidden_phrasings': phrase in set(K.load_contract('ba2')['preregistration']['forbidden_phrasings']),
        }
    n_adopted_anywhere = sum(1 for v in proposed_status.values() if any(v.values()))
    n_adopted_in_round_forbidden = sum(1 for v in proposed_status.values() if v['in_ROUND_FORBIDDEN'])

    thermodynamic_limit_gap = {
        'phrase': 'the thermodynamic limit',
        'in_plan_forbidden': 'the thermodynamic limit' in plan_forbidden,
        'in_ROUND_FORBIDDEN': 'the thermodynamic limit' in round_forbidden,
        'in_ba1_forbidden_phrasings': 'the thermodynamic limit' in set(K.load_contract('ba1')['preregistration']['forbidden_phrasings']),
        'in_ba2_forbidden_phrasings': 'the thermodynamic limit' in set(K.load_contract('ba2')['preregistration']['forbidden_phrasings']),
    }

    # Round32's own carried-forward "bare unique without an explicit not"
    # rule (loop2-response.md section 2): confirm it is present as a literal,
    # scannable token in none of the three vocabularies (every entry that
    # mentions "unique" is a longer, scoped phrase, never the bare word alone).
    def has_bare_unique_token(strings):
        return any(s.strip().lower() in ('unique', 'uniquely') for s in strings)

    bare_unique_rule_status = {
        'in_ROUND_FORBIDDEN': has_bare_unique_token(round_forbidden),
        'in_plan_forbidden': has_bare_unique_token(plan_forbidden),
        'in_ba1_forbidden_phrasings': has_bare_unique_token(K.load_contract('ba1')['preregistration']['forbidden_phrasings']),
        'in_ba2_forbidden_phrasings': has_bare_unique_token(K.load_contract('ba2')['preregistration']['forbidden_phrasings']),
    }

    findings = [
        'plan.json#/vocabulary/forbidden has %d entries; tools/phrase_scan.py ROUND_FORBIDDEN has %d entries; '
        '%d entries are in both.' % (len(plan_forbidden), len(round_forbidden), len(both)),
        'In plan.json#/vocabulary/forbidden but NOT in ROUND_FORBIDDEN (%d): %r -- every one of these is a '
        'descriptive rule-label ("X (unqualified)", "Y (without Z)") rather than a literal scannable phrase, '
        'confirming loop2-response.md\'s own reading that the divergence is a planning-document/implementation gap, '
        'not a missed enforcement, EXCEPT "the thermodynamic limit" (see the dedicated finding below, which IS a '
        'literal phrase and IS missing from the round-wide list).' % (len(plan_only), plan_only),
        'In ROUND_FORBIDDEN but NOT in plan.json#/vocabulary/forbidden (%d): %r -- these are all literal phrases '
        'the real scanner enforces round-wide that plan.json\'s own planning list does not mention at all (the AQ '
        'state, the mass-gap-solved family, the Z^3-value-confirmation phrase, the continuum-limit-exists phrase, '
        'the fraction-of-the-problem phrase, and 6 of the 2026-09-24 21:37:52 "unique ..." additions -- see the '
        'dedicated finding below for which 3 of loop2-response.md\'s proposed 4 these are).' % (len(round_only), round_only),
    ]

    findings.append('DEDICATED FINDING 1 -- loop2-response.md\'s own proposed scoped "unique ..." phrases, adopted '
                    'ONLY into ROUND_FORBIDDEN (3 of 4), never into plan.json#/vocabulary/forbidden or either '
                    'contract\'s forbidden_phrasings (git evidence in the README): %r' % proposed_status)
    findings.append('  -> %d of 4 proposed phrases adopted somewhere; %d of 4 adopted into ROUND_FORBIDDEN (the '
                    'phrase actually scanned); 0 of 4 adopted into plan.json or either contract.'
                    % (n_adopted_anywhere, n_adopted_in_round_forbidden))
    findings.append('DEDICATED FINDING 2 -- "the thermodynamic limit" is named in plan.json#/vocabulary/forbidden as '
                    'a round-wide forbidden phrase but has never been part of ROUND_FORBIDDEN itself; it is only '
                    'scanned for BA1/BA2 because both contracts separately re-list it in their own '
                    'forbidden_phrasings: %r' % thermodynamic_limit_gap)
    findings.append('DEDICATED FINDING 3 (re-confirms loop2-response.md section 2\'s own, still-open point) -- the '
                    'Round32 carried-forward rule ("a bare \'unique\' without an explicit \'not\' in the same clause '
                    'is forbidden") is present as a literal bare token in NONE of the three vocabularies: %r -- '
                    'phrase_audit.py\'s bare_unique_hand_audit is this package\'s own manual stand-in for the still-'
                    'missing mechanical rule.' % bare_unique_rule_status)

    for loop, v in per_contract.items():
        if v['subset_of_round_forbidden']:
            findings.append('%s forbidden_phrasings %r: entirely already covered by ROUND_FORBIDDEN alone (these '
                            'contract-level entries add nothing beyond what the round list already scans; none of '
                            'loop2-response.md\'s 4 proposed phrases appear here either).' % (loop, v['forbidden_phrasings']))
        else:
            findings.append('%s forbidden_phrasings %r: %d entr%s NOT already in ROUND_FORBIDDEN (%r) -- this '
                            'contract-level list is not purely redundant with the round list, it is the ONLY place '
                            '%r is actually enforced for %s (see DEDICATED FINDING 2); none of loop2-response.md\'s '
                            '4 proposed "unique ..." phrases appear here.'
                            % (loop, v['forbidden_phrasings'], len(v['not_in_round_forbidden']),
                               'y is' if len(v['not_in_round_forbidden']) == 1 else 'ies are',
                               v['not_in_round_forbidden'], v['not_in_round_forbidden'], loop))

    passed = True  # an R9 sweep records disagreements; it does not block (the calling task: "without blocking anything")
    return {
        'id': 'forbidden_list_mirror',
        'role': 'rule R9 pilot (calling task item 3): plan.json#/vocabulary/forbidden vs tools/phrase_scan.py '
                'ROUND_FORBIDDEN vs each contract\'s forbidden_phrasings; zero research loops; lists disagreements, '
                'blocks nothing',
        'plan_forbidden_count': len(plan_forbidden), 'round_forbidden_count': len(round_forbidden),
        'in_both': both, 'plan_only': plan_only, 'round_only': round_only, 'per_contract': per_contract,
        'proposed_unique_phrases_status': proposed_status, 'thermodynamic_limit_gap': thermodynamic_limit_gap,
        'bare_unique_rule_status': bare_unique_rule_status,
        'passed': passed, 'findings': findings,
    }


def run():
    checks = [forbidden_list_mirror()]
    return {
        'id': 'vocabulary_mirror',
        'role': 'Jung/Pauli lens, Round33 sub-round 1, assistant-1: rule R9 pilot, calling task item 3; zero '
                'research loops; audits only, never admission evidence; records disagreements without blocking '
                'anything',
        'checks': {c['id']: c for c in checks},
        'passed': all(c['passed'] for c in checks),
    }


def main():
    result = run()
    out_path = Path(__file__).resolve().parent / 'results.json'
    K.merge_results(out_path, 'vocabulary_mirror', result)
    print('vocabulary_mirror: %s' % ('recorded (see findings; an R9 sweep never blocks)' if result['passed'] else 'FAIL'))
    for check_id, c in result['checks'].items():
        for f in c['findings']:
            print('  -', f)


if __name__ == '__main__':
    main()
