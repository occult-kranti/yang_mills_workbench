#!/usr/bin/env python3
"""Generate the readable site from exact certificates and recorded histories."""
from pathlib import Path
from fractions import Fraction as F
import csv
import json
import math
import shutil
import hashlib

HERE=Path(__file__).resolve().parent
DIST=HERE.parents[1]/'dist'
def read(rel):return json.loads((HERE/rel).read_text())
def csvread(rel):
    with (HERE/rel).open() as f:return list(csv.DictReader(f))
def writecsv(name,rows):
    if not rows:raise RuntimeError('empty plot data')
    with (DIST/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def textdoc(paths):return '\n\n'.join((HERE/p).read_text() for p in paths)

def build():
    from proof_routes import replay_arithmetic
    replay_arithmetic()
    cs=read('solver/output/stationary_certificates.json');cover=read('solver/output/continuous_range_certificate.json')
    validation=read('solver/output/validation.json');edge=read('solver/output/edge_tests.json');drive=read('solver/output/dynamic_summary.json')
    reports=[]
    for label,rel in [('Independent exact/matrix audit','skeptic/independent_audit.json'),('Independent artifact audit','skeptic/artifact_audit.json'),('Independent acceptance audit','skeptic/acceptance_audit.json'),('Independent proof-wrapper audit','skeptic/proof_audit.json')]:
        r=read(rel)
        if r.get('status')!='passed':raise RuntimeError('Review not passed: '+rel)
        reports.append({'name':label,'status':str(r['check_count'])+' grouped checks passed','scope':r.get('scope_note','See the full independent review for exact source, branch and fixture scope.')})
    if validation.get('status')!='passed' or edge.get('status')!='passed':raise RuntimeError('Producer acceptance not complete')
    reports[:0]=[{'name':'Stationary and driven study','status':str(validation['gate_count'])+' gates passed','scope':'Exact point certificates, continuous coverage, independent radial/Mathieu comparisons and finite numerical evolution.'},
        {'name':'Certificate edge suite','status':str(edge['gate_count'])+' gates passed','scope':'Rational input, scope and precision binding, cutoff/tail conditions and changed certificate controls.'}]
    reports.append({'name':'Continuum Yang–Mills','status':'OPEN','scope':'No many-plaquette volume-uniform bound, continuum construction or physical mass-gap certificate.'})
    nodes=[];active=False
    for line in (HERE/'advisor/advisor.md').read_text().splitlines():
        if line.startswith('## 9.'):active=True;continue
        if active and line.startswith('**Forward'):break
        if active and line.startswith('|') and not line.startswith('| Node') and not line.startswith('|---'):
            values=[p.strip() for p in line.strip('|').split('|')]
            if len(values)==4:nodes.append({'id':f'T{len(nodes)+1:02d}','kind':values[1],'statement':values[0],'relation':'From '+values[2]+'; next: '+values[3]})
    if len(nodes)!=24:raise RuntimeError('Theory inventory changed; review required')
    nodes.append({'id':'T25','kind':'Proved coordinate classification','statement':'Joint trace z records two-loop relative orientation.','relation':'From simultaneous SU(2) conjugation and Gram data; next: the coupled physical kinetic operator and domain.'})
    docs={'advisor':textdoc(['advisor/advisor.md']),'solver':textdoc(['solver/README.md']),'skeptic':textdoc(['skeptic/REVIEW.md']),
        'integration':textdoc(['integration-review.md']),'range':json.dumps(cover,indent=2),
        'routes':json.dumps(read('proof_results.json'),indent=2),
        'checks':json.dumps({'study':validation,'edges':edge},indent=2),
        'drive':json.dumps({'summary':drive,'comparisons':read('solver/output/dynamic_comparisons.json')},indent=2)}
    coordinates=read('skeptic/coordinate_check.json')
    if (coordinates.get('status')!='passed' or coordinates.get('check_count')!=15
        or len(coordinates.get('checks',[]))!=15
        or not all(c.get('passed') is True for c in coordinates['checks'])
        or coordinates.get('source_sha256')!=hashlib.sha256((HERE/'skeptic/coordinate_check.py').read_bytes()).hexdigest()):
        raise RuntimeError('Coordinate review is missing, incomplete or stale')
    docs['coordinates']=textdoc(['skeptic/coordinate-note.md'])+'\n\n'+json.dumps(coordinates,indent=2)
    reports.append({'name':'Two-loop trace coordinates','status':str(coordinates['check_count'])+' separate exact-matrix gates passed','scope':'Domain, conjugation and relative-orientation fixtures; no coupled spectral theorem.'})
    certificates=[];rows=[];best={}
    for i,c in enumerate(cs):
        if F(c['alpha'])!=1:raise RuntimeError('Site certificate study expects normalized alpha=1')
        k=float(F(c['coupling'])/F(c['alpha']));lo=F(c['gap_interval']['lower']);hi=F(c['gap_interval']['upper']);key=f'certificate-{i}'
        docs[key]=json.dumps(c,indent=2)
        certificates.append({'id':str(i),'title':f'α={c["alpha"]}, κ={c["coupling"]}, N={c["N"]}',
          'status':'Positive gap certified' if c['positive_gap_certified'] else 'Enclosure valid; positive lower gap inconclusive',
          'display':f'Approximate gap display: [{float(lo):.14g}, {float(hi):.14g}]\nExact lower: {lo}\nExact upper: {hi}',
          'scope':'One physical SU(2) square, including the infinite character tail. Display decimals do not replace the exact rational endpoints.','document':key})
        row={'kappa':k,'N':c['N'],'gap_lower_display':float(lo),'gap_upper_display':float(hi),'exact_width_as_float':float(hi-lo),'log10_width_display':math.log10(float(hi-lo)),
             'range_lower':float(F(cover['conservative_uniform_gap_lower'])) if 0<=k<=10 else ''}
        rows.append(row)
        if k not in best or c['N']>best[k]['N']:best[k]=row
    writecsv('plaquette-gaps.csv',rows)
    chosen=[best[k] for k in sorted(best) if 0<=k<=10]
    plots={'gap':{'title':'Exact point enclosures and a whole-range bound','xLabel':'κ=λ/α, α=1','yLabel':'Dimensionless plaquette gap',
      'series':[{'name':label,'points':[[r['kappa'],r[key]] for r in chosen]} for key,label in [('gap_lower_display','Point lower enclosure'),('gap_upper_display','Point upper enclosure'),('range_lower','Proved bound for every κ in [0,10]')]],
      'csv':'/plaquette-gaps.csv','caption':'Recorded rational enclosures, displayed as decimals. Connecting point curves are visual guides; the separate Lipschitz coverage proof establishes the continuous-range lower bound.'}}
    tail=[r for r in rows if r['kappa']==100]
    plots['tail']={'title':'How much uncertainty the omitted representations allow','xLabel':'Retained character dimension N','yLabel':'log₁₀ exact enclosure width',
      'series':[{'name':'κ=100','points':[[r['N'],r['log10_width_display']] for r in tail]}],
      'csv':'/plaquette-gaps.csv','caption':'Widths are computed from exact rational endpoint differences before decimal conversion. The coarse N=8 enclosure is valid but wide; a fitted eigenvalue alone would conceal that uncertainty.'}
    hist=csvread('solver/output/dynamic_history.csv');writecsv('plaquette-drive.csv',hist)
    plots['drive']={'title':'Energy supplied by a smooth magnetic-coupling ramp','xLabel':'Time in units α=1','yLabel':'Energy / accumulated work',
      'series':[{'name':name,'points':[[float(r['time']),float(r[key])] for r in hist]} for key,name in [('energy','Measured state energy'),('integrated_work','Independently integrated source work')]],
      'csv':'/plaquette-drive.csv','caption':'Actual finite-Galerkin DOP853 history. Energy and integrated work nearly coincide. The separate tolerance, representation and midpoint-method checks are in the protocol record; no rigorous dynamic-tail enclosure is claimed.'}
    for p in plots.values():
        if not all(s['points'] and all(math.isfinite(v) for point in s['points'] for v in point) for s in p['series']):raise RuntimeError('nonfinite or missing plotted values')
    source=read('advisor/sources.json')['sources']
    sources=[{'title':s['title'],'url':s['url'],'use':s['used_for'],'depth':s['reading_depth']+'. '+s['limitations']} for s in source]
    payload={'date':'2026-09-09','certificates':certificates,'plots':plots,'nodes':nodes,'sources':sources,'reports':reports,'documents':docs,
      'range':{'status':'Certified in the declared one-square model','summary':'An exact rational calculation plus the tail and continuity theorems proves a positive lower gap for every real κ in [0,10], including all omitted representation states.',
        'display':'δ(κ) ≥ '+cover['conservative_uniform_gap_lower']+' = 0.999999\nFor every κ∈[0,10]; α=1\nGeneral scale: Δ(α,λ)≥0.999999 α when λ/α∈[0,10].'},
      'drive':{'summary':drive['protocol']+'. Energy supplied ≈'+format(drive['energy_change'],'.12g')+'; integrated work ≈'+format(drive['integrated_work'],'.12g')+'. N=16→24 state discrepancy ≈'+format(drive['N16_to_N24_state_discrepancy'],'.3g')+'. These are numerical evolution checks, separate from stationary certificates.'}}
    (DIST/'research-plaquette-data.js').write_text('window.OBSERVATORY_PLAQUETTE='+json.dumps(payload,ensure_ascii=False,allow_nan=False,separators=(',',':'))+';\n')
    (HERE/'site_data.json').write_text(json.dumps(payload,ensure_ascii=False,allow_nan=False,indent=2)+'\n')
    shutil.copyfile(HERE/'proof_results.json',DIST/'plaquette-proof-map.json')
    print(json.dumps({'certificates':len(cs),'theory_nodes':len(nodes),'plots':len(plots),'sources':len(sources)}))

if __name__=='__main__':build()
