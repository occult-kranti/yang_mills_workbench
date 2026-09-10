#!/usr/bin/env python3
"""Assemble the readable dossier from the same six accepted page records."""
from pathlib import Path
import json,sys
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'advisor'))
from freeze_gate import verify

def main():
    data=json.loads((HERE/'content.json').read_bytes())
    if [s['id'].lower() for s in data['solutions']]!=['a1','a2','b1','b2','c1','c2']:raise ValueError('Six result records required')
    gates=[verify(HERE/'advisor'/(s['id'].lower()+'-gate.json')) for s in data['solutions']]
    parts=['# Yang–Mills: six-loop research dossier','[Published workbench](https://occult-kranti.github.io/yang_mills_workbench/#research) · [Source repository](https://github.com/occult-kranti/yang_mills_workbench)','Three scientific roles; six sequential loops; two advisory decisions. The second planning decision updated B and C from the completed A1/A2 results. All eight collaboration stages are recorded. This is a set of reviewed conventional finite results, not a claimed solution of the four-dimensional continuum mass-gap problem.',data['summary'],data['open'],'## Evidence and scope','| Loop | Producer checks | Independent checks | Separate comparison checks |\n|---|---:|---:|---:|']
    parts[-1] += "\n"+"\n".join(f"| {g['loop'].upper()} | {g['producer_checks']} | {g['independent_checks']} | {g['comparison_checks']} |" for g in gates)
    parts+=['Normal and optimized executions repeat the same named gates and are counted once. Agreement between two algorithms is paired with their written derivations and discriminating controls. These are agent reviews, not credentialed human peer review.','The Hamiltonian is H=αΣC_e−Σλ_p x_p on the full, untruncated, physical SU(2) link space of the specified finite open graph, with normalized Haar, Casimirj(j+1), all-vertex Gauss law and no external charges. α andλ are energies. Conditional Euclidean coefficientsκ belong to a separately declared static measure.','## Collaboration graph','![Six loops and two advisor decisions](figures/collaboration.svg)']
    for solution in data['solutions']:
        loop=solution['id'].lower()
        parts += ['## '+solution['id']+' — '+solution['title'],solution['plain'],'```text\n'+solution['equation']+'\n```','**Scope:** '+solution['limit']]
        for section in solution['sections']:
            parts += ['### '+section['title'],section['text']]
            if section.get('equation'):parts+=['```text\n'+section['equation']+'\n```']
        if loop=='c1':parts+=['![Actual graph and its outer boundary](figures/four-cubes.png)']
        for plot in solution['plots']:parts+=['![Recorded scientific calculation](figures/'+plot+'.png)']
        parts+=['### Skeptical review',solution['review'],'**Feedback:** '+solution['next'],f'[Frozen contract](advisor/{loop}-contract.md) · [Forward derivation](forward/{loop}/report.md) · [Independent derivation](backward/{loop}/report.md) · [Accepted source inventory](advisor/{loop}-gate.json)']
    parts+=['## Unresolved implications and next cycle',(HERE/'next-roadmap.md').read_text(),'## Source applicability audit',(HERE/'advisor/source-audit.md').read_text(),'## Reproduction','See [README.md](README.md) for local launch, all eighteen scientific execution/comparison programs, the bidirectional dependency replay and build instructions. Exact rational endpoints and complete failure histories are included. The planner is not a formal proof-assistant kernel.','The standalone scientific figures were reviewed separately. Browser layout and keyboard testing remain unverified. This release reviews new scientific code, required source/data comparisons and affected integration; it does not claim a new line-by-line audit of every historical project file.']
    (HERE/'report.md').write_text('\n\n'.join(parts)+'\n')
    print('Six-result dossier assembled from accepted records')
if __name__=='__main__':main()
