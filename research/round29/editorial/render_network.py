#!/usr/bin/env python3
"""Render the admitted-loop projection of the canonical research graph."""
from pathlib import Path
import hashlib,json,textwrap
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch,FancyBboxPatch
from matplotlib.path import Path as DrawPath
def require(condition,message):
 if not condition:raise ValueError(message)
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/'papers/draft-02'
source=ROOT/'research/round29/network.json'
graph=json.loads(source.read_text())
findings=json.loads((ROOT/'research/round29/advisor/findings.json').read_text())
require(len(findings['loops'])==10, 'Render the final ten-loop network only.')
loops=sorted(findings['loops'],key=lambda x:x['sequence'])
loop_ids={'r29-'+x['id'].lower() for x in loops}
nodes={x['id']:x for x in graph['nodes']}
require(loop_ids<=nodes.keys(), 'Acceptance condition failed: loop_ids<=nodes.keys()')
edges=[e for e in graph['edges'] if e['to'] in loop_ids and e['type']=='source-dependency']
parents=sorted({e['from'] for e in edges}-loop_ids)
scope=[e for e in graph['edges'] if e['from'] in loop_ids and e['to']=='src-clay' and e['type']=='scope-boundary']
require(len(scope)==10, 'Every admitted loop must retain its continuum scope boundary.')
brief={
 'r18-b2':'R18-B2: full-space gap / bridge',
 'r21-i1':'I1: actual 24-link model',
 'r21-i2':'I2: vacuum rotation',
 'r28-ag3':'AG3: complete source budget',
 'r28-aj1':'AJ1: physical representation',
 'r28-ak1':'AK1: Wilson variance',
 'r28-ak2':'AK2: physical moment / heat',
 'src-gauvin-v3':'Gauvin (2026), v3: regulated transfer',
 'src-htw':'Henheik–Teufel–Wessel: local comparison',
 'src-ns':'Nachtergaele–Sims: unbounded-site dynamics',
 'src-nsy':'Nachtergaele–Sims–Young: dynamics',
}
fig,ax=plt.subplots(figsize=(6.3,7.4))
fig.subplots_adjust(left=.01,right=.99,bottom=.01,top=.98)
ax.set(xlim=(0,6.3),ylim=(0,7.4));ax.axis('off')
xs=[.88,3.03,5.18];pos={};labels={}
for i,key in enumerate(parents):
 y=6.75-i*5.5/max(len(parents)-1,1);pos[key]=(xs[0],y)
 labels[key]='\n'.join(textwrap.wrap(brief.get(key,nodes[key]['title']),26))
for entry in loops:
 key='r29-'+entry['id'].lower();row=(entry['sequence']-1)//2;col=1+(entry['sequence']-1)%2
 pos[key]=(xs[col],6.5-row*1.23)
 title=entry['title'].removeprefix('HNM ')
 labels[key]=entry['id']+'\n'+'\n'.join(textwrap.wrap(title,25))
for e in edges:
 a,b=pos[e['from']],pos[e['to']]
 start=(a[0]+.77,a[1]);end=(b[0]-.80,b[1])
 # Route cross-branch arrows in the gutters so they cannot masquerade as an
 # input from an intervening box that covers the middle of a straight line.
 route=None
 if a[0]==xs[0] and b[0]==xs[2]:
  route=[start,(1.93,a[1]),(1.93,b[1]+.59),(4.12,b[1]+.59),(4.12,b[1]),end]
 elif a[0]==xs[2] and b[0]==xs[1]:
  route=[(a[0]-.80,a[1]),(4.10,a[1]),(4.10,b[1]),(b[0]+.80,b[1])]
 elif a[0]==b[0]:
  route=[(a[0]+.80,a[1]),(6.02,a[1]),(6.02,b[1]),(b[0]+.80,b[1])]
 elif a[0]==xs[1] and b[0]==xs[2] and abs(a[1]-b[1])>.1:
  route=[start,(4.06,a[1]),(4.06,b[1]),end]
 options={'path':DrawPath(route,[DrawPath.MOVETO]+[DrawPath.LINETO]*(len(route)-1))} if route else {'posA':start,'posB':end,'connectionstyle':'arc3,rad=0'}
 ax.add_patch(FancyArrowPatch(**options,arrowstyle='-|>',mutation_scale=6,linewidth=.6,color='#5f7590',alpha=.72,zorder=1))
for key,(x,y) in pos.items():
 external=key.startswith('src-');is_loop=key in loop_ids
 limited=is_loop and nodes[key].get('status')=='limited'
 fill='#fff0d3' if limited else '#e7f0fa' if is_loop else '#f3f4f5'
 height=.70 if is_loop else .47
 box=FancyBboxPatch((x-.78,y-height/2),1.56,height,boxstyle='round,pad=0.025,rounding_size=0.04',facecolor=fill,edgecolor='#b58329' if limited else '#57738f' if is_loop else '#8c959d',linewidth=.65,zorder=3)
 ax.add_patch(box);ax.text(x,y,labels[key],ha='center',va='center',fontsize=7.2 if is_loop else 6.7,linespacing=1.2,zorder=4)
ax.text(xs[0],7.18,'Inherited inputs / external sources',ha='center',fontsize=6.6,fontweight='bold')
ax.text(xs[1],7.18,'First investigation',ha='center',fontsize=7,fontweight='bold')
ax.text(xs[2],7.18,'Adaptive second investigation',ha='center',fontsize=6.6,fontweight='bold')
# Ten common scope-boundary edges share a rail. The aggregation is declared in
# the figure and metadata; it cannot be mistaken for a successful proof arrow.
rail_x=6.18
for e in scope:
 x,y=pos[e['from']]
 ax.plot([x+.79,rail_x],[y-.29,y-.29],ls=(0,(2,2)),color='#9c5656',alpha=.35,lw=.45,zorder=0)
ax.plot([rail_x,rail_x],[.68,6.22],ls=(0,(2,2)),color='#9c5656',lw=.6,zorder=0)
ax.add_patch(FancyArrowPatch((rail_x,.68),(5.78,.46),arrowstyle='-|>',mutation_scale=6,linestyle=(0,(2,2)),color='#9c5656',linewidth=.7))
ax.add_patch(FancyBboxPatch((.25,.14),5.56,.59,boxstyle='round,pad=0.03',facecolor='#fbefef',edgecolor='#9c5656',linewidth=.7))
ax.text(3.03,.445,'Clay / Jaffe–Witten: continuum construction and physical mass gap\nAll ten scope-boundary edges remain open (shared dashed rail).',ha='center',va='center',fontsize=7,linespacing=1.35)
base=OUT/'figures/round29-dependencies'
fig.savefig(base.with_suffix('.pdf'))
fig.savefig(base.with_suffix('.png'),dpi=220)
plt.close(fig)
record={'source':'research/round29/network.json','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'projection':'All ten admitted loop nodes, their direct canonical input nodes/edges and all ten Clay scope-boundary edges. Equation nodes and older ancestor chains omitted. Common scope edges use an explicitly labelled shared rail.','nodes':sorted(pos),'source_dependencies':edges,'scope_boundaries':scope,'external_source_names_preserved':True}
base.with_suffix('.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'figure':str(base.with_suffix('.pdf').relative_to(ROOT)),'nodes':len(pos),'inputs':len(edges),'scope_boundaries':len(scope)}))
