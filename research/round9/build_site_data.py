#!/usr/bin/env python3
"""Generate site summaries and plot tables from saved, reviewed evidence."""
from pathlib import Path
import csv
import json
import math
import shutil
from fractions import Fraction

HERE=Path(__file__).resolve().parent
DIST=HERE.parents[1]/'dist'

def read(path):return json.loads((HERE/path).read_text())
def csvread(path):
    with (HERE/path).open() as f:return list(csv.DictReader(f))
def writecsv(name,rows):
    if not rows:raise RuntimeError('empty plot rows '+name)
    with (DIST/name).open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
def series(rows,groups,x,y,groupkey,label):
    result=[]
    for g in groups:
        selected=[r for r in rows if str(r[groupkey])==str(g)]
        points=[[float(r[x]),float(r[y])] for r in selected]
        if not points or not all(math.isfinite(z) for p in points for z in p):raise RuntimeError('invalid plot')
        result.append({'name':label(g),'points':points})
    return result

def build():
    diagnostics=read('lattice/results/all_diagnostics.json')
    rows=[]
    for chain in diagnostics['chains']:
        raw=csvread('lattice/results/'+chain['raw_csv'])
        for k in range(0,len(raw),64):
            block=raw[k:k+64]
            if len(block)!=64:raise RuntimeError('partial unplanned plot block')
            rows.append({'beta':chain['beta'],'start':chain['start'],'chain':str(chain['beta'])+' '+chain['start'],
                         'block_end':k+64,'plaquette_block_mean':sum(float(r['plaquette_mean']) for r in block)/64})
    writecsv('yangmills-lattice.csv',rows)
    plots={'lattice':{'title':'Finite-lattice plaquette histories, 64-sweep averages','xLabel':'Measured sweep (after warmup)','yLabel':'Mean ReTr Up / 2',
        'series':series(rows,['0.5 cold','0.5 hot','2.2 cold','2.2 hot'],'block_end','plaquette_block_mean','chain',str),
        'csv':'/yangmills-lattice.csv','caption':'Actual 2⁴ Wilson chains; block averages are descriptive points, not independent samples or error bars. β=2.2 uncertainty remains insufficient. CSV also includes the β=0 controls.'}}
    raw=csvread('transfer/output/su2_spectra.csv')
    spectrum=[dict(r,log10_beta=math.log10(float(r['beta']))) for r in raw]
    writecsv('yangmills-transfer.csv',spectrum)
    plots['transfer']={'title':'Exact SU(2) rotor energies across coupling','xLabel':'log₁₀ β','yLabel':'Dimensionless −log rⱼ',
       'series':series(spectrum,['0.5','1.0','1.5'],'log10_beta','dimensionless_energy','j',lambda x:'spin j='+x),
       'csv':'/yangmills-transfer.csv','caption':'Exact central-convolution energies from scaled Bessel evaluation, independently checked by Haar integration. These are rotor energies, not 4D glueball masses.'}
    stability=csvread('stability.csv');writecsv('yangmills-stability.csv',stability)
    plots['stability']={'title':'A shared-vacuum transfer-error budget','xLabel':'Physical time step a','yLabel':'Exact lower gap / attained gap',
        'series':series(stability,['1','2'],'a','gap_lower_bound','power',lambda p:'ε=0.2a' if p=='1' else 'ε=0.2a²'),
        'csv':'/yangmills-stability.csv','caption':'Exact two-state positive contractions with a shared vacuum. The reference gap is 1; order-a error can shift its limit to 0.8. This is a conditional-lemma fixture.'}
    fixture=read('advisor/exact_counterexample_results.json')
    normrows=[{'N':r['n'],'operator_norm':float(Fraction(r['operator_norm_exact'])),'product_L1':float(Fraction(r['kernel_product_l1_exact'])),'schur_row':float(Fraction(r['schur_sup_row_exact']))} for r in fixture['markov_kernels']]
    writecsv('yangmills-norm.csv',normrows)
    plots['norm']={'title':'Small average kernel error, persistent operator error','xLabel':'Number of uniform atoms N','yLabel':'Error norm',
        'series':[{'name':name,'points':[[r['N'],r[key]] for r in normrows]} for key,name in [('product_L1','Product-space L¹'),('operator_norm','Operator norm = Schur row bound')]],
        'csv':'/yangmills-norm.csv','caption':'Exact rational Markov-kernel counterexample with c=1/2 and δ=1/4. The average error tends to zero while the operator error stays at 1/4.'}
    documents={key:(HERE/path).read_text() for key,path in {
       'advisor':'advisor/advisor.md','transfer_proof':'transfer/PROOF.md','skeptic':'skeptic/REVIEW.md',
       'lattice_report':'lattice/RESULTS.md','integration':'integration-review.md'}.items()}
    for key,path in {'lattice_tests':'lattice/results/deterministic_checks_current.json','transfer_tests':'transfer/output/validation.json','routes':'proof_results.json'}.items():
        documents[key]=json.dumps(read(path),indent=2)
    independent=read('skeptic/independent_audit.json');theorems=read('skeptic/theorems_and_data_audit.json')
    transfer=read('transfer/output/validation.json');stat=read('stability-validation.json')
    if not independent.get('passed') or not theorems.get('passed') or transfer.get('status')!='passed' or stat.get('status')!='passed':
        raise RuntimeError('Cannot publish passed labels for failed or missing review evidence')
    reports=[{'name':'Lattice deterministic suite','status':'12 groups passed','summary':'Matrix/quaternion checks, local/global action, periodic geometry, gauge/center symmetries and invalid evidence.'},
       {'name':'Transfer implementation','status':str(transfer['check_count'])+' gates passed','summary':'Bessel/Decimal/Haar references, domain boundaries and scaling; scoped to the auxiliary rotor.'},
       {'name':'Independent matrix and Haar audit','status':str(independent['gate_count'])+' gates passed','summary':'Independent complex matrices and high-precision Haar oracle, with repaired source hashes.'},
       {'name':'Independent theorem and raw-data audit','status':str(theorems['count'])+' gates passed','summary':'Held-out matrix counterexamples, Decimal stability and independently recomputed raw chain statistics.'},
       {'name':'Exact rational evaluator','status':str(fixture['executed_gate_count'])+' gates passed in normal and optimized Python','summary':'Counterexamples and explicit acceptance preserved under python -O.'},
       {'name':'Diagonal stability fixtures','status':str(stat['count'])+' gates passed','summary':'Shared vacuum, exact bound saturation, semigroup telescope and rejected insufficient margins.'},
       {'name':'β=2.2 plaquette statistics','status':'INSUFFICIENT','summary':'Autocorrelation estimates exceed the declared threshold; uncertainty and hot/cold comparison are not promoted.'},
       {'name':'Continuum Yang–Mills','status':'OPEN','summary':'No construction or uniform physical gap certificate; finite results have no complete route to the prize target.'}]
    sources=read('advisor/sources.json')
    if isinstance(sources,dict):sources=sources['sources']
    sources.extend([{'title':'NIST DLMF: modified Bessel definitions','url':'https://dlmf.nist.gov/10.25','use':'Power series and normalization for the exact SU(2) benchmark.','depth':'Selected definitions and equations; independent derivation in transfer/PROOF.md.'},
       {'title':'NIST DLMF: integral representations','url':'https://dlmf.nist.gov/10.32','use':'Positive integral representation used in the strict order proof.','depth':'Selected integral identities, not a complete chapter audit.'},
       {'title':'NIST DLMF: large-argument expansions','url':'https://dlmf.nist.gov/10.40','use':'Fixed-spin large-beta asymptotic and continuum-time rotor limit.','depth':'Selected asymptotic formula; uniform-in-spin convergence is not assumed.'}])
    payload={'date':'2026-09-09','plots':plots,'documents':documents,'reports':reports,'sources':sources}
    (DIST/'research-yangmills-data.js').write_text('window.OBSERVATORY_YANGMILLS='+json.dumps(payload,ensure_ascii=False,allow_nan=False,separators=(',',':'))+';\n')
    (HERE/'site_data.json').write_text(json.dumps(payload,ensure_ascii=False,allow_nan=False,indent=2)+'\n')
    shutil.copyfile(HERE/'proof_results.json',DIST/'yangmills-proof-map.json')
    print(json.dumps({'plots':len(plots),'documents':len(documents),'sources':len(sources)}))

if __name__=='__main__':build()
