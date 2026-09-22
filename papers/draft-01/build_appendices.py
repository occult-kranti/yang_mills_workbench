#!/usr/bin/env python3
"""Build the full historical appendix from the pinned, existing research ledger."""
from pathlib import Path
import argparse, collections, hashlib, json, re

HERE = Path(__file__).resolve().parent
PIN = '40960f39a3dcaa6b2735d47adaa0e3b40e6a0f02'

def tex(s):
    s = str(s)
    replace = {'–':'--','—':'---','−':'-', '→':' -> ', '←':' <- ',
       '↔':' <-> ', '≈':' approximately ', '≤':' <= ', '≥':' >= ',
       '≠':' not equal ', '∞':' infinity ', '∈':' in ', '⊂':' subset ',
       '∑':' sum ', '∏':' product ', '∫':' integral ', '√':' sqrt ',
       '²':' squared ', '³':' cubed ', '¹':'1', '⁰':'0', '⁻':'-',
       '×':' x ', '·':' / ', 'δ':'delta','Δ':'Delta','α':'alpha',
       'β':'beta','γ':'gamma','η':'eta','θ':'theta','κ':'kappa',
       'λ':'lambda','μ':'mu','π':'pi','σ':'sigma','τ':'tau',
       'Ω':'Omega','ε':'epsilon','χ':'chi','ϕ':'phi','φ':'phi',
       'ℏ':'hbar','₀':'0','₁':'1','₂':'2','₃':'3','₄':'4','₅':'5',
       '₆':'6','₇':'7','₈':'8','₉':'9','₊':'+', '“':'``','”':"''",
       '’':"'", '‘':"'", '…':'...', '∥':'||', '±':' plus/minus ',
       'Θ':'Theta','Σ':'Sigma','ρ':'rho','ψ':'psi','ᵗ':' transpose ',
       '′':"'", '⁴':' fourth ', '⁵':' fifth ', '⁶':' sixth ',
       'ⁿ':' power-n ', '⟨':'<', '⟩':'>'}
    for a,b in replace.items(): s=s.replace(a,b)
    escapes = {'\\':r'\textbackslash{}','&':r'\&','%':r'\%', '$':r'\$',
       '#':r'\#','_':r'\_','{':r'\{','}':r'\}','~':r'\textasciitilde{}',
       '^':r'\textasciicircum{}'}
    s=''.join(escapes.get(c,c) for c in s)
    return s

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True)
    args=ap.parse_args(); root=args.repo.resolve()
    old=json.loads((root/'research/round25/all-results.json').read_text())
    nodes=json.loads((root/'research/round26/network.json').read_text())['nodes']
    rows=[]
    for rnd in old['rounds']:
        for run in rnd['runs']:
            rows.append({'record_id':f"r{rnd['round']}-{run['id']}",
              'round':rnd['round'], 'run':run['id'], 'title':run['title'],
              'kind':run['kind'], 'historical_verdict':run['verdict'],
              'finding':run['bullets'][0], 'boundary':' '.join(run['bullets'][1:]),
              'source_paths':run['sources'],
              'fresh_audit':'See contribution and skeptic ledgers; historical status is not a fresh proof.'})
    for node in nodes:
        if node['kind']!='loop':continue
        rows.append({'record_id':'r26-'+node['id'], 'round':26, 'run':node['id'],
          'title':node['title'], 'kind':'physics_loop',
          'historical_verdict':node['status'], 'finding':node['summary'],
          'boundary':node['detail'], 'source_paths':node['sources'],
          'fresh_audit':'Full pre-manuscript release replay; selective independent manuscript stress checks.'})
    assert len(rows)==121
    assert len({x['record_id'] for x in rows})==121
    assert sum(x['kind']=='physics_loop' for x in rows)==86
    sources={}
    for row in rows:
        for rel in row['source_paths']:
            p=(root/rel).resolve()
            if not p.is_relative_to(root) or not p.is_file():
                raise ValueError('Missing or unsafe source '+rel)
            sources[rel]=hashlib.sha256(p.read_bytes()).hexdigest()
    data={'source_commit':PIN,'scope':'121 historical records; not 121 claimed discoveries',
      'counts':{'entries':len(rows),'rounds':24,'explicit_loops':86},
      'entries':rows,'source_sha256':sources}
    (HERE/'audit/history-ledger.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    out=[r'\section{Complete historical record}',r'\label{app:history}',
       'This table preserves all 121 recorded study or loop entries. It is an index of the history, not a list of 121 new discoveries. Historical verdicts retain their original scope. The contribution and skeptic ledgers identify the fresh manuscript checks; inclusion here does not claim that every old production simulation was rerun. Complete source paths and SHA-256 bindings are in '+r'\repo{audit/history-ledger.json}'+'.',
       r'\begingroup\footnotesize\setlength{\tabcolsep}{4pt}\renewcommand{\arraystretch}{1.14}',
       r'\begin{longtable}{@{}p{.16\textwidth}p{.40\textwidth}p{.40\textwidth}@{}}',
       r'\caption{All recorded entries, grouped by round.}\label{tab:all-history}\\',
       r'\toprule Record & Historical entry & Verdict and first source \\ \midrule\endfirsthead',
       r'\toprule Record & Historical entry & Verdict and first source \\ \midrule\endhead',
       r'\midrule\multicolumn{3}{r}{Continued on next page}\\\endfoot',
       r'\bottomrule\endlastfoot']
    for row in rows:
        a='R'+str(row['round'])+r'\par '+tex(row['run'].upper())
        b=r'\textbf{'+tex(row['title'])+r'}'
        c=tex(row['historical_verdict'])
        c+=r'\par\repo{'+row['source_paths'][0]+'}'
        out.append(a+' & '+b+' & '+c+r' \\ \addlinespace')
    out += [r'\end{longtable}\endgroup']
    (HERE/'sections/history-appendix.tex').write_text('\n'.join(out)+'\n')
    print(json.dumps({'entries':len(rows),'sources':len(sources),'rounds':dict(collections.Counter(x['round'] for x in rows))}))

if __name__=='__main__':main()
