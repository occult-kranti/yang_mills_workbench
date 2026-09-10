#!/usr/bin/env python3
"""Standalone scientific figures from exactly the website's recorded plot data."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
HERE=Path(__file__).resolve().parent
DIST=HERE.parents[1]/'dist'

def main():
    data=json.loads((HERE/'site-data.json').read_bytes())
    out=HERE/'figures';out.mkdir(exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'svg.hashsalt':'ym16','axes.spines.top':False,'axes.spines.right':False})
    graph=json.loads((HERE/'forward/loop1/graph.json').read_bytes())
    fig,ax=plt.subplots(figsize=(9,4.7),layout='constrained')
    def xy(name):
        x,y,z=map(int,name.split(','));return (x+.45*y,z+.3*y)
    boundary=['1,0,0','1,1,0','1,1,1','1,0,1']
    ax.add_patch(Polygon([xy(p) for p in boundary],facecolor='#cf4c35',alpha=.12))
    for edge in graph['edges']:
        a,b=xy(edge['tail']),xy(edge['head']);shared=edge['tail'].startswith('1,') and edge['head'].startswith('1,')
        ax.plot([a[0],b[0]],[a[1],b[1]],color='#b84532' if shared else '#194b67',lw=3.5 if shared else 1.8)
    for vertex in graph['vertices']:
        x,y=xy(vertex);ax.scatter(x,y,s=17,color='#194b67',zorder=3)
    ax.text(.35,.55,'Left disk\n5 outer faces',ha='center',color='#194b67')
    ax.text(1.8,.55,'Right disk\n5 outer faces',ha='center',color='#194b67')
    ax.annotate('Shared square: included once\n4 links of incidence3',xy=(1.225,.65),xytext=(1.225,1.65),ha='center',arrowprops={'arrowstyle':'->','color':'#b84532'},color='#963421')
    ax.set_title('Two adjacent cubes:12 vertices ·20 links ·11 faces',loc='left',pad=20)
    ax.text(1.2,-.32,'Outer boundary alone:10 faces · a different Wilson action',ha='center')
    ax.set_xlim(-.15,2.6);ax.set_ylim(-.42,1.88);ax.set_aspect('equal');ax.axis('off')
    fig.savefig(out/'two-cubes.svg',metadata={'Date':None});fig.savefig(out/'two-cubes.png',dpi=170);plt.close(fig)
    (DIST/'shared-two-cubes.svg').write_bytes((out/'two-cubes.svg').read_bytes())
    overview,axes=plt.subplots(2,2,figsize=(13,8),layout='constrained')
    for i,(key,p) in enumerate(data['plots'].items()):
        if i>=4:raise ValueError('Unexpected plot count')
        fig,ax=plt.subplots(figsize=(8,4.6),layout='constrained')
        for target in (ax,axes.flat[i]):
            for s in p['series']:
                target.plot([r[0] for r in s['points']],[r[1] for r in s['points']],marker='o',markersize=4,label=s['name'])
            target.set_title(p['title'],loc='left',fontsize=11);target.set_xlabel(p['xLabel']);target.set_ylabel(p['yLabel']);target.grid(alpha=.18);target.legend(fontsize=8)
        fig.savefig(out/(key+'.svg'),metadata={'Date':None});fig.savefig(out/(key+'.png'),dpi=170);plt.close(fig)
    overview.savefig(out/'overview.png',dpi=150);plt.close(overview)
    print(json.dumps({'status':'passed','figures':5,'note':'Plots use rounded exact-data displays, not extra scientific evidence.'}))
if __name__=='__main__':main()
