"""Recorded exact enclosures and separate quadrature/Bessel diagnostics."""
from pathlib import Path
import csv,json,math,hashlib
import numpy as np
from scipy.integrate import quad
from scipy.special import ive
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import moment_bounds as m

HERE=Path(__file__).resolve().parent;OUT=HERE/'output'

def main():
    OUT.mkdir(exist_ok=True);source=m.source_hash();cases=[];rows=[]
    grid=[(k,r) for k in ('1','5','20') for r in range(1,7)]
    grid += [(k,4) for k in ('0','-1/1000','1/1000','-1/100','1/100','-1','-5','-20','-100','100')]
    for k,r in grid:
        c=m.certify(k,r,56)
        if not m.verify(c):raise RuntimeError('Certificate did not replay')
        lo,hi=map(m.F,c['mean_interval']);vl,vu=map(m.F,c['variance_interval']);x=float(m.F(k))
        bessel=float(ive(2,x)/ive(1,x)) if x else 0.
        weight=lambda t:math.exp(x*math.cos(t)-abs(x))*math.sin(t)**2
        z=quad(weight,0,math.pi,epsabs=1e-13,epsrel=1e-13)[0]
        mean=quad(lambda t:math.cos(t)*weight(t),0,math.pi,epsabs=1e-13,epsrel=1e-13)[0]/z
        variance=quad(lambda t:(math.cos(t)-mean)**2*weight(t),0,math.pi,epsabs=1e-13,epsrel=1e-13)[0]/z
        if not all(math.isfinite(v) for v in (bessel,mean,variance)) or abs(mean-bessel)>2e-12:raise RuntimeError('Independent numerical references disagree')
        cases.append(c);rows.append({'kappa':k,'level':r,'mean_lower':str(lo),'mean_upper':str(hi),'mean_width':str(hi-lo),
            'log10_mean_width':math.log10(float(hi-lo)) if hi>lo else '',
            'variance_lower':str(vl),'variance_upper':str(vu),'variance_width':str(vu-vl),
            'bessel_mean_diagnostic':bessel,'quadrature_mean_diagnostic':mean,'quadrature_variance_diagnostic':variance,
            'optimizer_slack_per_side':c.get('optimization_slack_per_side','0')})
    if source!=m.source_hash():raise RuntimeError('Source changed during study')
    with (OUT/'bounds.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    (OUT/'certificates.json').write_text(json.dumps({'status':'passed','source_sha256':source,'certificates':cases},indent=2)+'\n')
    fig,ax=plt.subplots(figsize=(7.3,4.6))
    for k in ('1','5','20'):
        a=[r for r in rows if r['kappa']==k];ax.plot([r['level'] for r in a],[r['log10_mean_width'] for r in a],'o-',label='κ='+k)
    ax.set(xlabel='Positivity level r',ylabel='log₁₀ certified mean-interval width',title='Compact hierarchy: exact outer bounds');ax.legend();ax.grid(alpha=.2);fig.tight_layout()
    for ext in ('png','svg'):fig.savefig(OUT/('moment_convergence.'+ext),dpi=170)
    plt.close(fig)
    hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE/'moment_bounds.py',Path(__file__))}
    (OUT/'study.json').write_text(json.dumps({'status':'passed','cases':len(cases),'source_hashes':hashes,
        'limits':['Exact dual cuts and PSD inner points certify the moment intervals.','Quadrature and Bessel values are diagnostics, not proof premises.','Single Euclidean plaquette, not an interacting Hamiltonian vacuum or mass-gap theorem.']},indent=2)+'\n')
    print(json.dumps({'status':'passed','cases':len(cases),'k1_r6_width':next(r['mean_width'] for r in rows if r['kappa']=='1' and r['level']==6)}))

if __name__=='__main__':main()
