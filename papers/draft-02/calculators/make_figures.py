#!/usr/bin/env python3
"""Generate paper figures and CSV data from the portable calculators.

Numerical curves display formulas or finite-compression diagnostics, not
measured errors. Rational certificate values come from heat_certificates().
"""
from __future__ import annotations
import argparse
import csv
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
import mpmath as mp

import ym_calculators as y

BLUE='#24628C'
GOLD='#B67B24'
RED='#AC5147'
OLIVE='#6A7850'
INK='#26323D'
GREY='#76808A'


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,default=y.HERE.parent/'figures')
    args=ap.parse_args()
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    data=out/'data';data.mkdir(exist_ok=True)
    y.configure_precision(70)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.titlesize':11,
                         'axes.labelsize':10,'xtick.labelsize':9,'ytick.labelsize':9,
                         'legend.fontsize':8.5,'axes.edgecolor':INK,'text.color':INK,
                         'axes.labelcolor':INK,'xtick.color':INK,'ytick.color':INK,
                         'axes.spines.top':False,'axes.spines.right':False,
                         'grid.color':'#DDE2E6','grid.linewidth':0.55,
                         'lines.linewidth':1.8,'pdf.fonttype':42,'ps.fonttype':42})
    metadata=[]
    pages=PdfPages(out/'figure_atlas.pdf',metadata={'Title':'Source-bound Yang–Mills workbench figures','Author':'Research companion; generated from declared formulas'})
    def save(fig,name,caption,source_ids,page=True):
        fig.savefig(out/(name+'.pdf'),bbox_inches='tight',metadata={'Title':caption[:120]})
        fig.savefig(out/(name+'.png'),dpi=240,bbox_inches='tight',facecolor='white')
        if page: pages.savefig(fig,bbox_inches='tight')
        metadata.append({'name':name,'caption':caption,'sources':source_ids,
                         'arithmetic':'70-digit mpmath formulas unless marked exact rational; plot rendering converts to float',
                         'csv':name+'.csv' if (data/(name+'.csv')).exists() else None})
    def csvwrite(name,rows):
        if not rows:return
        with (data/(name+'.csv')).open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    def decorate(ax):
        ax.grid(True,alpha=.7);ax.set_axisbelow(True)
    def footer(fig,text):
        fig.text(.08,.015,text,fontsize=8,color=GREY,ha='left',va='bottom')

    # Figure 1: two models with separately named couplings.
    fig,axs=plt.subplots(2,2,figsize=(7.5,6.2));fig.subplots_adjust(hspace=.53,wspace=.33,bottom=.14,top=.9)
    fig.suptitle('Distinct SU(2) reductions: spectrum and static response',x=.08,ha='left',fontsize=14)
    ratios=np.linspace(0,10,41);jrows=[]
    for r in ratios:
        v=y.jacobi(str(r),dimension=24)
        jrows.append({'lambda_over_alpha':r,'gap_over_alpha':str(v['gap_over_alpha']),'E0_over_alpha':str(v['E0']),'dimension':24})
    ax=axs[0,0];ax.plot(ratios,[float(x['gap_over_alpha']) for x in jrows],color=BLUE,label='N = 24 compression')
    ax.axhline(.999999,color=INK,ls='--',label='Source-proved gap floor')
    ax.set(xlabel=r'Energy ratio $\lambda/\alpha$',ylabel=r'Gap divided by $\alpha$',ylim=(0,11),title='A  One-square Jacobi diagnostic');ax.legend(loc='upper left');decorate(ax)
    ks=np.linspace(-8,8,241);srows=[]
    for kval in ks:
        k=mp.mpf(str(kval))
        u=mp.besseli(2,k)/mp.besseli(1,k) if k else mp.mpf(0)
        var=1-u*u-3*u/k if k else mp.mpf(1)/4
        wrong=2*k/(3+mp.sqrt(9+4*k*k))
        srows.append({'kappa':kval,'mean':str(u),'variance':str(var),'point_closure_mean':str(wrong)})
    ax=axs[0,1];ax.plot(ks,[float(x['mean']) for x in srows],color=BLUE,label='Haar mean')
    ax.plot(ks,[float(x['point_closure_mean']) for x in srows],color=GOLD,ls='--',label='Zero-variance closure')
    ax.set(xlabel=r'Static tilt $\kappa$',ylabel='Mean of half trace',ylim=(-1,1),title='B  Static tilted-Haar measure');ax.legend();decorate(ax)
    ax=axs[1,0];ax.plot(ks,[float(x['variance']) for x in srows],color=BLUE)
    ax.scatter([0],[.25],s=25,color=INK,zorder=3);ax.annotate(r"$u'(0)=1/4$",(0,.25),xytext=(1.1,.225),fontsize=10)
    ax.set(xlabel=r'Static tilt $\kappa$',ylabel=r'Susceptibility $u^{\prime}(\kappa)$',ylim=(0,.28),title='C  Variance retained in the scalar equation');decorate(ax)
    ax=axs[1,1];ax.axis('off')
    ax.text(0,.97,'Different obligations',weight='bold',va='top',fontsize=11)
    ax.text(0,.79,'Jacobi: infinite character tower;\nfinite spatial graph.\nN = 24 states do not certify its tail.\n\nStatic response: a probability measure;\nno physical time generator is identified.\n\nDropping variance changes the origin\nslope from 1/4 to 1/3.',va='top',fontsize=10,linespacing=1.35)
    footer(fig,'Gap floor: inherited exact Round10 certificate on 0 ≤ λ/α ≤ 10. Static curves: exact Bessel formula evaluated numerically.\nNumerical agreement and truncation refinement are diagnostics; neither proves a continuum theorem.')
    csvwrite('jacobi_spectrum',jrows);csvwrite('static_response',srows)
    csvwrite('jacobi_static',[{'family':'jacobi','x':r['lambda_over_alpha'],'value':r['gap_over_alpha'],'comparator':'0.999999'} for r in jrows]+[{'family':'static','x':r['kappa'],'value':r['mean'],'comparator':r['point_closure_mean']} for r in srows])
    save(fig,'jacobi_static','One-square spectral diagnostics and the distinct static tilted-Haar response; numerical curves do not replace exact source proofs.',['R10','R13']);plt.close(fig)

    # Figure 2: complete support and coupled observation-window exponents.
    fig,axs=plt.subplots(1,2,figsize=(7.5,4.5));fig.subplots_adjust(wspace=.34,bottom=.25,top=.82)
    fig.suptitle('Complete support controls the available time window',x=.08,ha='left',fontsize=14)
    ax=axs[0];bs=np.linspace(0,1,201);ax.fill_between(bs,0,3*(1-bs),color=BLUE,alpha=.16)
    ax.plot(bs,3*(1-bs),color=BLUE,ls='--');ax.axvline(1,color=INK,lw=1)
    ax.text(.09,.45,'Vanishing upper certificate',fontsize=9,color=BLUE)
    ax.text(.37,2.5,'No conclusion from\nthis budget alone',fontsize=9,color=GREY)
    ax.set(xlabel=r'Support exponent $\beta$',ylabel=r'Time exponent $\gamma$',xlim=(0,1.25),ylim=(0,3.25),title=r'A  Strict region: $\gamma<3(1-\beta)$');decorate(ax)
    eps=np.logspace(-5,-1,101);configs=[('0','2',BLUE,'-'),('1/2','1',GOLD,'--'),('1/2','3/2',RED,':'),('1','0',OLIVE,'-.')]
    rows=[];ax=axs[1]
    for beta,gamma,color,style in configs:
        vals=[]
        for ee in eps:
            e=mp.mpf(str(ee));r=y.window_budget(1-e,L=None,beta=beta,gamma=gamma)
            vals.append(float(r['normalized_correlation_error_upper']))
            rows.append({'epsilon':str(e),'beta':beta,'gamma':gamma,'L':r['L'],'state_term':str(r['state_term']),'dynamic_term':str(r['dynamic_term']),'envelope':str(r['normalized_correlation_error_upper'])})
        ax.loglog(eps,vals,color=color,ls=style,label=rf'$\beta={beta},\ \gamma={gamma}$')
    ax.invert_xaxis();ax.set(xlabel=r'$\epsilon=1-q$ (toward the endpoint $\rightarrow$)',ylabel='Normalized error upper budget',title='B  Exact support budget evaluated');ax.legend(loc='upper right',fontsize=8);decorate(ax)
    footer(fig,'Canonical summable family, η = 1/2, C = ℓ = 1; L = max(1, floor(ε⁻ᵝ)).\nBoundary curves are excluded from the vanishing certificate. A positive or divergent upper bound is not a lower bound\non actual correlation error. The q = 1 Hamiltonian is not inserted into the summable family.')
    csvwrite('support_window',rows);save(fig,'support_window','Complete-support window certificate: strict sufficient exponent region and evaluated upper budgets, not measured correlation errors.',['R22-N1','R22-N2']);plt.close(fig)

    # Figure 3: Gaussian contraction and triangular feasibility in distinct support budgets.
    fig,axs=plt.subplots(1,2,figsize=(7.5,4.5));fig.subplots_adjust(wspace=.34,bottom=.24,top=.82)
    fig.suptitle('Filtered correction: contraction and locality are separate',x=.08,ha='left',fontsize=14)
    durations=np.linspace(.5,8,160);rows=[];cons=[];sharp=[]
    for s in durations:
        r=y.filter_budget('gaussian','35/1664',str(s));cons.append(float(r['operator_residual_over_r_rational_upper']));sharp.append(float(r['operator_residual_over_r_sharper_numeric_upper']))
        rows.append({'kind':'gaussian','M':'35/1664','duration':s,'residual_budget':cons[-1],'other':sharp[-1]})
    ax=axs[0];ax.plot(durations,cons,color=BLUE,label=r'Rational bound: $\sqrt{2/\pi}<1$');ax.plot(durations,sharp,color=GOLD,ls='--',label='Sharper numerical evaluation')
    ax.scatter([4],[float(F(626,1629))],color=INK,s=25,zorder=3);ax.annotate('626/1629 < 0.385',(4,float(F(626,1629))),xytext=(2.0,.65),fontsize=9,arrowprops={'arrowstyle':'-','color':GREY})
    ax.axhline(float(F(210,1629)),color=GREY,ls=':',label='Upper-budget floor')
    ax.set(xlabel='Gaussian proof duration s',ylabel=r'Upper bound for $\|R_s(A)\|/\|A\|$',ylim=(0,1.04),title='A  Origin source: three crossing stars');ax.legend(fontsize=7.7,loc='upper right');decorate(ax)
    mm=np.logspace(-5,np.log10(35/1664),240);lower=2/(1-25*mm);upper=1/(192*mm)
    ax=axs[1];ax.loglog(mm,lower,color=GOLD,label='Strict contraction lower duration');ax.loglog(mm,upper,color=BLUE,label='Strict residual-locality upper duration')
    valid=lower<upper;ax.fill_between(mm,lower,upper,where=valid,color=BLUE,alpha=.16)
    ax.axvline(1/409,color=INK,ls='--',lw=1);ax.scatter([.001],[3],color=INK,s=25,zorder=3)
    ax.annotate('M = 1/1000, T = 3',(.001,3),xytext=(.000025,1),fontsize=8.5,arrowprops={'arrowstyle':'-','color':GREY})
    ax.text(1/409*1.12,120,'1/409',rotation=90,fontsize=8,color=INK)
    ax.set(xlabel=r'Interaction cap $M=7|\tau|$',ylabel='Triangular proof duration T',ylim=(.1,1000),title='B  Translated family: twelve crossings');ax.legend(loc='upper right',fontsize=7.1);decorate(ax)
    for m,lo,hi in zip(mm,lower,upper):rows.append({'kind':'triangle_feasibility','M':m,'duration':lo,'residual_budget':hi,'other':lo<hi})
    footer(fig,'Panel A: AB2 original cap M = 35/1664. Panel B: AE2 requires 2/(1−25M) < T < 1/(192M).\nIts joint open interval exists exactly when 409M < 1. The zero-frequency residual is one for both filters.\nThese are sufficient upper certificates; neither a budget floor nor a failed locality estimate proves actual divergence.')
    csvwrite('filter_budgets',rows);save(fig,'filter_budgets','Source-specific Gaussian contraction and the translated-family triangular locality/contraction feasibility interval.',['R26-AB2','R26-AE2']);plt.close(fig)

    # Figure 4: retain the admitted tiny-clock range instead of inventing oscillations.
    fig,axs=plt.subplots(2,2,figsize=(7.5,6.3));fig.subplots_adjust(wspace=.33,hspace=.54,bottom=.15,top=.9)
    fig.suptitle('Wilson endpoints: one clock, distinguishable probes',x=.08,ha='left',fontsize=14)
    zs=np.linspace(0,1e-6,161);rows=[]
    for z in zs:
        r=y.wilson(str(z));rows.append({'z':z,'single_deficit':str(r['single_deficit']),'sum_real_deficit':str(r['sum_real_deficit']),'sum_imaginary':str(r['sum_imaginary'])})
    xx=zs/1e-6;ax=axs[0,0]
    ax.plot(xx,[float(r['single_deficit'])*1e16 for r in rows],color=BLUE,label='Six-cycle single source')
    ax.plot(xx,[float(r['sum_real_deficit'])*1e16 for r in rows],color=GOLD,ls='--',label='Coherent sum')
    ax.axhline(0,color=GREY,ls=':',label='Elementary face (null endpoint)')
    ax.set(xlabel=r'$z$ in units of $10^{-6}$',ylabel=r'Real deficit $\times\,10^{16}$',title='A  Quadratic real response');ax.legend(fontsize=7.7);decorate(ax)
    ax=axs[0,1];ax.plot(xx,[float(r['sum_imaginary'])*1e8 for r in rows],color=GOLD,label='Coherent sum')
    ax.axhline(0,color=BLUE,ls='--',label='Single cycle / elementary face')
    ax.set(xlabel=r'$z$ in units of $10^{-6}$',ylabel=r'Imaginary part $\times\,10^8$',title='B  Linear signed response');ax.legend(fontsize=7.7);decorate(ax)
    freq=np.array([-2*np.sqrt(3),-2,0,2,2*np.sqrt(3)])
    wx=np.array([1/24,1/8,2/3,1/8,1/24]);ws=np.array([1/12-1/(8*np.sqrt(3)),1/8,1/3,3/8,1/12+1/(8*np.sqrt(3))])
    ax=axs[1,0]
    ax.vlines(freq-.07,0,wx,color=BLUE,lw=1.5);ax.scatter(freq-.07,wx,color=BLUE,s=25,label='Single')
    ax.vlines(freq+.07,0,ws,color=GOLD,lw=1.5);ax.scatter(freq+.07,ws,color=GOLD,marker='s',s=23,label='Sum')
    ax.set_xticks(freq,labels=[r'$-2\sqrt{3}$',r'$-2$','0','2',r'$2\sqrt{3}$'])
    ax.set(xlabel='Adjacency eigenvalue (phase = eigenvalue × z/84)',ylabel='Source spectral weight',ylim=(0,.73),title='C  More than one reached frequency');ax.legend();decorate(ax)
    ax=axs[1,1];ix=np.arange(3)
    ax.bar(ix-.16,[1,4,8],width=.3,color=BLUE,label='Operator norm squared')
    ax.bar(ix+.16,[1,2,2.5],width=.3,color=GOLD,label='Fourth vacuum moment')
    ax.set_xticks(ix,labels=['Rank swap','Single cycle','Coherent sum'])
    ax.set(ylabel='Dimensionless value',ylim=(0,9),title='D  Equal variance does not fix the operator');ax.legend(fontsize=7.5);ax.grid(axis='y',alpha=.7);ax.set_axisbelow(True)
    footer(fig,'Actual multiplier endpoints, 0 ≤ z ≤ 10⁻⁶. The elementary face is a null probe at this clock.\nThe coherent sum shares the rank-swap endpoint scalar, but its norm squared is 8 and fourth vacuum moment is 5/2.\nCurves evaluate exact limiting formulas. They do not include finite-q remainders, physical clock calibration or measured data.')
    csvwrite('wilson_spectral_weights',[{'adjacency_eigenvalue':v,'single_source_weight':a,'sum_source_weight':b} for v,a,b in zip(freq,wx,ws)])
    csvwrite('wilson_operator_comparison',[{'operator':n,'norm_squared':a,'fourth_vacuum_moment':b,'vacuum_variance':1} for n,a,b in zip(['rank','single','sum'],[1,4,8],[1,2,2.5])])
    csvwrite('wilson_endpoints',rows);save(fig,'wilson_endpoints','Wilson endpoint response in the admitted clock range, reached spectral measures, and operator-norm versus moment distinctions.',['R26-AD1','R26-AD2']);plt.close(fig)

    # Figure 5: physical omitted-channel and numerical evaluator budgets, separately.
    h=y.heat_certificates();ts=np.linspace(0,6,181);rows=[]
    (data/'heat_certificate_constants.json').write_text(json.dumps(y.jsonable(h),indent=2)+'\n')
    for t in ts:
        e=y.heat_envelopes(sigma=str(t));den=float(e['denominator'])
        rows.append({'sigma':t,'early_relative':str(e['early_absolute_numeric']/y.real(e['denominator'])),'late_relative':str(e['late_absolute_numeric']/y.real(e['denominator'])),'minimum_relative':str(e['pointwise_relative_upper_numeric'])})
    fig,axs=plt.subplots(1,2,figsize=(7.5,4.1));fig.subplots_adjust(wspace=.33,bottom=.29,top=.81)
    fig.suptitle('Heat approximation: physical omission and numerical error',x=.08,ha='left',fontsize=14)
    ax=axs[0]
    ax.plot(ts,[float(r['early_relative'])*1e5 for r in rows],color=GOLD,ls='--',label='Early Duhamel upper bound')
    ax.plot(ts,[float(r['late_relative'])*1e5 for r in rows],color=BLUE,ls=':',label='Late spectral upper bound')
    ax.plot(ts,[float(r['minimum_relative'])*1e5 for r in rows],color=INK,label='Pointwise smaller upper bound')
    ax.axhline(float(h['AC2']['all_time_physical_relative'])*1e5,color=GREY,ls='-.',label='Uniform rational certificate')
    ax.axvline(2.6,color=GREY,ls=':',lw=1)
    ax.set(xlabel=r'Heat time $\sigma=\alpha t/\hbar$',ylabel=r'Relative upper bound $\times\,10^5$',ylim=(0,10),title='A  AC2 complete physical omission');ax.legend(fontsize=7.1,loc='upper right');decorate(ax)
    ax=axs[1];early=float(h['AF2']['early_total']);late=float(h['AF2']['late_total'])
    ax.plot([.05,8],[early,early],color=GOLD,label='Early numerical certificate')
    ax.plot([8,30],[late,late],color=BLUE,label='Late numerical certificate')
    ax.scatter([8],[early],s=28,color=GOLD,zorder=3);ax.scatter([8],[late],s=30,facecolor='white',edgecolor=BLUE,zorder=3)
    ax.axhline(float(h['AC2']['all_time_physical_relative']),color=GREY,ls='--',label='Physical relative certificate')
    ax.axvline(8,color=GREY,ls=':',lw=1)
    ax.set_yscale('log');ax.set(xlabel=r'Heat time $\sigma$ (late branch continues forever)',ylabel='Numerical absolute /\nphysical relative bound',ylim=(1e-16,1e-4),title='B  AF2 piecewise evaluator budgets');ax.legend(fontsize=7.1,loc='center right');decorate(ax)
    footer(fig,'λ ≤ 0.01 for AC2; λ = 0.01 for AF2. Inputs: normalized original P21 vectors within 0.01 of the vacuum.\nPhysical bound = 457097/12472250000; denominator ≥ 7127/7200. The 293-dimensional space is an enrichment.\nThis companion recomputes scalar certificates. It does not execute the original 293-coordinate heat solver.')
    csvwrite('heat_certificates',rows);save(fig,'heat_certificates','Early/late physical error bounds and the separate all-time numerical evaluator budget, on the original P21 preparation class.',['R26-AC2','R26-AF1','R26-AF2']);plt.close(fig)
    pages.close()

    # Optional compact provenance inventory; no force layout implies theorem implication.
    net=json.loads((y.HERE/'source_data/network_audit.json').read_text())
    fig,ax=plt.subplots(figsize=(7.5,3.6));fig.subplots_adjust(left=.085,right=.98,bottom=.29,top=.8)
    fig.suptitle('Evidence network inventory by round provenance',x=.085,ha='left',fontsize=14)
    labels=list(net['nodes_by_round']);values=list(net['nodes_by_round'].values());positions=np.arange(len(labels))
    ax.bar(positions,values,color=[BLUE]*(len(labels)-1)+[GOLD],width=.7)
    ax.set_xticks(positions,labels=[k[1:] for k in labels]);ax.set(xlabel='Research round identifier',ylabel='Stored network nodes',ylim=(0,53));ax.grid(axis='y');ax.set_axisbelow(True)
    ax.text(.01,.91,'158 unique nodes  ·  260 edges  ·  0 dangling edges',transform=ax.transAxes,fontsize=10,color=INK)
    ax.annotate('R26: 10 loops + 26 equations\n+ 4 premises + 7 open goals',(positions[-1],47),xytext=(positions[-1]-9,29),fontsize=9,arrowprops={'arrowstyle':'-','color':GREY})
    footer(fig,'Counts audit research/round26/network.json at commit 40960f39a3dc. A node is not a completed investigation.\nEdge types: 240 recorded dependencies, 8 review selections, 12 proposed transfers. Provenance does not itself\nauthorize transfer of model conclusions; open/planned nodes are not established results.')
    csvwrite('network',[{'round':k,'stored_nodes':v} for k,v in net['nodes_by_round'].items()]);save(fig,'network','Audited inventory of the actual evidence-network schema; node counts are not research-loop counts or proof scores.',['R26-network'],page=False);plt.close(fig)
    from make_network import generate_network
    metadata.append(generate_network(out))
    # All numerical source rows and figure titles remain inspectable beside the PDFs.
    (out/'figure_metadata.json').write_text(json.dumps({'repository_commit':y.COMMIT,'figures':metadata,'atlas_pages':5,'network_optional_separate':True},indent=2)+'\n')
    hashes={str(p.relative_to(out)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(out.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.json'}
    (out/'SHA256SUMS.json').write_text(json.dumps(hashes,indent=2)+'\n')
    print(json.dumps({'figures':len(metadata),'atlas_pages':5,'output':str(out)}))


if __name__=='__main__':
    main()
