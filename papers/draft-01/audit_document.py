#!/usr/bin/env python3
"""Structural manuscript checks; this script is not a mathematical proof checker."""
from pathlib import Path
import argparse, collections, hashlib, json,re,subprocess
ROOT=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);a=ap.parse_args()
    files=[ROOT/'main.tex']+list((ROOT/'sections').glob('*.tex'))+[ROOT/'sources/related-work.tex']
    text='\n'.join(p.read_text() for p in files)
    labs=re.findall(r'\\label\{([^}]+)\}',text)
    duplicates=[k for k,v in collections.Counter(labs).items() if v>1]
    refs=re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',text)
    missingrefs=sorted(set(refs)-set(labs))
    bib=(ROOT/'sources/references.bib').read_text()
    keys=set(re.findall(r'@\w+\{([^,]+),',bib))
    citations=[]
    for cite in re.findall(r'\\cite(?:\[[^]]*\])?\{([^}]+)\}',text):citations+=cite.split(',')
    missingcites=sorted(set(citations)-keys)
    inputs=re.findall(r'\\input\{([^}]+)\}',text)
    missinginputs=[x for x in inputs if not (ROOT/(x+'.tex')).is_file()]
    figures=re.findall(r'\\includegraphics(?:\[[^]]*\])?\{([^}]+)\}',text)
    missingfigures=[x for x in figures if not (ROOT/x).is_file()]
    history=json.loads((ROOT/'audit/history-ledger.json').read_text())
    missing_sources=[];changed_sources=[]
    for rel,expected in history['source_sha256'].items():
        p=a.repo/rel
        if not p.is_file():missing_sources.append(rel)
        elif hashlib.sha256(p.read_bytes()).hexdigest()!=expected:changed_sources.append(rel)
    checks={'unique_labels':not duplicates,'references_resolve':not missingrefs,
      'citations_resolve':not missingcites,'inputs_exist':not missinginputs,'figures_exist':not missingfigures,
      'history_121':len(history['entries'])==121,'loops_86':sum(x['kind']=='physics_loop' for x in history['entries'])==86,
      'source_paths_exist':not missing_sources,'historical_sources_unchanged':not changed_sources,
      'no_unnumbered_star_tags':r'\tag*{\workstar}' not in text,
      'no_unexpected_control_characters':not any(ord(c)<32 and c not in '\n\r\t' for c in text)}
    result={'scope':'Document integrity, cross-reference and source-byte checks only; not formal proof verification',
     'status':'passed' if all(checks.values()) else 'failed','checks':checks,
     'counts':{'labels':len(labs),'references':len(refs),'bibliography_entries':len(keys),'cited_entries':len(set(citations)),
       'figures':len(figures),'star_markers':text.count(r'\workstar'),'historical_source_files':len(history['source_sha256'])},
     'issues':{'duplicate_labels':duplicates,'missing_references':missingrefs,'missing_citations':missingcites,
       'missing_inputs':missinginputs,'missing_figures':missingfigures,'missing_sources':missing_sources,'changed_sources':changed_sources}}
    (ROOT/'audit/document-integrity.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    if result['status']!='passed':raise SystemExit(1)
if __name__=='__main__':main()
