#!/usr/bin/env python3
"""Standalone figures from exactly the recorded dashboard data."""
from pathlib import Path
import html,json,math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
HERE=Path(__file__).resolve().parent
DIST=HERE.parents[1]/'dist'

def four_cube_figure(out):
    graph=json.loads((HERE/'forward/c1/output/graph.json').read_bytes())
    outer=[f for f in graph['faces'] if len(f['incident_cells'])==1]
    outer_edges={w['edge'] for f in outer for w in f['word']}
    center='e2:1,1,0'
    if (len(graph['vertices']),len(graph['edges']),len(graph['faces']),len(outer_edges),len(outer))!=(18,33,20,32,16) or center in outer_edges:raise ValueError('Changed graph figure contract')
    def xy(v):
        x,y,z=map(int,v.split(','));return x+.43*y,z+.26*y
    fig,axes=plt.subplots(1,2,figsize=(11,4.9),layout='constrained')
    for index,ax in enumerate(axes):
        if index==0:
            for f in graph['faces']:
                if len(f['incident_cells'])==2:ax.add_patch(Polygon([xy(v) for v in f['vertices']],facecolor='#b74732',alpha=.13))
        for edge in graph['edges']:
            if index and edge['id'] not in outer_edges:continue
            a,b=xy(edge['tail']),xy(edge['head']);central=edge['id']==center
            ax.plot([a[0],b[0]],[a[1],b[1]],color='#b74732' if central else '#194b67',lw=4 if central else 1.5,zorder=3 if central else 2)
        for v in graph['vertices']:
            x,y=xy(v);ax.scatter(x,y,s=15,color='#194b67',zorder=4)
        ax.set_title(('Full complex: 18V, 33E, 20F' if index==0 else 'Outer boundary: 18V, 32E, 16F'),loc='left',fontsize=12)
        label='Central link: four incident internal faces' if index==0 else 'Central link and four internal faces absent'
        ax.text(1.4,-.24,label,ha='center',fontsize=9,color='#963421' if index==0 else '#194b67')
        ax.set_xlim(-.2,3.05);ax.set_ylim(-.4,1.75);ax.set_aspect('equal');ax.axis('off')
    fig.savefig(out/'four-cubes.svg',metadata={'Date':None});fig.savefig(out/'four-cubes.png',dpi=160);plt.close(fig)
    (DIST/'six-four-cubes.svg').write_bytes((out/'four-cubes.svg').read_bytes())

def collaboration_svg():
    stages=[('Plan','Initial advisor review'),('A1','Local split and obstruction'),('A2','Sparse-support gap'),('Revise','Update goals B and C'),('B1','Dense finite trial'),('B2','Repair the finite endpoint'),('C1','Four-cube invariant tensor'),('C2','Conditional channel experiment')]
    width,height=900,880;parts=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc"><title id="title">Six research loops and two advisory decisions</title><desc id="desc">Forward and backward researchers independently report to the advisor. Each gate selects the next loop. A second planning decision follows A2.</desc><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10z" fill="#597080"/></marker></defs><rect width="900" height="880" fill="white"/>']
    for x,text in [(170,'Forward researcher'),(450,'Advisor–skeptic'),(730,'Backward researcher')]:parts.append(f'<text x="{x}" y="30" text-anchor="middle" font-family="sans-serif" font-size="17" fill="#172b38">{text}</text>')
    for index,(name,description) in enumerate(stages):
        y=85+index*100
        if index:parts.append(f'<path d="M450 {y-72}V{y-28}" stroke="#597080" stroke-width="1.8" marker-end="url(#arrow)"/>')
        control=name in ('Plan','Revise')
        if not control:
            for x,label in [(170,'Derive and compute'),(730,'Rebuild and challenge')]:
                parts.append(f'<rect x="{x-115}" y="{y-24}" width="230" height="48" fill="#f3f6f8" stroke="#597080"/><text x="{x}" y="{y+5}" text-anchor="middle" font-family="sans-serif" font-size="14" fill="#172b38">{label}</text>')
            parts.append(f'<path d="M285 {y}H329M615 {y}H571" fill="none" stroke="#597080" stroke-width="1.8" marker-end="url(#arrow)"/>')
        parts.append(f'<rect x="335" y="{y-27}" width="230" height="54" fill="{("#e9f0ed" if control else "#fff")}" stroke="#244f62" stroke-width="1.5"/><text x="450" y="{y-5}" text-anchor="middle" font-family="sans-serif" font-size="15" fill="#172b38">{html.escape(name+" · "+("Decision" if control else "Accepted gate"))}</text><text x="450" y="{y+15}" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#172b38">{html.escape(description)}</text>')
    parts.append('<text x="450" y="850" text-anchor="middle" font-family="sans-serif" font-size="13" fill="#172b38">Completed sequence; original dense and continuum obligations stay open.</text></svg>')
    return ''.join(parts)

def main():
    data=json.loads((HERE/'site-data.json').read_bytes());out=HERE/'figures';out.mkdir(exist_ok=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.hashsalt':'ym17','axes.spines.top':False,'axes.spines.right':False})
    count=len(data['plots']);cols=2;rows=math.ceil(count/cols)
    overview,axes=plt.subplots(rows,cols,figsize=(13,4.2*rows),layout='constrained',squeeze=False)
    for index,(key,p) in enumerate(data['plots'].items()):
        fig,ax=plt.subplots(figsize=(8.2,4.7),layout='constrained')
        for target in (ax,axes.flat[index]):
            for series in p['series']:
                target.plot([q[0] for q in series['points']],[q[1] for q in series['points']],marker='o',markersize=3.5,label=series['name'])
            target.set_title(p['title'],loc='left',fontsize=11);target.set_xlabel(p['xLabel']);target.set_ylabel(p['yLabel']);target.grid(alpha=.18);target.legend(fontsize=8)
        fig.savefig(out/(key+'.svg'),metadata={'Date':None});fig.savefig(out/(key+'.png'),dpi=160);plt.close(fig)
    for unused in range(count,rows*cols):axes.flat[unused].axis('off')
    overview.savefig(out/'overview.png',dpi=140);plt.close(overview)
    svg=collaboration_svg();(out/'collaboration.svg').write_text(svg);(DIST/'six-collaboration.svg').write_text(svg)
    four_cube_figure(out)
    print(json.dumps({'status':'passed','scientific_plots':count,'collaboration_graph':True,'scope':'Recorded scientific data, display rounding only; no extra physics evidence.'}))
if __name__=='__main__':main()
