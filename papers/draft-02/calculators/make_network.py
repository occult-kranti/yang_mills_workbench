#!/usr/bin/env python3
"""Draw every audited evidence node and directed edge; positions are schematic."""
import argparse
import csv
import json
from pathlib import Path
import re
from collections import Counter

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.lines import Line2D
import numpy as np

HERE=Path(__file__).resolve().parent


def generate_network(out:Path):
    out=Path(out);out.mkdir(parents=True,exist_ok=True);(out/'data').mkdir(exist_ok=True)
    d=json.loads((HERE/'source_data/network_structure.json').read_text())
    ids=[n['id'] for n in d['nodes']]
    if len(ids)!=158 or len(ids)!=len(set(ids)) or len(d['edges'])!=260:
        raise ValueError('unexpected structural counts')
    if any(e['from'] not in ids or e['to'] not in ids for e in d['edges']):
        raise ValueError('dangling edge')
    edge_types=Counter(e['type'] for e in d['edges'])
    styles={'proven-dependency':('#567E9A','-',.29,.65),
            'review-selection':('#A87322','--',.8,1.25),
            'proposed-transfer':('#A24F59',':',.9,1.3)}
    if set(edge_types)!=set(styles):raise ValueError('unknown edge type')
    positions={};round_labels=[];groups={}
    early=[n for n in d['nodes'] if n['kind']=='history' and int(re.match(r'r(\d+)',n['id']).group(1))<=15]
    recent=[n for n in d['nodes'] if n['kind']=='history' and int(re.match(r'r(\d+)',n['id']).group(1))>15]
    for column,nodes in [(0,early),(1,recent)]:
        rounds=sorted(set(int(re.match(r'r(\d+)',n['id']).group(1)) for n in nodes))
        for yy,rr in zip(np.linspace(.93,.08,len(rounds)),rounds):
            selected=[n for n in nodes if int(re.match(r'r(\d+)',n['id']).group(1))==rr]
            round_labels.append((column-.38,yy,'R'+str(rr)))
            for i,node in enumerate(selected):
                positions[node['id']]=(column-.1+(i%5)*.07,yy-(i//5)*.02)
                groups[node['id']]='history_early' if column==0 else 'history_recent'
    loops=[n for n in d['nodes'] if n['kind']=='loop']
    for yy,n in zip(np.linspace(.91,.19,len(loops)),loops):
        positions[n['id']]=(2,yy);groups[n['id']]='current_loop'
        eq=[e for e in d['nodes'] if e['kind']=='equation' and e['id'].startswith(n['id']+'-')]
        for i,node in enumerate(eq):
            positions[node['id']]=(3+(i-(len(eq)-1)/2)*.075,yy+.012*(i%2));groups[node['id']]='equation'
    prem=[n for n in d['nodes'] if n['kind']=='premise']
    for i,n in enumerate(prem):
        positions[n['id']]=(2.88+.08*i,.07);groups[n['id']]='premise'
    opens=[n for n in d['nodes'] if n['kind']=='open']
    for yy,n in zip(np.linspace(.88,.12,len(opens)),opens):
        positions[n['id']]=(4,yy);groups[n['id']]='open'
    if set(positions)!=set(ids):raise ValueError('layout omitted nodes')
    fig,ax=plt.subplots(figsize=(10.8,6.7));fig.subplots_adjust(left=.055,right=.98,bottom=.17,top=.82)
    fig.suptitle('Recorded evidence relations: all 158 nodes and 260 directed edges',x=.055,ha='left',fontsize=14)
    fig.text(.055,.875,'Schematic organization by historical round and current node kind; position and distance have no physical meaning.',fontsize=9,color='#52606D')
    for xx in [.48,1.48,2.48,3.48]:ax.axvline(xx,color='#E2E6E9',lw=.65,zorder=0)
    for typ in styles:
        color,ls,alpha,lw=styles[typ]
        for idx,e in enumerate(d['edges']):
            if e['type']!=typ:continue
            a,b=positions[e['from']],positions[e['to']]
            rad=.06 if b[0]>=a[0] else -.13
            if abs(b[0]-a[0])<.4:rad=.28 if idx%2 else -.28
            patch=FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=5.5,
                                  shrinkA=2.5,shrinkB=2.5,connectionstyle=f'arc3,rad={rad}',
                                  color=color,linestyle=ls,alpha=alpha,lw=lw,zorder=1)
            ax.add_patch(patch)
    marks={'history_early':('o','#49728F',10),'history_recent':('o','#49728F',10),
           'current_loop':('o','#174B70',35),'equation':('s','#87A6B9',21),
           'premise':('D','#69727B',24),'open':('D','#FFFFFF',37)}
    for name,(marker,color,size) in marks.items():
        pts=[positions[i] for i in ids if groups[i]==name]
        ax.scatter([p[0] for p in pts],[p[1] for p in pts],marker=marker,c=color,s=size,
                   edgecolors='#9C4B55' if name=='open' else 'white',linewidths=.55,zorder=3)
    for xx,yy,label in round_labels:ax.text(xx,yy,label,fontsize=8,va='center',color='#394854')
    for n in loops:
        xx,yy=positions[n['id']];ax.text(xx-.1,yy,n['id'].upper(),ha='right',va='center',fontsize=9,color='#174B70')
    short={'open-next-diagonal':'Nonlinear iteration','open-volume':'Graph-size limit','open-clock':'Physical clock','open-continuum':'Continuum / gap',
           'next-ag':'AG planned','next-ah':'AH planned','next-ai':'AI planned'}
    for n in opens:
        xx,yy=positions[n['id']];ax.text(xx+.08,yy,short[n['id']],fontsize=8,va='center',color='#7D3E46',bbox={'facecolor':'white','edgecolor':'none','pad':.6})
    headings=[(0,'Historical R3–15'),(1,'Historical R16–25'),(2,'R26 loops (10)'),(3,'Equations (26)\nPremises (4, bottom)'),(4,'Open / planned (7)')]
    for xx,label in headings:ax.text(xx,1.04,label,ha='center',va='bottom',fontsize=10,weight='bold',color='#26323D')
    ax.set_xlim(-.48,4.9);ax.set_ylim(.015,1.08);ax.axis('off')
    handles=[Line2D([0],[0],color=styles[k][0],linestyle=styles[k][1],lw=1.7,label=f'{name} ({edge_types[k]})')
             for k,name in [('proven-dependency','Recorded dependency'),('review-selection','Review selection'),('proposed-transfer','Proposed transfer')]]
    fig.legend(handles=handles,loc='lower left',bbox_to_anchor=(.055,.065),ncol=3,frameon=False,fontsize=9)
    fig.text(.055,.025,'Source: research/round26/network.json at commit 40960f39a3dc. Every structural node and edge is included; labels are selective.\nA recorded dependency is provenance, not permission to transfer a theorem between models. Planned nodes are not completed investigations.',fontsize=8,color='#52606D')
    fig.savefig(out/'network_structure.pdf',bbox_inches='tight',metadata={'Title':'Audited directed evidence network'})
    fig.savefig(out/'network_structure.png',bbox_inches='tight',dpi=240,facecolor='white');plt.close(fig)
    with (out/'data/network_nodes.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['id','kind','status','group','layout_x','layout_y'])
        for n in d['nodes']:w.writerow([n['id'],n['kind'],n['status'],groups[n['id']],*positions[n['id']]])
    with (out/'data/network_edges.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['from','to','type']);w.writeheader();w.writerows(d['edges'])
    audit={'node_count':len(ids),'unique_ids':len(set(ids)),'drawn_nodes':len(positions),'edge_count':len(d['edges']),
           'drawn_edges':len(d['edges']),'dangling_edges':0,'edges_by_type':dict(edge_types),
           'scope':'Directed provenance diagram; grouping layout is not mathematical/physical distance or an automatic theorem implication.'}
    (out/'network_structure_audit.json').write_text(json.dumps(audit,indent=2)+'\n')
    return {'name':'network_structure','caption':'Complete directed evidence network; selective labels and nonphysical grouping layout.',
            'sources':['R26-network'],'arithmetic':'Exact counts from pinned structural source; deterministic schematic layout',
            'csv':['network_nodes.csv','network_edges.csv']}


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,default=HERE.parent/'figures')
    print(json.dumps(generate_network(p.parse_args().output)))
