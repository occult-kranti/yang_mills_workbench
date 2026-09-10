#!/usr/bin/env python3
"""Standalone scientific figures from the identical recorded website series."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE=Path(__file__).resolve().parent

def main():
    data=json.loads((HERE/'site-data.json').read_bytes());out=HERE/'figures';out.mkdir(exist_ok=True)
    plt.rcParams.update({'font.size':10,'axes.grid':True,'grid.alpha':.2,'svg.fonttype':'none'})
    overview,axes=plt.subplots(3,2,figsize=(14,13),constrained_layout=True)
    for ax,(key,p) in zip(axes.flat,data['plots'].items()):
        fig,one=plt.subplots(figsize=(9,5),constrained_layout=True)
        for target in (ax,one):
            for s in p['series']:
                if not s['points']:raise ValueError('Empty scientific series')
                x,y=zip(*s['points']);target.plot(x,y,marker='o',markersize=3,label=s['name'])
            target.set(title=p['title'],xlabel=p['xLabel'],ylabel=p['yLabel']);target.legend(fontsize=8)
        fig.savefig(out/(key+'.png'),dpi=160);fig.savefig(out/(key+'.svg'));plt.close(fig)
    axes.flat[-1].axis('off');axes.flat[-1].text(.04,.9,'Round15: six completed research loops\n\nA: complete finite interval\nB: exact closed-cube integral\nC: finite physical spectral improvement\n\nOriginal volume-uniform threshold: open\nFour-dimensional Yang–Mills: open\n\nFigures show rounded recorded endpoints.\nExact certificates and CSV files supply the evidence.',va='top',fontsize=13)
    overview.savefig(out/'overview.png',dpi=140);plt.close(overview)
    print(json.dumps({'status':'rendered','figures':5,'overview':'figures/overview.png'}))
if __name__=='__main__':main()
