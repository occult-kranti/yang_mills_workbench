#!/usr/bin/env python3
"""Scientific figure of an admitted inequality; no simulated dynamics."""
from pathlib import Path
from fractions import Fraction as F
import argparse
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from admission import ROOT,gate

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--preview',type=Path);args=parser.parse_args()
    gate('w1')
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False,'svg.hashsalt':'ym24-w1'})
    fig,ax=plt.subplots(figsize=(8.1,5.3));fig.subplots_adjust(left=.12,right=.98,top=.91,bottom=.24);fig.patch.set_facecolor('#fbfaf7');ax.set_facecolor('#fbfaf7')
    theta=[F(i,16*200) for i in range(1,201)]
    for n,color in [(1,'#2c6570'),(3,'#8c763e'),(5,'#8e4940')]:
        tau=F(n,1664);y=[1-12*t*(1+28*tau) for t in theta]
        ax.plot([float(t) for t in theta],[float(v) for v in y],color=color,label=f'|τ| = {n}/1664',linewidth=2)
        ax.plot([1/16],[float(y[-1])],'o',color=color,markersize=5)
    floor=F(311,1664);ax.axhline(float(floor),color='#6a6a6a',linestyle='--',linewidth=1)
    ax.text(.002,float(floor)+.026,'Uniform floor: 311/1664 ≈ 0.1869',color='#555555')
    ax.set(xlim=(0,1/16),ylim=(0,1.04),xlabel='Θ — dimensionless proof-filter duration',ylabel='Certified lower factor for ‖RΘ(A)‖ / ‖w‖',title='The selected source survives the short filter')
    ax.legend(frameon=False,loc='upper right');ax.grid(alpha=.15)
    fig.text(.5,.035,'Bound: 1 − 12Θ(1 + 28|τ|), for 0 < Θ ≤ 1/16 and τ ≠ 0.\nAn analytic lower bound in the S model, not a measured residual or a trajectory.',ha='center',fontsize=9,color='#555555')
    fig.savefig(ROOT/'dist/round24-residual-bound.svg',bbox_inches='tight',metadata={'Date':None})
    if args.preview: fig.savefig(args.preview,bbox_inches='tight',dpi=150)
    plt.close(fig)
    print('Built admitted W1 bound figure')
if __name__=='__main__':main()
