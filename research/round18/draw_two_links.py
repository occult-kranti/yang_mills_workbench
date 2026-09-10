"""Actual finite graph for the accepted two-link conditional integral."""
from pathlib import Path
from itertools import product
import json,sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon,Patch
HERE=Path(__file__).resolve().parent;DIST=HERE.parents[1]/'dist'

def geometry():
    sizes=(3,3,2);vertices=list(product(*(range(n) for n in sizes)))
    edges={}
    for v in vertices:
        for a in range(3):
            if v[a]+1<sizes[a]:
                w=list(v);w[a]+=1;edges[(a,*v)]=(v,tuple(w))
    faces=[]
    for normal in range(3):
        a,b=[i for i in range(3) if i!=normal]
        for v in vertices:
            if v[a]+1>=sizes[a] or v[b]+1>=sizes[b]:continue
            p=list(v);p[a]+=1;q=p.copy();q[b]+=1;r=list(v);r[b]+=1
            corners=(v,tuple(p),tuple(q),tuple(r));boundary=[]
            for x,y in zip(corners,corners[1:]+corners[:1]):
                axis=next(i for i in range(3) if x[i]!=y[i]);start=min(x,y);boundary.append((axis,*start))
            faces.append({'id':f'{normal}:'+','.join(map(str,v)),'corners':corners,'edges':boundary})
    U=(2,1,1,0);V=(2,1,0,0)
    for f in faces:
        f['class']='shared' if U in f['edges'] and V in f['edges'] else 'U-only' if U in f['edges'] else 'V-only' if V in f['edges'] else 'fixed'
    counts={k:sum(f['class']==k for f in faces) for k in ('U-only','V-only','shared','fixed')}
    if (len(vertices),len(edges),len(faces),counts)!=(18,33,20,{'U-only':3,'V-only':2,'shared':1,'fixed':14}):raise ValueError('Wrong actual graph')
    return vertices,edges,faces,U,V,counts

def main():
    sys.path.insert(0,str(HERE/'advisor'));from freeze_gate import verify
    verify(HERE/'advisor/c2-gate.json')
    vertices,edges,faces,U,V,counts=geometry()
    actual=json.loads((HERE/'forward/c2/output/completecollection.json').read_bytes())['graph']
    if actual['variable_links']!={'U':'e2:1,1,0','V':'e2:1,0,0'}:raise ValueError('Integrated-link labels changed')
    vertex_ids={','.join(map(str,v)) for v in vertices}
    edge_ids={'e'+str(k[0])+':'+','.join(map(str,k[1:])):( ','.join(map(str,a)), ','.join(map(str,b))) for k,(a,b) in edges.items()}
    face_edges={'f'+f['id']:{'e'+str(k[0])+':'+','.join(map(str,k[1:])) for k in f['edges']} for f in faces}
    if vertex_ids!=set(actual['vertices']) or edge_ids!={e['id']:(e['tail'],e['head']) for e in actual['edges']} or face_edges!={f['id']:{t['edge'] for t in f['word']} for f in actual['faces']}:raise ValueError('Drawing geometry differs from the accepted graph')
    project=lambda p:(170*p[0]+95*p[1],110*p[1]+270*p[2])
    colors={'U-only':'#c96a16','V-only':'#18749a','shared':'#8054a6'}
    fig,ax=plt.subplots(figsize=(9,8));fig.subplots_adjust(top=.84,bottom=.18,left=.07,right=.93)
    for f in faces:
        if f['class']!='fixed':ax.add_patch(Polygon([project(v) for v in f['corners']],closed=True,facecolor=colors[f['class']],edgecolor='none',alpha=.14))
    for key,(a,b) in edges.items():
        p,q=project(a),project(b);color='#b22531' if key==U else '#08799a' if key==V else '#6c7a88';width=4.2 if key in (U,V) else 1.15
        ax.plot([p[0],q[0]],[p[1],q[1]],color=color,lw=width,zorder=4 if key in (U,V) else 2)
    x,y=zip(*(project(v) for v in vertices));ax.scatter(x,y,s=22,color='#293d4e',zorder=5)
    for key,label,color,offset in [(U,'U  (1,1,z)','#9b1422',(16,0)),(V,'V  (1,0,z)','#066882',(16,-10))]:
        a,b=edges[key];p=project(a);q=project(b);ax.text(p[0]+offset[0],(p[1]+q[1])/2+offset[1],label,color=color,fontsize=12,fontweight='bold',bbox={'facecolor':'white','edgecolor':'none','alpha':.87,'pad':3},zorder=6)
    ax.text(-12,-30,'(0,0,0)',fontsize=10,color='#405466');ax.text(340,-30,'x',fontsize=11);ax.text(540,205,'y',fontsize=11);ax.text(-20,282,'z',fontsize=11)
    ax.set_aspect('equal');ax.set_xlim(-40,585);ax.set_ylim(-50,535);ax.axis('off')
    fig.suptitle('Two integrated links on the actual four-cube graph',fontsize=15,fontweight='bold',y=.96)
    fig.text(.5,.91,'18 vertices · 33 links · 20 faces · 31 links fixed to identity',ha='center',fontsize=11,color='#425769')
    handles=[Patch(facecolor=colors[k],alpha=.45,label=label) for k,label in [('U-only','3 U-only faces: 3x'),('V-only','2 V-only faces: 2y'),('shared','1 shared face: w')]]
    fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.5,.072),ncol=3,frameon=False,fontsize=10)
    fig.text(.5,.035,'The six variable weights give S = κ(3x + 2y + w). The other 14 are constant in this conditional integral.',ha='center',fontsize=9,color='#425769')
    out=HERE/'figures';out.mkdir(exist_ok=True)
    with matplotlib.rc_context({'svg.fonttype':'none'}):fig.savefig(DIST/'next-two-links.svg');fig.savefig(out/'two-links.svg')
    fig.savefig(out/'two-links.png',dpi=160);plt.close(fig)
    data={'status':'passed','vertices':[list(v) for v in vertices],'edges':[{'id':list(k),'endpoints':[list(x) for x in value]} for k,value in edges.items()],'faces':faces,'U':U,'V':V,'face_classes':counts,'scope':'Independent geometry for the presentation, checked against the frozen six-face contract; signed-word and integral proofs are in C2.'}
    (HERE/'figure-two-links.json').write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'status':'passed','vertices':18,'edges':33,'faces':20,'affected':6}))
if __name__=='__main__':main()
