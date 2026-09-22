#!/usr/bin/env python3
"""Deterministic additive Draft03 integration, exclusively from three gated loops."""
from pathlib import Path
import hashlib
import json
import re
import shutil
import subprocess
from tex_helpers import tx, prose, inline_math, plain

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'papers/draft-03'
PREVIOUS = ROOT / 'papers/draft-02'
ROUND = ROOT / 'research/round30'
AUTHOR = 'Hruday N M (BUNZEEY)'

def require(ok, message):
    if not ok:
        raise ValueError(message)

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def dump(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n')

def summary_latex(rid, fallback):
    summaries = {
        'AT1': r'In the actual numerical-cap AQ state at either sign of $|\tau|\le10^{-8}$, the centered original Wilson vector satisfies $\chi\in D(H_{\rm phys})$. Its second-energy moment is at most $\alpha^2(36+98|\tau|)<37\alpha^2$, and its first-energy moment equals $\alpha\omega_{\rm num}(1-W^2)$.',
        'AT2': r'For the same state, the unnormalized spectral mass satisfies $\nu([\alpha/16,8\alpha])\ge307992/1984375$. On the physical vacuum-orthogonal sector let $R=\langle\chi,H_{\rm phys}^{-1}\chi\rangle$. Its dimensionless value has lower bound $3843876001/47000000000$ and upper bound $28462237549/7503125000$: these are bounds on $\alpha R$, not an evaluated response or a unique spectral measure.',
        'AT3': r'The fixed 4097-node protocol conditionally encloses $I=\alpha R$ when supplied certified centered AQ samples with absolute error at most $10^{-6}$. Exact rational data give interval width below $1/500$; arithmetic bins contribute their explicitly bounded trapezoid width. Both executed abstract A/B benchmarks pass, and their full admissible-error output envelopes are disjoint. No actual AQ correlation samples or response value are supplied.'
    }
    return summaries.get(rid, prose(fallback))

def source_records():
    records = []
    for lens in ['modern', 'historical']:
        file = ROUND / 'experts' / lens / 'sources.json'
        data = json.loads(file.read_text())
        entries = data.get('records', data.get('sources', []))
        for entry in entries:
            records.append((lens, entry))
    extra = json.loads((ROUND / 'editorial/method-source-addendum.json').read_text())
    records.extend(('method addendum', entry) for entry in extra['records'])
    return records

def render_report(path, entry, direction, registry):
    """Preserve the source report's paragraphs and all displayed equations."""
    rid = entry['id'].upper()
    lid = rid.lower()
    initial = 'F' if direction == 'forward' else 'R'
    source_text = path.read_text()
    ast = json.loads(subprocess.check_output(
        ['pandoc', '-f', 'markdown+tex_math_single_backslash+tex_math_dollars', '-t', 'json'],
        input=source_text, text=True))
    counter = [0]

    def walk(node):
        if isinstance(node, list):
            return [walk(x) for x in node]
        if not isinstance(node, dict):
            return node
        kind, content = node.get('t'), node.get('c')
        if kind == 'Header':
            level, attr, inlines = content
            attr[0] = f'r30-{lid}-{direction}-' + attr[0]
            if level == 1:
                title = entry['title'].removeprefix('HNM ').removeprefix('Hruday ')
                inlines = [{'t': 'Str', 'c': f'Hruday {rid}: {title} ({direction} derivation)'}]
            elif inlines and inlines[0].get('t') == 'Str' and re.fullmatch(r'\d+\.', inlines[0]['c']):
                inlines = inlines[1:]
                if inlines and inlines[0].get('t') == 'Space':
                    inlines = inlines[1:]
            # Independent directions get complete sections; subsection hierarchy preserved.
            return {'t': kind, 'c': [level, attr, walk(inlines)]}
        if kind == 'Code':
            code = content[1].replace('²', '^2').replace('³', '^3').replace('⁴', '^4')
            if code.startswith(('http://', 'https://')):
                return {'t': 'RawInline', 'c': ['latex', r'\url{' + code + '}']}
            if code.startswith(('research/', 'papers/', 'inputs/')) or len(code) > 64:
                return {'t': 'RawInline', 'c': ['latex', r'{\small\path{' + code + '}}']}
            math = inline_math(code)
            if math is not None:
                return {'t': 'Math', 'c': [{'t': 'InlineMath'}, math]}
            return {'t': kind, 'c': [content[0], code]}
        if kind == 'Math' and content[0]['t'] == 'DisplayMath':
            counter[0] += 1
            n = counter[0]
            math = content[1].strip()
            tag_match = re.search(r'\\tag\{([^}]+)\}', math)
            source_tag = tag_match[1] if tag_match else None
            tag = source_tag if source_tag and source_tag.startswith('HNM-') else f'HNM-{rid}-{initial}{n:02d}'
            math = re.sub(r'\\tag\{[^}]+\}', '', math)
            math = re.sub(r'\\label\{[^}]+\}', '', math)
            math = re.sub(r'\n\s*\n', '\n', math).strip()
            math = re.sub(r'(?<![A-Za-z\\])Vsel_R\b', lambda _: r'V_R^{\mathrm{sel}}', math)
            # These long source displays retain their exact algebra and tag;
            # grouping into lines avoids unreadably shrinking an entire chain.
            line_groups = {'HNM-AT2-F02': 2, 'HNM-AT2-F03': 2, 'HNM-AT2-R01': 2,
                           'HNM-AT3-R02': 3, 'HNM-AT3-R06': 1, 'HNM-AT3-R10': 1}
            if tag in line_groups:
                pieces = re.split(r'\\(?:qquad|quad)\s*', math)
                group_size = line_groups[tag]
                lines = [r'\quad '.join(pieces[i:i + group_size]) for i in range(0, len(pieces), group_size)]
                math = r'\begin{gathered}' + '\n' + '\\\\\n'.join(lines) + '\n' + r'\end{gathered}'
            label = f'r30:{lid}:{direction}:eq{n}'
            relative = f'addenda/round30/{lid}-{direction}.tex'
            registry['equations'].append({
                'id': f'HNM-E-R30-{rid}-{initial}-{n:02d}',
                'legacy_label': label, 'legacy_source_tag': source_tag,
                'label_kind': 'equation', 'source': relative,
                'source_path': str(path.relative_to(ROOT)), 'direction': direction,
                'contribution_ids': ['HNM-C-' + rid],
                'scope': 'Source equation alias, not an additional discovery. The complete loop gate determines the accepted shared result and any directional refinement.',
                'printed_locator': tag,
            })
            latex = '\n'.join([r'\begin{equation}', r'\hnmfit{' + math + '}', r'\tag{' + tag + r'}\label{' + label + '}', r'\end{equation}'])
            return {'t': 'RawInline', 'c': ['latex', latex]}
        return {key: walk(value) for key, value in node.items()}

    ast = walk(ast)
    body = subprocess.check_output(['pandoc', '-f', 'json', '-t', 'latex', '--wrap=none'], input=json.dumps(ast), text=True)
    body = re.sub(r'\\label\{(?!r30:)([^}]+)\}', lambda m: r'\label{r30:' + lid + ':' + direction + ':' + m[1] + '}', body)
    body = body.replace('Gauvin, arXiv:2503.15539v3', r'Gauvin~\citep{gauvin2026}, arXiv:2503.15539v3')
    note = (r'\begin{quote}\small\textbf{Source-bound ' + direction + r' derivation.} '
            + r'This is the complete typeset mathematical report of one producer. Prospective claims describe its original freeze; '
            + r'the shared reviewed result and permitted refinements are stated in the admission section. The two agents share inherited premises and model ancestry. '
            + r'This is neither an independent physical observation nor external human peer review.\end{quote}' + '\n')
    split = body.find('\n\n')
    body = body[:split+2] + note + body[split+2:]
    body += '\n' + r'\repo{' + str(path.relative_to(ROOT)) + '}\n'
    return body

def write_sources():
    rows = [r'\section{Round30 source comparison and reading limits}', r'\label{sec:r30-sources}',
            r'The following records describe selected source reading, not an exhaustive state-of-the-art survey. Historical documents, patents, government custody and subreddit discussions may motivate controls, but none establishes a new Hamiltonian term. An unread lead remains a lead. Standard methods and their authors retain attribution.',
            r'The modern comparison uses moment duality of Bertsimas--Popescu~\citep{bertsimas2005moments} and the spectral-kernel formulation of Abbott and collaborators~\citep{abbott2026causal}. These precede this application. The positive pointwise certificates in the following derivations do not claim a new generic moment method. The magnetic-basis trial-state route of Spriggs and collaborators~\citep{spriggs2025su2} remains prospective; finite numerical energy improvements do not prove a lower gap.',
            r'\begingroup\footnotesize\setlength{\tabcolsep}{4pt}',
            r'\begin{longtable}{@{}p{43mm}p{65mm}p{44mm}@{}}',
            r'\toprule Source / version & Actual reading and relevance & Limits\\\midrule\endhead']
    for lens, record in source_records():
        name = record.get('title', record.get('id', 'Source'))
        url = record.get('url', '')
        version = record.get('version_date', record.get('version', record.get('date', '')))
        depth = record.get('reading_depth', '')
        sections = record.get('sections_read', record.get('passages_read', record.get('passages', record.get('passage_read', []))))
        if isinstance(sections, list):
            sections = '; '.join(str(x) for x in sections)
        relevance = record.get('relevance', record.get('modern_use', record.get('use', '')))
        limits = record.get('unresolved', record.get('limits', record.get('verification_limit', 'See linked reading ledger.')))
        a = (r'\href{' + url + '}{' + tx(name) + '}' if url else tx(name)) + r'\par ' + tx(version)
        b = tx(depth) + r'\par ' + tx(sections) + r'\par ' + tx(relevance)
        rows.append(a + ' & ' + b + ' & ' + tx(limits) + r'\\\addlinespace')
    rows += [r'\bottomrule\end{longtable}\endgroup', r'\repo{research/round30/experts/modern/sources.json}', r'\par\repo{research/round30/experts/historical/sources.json}']
    (OUT / 'sections/round30-sources.tex').write_text('\n'.join(rows) + '\n')

def append_bibliography():
    file = OUT / 'sources/references.bib'
    text = (PREVIOUS / 'sources/references.bib').read_text()
    text += r'''
@article{bertsimas2005moments,
 author={Dimitris Bertsimas and Ioana Popescu},
 title={Optimal Inequalities in Probability Theory: A Convex Optimization Approach},
 journal={SIAM Journal on Optimization},volume={15},number={3},pages={780--804},year={2005},
 doi={10.1137/S1052623401399903},
 url={https://web.mit.edu/dbertsim/www/papers/MomentProblems/Optimal-inequalities-in-probability-theory-A-convex-optimization-approach-SIAM15.pdf}}
@misc{abbott2026causal,
 author={Ryan Abbott and Sarah Fields and William I. Jay and Patrick Oare and Matteo Saccardi},
 title={The Causal Bootstrap: Bounding Smeared Spectral Functions from Non-Perturbative Euclidean Data},
 year={2026},eprint={2605.20509},archivePrefix={arXiv},note={Version 1, 19 May 2026; selected sections read},
 url={https://arxiv.org/abs/2605.20509v1}}
@misc{spriggs2025su2,
 author={Thomas Spriggs and Eliska Greplova and Juan Carrasquilla and Jannes Nys},
 title={Accurate ground states of SU(2) lattice gauge theory in 2+1D and 3+1D},
 year={2025},eprint={2509.12323},archivePrefix={arXiv},note={Version 1, 15 September 2025},
 url={https://arxiv.org/abs/2509.12323v1}}
'''
    file.write_text(text)

def append_names(registry):
    additions = [r'\clearpage\subsection{Round30 contribution and statement aliases}',
                 r'The following three records extend the inherited catalog. Aliases for both directions preserve provenance and do not double the number of contributions. No new axioms are asserted.']
    for contribution in registry['contributions']:
        if contribution.get('round') != 30:
            continue
        additions += [r'\paragraph{' + tx(contribution['id']) + ': ' + tx(contribution['display_name']) + '} ' + summary_latex(contribution['legacy_id'], contribution['summary']),
                      r'\textbf{Scoped statement alias: ' + tx('HNM-T-' + contribution['legacy_id']) + r'.} The admission and its limits are in Section~\ref{stmt:' + contribution['legacy_id'] + '}.',
                      r'\textbf{Status and scope.} ' + tx(contribution['status']) + '. ' + prose(contribution['limitation'])]
    additions += [r'\subsection{Round30 equation concordance}', r'\begingroup\footnotesize\setlength{\tabcolsep}{3pt}',
                  r'\begin{longtable}{@{}p{41mm}p{32mm}p{78mm}@{}}',
                  r'\toprule Stable equation alias & Printed locator & Frozen derivation\\\midrule\endhead']
    for equation in registry['equations']:
        if not equation['id'].startswith('HNM-E-R30-'):
            continue
        additions.append(tx(equation['id']) + ' & ' + r'\ref{' + equation['legacy_label'] + '} & ' + r'\repo{' + equation['source_path'] + '}' + r'\\\addlinespace')
    additions += [r'\bottomrule\end{longtable}\endgroup', r'\subsection{Round30 quantity aliases}']
    for quantity in registry['quantities']:
        if quantity.get('round') == 30:
            additions += [r'\paragraph{' + tx(quantity['id']) + '} ' + tx(quantity['display_name']) + r': $' + quantity['symbol'] + r'$. ' + tx(quantity['units']) + '. ' + tx(quantity['limitation'])]
    (OUT / 'sections/naming-appendix.tex').write_text((PREVIOUS / 'sections/naming-appendix.tex').read_text() + '\n' + '\n'.join(additions) + '\n')
    readme = (PREVIOUS / 'registry/README.md').read_text() + '\n## Round30 additive records\n\n'
    for contribution in registry['contributions']:
        if contribution.get('round') == 30:
            readme += f"- {contribution['id']}: {contribution['display_name']} ({contribution['status']}).\n"
    readme += '\nBoth directions receive separate equation aliases; there are exactly three Round30 contribution records, not one discovery per equation. No new axioms.\n'
    (OUT / 'registry/README.md').write_text(readme)

def append_contribution_catalog(registry):
    text = (PREVIOUS / 'sections/contribution-appendix.tex').read_text()
    text += '\n' + r'\subsection{Round30 additions to the complete catalog}' + '\n'
    text += r'The inherited rows above preserve their original gates. The current same-state AT1 extension is separately reviewed and is not a retroactive change to AO or AQ. These three additional records complete the current catalog; their equation aliases do not add further discoveries.' + '\n'
    for item in registry['contributions']:
        if item.get('round') != 30:
            continue
        text += '\n' + r'\paragraph{' + tx(item['id']) + ': ' + tx(item['display_name']) + '} ' + summary_latex(item['legacy_id'], item['summary']) + '\n'
        text += r'\textbf{Application.} ' + tx(item.get('editorial_application', item['application'])) + '\n'
        text += r'\textbf{Surviving limitations.} ' + prose(item['limitation']) + '\n'
        text += r'\textbf{Evidence.} Section~\ref{stmt:' + item['legacy_id'] + '}; ' + r'\repo{' + item['source_paths'][0] + '}\n'
    (OUT / 'sections/contribution-appendix.tex').write_text(text)

def annotate_carried_scopes():
    note = (r'\begin{quote}\small\textbf{Draft03 current extension: HNM-C-AT1.} '
            r'The statements and future goals below retain their Round29 admission date. '
            r'Round30 separately proves the original Wilson operator domain and energy-moment certificate in the actual AQ state; see Section~\ref{stmt:AT1}. '
            r'This fresh seven-star proof has second-moment ceiling $\alpha^2(36+98|\tau|)$ and does not identify AQ with AO or replace the earlier orthant coefficient. '
            r'Historical statements that the AQ moment theorem is missing are superseded only by that new scoped gate.\end{quote}' + '\n\n')
    for name in ['addenda/round29/aq2.tex', 'sections/round29-closeout.tex']:
        text = (PREVIOUS / name).read_text()
        split = text.find('\n\n')
        require(split >= 0, f'Expected introductory paragraph in {name}')
        (OUT / name).write_text(text[:split + 2] + note + text[split + 2:])

def write_priority(registry):
    by_id = {x['id']: x for x in registry['contributions']}
    current = [x for x in registry['contributions'] if x.get('round') == 30]
    order = ['HNM-C-AQ2', 'HNM-C-AM2'] + [x['id'] for x in current] + ['HNM-C-RECENT25', 'HNM-C-AL1', 'HNM-C-AO2', 'HNM-C-EARLY10', 'HNM-C-AH2']
    rationale = {
        'HNM-C-AQ2': 'Supplies the fixed-lattice physical representation, positive gap and original Wilson witness used by the current spectral continuation.',
        'HNM-C-AM2': 'The complete finite-volume numerical stability premise underlies that representation; the bound is uniform over its declared volumes.',
        'HNM-C-RECENT25': 'Identifies a critical growing-time failure of a tempting limit interchange in the separate canonical model.',
        'HNM-C-AL1': 'Prevents the existing small-interaction theorem from being mistaken for a weak-coupling continuum strategy.',
        'HNM-C-AO2': 'Provides the earlier-state moment proof pattern while preserving the state distinction.',
        'HNM-C-EARLY10': 'Shows what a full representation-space enclosure requires beyond finite diagonalization.',
        'HNM-C-AH2': 'Provides a finite-graph omitted-channel heat certificate; evaluated output remains a separate deliverable.'}
    rationale.update({
        'HNM-C-AT1': 'Closes the domain and moment gap for the actual numerical-cap AQ state, enabling the next two spectral certificates without identifying distinct states.',
        'HNM-C-AT2': 'Turns actual-state moment information into a nonzero finite-window mass guarantee and rigorous inverse-energy bounds while exposing non-identification.',
        'HNM-C-AT3': 'Supplies a conditional finite-data protocol after moment ambiguity; abstract benchmark success remains separate from producing actual AQ samples.'})
    rows = [r'\section{Current priority-ranked results and their limits}', r'\label{app:priority}',
            r'This qualitative ranking emphasizes dependencies and usable conclusions for the current route. It is neither a scientific-priority judgment nor a percentage of continuum Yang--Mills solved. The old gate limitations are preserved in the full catalog; a separately gated current extension is shown beside the earlier result. Recency and equation counts are not ranking criteria.',
            r'\begingroup\small\setlength{\tabcolsep}{3pt}', r'\begin{longtable}{@{}p{10mm}p{38mm}p{54mm}p{51mm}@{}}',
            r'\toprule Rank & Hruday record & Why useful & Scope / surviving limit\\\midrule\endhead']
    short_limits = {
        'HNM-C-AQ2': 'Chosen GNS representation only; no all-state uniqueness, boundary identification, particle pole or continuum construction. AT1 separately supplies same-state domain/moment control.',
        'HNM-C-AM2': 'Fixed-spacing complete-factor model; no weak-bare-coupling bridge or evaluated general boundary constant.',
        'HNM-C-RECENT25': 'Existential probe and growing clock; separate canonical model and same-author historical review.',
        'HNM-C-AL1': 'Obstruction to the sufficient theorem, not a no-gap theorem.',
        'HNM-C-AO2': 'Original orthant state and smallness range; no AO/AQ state equality.',
        'HNM-C-EARLY10': 'Finite graph; continuum matching remains open.',
        'HNM-C-AH2': 'Finite generated span; not an evaluated 561-coordinate heat vector or continuum certificate.'}
    for item in registry['contributions']:
        if item.get('priority') is not None:
            item['historical_priority'] = item['priority']
        item['priority'] = None
    for rank, cid in enumerate(order, 1):
        item = by_id[cid]
        reason = item.get('priority_rationale') or rationale[cid]
        item['priority'] = rank
        item['priority_rationale'] = reason
        limit = short_limits.get(cid, item['limitation'])
        rows.append(str(rank) + ' & ' + r'\textbf{' + tx(cid) + '} ' + tx(item['display_name']) + ' & ' + prose(reason) + ' & ' + prose(limit) + r'\\\addlinespace')
    rows += [r'\bottomrule\end{longtable}\endgroup']
    (OUT / 'sections/priority-appendix.tex').write_text('\n'.join(rows) + '\n')

def main():
    findings_path = ROUND / 'advisor/findings.json'
    require(findings_path.exists(), 'Final three-loop findings are required before integration.')
    findings = json.loads(findings_path.read_text())
    loops = sorted(findings['loops'], key=lambda item: item['sequence'])
    require(len(loops) == 3 and len({x['id'] for x in loops}) == 3, 'Exactly three distinct reviewed loops required.')
    require([x['sequence'] for x in loops] == [1, 2, 3], 'Expected completed sequences 1, 2, 3.')
    roadmap_path = ROUND / 'advisor/roadmap.json'
    require(roadmap_path.exists(), 'Post-cycle roadmap is required.')
    registry = json.loads((PREVIOUS / 'registry/hnm-registry.json').read_text())
    registry['edition'] = 'Draft03 through three Round30 investigations'
    inputs = {str(findings_path.relative_to(ROOT)): sha(findings_path), str(roadmap_path.relative_to(ROOT)): sha(roadmap_path),
              'papers/draft-02/registry/hnm-registry.json': sha(PREVIOUS / 'registry/hnm-registry.json')}
    destination = OUT / 'addenda/round30'
    destination.mkdir(parents=True, exist_ok=True)
    chapter = [r'\section{Round30: three adaptive investigations}', r'\label{sec:round30-overview}',
               r'Human author: \textbf{Hruday N M (BUNZEEY)}. This cycle contains exactly three reviewed investigations. AT1 was selected from the inherited roadmap; the later contracts were selected only after the preceding evidence and skeptical feedback. Source research, replay, editorial integration and publication do not count as extra investigations.',
               r'The current conclusions concern the original Wilson observable in the numerical-cap AQ state. HNM names identify this specific contribution record. Earlier eponyms, authors, physical symbols and frozen evidence remain intact. The three contributions and their separate equation aliases are not three proofs of continuum Yang--Mills.',
               r'\input{sections/round30-sources}']
    for entry in loops:
        rid = entry['id'].upper()
        lid = rid.lower()
        evidence = entry['evidence'] if isinstance(entry['evidence'], list) else [entry['evidence']]
        gates = [name for name in evidence if name.endswith('-gate.json')]
        require(len(gates) == 1, f'Expected exactly one reviewed gate for {rid}')
        gate_name = gates[0]
        gate_path = ROOT / gate_name
        gate = json.loads(gate_path.read_text())
        require('bindings' in gate and gate['bindings'], f'Missing source bindings for {rid}')
        for name, digest in gate['bindings'].items():
            path = ROOT / name
            require(path.exists() and sha(path) == digest, f'Source binding mismatch: {name}')
        inputs[str(gate_path.relative_to(ROOT))] = sha(gate_path)
        paths = [gate_name]
        for direction in ['forward', 'reverse']:
            path = ROUND / direction / lid / 'report.md'
            require(path.exists(), f'Missing {path}')
            inputs[str(path.relative_to(ROOT))] = sha(path)
            paths.append(str(path.relative_to(ROOT)))
            (destination / f'{lid}-{direction}.tex').write_text(render_report(path, entry, direction, registry))
        review_path = ROUND / 'skeptic' / f'{lid}.md'
        require(review_path.exists(), f'Missing skeptical review {review_path}')
        inputs[str(review_path.relative_to(ROOT))] = sha(review_path)
        paths.append(str(review_path.relative_to(ROOT)))
        title = entry['title'].removeprefix('HNM ').removeprefix('Hruday ')
        limits = entry['limitations']
        if isinstance(limits, str):
            limits = [limits]
        contribution = dict(id='HNM-C-' + rid, legacy_id=rid, legacy_title=entry['title'], title=title,
                            display_name='Hruday ' + title, round=30, source_rounds=[30], status=entry['status'],
                            classification=entry.get('classification', 'model-specific application of established mathematics'),
                            equation_labels=[x['legacy_label'] for x in registry['equations'] if x.get('contribution_ids') == ['HNM-C-' + rid]],
                            source_paths=paths, application=entry['accepted'], summary=entry['accepted'], limitation=' '.join(limits),
                            next=gate.get('decision', 'See the post-cycle roadmap.'), source_status=entry['status'], proof_status=entry['status'],
                            priority=None, priority_status='Unverified scientific priority; HNM is a project record alias.',
                            statement_ids=['HNM-T-' + rid], current_extensions=[], priority_rationale=entry.get('priority_rationale', ''))
        contribution['editorial_application'] = ' '.join(entry.get('applications', [entry['accepted']]))
        registry['contributions'].append(contribution)
        registry['statements'].append(dict(id='HNM-T-' + rid, type='scoped proposition and certificate', contribution_id='HNM-C-' + rid,
                                          legacy_id=rid, title=contribution['display_name'], summary=entry['accepted'], scope=' '.join(limits),
                                          status=entry['status'], source_paths=paths, gate=gate_name, manuscript_label='stmt:' + rid,
                                          priority_status='Project statement alias; not a claim of invented general mathematics.'))
        chapter += [r'\clearpage\section{Hruday ' + rid + ': reviewed admission}', r'\label{stmt:' + rid + '}',
                    r'\textbf{Verdict: ' + tx(entry['status'].replace('_', ' ')) + '.} ' + summary_latex(rid, entry['accepted']),
                    r'\subsection*{Limits and independent review}',
                    r'The producer reports were frozen separately before exchange. Their common ancestry, contract and inherited methods remain disclosed. The skeptic reviewed both proofs and executed controls; this does not constitute external human peer review.',
                    r'\begin{itemize}']
        chapter += [r'\item ' + prose(limit) for limit in limits]
        chapter += [r'\end{itemize}', r'\repo{' + gate_name + '}', r'\par\repo{' + str(review_path.relative_to(ROOT)) + '}']
        differences = entry.get('reverse_differences', [])
        if isinstance(differences, str):
            differences = [differences]
        if differences:
            chapter += [r'\subsection*{Substantive directional differences}', r'\begin{itemize}']
            chapter += [r'\item ' + prose(x) for x in differences]
            chapter += [r'\end{itemize}']
        else:
            chapter += [r'The following complete reverse derivation preserves its different organization and countercontrols, rather than treating repeated code execution as independent evidence. The shared gate governs both directions; source-specific refinements remain attributed.']
        if rid == 'AT3':
            chapter += [r'\subsection*{The two reusable input domains}',
                        r'The forward \repo{evaluator.py} accepts exact rational sample values or enclosing pairs. Wider arithmetic bins still yield a conditional enclosing interval, but can fail its width verdict. The reverse \repo{check.py} evaluator requires enclosing pairs, arithmetic width at most $10^{-12}$, and its additional mass/error envelope checks; its CSV route also validates the complete time grid. These are different admitted API domains, not interchangeable promises.',
                        r'For both APIs, callers must establish centering, the actual AQ state/model provenance and the deterministic sample-error premise. Syntax checks cannot certify those physical conditions. The executed CSV data are synthetic A/B controls, and no actual AQ correlation samples or response value are supplied.']
        figure_names = {'AT2': 'hnm-spectral-certificates.pdf', 'AT3': 'hnm-euclidean-readout.pdf'}
        figure_captions = {
            'AT2': 'Hruday spectral-certificate summary. Bounds use the actual AQ moment constraints. The equal-moment spectra are abstract controls illustrating non-identification of a unique spectral response; none is asserted to be the AQ spectrum. All displayed bounds retain the fixed-lattice gate assumptions.',
            'AT3': 'Hruday conditional Euclidean readout protocol and abstract-control demonstration. The fixed sampling grid and error allowances are protocol choices. The figure supplies no computed or measured AQ Euclidean samples and identifies no particle pole.'}
        if rid in figure_names:
            figure_name = figure_names[rid]
            source_figure = ROUND / 'figures' / figure_name
            require(source_figure.exists(), f'Final reviewed figure required: {source_figure}')
            shutil.copy2(source_figure, OUT / 'figures' / figure_name)
            inputs[str(source_figure.relative_to(ROOT))] = sha(source_figure)
            caption_name = 'captions.json' if rid == 'AT2' else 'euclidean-caption.json'
            caption_path = ROUND / 'figures' / caption_name
            require(caption_path.exists(), f'Final figure caption required: {caption_path}')
            caption = json.loads(caption_path.read_text())
            inputs[str(caption_path.relative_to(ROOT))] = sha(caption_path)
            require(caption['source'] == gate_name or caption['source'] in gate['bindings'], f'Figure must cite {rid} gate or gate-bound output')
            require(caption.get('gate_sha256') == sha(gate_path), f'Figure must bind the {rid} gate')
            if caption['source'] != gate_name:
                require(caption.get('source_sha256') == sha(ROOT / caption['source']), f'Figure source digest mismatch for {rid}')
                inputs[caption['source']] = sha(ROOT / caption['source'])
            figure_captions[rid] = tx(caption['caption'] + ' ' + caption.get('curve_accuracy', ''))
            chapter += [r'\clearpage\begin{figure}[p]\centering',
                        r'\includegraphics[width=\textwidth,height=.78\textheight,keepaspectratio]{figures/' + figure_name + '}',
                        r'\caption{' + figure_captions[rid] + r'}\label{fig:r30-' + lid + '}', r'\end{figure}\clearpage']
        chapter += [r'\clearpage\input{addenda/round30/' + lid + '-forward}', r'\clearpage\input{addenda/round30/' + lid + '-reverse}']
    # Historical limitations retain their exact words, with separate current extensions.
    current = {x['legacy_id']: x for x in registry['contributions'] if x.get('round') == 30}
    if 'AT1' in current:
        for item in registry['contributions']:
            if item['id'] in {'HNM-C-AQ2', 'HNM-C-AO2'}:
                item.setdefault('current_extensions', []).append({
                    'id': 'HNM-C-AT1', 'title': current['AT1']['display_name'], 'summary': current['AT1']['summary'],
                    'source_paths': current['AT1']['source_paths'],
                    'relation': 'Fresh same-AQ-state proof; AO remains method ancestry and no state-identification claim is made.'})
    registry['quantities'].extend([
        dict(id='HNM-Q-AT1-AQ-SECOND-MOMENT', symbol=r'B_2=\alpha^2(36+98|\tau|)', display_name='Hruday AQ Wilson second-moment ceiling', units='energy squared', limitation='Ceiling, not an equality or second-moment convergence theorem.', round=30),
        dict(id='HNM-Q-AT1-AQ-FIRST-MOMENT', symbol=r'\mu_1=\alpha\omega_{\rm num}(1-W^2)', display_name='Hruday AQ Wilson first-energy identity', units='energy', limitation='Same chosen numerical-cap state; no identification with AO.', round=30),
        dict(id='HNM-Q-R30-SPECTRAL-MASS', symbol=r's=q-w^2', display_name='Hruday centered Wilson spectral mass registry', units='dimensionless', limitation='q and w are actual state expectations; not reference values.', round=30),
        dict(id='HNM-Q-R30-INVERSE-ENERGY', symbol=r'R=\int E^{-1}\,d\nu(E)', display_name='Hruday inverse-energy Wilson functional', units='inverse energy', limitation='A spectral functional; a perturbed-state susceptibility requires additional differentiability.', round=30),
        dict(id='HNM-Q-AT2-WINDOW-CHOICE', symbol=r'L=8', display_name='Hruday window-certificate design choice', units='dimensionless energy cutoff x=E/alpha', limitation='Proof choice; L alpha is the physical upper endpoint. Neither an eigenvalue nor a new physical constant.', round=30, kind='proof_choice'),
        dict(id='HNM-Q-AT2-TANGENT-CHOICE', symbol=r'c=3', display_name='Hruday reciprocal-minorant tangent choice', units='dimensionless energy coordinate', limitation='Chosen certificate parameter; no optimizer or physical-pole interpretation.', round=30, kind='proof_choice'),
        dict(id='HNM-Q-AT2-MAJORANT-CHOICE', symbol=r'b=49', display_name='Hruday reciprocal-majorant factor choice', units='dimensionless energy coordinate', limitation='Chosen polynomial factor parameter; no optimizer or physical-pole interpretation.', round=30, kind='proof_choice'),
        dict(id='HNM-Q-AT3-EUCLIDEAN-HORIZON', symbol=r'T=128', display_name='Hruday Euclidean readout horizon choice', units='dimensionless Euclidean coordinate conjugate to x=E/alpha', limitation='Protocol design parameter; physical Euclidean duration is hbar T/alpha. No real-time observation or measured AQ data is supplied.', round=30, kind='design_variable'),
        dict(id='HNM-Q-AT3-EUCLIDEAN-STEP', symbol=r'h=1/32', display_name='Hruday Euclidean readout grid step', units='dimensionless Euclidean coordinate', limitation='Protocol design parameter; not Planck constant, lattice spacing or a new dynamics clock.', round=30, kind='design_variable'),
        dict(id='HNM-Q-AT3-INTERVAL-COUNT', symbol=r'N=4096', display_name='Hruday Euclidean readout interval count', units='dimensionless integer count', limitation='N grid intervals and N+1 sample locations; a design count rather than degrees of freedom in the AQ Hamiltonian.', round=30, kind='design_variable'),
        dict(id='HNM-Q-AT3-SAMPLE-ALLOWANCE', symbol=r'\varepsilon=10^{-6}', display_name='Hruday Euclidean sample-error allowance', units='dimensionless correlation amplitude', limitation='Deterministic per-sample absolute error assumption, not measured uncertainty, a confidence interval or a claimed capability to produce AQ samples.', round=30, kind='data_error_allowance'),
        dict(id='HNM-Q-AT3-QUADRATURE-ALLOWANCE', symbol=r'Q=h^2u_{\rm up}/8=47/512000', display_name='Hruday integrated-curvature quadrature allowance', units='dimensionless inverse-energy functional I=alpha R', limitation='Certified one-sided quadrature allowance, not an observed integration error or a new quadrature method.', round=30, kind='proof_budget'),
        dict(id='HNM-Q-AT3-TAIL-ALLOWANCE', symbol=r'D=(504/125)e^{-8}', display_name='Hruday omitted-Euclidean-tail allowance', units='dimensionless inverse-energy functional I=alpha R', limitation='Uniform upper bound for the unobserved tail; rational arithmetic must enclose the exponential outward.', round=30, kind='proof_budget'),
        dict(id='HNM-Q-AT3-NOISE-ALLOWANCE', symbol=r'J=T\varepsilon=2/15625', display_name='Hruday deterministic readout-error allowance', units='dimensionless inverse-energy functional I=alpha R', limitation='Worst-case signed weighted error; not a root-sample-count stochastic uncertainty.', round=30, kind='proof_budget'),
        dict(id='HNM-Q-AT3-ARITHMETIC-GRID', symbol=r'G=10^{30}\ \text{(forward)},\quad D=10^{30}\ \text{(reverse)}', display_name='Hruday directed-rational arithmetic grid choice', units='dimensionless integer denominator', limitation='Implementation design, distinct from the forward tail allowance also denoted D; the source-local symbols remain unchanged.', round=30, kind='implementation_choice'),
        dict(id='HNM-Q-AT3-REVERSE-BIN-ALLOWANCE', symbol=r'10^{-12}', display_name='Hruday reverse-API arithmetic-bin width allowance', units='dimensionless correlation amplitude', limitation='Reverse API input restriction. Forward API permits wider bins and returns the resulting interval-width verdict; the two domains are not asserted equal.', round=30, kind='data_representation_allowance'),
    ])
    roadmap = json.loads(roadmap_path.read_text())
    calculator_source = ROUND / 'calculators/spectral_certificate.py'
    require(calculator_source.exists(), 'Reviewed spectral calculator is required')
    shutil.copy2(calculator_source, OUT / 'calculators/hnm_round30.py')
    inputs[str(calculator_source.relative_to(ROOT))] = sha(calculator_source)
    chapter += [r'\clearpage\section{Round30 closeout and next unexecuted goals}', r'\label{sec:r30-closeout}',
                r'All three investigations in this cycle have recorded reviews. The complete evidence and current next-step plan are the source-bound machine-readable records below. A selected next goal is not an executed fourth investigation.',
                r'\repo{research/round30/advisor/findings.json}', r'\par\repo{research/round30/advisor/roadmap.json}']
    chapter += [r'\subsection*{Exact certificate calculator}',
                r'The standalone calculator below evaluates the admitted AT2 window and inverse-energy bounds with rational arithmetic. It requires positive energy coefficient $\alpha$ and $|\tau|\le10^{-8}$; those validations do not enlarge the theorem range. It returns a bound on the actual unknown response, not a sampled AQ spectrum or an identified susceptibility.',
                r'\begin{verbatim}' + '\npython3 calculators/hnm_round30.py --alpha 1 --tau 1/100000000\n' + r'\end{verbatim}',
                r'The command is relative to the unpacked manuscript directory. The source-bound repository original is \repo{research/round30/calculators/spectral_certificate.py}.']
    for goal in roadmap.get('goals', []):
        chapter += [r'\paragraph{' + tx(str(goal.get('id', 'Goal'))) + ': ' + tx(goal.get('title', '')) + '} ' + prose(goal.get('target', goal.get('question', ''))),
                    r'\textbf{Status.} ' + tx(goal.get('status', 'planned, not executed')) + '. ' + prose(goal.get('missing_premise', ''))]
        for key, title in [('proposed_first_loop_test', 'First prospective test'), ('second_loop_rule', 'Adaptive follow-up rule'), ('exact_model', 'Exact model boundary'), ('reason_for_rank', 'Reason for rank')]:
            if goal.get(key):
                chapter += [r'\textbf{' + title + '.} ' + prose(goal[key])]
    chapter += [r'\subsection*{Attribution and reproducibility}',
                r'Hruday N M (BUNZEEY) is the human project author. AI systems assisted source retrieval, derivation, implementation and review. The result is a source-qualified research record, not an externally peer-reviewed paper or arXiv acceptance. General moment methods and operator constructions retain their original authors. No new axioms are asserted.',
                r'\repo{research/round30/reproduce.py}', r'\par\repo{papers/draft-03/build.py}']
    (OUT / 'sections/round30.tex').write_text('\n\n'.join(chapter) + '\n')
    write_sources()
    append_bibliography()
    append_names(registry)
    append_contribution_catalog(registry)
    annotate_carried_scopes()
    write_priority(registry)
    registry['contribution_count'] = len(registry['contributions'])
    for field in ['contributions', 'equations', 'quantities', 'statements']:
        ids = [x['id'] for x in registry[field]]
        require(len(ids) == len(set(ids)), f'Duplicate {field} IDs')
    dump(OUT / 'registry/hnm-registry.json', registry)
    for lens in ['modern', 'historical']:
        name = f'research/round30/experts/{lens}/sources.json'
        inputs[name] = sha(ROOT / name)
    name = 'research/round30/editorial/method-source-addendum.json'
    inputs[name] = sha(ROOT / name)
    dump(OUT / 'round30-inputs.json', {'schema': 'hnm-draft03-inputs-v1', 'admitted_loops': [x['id'] for x in loops], 'sha256': inputs,
                                     'scope': 'Current three-loop gate, report, review and literature bindings; inherited evidence remains historical.'})
    print(json.dumps({'loops': [x['id'] for x in loops], 'contributions': len(registry['contributions']), 'equations': len(registry['equations'])}))

if __name__ == '__main__':
    main()
